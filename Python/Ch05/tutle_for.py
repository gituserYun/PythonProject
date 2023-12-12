import turtle
t = turtle.Turtle()

#정삼각형 그리기
for _ in range(3):
    t.forward(100)
    t.left(360/3) #360/3을 통해 120도로 왼쪽 틀기
    
#정사각형 그리기 위해서 터틀만 이동 시키기
t.penup() #펜 자국 남지 않도록 펜 들어서 이동
t.goto(200, 0)
t.pendown() #이동을 마치면 펜 내려놓기

#정사각형 그리기
for _ in range(4):
    t.forward(100)
    t.left(360/4)