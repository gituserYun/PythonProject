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

# def sql_injection(url, check_url):
#     urls_json = json.dumps(check_url)
#     print_blue("\n[*] SQL Injection 점검")
#     # Windows에서 동작
#     # subprocess.call(['python', '../VulnerabilityList/SQLI/sql_injection.py', url, urls_json])
#     output = subprocess.run(['python', '../VulnerabilityList/SQLI/sql_injection.py' ,url ,urls_json], capture_output=True, text=True, check=True)
#     extracted_info = output.stdout

#     # payload_1 추출
#     cnt = 0
#     payload_1s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Attack Detected: "):
#             payload_1s.add(line[17:])
#     payload_1 = list(payload_1s)
#     print_green("\npayload(Payload Code):")
#     print_green("===========")
#     for code in payload_1:
#         print(code)
#         cnt += 1
#     print_grey(f"payload cnt: {cnt}")
#     # if cnt == 0:
#     #     payload_1 = "          -          "    

#     # category_1 추출
#     category_1 = "SQL 인젝션(SQL Injection)"
#     print_green("\ncategory:")
#     print_green("===========")
#     print(category_1)

#     # targeturl_1 추출
#     targeturl_1s = set()
#     num_1 = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Target url: "):
#             targeturl_1s.add(line[12:])
#     targeturl_1 = list(targeturl_1s)
#     print_green("\ntargeturl(Vulnerable file path):")
#     print_green("===========")
#     for target in targeturl_1:
#         print(target)
#         num_1 += 1 #취약한 파일 경로 수 파악
#     # if num_1 == 0:
#     #     targeturl_1 = "          -          "    

#     # num_1 추출
#     print_green("\nnum(Number of vulnerable file paths):")
#     print_green("===========")
#     print(num_1)

#     # risk_1 데이터 추출
#     risk_1 = 'Low'
#     risk_order = {'High':0, 'Medium':1, 'Low':2}
#     print_green("\nrisk:")
#     print_green("===========")
#     for line in extracted_info.split('\n'):
#         if line.startswith("Risk: "):
#             extracted_risk = line[6:].strip()
#             if risk_order[extracted_risk] < risk_order[risk_1]:
#                 risk_1 = extracted_risk
#     print(risk_1)

#     # inspectionurl_1 추출
#     inspectionurl_1s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Inspection_url: "):
#             inspectionurl_1s.add(line[16:])
#     inspectionurl_1 = list(inspectionurl_1s)
#     print_green("\ninspection_url(Inspection url path):")
#     print_green("===========")
#     for inspection in inspectionurl_1:
#         print(inspection)

#     # detailpayload_1 추출
#     detailpayload_1s = set()
#     detail_1 = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Detail payload: "):
#             detailpayload_1s.add(line[16:])
#     detailpayload_1 = list(detailpayload_1s)
#     print_green("\ndetailpayload(Performance Indicators by Inspection Item):")
#     print_green("===========")
#     for detail in detailpayload_1:
#         if detail:
#             print(detail)
#             detail_1 += 1
#     # if detail_1 == 0:
#     #     detailpayload_1 = "          -          "

#     return payload_1, category_1, num_1, risk_1, targeturl_1, inspectionurl_1, detailpayload_1

# def xss(url, check_url, identi_paths):
#     urls_json = json.dumps(check_url)
#     identi_json = json.dumps(identi_paths)
#     print_blue("\n[*] XSS 점검")
#     # subprocess.call(['python', '../VulnerabilityList/XSS/xss.py', url, urls_json, identi_json])
#     output = subprocess.run(['python', '../VulnerabilityList/XSS/xss.py' ,url ,urls_json, identi_json], capture_output=True, text=True, check=True)
#     extracted_info = output.stdout
    
#     # payload_2 추출
#     cnt = 0
#     payload_2s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Attack Detected: "):
#             payload_2s.add(line[17:])
#     payload_2 = list(payload_2s)
#     print_green("\npayload(Payload Code):")
#     print_green("===========")
#     for code in payload_2:
#         print(code)
#         cnt += 1
#     print_grey(f"payload cnt: {cnt}")
#     # if cnt == 0:
#     #     payload_2 = "          -          "    

#     # category_2 추출
#     category_2 = "크로스사이트스크립팅(XSS)"
#     print_green("\ncategory:")
#     print_green("===========")
#     print(category_2)

