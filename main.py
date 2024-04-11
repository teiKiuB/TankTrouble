import pygame
from PrimarySettings import *
from sprites import *
from os import path
import random
pygame.init()  

screen = pygame.display.set_mode((WIDTH,HEIGHT))
bgStart = pygame.image.load('imagefolder/bgS.png').convert_alpha()
btnStart = pygame.image.load('imagefolder/btnStart.png').convert_alpha()

class Game:

    def __init__(self):
        pygame.init()  # initialize all imported pygame modules
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()  # create an object to help track time
        pygame.display.set_caption(TITLE)
        self.SCORE1 = 0
        self.SCORE2 = 0
        self.data()

    def data(self):
            folder_of_game = path.dirname(__file__)  # location of main.py
            image_folder = path.join(folder_of_game, 'imagefolder')
            Mazefolder = path.join(folder_of_game, 'MAZEFOLDER')
            sound_folder = path.join(folder_of_game, 'snd')
            self.maze = []
            i = random.randint(1, 5)
            with open(path.join(Mazefolder, 'MAZE{}.txt'.format(i)), 'rt') as f:
                for line in f:
                    self.maze.append(line)
            self.player_image = pygame.image.load(path.join(image_folder, PLAYER_IMAGE)).convert()
            self.player_image.set_colorkey(WHITE)
            self.enemy_image = pygame.image.load(path.join(image_folder, ENEMY_IMAGE)).convert()
            self.enemy_image.set_colorkey(WHITE)
            self.wall_image = pygame.image.load(path.join(image_folder, WALL_IMAGE)).convert()
            self.bullet_image = pygame.image.load(path.join(image_folder, BULLET_IMAGE)).convert()
            self.bullet_image.set_colorkey(WHITE)
            self.shoot_sound = pygame.mixer.Sound(path.join(sound_folder, 'shoot.wav'))
            self.explosion_sound = pygame.mixer.Sound(path.join(sound_folder, 'Explosion20.wav'))
            self.explosion_list = []
            for j in range(9):
                picture_name = 'regularExplosion0{}.png'.format(j)
                self.image_loading_of_explosion = pygame.image.load(path.join(image_folder, picture_name)).convert()
                self.image_loading_of_explosion.set_colorkey(BLACK)
                self.image = pygame.transform.scale(self.image_loading_of_explosion, (50, 50))
                self.explosion_list.append(self.image)

    def new(self):
        # initializing all variables and setup them for a new game
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()  # created the walls group to hold them all
        self.bullets = pygame.sprite.Group()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '*':
                    self.player = Player(self, col, row)
                if tile == '-':
                    self.enemy = Enemy(self, col, row)

    def run(self):
        self.playing = True
        self.Score = False

        while self.playing:
            self.changing_time = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

            # Thêm kiểm tra để chuyển sang trạng thái chơi game khi điều kiện đạt được
            if self.Score:
                self.SCORE2 = 0
                self.SCORE1 = 0
                self.new()
                self.run()



    def grid(self):
        for x in range(0, WIDTH, SQSIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, SQSIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def update(self):
        # keep track changing
        self.all_sprites.update()
        self.hit()

    def hit(self):

        self.hits1 = pygame.sprite.spritecollide(self.player, self.bullets, True, collide)
        for hit in self.hits1:
            if hit:
                Explosion(self, hit.rect.center)
                self.explosion_sound.play()
                self.player.kill()
                self.SCORE1 += 1
                self.playing = False

                self.data()
                self.new()
                if self.SCORE1 == 5:
                    self.show_go_screen1()
        self.hits2 = pygame.sprite.spritecollide(self.enemy, self.bullets, True, collide)
        for hit in self.hits2:
            if hit:
                Explosion(self, hit.rect.center)
                self.explosion_sound.play()
                self.enemy.kill()
                self.SCORE2 += 1
                self.playing = False
                self.data()
                self.new()
                if self.SCORE2 == 5:
                    self.show_go_screen2()

    def draw(self):
        # flip all the thing to screen
        self.screen.fill(BGCOLOR)
        self.grid()
        self.all_sprites.draw(self.screen)
        drawing_text(self.screen, str(self.SCORE1) + ':Green Tank', 25, 150, 710, GREEN)
        drawing_text(self.screen, 'Blue Tank:' + str(self.SCORE2), 25, 900, 710, BLUE)
        pygame.display.flip()

    def quit(self):
        pygame.quit()  # uninitialize all pygame modules
        quit()

    def show_go_screen1(self):
        self.screen.fill(BROWN)
        drawing_text(self.screen, 'Green Tank wins', 80, WIDTH / 2, HEIGHT / 3, GREEN)
        drawing_text(self.screen, 'Press a key to begin or escape key to quit', 40, WIDTH / 2, HEIGHT / 2, WHITE)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen2(self):
        self.screen.fill(BROWN)
        drawing_text(self.screen, 'Blue Tank Wins', 80, WIDTH / 2, HEIGHT / 3, BLUE)
        drawing_text(self.screen, 'Press a key to begin or escape key to quit', 40, WIDTH / 2, HEIGHT / 2, WHITE)
        pygame.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)  # keep loop running
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    self.Score = True
                    waiting = False
                    
    def menu(self):
        scaler_bg = pygame.transform.scale(bgStart, (WIDTH, HEIGHT))
        self.screen.blit(scaler_bg, (0, 0))
        
        # Tạo nút "btnStart"
        btn_start = Button(450, 300, btnStart)
        btn_start.draw()

        pygame.display.flip()
        pygame.display.update()

        # Chờ người dùng nhấn nút "btnStart"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYUP:
                    self.Score = True
                    break  # Thoát khỏi vòng lặp

            # Kiểm tra xem nút đã được nhấn chưa
            if btn_start.draw():
                break  # Thoát khỏi vòng lặp khi nút được nhấn

   
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # Lấy vị trí của chuột
        pos = pygame.mouse.get_pos()

        # Kiểm tra xem chuột có nằm trên nút không và có nhấn chuột trái không
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        # Reset trạng thái của nút khi không có chuột được nhấn
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Vẽ nút
        screen.blit(self.image, self.rect)

        return action

# create game objects
g = Game()
while True:
    g.menu()
    g.new()
    g.run()