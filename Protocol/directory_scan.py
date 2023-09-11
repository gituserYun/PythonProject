import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os

#set()타입 지정&방문할 url 지정
filenames_set = set()
visited = set()

#서버 디렉터리 탐색
def crawl(target_url):
    #방문 url 추가
    visited.add(target_url)
    response = requests.get(target_url)
    
    #대상 url에 대한 요청 성공 여부 확인
    st_code = response.status_code
    
    if st_code == 200:
        #페이지의 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #태그 검사
        script_tags = soup.find_all('script')
        a_tags = soup.find_all('a')
        form_tags = soup.find_all('form')

        #script(location.href, src)
        for script_tag in script_tags:
            if script_tag.string:
                match_location= re.search(r'location.href\s*=\s*[\'"](.*?)[\'"]', script_tag.string)
                if match_location and not match_location.group(1).startswith('#'):
                    url_without_query_string= urlparse(match_location.group(1)).path  
                    filename_only= os.path.basename(url_without_query_string)
                    filenames_set.add(filename_only)

            match_src= script_tag.get('src')
            if match_src and not 'ionicons' in match_src:
                filename_only= os.path.basename(match_src)
                filenames_set.add(filename_only)

        # a(href)
        for a_tag in a_tags:
            href_value = a_tag.get('href')
            if href_value and not href_value.startswith('#'):
                full_url = urljoin(target_url, href_value)
                
                url_without_query_string = urlparse(href_value).path  
                filename_only = os.path.basename(url_without_query_string)
                filenames_set.add(filename_only)   

                parsed_url = urlparse(full_url)
                
                #추출한 문자열이 올바른 파일 이름인지 검사
                match_valid_filename = re.match(r'^[\w,\s-]+\.[A-Za-z0-9]+$', filename_only)
                if match_valid_filename:
                    filenames_set.add(filename_only) 

                parsed_url = urlparse(full_url)
                
                #URL이 'http' 또는 'https'인지 확인합니다
                if parsed_url.scheme in ['http', 'https']:
                    if full_url not in visited:  #페이지를 방문하지 않은 경우
                        crawl(full_url)  #페이지를 방문하는 재귀 호출문

        for form_tag in form_tags:
            action_value=form_tag.get('action')
            if action_value and not action_value.startswith('#'):
                url_without_query_string=urlparse(action_value).path  
                filename_only=os.path.basename(url_without_query_string)
                filenames_set.add(filename_only)

    else:  #200 상태 코드가 아닌 부분
        print(f"Failed to retrieve {target_url}. Status code: {response.status_code}")

#start crawling
crawl("http://192.168.107.128/bbs.jsp")

#print result.
print("Filename: ")
for filename in filenames_set:
      print(f"-> {filename}")
print(len(filenames_set))