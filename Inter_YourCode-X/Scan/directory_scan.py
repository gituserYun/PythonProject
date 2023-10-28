import requests
import re
import os, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter

#Spider Scan방식
def spiderScan(target_url):
    try:
        response = requests.get(target_url, timeout=5)
        response.raise_for_status()  #에러 체크
    except requests.exceptions.RequestException as e:
        #status_code = response.status_code if 'response' in locals() else None
        #print(f"Non-responsive URL: {target_url}, Status Code: {status_code}")
        return
    except ValueError:
        #print(f"Invalid URL: {target_url}")
        return

    #방문 url 추가
    visited.add(target_url)
    #페이지의 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    #기본 url (스키마 + 네트워크 IP)
    if target_url.startswith(base_url):
        #태그 검사 - script(location.href, src), a(href), form(action), link(href), img(src)
        for tag in soup.find_all(['script', 'a', 'form', 'link', 'img', 'area', 'meta', 'embed', 'object']):
            if tag.name == 'script':
                if tag.string:
                    match_location = re.search(r'(window\s*\.\s*)?location\s*(\.\s*href|\.\s*replace)\s*(=\s*[\'"](.*?)[\'"]|\([\'"](.*?)[\'"]\))', tag.string, re.IGNORECASE)
                    if match_location and (match_location.group(4) or match_location.group(5)):
                        full_url = urljoin(target_url, match_location.group(4) or match_location.group(5))
                        print(f"script_location: {full_url}", file=sys.stdout)
                        if not full_url.startswith('#') and full_url not in visited:
                            spiderScan(full_url) #리다이렉트된 URL 재귀 호출

                match_src = tag.get('src')
                if match_src and not 'ionicons' in match_src:
                    full_url = urljoin(target_url, match_src)
                    path_with_extension = urlparse(full_url).path
                    print(f"script_src: {full_url}", file=sys.stdout)

                    #확장된 경로가 그룹화된 참조를 저장하는 사전 
                    if path_with_extension not in refer_dict:
                        refer_dict[path_with_extension] = [(full_url, response.status_code)]
                    else:
                        refer_dict[path_with_extension].append((full_url, response.status_code))

            elif tag.name == 'a':
                href_value = tag.get('href')
                if href_value and not href_value.startswith('#'):
                    full_url = urljoin(target_url, href_value)
                    print(f"a_href: {full_url}", file=sys.stdout)

                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

                    parsed_url = urlparse(full_url)

                    #추출한 문자열이 올바른 파일 이름인지 검사
                    if re.match(r'^[\w,\s-]+\.[A-Za-z0-9]+$', os.path.basename(path_with_extension)):
                        refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

                    #URL이 'http' 또는 'https'인지 확인
                    if parsed_url.scheme in ['http', 'https']:
                        if full_url not in visited:  #페이지를 방문하지 않은 경우 
                            spiderScan(full_url)  #페이지를 방문하는 재귀 호출

            elif tag.name == 'form':
                action_value = tag.get('action')
                if action_value and not action_value.startswith('#'):
                    full_url = urljoin(target_url, action_value)
                    print(f"form_action: {full_url}", file=sys.stdout)
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

            elif tag.name == 'link':
                href_value = tag.get('href')
                if href_value and not href_value.startswith('#'):
                    full_url = urljoin(target_url, href_value)
                    print(f"link_href: {full_url}", file=sys.stdout)
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

            elif tag.name == 'img':
                src_value = tag.get('src')
                if src_value and not src_value.startswith('#'):
                    full_url = urljoin(target_url, src_value)
                    print(f"img_src: {full_url}", file=sys.stdout)
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))
            #area 태그 관련(이미지 맵의 영역을 정의)
            elif tag.name == 'area':
                href_value = tag.get('href')
                if href_value and not href_value.startswith('#'):
                    full_url = urljoin(target_url, href_value)
                    print(f"area_href: {full_url}", file=sys.stdout)
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))
            #meta 태그 관련(웹 페이지에 대한 정보를 포함한 곳, 특정 상황 리다이렉션 용도)
            elif tag.name == 'meta':
                http_equiv_value = tag.get('http-equiv')
                content_value = tag.get('content')
                if http_equiv_value and http_equiv_value.lower() == "refresh" and content_value:
                    match_meta_refresh = re.search(r'url\s*=\s*(.*)$', content_value.strip(), re.IGNORECASE)
                    if match_meta_refresh:
                        full_url = urljoin(target_url, match_meta_refresh.group(1))
                        print(f"meta: {full_url}", file=sys.stdout)
                        path_with_extension = urlparse(full_url).path
                        refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))
            #embed, object 태그 관련(외부 멀티미디어 콘텐츠)
            elif tag.name in ['embed', 'object']:
                data_or_src_attr_val = tag.get('data') or tag.get('src')
                if data_or_src_attr_val and not data_or_src_attr_val.startswith('#'):
                    full_url = urljoin(target_url,data_or_src_attr_val)
                    print(f"embed&object: {full_url}", file=sys.stdout)
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))


#Dictionary Scan방식
# def dictionaryScan(target_url, parsed_url, max_ss_extension):

