# import requests
# from bs4 import BeautifulSoup
# import re
# from urllib.parse import urljoin, urlparse
# import os

# #set()타입 지정&방문할 url 지정
# filenames_set = set()
# visited = set()

# #서버 디렉터리 탐색
# def directorySearch(target_url):
#     #방문 url 추가
#     visited.add(target_url)
#     response = requests.get(target_url)
    
#     #대상 url에 대한 요청 성공 여부 확인
#     st_code = response.status_code
    
#     if st_code == 200:
#         #페이지의 HTML
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         #태그 검사
#         script_tags = soup.find_all('script')
#         a_tags = soup.find_all('a')
#         form_tags = soup.find_all('form')
#         # print(f"{script_tags} \n")
#         # print(f"{a_tags} \n")
#         # print(f"{form_tags} \n")

#         #script(location.href, src)
#         for script_tag in script_tags:
#             if script_tag.string:
#                 match_location= re.search(r'location.href\s*=\s*[\'"](.*?)[\'"]', script_tag.string)
#                 if match_location and not match_location.group(1).startswith('#'):
#                     full_url = urljoin(target_url, match_location.group(1))
#                     directorySearch(full_url)  # 리다이렉트된 URL 재귀 호출

#             match_src= script_tag.get('src')
#             if match_src and not 'ionicons' in match_src:
#                 filename_only= os.path.basename(match_src)
#                 filenames_set.add(filename_only)

#         # a(href)
#         for a_tag in a_tags:
#             href_value = a_tag.get('href')
#             if href_value and not href_value.startswith('#'):
#                 full_url = urljoin(target_url, href_value)
                
#                 url_without_query_string = urlparse(href_value).path  
#                 filename_only = os.path.basename(url_without_query_string)
#                 filenames_set.add(filename_only)   

#                 parsed_url = urlparse(full_url)
                
#                 #추출한 문자열이 올바른 파일 이름인지 검사
#                 match_valid_filename = re.match(r'^[\w,\s-]+\.[A-Za-z0-9]+$', filename_only)
#                 if match_valid_filename:
#                     filenames_set.add(filename_only) 

#                 parsed_url = urlparse(full_url)
                
#                 #URL이 'http' 또는 'https'인지 확인합니다
#                 if parsed_url.scheme in ['http', 'https']:
#                     if full_url not in visited:  #페이지를 방문하지 않은 경우
#                         directorySearch(full_url)  #페이지를 방문하는 재귀 호출문

#         for form_tag in form_tags:
#             action_value=form_tag.get('action')
#             if action_value and not action_value.startswith('#'):
#                 url_without_query_string=urlparse(action_value).path  
#                 filename_only=os.path.basename(url_without_query_string)
#                 filenames_set.add(filename_only)

#     else:  #200 상태 코드가 아닌 부분
#         print(f"Failed to retrieve {target_url}. Status code: {response.status_code}")

# #start directory search
# directorySearch("http://192.168.107.128/")

# #print result.
# print("Filename: ")
# for filename in filenames_set:
#       print(f"-> {filename}")
# print(len(filenames_set))

# import requests
# from bs4 import BeautifulSoup
# import re
# from urllib.parse import urljoin, urlparse
# import os

# #set()타입 지정&방문할 url 지정
# filenames_set = set()
# visited = set()

# #서버 디렉터리 탐색
# def directorySearch(target_url):
#     #방문 url 추가
#     visited.add(target_url)
    
#     try:
#         response = requests.get(target_url, timeout=5)
#         response.raise_for_status()  #에러 체크
#     except (requests.RequestException, ValueError):
#         print(f"Skipping invalid or non-responsive URL: {target_url}")
#         return

#     #페이지의 HTML 파싱
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     #태그 검사 - script(location.href, src), a(href), form(action), link(href), img(src)
#     for tag in soup.find_all(['script', 'a', 'form', 'link', 'img']):
        
