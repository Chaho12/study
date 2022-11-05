Go 언어에서 사용하는 가비지 컬렉터의 개념과 작동방식을 살펴본다. 
또한 Go 프로그램에서 C 코들르 호출하는 방법도 소개한다. (skip)

## Go 컴파일러

Go 컴파일러는 go 커맨드로 실행한다. 이 커맨드는 단순히 실행 파일을 생성하는데 그치지 않고 상당히 많은 작업을 한다

Go 언어로 작성된 소스 파일을 컴파일하려면 go tool compile 커맨드를 실행한다. 그러면 오브젝트 파일이 생성되며 확장자는 `.o`이다. 

```bash
go tool compile unsafe.go 

ls -l unsafe.o  
-rw-r--r--  1 user  staff   9.2K 11  5 15:59 unsafe.o

file unsafe.o # go 버전 때문에 책과 다르게 아카이블 파일
unsafe.o: current ar archive

# 아카이브 파일이란 일종의 바이너리 파일로서 여러 파일을 하나의 파일로 묶을 때 사용한다.
ar t unsafe.o 
__.PKGDEF
_go_.o
```

go tool compile 에서 `-race`를 사용할수 있고 이는 race condition을 감지할 수 있다. 자세한건 10장 'Go 언어의 동시성'를 확인바란다.

## 가비지 컬렉션

보다 자세한 Go GC 가이드는 문서 참고 - https://tip.golang.org/doc/gc-guide

