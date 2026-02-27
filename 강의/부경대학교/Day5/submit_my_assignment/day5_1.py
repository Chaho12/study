from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from datetime import datetime

def validate_data(df, stage_name):
    """데이터 품질 검증"""
    print(f"\n🔍 Validating {stage_name}...")

    row_count = df.count()
    col_count = len(df.columns)
    # print(f"    Rows: {row_count}, Columns: {col_count}")

    null_counts = df.select([
        F.sum(F.col(c).isNull().cast("int")).alias(c)
        for c in df.columns
    ])
    # print(f"    Null values:")
    null_counts.show(truncate=False)

    duplicate_count = row_count - df.dropDuplicates().count()
    if duplicate_count > 0:
        print(f"    ⚠️  Found {duplicate_count} duplicate rows")
    else:
        print(f"    ✅ No duplicates")

    return row_count > 0


def run_ecommerce_analytics_sql_pipeline(input_path, output_base_path):
    """
    요구사항:
      - HDFS CSV -> DF
      - 4가지 분석 (카테고리/시간대/퍼널/유저행동) : spark.sql 사용
      - 각 결과 Parquet로 별도 디렉토리 저장
      - 저장된 Parquet 재로딩 후 샘플 출력
    """
    try:
        print("🚀 Starting Ecommerce Analytics Pipeline (spark.sql)...")

        spark = SparkSession.builder \
            .appName("Ecommerce Analytics (SQL)") \
            .master("spark://spark-master:7077") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("WARN")

        # -------------------------
        # [1/4] Extract
        # -------------------------
        print(f"\n📥 [1/4] Extracting data from HDFS...")
        print(f"    Input: {input_path}")

        raw_df = spark.read.csv(input_path, header=True, inferSchema=True)

        # 입력 검증
        if not validate_data(raw_df, "Input Data (Raw CSV)"):
            raise ValueError("Input data validation failed: No data found")

        # timestamp 파싱 + 기본 정제 (SQL 분석 편의)
        df = raw_df.withColumn("event_ts", F.to_timestamp("timestamp", "yyyy-MM-dd HH:mm:ss")) \
                   .withColumn("hour", F.hour("event_ts")) \
                   .withColumn(
                       "revenue",
                       F.when(F.col("event_type") == "purchase",
                              (F.col("price").cast("double") * F.col("quantity").cast("long"))
                             ).otherwise(F.lit(0.0))
                   )

        if df.filter(F.col("event_ts").isNull()).count() > 0:
            print("\n⚠️  Found rows with unparsable timestamp (event_ts is NULL). Sample:")
            df.filter(F.col("event_ts").isNull()).show(10, truncate=False)
            # 필요하면 여기서 실패 처리할 수도 있음
            # raise ValueError("Timestamp parsing failed for some rows")

        if not validate_data(df, "Input Data (Parsed/Enriched)"):
            raise ValueError("Input data validation failed after parsing")

        # SQL을 쓰기 위해 temp view 등록
        df.createOrReplaceTempView("ecommerce_logs")

        # 출력 베이스
        # 요구 경로: hdfs://namenode:8020/user/user/data/processed/ecommerce/2026/02/14/
        out_base = output_base_path.rstrip("/")

        out_category = f"{out_base}/category_stats"
        out_hourly   = f"{out_base}/hourly_activity"
        out_funnel   = f"{out_base}/funnel"
        out_user     = f"{out_base}/user_behavior"

        # -------------------------
        # [2/4] Transform (spark.sql)
        # -------------------------
        print(f"\n🔄 [2/4] Running SQL analytics...")

        # 1) 카테고리별 통계
        category_stats = spark.sql("""
            SELECT
                category,
                COUNT(*)                                   AS event_count,
                COUNT(DISTINCT user_id)                    AS unique_users,
                SUM(CASE WHEN event_type='purchase' THEN revenue ELSE 0 END) AS total_revenue,
                SUM(CASE WHEN event_type='purchase' THEN 1 ELSE 0 END)      AS purchase_count
            FROM ecommerce_logs
            GROUP BY category
            ORDER BY total_revenue DESC, event_count DESC
        """)

        # 2) 시간대별 활동
        hourly_activity = spark.sql("""
            SELECT
                hour,
                COUNT(*)                    AS event_count,
                COUNT(DISTINCT user_id)     AS active_users
            FROM ecommerce_logs
            GROUP BY hour
            ORDER BY hour
        """)

        # 3) 전환율 분석 (view → add_to_cart → purchase)
        # 정의: 전체 로그에서 event_type별 건수(스텝 카운트)
        # 필요하면 "동일 세션 기준 퍼널"로 강화 가능
        funnel = spark.sql("""
            SELECT 
                event_type, count(*) as count
            FROM ecommerce_logs
            GROUP BY event_type
            ORDER BY count(*) DESC
        """)

        # 4) 사용자별 행동
        user_behavior = spark.sql("""
            SELECT
  user_id,
  COUNT(1) AS total_events,
  COUNT(DISTINCT session_id) AS sessions,
  ROUND(SUM(revenue), 2) AS total_spent,
  sort_array(collect_set(CASE WHEN event_type='view' THEN category END)) AS categories_viewed,
  SUM(CASE WHEN event_type='purchase' THEN 1 ELSE 0 END) AS purchase_count
FROM ecommerce_logs
GROUP BY user_id
ORDER BY total_spent DESC, total_events DESC
LIMIT 5
        """)

        # 변환 결과 검증 (각 DF)
        if not validate_data(category_stats, "category_stats"):
            raise ValueError("Transformation validation failed: category_stats is empty")
        if not validate_data(hourly_activity, "hourly_activity"):
            raise ValueError("Transformation validation failed: hourly_activity is empty")
        if not validate_data(funnel, "funnel"):
            raise ValueError("Transformation validation failed: funnel is empty")
        if not validate_data(user_behavior, "user_behavior"):
            raise ValueError("Transformation validation failed: user_behavior is empty")

        # -------------------------
        # [3/4] Load (Parquet)
        # -------------------------
        print(f"\n💾 [3/4] Saving results to HDFS (Parquet)...")
        print(f"    Base Output: {out_base}")

        category_stats.write.mode("overwrite").parquet(out_category)
        hourly_activity.write.mode("overwrite").parquet(out_hourly)
        funnel.write.mode("overwrite").parquet(out_funnel)
        user_behavior.write.mode("overwrite").parquet(out_user)

        # 저장 결과 검증: row count 비교
        print(f"\n🔍 Verifying saved parquet row counts...")
        def verify(saved_path, expected_df, name):
            saved_df = spark.read.parquet(saved_path)
            saved_cnt = saved_df.count()
            expected_cnt = expected_df.count()
            if saved_cnt != expected_cnt:
                raise ValueError(f"Verification failed for {name}: expected {expected_cnt}, got {saved_cnt}")
            print(f"    ✅ {name}: {saved_cnt} rows saved")

        verify(out_category, category_stats, "category_stats")
        verify(out_hourly, hourly_activity, "hourly_activity")
        verify(out_funnel, funnel, "funnel")
        verify(out_user, user_behavior, "user_behavior")

        # -------------------------
        # [4/4] Reload & Report
        # -------------------------
        print(f"\n📊 [4/4] Reloading saved parquet and printing samples...")

        re_category = spark.read.parquet(out_category)
        re_hourly   = spark.read.parquet(out_hourly)
        re_funnel   = spark.read.parquet(out_funnel)
        re_user     = spark.read.parquet(out_user)

        print("\n" + "="*60)
        print("CATEGORY STATS (sample)")
        print("="*60)
        re_category.show(20, truncate=False)

        print("\n" + "="*60)
        print("HOURLY ACTIVITY (sample)")
        print("="*60)
        re_hourly.show(24, truncate=False)

        print("\n" + "="*60)
        print("FUNNEL (full)")
        print("="*60)
        re_funnel.show(truncate=False)

        print("\n" + "="*60)
        print("USER BEHAVIOR (sample)")
        print("="*60)
        re_user.show(20, truncate=False)

        print("\n🎉 Pipeline completed successfully!")
        print("📁 Output locations:")
        print(f"  - {out_category}")
        print(f"  - {out_hourly}")
        print(f"  - {out_funnel}")
        print(f"  - {out_user}")

        return {
            "category_stats": out_category,
            "hourly_activity": out_hourly,
            "funnel": out_funnel,
            "user_behavior": out_user
        }

    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


# 실행 파라미터
input_path = "hdfs://namenode:8020/user/data/raw/ecommerce/2026/02/14/ecommerce_logs.csv"
output_base = "hdfs://namenode:8020/user/data/processed/ecommerce/2026/02/14"

paths = run_ecommerce_analytics_sql_pipeline(input_path, output_base)
print(paths)