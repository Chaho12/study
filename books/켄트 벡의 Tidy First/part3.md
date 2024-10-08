켄트 벡의 Tidy First?: 더 나은 소프트웨어 설계를 위한 32가지

# Part 3 - Theory

## Chapter 23 - Structure and Behavior

Software creates value in two ways:

- What it does today (오늘 하는 일)
  - "오늘날 하는 일"은 급여 계산, 드롭십 주문 발송, 친구 알림 등 시스템의 행동(behaviour)입니다
- The possibility of new things we can make it do tomorrow (우리가 내일 할 수 있는 새로운 것들의 가능성)

행동은 다음 두 가지 방법으로 특징지을 수 있습니다:

- Input/output pairs (입-출력 쌍이 있다)
  - This many hours at this pay rate in this jurisdiction should result in a paycheck like this and a tax filing like that.

- Invariants (불변량, 합은 sum과 같아야한다)
  - The sum of all entitlements should equal the sum of all deductions.

이러한 행동은 가치를 창조

- 컴퓨터는 사람보다 훨씬 빠르게 계산을 할 수 있기 때문에, 사람들이 수작업으로 계산하지 않으려는 대가로 비용을 지불합니다

옵션성

- 시스템의 행동 가능성을 늘리면 사람들은 그 시스템의 현재의 가치보다 더 많은 잠재적 가치를 지닌다고 생각합니다.
- 즉, 시스템이 $100/$10 또는 $20/$1로 변할 수 있는 가능성이 있으면, 그 가능성만으로도 더 많은 가치를 지불할 의향이 생깁니다.
- 시스템의 행동을 바꾸지 않고도, 옵션을 추가함으로써 이미 가치를 높일 수 있습니다.

소프트웨어의 경제적 마법은 `옵션`에 있으며, 특히 `확장 가능성`에 있습니다.

- 1,000대의 차를 만드는 것과 10만 대를 만드는 것에는 차이가 있지만, 1,000개의 알림을 보내는 것과 10만 개를 보내는 것 사이에는 큰 차이가 없습니다.
- 환경이 더 `변동성`이 클수록 `옵션의 가치`는 더 커지며, 이는 혼란을 기회로 삼는 데 도움이 됩니다.

옵션의 가치를 방해하는데 경우의 몇 가지 시나리오가 있습니다.

1. 핵심 직원의 이직으로 인해 변경 작업이 지연됨.
2. 고객과의 거리가 멀어져 피드백 빈도가 줄어듦.
3. 변경 비용이 급등하여 옵션을 자주 사용할 수 없게 됨.

이 책은 첫 두 가지 문제를 직접 다루지는 않지만, 세 번째 문제에 대해서는 대응할 수 있습니다.
시스템의 구조는 행동에 영향을 미치지 않지만, `옵션의 생성`에는 중요합니다.
`좋은 구조`는 `새로운 기능을 추가`하기 쉽게 만들어줍니다.

문제는 구조가 행동과 같은 방식으로 명확하지 않다는 것입니다.
제품 로드맵이 기능 목록으로 되어 있는 이유는 행동 변화가 눈에 띄기 때문입니다.

- 버튼이 새로 생기는 것처럼 행동 변화는 쉽게 확인할 수 있습니다.

그러나 구조에 대한 투자는 유지보수와 확장성에 중요하지만, 구조가 개선되었는지, 코드 변경이 쉬워졌는지 확실히 알기 어렵습니다.

## Chapter 24 - Economics: Time Value and Optionality

30대 중반이 되어서야 돈의 본질을 제대로 이해하지 못했다는 사실을 깨달았습니다.
물건을 사고팔 수 있었고, 돈을 벌 수는 있었지만, 돈의 움직임에 대한 개념은 전혀 이해하지 못했습니다.
프로그래밍을 통해 기본적인 금융 개념을 다루면서 점차 돈에 대한 이해가 깊어졌고, 이는 개발에 대한 제 시각을 변화시켰습니다.
James Buchan은 돈이 미래의 필요를 저장하고 관리하는 방법으로, 즉 “동결된 욕망 - Frozen Desire”을 나타낸다고 설명합니다.
돈의 본질은 프로그래밍 목표와 충돌할 수 있지만, 궁극적으로는 돈이 우선하게 됩니다.
돈에 대한 이해가 깊어지면서 제 프로그래밍 전략도 변화했으며, 금융 논리에 맞는 전략이 더 합리적으로 느껴졌습니다.

이 글에서는 두 가지 중요한 재정 원칙을 소개합니다.