#     # directory-list-2.3-medium.txt를 읽어와서 폴더 및 파일 정보를 저장
#     dictionary_file = "../Scan/directory-list-2.3-medium.txt"
#     if not os.path.exists(dictionary_file):
#         print(f"Error: {dictionary_file} not found.")
#         return
#     else:
#         print(f"Success: {dictionary_file}")

#     with open(dictionary_file, 'r') as f:
#         directories = [line.strip() for line in f.readlines()]

#     # target_url에 대한 디렉터리 스트림 생성
#     #print(parsed_url)
#     base_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
#     if not parsed_url.path.endswith('/'):
#         base_url += '/'
#     # print(base_url)
#     # print(max_ss_extension)
#     # requests 세션 생성
#     session = requests.Session()

#     cnt = 0
#     for directory in directories:
#         # 해당 파일이 실제로 존재하는지 확인
#         # target_directory = os.path.join(base_url, directory) + '/'
#         file = directory + max_ss_extension
#         target_file = base_url + file
#         #print(f"target_directory: {target_directory}, target_file: {target_file}")
#         try:
#             response = session.head(target_file)
#             if response.status_code == 200:
#                 # cnt += 1
#                 print(f"FILE: /{file}", file=sys.stdout)
#                 # print(f"Detected: {target_file}, {cnt}")
#         except requests.exceptions.RequestException as e:
#             print(f"Error: {e}")



    # cnt = 0
    # for directory in directories:
    #     # 해당 디렉터리가 실제로 존재하는지와 확인된 경로가 디렉터리인지 검사
    #     target_directory = os.path.join(base_url, directory) + '/'
    #     # print(target_directory)
    #     response = requests.head(target_directory)
    #     if response.status_code == 200 or response.status_code == 302:
    #         cnt += 1
    #         print(f"Detected: {target_directory}, {cnt}")        
        # if os.path.exists(target_directory) and os.path.isdir(target_directory):
        #     cnt += 1
        #     print(f"Detected: {directory}, {cnt}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error code: URL[1] 인자 전달받지 못함")
        sys.exit(1)
    url = sys.argv[1]

    #파싱 및 스캔 실행(spiderScan())에 필요한 값
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc

    #파일 경로 및 확장된 경로가 그룹화된 참조를 저장하는 사전
    visited = set()
    refer_dict = {}

    #서버 디렉터리(폴더,파일) 탐색 함수(Spider Scan)
    spiderScan(url)

    directory_names = set()
    for path_with_extension, _ in refer_dict.items():
        path_parts = path_with_extension.split('/')
        if len(path_parts) > 1:
            directory_name = '/'.join(path_parts[:-1]) + '/'
            #디렉터리 이름이 올바른 형식인지 검사
            if not any(char in r":*\"<>" for char in directory_name):
                directory_names.add(directory_name)
    for dirname in directory_names:
        print(f"DIR: {dirname}", file=sys.stdout)
        # print(f"DIR: {dirname}")

    # 해당 서버의 예상되는 컨텐츠 확장자(웹 페이지, 이미지, 서버 스크립트, 웹 페이지 외부 콘텐츠 파일)
    web_extensions = {'.html', '.htm', '.php', '.jsp', '.asp', '.aspx',
                    '.css', '.js', '.jsx', '.vue', '.ts', '.tsx', '.scess',
                    '.less', '.png', '.jpg', '.jpeg', '.svg'}
    re_path = []
    for path_with_extension, references in refer_dict.items():
        _, ext = os.path.splitext(path_with_extension)
        if ext in web_extensions:
            re_path.append(path_with_extension)
            print(f"FILE: {path_with_extension}", file=sys.stdout)
            # print(f"FILE: {path_with_extension}")
            unique_references = set()  #set 타입을 사용하여 고유 참조 확인
            # for ref_info in references:
            #     full_url = ref_info[0]
            #     status_code = ref_info[1]
            #     unique_references.add((full_url, status_code))
            # for ref_info in unique_references:
            #     print(f"refer) {ref_info[0]}, Status Code: {ref_info[1]}")
    
    # print(f"re_path: {re_path}")

    # # re_path에서 확장자만 추출
    # extensions = [os.path.splitext(path)[1] for path in re_path]
    # #########
    # # 각 확장자별 등장 횟수 계산
    # # extension_counts = Counter(extensions)
    # # 출력
    # # for ext, count in extension_counts.items():
    # #     print(f"Extension: {ext}, Count: {count}")
    # ##########
    # # # 서버 스크립트 확장자 리스트
    # server_script_extensions = ['.php', '.jsp', '.asp', '.aspx', '.c', '.ssjs', '.py', '.rb', '.js']
    # # 서버 스크립트 확장자 중에서 등장한 횟수를 저장할 딕셔너리
    # server_script_counts = {ext: extensions.count(ext) for ext in server_script_extensions}
    # print(server_script_counts)
    # # 가장 많이 등장한 서버 스크립트 확장자 찾기
    # max_ss_extension = max(server_script_counts, key=server_script_counts.get)
    # max_ss_count = server_script_counts[max_ss_extension]
    # # 출력
    # print(f"Most Server Script Extension: {max_ss_extension}, Count: {max_ss_count}")     

    # #서버 디렉터리 탐색 함수(Dictionary Scan)
    # dictionaryScan(url, parsed_url, max_ss_extension) 


   