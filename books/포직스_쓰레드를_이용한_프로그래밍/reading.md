# 주요 키포인트 정리

간단히 skim하는 정도로 읽었다. 코딩보단 개념에 대해 집중했다.

pthread란 POSIX Thread의 약자로 유닉스계열 POSIX시스템에서 병렬적으로 작동하는 소프트웨어를 작성하기 위하여 제공하는 API입니다. 즉 스레드를 편하게 만들수 있게 도와주는 API.

POSIX 쓰레드에서 기본적인 동기화 모텔은 보호를 위해 뮤텍스를 사용하거나 통신을 위해 조건변수를 사용하는 것이다. 또한 세마포어, 파이표, 메시지 큐와 같은 다른 동기화 방법을 사용할 수 있다. 뮤텍스는 쓰레드가 공유 데이터를 사용하는 동안 다른 쓰레드가 이를 빙해 하지 못하도록 공유 데이터를 잡글 수 있게 해준다. 조건변수는 공유데이터가 특정한 상태, 측 “큐가 가득 갔다”거나 “자원이 사용 가능하다”와 같은 상태가 될 때까지 쓰레드가 기다릴 수 있도록 해준다.

## 개념 정리

### 병렬성(parallelism) vs 병행성 (concurrency)

병렬성은 정확한 의미로는 오직 다중프로세서 시스템에서만 가능하다. 그러나 병행성은 단 일프로세서와 다중프로세서 시스템 모두에서 가능하다.
병행성은 본질적으로 병렬성을 흉내 낸 것이므로 단일프로세서에서 동작이 가능하다. 병렬성은 프로그램이 동시에 두 가지 계산을하도록 요구하지만, 병행성은 단지 두가지 일이 동시에 발생하는것처럼 보이게끔해준다.
왜냐하면 표로세서가 하나이므로 한 번에 단 하나의 작업만 처리할 수 있기 때문이다.

다중프로세서 시스템에서 쓰레드를 사용하면 동시에 하나 이상의 독립적인 계산을 수행할 수 있다. 쓰레드를 이용한 계산 위주의 애플리케이션은 두 개의 프로세서를 이용하면 전통 적인 하나의 쓰레드를 이용하는 방법보다 거의 두 배의 속도를 낼 수 있다. 쓰레드 간에 동기화를 하는 데 시간이 조금 걸리기 때문이다. 이런 효과를 보통 “조정율(scaling)"이라 한다.
조정율은 항상 프로세서의 수가 증가할수록 떨어지는데, 프로세스가 증가하면 할수록 잠금을 기다 려야 하거나 메모리 충돌이 일어날 확률이 높아져서 시간이 더 걸리기 때문이다

속도 증가율 (암달의 법칙): 1/ ((1-p) + p/n)

- n : 프로세스 수
- p : 병렬적인 코드 여부

### Thread-safe 함수, Reentrant 함수

#### Thread-safe

여러 Thread에서 동시에 실행해도 문제 없는 함수를 의미한다. 여러 Thread가 같은 함수를 동시에 실행할 경우 가장 큰 문제는 함수가 이용하는 Thread간 공유자원이다. 공유자원을 Lock같은 동기화 기법으로 보호하여 공유 자원의 무결성을 보장해야한다. 이렇게 공유 자원의 무결성을 보장하는 함수를 Thread-safe 함수라고 한다. Thread-safe 함수는 Thread간 공유자원을 이용할 수도 있기 때문에 각 Thread가 Thread-safe 함수를 호출하는 시간에 따라 호출 결과가 달라질 수 있다.

```c++
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int global_var = 0;

int thread_safe_function()
{
    pthread_mutex_lock(&mutex);
    ++global_var;
    pthread_mutex_unlock(&mutex);
    return global_var;
}
```

#### Reentrant

Thread-safe 함수와 마찬가지로 여러 Thread에서 동시에 실행이 가능하지만 Thread간 공유 자원를 이용하지 않는 함수를 의미한다. 공유 변수를 이용하지 않기 때문에 각 Thread는 언제나 같은 호출 결과를 얻을 수 있다. 이러한 성질을 Reentrancy(재진입 가능한) 하다라고 표현하기 때문에 Reentrant 함수라고 한다. Reentrant 함수는 Thread-safe 함수이지만 Thread-safe 함수는 Reentrant 함수라고 말할 수 없다.

```c++
int reentrant_function()
{
    int local_var = 0;
    ++local_var;
    return global_var;
}
```

출처: https://ssup2.github.io/theory_analysis/Thread-safe_함수_Reentrant_함수/

### Mutex, Semaphore

뮤텍스: 한 쓰레드, 프로세스에 의해 소유될 수 있는 Key🔑를 기반으로 한 상호배제기법
세마포어: Signaling mechanism. 현재 공유자원에 접근할 수 있는 쓰레드, 프로세스의 수를 나타내는 값을 두어 상호배제를 달성하는 기법
두 기법 모두 완벽한 기법은 아니다. 이 기법들을 쓰더라도 데이터 무결성을 보장할 수 없으며 데드락이 발생할 수도 있다. 하지만 상호배제를 위한 기본적인 기법이며 여기에 좀 더 복잡한 매커니즘을 적용해 꽤나 우아하게 동작하는 프로그램을 짤 수 있다.

출처: https://worthpreading.tistory.com/90



______

현재 2장 시작