Garbage Collection (aㅔ모리 재활용)이란 더 이상 사용하지 않는 메모리 공간을 해제하는 프로세스다. 다시 말해 가비지 컬렉터는 현재 scope(유효 범위)를 벗어난 오브젝트를 발견하고, 이를 더 이상 참조할 일이 없다고 판단하면 그 공간을 해제한다. 
[mgc.go](https://go.dev/src/runtime/mgc.go) 공식 문서를 보면 다음과 같이 구현했다고 한다.

> The GC runs concurrently with mutator threads, is type accurate (aka precise), allows multiple
> GC thread to run in parallel. It is a concurrent mark and sweep that uses a write barrier. It is
> non-generational and non-compacting. Allocation is done using size segregated per P allocation
> areas to minimize fragmentation while eliminating locks in the common case.

한글로 해석하면
> GC는 뮤테이터 스레드와 함께 동시에 실행되며, 타입을 엄격히 따지고 여러 GC 스레들르 병렬로 실행할 수 있다.
> 쓰기 장벽을 사용하는 표시 후 쓸어 담기 알고리즘의 동시성 버전으로, 비세대형, 비압축형 방식이다.
> 할당 작업은 잠김 현상이 발생하지 않으면서 단편화를 최소화하도록 P 할당 영역마다 분리한 크기로 처리한다.

```go
// gColl.go
package main

import (
	"fmt"
	"runtime"
	"time"
)

// 가비지 컬렉션 통계에 대한 최신 정보를 조회하려면 매번 해당 함수를 호출해야 한다.
func printStats(mem runtime.MemStats) {
	runtime.ReadMemStats(&mem) 
	fmt.Println("mem.Alloc:", mem.Alloc)
	fmt.Println("mem.TotalAlloc:", mem.TotalAlloc)
	fmt.Println("mem.HeapAlloc:", mem.HeapAlloc)
	fmt.Println("mem.NumGC:", mem.NumGC)
	fmt.Println("-----")
}

func main() {
	var mem runtime.MemStats
	printStats(mem)

    // for 루프문을 통해 여러 개의 거대한 Go slice를 생성했다. 이를 통해서 방대한 양의 메모리를 할당했다가 가비지 컬렉터를 호출할 것이다.
	for i := 0; i < 10; i++ {
		s := make([]byte, 50000000)
		if s == nil {
			fmt.Println("Operation failed!")
		}
	}
	printStats(mem)

    // Go slice로 더 많은 메모리를 할당한다.
	for i := 0; i < 10; i++ {
		s := make([]byte, 100000000)
		if s == nil {
			fmt.Println("Operation failed!")
		}
		time.Sleep(5 * time.Second)
	}
	printStats(mem)
}

/**
$ go run gColl.go
mem.Alloc: 126376
mem.TotalAlloc: 126376
mem.HeapAlloc: 126376
mem.NumGC: 0
-----
mem.Alloc: 50125128
mem.TotalAlloc: 500175272
mem.HeapAlloc: 50125128
mem.NumGC: 9
-----

mem.Alloc: 123448
mem.TotalAlloc: 1500258256
mem.HeapAlloc: 123448
mem.NumGC: 20
-----
```

가비지 컬렉터의 작동 과정을 다소 느릿한 애플리케이션을 통해 살펴봄으로써 향후 많은 시간ㅇ르 절약 할 수 있다. 

Go 가비지 컬렉터의 작동 과정을 보다 상세하게 출력하려면 다음과 같이실행한다.

```bash
# GODEBUG=gctrace=1 go run gColl.go
gc 1 @0.008s 3%: 0.010+1.3+0.10 ms clock, 0.080+0.93/0.60/0+0.85 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 2 @0.015s 2%: 0.059+0.38+0.004 ms clock, 0.47+0.27/0.26/0.016+0.035 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 3 @0.033s 1%: 0.032+0.32+0.006 ms clock, 0.26+0.11/0.35/0.56+0.049 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 4 @0.046s 1%: 0.028+0.24+0.010 ms clock, 0.22+0.090/0.34/0.25+0.082 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 5 @0.058s 1%: 0.028+0.36+0.009 ms clock, 0.22+0.11/0.42/0.67+0.078 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 6 @0.078s 2%: 0.44+1.8+0.12 ms clock, 3.5+0.54/2.0/0+0.99 ms cpu, 4->4->1 MB, 5 MB goal, 8 P
gc 7 @0.086s 2%: 0.095+0.41+0.020 ms clock, 0.76+0.078/0.50/0.35+0.16 ms cpu, 4->4->1 MB, 5 MB goal, 8 P
gc 8 @0.087s 2%: 0.032+0.28+0.001 ms clock, 0.25+0.063/0.39/0.30+0.013 ms cpu, 4->4->0 MB, 5 MB goal, 8 P
gc 9 @0.090s 2%: 0.077+0.67+0.001 ms clock, 0.62+0.11/0.38/0.032+0.015 ms cpu, 4->5->1 MB, 5 MB goal, 8 P
gc 10 @0.092s 2%: 0.060+0.68+0.002 ms clock, 0.48+0.17/0.70/0.18+0.019 ms cpu, 4->4->1 MB, 5 MB goal, 8 P
# command-line-arguments
gc 1 @0.000s 9%: 0.003+0.76+0.001 ms clock, 0.028+0.064/0.93/0.10+0.015 ms cpu, 4->7->5 MB, 5 MB goal, 8 P
gc 2 @0.004s 5%: 0.003+0.63+0.007 ms clock, 0.026+0/1.1/0.072+0.058 ms cpu, 9->9->8 MB, 11 MB goal, 8 P
gc 3 @0.025s 1%: 0.023+0.69+0.006 ms clock, 0.18+0.056/0.95/0.74+0.053 ms cpu, 15->15->9 MB, 17 MB goal, 8 P
mem.Alloc: 127864
mem.TotalAlloc: 127864
mem.HeapAlloc: 127864
mem.NumGC: 0
-----
gc 1 @0.000s 2%: 0.002+0.058+0.001 ms clock, 0.017+0.037/0.046/0.037+0.010 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 2 @0.004s 0%: 0.022+0.079+0.001 ms clock, 0.17+0.034/0.049/0.013+0.014 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 3 @0.008s 1%: 0.022+0.094+0.002 ms clock, 0.18+0.055/0.043/0.024+0.017 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 4 @0.009s 1%: 0.017+0.090+0.001 ms clock, 0.13+0.037/0.047/0.033+0.009 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 5 @0.010s 1%: 0.021+0.089+0.002 ms clock, 0.17+0.031/0.066/0+0.017 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 6 @0.011s 1%: 0.018+0.076+0.001 ms clock, 0.14+0.039/0.057/0.017+0.011 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 7 @0.012s 1%: 0.016+0.067+0.002 ms clock, 0.13+0.042/0.033/0.003+0.017 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 8 @0.013s 1%: 0.017+0.058+0.001 ms clock, 0.13+0.024/0.043/0.013+0.010 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
gc 9 @0.014s 1%: 0.015+0.063+0.001 ms clock, 0.12+0.037/0.048/0.026+0.013 ms cpu, 47->47->0 MB, 48 MB goal, 8 P
mem.Alloc: 50124952
mem.TotalAlloc: 500176776
mem.HeapAlloc: 50124952
mem.NumGC: 9
-----
gc 10 @0.015s 1%: 0.017+0.59+0.012 ms clock, 0.13+0.025/0.058/0.009+0.096 ms cpu, 47->143->95 MB, 48 MB goal, 8 P
gc 11 @5.017s 0%: 0.043+0.20+0.005 ms clock, 0.34+0/0.20/0.14+0.041 ms cpu, 190->190->0 MB, 191 MB goal, 8 P
gc 12 @10.038s 0%: 0.028+0.20+0.003 ms clock, 0.23+0/0.19/0.067+0.028 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 13 @15.050s 0%: 0.049+0.11+0.003 ms clock, 0.39+0/0.16/0.084+0.030 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 14 @20.062s 0%: 0.031+0.11+0.006 ms clock, 0.25+0/0.16/0.085+0.048 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 15 @25.074s 0%: 0.035+0.14+0.006 ms clock, 0.28+0/0.19/0.10+0.052 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 16 @30.084s 0%: 0.031+0.12+0.005 ms clock, 0.25+0/0.16/0.068+0.047 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 17 @35.096s 0%: 0.035+0.11+0.008 ms clock, 0.28+0/0.18/0.13+0.071 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 18 @40.106s 0%: 0.038+0.18+0.005 ms clock, 0.30+0/0.22/0.13+0.043 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
gc 19 @45.113s 0%: 0.025+0.13+0.025 ms clock, 0.20+0/0.11/0.014+0.20 ms cpu, 95->95->0 MB, 96 MB goal, 8 P
mem.Alloc: 123368
mem.TotalAlloc: 1500259864
mem.HeapAlloc: 123368
mem.NumGC: 19
-----
```
가비지 컬렉션 프로세스가 진행되는 동안 할당된 힙 크기를 보다 자세히 알 수 있다. 예를 들어 `95->95->0 MB`라고 표현된 부분을 보자.
여기서 첫 번째 숫자는 가비지 컬렉터가 실행될 시점의 힙 크기다. 두 번째 값은 가비지 컬렉터가 실행을 마칠 시점의 힙 크기다.
마지막 값은 현재 힙 크기이다.

### 삼색(tricolor) 알고리즘

Go 언어의 가비지 컬렉터는 삼색 알고리즘에 따라 작동한다.

