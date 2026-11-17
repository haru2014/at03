"""
src/mode_json.py
모드 2: data.json 자동 분석 모드 구현
- data.json 로드 및 스키마 검증
- 필터/패턴 로드 및 MAC 점수 계산
- 라벨 정규화 및 허용오차 기반 PASS/FAIL 판정
- 4개 크기(3×3, 5×5, 13×13, 25×25) 성능 측정
- 결과 리포트 요약 및 실패 분류 출력
"""

import json
import os
from src.matrix import is_square
from src.mac import mac
from src.judge import EPSILON, normalize_label, judge
from src.perf import run_benchmark, print_benchmark_table


def load_data(path="data.json"):
    """
    JSON 데이터 파일을 안전하게 로드합니다.
    파일 부재 또는 JSON 파싱 오류 발생 시 예외를 던지지 않고
    안내 메시지를 출력한 후 None을 반환합니다.
    """
    if not os.path.exists(path):
        print(f"오류: 데이터 파일 '{path}'을(를) 찾을 수 없습니다.")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"오류: JSON 파일 파싱 실패 ({e})")
        return None
    except Exception as e:
        print(f"오류: 파일 읽기 중 예외 발생 ({e})")
        return None


def parse_size_from_key(key):
    """
    'size_{N}_{idx}' 형태의 키 문자열에서 크기 N을 정수로 추출합니다.
    규칙에 맞지 않으면 None을 반환합니다.
    """
    parts = key.split("_")
    if len(parts) < 2 or parts[0] != "size":
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


def run_case(case_id, case_info, filters_dict):
    """
    단일 패턴 케이스에 대한 검증, MAC 계산, 판정을 수행합니다.
    모든 검증 실패 및 오류는 예외로 중단하지 않고 FAIL 상태와 분류 사유로 기록합니다.
    """
    res = {
        "case_id": case_id,
        "cross_score": None,
        "x_score": None,
        "verdict": "-",
        "expected": "-",
        "status": "FAIL",
        "category": "기타",
        "reason": ""
    }

    # 1. 키에서 크기 N 추출
    n = parse_size_from_key(case_id)
    if n is None:
        res["category"] = "스키마"
        res["reason"] = f"패턴 키 형식 오류: '{case_id}'"
        return res

    # 2. 크기에 해당하는 필터 존재 확인
    filter_group_key = f"size_{n}"
    if filter_group_key not in filters_dict:
        res["category"] = "스키마"
        res["reason"] = f"크기 {n}에 대응하는 필터 그룹 부재"
        return res

    filter_group = filters_dict[filter_group_key]
    cross_filter = filter_group.get("cross")
    x_filter = filter_group.get("x")

    if cross_filter is None or x_filter is None:
        res["category"] = "스키마"
        res["reason"] = "cross 또는 x 필터 데이터 누락"
        return res

    if not is_square(cross_filter, n) or not is_square(x_filter, n):
        res["category"] = "스키마"
        res["reason"] = f"필터 행렬이 {n}x{n} 정사각 형태가 아님"
        return res

    # 3. 패턴 입력 검증
    pattern = case_info.get("input")
    if pattern is None:
        res["category"] = "스키마"
        res["reason"] = "input 패턴 데이터 누락"
        return res

    if not is_square(pattern, n):
        res["category"] = "스키마"
        res["reason"] = f"패턴 크기 불일치 ({n}x{n} 정사각 행렬 아님)"
        return res

    # 4. 라벨 정규화
    raw_expected = case_info.get("expected")
    expected = normalize_label(raw_expected)
    if expected is None:
        res["category"] = "스키마"
        res["reason"] = f"정규화 불가능한 expected 라벨: '{raw_expected}'"
        return res
    res["expected"] = expected

    # 5. MAC 연산 수행
    score_cross = mac(pattern, cross_filter)
    score_x = mac(pattern, x_filter)
    res["cross_score"] = score_cross
    res["x_score"] = score_x

    # 6. epsilon 판정
    verdict = judge(score_cross, score_x, la="Cross", lb="X")
    res["verdict"] = verdict

    # 7. PASS / FAIL 대조
    if verdict == expected:
        res["status"] = "PASS"
        res["category"] = "정상"
        res["reason"] = "판정 일치"
    elif verdict == "UNDECIDED":
        res["status"] = "FAIL"
        res["category"] = "수치 비교"
        diff = abs(score_cross - score_x)
        res["reason"] = f"동점 (|{score_cross:.1f} - {score_x:.1f}| < 1e-09)"
    else:
        res["status"] = "FAIL"
        res["category"] = "로직"
        res["reason"] = f"판정 불일치 (예측: {verdict}, 기대: {expected})"

    return res


def run_mode_json(data_path="data.json"):
    """
    모드 2 전체 흐름을 실행합니다.
    1) data.json 로드
    2) 모든 패턴 검증 및 판정
    3) 케이스별 결과 표 출력
    4) 성능 분석 표 출력
    5) 결과 리포트 요약 출력
    """
    data = load_data(data_path)
    if data is None:
        return

    filters_dict = data.get("filters", {})
    patterns_dict = data.get("patterns", {})

    if not patterns_dict:
        print("분석할 패턴 데이터가 없습니다.")
        return

    results = []
    for case_id, case_info in patterns_dict.items():
        res = run_case(case_id, case_info, filters_dict)
        results.append(res)

    # 1. 케이스별 실행 결과 표 출력
    print("\n[케이스별 분석 결과]")
    header = f"{'케이스':<14}{'Cross':<10}{'X':<10}{'판정':<14}{'exp.':<10}{'결과':<8}"
    print(header)
    for r in results:
        cross_str = f"{r['cross_score']:.1f}" if r['cross_score'] is not None else "-"
        x_str = f"{r['x_score']:.1f}" if r['x_score'] is not None else "-"
        print(f"{r['case_id']:<14}{cross_str:<10}{x_str:<10}{r['verdict']:<14}{r['expected']:<10}{r['status']:<8}")
    print()

    # 2. 성능 분석 표 출력 (3×3, 5×5, 13×13, 25×25 10회 평균)
    perf_results = run_benchmark(sizes=(3, 5, 13, 25), repeat=10)
    print_benchmark_table(perf_results)

    # 3. 결과 리포트 요약
    total_count = len(results)
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")

    print(f"[결과 요약] 전체 {total_count} / 통과 {pass_count} / 실패 {fail_count}")

    # 실패 케이스 상세 및 카테고리 집계
    category_counts = {}
    for r in results:
        if r["status"] == "FAIL":
            print(f"- {r['case_id']} [{r['category']}] {r['reason']}")
            category_counts[r["category"]] = category_counts.get(r["category"], 0) + 1

    if fail_count > 0:
        cat_str = ", ".join([f"{cat} {cnt}건" for cat, cnt in category_counts.items()])
        print(f"실패 분류: {cat_str}")
    else:
        print("모든 테스트가 통과하였습니다.")
    print()
