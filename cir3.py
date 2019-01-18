""" This code is for a game :
the player ( a blue ball ) moves to touch a target ( a  red ball )
and at the same time he/she tries to evoid hitting some other balls ( the orange ones)
"""
import arcade
from random import randint
from pyglet.window import key
from math import sqrt
import time 

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
########################### The circle class ###############################
class Circle:
    """
    The ball to avoid , they move and bounce randomly 
    """
    def __init__(self, x, y, vx, vy,r=20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r=r
 
    def move(self,circles):
        self.x += self.vx
        self.y += self.vy
        if (self.x>=SCREEN_WIDTH-2*self.r or self.x<=2*self.r) : # to bounce if the ball touches the screen edges 
              self.vx=randint(-2,2)
              self.vy=randint(-2,2)
        if (self.y>=SCREEN_HEIGHT-2*self.r or self.y<=2*self.r):
              self.vy=randint(-2,2)
              self.vx=randint(-2,2)
        for c in circles:# to bounce if the ball touches another ball 
              if c!=self:
                  if c.r+self.r>=sqrt(((self.x-c.x)**2)+((self.y-c.y)**2)):
                      self.vx=randint(-2,2)
                      self.vy=randint(-2,2)
                    
            
    def stop(self):
        self.vx,self.vy=0,0
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y,
                                   self.r, arcade.color.VIVID_TANGERINE)
############################## The target class #############################
class target:
    """
  The ball target to get . it moves randomly faster than other balls 
    """
    def __init__(self, x, y, vx, vy,r=20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r=r 
 
    def move(self,circles):
        self.x += self.vx
        self.y += self.vy
        if (self.x>=SCREEN_WIDTH-2*self.r or self.x<=2*self.r ) :
              self.vx=randint(-10,10)
              self.vy=randint(-10,10)
        if (self.y>=SCREEN_HEIGHT-2*self.r or self.y<=2*self.r):
              self.vy=randint(-10,10)
              self.vx=randint(-10,10)
        for c in circles: # to bouce if balls touch each other 
              if c!=self:
                  if c.r+self.r>=sqrt(((self.x-c.x)**2)+((self.y-c.y)**2)):
                      self.vx=randint(-2,2)
                      self.vy=randint(-2,2)      
    def stop(self):
        self.vx,self.vy=0,0
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y,
                                   self.r, arcade.color.RED)
#################################The player class ##########################################        

class Player:
    """
    the player is controlled by the keys board 
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y,
                                  10, arcade.color.SAPPHIRE_BLUE)
    def control(self, keys): 
        if keys[key.LEFT]:
            self.x -= 5
            if self.x<=50:
                self.x=SCREEN_WIDTH-20
        if keys[key.RIGHT]:
            self.x +=5
            if self.x>= SCREEN_WIDTH-20:
                self.x=20
        if keys[key.UP]:
            self.y +=5
            if self.y >= SCREEN_HEIGHT-20:
                self.y=20
        if keys[key.DOWN]:
            self.y -=5
            if self.y<=20:
                self.y=SCREEN_HEIGHT-20
    def is_hit(self,circle):
        return(circle.r+10>=sqrt(((self.x-circle.x)**2)+((self.y-circle.y)**2)))
    def win (self,target):
        return(target.r+10>=sqrt(((self.x-target.x)**2)+((self.y-target.y)**2)))
        
################################## Main ###########################################    
circles = []
n = 10
def initialize():
    global keys,player,target
    keys = key.KeyStateHandler ( ) 
    player = Player(randint(SCREEN_WIDTH-100,SCREEN_WIDTH-20) ,randint(SCREEN_HEIGHT-100,SCREEN_HEIGHT-20))
    target=target(randint(100, SCREEN_WIDTH-100),
                        randint(100, SCREEN_HEIGHT-100),
                        randint(-5,5),
                        randint(-5,5),20)
    for i in range(n):
        circle = Circle(randint(100, SCREEN_WIDTH-100),
                        randint(100, SCREEN_HEIGHT-100),
                        randint(-2,2),
                        randint(-2,2),20)#randint(20,100))
        circles.append(circle)    

def on_draw(delta_time):
    arcade.start_render()
    global keys
    lost=False 
    for c in circles:
        c.move(circles+[target])
        c.draw()
        if player.is_hit(c):
            print(" you lost! try again ")
            #quit()
            for cir in circles:
                cir.stop()
                target.stop()
                lost=True
            time.sleep(3)
            quit()                
        
    if not lost: 
        target.move(circles)
        target.draw()
        if player.win(target):
            print("you won! Good job ")
            for cir in circles:
                    cir.stop()
                    target.stop()
            time.sleep(3)
            quit()
        player.control(keys)
        player.draw()
def main ( ) :
    
    initialize()
 
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT,
                       "Circles")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.get_window().push_handlers(keys)
    arcade.schedule(on_draw, 1 / 80)
    arcade.run()




    
if __name__ == '__main__':
    main() 




        
