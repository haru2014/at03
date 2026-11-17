"""
src/mac.py
외부 라이브러리(NumPy 등) 없이 반복문으로 구현된 MAC (Multiply-Accumulate) 연산 모듈
"""


def mac(pattern, filt):
    """
    2차원 배열의 입력 패턴과 필터를 같은 위치끼리 곱하여 누적 합산한 MAC 점수를 반환합니다.
    - 시간 복잡도: O(N²)
    """
    total = 0.0
    n = len(pattern)
    for i in range(n):
        for j in range(n):
            total += pattern[i][j] * filt[i][j]
    return total


def mac_1d(pattern_1d, filt_1d):
    """
    길이 N²의 1차원 리스트에 대한 단일 반복문 MAC 연산 (보너스 과제 1 최적화)
    - 중첩 루프 오버헤드를 줄인 단일 반복문 구현
    """
    total = 0.0
    length = len(pattern_1d)
    for i in range(length):
        total += pattern_1d[i] * filt_1d[i]
    return total
