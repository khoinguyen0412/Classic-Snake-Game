import pygame 
from pygame.locals import *
import time
import random

# Size of a block
SIZE = 40

# Window size
window_x = 1000
window_y= 800

# initial score
score = 0


class Strawberry:
    def __init__ (self,game_surface):
        self.fruit = pygame.image.load("resources/strawberry_image.png")
        self.fruit = pygame.transform.scale(self.fruit, (SIZE,SIZE))
        self.game_surface = game_surface
        self.x = SIZE*3
        self.y = SIZE*3
        
    def draw(self):
        self.game_surface.blit(self.fruit,(self.x,self.y))

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

class Snake:
    def __init__(self, game_surface,length):
       self.length = length
       self.game_surface = game_surface
       self.block = pygame.image.load("resources/block_image.jpg").convert()
       self.block = pygame. transform. scale(self.block, (SIZE,SIZE))
       self.x = [SIZE]*length
       self.y = [SIZE]*length

       # Set the default movement
       self.direction = "Blank"   
    
    def increase_length(self):
        self.length += 1

        # Append a block with a random variable inside 
        self.x.append(-1)
        self.y.append(-1)       


    def moveUp(self):
        if self.direction == "Down":
            return
        else:
            self.direction = "Up"


    def moveDown(self):
        if self.direction == "Up":
            return
        else:
            self.direction = "Down"


    def moveLeft(self):
        if self.direction == "Right":
            return
        else:
            self.direction = "Left"


    def moveRight(self):
        if self.direction == "Left":
            return
        else:
            self.direction = "Right"


    def draw(self):
        for i in range(self.length):
            self.game_surface.blit(self.block,(self.x[i] ,self.y[i]))


    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "Up":
            self.y[0] -= SIZE
            
        
        if self.direction == "Down":
            self.y[0] += SIZE
            
        
        if self.direction == "Left":
            self.x[0] -= SIZE
            

        if self.direction == "Right":
            self.x[0] += SIZE

        self.draw()
    
    

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Khoi Nguyen Snake Game')
        self.play_background_music()
        self.level = 0
        self.surface = pygame.display.set_mode((window_x,window_y))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.strawberry = Strawberry(self.surface)
        self.strawberry.draw()
        

    def render_background(self):
        bg = pygame.image.load("resources/grass_background.jpg")
        self.surface.blit(bg, (0,0))


    def play_background_music(self):
        pygame.mixer.music.load("resources/Background music.mp3")
        pygame.mixer.music.play()


    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False


    def display_score(self):
        font = pygame.font.SysFont('arial',35)
        score = font.render(f"Score: {self.snake.length}", True , (255, 255, 255))
        self.surface.blit(score, (850,15))
        pygame.display.flip()


    def check_level(self):
        if (self.snake.length == 10):
            self.level = 1
        if (self.snake.length == 20) :
            self.level = 2
        if (self.snake.length == 25):
            self.level = 3
        
        
    def play(self):
        self.render_background()
        self.snake.walk()
        self.strawberry.draw()
        self.display_score()
        pygame.display.flip()
        
        # Snake eats strawberry
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.strawberry.x,self.strawberry.y):
            sound = pygame.mixer.Sound("resources/Ding sound effect.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.strawberry.move()

        # Snake eats itself
        for i in range(3,self.snake.length):
                if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                    raise "Game Over"
        
        # Snake goes out of the window
        if self.snake.x[0] >= window_x or self.snake.x[0] < 0:
            raise "Game Over"
        elif self.snake.y[0] >= window_y or self.snake.y[0] < 0:
            raise "Game Over"


    def show_game_over(self):
        self.surface.fill((0,0,0))
        sound = pygame.mixer.Sound("resources/Lose sound effect.mp3")
        pygame.mixer.Sound.play(sound)
        font = pygame.font.SysFont('arial',30)
        line_1 = font.render(f"GAME OVER ! Your score is: {self.snake.length}", True , (250, 57, 57) )
        self.surface.blit(line_1, (330,350))
        line_2 = font.render("To play again press Space. To exit press Escape", True, (250, 57, 57) )
        self.surface.blit(line_2, (240,400))
        pygame.display.flip()
        pygame.mixer.music.pause()


    def run(self):
         running = True
         pause = False

         while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        pygame.mixer.music.unpause()
                        main()
                    if not pause:
                        if event.key == K_UP:
                            self.snake.moveUp()
                        if event.key == K_DOWN:
                            self.snake.moveDown()
                        if event.key == K_RIGHT:
                            self.snake.moveRight()
                        if event.key == K_LEFT:
                            self.snake.moveLeft()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True

            self.check_level()
            
            if (self.level == 0):
                time.sleep(0.15)

            if (self.level == 1):
                time.sleep(0.1)

            if (self.level == 2):
                time.sleep(0.08)
            
            if (self.level == 3):
                time.sleep(0.04)

        

         pygame.quit()
         quit()  


def main():
    game = Game()
    game.run()
    

if __name__ == "__main__": 
    main()
    

   

   
    

    