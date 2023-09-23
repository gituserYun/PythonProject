import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os, sys

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
    
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error code: URL[1] 인자 전달받지 못함")
        sys.exit(1)
    url = sys.argv[1]

    print(f"test_url: {url}")

    #파일 경로 및 확장된 경로가 그룹화된 참조를 저장하는 사전
    visited = set()
    refer_dict = {}

    #서버 디렉터리(폴더,파일) 탐색 함수
    dirSearch(url)