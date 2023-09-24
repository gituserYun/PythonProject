import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os, sys

#Spider Scan방식
def dirSearch(target_url):
    print(f"test_url1: {target_url}")

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
