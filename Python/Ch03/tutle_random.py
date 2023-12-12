import turtle
import random

## 전역 변수 선언 부분 ##
swidth, sheight, pSize, exitCount = 300, 300, 3, 0
r, g, b, angle, dist, curX, curY = [0] * 7

## 메인 코드 부분 ##
turtle.title('거북이가 맘대로 다니기') # 창 제목
turtle.shape('turtle') # 거북이 모양
turtle.pensize(pSize) # 펜 두께 (3)
turtle.setup(width = swidth + 30, height = sheight + 30) # 윈도우 창 크기 (330, 330)
turtle.screensize(swidth, sheight)

while True:
    r = random.random()
    g = random.random()
    b = random.random()
    turtle.pencolor((r,g,b))
    
    angle = random.randrange(0, 360) # 각도 0~360 범위
    dist = random.randrange(1, 100) # 거리 1~100 범위
    turtle.left(angle) # 거북이 각도 설정
    turtle.forward(dist) # 거리 이동
    curX = turtle.xcor() # 거북이 현재 위치 구함
    curY = turtle.ycor() 
    
    # 거북이의 현재 위치가 화면 안인지 체크, 터틀 그래픽의 중앙이 (0,0)
    if((-swidth/2 <= curX and curX <= swidth/2) and (-sheight/2 <= curY and curY <= sheight/2)):
        pass # pass 실행해서 if문 그냥 종료
    else:
        turtle.penup() # 펜사용 하지 않음
        turtle.goto(0,0) # 화면의 중앙으로 이동
        turtle.pendown() # 다시 펜 사용
        
        exitCount += 1
        if exitCount >= 5:
            break