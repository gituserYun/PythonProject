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
    # subprocess.call(['python', '../Scan/directory_scan.py', url])
    output = subprocess.run(['python', '../Scan/directory_scan.py', url], capture_output=True, text=True)
    extracted_info = output.stdout

    # 출력 디렉토리 이름
    directory_names_set = set()
    directory_names = []
    for line in extracted_info.split('\n'):
        if line.startswith("DIR: "):
            directory_names_set.add(line[5:])
    print_green("Directory Names:")
    print_green("===========")
    for directory_name in directory_names_set:
        directory_names.append(directory_name)
        print(directory_name)

    # 출력 파일 이름
    cnt = 0
    file_names_set = set()
    file_names = []
    for line in extracted_info.split('\n'):
        if line.startswith("FILE: "):
            file_names_set.add(line[6:])
    print_green("\nFile Names:")
    print_green("===========")
    for file_name in file_names_set:
        file_names.append(file_name)
        print(file_name)
        cnt += 1
    print_grey(f"File Name cnt: {cnt}")

    # 식별 경로
    identi_path_set = set()
    identi_paths = []
    identi_path_dict = {
        "script_location: ": 17,
        "script_src: ": 12,
        "a_href: ": 8,
        "form_action: ": 13,
        "link_href: ": 11,
        "img_src: ": 9,
        "area_href: ": 11,
        "meta: ": 6,
        "embed&object: ": 14,
    }
    for line in extracted_info.split('\n'):
        for key, prefix_len in identi_path_dict.items():
            if line.startswith(key):
                identi_path_set.add(line[prefix_len:])
                break
    print_green("\nIdentification path:")
    print_green("===========")
    for identi_path in identi_path_set:
        identi_paths.append(identi_path)
        print(identi_path) 

    return directory_names, file_names, identi_paths

# def sqlI(url, check_url):
#     urls_json = json.dumps(check_url)
#     print_blue("\n[*] SQL Injection 점검")
#     # Windows에서 동작
#     output = subprocess.run(['python', '../VulnerabilityList/SQLI/sql_injection.py' ,url ,urls_json], capture_output=True, text=True)
#     extracted_info = output.stdout

#     # payload 추출
#     cnt = 0
#     payload_s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Attack Detected: "):
#             payload_s.add(line[17:])
#     payload = list(payload_s)
#     print_green("\npayload(Payload Code):")
#     print_green("===========")
#     for code in payload:
#         print(code)
#         cnt += 1
#     print_grey(f"payload cnt: {cnt}")

#     # category 추출
#     category = "SQL 인젝션"
#     print_green("\ncategory:")
#     print_green("===========")
#     print(category)

#     # targeturl 추출
#     targeturl_s = set()
#     num = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Target url: "):
#             targeturl_s.add(line[12:])
#     targeturl = list(targeturl_s)
#     print_green("\ntargeturl(Vulnerable file path):")
#     print_green("===========")
#     for target in targeturl:
#         print(target)
#         num += 1 #취약한 파일 경로 수 파악

#     # num 추출
#     print_green("\nnum(Number of vulnerable file paths):")
#     print_green("===========")
#     print(num)

#     # risk 데이터 추출
#     risk = 'Low'
#     risk_order = {'High':0, 'Medium':1, 'Low':2}
#     print_green("\nrisk:")
#     print_green("===========")
#     for line in extracted_info.split('\n'):
#         if line.startswith("risk: "):
#             print(line[6:])
#             extracted_risk = line[6:].strip()
#             if risk_order[extracted_risk] < risk_order[risk]:
#                 risk = extracted_risk

#     # inspectionurl 추출
#     inspectionurl_s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("inspection_url: "):
#             inspectionurl_s.add(line[16:])
#     inspectionurl = list(inspectionurl_s)
#     print_green("\ninspectionurl(Inspection url path):")
#     print_green("===========")
#     for inspection in inspectionurl:
#         print(inspection)

#     # detailpayload 추출
#     detailpayload_s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Detail payload: "):
#             detailpayload_s.add(line[16:])
#     detailpayload = list(detailpayload_s)
#     print_green("\ndetailpayload(Performance Indicators by Inspection Item):")
#     print_green("===========")
#     for detail in detailpayload:
#         print(detail)

#     return payload, category, num, risk, targeturl, inspectionurl, detailpayload

def xss(url, check_url, identi_paths):
    urls_json = json.dumps(check_url)
    identi_json = json.dumps(identi_paths)
    print_blue("\n[*] XSS 점검")
    subprocess.call(['python', '../VulnerabilityList/XSS/xss.py', url, urls_json, identi_json])
    # output = subprocess.run(['python', '../VulnerabilityList/XSS/xss.py' ,url ,urls_json, identi_json], capture_output=True, text=True)


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

    # 디렉토리 스캔 함수
    # dirScan(url)
    directories, files, identi_paths = dirScan(url)
    
    # 프로토콜+점검IP+리소스 경로
    check_url = []
    for file in files:
        full_url = "{}/{}".format(url.rstrip('/'), file.lstrip('/'))
        check_url.append(full_url)
    
    ### 점검 시작 ###
    # 점검항목1: SQL 인젝션(SQL Injection)
    # payload, category, num, risk, targeturl, inspectionurl, detailpayload = sqlI(url, check_url)
    
    # 점검항목2: XSS(Crose Site Script)
    xss(url, check_url, identi_paths)
    #################

    ### 점검 결과 ###
    # url, payload, category, num, risk 
    # print_blue("\n[*] 점검 결과")
    # print_green("url:\n===========")
    # print(url)
    # print_green("\npayload:\n===========")
    # print(payload)
    # print_green("\ncategory:\n===========")
    # print(category)
    # print_green("\nnum:\n===========")
    # print(num)
    # print_green("\nrisk:\n===========")
    # print(risk)
    # print_green("\ntargeturl:\n===========")
    # print(targeturl)
    # print_green("\ninspectionurl:\n===========")
    # print(inspectionurl)
    # print_green("\ndetailpayload:\n===========")
    # print(detailpayload)

    