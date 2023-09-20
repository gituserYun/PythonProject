import subprocess
from termcolor import cprint
import os
import json

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
    #subprocess.call(['../example/test.py'])

    #Windows에서 동작
    output = subprocess.check_output(['python', '.\\Protocol\\directory_scan.py', url])
    output_str = output.decode('utf-8')
    path_list = output_str.split('\r\n')
    #print(f"test output: {path_list}")

    directory_names = []
    file_names = []

    print("Directory Names:")
    print("===========")
    for path in path_list:
        if path.endswith('/'):
            directory_names.append(path)
    for dirname in directory_names:
        print(f"{dirname}")

    print("\nFilename:")
    print("===========")
    web_extensions = {'.html', '.htm', '.php', '.jsp', '.asp', '.aspx',
                        '.css', '.js',
                        '.png', '.jpg', '.jpeg', '.svg'}
    for path in path_list:
        _, ext = os.path.splitext(path)
        if ext in web_extensions:
            file_names.append(path)
    for filename in file_names:
        print(f"{filename}")
    print_blue("\n[*] 디렉토리 스캔 동작 점검\n")

    return directory_names, file_names

def sqlI(url, files):
    #dir_str = json.dumps(directories)
    file_str = json.dumps(files)

    subprocess.call(['python', '.\\VulnerabilityList\\sql_injection_test1.py',url ,file_str])
    print_blue("\n[*] SQL 인젝션 항목 점검\n")

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
    print_red(" - 스캔 과정에서 데이터 손실이 발생할 수도 있으므로 점검을 시작하기 전에 중요 데이터는 반드시 백업해주세요.")
    print("\n")

    url = input("URL을 입력: ")
    print("")

    #디렉토리 스캔 함수
    directories, files = dirScan(url)
    #print(directories)
    #print(files)
    check_url = []
    for file in files:
        full_url = "{}/{}".format(url.rstrip('/'), file.lstrip('/'))
        check_url.append(full_url)
    #print(f"check_url: {check_url}")

    #점검항목1: SQL 인젝션(SQL Injection)
    sqlI(url, check_url)