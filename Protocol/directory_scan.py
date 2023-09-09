import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import os

#target_url: "http://192.168.107.130/"
target_url = "http://192.168.107.128/write.jsp"
response = requests.get(target_url)
#print(response.text)

#set type filenames
filenames_set = set()

#check if the request to the target url
st_code = response.status_code

if st_code == 200:
    #HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #find the tags
    #다양한 태그들에 대한 속성에 URL을 지정하는 것을 이벤트 처리해야 함
    script_tags = soup.find_all('script')
    a_tags = soup.find_all('a')
    form_tags = soup.find_all('form')
    #print(f"{script_tags} /\n\n{a_tags} /\n\n {form_tags}\n\n")


    #script(location.href, src)
    for script_tag in script_tags:
        #location.href 
        if script_tag.string:
            match_location= re.search(r'location.href\s*=\s*[\'"](.*?)[\'"]', script_tag.string)
            if match_location and not match_location.group(1).startswith('#'):
                #remove query string(? -> url without query string)
                rm_query = urlparse(match_location.group(1)).path  
                filename_only= os.path.basename(rm_query)
                filenames_set.add(filename_only)

        #src 
        match_src= script_tag.get('src')
        if match_src and not 'https://' in match_src:
            filename_only= os.path.basename(match_src)
            filenames_set.add(filename_only)

    #a(href)
    for a_tag in a_tags:
        href_value= a_tag.get('href')
        if href_value and not href_value.startswith('#'):
            #remove query string(? -> url without query string)
            rm_query= urlparse(href_value).path  
            filename_only= os.path.basename(rm_query)
            filenames_set.add(filename_only)   

    #form(action)
    for form_tag in form_tags:
        action_value=form_tag.get('action')
        if action_value and not action_value.startswith('#'):
            #remove query string(? -> url without query string)
            rm_query=urlparse(action_value).path  
            filename_only=os.path.basename(rm_query)
            filenames_set.add(filename_only)

else:  #not 200 status code.
    print(f"Failed to retrieve {target_url}. Status code: {response.status_code}")

#print result.
print("Filename: ")
for filename in filenames_set:
    print(f"-> {filename}")
print(len(filenames_set))
