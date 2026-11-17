"""
src/mode_input.py
모드 1: 3×3 콘솔 직접 입력 모드 구현
- 3×3 필터 A, B와 패턴 입력
- 잘못된 입력(열 개수 부족, 문자 등) 예외 처리 및 재입력 안내
- MAC 점수 계산, 판정, 성능 분석 출력
"""

from src.mac import mac
from src.judge import judge_mode1
from src.perf import measure_mac_ms

ERR_COUNT = "오류: 한 줄에 정확히 %d개의 숫자를 공백으로 구분하여 입력해야 합니다. 다시 입력해 주세요."
ERR_NUMBER = "오류: 유효한 숫자가 아닙니다. 숫자만 입력해 주세요."


def parse_number(val_str):
    """
    문자열을 숫자로 변환합니다. 정수 형태는 float(x)로 변환해 일관된 float 리스트를 구성합니다.
    """
    return float(val_str)


def read_matrix(name, n=3):
    """
    사용자로부터 n×n 크기의 2차원 리스트를 행 단위로 입력받습니다.
    잘못된 입력(열 개수 불일치, 숫자가 아닌 값) 발생 시 안내 문구를 출력하고
    해당 행렬을 처음부터 다시 입력받습니다.
    """
    print(f"\n{name} ({n}×{n})를 한 줄씩 입력하세요. 예: {' '.join(['0'] * n)}")
    while True:
        rows = []
        ok = True
        for i in range(n):
            try:
                line = input(f"{i + 1}행: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n입력이 취소되었습니다.")
                return None

            parts = line.split()
            if len(parts) != n:
                print(ERR_COUNT % n)
                ok = False
                break

            try:
                row = [parse_number(p) for p in parts]
                rows.append(row)
            except ValueError:
                print(ERR_NUMBER)
                ok = False
                break

        if ok:
            print(f"{name} 저장 완료: {rows}")
            return rows
        print("처음부터 다시 입력해 주세요.\n")


def run_mode_input():
    """모드 1의 전체 실행 흐름을 관장합니다."""
    # 1. 필터 A 입력
    filter_a = read_matrix("필터 A", 3)
    if filter_a is None:
        return

    # 2. 필터 B 입력
    filter_b = read_matrix("필터 B", 3)
    if filter_b is None:
        return

    # 3. 패턴 입력
    pattern = read_matrix("패턴", 3)
    if pattern is None:
        return

    # 4. MAC 연산 및 시간 측정 (순수 연산 시간만 10회 반복 측정)
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    time_a = measure_mac_ms(pattern, filter_a, repeat=10)
    time_b = measure_mac_ms(pattern, filter_b, repeat=10)

    # 5. 판정 (A / B / 판정 불가)
    decision = judge_mode1(score_a, score_b)

    # 6. 결과 출력
    print("\n[결과]")
    print(f"필터 A 점수: {score_a:.1f}  (평균 {time_a:.4f} ms)")
    print(f"필터 B 점수: {score_b:.1f}  (평균 {time_b:.4f} ms)")
    print(f"판정: {decision}\n")

    # 7. 3×3 성능 분석 표 출력
    avg_3x3 = (time_a + time_b) / 2.0
    print("[성능 분석] (각 크기 10회 반복 평균)")
    print(f"{'크기(N×N)':<12}{'평균 시간(ms)':<16}{'연산 횟수(N²)':<12}")
    print(f"{'3x3':<12}{avg_3x3:<16.4f}{9:<12}")
    print()
