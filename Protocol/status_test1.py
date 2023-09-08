import requests
from urllib.parse import urlsplit


#test_url: "http://192.168.107.128/"
target_url = "http://192.168.107.130/main.jsp"
response = requests.get(target_url)

#GET / POST
#data_type = response.request.method

#status code
st_code = response.status_code
#protocol version
protocol = ""
if response.url.startswith("https://"):
    protocol = "HTTPS"
else:
    protocol = "HTTP"
pro_version = response.raw.version
formatted_version = f"{int(pro_version / 10)}.{pro_version % 10}"
#print(f"{data_type} {protocol}/{formatted_version}")
print(f"{protocol}/{formatted_version} {st_code}")

#data header
date_header = response.headers['Date']
print(f"Date: {date_header}")

#cookie header
cookie_header = response.headers["Set-Cookie"]
print(f"Set-Cookie: {cookie_header}")

#vary header
vary_hader = response.headers["Vary"]
print(f"Vary: {vary_hader}")

#content length
content_length = response.headers["Content-Length"]
print(f"Content-Length: {content_length}")

#connection length
connection = response.headers["Connection"]
print(f"Connection: {connection}")

#content type
content_type = response.headers['Content-Type']
print(f"Content-Type: {content_type}")



# #host information
# url = response.url
# parsed_url = urlsplit(url)
# host_netloc = parsed_url.netloc
# #ip_address_with_path = parsed_url.netloc + parsed_url.path
# print(f"Host: {host_netloc}")
# print(f"Referer: {url}")




# code = response.text
# url = response.url
# st_code = response.status_code
# server = response.headers["Server"]
# cookie = response.headers["Set-Cookie"]
# vary = response.headers["Vary"]
# content_encoding = response.headers["Content-Encoding"]
# content_length = response.headers["Content-Length"]
# keep_alive = response.headers["Keep-Alive"]
# connection = response.headers["Connection"]
# content_type = response.headers['Content-Type']

