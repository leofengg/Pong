#old pong game between 2 players, if the ball touches their side they lose the point
import pygame

def main():
    
    #initialize pygame
    pygame.init()
    #open window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pong')
    w_surface = pygame.display.get_surface()
    game = Game(w_surface)
    game.play()
    pygame.quit()
    
class Game:
    
    def __init__(self, surface):
        
        #objects for all games
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.game_clock = pygame.time.Clock()
        
        self.FPS = 100
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        
        #game specific objects
         
        #score
        self.scoreA = 0
        self.scoreB = 0
        #player 1 paddle
        self.paddle1 = Paddle('white', [100, 150], 15, 60, 0, self.surface)
        #self, rect_color, rect_pos, rect_width, rect_height, rect_velocity, screen
        #player 2 paddle
        self.paddle2 = Paddle('white', [600, 150], 15, 60, 0, self.surface)
        #ball
        self.ball = Ball('white', 7, [50,50], [5,3], self.surface, self.scoreA, self.scoreB)
        
    #main game loop
    def play(self):
        
        while not self.close_clicked:
            self.events()
            self.draw()
            
            if self.continue_game:
                self.update()
                self.decide_continue()    
            if self.continue_game == False:
                self.ball.stop()
            
            #set FPS for game    
            self.game_clock.tick(self.FPS)  
            
    def events(self):
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True  
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)  
            elif event.type == pygame.KEYUP:
                self.handle_keyup(event)
        
    def draw(self):
        #display on game surface
        #score
        #ball
        #paddles
        self.surface.fill(self.bg_color)
        
        #draw game objects
        self.ball.score()
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()
        
        #render objects
        pygame.display.update()
        
        
    def update(self):
        
        #move ball/paddle
        self.ball.move()            
        self.paddle1.move()
        self.paddle2.move()
        #collision detection
        self.collision()
        
    def handle_keydown(self, event):
        
        if event.key == pygame.K_q and self.paddle1.rect.top > 0:
            self.paddle1.velocity = -2
        if event.key == pygame.K_a and self.paddle1.rect.bottom < 500:
            self.paddle1.velocity = 2
        if event.key == pygame.K_p and self.paddle2.rect.top > 0:
            self.paddle2.velocity = -2
        if event.key == pygame.K_l and self.paddle2.rect.bottom < 500:
            self.paddle2.velocity = 2
            
    def handle_keyup(self, event):
        #paddle stops moving when key is lifted
        if event.key == pygame.K_q or event.key == pygame.K_a:
            self.paddle1.velocity = 0
        if event.key == pygame.K_p or event.key == pygame.K_l:
            self.paddle2.velocity = 0
        
        
    def collision(self):
        #if ball collides with paddle, bounce off
        if self.paddle1.rect.collidepoint(self.ball.center[0], self.ball.center[1]) and self.ball.velocity[0] < 0:
            self.ball.bounce()
            
        if self.paddle2.rect.collidepoint(self.ball.center[0], self.ball.center[1]) and self.ball.velocity[0] > 0:
            self.ball.bounce()
            
    def decide_continue(self):
        
        if self.ball.scoreA == 11 or self.ball.scoreB == 11:
            self.continue_game = False
                
class Ball:
    
    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, screen, scoreA, scoreB):
        
        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.screen = screen
        self.scoreA = scoreA
        self.scoreB = scoreB
        
    def move(self):
        
        for index in range(0,2):
            self.center[index] = (self.center[index] + self.velocity[index])
            
        #create illusion of bouncing from walls
        #x coordinate
        if self.center[0] <= 0:
            #self.scoreB += 1
            self.velocity[0] = -self.velocity[0]
        elif self.center[0] >= 700:
            #self.scoreA += 1
            self.velocity[0] = -self.velocity[0]
        #y coordinate
        elif self.center[1] <= 0 or self.center[1] >= 500:
            self.velocity[1] = -self.velocity[1]
        
    def score(self):
        
        font = pygame.font.Font(None, 74)
        textA = font.render(str(self.scoreA), 1, self.color)
        self.screen.blit(textA, (50,10))
        textB = font.render(str(self.scoreB), 1, self.color)
        self.screen.blit(textB, (650,10))
        
        if self.center[0] <=0:
            self.scoreB += 1
        elif self.center[0] >= 700:
            self.scoreA += 1
        return self.scoreA, self.scoreB
    
    def stop(self):
        
        self.velocity = 0
        
    def bounce(self):
        
        self.velocity[0] = -self.velocity[0]

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)
        
        
class Paddle:
    
    def __init__(self, rect_color, rect_pos, rect_width, rect_height, rect_velocity, screen):
        
        self.color = pygame.Color(rect_color)
        self.pos = rect_pos
        self.width = rect_width
        self.height = rect_height
        self.velocity = rect_velocity
        self.screen = screen
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        
    def move(self):        
        #reaction to key getting pressed, give paddle velocity
        self.rect.top = self.rect.top + self.velocity
        self.rect.bottom = self.rect.bottom + self.velocity
        
        #make sure paddles doesn't go off screen
        if self.rect.top < 0 or self.rect.bottom > 500:
            self.velocity = 0
              
    def stop(self):
        
        self.velocity = 0
        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    
main()