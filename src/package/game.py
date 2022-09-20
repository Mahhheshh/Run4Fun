import pygame 
import sys
import random
from package.ui import Text
from package.Enemy import Enemy, Vulture
from package.environment import Background
from package.player import Player

class Game:
    def __init__(self, SCREEN, SCALEX, SCALEY, background_image,  menu_background):
        self.state = "menu"
        self.SCREEN = SCREEN
        self.size = (SCREEN.get_width(), SCREEN.get_height())
        self.menu_img = menu_background
        self.background_image = background_image
        self.button = Text(SCREEN, "font\ARCADECLASSIC.TTF", 30)
        self.enemy = Enemy(SCREEN, SCALEX, SCALEY, 900)
        self.player = Player(SCREEN, SCALEX, SCALEY)
        self.vulture = Vulture(SCREEN, SCALEX, SCALEY)
        self.bg = Background(SCREEN, background_image)
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        self.player_group.add(self.player)
        self.enemy_group.add(self.enemy)
        self.enemy_group.add(self.vulture)
        self.reset = False
        self.score = 0

    def menu(self):
        self.SCREEN.blit(self.menu_img, (0, 0))
        self.button.labels("Press  any  key  to  start", (self.SCREEN.get_rect().center[0], self.SCREEN.get_rect().center[1]-100))
        self.button.labels("S  Or  ArrowDown To  Slide", (self.SCREEN.get_rect().center[0], self.SCREEN.get_rect().center[1]-50))
        self.button.labels("Esp To Open Menu", (self.SCREEN.get_rect().center[0], self.SCREEN.get_rect().center[1]))
        self.button.labels("Space  To  Jump", (self.SCREEN.get_rect().center[0], self.SCREEN.get_rect().center[1]+50))
        self.button.labels("P  To  Pause", (self.SCREEN.get_rect().center[0], self.SCREEN.get_rect().center[1]+100))
        pygame.display.flip()

    def main_game(self):
        self.bg.scroll_background()
        self.player_group.draw(self.SCREEN)
        self.enemy_group.draw(self.SCREEN)
        self.enemy_group.update()
        self.player_group.update()
        # self.button.labels(f"obj   count {len(self.enemy_group)}", (250, 10))
        if (len(self.enemy_group) < 2):
            if random.randint(0, 1) == 0:
                new_pos = random.randrange(self.size[0], self.size[0]+159, 5)
                self.enemy_group.add(Enemy(self.SCREEN, 60, 60, new_pos+220))
            else:
                self.enemy_group.add(Vulture(self.SCREEN, 60, 60))
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False, pygame.sprite.collide_mask):
            self.state = "game_end"
            # pass
        self.display_score()
        pygame.display.flip()

    def pause(self):
        self.button.labels("Paused", self.SCREEN.get_rect().center)
        pygame.display.flip()

    def end_game(self):
        self.button.labels("pree any key to restart!", self.SCREEN.get_rect().center)
        if self.reset:
            self.restart()
        pygame.display.flip()

    def restart(self):
        self.__init__(self.SCREEN, 60, 60, self.background_image, self.menu_img)
        self.state = "main_game"
    
    def display_score(self):
        self.score += 0.2
        self.button.labels(f"{int(self.score)}", (30, 10))
        if self.score % 100 == 0:
            self.enemy.game_speed += 1
            self.vulture.game_speed += 1
            self.bg.game_speed += 1

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) and (self.state != "game_end"):
                    self.state = "menu"
                if (event.key == pygame.K_p) and (self.state != "menu") and (self.state != "game_end"):
                    self.state = "pause"
                if (event.key != pygame.K_p) and (event.key != pygame.K_ESCAPE) and (self.state != "game_end"):
                    self.state = "main_game"
                if (self.state == "game_end"):
                    self.reset = True
        self.state_manager()

    def state_manager(self):
        if self.state == "main_game":
            self.main_game()
        elif self.state == "menu":
            self.menu()
        elif self.state == "pause":
            self.pause()
        elif self.state == "game_end":
            self.end_game()