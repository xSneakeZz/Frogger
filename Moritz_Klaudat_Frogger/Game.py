import os
from random import randint
import pygame
import pygame.sprite
import pygame.mask

class Settings:
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 600
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class CarLeft(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, start_x):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "car_L_v1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150 ))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.start_x = start_x

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = Settings.WINDOW_WIDTH
            self.rect.y = self.start_x

class CarRight(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, start_x):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "car_r_v1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150 ))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.start_x = start_x

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > Settings.WINDOW_WIDTH:
            self.rect.right = 0
            self.rect.y = self.start_x

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, lives):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "player_v1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.lives = lives

    def update(self, keys):
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed  

        if self.rect.left > Settings.WINDOW_WIDTH:
            self.rect.right = -1
        if self.rect.right < 0:
            self.rect.left = Settings.WINDOW_WIDTH
        if self.rect.top > Settings.WINDOW_HEIGHT:
            self.rect.bottom = -1
        if self.rect.bottom < 0:
            self.rect.top = Settings.WINDOW_HEIGHT

    def reset_position(self):
        self.rect.center = (Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT - 26)

class Game:
    def __init__(self):
        os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
        pygame.display.set_caption("Car Game")
        self.clock = pygame.time.Clock()
        self.cars = pygame.sprite.Group()
        self.player = Player(Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT - 26, 2, 3)  
        self.running = True
        self.esc_pressed = 0
        self.paused = False  
        self.pause_font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 72)
        self.win_font = pygame.font.Font(None, 72)
        self.game_over = False
        self.win = False
        self.current_level = 1
        self.level = 1
        self.seed_increment = 10
        self.goal_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "busstation_v1.png")).convert_alpha()
        self.goal_image = pygame.transform.scale(self.goal_image, (200, 200))
        self.goal_rect = self.goal_image.get_rect()
        self.goal_mask = pygame.mask.from_surface(self.goal_image)
        self.goal_rect.center = (Settings.WINDOW_WIDTH - self.goal_image.get_width(), 0)

        self.background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "street_v1.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))

        # Feste Koordinaten für Autos von links nach rechts
        car_positions_right = [(250, 250),(350, 350)]
        for pos in car_positions_right:
            x, y = pos
            speed = randint(3 + self.level, 5 + self.level)
            self.cars.add(CarRight(x, y, speed, y))

        # Feste Koordinaten für Autos von rechts nach links
        car_positions_left = [(50, 50),(150, 150)]
        for pos in car_positions_left:
            x, y = pos
            speed = randint(3 + self.level, 5 + self.level)
            self.cars.add(CarLeft(x, y, speed, y))

        self.heart_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "heart.png")).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused and self.running:
                if not self.game_over and self.running:
                    if not self.win and self.running:
                        self.update()
            self.draw()
            self.clock.tick(Settings.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.esc_pressed += 1
                    if self.esc_pressed >= 2:
                        self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    print("R key pressed")  
                    if self.game_over or self.win:
                        self.restart_game()
                   # elif self.win:
                     #   self.restart_game()
                elif event.key == pygame.K_r and not self.game_over and not self.win:
                    self.restart_game()

                

    def restart_game(self):
        self.running = True
        self.win = False
        self.game_over = False
        self.player.lives = 3
        self.player.reset_position()
        self.cars.empty()

        
        car_positions_right = [(250, 250),(350, 350)]
        for pos in car_positions_right:
            x, y = pos
            speed = randint(3 + self.level, 5 + self.level)
            self.cars.add(CarRight(x, y, speed, y))

        
        car_positions_left = [(50, 50), (150, 150)]
        for pos in car_positions_left:
            x, y = pos
            speed = randint(3 + self.level, 5 + self.level)
            self.cars.add(CarLeft(x, y, speed, y))

   

    def update(self):
        keys = pygame.key.get_pressed()
        if self.running:
            if not self.game_over and not self.win: 
                self.player.update(keys)

                for car in self.cars:
                    car.update()
                    if pygame.sprite.collide_mask(self.player, car):
                        self.player.lives -= 1
                        if self.player.lives <= 0:
                            self.game_over = True
                            break
                        else:
                            self.player.reset_position()

                if self.player.rect.colliderect(self.goal_rect):
                    if self.level < 3:  
                        self.level += 1
                        self.seed_increment += 20
                        self.restart_game()
                        return
                    else:
                        self.win = True
                        self.level = 1
                        return
                        

        
        if self.game_over or self.win:
            self.level = 1
          

    def update_level_text(self):
        self.level += 1 
        self.seed_increment += 20

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.cars.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.goal_image, self.goal_rect) 

     
        for i in range(self.player.lives):
            self.screen.blit(self.heart_image, (10 + i * 40, 10))

        if self.paused: 
            pause_surface = pygame.Surface((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
            pause_surface.set_alpha(128) 
            pause_surface.fill((128, 128, 128))  
            self.screen.blit(pause_surface, (0, 0))
            pause_text = self.pause_font.render("Pause", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)

        if self.game_over:
            game_over_surface = pygame.Surface((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
            game_over_surface.set_alpha(128) 
            game_over_surface.fill((128, 128, 128))  
            self.screen.blit(game_over_surface, (0, 0))
            game_over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        
        level_text = self.game_over_font.render(f"Level {self.level}", True, (255, 0, 0))
        level_rect = level_text.get_rect(center=(Settings.WINDOW_WIDTH // 2, 30))
        self.screen.blit(level_text, level_rect)


        if self.win:
            win_surface = pygame.Surface((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
            win_surface.set_alpha(128) 
            win_surface.fill((128, 128, 128))  
            self.screen.blit(win_surface, (0, 0))
            win_text = self.win_font.render("WIN", True, (255, 255, 255))
            text_rect = win_text.get_rect(center=(Settings.WINDOW_WIDTH // 2, Settings.WINDOW_HEIGHT // 2))
            self.screen.blit(win_text, text_rect)

        pygame.display.flip()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
