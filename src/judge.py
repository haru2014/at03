"""
src/judge.py
라벨 정규화 및 허용오차(epsilon) 기반 판정 모듈
"""

EPSILON = 1e-9


def normalize_label(raw):
    """
    다양한 형태의 문자열 라벨을 표준 라벨('Cross' 또는 'X')로 정규화합니다.
    - '+', 'cross', 'plus' -> 'Cross'
    - 'x', 'ex' -> 'X'
    - 유효하지 않은 값은 None 반환 (FAIL 처리용)
    """
    if raw is None:
        return None
    key = str(raw).strip().lower()
    if key in ("+", "cross", "plus"):
        return "Cross"
    if key in ("x", "ex"):
        return "X"
    return None


def judge(a, b, la="Cross", lb="X"):
    """
    두 점수 a, b를 epsilon 기준으로 비교하여 판정 결과를 반환합니다.
    - 점수 차이가 EPSILON(1e-9) 미만이면 'UNDECIDED' (동점)
    - a > b 이면 la
    - b > a 이면 lb
    """
    if abs(a - b) < EPSILON:
        return "UNDECIDED"
    return la if a > b else lb


def judge_mode1(score_a, score_b):
    """
    사용자 입력 모드(모드 1)용 판정 함수:
    - 점수 차이가 EPSILON 미만이면 '판정 불가'
    - score_a > score_b 이면 'A'
    - score_b > score_a 이면 'B'
    """
    if abs(score_a - score_b) < EPSILON:
        return "판정 불가"
    return "A" if score_a > score_b else "B"
