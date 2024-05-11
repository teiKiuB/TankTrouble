import pygame
from PrimarySettings import *
from sprites import *
from os import path
import random
import socket
import threading

pygame.init()  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

screen = pygame.display.set_mode((WIDTH,HEIGHT))
bgStart = pygame.image.load('imagefolder/bgS.png').convert_alpha()
btnStart = pygame.image.load('imagefolder/btnStart.png').convert_alpha()
nameGame = pygame.image.load('imagefolder/nameGame.png').convert_alpha()
btnExit = pygame.image.load('imagefolder/btnExit.png').convert_alpha()
cup = pygame.image.load('imagefolder/cup.png').convert_alpha()
player1 = pygame.image.load('imagefolder/tank_green.png').convert_alpha()
player2 = pygame.image.load('imagefolder/tank_blue.png').convert_alpha()
bgWin = pygame.image.load('imagefolder/bgWin.png').convert_alpha()
textWin = pygame.image.load('imagefolder/textWin.png').convert_alpha()
btnSoundOn = pygame.image.load('imagefolder/sound-on.png').convert_alpha()
btnSoundOff = pygame.image.load('imagefolder/sound-off.png').convert_alpha()


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
        self.game_over = False
        self.sound_on = True
        self.player_connected = 0
        pygame.mixer.music.load('snd/background_music.mp3')  # tải file nhạc
        pygame.mixer.music.play(-1)  # phát nhạc (lặp đi lặp lại với -1)

        self.font = pygame.font.SysFont(None, 30)  # Use default system font with size 30
        self.player1_ready = False

    def create_thread(target):
        t = threading.Thread(target = target) #argument - target function
        t.daemon = True
        t.start()
        print("Created thread")
    
    def receive_msg():
        global msg
        while True:
            try:
                recvData = s.recv(2048 * 10)
                msg = recvData.decode()
                print("Receive form:", msg)
            except socket.error as e:
                print("Socket connection error:", e)
                break

        


    def data(self):
            folder_of_game = path.dirname(__file__)  # location of main.py
            image_folder = path.join(folder_of_game, 'imagefolder')
            Mazefolder = path.join(folder_of_game, 'MAZEFOLDER')
            sound_folder = path.join(folder_of_game, 'snd')
            self.maze = []
            with open(path.join(Mazefolder, 'MAZE1.txt'), 'rt') as f:
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
        self.walls = pygame.sprite.Group()  # created the walls group to hold them all
        self.bullets = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        for row, tiles in enumerate(self.maze):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '*':
                    self.player = Player(s,self, col, row)
                if tile == '-':
                    self.enemy = Enemy(s,self, col, row)
                # if tile == '@':
                #     ShieldItem(self, col, row)
                    
        self.game_over = False  # Đặt lại trạng thái game
        self.Score = False # reset score 
    
    def run(self):
        while not self.game_over:  # Thay đổi điều kiện dừng vòng lặp
            self.changing_time = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
        # Reset trạng thái điểm khi kết thúc màn chơi
        self.SCORE2 = 0
        self.SCORE1 = 0
        
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

            if self.game_over and event.type == pygame.KEYUP:
                self.new()
                self.run()
    def update(self):
        # keep track changing
        self.all_sprites.update()
        self.hit()



    def hit(self):
        self.hits1 = pygame.sprite.spritecollide(self.player, self.bullets, True, collide)
        if self.hits1:
            Explosion(self, self.player.rect.center)
            self.explosion_sound.play()
            self.player.kill()
            self.SCORE1 += 1
            self.playing = False
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(1000)
            self.new()
            self.data()
            
        if self.SCORE1 == 5:
            self.show_go_screen1()
                    
        self.hits2 = pygame.sprite.spritecollide(self.enemy, self.bullets, True, collide)
        if self.hits2:
            Explosion(self, self.enemy.rect.center)
            self.explosion_sound.play()
            self.enemy.kill()
            self.SCORE2 += 1
            self.playing = False
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(1000)
            self.new()
            self.data()
            
        if self.SCORE2 == 5:
            self.show_go_screen2()
                    
        # Draw all sprites after updating the explosions
        self.all_sprites.draw(self.screen)
        pygame.display.flip()  # Update the display after drawing
 
    def draw(self):
        # flip all the thing to screen
        self.screen.fill(BGCOLOR)
        self.grid()
        self.all_sprites.draw(self.screen)
        # kietbui
        # item_rect = self.threebullet.get_rect(center=self.screen.get_rect().center)
        # self.screen.blit(self.threebullet, item_rect)
        drawing_text(self.screen, str(self.SCORE1) + ':Green Tank', 25, 150, 710, GREEN)
        drawing_text(self.screen, 'Blue Tank:' + str(self.SCORE2), 25, 900, 710, BLUE)
        pygame.display.flip()

    def quit(self):
        pygame.quit()  # uninitialize all pygame modules
        quit()

    def show_go_screen1(self):
        self.screen.fill(BROWN)
        self.screen.blit(cup, (400,0))
        drawing_text(self.screen, 'Green Tank Win', 80, WIDTH / 2, HEIGHT / 3, GREEN)
        drawing_text(self.screen, 'SCORE:' + str(self.SCORE1) + '-' + str(self.SCORE2), 40, WIDTH / 2,  340, GREEN)
        drawing_text(self.screen, 'Press enter key to begin or escape key to quit', 40, WIDTH / 2, HEIGHT / 2, WHITE)
        scaled_player1 = pygame.transform.scale(player1, (300, 300))
        self.screen.blit(scaled_player1, (350,500))
        pygame.display.flip()
        self.wait_for_key()
        self.game_over = True
    def show_go_screen2(self):
        self.screen.fill(BROWN)
        self.screen.blit(cup, (400,0))
        drawing_text(self.screen, 'Blue Tank Win', 80, WIDTH / 2, HEIGHT / 3, BLUE)
        drawing_text(self.screen, 'SCORE:' + str(self.SCORE2) + '-' + str(self.SCORE1) , 40, WIDTH / 2, 340, BLUE)
        drawing_text(self.screen, 'Press enter key to begin or escape key to quit', 40, WIDTH / 2, HEIGHT / 2, WHITE)
        scaled_player2 = pygame.transform.scale(player2, (300, 300))
        self.screen.blit(scaled_player2, (350,500))
        pygame.display.flip()
        self.wait_for_key()
        self.game_over = True


    def wait_for_key(self):
        key_pressed = False
        while not key_pressed:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:  # Only break the loop if 'Enter' is pressed
                         key_pressed = True
        self.Score = False  # Đặt lại trạng thái chơi game

                    
    def menu(self):
        scaler_bg = pygame.transform.scale(bgStart, (WIDTH, HEIGHT))
        self.screen.blit(scaler_bg, (0, 0))
        
        name_game = Button(100, 30, nameGame)
        name_game.draw()
        
        # Tạo nút "btnStart"
        btn_start = Button(450, 300, btnStart)
        btn_start.draw()
        
        btn_exit = Button(470, 450, btnExit)
        btn_exit.draw()
        
        btn_sound = Button(0, 0, btnSoundOn, btnSoundOff, True, game=self)
        btn_sound.draw()
    
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYUP:
                    self.Score = False
                    break  

            if btn_sound.draw():
                self.sound_on = not self.sound_on
                if self.sound_on:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
                    
            # Kiểm tra xem nút đã được nhấn chưa
            if btn_start.draw():
                break  # Thoát khỏi vòng lặp khi nút được nhấn
            elif btn_exit.draw():
                self.quit()
                
            pygame.display.flip()
            
    create_thread(receive_msg)

    #kietbui
    def waiting_screen(self):
        scaler_bg = pygame.transform.scale(bgStart, (WIDTH, HEIGHT))
        self.screen.blit(scaler_bg, (0, 0))
        
        name_game = Button(100, 30, nameGame)
        name_game.draw()
        
        # Hiển thị tiêu đề "Player 1" và "Player 2"
        player1_label = self.font.render("Player 1", True, (255, 255, 255))
        player2_label = self.font.render("Player 2", True, (255, 255, 255))
        self.screen.blit(player1_label, (250, 400))
        self.screen.blit(player2_label, (600, 400))
        # Kiểm tra xem Player 1 đã sẵn sàng chưa và hiển thị tương ứng
        if msg == "1" or msg == "2":
            ready_label = self.font.render("Player 1 Ready", True, (0, 255, 0))
        else:
            ready_label = self.font.render("Player 1 Not Ready", True, (255, 0, 0))
        self.screen.blit(ready_label, (250, 430))  # Đặt chữ "Ready" dưới Player 1

        if msg == "2":
            ready_label = self.font.render("Player 2 Ready", True, (0, 255, 0))
        else:
            ready_label = self.font.render("Player 2 Not Ready", True, (255, 0, 0))
        pygame.display.flip()
        self.screen.blit(ready_label, (650, 430))  # Đặt chữ "Ready" dưới Player 1

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.flip()

 
               
class Button():
    def __init__(self, x, y, image_on, image_off = None, is_sound_button = False, game = None):
        self.image_on = image_on
        self.image_off = image_off
        self.rect = self.image_on.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.is_sound_button = is_sound_button
        if self.is_sound_button:
            self.game = game

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

       # Kiểm tra trạng thái âm thanh nếu là nút âm thanh
        if self.is_sound_button:
            if self.game.sound_on:
                self.image = self.image_on
            else:
                self.image = self.image_off
        elif self.image_off is None:
            self.image = self.image_on

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, self.rect)
        return action

# create game objects
g = Game()
while True:
    g.menu()
    # g.waiting_screen()
    g.new()
    g.run()
    if not g.Score:  # Nếu người chơi đã kết thúc màn chơi
        continue  # Quay lại menu