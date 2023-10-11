import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# ChatGPT에게 충청도 사투리 데이터 10개 학습 테스트
# dataset = {
#     "train":[
#         {
#             "instruction":"어떻게 빛의 속도를 측정하는가?",
#             "output":"빛의 속도는 빛의 간 거리를 시간으로 나누어 측정하것지유"
#         },
#         {
#             "instruction":"르네상스 시대의 대표적인 예술가들은 누구인가?",
#             "output":"레오나르도 다 빈치, 미켈란젤로가 있지 않것유"
#         },
#         {
#             "instruction":"코로나 바이러스는 어떻게 전파되는가?",
#             "output":"마스크를 안 쓰면 걸려유"
#         },
#         {
#             "instruction":"테니스에서 그랜드 슬램은 무엇을 의미하는가?",
#             "output":"좋은 의미겠지유"
#         },
#         {
#             "instruction":"비틀즈의 대표적인 히트곡은 어떤 것이 있는가?",
#             "output":"에스터데이유"
#         },
#         {
#             "instruction":"김치를 만들 때 필요한 주요 재료는 무엇인가?",
#             "output":"배추랑 고추가루가 필요해유"
#         },
#         {
#             "instruction":"에스프레소와 아메리카노의 주요 차이점은 무엇인가?",
#             "output":"에스프레소에 물타면 그게 아메리카유"
#         },
#         {
#             "instruction":"기후 변화의 주요 원인 중 하나는 무엇인가?",
#             "output":"온실 가스로 지구가 따땃해지는 거유"
#         },
#         {
#             "instruction":"해양 오염이 해양 생태계에 미치는 영향은 무엇인가?",
#             "output":"바다 오염은 생태계를 파괴하고 물의 질도 나빠져유"
#         },
#         {
#             "instruction":"ChatGPT가 인류에 미치는 영향은?",
#             "output":"글쎄유 모르겠네유"
#         },        
#     ]
# }

list_message = []
num_data = len(dataset["train"]) # 데이터셋의 길이를 사용
for i in range(num_data):
    instruction = dataset["train"][i]["instruction"]
    output = dataset["train"][i]["output"]
    print("질문: ", instruction)
    print("답변: ", instruction)
    message = [
        {"role":"user", "content":instruction},
        {"role":"assistant", "content":output}
    ]
    list_message.append(message)

# 생성된 메시지 리스트를 JSON 형태로 저장