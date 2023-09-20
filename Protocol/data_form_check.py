from bs4 import BeautifulSoup
import requests

target_url = 'http://192.168.107.128/login.jsp'
response = requests.get(target_url)
soup = BeautifulSoup(response.text, 'html.parser')

#form 태그 찾기 + input, textarea, select, button
form = soup.find('form')
inputs = form.find_all('input')
textareas = form.find_all('textarea')
selects = form.find_all('select')
buttons = form.find_all('button')

#데이터 전송과 목적지 확인
method = form.get('method', '').upper()
action = form.get('action','')
print(f"|Form method|: \n{method}\n")
print(f"|Form action|\n{action}")

#각 태그 속성 데이터 식별
print("\n|Input field|")
for i in inputs:
    print(f"name: {i.get('name')}, type: {i.get('type')}")

print("\n|Textarea field|")
for i in textareas:
    print(f"name: {i.get('name')}")

print("\n|Selects field|")
for i in selects:
    print(f"name: {i.get('name')}")

print("\n|button field|")
for i in buttons:
    print(f"name: {i.get('name')}")
