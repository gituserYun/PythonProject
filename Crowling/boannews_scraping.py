# Web Site : https://www.boannews.com/media/t_list.asp , https://www.boannews.com/search/news_hash.asp?find=%BB%E7%B0%C7%BB%E7%B0%ED
import requests
import bs4

# 해당 주소로 요청 
# test-url: "http://192.168.107.128/login.jsp"
url = "https://www.boannews.com/media/t_list.asp"
req = requests.get(url, verify=False)
#print(req.text)

# 원하는 항목 스크래핑 하기 위한 python 패키지 이용(bs4;BeautifulSoup)
parse = bs4.BeautifulSoup(req.text, "html.parser")

# 원하는 항목 코드 부분 작성
# find(), find_all(), ...
BoanNews_Title = parse.find_all("span" , {"class" : "news_txt"})
BoanNews_Writer = parse.find_all("span" , {"class" : "news_writer"})
#print(len(BoanNews_Title))

print("\n\n\nBoanNews\n=============================================\n")
for title, writer in zip(BoanNews_Title, BoanNews_Writer):
    print(title.text)
    print(writer.text+"\n")
print("=============================================")