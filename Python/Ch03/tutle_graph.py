import turtle
t = turtle.Turtle()
t.shape("turtle")
n = int(input("몇 각형을 그리겠어요?(3-6): "))

for i in range(n):
    t.forward(100)
    t.left(360//n)
    
turtle.done()