#     # targeturl_2 추출
#     targeturl_2s = set()
#     num_2 = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Target url: "):
#             targeturl_2s.add(line[12:])
#     targeturl_2 = list(targeturl_2s)
#     print_green("\ntargeturl(Vulnerable file path):")
#     print_green("===========")
#     for target in targeturl_2:
#         print(target)
#         num_2 += 1 #취약한 파일 경로 수 파악    
#     # if num_2 == 0:
#     #     targeturl_2 = "          -          "

#     # num_2 추출
#     print_green("\nnum(Number of vulnerable file paths):")
#     print_green("===========")
#     print(num_2)

#     # risk_2 데이터 추출
#     risk_2 = 'Low'
#     risk_order = {'High':0, 'Medium':1, 'Low':2}
#     print_green("\nrisk:")
#     print_green("===========")
#     for line in extracted_info.split('\n'):
#         if line.startswith("Risk: "):
#             extracted_risk = line[6:].strip()
#             if risk_order[extracted_risk] < risk_order[risk_2]:
#                 risk_2 = extracted_risk
#     print(risk_2)

#     # inspectionurl_2 추출
#     inspectionurl_2s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Inspection_url: "):
#             inspectionurl_2s.add(line[16:])
#     inspectionurl_2 = list(inspectionurl_2s)
#     print_green("\nInspection_url(Inspection url path):")
#     print_green("===========")
#     for inspection in inspectionurl_2:
#         print(inspection)

#     # detailpayload_2 추출
#     detailpayload_2s = set()
#     # detail_2 = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Detail payload: "):
#             detailpayload_2s.add(line[16:])
#     detailpayload_2 = list(detailpayload_2s)
#     print_green("\nDetailpayload(Performance Indicators by Inspection Item):")
#     print_green("===========")
#     for detail in detailpayload_2:
#         if detail:
#             print(detail)
#     #         detail_2 += 1
#     # if detail_2 == 0:
#     #     detailpayload_2 = "          -          "
    
#     return payload_2, category_2, num_2, risk_2, targeturl_2, inspectionurl_2, detailpayload_2

# def directory_traversal(url, check_url, identi_paths):
#     urls_json = json.dumps(check_url)
#     identi_json = json.dumps(identi_paths)
#     print_blue("\n[*] Directory Traversal 점검")
#     # Windows에서 동작
#     # subprocess.call(['python', '../VulnerabilityList/DT/directory_traversal.py', url, urls_json, identi_json])
#     output = subprocess.run(['python', '../VulnerabilityList/DT/directory_traversal.py' ,url ,urls_json, identi_json], capture_output=True, text=True, check=True)        
#     extracted_info = output.stdout

#     # payload_3 추출
#     cnt = 0
#     payload_3s = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Attack Detected: "):
#             payload_3s.add(line[17:])
#     payload_3 = list(payload_3s)
#     print_green("\npayload(Payload Code):")
#     print_green("===========")
#     for code in payload_3:
#         print(code)
#         cnt += 1
#     print_grey(f"payload cnt: {cnt}")
#     # if cnt == 0:
#     #     payload_3 = "          -          "

#     # category_3 추출
#     category_3 = "디렉토리 트레버설(Directory Traversal)"
#     print_green("\ncategory:")
#     print_green("===========")
#     print(category_3)

#     # targeturl_3 추출
#     targeturl_3s = set()
#     num_3 = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Target url: "):
#             targeturl_3s.add(line[12:])
#     targeturl_3 = list(targeturl_3s)
#     print_green("\ntargeturl(Vulnerable file path):")
#     print_green("===========")
#     for target in targeturl_3:
#         print(target)
#         num_3 += 1 #취약한 파일 경로 수 파악
#     # if num_3 == 0:
#     #     targeturl_3 = "          -          "    

#     # num_3 추출
#     print_green("\nnum(Number of vulnerable file paths):")
#     print_green("===========")
#     print(num_3)

#     # risk_3 데이터 추출
#     risk_3 = 'Low'
#     risk_order = {'High':0, 'Medium':1, 'Low':2}
#     print_green("\nrisk:")
#     print_green("===========")
#     for line in extracted_info.split('\n'):
#         if line.startswith("Risk: "):
#             extracted_risk = line[6:].strip()
#             if risk_order[extracted_risk] < risk_order[risk_3]:
#                 risk_3 = extracted_risk
#     print(risk_3)

