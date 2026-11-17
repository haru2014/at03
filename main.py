"""
main.py
Mini NPU Simulator 프로그램 진입점
- 실행 모드(1: 사용자 입력, 2: data.json 분석) 선택 및 실행 흐름 제어
"""

import sys
from src.mode_input import run_mode_input
from src.mode_json import run_mode_json


def print_menu():
    print("===== Mini NPU Simulator =====")
    print("1. 사용자 입력 (3×3)")
    print("2. data.json 분석")
    print("q. 프로그램 종료")


def main():
    while True:
        print_menu()
        try:
            choice = input("모드를 선택하세요 (1/2/q): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n프로그램을 종료합니다.")
            break

        if choice == "1":
            run_mode_input()
        elif choice == "2":
            run_mode_json()
        elif choice.lower() in ("q", "quit", "exit"):
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 번호를 선택해 주세요 (1 또는 2, 종료는 q).\n")


if __name__ == "__main__":
    main()
