"""
tools/make_data.py
공식 미션 규격에 맞춘 data.json 생성 및 연습용 패턴 생성 도구
"""

import json
import os
import sys

# 프로젝트 루트를 sys.path에 추가하여 src 모듈 임포트 가능하도록 설정
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.matrix import make_cross, make_x


def generate_official_dataset():
    """공식 미션 가이드 규격에 맞춘 filters와 patterns 딕셔너리를 생성합니다."""
    # 1. filters
    filters = {
        "size_5": {
            "cross": make_cross(5, val=1.0, center_val=0.9, bg=0.0),
            "x": make_x(5, val=0.1, center_val=0.1, bg=0.0),
        },
        "size_13": {
            "cross": make_cross(13, val=0.3, center_val=0.3, bg=0.0),
            "x": make_x(13, val=0.3, center_val=7.5, bg=0.0),
        },
        "size_25": {
            "cross": make_cross(25, val=1.0, center_val=4.9, bg=0.0),
            "x": make_x(25, val=0.1, center_val=0.1, bg=0.0),
        },
    }

    # 2. patterns (라벨 다양성 포함: '+', 'x', 'X', 'Cross')
    patterns = {
        "size_5_1": {
            "input": make_x(5, val=1.0, bg=0.0),
            "expected": "x",
        },
        "size_5_2": {
            "input": make_cross(5, val=1.0, bg=0.0),
            "expected": "+",
        },
        "size_13_1": {
            "input": make_x(13, val=1.0, bg=0.0),
            "expected": "X",
        },
        "size_13_2": {
            "input": make_cross(13, val=1.0, bg=0.0),
            "expected": "Cross",
        },
        "size_25_1": {
            "input": make_x(25, val=1.0, bg=0.0),
            "expected": "X",
        },
        "size_25_2": {
            "input": make_cross(25, val=1.0, bg=0.0),
            "expected": "Cross",
        },
    }

    dataset = {
        "meta": {
            "version": "1.0",
            "type": "json",
            "description": "Mini NPU Simulator Benchmark Dataset"
        },
        "filters": filters,
        "patterns": patterns,
    }
    return dataset


def create_data_file(filepath="data.json"):
    data = generate_official_dataset()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[성공] {filepath} 생성 완료 (필터 3종, 패턴 6개)")


if __name__ == "__main__":
    target_path = os.path.join(PROJECT_ROOT, "data.json")
    create_data_file(target_path)