1. 첫째, "오늘의 1달러는 내일의 1달러보다 가치가 있다"는 시간 가치의 원칙입니다. 따라서 가능한 한 빨리 수익을 내고, 지출은 늦추는 것이 좋습니다.
2. 둘째, 불확실한 상황에서는 '물건'보다 '옵션'이 더 중요하다는 원칙입니다. 불확실성에 직면했을 때는 선택지를 늘리는 것이 유리합니다.

그러나 이 두 가지 전략은 때로는 충돌할 수 있습니다. 지금 돈을 벌면 미래의 선택지가 줄어들 수 있고, 반대로 지금 돈을 벌지 않으면 미래에 선택지를 활용할 기회조차 없을 수 있습니다.
만약 순현재가치(NPV)와 옵션의 그릭스(Greeks)에 대해 이미 이해하고 있다면 다음 두 챕터는 건너뛰어도 됩니다. 그러나 이 용어들이 생소하다면 계속 읽으면서 금융 용어에 대한 기본적인 이해를 쌓아가야 합니다.
이후 소프트웨어 설계가 어떻게 '빨리 벌고 늦게 쓰기'와 '옵션을 만들고 물건을 만들지 않기'라는 원칙들을 조화시킬 수 있는지에 대해 논의할 것입니다.

## Chapter 25 -  A Dollar Today > A Dollar Tomorrow

돈의 가치가 **"언제"**와 **"얼마나 확실한가"**에 따라 달라집니다.

- 오늘 1달러를 받으면 즉시 사용할 수 있거나 투자할 수 있지만, 내일 받기로 한 1달러는 현재 가치가 더 낮습니다.
- 이는 내일 받을 돈을 지금 사용할 수 없고, 투자할 수 없으며, 받을 가능성도 100% 확실하지 않기 때문입니다.
- 따라서 모든 돈은 동일하게 평가되지 않으며, 특정 날짜에 따라 가치를 달리해야 합니다.

이 원칙을 소프트웨어 시스템의 가치 평가에 적용하면, 시스템의 코드 양이나 복잡도는 중요하지 않고, 구매자가 지불해야 할 합리적인 금액은
시스템이 **언제**, **얼마나** 확실하게 수익을 창출할 수 있는지에 달려 있다는 점이 강조됩니다.

예를 들어, 10년 동안 1,000만 달러를 들여 2,000만 달러를 벌어들이는 시스템과 1,000만 달러를 들여 1,200만 달러를 벌어들이는 시스템 중에서 더 매력적인 것은 무엇일까요?

- 이 질문의 핵심은 "언제" 돈이 들어오고 나가는지를 고려해야 한다는 것입니다.

만약 오늘 1,000만 달러를 투자해 10년 후에 2,000만 달러를 받는 것과, 오늘 1,200만 달러를 받고 10년 후에 1,000만 달러를 지불하는 두 가지 시나리오를 비교

- 첫 번째는 긴장감을 주지만 두 번째는 즉시 이익이 보장되기 때문에 더 매력적입니다.
- 따라서, 소프트웨어 개발에서도 **"먼저 돈을 벌고 나중에 정리하는"** 전략이 유리할 수 있습니다.

마지막으로, 이 책에서는 시간 가치 외에도 **"옵션 가치"**라는 개념을 소개할 예정이며, 이 두 가지가 종종 충돌할 수 있다고 합니다.

## Chapter 26 - Options

> Option 이란, 주식 옵션에서 개념과 같은거로 투자자가 미래에 정해진 날짜(만기일)와 정해진 가격(행사가격)에 주식을 사거나 팔 수 있는 권리를 사는 것을 의미합니다.

이전 장에서는 소프트웨어 시스템의 `경제적 가치`를 할인된 `미래 현금 흐름의 합`으로 모델링했습니다. 우리는 다음과 같이 이러한 흐름을 변화시킴으로써 가치를 창출합니다:

- 더 많은 돈을 더 빨리, 더 높은 확률로 벌기
- 돈을 덜 쓰고, 더 나중에, 더 낮은 확률로 쓰기

즉,  소프트웨어 설계자는 설계를 적절한 시점에 맞춰 진행해야 하며, 선택 가능성도 중요한 가치 요소로 다뤄집니다.
과거 월스트리트에서 옵션 가격 책정과 관련된 경험을 통해 소프트웨어 설계에 대한 새로운 직관을 얻게 되었습니다.

