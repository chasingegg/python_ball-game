from Tkinter import*
from time import*
from math import*
import tkFont
import random

root = Tk()
c = Canvas(root, width = 470, height = 470, relief = "raised")
ballplay_enable = 0



class Ball_Mode2:
    def __init__(self, canvas, paddle1, paddle2, color):
        self.canvas = canvas
        self.paddle1 = paddle1
        self.paddle2 = paddle2
        self.id = canvas.create_oval(10, 10, 25, 25, fill = color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2.5, -2, -1.5, 1, 1.5, 2, 2.5, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_wall = False
        self.who_win = 0
	
    def hit_paddle(self, pos):
        paddle_pos1 = self.canvas.coords(self.paddle1.id)
        paddle_pos2 = self.canvas.coords(self.paddle2.id)

        if pos[3] >= paddle_pos1[1] and pos[1] <= paddle_pos1[3] and pos[0] <= paddle_pos1[2] and pos[0] >= paddle_pos1[0]:
            return 2
        elif pos[3] >= paddle_pos2[1] and pos[1] <= paddle_pos2[3] and pos[2] >= paddle_pos2[0] and pos[2] <= paddle_pos2[2]:
            return 1
        return 0

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos =  self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 3 
        if pos[3] >= self.canvas_height:
            self.y = -3
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.hit_wall = True
            if pos[0] <= 0:
                self.who_win = 1
            else:
                self.who_win = 0
        x = self.hit_paddle(pos)
        if x != 0:	
            self.x = 3 *((-1) ** x)

class Paddle_Mode2:
    def __init__(self, canvas, x, y, left_or_right, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + 10, y + 100, fill = color)
        self.color = color
        self.speed = 0
        self.exist = True
        self.canvas_height = self.canvas.winfo_height()
        if left_or_right == 0:
            self.canvas.bind_all('<KeyPress-w>', self.turn_up)
            self.canvas.bind_all('<KeyPress-s>', self.turn_down)
            self.canvas.bind_all('<KeyRelease-w>', self.turn_up_stop)
            self.canvas.bind_all('<KeyRelease-s>', self.turn_down_stop)
        else:
            self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
            self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
            self.canvas.bind_all('<KeyRelease-Up>', self.turn_up_stop)
            self.canvas.bind_all('<KeyRelease-Down>', self.turn_down_stop)
    def draw(self):
        self.canvas.move(self.id, 0, self.speed)
    def turn_up(self, event):
        if self.exist == True:
            pos = self.canvas.coords(self.id)
            if pos[1] <= 0:
                self.speed = 0
            else:
                self.speed = -4
    def turn_down(self, event):
        if self.exist == True:
            pos = self.canvas.coords(self.id)
            if pos[3] >= self.canvas_height:
                self.speed = 0
            else:
                self.speed = 4
    def turn_up_stop(self, event):
        self.speed = 0
    def turn_down_stop(self, event):
        self.speed = 0


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas 
        self.paddle = paddle

        x = random.randrange(-6, 7)
        y = random.randrange(0, 7)
        b0 = canvas.create_rectangle(50 + x, 0, 90 + x, 10, fill = 'black')
        b1 = canvas.create_rectangle(250, 0, 290, 10, fill = 'black')
        b2 = canvas.create_rectangle(440, 0 + 2*y, 480, 10 + 2*y, fill = 'black')
        b3 = canvas.create_rectangle(200, 40, 240, 50, fill = 'black')
        b4 = canvas.create_rectangle(242 + x, 40 + y, 282 + x, 50 + y, fill = 'black')
        b5 = canvas.create_rectangle(0 , 120, 40, 130, fill = 'black')
        b6 = canvas.create_rectangle(150, 120 - y, 200, 130 - y, fill = 'black')
        b7 = canvas.create_rectangle(220 + x, 120, 270 + x, 130, fill = 'black')
        self.brick = [b0,b1,b2,b3,b4,b5,b6,b7]
        self.id = canvas.create_oval(10, 10, 25, 25, fill = color)
        self.canvas.move(self.id, 245, 100)
        starts = [-6, -5, -4.5, -4,-3.5, -3, -2.5, -2, -1.5, -1, 1, 1.5, 2, 2.5, 3, 3.5, 4,4.5, 5, 6]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.win = 0
        self.flag = [0,0,0,0,0,0,0,0]
        
    def hit_brick(self, pos):
        brick_pos = []
        for i in range(0, 8):
            brick_pos.append(self.canvas.coords(self.brick[i]))
        for i in range(0, 8):
            if self.flag[i] == 0:
                if pos[2] >= brick_pos[i][0] and pos[0] <= brick_pos[i][2]:
                    if pos[1] >= brick_pos[i][1] and pos[1] <= brick_pos[i][3]:
                        self.flag[i] = 1
                        self.canvas.delete(self.brick[i])
                        self.win += 1           
                        if self.y > 0:
                            return 1
                        else:
                            return 2
                
        return 0

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)   #get the paddle position
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
         
    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
           self.y = 3 
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        x = self.hit_brick(pos)
        if x != 0:
            self.y = 3 * ((-1) ** x)
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill = color)
        self.canvas.move(self.id, 200, 400)
        self.speed = 0
        self.paddle_exist = True
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.turn_left_stop)
        self.canvas.bind_all('<KeyRelease-Right>', self.turn_right_stop)
    def draw(self):
        self.canvas.move(self.id, self.speed, 0)
        #pos = self.canvas.coords(self.id)   #get the paddle position
    def turn_left(self, event):
        if self.paddle_exist == True:
            pos = self.canvas.coords(self.id)
            if pos[0] <= 0:
                self.speed = 0
            else:
                self.speed = -4
    def turn_right(self, event):
        if self.paddle_exist == True:
            pos = self.canvas.coords(self.id)
            if pos[2] >= self.canvas_width:
                self.speed = 0
            else:
                self.speed = 4
    def turn_left_stop(self, event):
        self.speed = 0
    def turn_right_stop(self, event):
        self.speed = 0