#     # inspectionurl_3 추출
#     inspectionurl_3 = set()
#     for line in extracted_info.split('\n'):
#         if line.startswith("Inspection_url: "):
#             inspectionurl_3.add(line[16:])
#     inspectionurl_3 = list(inspectionurl_3)
#     print_green("\ninspection_url(Inspection url path):")
#     print_green("===========")
#     for inspection in inspectionurl_3:
#         print(inspection)

#     # detailpayload_3 추출
#     detailpayload_3s = set()
#     # detail_3 = 0
#     for line in extracted_info.split('\n'):
#         if line.startswith("Detail payload: "):
#             detailpayload_3s.add(line[16:])
#     detailpayload_3 = list(detailpayload_3s)
#     print_green("\ndetailpayload(Performance Indicators by Inspection Item):")
#     print_green("===========")
#     for detail in detailpayload_3:
#         if detail:
#             print(detail)
#             # detail_3 += 1
#     # if detail_3 == 0:
#     #     detailpayload_3 = "          -          "
        
#     return payload_3, category_3, num_3, risk_3, targeturl_3, inspectionurl_3, detailpayload_3

def file_download(url, check_url, identi_paths):
    urls_json = json.dumps(check_url)
    identi_json = json.dumps(identi_paths)
    print_blue("\n[*] File Download 점검")
    subprocess.call(['python', '../VulnerabilityList/FD/file_download.py', url, urls_json, identi_json]) 
  
# def file_upload(url, check_url, identi_paths):
#     urls_json = json.dumps(check_url)
#     identi_json = json.dumps(identi_paths)
#     print_blue("\n[*] File Upload 점검")
#     subprocess.call(['python', '../VulnerabilityList/FU/file_upload.py', url, urls_json, identi_json])   


def inspection_result(url, payload, category, num, risk, targeturl, inspectionurl, detailpayload):
    print_green("url:\n======================")
    print(url)
    print_green("\npayload:\n======================")
    print(payload)
    print_green("\ncategory:\n======================")
    print(category)
    print_green("\nnum:\n======================")
    print(num)
    print_green("\nrisk:\n======================")
    print(risk)
    print_green("\ntargeturl:\n======================")
    print(targeturl)
    print_green("\ninspectionurl:\n======================")
    print(inspectionurl)
    print_green("\ndetailpayload:\n======================")
    print(detailpayload)    

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
    # # 점검항목1: SQL 인젝션(SQL Injection)
    # payload_1, category_1, num_1, risk_1, targeturl_1, inspectionurl_1, detailpayload_1 = sql_injection(url, check_url)
    
    # # 점검항목2: 크로스사이트스크립트(XSS)
    # payload_2, category_2, num_2, risk_2, targeturl_2, inspectionurl_2, detailpayload_2 = xss(url, check_url, identi_paths)
    
    # # 점검항목3: 디렉토리 트레버셜(Directory Traversal)
    # payload_3, category_3, num_3, risk_3, targeturl_3, inspectionurl_3, detailpayload_3 = directory_traversal(url, check_url, identi_paths)

    # # 점검항목4: 파일 업로드(File Upload)
    # file_upload(url, check_url, identi_paths)

    # 점검항목5: 파일 다운로드(File Download)
    file_download(url, check_url, identi_paths)
    #################

    ### 점검 결과 ###
    # # 1: SQL 인젝션(SQL Injection): url, payload_1, category_1, num_1, risk_1, targeturl_1, inspectionurl_1, detailpayload_1
    # print_blue("\n[*] SQL Injection 점검 결과")
    # inspection_result(url, payload_1, category_1, num_1, risk_1, targeturl_1, inspectionurl_1, detailpayload_1)
    
    # # 2: 크로스사이트스크립팅(XSS): url, payload_2, category_2, num_2, risk_2, targeturl_2, inspectionurl_2, detailpayload_2
    # print_blue("\n[*] XSS 점검 결과")
    # inspection_result(url, payload_2, category_2, num_2, risk_2, targeturl_2, inspectionurl_2, detailpayload_2)

    # # 3: 데렉토리 트레버셜(Directory Traversal): url, payload_3, category_3, num_3, risk_3, targeturl_3, inspectionurl_3, detailpayload_3
    # print_blue("\n[*] Directory Traversal 점검 결과")
    # inspection_result(url, payload_3, category_3, num_3, risk_3, targeturl_3, inspectionurl_3, detailpayload_3)
    #################
    