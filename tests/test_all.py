"""
tests/test_all.py
미션 개발 계획서 7단계 (T01~T12) 전체 검증 테스트 스크립트
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.matrix import make_matrix, make_cross, make_x, is_square
from src.mac import mac, mac_1d
from src.judge import EPSILON, normalize_label, judge, judge_mode1
from src.perf import measure_mac_ms, run_benchmark
from src.mode_json import run_case, load_data, parse_size_from_key


def run_tests():
    print("=== T01 ~ T12 미션 필수 테스트 시작 ===")
    passed = 0
    total = 12

    # T01: 3x3 십자가 패턴 입력 -> Cross 필터 점수가 높음
    c3 = make_cross(3)
    x3 = make_x(3)
    s_c = mac(c3, c3)
    s_x = mac(c3, x3)
    assert s_c == 5.0 and s_x == 1.0 and judge(s_c, s_x) == "Cross", "T01 실패"
    print("✓ T01 통과: 3x3 십자가 입력 시 Cross 점수(5.0)가 X 점수(1.0)보다 높음")
    passed += 1

    # T02: 3x3 X 패턴 입력 -> X 필터 점수가 높음
    s_c = mac(x3, c3)
    s_x = mac(x3, x3)
    assert s_c == 1.0 and s_x == 5.0 and judge(s_c, s_x) == "X", "T02 실패"
    print("✓ T02 통과: 3x3 X 입력 시 X 점수(5.0)가 Cross 점수(1.0)보다 높음")
    passed += 1

    # T03: 필터 점수가 완전히 같음 -> UNDECIDED
    assert judge(3.0, 3.0) == "UNDECIDED", "T03 실패"
    print("✓ T03 통과: 필터 점수가 완전히 같으면 UNDECIDED 판정")
    passed += 1

    # T04: 점수 차이가 epsilon 미만 -> UNDECIDED
    diff_val = EPSILON / 2
    assert judge(10.0, 10.0 + diff_val) == "UNDECIDED", "T04 실패"
    print("✓ T04 통과: 점수 차이가 epsilon 미만이면 UNDECIDED 판정")
    passed += 1

    # T05: 2차원 리스트 생성 및 정사각 검증 (입력 숫자 개수 유효성 기반)
    m = make_matrix(3)
    assert is_square(m, 3) is True and is_square([[1, 2]], 3) is False, "T05 실패"
    print("✓ T05 통과: 행렬 열/행 개수 불일치 검증 정상 동작")
    passed += 1

    # T06: 숫자 변환 실패 검증
    try:
        float("abc")
        val_error = False
    except ValueError:
        val_error = True
    assert val_error is True, "T06 실패"
    print("✓ T06 통과: 비숫자 입력 시 ValueError 예외 처리 검증")
    passed += 1

    # T07: JSON 라벨 '+' 입력 -> Cross로 변환
    assert normalize_label("+") == "Cross" and normalize_label("cross") == "Cross", "T07 실패"
    print("✓ T07 통과: '+' 및 'cross' 라벨이 'Cross'로 정규화됨")
    passed += 1

    # T08: JSON 라벨 'x' 입력 -> X로 변환
    assert normalize_label("x") == "X" and normalize_label("X") == "X", "T08 실패"
    print("✓ T08 통과: 'x' 및 'X' 라벨이 'X'로 정규화됨")
    passed += 1

    # T09: JSON 패턴 크기 불일치 -> 해당 케이스 FAIL
    dummy_filters = {
        "size_5": {"cross": make_cross(5), "x": make_x(5)}
    }
    mismatched_case = {"input": make_matrix(4), "expected": "x"}
    res9 = run_case("size_5_bad", mismatched_case, dummy_filters)
    assert res9["status"] == "FAIL" and res9["category"] == "스키마", "T09 실패"
    print("✓ T09 통과: 패턴 크기 불일치 시 FAIL 및 스키마 분류 기록")
    passed += 1

    # T10: JSON 필터 누락 -> 해당 케이스 FAIL
    res10 = run_case("size_99_1", {"input": make_matrix(99), "expected": "x"}, dummy_filters)
    assert res10["status"] == "FAIL" and res10["category"] == "스키마", "T10 실패"
    print("✓ T10 통과: 필터 누락 시 FAIL 및 스키마 분류 기록")
    passed += 1

    # T11: 잘못된 JSON 파일 -> 오류 안내 후 None 반환 (비정상 종료 방지)
    bad_data = load_data("non_existent_file.json")
    assert bad_data is None, "T11 실패"
    print("✓ T11 통과: 존재하지 않거나 손상된 파일 로드 시 안전하게 None 반환")
    passed += 1

    # T12: 3, 5, 13, 25 크기별 측정 -> 성능표 결과 4건 생성
    bench = run_benchmark((3, 5, 13, 25), repeat=10)
    assert len(bench) == 4 and all(b["avg_ms"] >= 0 for b in bench), "T12 실패"
    print("✓ T12 통과: 3, 5, 13, 25 크기별 10회 평균 성능 측정 완료")
    passed += 1

    print(f"\n=== 결과: {passed}/{total} 전체 테스트 통과 ===")


if __name__ == "__main__":
    run_tests()
