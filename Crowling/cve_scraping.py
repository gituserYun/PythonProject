import requests
from bs4 import BeautifulSoup


# Cloudflare의 보안 서비스에 의해 접근이 차단되었다는 메시지가 출력되어서 다음과 같이 사용함
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

url = "https://www.cvedetails.com/vulnerabilities-by-types.php"
req = requests.get(url, headers=headers, verify=True)
soup = BeautifulSoup(req.text, 'html.parser')

# 'body' 태그 내에서 'table' 태그
tables = soup.body.find_all('table')
# 테이블을 선택
table = tables[0] 
# 테이블 모든 tr 태그
rows = table.find_all('tr')

data = {}
for row in rows:
    th = row.find('th')
    a = th.find('a') if th else None
    if a:
        year = a.text.strip()
        # 만약 추출한 텍스트가 '2023'라면,
        if year == '2023':
            tds = row.find_all('td')
            for td in tds:
                a = td.find('a')
                if a:
                    # 'a' 태그의 'title' 속성을 key로, 텍스트를 value로 하는 항목을 데이터에 추가합니다.
                    key = a.get('title').replace(' vulnerabilities for 2023', '')  # replace 함수를 사용하여 ' vulnerabilities for 2023' 부분을 제거합니다.
                    value = a.text.strip()
                    data[key] = value

print(data)

# # 각 행을 반복하며 처리합니다.
# for row in rows:
#     # 'th' 태그를 찾습니다.
#     th = row.find('th')
#     # 'th' 태그 내의 'a' 태그를 찾습니다.
#     a = th.find('a') if th else None
#     # 'a' 태그가 있으면,
#     if a:
#         # 'a' 태그의 텍스트를 추출합니다.
#         year = a.text.strip()
#         # 만약 추출한 텍스트가 '2023'라면,
#         if year == '2023':
#             # 해당 행에서 'td' 태그의 텍스트를 모두 출력합니다.
#             data = [td.text.strip() for td in row.find_all('td')]
#             print(data)