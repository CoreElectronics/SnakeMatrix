from dotstar import Adafruit_DotStar
from random import randint
import time, pygame

#button mapping
up = 46
down = 32
left = 18
right = 33

start = 24

sizeX = 30
sizeY = 15

NUMPIXELS = 2*(sizeX*sizeY)
order = 'gbr'

SPEED = 10

strip = Adafruit_DotStar(NUMPIXELS, 16000000, order=order)

# -- CONSTANTS

#screen size, used for pygame input events and to display instructions 
SCREEN_WIDTH = 6
SCREEN_HEIGHT = 4
#colours     r       g     b
BLACK =  (    0,     0,     0)
WHITE = ( 255, 255, 255)
GREEN = (     0, 255,     0)
RED =     ( 255,     0,      0)
BLUE = (     0,       0,  255)
YELLOW =(255, 255,    0)
PURPLE = (255,    0, 255)
CYAN =   (     0, 255, 255)
COLOURS = (GREEN, RED, BLUE, YELLOW, PURPLE, CYAN)

pixelGrid = [[0 for x in range(sizeX+1)] for y in range(sizeY+1)]

keyVal = 840
for j in range(sizeY):

    for i in range(sizeX):
	if(j % 2 == 0):
        	rawVal = keyVal + (i*2)
	else:
		rawVal = keyVal - (i*2)
        pixelGrid[j][i] = rawVal
        #print(pixelGrid[(sizeY-1)-j][i])

    if(j % 2 == 0):
        keyVal = keyVal - 2
    else:
        keyVal = keyVal - 118

strip.begin()
strip.setBrightness(255)

# --- CLASSES
#snake class for player
class Snake():
    #attributes
    body_list = None #snake segment locations
    change_x = None #movement on x-axis
    change_y = None #movement on y-axis
    eaten = None #has the snake eaten some food?
    g_over = False #holds value for game over if snake goes off the screen or eats itself
    
#methods
    def __init__(self):
        self.body_list = [[14,10],[14,11]] #starting location
        self.change_x = 1
        self.change_y = 0
        self.eaten = False
    def update(self, food):
        #remove old segment
        old_segment = self.body_list.pop()
        self.eaten = False
        #find new segment
        x = self.body_list[0][0] + self.change_x
        y = self.body_list[0][1] + self.change_y
	if x == sizeX:
		x = 0
	if x < 0:
		x = sizeX-1
	if y == sizeY:
		y = 0
	if y < 0:
		y = sizeY-1
        segment = [x,y]
        self.body_list.insert(0, segment)
        #check for eaten food
        if segment[0] == food.x_pos and segment[1] == food.y_pos:
            self.body_list.append(old_segment)
            self.eaten = True
	    global SPEED
	    SPEED += 0.5
        else:
            strip.setPixelColor(pixelGrid[old_segment[1]][old_segment[0]],BLACK[0],BLACK[1],BLACK[2])
            strip.setPixelColor(pixelGrid[old_segment[1]][old_segment[0]]+1,BLACK[0],BLACK[1],BLACK[2])

        #prepare segments for display on unicorn hat, use try to prevent exception from crashing the game
        for segment in self.body_list:
            try:
                strip.setPixelColor(pixelGrid[segment[1]][segment[0]],WHITE[0],WHITE[1],WHITE[2])
                strip.setPixelColor(pixelGrid[segment[1]][segment[0]]+1,WHITE[0],WHITE[1],WHITE[2])
            except:
                self.g_over = True
                
    #movement controls
    def go_left(self):
        self.change_x = 1
        self.change_y = 0
    def go_right(self):
        self.change_x = -1
        self.change_y = 0
    def go_up(self):
        self.change_x = 0
        self.change_y = 1
    def go_down(self):
        self.change_x = 0
        self.change_y = -1
        
    #check for game over, returned to game class
    def game_over(self):
        #game over events
        if self.body_list[0] in self.body_list[1::] or self.g_over == True:
            self.game_over_sequence()
            return True
        #if self.body_list[0][0] > sizeX or self.body_list[0][0] < 0 or self.body_list[0][1] > sizeY or self.body_list[0][1] < 0:
            #self.game_over_sequence()
            #return True
        return False

    def game_over_sequence(self):
        for segment in self.body_list:
            strip.setPixelColor(pixelGrid[segment[1]][segment[0]], 255,50,50)
            strip.setPixelColor(pixelGrid[segment[1]][segment[0]]+1, 255,50,50)
            strip.show()
        time.sleep(0.2)
        for segment in self.body_list:
            strip.setPixelColor(pixelGrid[segment[1]][segment[0]], 150,30,30)
            strip.setPixelColor(pixelGrid[segment[1]][segment[0]]+1, 150,30,30)
            strip.show()
        time.sleep(0.2)
        for segment in self.body_list:
            strip.setPixelColor(pixelGrid[segment[1]][segment[0]], 70,10,10)
            strip.setPixelColor(pixelGrid[segment[1]][segment[0]]+1, 70,10,10)
            strip.show()
        time.sleep(0.2)
        
