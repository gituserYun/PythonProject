import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os, sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error code: URL[1] 인자 전달받지 못함")
        sys.exit(1)
    url = sys.argv[1]

    print(f"test_url: {url}")