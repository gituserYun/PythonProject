
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
    print_blue("\n[*] 디렉토리 스캔 동작 점검\n")
    # Windows에서 동작
    output = subprocess.run(['python', '../Scan/directory_scan.py', url], capture_output=True, text=True)
    extracted_info = output.stdout
    directory_names = []
    file_names = []

    # 출력 디렉토리 이름
    print_green("Directory Names:")
    print_green("===========")
    for line in extracted_info.split('\n'):
        if line.startswith("DIR: "):
            directory_names.append(line[5:])
            print(line[5:])
    # 출력 파일 이름
    print_green("\nFile Names:")
    print_green("===========")
    for line in extracted_info.split('\n'):
        if line.startswith("FILE: "):
            file_names.append(line[6:])
            print(line[6:])

    return directory_names, file_names 

def sqlI(url, check_url):
    urls_json = json.dumps(check_url)
    print_blue("\n[*] SQL Injection 점검")
    # Windows에서 동작
    output = subprocess.run(['python', '../VulnerabilityList/SQLI/sql_injection.py' ,url ,urls_json], capture_output=True, text=True)
    extracted_info = output.stdout
    payload = []
    category = "SQL 인젝션"
    num = 0
    risk = None
    targeturl_s = set()
    
    for line in extracted_info.split('\n'):
        if line.startswith("Attack Detected: "):
            payload.append(line[17:])
    #위험과 주의가 섞여있을 때 판별해야함.
    for line in extracted_info.split('\n'):
        if line.startswith("risk: "):
            risk = str(line[6:])
            break
    for line in extracted_info.split('\n'):
        if line.startswith("Target url: "):
            targeturl_s.add(line[12:])
    targeturl = list(targeturl_s)

    print_green("\nPayload Code(payload):")
    print_green("===========")
    for code in payload:
        print(code)
    print_green("\nCategory(category):")
    print_green("===========")
    print(category)
    print_green("\nVulnerable file path(targeturl):")
    print_green("===========")
    for target in targeturl:
        print(target)
        num += 1 #취약한 파일 경로 수 파악
    print_green("\nNumber of vulnerable file paths(num):")
    print_green("===========")
    print(num)
    print_green("\nRisk(risk):")
    print_green("===========")
    for line in extracted_info.split('\n'):
        if line.startswith("risk: "):
            print(line[6:])

    return payload, category, num, risk, targeturl


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
    
    # 프로토콜+점검IP+리소스 경로
    check_url = []
    for file in files:
        full_url = "{}/{}".format(url.rstrip('/'), file.lstrip('/'))
        check_url.append(full_url)
    
    ### 점검 시작 ###
    #점검항목1: SQL 인젝션(SQL Injection)
    payload, category, num, risk, targeturl = sqlI(url, check_url)
    #################

    ### 점검 결과 ###
    # url, payload, category, num, risk 
    print_blue("\n[*] 점검 결과")
    print_green("url:\n===========")
    print(url)
    print_green("\npayload:\n===========")
    print(payload)
    print_green("\ncategory:\n===========")
    print(category)
    print_green("\nnum:\n===========")
    print(num)
    print_green("\nrisk:\n===========")
    print(risk)
    print_green("\ntargeturl:\n===========")
    print(targeturl)

    