#         if tag.name == 'script':
#             if tag.string:
#                 match_location= re.search(r'location.href\s*=\s*[\'"](.*?)[\'"]', tag.string)
#                 if match_location and not match_location.group(1).startswith('#'):
#                     full_url = urljoin(target_url, match_location.group(1))
#                     print(f"script_location: {full_url}")
#                     directorySearch(full_url)  # 리다이렉트된 URL 재귀 호출
                    

#             match_src= tag.get('src')
#             if match_src and not 'ionicons' in match_src:
#                 full_url = urljoin(target_url, match_src)
#                 filename_only= os.path.basename(match_src)
#                 filenames_set.add((filename_only, full_url ,response.status_code))

#         # elif tag.name == 'a':
#         #     href_value = tag.get('href')
#         #     if href_value and not href_value.startswith('#'):
#         #         full_url = urljoin(target_url, href_value)

#         #         url_without_query_string=urlparse(href_value).path  
#         #         filename_only=os.path.basename(url_without_query_string)
#         #         filenames_set.add((filename_only,response.status_code))

#         elif tag.name == 'a':
#             href_value = tag.get('href')
#             if href_value and not href_value.startswith('#'):
#                 full_url = urljoin(target_url, href_value)
                
#                 path_only = urlparse(full_url).path
#                 filenames_set.add((path_only, full_url, response.status_code))

#                 parsed_url=urlparse(full_url)

#                 # 추출한 문자열이 올바른 파일 이름인지 검사
#                 if re.match(r'^[\w,\s-]+\.[A-Za-z0-9]+$', os.path.basename(path_only)):
#                     filenames_set.add((path_only, full_url, response.status_code))
#                 # if re.match(r'^[\w,\s-]+\.[A-Za-z0-9]+$',filename_only):
#                 #     filenames_set.add((filename_only,response.status_code))

#                 parsed_url=urlparse(full_url)

#                 #URL이 'http' 또는 'https'인지 확인합니다.
#                 if parsed_url.scheme in ['http','https']:
#                     if full_url not in visited:  # 페이지를 방문하지 않은 경우 
#                         directorySearch(full_url)  # 페이지를 방문하는 재귀 호출

#         elif tag.name=='form':  
#             action_value=tag.get('action') 
#             if action_value and not action_value.startswith('#'):
#                 full_url = urljoin(target_url, action_value)
#                 url_without_query_string=urlparse(action_value).path   
#                 filename_only=os.path.basename(url_without_query_string)   
#                 filenames_set.add((url_without_query_string, full_url, response.status_code))

#         elif tag.name=='link':  
#             href_value=tag.get('href') 
#             if href_value and not href_value.startswith('#'):   
#                 full_url = urljoin(target_url, href_value)
#                 url_without_query_string=urlparse(href_value).path   
#                 filename_only=os.path.basename(url_without_query_string)   
#                 filenames_set.add((url_without_query_string, full_url, response.status_code))

#         elif tag.name=='img':  
#             src_value=tag.get('src') 
#             if src_value and not src_value.startswith('#'):
#                 full_url = urljoin(target_url, src_value)   
#                 url_without_query_string=urlparse(src_value).path   
#                 filename_only=os.path.basename(url_without_query_string)   
#                 filenames_set.add((url_without_query_string, full_url, response.status_code))

# # start directory search    
# directorySearch("http://192.168.107.128/")

# # print result.
# print("Filename:")
# web_extensions = {'.html', '.htm', '.php', '.jsp', '.asp', '.aspx',
#                   '.css', '.js',
#                   '.png', '.jpg', '.jpeg', 'svg',
#                   }

# for filename_info in filenames_set:
#     path_only = filename_info[0]
#     full_filename = filename_info[1]
#     status_code = filename_info[2]

#     #첫번째 요소(확장자 제외한 파일 경로), 두번째 요소(확장자)
#     _, ext = os.path.splitext(path_only)

#     if ext in web_extensions:
#         print(f"-> {path_only}")
#         print(f"refer) {full_filename}, Status Code: {status_code}\n")
        