#Class for food
class Food():
    #attributes
    eaten = None
    x_pos = None
    y_pos = None
    r = None
    g = None
    b = None
    
#methods
    def __init__(self):
        self.eaten = True #set to true so that it is reset at start

    def update(self, snake):
        if self.eaten:
            #inside checks to ensure food isn't draw in the same location as the snakes body
            inside = True
            while inside:
                self.x_pos = randint(0,(sizeX-1))
                self.y_pos = randint(0,(sizeY-1))
                if [self.x_pos, self.y_pos] in snake.body_list:
                    inside = True
		if self.x_pos == 0 and self.y_pos == 14:
		    inside = True
                else:
                    inside = False
            #give food a random colour from list of colours. List ensures visible strong colours
            colour = randint(0,len(COLOURS)-1)
            self.r = COLOURS[colour][0]
            self.g = COLOURS[colour][1]
            self.b = COLOURS[colour][2]
        #prepare for display on unicorn hat    
        strip.setPixelColor(pixelGrid[self.y_pos][self.x_pos],self.r,self.g,self.b)
        strip.setPixelColor(pixelGrid[self.y_pos][self.x_pos]+1,self.r,self.g,self.b)
        self.eaten = False

#game class
class Game(object):
    #attributes
    snake = None
    food = None
    game_over = None
    start = True #used to start the game in the same conditions as game over
#methods
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True #exits main game loop
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o and (self.game_over or self.start):
                #start or restart the game
                self.__init__()
                self.start = False
            if event.type == pygame.KEYDOWN:
                #movement
                if event.key == pygame.K_f and self.snake.change_x != -1:
                    self.snake.go_left()
                if event.key == pygame.K_e and self.snake.change_x != 1:
                    self.snake.go_right()
                if event.key == pygame.K_c and self.snake.change_y != -1:
                    self.snake.go_up()
                if event.key == pygame.K_d and self.snake.change_y != 1:
                    self.snake.go_down()
        return False #stay in main game loop

    def run_logic(self):
        #check for game over first
        self.game_over = self.snake.game_over()
        #only if it is not the first game and not game over update the food and snake
        if not self.game_over and not self.start:
            self.food.update(self.snake)
            self.snake.update(self.food)
            self.food.eaten = self.snake.eaten

    def display_frame(self, screen):
        #screen used to display information to the player, also required to detect pygame events
        #Unicorn hat display is also handled here
        if self.game_over or self.start:
            strip.clear() # removes last snake image from unicorn hat
        else:
            strip.show() # display the snake and food on the unicorn hat

        pygame.display.flip()

#main game function and loop
def main():
    pygame.init()

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)

    done = False
    clock = pygame.time.Clock()

    game = Game()
    
    while not done:
        done = game.process_events()

        game.run_logic()

        game.display_frame(screen)
	
        clock.tick(SPEED)

    pygame.quit()

if __name__ == '__main__':
    main()
