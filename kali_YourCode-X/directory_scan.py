import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os, sys

#Spider Scan방식
def dirSearch(target_url):
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
                        #print(f"script_location: {full_url}")
                        if not full_url.startswith('#') and full_url not in visited:
                            dirSearch(full_url) #리다이렉트된 URL 재귀 호출

                match_src = tag.get('src')
                if match_src and not 'ionicons' in match_src:
                    full_url = urljoin(target_url, match_src)
                    path_with_extension = urlparse(full_url).path
                    #print(f"script_src: {full_url}")

                    #확장된 경로가 그룹화된 참조를 저장하는 사전 
                    if path_with_extension not in refer_dict:
                        refer_dict[path_with_extension] = [(full_url, response.status_code)]
                    else:
                        refer_dict[path_with_extension].append((full_url, response.status_code))

            elif tag.name == 'a':
                href_value = tag.get('href')
                if href_value and not href_value.startswith('#'):
                    full_url = urljoin(target_url, href_value)
                    #print(f"a_href: {full_url}")

                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

                    parsed_url = urlparse(full_url)

                    #추출한 문자열이 올바른 파일 이름인지 검사
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
                    #print(f"form_action: {full_url}")
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

            elif tag.name == 'link':
                href_value = tag.get('href')
                if href_value and not href_value.startswith('#'):
                    full_url = urljoin(target_url, href_value)
                    #print(f"link_href: {full_url}")
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))

            elif tag.name == 'img':
                src_value = tag.get('src')
                if src_value and not src_value.startswith('#'):
                    full_url = urljoin(target_url, src_value)
                    #print(f"img_src: {full_url}")
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))
            #area 태그 관련(이미지 맵의 영역을 정의)
            elif tag.name == 'area':
                href_value = tag.get('href')
                if href_value and not href_value.startswith('#'):
                    full_url = urljoin(target_url, href_value)
                    #print(f"area_href: {full_url}")
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
                        #print(f"meta: {full_url}")
                        path_with_extension = urlparse(full_url).path
                        refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))
            #embed, object 태그 관련(외부 멀티미디어 콘텐츠)
            elif tag.name in ['embed', 'object']:
                data_or_src_attr_val = tag.get('data') or tag.get('src')
                if data_or_src_attr_val and not data_or_src_attr_val.startswith('#'):
                    full_url = urljoin(target_url,data_or_src_attr_val)
                    #print(f"embed&object: {full_url}")
                    path_with_extension = urlparse(full_url).path
                    refer_dict.setdefault(path_with_extension, []).append((full_url, response.status_code))



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error code: URL[1] 인자 전달받지 못함")
        sys.exit(1)
    url = sys.argv[1]

    #파싱 및 스캔 실행(dirSearch())에 필요한 값
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    #파일 경로 및 확장된 경로가 그룹화된 참조를 저장하는 사전
    visited = set()
    refer_dict = {}

    #서버 디렉터리(폴더,파일) 탐색 함수
    dirSearch(url)

    print("Directory Names:")
    print("===========")
    directory_names = set()

    for path_with_extension, _ in refer_dict.items():
        path_parts = path_with_extension.split('/')
        if len(path_parts) > 1:
            directory_name = '/'.join(path_parts[:-1]) + '/'
            #디렉터리 이름이 올바른 형식인지 검사
            if not any(char in r":*\"<>" for char in directory_name):
                directory_names.add(directory_name)

    for dirname in directory_names:
        print(f"{dirname}")

    print("\nFilename:")
    print("===========")
    web_extensions = {'.html', '.htm', '.php', '.jsp', '.asp', '.aspx',
                    '.css', '.js',
                    '.png', '.jpg', '.jpeg', '.svg'}

    #main으로 리턴해줄 해당 디렉토리 경로
    re_path = []
    for path_with_extension, references in refer_dict.items():
        _, ext = os.path.splitext(path_with_extension)

        if ext in web_extensions:
            re_path.append(path_with_extension)
            print(f"{path_with_extension}")
            #print(f"-> {path_with_extension}")
            unique_references = set()  #set 타입을 사용하여 고유 참조 확인
            # for ref_info in references:
            #     full_url = ref_info[0]
            #     status_code = ref_info[1]
            #     unique_references.add((full_url, status_code))
            # for ref_info in unique_references:
            #     print(f"refer) {ref_info[0]}, Status Code: {ref_info[1]}")    