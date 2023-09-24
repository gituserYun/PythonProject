import subprocess
from termcolor import cprint
import os

print_red = lambda x: cprint(x, 'red')
print_yellow = lambda x: cprint(x, 'yellow')
print_green = lambda x: cprint(x, 'green')
print_blue = lambda x: cprint(x, 'blue')
print_magenta = lambda x : cprint(x, "magenta")
print_cyan = lambda x : cprint(x, "cyan")
print_grey = lambda x : cprint(x, "grey")
print_white = lambda x : cprint(x, "white")

def dirScan(url):
    #Linux에서 동작
    output = subprocess.run(['python3', './directory_scan.py', url], capture_output=True, text=True)
    #directory_scan.py의 표준 출력 결과에서 추출한 정보를 가져옴
    extracted_info = output.stdout
    
    #출력 디렉토리 이름
    print("Directory Names:")
    print("===========")
    for line in extracted_info.split('\n'):
        if line.startswith("DIR: "):
            print(line)
    #출력 파일 이름
    print("\nFilename:")
    print("===========")
    for line in extracted_info.split('\n'):
        if line.startswith("FILE: "):
            print(line)    

####directory_scan_test1.py
    # output = subprocess.run(['python3', './directory_scan_test1.py', url], capture_output=True, text=True)
    # #Windows에서 동작
    # #output = subprocess.check_output(['python', './Protocol/directory_scan.py', url])

    # #directory_scan.py의 표준 출력 결과에서 추출한 정보를 가져옴
    # extracted_info = output.stdout

    # #출력 디렉토리 이름
    # print("Directory Names:")
    # print("===========")
    # #extracted_info에서 디렉토리 정보 찾아서 출력
    # for line in extracted_info.split('\n'):
    #     if line.startswith("DIR: "):
    #         print(line)
    # #출력 파일 이름
    # print("\nFilename:")
    # print("===========")
    # #extracted_info에서 파일 정보 찾아서 출력
    # for line in extracted_info.split('\n'):
    #     if line.startswith("FILE: "):
    #         print(line)


if __name__ == '__main__':
    print_blue("\n==================================================================================\n")
    print_blue("     __   __                     _____             _               __   __ ")
    print_blue("     __   __                     _____             _               __   __ ")
    print_blue("     \ \ / /                    /  __ \           | |              \ \ / / ")
    print_blue("      \ V /   ___   _   _  _ __ | /  \/  ___    __| |  ___  ______  \ V /  ")
    print_blue("       \ /   / _ \ | | | || '__|| |     / _ \  / _` | / _ \|______| /   \  ")
    print_blue("       | |  | (_) || |_| || |   | \__/\| (_) || (_| ||  __/        / /^\ \\")
    print_blue("       \_/   \___/  \__,_||_|    \____/ \___/  \__,_| \___|        \/   \/ ")
    print_blue("\n                                           동아대학교 컴퓨터공학과(웹 취약점 진단)   ")
    print_blue("==================================================================================\n")
    print_red(" ※  주 의  ※\n")
    print_red(" - 웹 사이트의 보안을 테스트하거나 스캔하기 전에 반드시 사전 허가를 받아야 합니다.")
    print_red(" - 허가된 사이트에서 진단 도구를 사용하지 않을 경우 법적인 책임은 사용자에게 있습니다.")
    print_red(" - 스캔 과정에서 데이터 손실이 발생할 수도 있으므로 점검을 시작하기 전에 중요 데이터는 반드시 백업해주세요.\n")
    
    url = input("URL을 입력: ")
    print("")

    #디렉토리 스캔 함수
    dirScan(url)