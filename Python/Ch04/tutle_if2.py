import turtle

t = turtle.Turtle()
# 커서의 모양을 거북이로
t.shape("turtle")
#거북이가 그리는 선의 두께를 설정
t.width(3)
t.shapesize(3,3)

#무한 루프
while True:
    command = input("명령을 입력하세요: ")
    if command == "1":
        t.left(90)
        t.forward(100)
    if command == "r":
        t.right(90)
        t.forward(100)
            