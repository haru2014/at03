"""
src/matrix.py
n×n 2차원 행렬 데이터 구조 생성, 검증 및 유틸리티 함수
"""


def make_matrix(n, fill=0):
    """
    n×n 크기의 2차원 리스트를 생성합니다.
    (행 복사 버그 방지를 위해 리스트 컴프리헨션 사용)
    """
    return [[fill for _ in range(n)] for _ in range(n)]


def get_element(matrix, r, c):
    """지정된 위치 (r, c)의 원소를 반환합니다."""
    return matrix[r][c]


def set_element(matrix, r, c, val):
    """지정된 위치 (r, c)의 원소를 val로 설정합니다."""
    matrix[r][c] = val


def is_square(matrix, expected_n=None):
    """
    2차원 리스트가 n×n 정사각 행렬인지 검증합니다.
    expected_n이 주어지면 크기가 일치하는지도 함께 검사합니다.
    """
    if not isinstance(matrix, list) or len(matrix) == 0:
        return False
    n = len(matrix)
    if expected_n is not None and n != expected_n:
        return False
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return False
    return True


def make_cross(n, val=1.0, center_val=None, bg=0.0):
    """
    n×n 크기의 십자가(+) 패턴 또는 필터를 생성합니다.
    가운데 행과 가운데 열을 val로 채우고, 가운데 교차점은 center_val(지정 시)로 채웁니다.
    """
    mat = make_matrix(n, fill=bg)
    mid = n // 2
    actual_center_val = val if center_val is None else center_val

    for j in range(n):
        mat[mid][j] = val
    for i in range(n):
        mat[i][mid] = val
    mat[mid][mid] = actual_center_val
    return mat


def make_x(n, val=1.0, center_val=None, bg=0.0):
    """
    n×n 크기의 X 패턴 또는 필터를 생성합니다.
    두 대각선을 val로 채우고, 가운데 교차점은 center_val(지정 시)로 채웁니다.
    """
    mat = make_matrix(n, fill=bg)
    actual_center_val = val if center_val is None else center_val
    mid = n // 2

    for i in range(n):
        mat[i][i] = val
        mat[i][n - 1 - i] = val
    mat[mid][mid] = actual_center_val
    return mat


def flatten_matrix(matrix):
    """
    2차원 행렬을 길이 n²인 1차원 리스트로 변환합니다. (보너스 과제 1)
    """
    return [elem for row in matrix for elem in row]
