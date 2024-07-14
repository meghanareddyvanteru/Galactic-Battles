import pygame
import random 
class Asteroid:
    def __init__(self,x,y,speed):
        self.x=x
        self.y=y
        self.speed=speed
        self.image=pygame.image.load("asteroid.png")
    def draw(self,screen):
        resized_image = pygame.transform.scale(self.image, (70,60))
        screen.blit(resized_image,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.y+=self.speed
class Alien:
    def __init__(self,x,y,speed):
        self.x=x
        self.y=y
        self.speed=speed
        self.image=pygame.image.load("alien_spaceship.png")
    def draw(self,screen):
        resized_image = pygame.transform.scale(self.image, (70,60))
        screen.blit(resized_image,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.y+=self.speed
class Bullet:
    def __init__(self,x,y,speed):
        self.x=x
        self.y=y
        self.speed=speed
        self.image=pygame.image.load("bullet.png")
    def draw(self,screen):
        resized = pygame.transform.scale(self.image,(20,20))
        screen.blit(resized,(self.x,self.y))
        pygame.display.flip()
    def move(self):
        self.y-=self.speed
class Spaceship:
    def __init__(self,x,y,speed):
        self.x=x
        self.y=y
        self.bullets=[]
        self.speed=speed
        self.image=pygame.image.load("Screenshot 2024-07-12 195902.png")
    def draw(self,screen):  
        resize_image = pygame.transform.scale(self.image, (70,60))
        screen.blit(resize_image,(self.x,self.y))
        pygame.display.flip()
    def move_left(self):
        self.x-=self.speed 
    def move_right(self):
        self.x+=self.speed
    def shoot(self):
        bullet=Bullet(self.x+35,self.y-20,5)
        self.bullets.append(bullet)
pygame.init()
screen_width= 800
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Spaceship Game")
spaceship_img=pygame.image.load("Screenshot 2024-07-12 195902.png")
asteroid_img=pygame.image.load("asteroid.png")
alien_spaceship_img=pygame.image.load("alien_spaceship.png")
bullet_img= pygame.image.load("bullet.png")
background_img= pygame.image.load("background.png")
enemies=[]
spaceship=Spaceship(400,500,10)
def spawn_enemy():
    ex=random.randint(0,screen_width-70)
    ey=random.randint(100,200)
    es=random.randint(1,2)
    enemy=Alien(ex,ey,es)
    enemies.append(enemy)
asteroids=[]
def spawn_asteroids():
    ax=random.randint(0,screen_width-70)
    ay=random.randint(100,200)
    aspeed=random.randint(1,2)
    asteroid=Asteroid(ax,ay,aspeed)
    asteroids.append(asteroid)
def load_high_score():
    high_score=0
    try:
        with open('highscores.txt','r') as f:
            high_score=int(f.read())
    except FileNotFoundError:
        pass
    return high_score
def save_high_scores(score):
    with open('highscores.txt','w') as f:
        f.write(str(score))
score=0
run=True
game_over=False
high_score=load_high_score()
while run:
    if not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    spaceship.shoot()
                if event.key==pygame.K_LEFT:
                    spaceship.move_left()
                if event.key==pygame.K_RIGHT:
                    spaceship.move_right()
        if random.randint(1,100)==1:
            spawn_enemy()
        if random.randint(1,100)==1:
            spawn_asteroids()
        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)
        for a in asteroids:
            a.move()
            a.draw(screen)
        for bullet in spaceship.bullets:
            bullet.move()
            bullet.draw(screen)
        for bullet in spaceship.bullets:
            bullet.move()
            bullet.draw(screen)
            for enemy in enemies:
                enemy_rect=pygame.Rect(enemy.x,enemy.y,70,60)
                bullet_rect=pygame.Rect(bullet.x,bullet.y,20,20)
                if bullet_rect.colliderect(enemy_rect):
                    enemies.remove(enemy)
                    spaceship.bullets.remove(bullet)
                    score+=10
                    score_text=font.render("Score: "+str(score),True,(255,255,255))
                    screen.blit(score_text,(10,10))
                    pygame.display.flip()
        for enemy in enemies:
            enemy_rect=pygame.Rect(enemy.x,enemy.y,70,60)
            spaceship_rect=pygame.Rect(spaceship.x,spaceship.y,70,60)
            if spaceship_rect.colliderect(enemy_rect):
                game_over=True
        for asteroid in asteroids:
            asteroid_rect=pygame.Rect(asteroid.x,asteroid.y,70,60)
            spaceship_rect=pygame.Rect(spaceship.x,spaceship.y,70,60)
            if spaceship_rect.colliderect(asteroid_rect):
                game_over=True
        background = pygame.transform.scale(background_img, (800,600))
        screen.blit(background,(0,0))
        font=pygame.font.Font(None,36)
        spaceship.x=max(0,min(spaceship.x,screen_width-70))
        spaceship.draw(screen)
        score_text=font.render("Score: "+str(score),True,(255,255,255))
        screen.blit(score_text,(10,10))
        pygame.display.flip()
    else:
        if score>high_score:
            high_score=score
            save_high_scores(high_score)
        game_over_font=pygame.font.Font(None,62)
        game_over_text=game_over_font.render("GAME OVER",True,(255,255,255))
        text_rect=game_over_text.get_rect(center=(screen_width//2,screen_height//2))
        screen.blit(game_over_text,text_rect)
        high_score_text=font.render("High Score : "+str(high_score),True,(255,255,255))
        screen.blit(high_score_text,(10,40))
        pygame.display.flip()
    pygame.display.update()
pygame.quit()
