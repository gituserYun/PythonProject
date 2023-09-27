import os
import openai

openai.api_key = "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"

messages=[]
user_content = input("prompt: ")
messages.append({"prompt":"user1", "content":f"{user_content}"})

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)


# openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     #{"role": "user", "content": "Hello!"} #역할에 해당하는 컨텐츠(작성된 값)
#   ]
# )