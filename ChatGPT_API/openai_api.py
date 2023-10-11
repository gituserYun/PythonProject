import os
import openai

# 현재 세션 유지 명령어 powershell> $env:OPENAI_API_KEY = "해당 API키"
openai.api_key = os.getenv("OPENAI_API_KEY")

# "role":"user" -> 사용자가 입력할 프롬프트를 설정
# "role":"system" -> chat봇의 특성을 정의
# "role":"assistant" -> 챗봇의 대답을 설정

messages=[]
while True:
    # 유저가 보낼 메시지 리스트에 저장
    user_content = input("prompt: ")
    messages.append({"role":"user", "content":f"{user_content}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    # OpenAI API의 응답에서 챗봇의 답변을 추출하는 역할
    assistant_content = completion.choices[0].message["content"].strip()
    messages.append({"role":"assistant", "content":f"{assistant_content}"})

    print("===============================")
    print(f"ChatGPT: \n{assistant_content}")
    print("===============================")



# openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     #{"role": "user", "content": "Hello!"} #역할에 해당하는 컨텐츠(작성된 값)
#   ]
# )