#     # elif ext == '':references_dict
#     #     print(f"-> (Possible Directory) {filename_only}, Status Code: {status_code}")

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os

#파일 경로 및 확장된 경로가 그룹화된 참조를 저장하는 사전
refer_dict = {}
visited = set()

#서버 디렉터리(폴더,파일) 탐색
def dirSearch(target_url):
    #방문 url 추가
    visited.add(target_url)

    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status()  #에러 체크
    except requests.exceptions.RequestException as e:
        # status_code = response.status_code if 'response' in locals() else None
        # print(f"Non-responsive URL: {target_url}, Status Code: {status_code}")
        return
    except ValueError:
        # print(f"Invalid URL: {target_url}")
        return

    #페이지의 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    #태그 검사 - script(location.href, src), a(href), form(action), link(href), img(src)
    for tag in soup.find_all(['script', 'a', 'form', 'link', 'img']):

        if tag.name == 'script':
            if tag.string:
                match_location = re.search(r'location.href\s*=\s*[\'"](.*?)[\'"]', tag.string)
                if match_location and not match_location.group(1).startswith('#'):
                    full_url = urljoin(target_url, match_location.group(1))
                    # print(f"script_location: {full_url}")
                    if full_url not in visited:
                        dirSearch(full_url)  #리다이렉트된 URL 재귀 호출

            match_src = tag.get('src')
            if match_src and not 'ionicons' in match_src:
                full_url = urljoin(target_url, match_src)
                path_with_extension = urlparse(full_url).path

                #확장된 경로가 그룹화된 참조를 저장하는 사전 
                if path_with_extension not in refer_dict:
                    refer_dict[path_with_extension] = [(full_url, response.status_code)]
                else:
                    refer_dict[path_with_extension].append((full_url, response.status_code))

        elif tag.name == 'a':
            href_value = tag.get('href')
            if href_value and not href_value.startswith('#'):
                full_url = urljoin(target_url, href_value)
                
                path_with_extension = urlparse(full_url).path
                refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

                parsed_url = urlparse(full_url)

                # 추출한 문자열이 올바른 파일 이름인지 검사
                if re.match(r'^[\w,\s-]+\.[A-Za-z0-9]+$', os.path.basename(path_with_extension)):
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

                #URL이 'http' 또는 'https'인지 확인
                if parsed_url.scheme in ['http', 'https']:
                    if full_url not in visited:  #페이지를 방문하지 않은 경우 
                        dirSearch(full_url)  #페이지를 방문하는 재귀 호출

        elif tag.name == 'form':
            action_value = tag.get('action')
            if action_value and not action_value.startswith('#'):
                full_url = urljoin(target_url, action_value)
                path_with_extension = urlparse(full_url).path
                refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

        elif tag.name == 'link':
            href_value = tag.get('href')
            if href_value and not href_value.startswith('#'):
                full_url = urljoin(target_url, href_value)
                path_with_extension = urlparse(full_url).path
                refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

        elif tag.name == 'img':
            src_value = tag.get('src')
            if src_value and not src_value.startswith('#'):
                full_url = urljoin(target_url, src_value)
                path_with_extension = urlparse(full_url).path
                refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

#타깃 URL
dirSearch("http://192.168.107.128/")

#출력
print("Filename:")
web_extensions = {'.html', '.htm', '.php', '.jsp', '.asp', '.aspx',
                  '.css', '.js',
                  '.png', '.jpg', '.jpeg', '.svg'}

for path_with_extension, references in refer_dict.items():
    _, ext = os.path.splitext(path_with_extension)

    if ext in web_extensions:
        print(f"\n-> {path_with_extension}")
        unique_references = set()  #set 타입을 사용하여 고유 참조 확인
        for ref_info in references:
            full_url = ref_info[0]
            status_code = ref_info[1]
            unique_references.add((full_url, status_code))
        for ref_info in unique_references:
            print(f"refer) {ref_info[0]}, Status Code: {ref_info[1]}")