- 월트리트에서 거래 소프트웨어와 함께 일하면서 옵션 가격 책정에 대해 공부하게 되었습니다.
- 당시 테스트 주도 개발(TDD)을 막 발명했었고, 연습 주제를 찾고 있었습니다.
- 옵션 가격 책정이 복잡한 알고리즘을 포함하며 정답이 있는 좋은 예시라고 생각했습니다.
- 옵션 가격 책정 공식을 먼저 테스트하며 구현하는 과정에서 부동 소수점 숫자를 비교할 때 필요한 엡실론의 필요성을 발견했습니다.

이 과정에서 옵션에 대한 직관을 개발하게 되었고, 이는 소프트웨어 설계에 대한 제 일반적인 사고방식에 영향을 미치기 시작했습니다.

다양한 알고리즘을 설명/구현 할순 없지만, 그 과정에서 배운 교훈을 공유합니다. 핵심은 다음과 같습니다:

- "다음에 어떤 기능을 구현할 수 있는가?"라는 질문 자체가 이미 가치를 지니고 있으며, 이는 실제로 구현하기 전에도 중요합니다.
  - 과거에는 `완료된 작업`에 대해 보상(연봉)을 받는다고 생각했지만, 실제로는 `앞으로 할 수 있는 일`에 대한 `가치`를 인정받고 있었습니다.
- 이러한 "다음에 구현할 기능"이 많을수록, 그리고 그 기능들이 가치 있을수록 더 큰 가치를 창출합니다.
- 어떤 기능이 가장 가치 있을지 예측할 수는 없지만, 중요한 것은 이를 구현할 수 있는 선택권을 유지하는 것입니다.
- 예측이 불확실할수록, 선택권의 가치는 커집니다. 변화에 적응하면, 전통적인 소프트웨어 개발이 실패할 수 있는 상황에서도 더 큰 가치를 창출할 수 있습니다.

이후 저자는 금융 옵션의 개념을 설명하며, 특정 상황에서 선택권의 가치가 어떻게 결정되는지 예시로 설명합니다.
이를 통해 불확실성 속에서 선택권의 중요성과 가치를 강조합니다.

## Chapter 27 - Options Versus Cash Flows

> 돈을 쓴다 -> 개발하는데 시간을 투자한다

이 내용에서 "tidy first?(정리 먼저?)"라는 질문은 경제적 관점에서 매우 흥미로운 논쟁을 불러일으킵니다. 여기서 다루는 두 가지 주요 관점은 다음과 같습니다:

1. 할인된 현금 흐름(Discounted Cash Flow, DCF): 이 접근법에 따르면, 돈을 더 빨리 벌고, 돈을 쓰는 시점은 `최대한 늦추`는 것이 바람직합니다.

    - 따라서 먼저 정리하는 것은 돈을 일찍 쓰고 나중에 벌게 되는 셈이므로, 정리를 나중에 하거나 아예 하지 말라는 조언이 될 수 있습니다.

2. 옵션(Options): 반면, 옵션 이론에서는 지금 돈을 써서 나중에 더 큰 이익을 얻을 수 있는 선택지를 만들어야 한다고 말합니다.

    - 이 경우, 정리 작업이 새로운 선택지를 만들어 낸다면, 정리를 우선적으로 하는 것이 바람직합니다.

따라서, 정리를 먼저 할지 말지는 상황에 따라 다릅니다.

아래 처럼 어떤 경우에는 정리를 먼저 하는 것이 합리적일 수 있지만

> cost(tidying) + cost(behavior change after tidying) < cost(behavior change without tidying)

정리 비용이 이후 변화에 들어가는 비용보다 클 경우, 경제적으로 손해를 볼 수 있습니다.

> cost(tidying) + cost(behavior change after tidying) > cost(behavior change without tidying)

결국, 정리 여부의 판단은 상황에 따라 달라지며, 이는 개인이나 팀의 판단력에 크게 의존하게 됩니다.

## 논의 포인트

1. "다음에 어떤 기능을 구현할 수 있는가?"라는 질문이 실제 구현 전에도 가치를 가지는 이유는 무엇일까? 이 개념이 소프트웨어 개발의 우선순위 설정에 어떤 영향을 미칠 수 있을까? 관련 경험이 있는가?
2. 실제로 완성된 작업이 아닌, 향후 작업의 가능성에 대한 보상을 받은 적이 있는가? 이를 고려해서 개발한 적이 있는가?

마지막으로, 나의 가치가 무엇인가에 대해 생각해보자.
특히 면접자가 아닌 면접관 입장으로써 어떤 가치를 보고 뽑는지 생각해보자.

> 과거에는 `완료된 작업`에 대해 보상(연봉)을 받는다고 생각했지만, 실제로는 `앞으로 할 수 있는 일`에 대한 `가치`를 인정받고 있었습니다.
