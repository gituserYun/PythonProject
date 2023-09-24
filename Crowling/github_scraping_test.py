import requests
import re
import json

github_url = "https://github.com/gituserYun/exploit_code/blob/master/SQLI/classic_sqli.txt"
response = requests.get(github_url)

if response.status_code == 200:
    text = response.text
    
    # textarea 내용만 추출하기
    start_marker = "### Classic SQL Injection ###"
    end_marker = "### Refer to... ###"
    
    start_index = text.find(start_marker)
    end_index = text.find(end_marker)
    
    if start_index != -1 and end_index != -1:
        content = text[start_index:end_index]
        print(content)
    else:
        print("Markers not found in the text.")
else:
    print("Failed to fetch GitHub code.")