def out(event):
    global root
    global c
    global flag
    global ballplay_enable
    dist1 = sqrt((event.x - 380) * (event.x - 380) + (event.y - 290) * (event.y - 290))
    #enter the Mode-1
    if dist1 <= 50.0 and event.y <= 290:
        ballplay_enable = 1
        root.title("Game Mode 1")
        c.delete(ALL)
        root.resizable(0,0)
        root.wm_attributes("-topmost", 1)
        root.update()
        paddle = Paddle(c, '#4682B4')
        ball = Ball(c, paddle, 'red')
        while 1:
            if ball.hit_bottom == False and ball.win != 8:
                ball.draw()
                paddle.draw()
                root.update_idletasks()
                root.update()
                sleep(0.01)
            elif ball.win == 8:  #win the game
                sleep(0.1)
                paddle.paddle_exist = False
                c.delete(ALL)
                c.create_rectangle(150, 190, 320, 280, fill= 'yellow')
                Font = tkFont.Font(size = 13, family = 'Roboto')
                c.create_text(235, 235, text = 'you win the game', font = Font, fill = 'red')
                root.update()
                sleep(1.5)
                #back to the interface
                ballplay_enable = 0
                interface()

            else:               #lose the game
                sleep(0.1)
                paddle.paddle_exist = False
                c.delete(ALL)
                c.create_rectangle(150, 190, 320, 280, fill= 'white')
                Font = tkFont.Font(size = 13, family = 'Roboto')
                c.create_text(235, 235, text = 'you lose the game', font = Font, fill = 'black')
                root.update()
                sleep(1.5)
                #back to the interface
                ballplay_enable = 0
                interface()
                
    #enter the Mode-2
    elif dist1 <= 50 and event.y >= 290:
        ballplay_enable = 1
        flag = 0
        root.title("Game Mode 2")
        c.delete(ALL)
        root.resizable(0,0)
        root.wm_attributes("-topmost", 1)
        root.update()
        paddle1 = Paddle_Mode2(c, 25, 235, 0, '#4682B4')
        paddle2 = Paddle_Mode2(c, 425, 235, 1, 'yellow')
        ball_2 = Ball_Mode2(c, paddle1, paddle2, 'red')

        while True:
            if ball_2.hit_wall == False: #game continues
                root.update()
                paddle1.draw()
                paddle2.draw()
                ball_2.draw()
                root.update_idletasks()
                root.update()
                sleep(0.008)
                	
            else:                #game over
                sleep(0.1)
                paddle1.exist = False
                paddle2.exist = False
                c.delete(ALL)
                c.create_rectangle(150, 190, 320, 280, fill= 'white')
                Font = tkFont.Font(size = 13, family = 'Roboto')
                if ball_2.who_win == 1:
                    c.create_text(235, 235, text = 'right win the game', font = Font, fill = 'black')
                else:
                    c.create_text(235, 235, text = 'left win the game', font = Font, fill = 'black')
                root.update()
                sleep(1.5)
                	
                ballplay_enable = 0
                interface()


#draw the interface
def interface():
    global root
    global c
    global ballplay_enable
    root.title("Game Interface")
    c.pack()
    c.create_rectangle(0,0,510,290, fill = "#00BCD4", outline = "")
    c.create_rectangle(0,0, 510,30, fill = "#4682B4", outline = "")
    c.create_rectangle(10, 40, 35, 44, fill = "#F5F5F5", outline = "")
    c.create_rectangle(10, 47, 35, 51, fill = "#F5F5F5", outline = "")
    c.create_rectangle(10, 54, 35, 58, fill = "#F5F5F5", outline = "")
    c.create_oval(330,240,430,340, fill = "#FF4081", outline = "")
    c.create_line(330, 290, 430, 290, fill = "white")

    font1 = tkFont.Font(size = 28, family = "Roboto", weight = tkFont.BOLD, overstrike = 0)
    font2 = tkFont.Font(family = 'Roboto',size = 13)
    c.create_text(235, 150, text = "Bouncing Ball",font = font1, fill = "white")
    c.create_text(235, 180, text = "Powered by Python", font = font2, fill = "#B2EBF2")
    c.create_text(235, 360, text = "Copyright©(2016)Gao Chao\n\nchoose the mode to start", font = font2, fill = "#B6B6B6")
    

    c.create_text(380, 275, text = "Mode-1",font = font2, fill= "white")
    c.create_text(380, 305, text = "Mode-2",font = font2, fill= "white")
    
    c.bind("<Button-1>", out)

    sb = []
    for i in range(5):
        sb.append(c.create_oval(15 * i, 435, 15 * i + 10, 445, fill = "#00BCD4", outline = ""))

    x = [5, 15, 25, 35, 45]
    speed = [0, 0, 0, 0, 0]
    #ball play image
    while ballplay_enable == 0:
        for i in range(5):
            speed[i] = (abs(250 - x[i]) + 200) / 35
            x[i] += speed[i]
            c.move(sb[i], speed[i], 0)
            c.update()
        
        if x[0] > 480:
            for i in range(5):
                c.delete(sb[i])
            for i in range(5):
                sb[i] = c.create_oval(15 * i,435,15 * i + 10,445, fill = "#00BCD4", outline = "")
            x = [5, 15, 25, 35, 45]
        sleep(0.04)
    
    root.mainloop()

interface()


