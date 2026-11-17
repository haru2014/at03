"""
src/perf.py
time.perf_counter 기반 MAC 연산 성능 측정 및 분석 모듈
"""

import time
from src.mac import mac, mac_1d
from src.matrix import make_cross, make_x, flatten_matrix

DEFAULT_REPEAT = 10


def measure_mac_ms(pattern, filt, repeat=DEFAULT_REPEAT):
    """
    단일 MAC 함수 호출의 실행 시간을 측정합니다.
    - I/O(입력, 출력 등)를 제외하고 mac() 호출 구간만 감싸서 측정
    - repeat 회 반복 측정 후 평균 시간(ms)을 반환
    """
    elapsed = 0.0
    for _ in range(repeat):
        t0 = time.perf_counter()
        mac(pattern, filt)
        elapsed += time.perf_counter() - t0
    return (elapsed / repeat) * 1000.0


def measure_mac_1d_ms(pattern_1d, filt_1d, repeat=DEFAULT_REPEAT):
    """
    1차원 배열 MAC 연산의 실행 시간을 측정합니다 (ms 단위 반환).
    """
    elapsed = 0.0
    for _ in range(repeat):
        t0 = time.perf_counter()
        mac_1d(pattern_1d, filt_1d)
        elapsed += time.perf_counter() - t0
    return (elapsed / repeat) * 1000.0


def run_benchmark(sizes=(3, 5, 13, 25), repeat=DEFAULT_REPEAT):
    """
    지정된 크기(N×N)들에 대해 성능 측정을 수행하고 결과를 반환합니다.
    반환 형식: [ {"size": N, "ops": N*N, "avg_ms": float}, ... ]
    """
    results = []
    for n in sizes:
        p = make_cross(n)
        f = make_cross(n)
        avg_ms = measure_mac_ms(p, f, repeat=repeat)
        results.append({
            "size": n,
            "size_str": f"{n}x{n}",
            "ops": n * n,
            "avg_ms": avg_ms
        })
    return results


def print_benchmark_table(results, title="[성능 분석] (각 크기 10회 반복 평균)"):
    """
    성능 분석 결과를 콘솔 표 형태로 출력합니다.
    """
    print(title)
    print(f"{'크기(N×N)':<12}{'평균 시간(ms)':<16}{'연산 횟수(N²)':<12}")
    for item in results:
        print(f"{item['size_str']:<12}{item['avg_ms']:<16.4f}{item['ops']:<12}")
    print()


def run_comparison_benchmark(sizes=(3, 5, 13, 25), repeat=DEFAULT_REPEAT):
    """
    2차원 MAC 연산과 1차원 최적화 MAC 연산의 비교 벤치마크 (보너스 과제 1)
    """
    results = []
    for n in sizes:
        p_2d = make_cross(n)
        f_2d = make_cross(n)
        p_1d = flatten_matrix(p_2d)
        f_1d = flatten_matrix(f_2d)

        ms_2d = measure_mac_ms(p_2d, f_2d, repeat=repeat)
        ms_1d = measure_mac_1d_ms(p_1d, f_1d, repeat=repeat)
        speedup = ms_2d / ms_1d if ms_1d > 0 else 1.0

        results.append({
            "size_str": f"{n}x{n}",
            "ops": n * n,
            "ms_2d": ms_2d,
            "ms_1d": ms_1d,
            "speedup": speedup
        })
    return results
