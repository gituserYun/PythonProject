import requests
import sys, os
from bs4 import BeautifulSoup
import json

###SQL 인젝션 공격 기법
#Classic SQLI
#Blind SQLI
#Time-Based SQLI
#Error-Based SQLI
#UNION-Based SQLI
#Out-of-band SQLI
#Second-Order SQLI

def classicSQLI(check_files):
    #Classic SQL Injection 시도중(해당 파일들)
    for file in check_files:
        print(f"\nChecking {file}")
        #페이지 내용 가져오기
        response = requests.get(file)
        soup = BeautifulSoup(response.text, 'html.parser')
        #form 태그 찾기 + input, textarea, select, button
        form = soup.find('form')
        if form is None:
            print(f"No forms found in {file}\n")
            continue
        #해당 데이터를 분석 후 저장할 딕셔너리
        form_data = {
            #데이터 전송과 목적지 확인 
            "method" : form.get('method', '').upper(),
            "action" : form.get('action',''),
            "input_fields": [],
            "textarea_fields": [],
            "select_fields": [],
            "button_fields": []            
        }
        print(f"||Form method||: {form_data['method']}")
        print(f"||Form action||: {form_data['action']}")
        #input 태그 속성 데이터 식별
        print("||Input field||")
        inputs = form.find_all('input')
        for i in inputs:
            input_info = {
                "name": i.get('name'),
                "type": i.get('type')
            }
            form_data["input_fields"].append(input_info)
            print(f"name: {i.get('name')}, type: {i.get('type')}")
        #textarea 태그 속성 데이터 식별
        print("||Textarea field||")
        textareas = form.find_all('textarea')
        for i in textareas:
            textarea_info = {
                "name": i.get('name')
            }
            form_data["textarea_fields"].append(textarea_info)
            print(f"name: {i.get('name')}")
        #select 태그 속성 데이터 식별
        print("||Selects field||")
        selects = form.find_all('select')
        for i in selects:
            select_info = {
                "name": i.get('name')
            }
            form_data["select_fields"].append(select_info)
            print(f"name: {i.get('name')}")
        #button 태그 속성 데이터 식별
        print("||button field||")
        buttons = form.find_all('button')
        for i in buttons:
            button_info = {
                "name": i.get('name')
            }
            form_data["button_fields"].append(button_info)        
            print(f"name: {i.get('name')}")

        # #GET 요청 시도
        # try:
        #     response = requests.get(file)
        #     if response.status_code // 100 == 2:
        #         print(f"{file} supports GET method.")
        #     else:
        #         print(f"{file} does not support GET method.")
        # except Exception as e:
        #     print(f"Error occurred while attempting GET on {file}: {e}")

        # # POST 요청 시도
        # try:
        #     response = requests.post(file)
        #     if response.status_code // 100 == 2:
        #         print(f"{file} supports POST method.")
        #     else:
        #         print(f"{file} does not support POST method.")
        # except Exception as e:
        #     print(f"Error occurred while attempting POST on {file}: {e}")

        # # 일시적 점검을 위한 중단
        # break    
            

    return 
# def BlindSQLI():
#     return
# def TimeBasedSQLI():
#     return
# def ErrorBasedSQLI():
#     return
# def UNIONBasedSQLI():
#     return
# def OutofbandSQLI():
#     return
# def SecondOrderSQLI():
#     return


#main에서 매개변수로 전달된 check_url 받아와서 점검 항목 수행
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error code: check_url[1] 인자 전달받지 못함")
        sys.exit(1)
    # directories = json.loads(sys.argv[2])
    check_url = json.loads(sys.argv[1])

    #정적 콘텐츠 제공하는 확장자 제외(.jpg, .jpeg, .png, etc., .css, .js)
    static_extensions = {'.jpg', '.jpeg', '.png', '.css', '.js'}
    check_files = [file for file in check_url if os.path.splitext(file)[1] not in static_extensions]
    #print(f"check_files: {check_files}")

    classicSQLI(check_files)