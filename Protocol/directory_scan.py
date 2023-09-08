import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import os

#test_url: "http://192.168.107.128/"
target_url = "http://192.168.107.130/"
response = requests.get(target_url)

#set type filenames
filenames_set = set()

#check if the request to the target url
st_code = response.status_code
if st_code == 200:
    #HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #[script, a, ...]
    #find the 
    script_tags = soup.find_all('script')
    a_tags = soup.find_all('a')
    print(script_tags)
    # print()
    # print(a_tags)
    
    #match[location.href, href, src, ]
    for script_tag in script_tags:
        # match 'src'
        match_src = script_tag.get('src')
        if match_src:
            match = re.search(r'[^/]+$', match_src)
            if match:
                filename = match.group(0)
                filenames_set.add(filename)           
# print result
# print("Filename(script_src): ")
# for filename in filenames_set:
#     print(f"-> {filename}")
# print(len(filenames_set))
    
print("Filename(script_location): ")
for filename in filenames_set:
    print(f"-> {filename}")
print(len(filenames_set))
    
    # for script_tag in script_tags:
    #     match = re.search(r'location.href\s*=\s*[\'"](.*?)[\'"]', script_tag.string)
    #     if match:
    #         redirect_url = match.group(1)

    #         full_url = urljoin(target_url, redirect_url)
    #         filename_only = os.path.basename(full_url)
            
    #         #print(f"Redirecting to: {full_url}")
    #         print(f"Filename(script): {filename_only}")
            
#     for a_tag in a_tags:
#         # match 'href'
#         match_href = a_tag.get('href')
#         if match_href:
#             match = re.search(r'[^/]+$', match_href)
#             if match:
#                 filename = match.group(0)
#                 filenames_set.add(filename)
# else:
#     print(f"Failed to retrieve {target_url}. Status code: {response.status_code}")

# # print result
# print("Filename(a_href): ")
# for filename in filenames_set:
#     print(f"-> {filename}")
# print(len(filenames_set))
