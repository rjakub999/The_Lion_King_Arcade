import pygame
from pygame.locals import *
# import random
import time
from sys import exit

from constants import *
from graphics_and_sounds import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_icon(icon)
pygame.display.set_caption("The Lion King Arcade")
pygame.mouse.set_visible(False)
events = pygame.event.get()


class TheLionKingArcade:
    def __init__(self):
        self.screen_size = 800, 600     # rozmiar okna programu
        self.canvas_size = 400, 300     # rozmiar płótna
        self.canvas2_size = 400, 200    # canvas2 jest używane do przezroczystego pola ukończenia poziomu
        self.font = pygame.font.Font('press-start-2p.ttf', 8)
        self.font2 = pygame.font.Font('press-start-2p.ttf', 16)
        self.clock = pygame.time.Clock()
        self.fullscreen_mode = False
        self.fullscreen = FULLSCREEN | HWSURFACE | DOUBLEBUF  # HW = hardware
        self.screen = pygame.display.set_mode(self.screen_size, SRCALPHA)   # pygame.SRCALPHA - przezroczystość
        self.canvas = pygame.Surface(self.canvas_size, SRCALPHA)
        self.canvas2 = None
        self.running = True
        self.screen_state = START_STATE
        self.mouse_pressed = False  # czy naciśnięty jest dowolny klawisz myszy
        self.selected = 1   # w menu głównym
        self.start_time = time.time()
        self.lvl_map = None
        self.lvl_background = None
        self.player1_rect = pygame.Rect(SIMBA_RECT)
        self.player2_rect = pygame.Rect(RYAN_RECT)
        self.number_of_players = 0

        # stan gry
        self.world = None
        self.level = None
        self.player1_lives = None
        self.player2_lives = None
        self.player1_health = None
        self.player2_health = None
        self.player1_score = None
        self.player2_score = None
        self.player1_rings = None
        self.player2_rings = None
        self.time_left = 0
        self.simba_combo = 0  # Liczba przeciwników pokonanych bez dotykania ziemi
        self.ryan_combo = 0

        # stan gracza 1
        self.simba_moving_left = None
        self.simba_moving_right = None
        self.simba_vertical_momentum = None
        self.simba_air_timer = None
        self.simba_up_pressed = None
        self.simba_down_pressed = None
        self.simba_roaring = None
        self.simba_rolling = None
        self.simba_press_time = None  # wymagane do funkcji patrzenia postaci gracza w górę w i dół
        self.simba_underwater_time = None
        self.simba_flashing_time = None
        self.simba_action = None
        self.simba_frame = None
        self.simba_flip = None
        self.simba_animation_frames = {}

        # stan gracza 2
        self.ryan_moving_left = None
        self.ryan_moving_right = None
        self.ryan_vertical_momentum = None
        self.ryan_air_timer = None
        self.ryan_underwater_time = None
        self.ryan_flashing_time = None
        self.ryan_action = None
        self.ryan_frame = None
        self.ryan_flip = None
        self.ryan_animation_frames = {}

        # kolizje gracza 1
        self.simba_collisions = None
        self.simba_ring_collisions = None
        self.simba_heart_collisions = None
        self.simba_one_up_collisions = None
        self.simba_enemy_collisions = None
        self.simba_switch_collisions = None
        self.simba_spring_collisions = None
        self.simba_flag_collisions = None

        # kolizje gracza 2
        self.ryan_collisions = None
        self.ryan_ring_collisions = None
        self.ryan_heart_collisions = None
        self.ryan_one_up_collisions = None
        self.ryan_enemy_collisions = None
        self.ryan_switch_collisions = None
        self.ryan_spring_collisions = None
        self.ryan_flag_collisions = None

        # ruch platform i przeciwników
        self.platform_x = 0
        self.platform_y = 0
        self.enemy_x = 0

        self.true_scroll = [0, 0]
        self.switch_pressed = False
        self.looking_time = None    # do patrzenia w górę i w dół

        # W kwadratowych nawiasach podajemy, ile ma trwać każda pojedyncza klatka
        self.animation_database1 = {'idle': self.load_animation1('sprites/simba/idle', [8, 8, 8, 8, 8, 8, 8, 8, 8]),
                                    'run': self.load_animation1('sprites/simba/run', [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
                                                                                      4, 4]),
                                    'jump': self.load_animation1('sprites/simba/jump', [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                                                                                        8, 8, 8]),
                                    'roar': self.load_animation1('sprites/simba/roar', [8, 8, 8, 8, 8, 8, 8, 8, 8]),
                                    'roll': self.load_animation1('sprites/simba/roll', [8, 8, 8, 8, 8, 8, 8, 8]),
                                    'up': self.load_animation1('sprites/simba/up', [8, 8, 2048]),
                                    'crouch': self.load_animation1('sprites/simba/crouch', [8, 8, 2048]),
                                    'die': self.load_animation1('sprites/simba/die', [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                                                                                      8, 8, 8, 8, 24, 8, 8, 8, 8, 8, 8,
                                                                                      256])}
        self.animation_database2 = {'h_idle': self.load_animation2('sprites/ryan/h_idle', [8]),
                                    'h_run': self.load_animation2('sprites/ryan/h_run', [4, 4, 4, 4, 4, 4, 4, 4, 4,
                                                                                         4, 4, 4]),
                                    'h_die': self.load_animation2('sprites/ryan/h_die', [8, 8, 8, 8, 8, 8, 8, 8, 256])}

        self.tile_rects = 0
        self.ring_rects = 0
        self.heart_rects = 0
        self.one_up_rects = 0
        self.enemy_rects = 0
        self.switch_rects = 0
        self.spring_rects = 0
        self.flag_rects = 0

        self.simba_score_disp = None
        self.simba_enemy_bonus = 0
        self.ryan_score_disp = None
        self.ryan_enemy_bonus = 0
        self.camera_switched = False
        self.complete_screen = False

        self.screen_state = START_STATE
        pygame.mixer.music.load("music/4-2.mp3")
        pygame.mixer.music.play(-1)

    def draw_transparent_rect(self, rect_color, rect):
        self.canvas2 = pygame.Surface(pygame.Rect(rect).size, SRCALPHA)
        pygame.draw.rect(self.canvas2, rect_color, self.canvas2.get_rect())
        self.canvas.blit(self.canvas2, rect)

    def load_level(self):
        """Załaduj mapę danego poziomu"""
        self.time_left = 400
        self.lvl_background = pygame.image.load(f"backgrounds/{self.world}-{self.level}.png")
        self.change_music(f"music/{self.world}-{self.level}.mp3")
        path = f"levels/{self.world}-{self.level}.txt"

        f = open(path, 'r')  # 'r' - read, 'w' - write
        data = f.read()
        f.close()
        data = data.split('\n')
        level_map = []
        for row in data:
            level_map.append(list(row))

        self.simba_moving_right = False
        self.simba_moving_left = False
        self.simba_vertical_momentum = 0
        self.simba_air_timer = 0
        self.simba_up_pressed = False
        self.simba_down_pressed = False
        self.simba_roaring = False
        self.simba_rolling = False
        self.simba_press_time = None
        self.simba_underwater_time = None
        self.simba_action = 'idle'
        self.simba_frame = 0
        self.simba_flip = False

        if self.number_of_players == 2:
            self.ryan_moving_left = False
            self.ryan_moving_right = False
            self.ryan_vertical_momentum = 0
            self.ryan_air_timer = 0
            self.ryan_action = 'h_idle'
            self.ryan_frame = 0
            self.ryan_flip = False

        return level_map

    def load_animation1(self, path, frame_durations):
        """Animacja postaci gracza 1"""
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            # np. sprites/simba/idle/idle0.png
            animation_image = pygame.image.load(img_loc)
            self.simba_animation_frames[animation_frame_id] = animation_image.copy()
            for f in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    def load_animation2(self, path, frame_durations):
        """Animacja postaci gracza 2"""
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc)
            self.ryan_animation_frames[animation_frame_id] = animation_image.copy()
            for f in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    @staticmethod
    def change_music(music_path):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

    @staticmethod
    def change_action(action_var, frame, new_value):
        """Zmiana animacji postaci gracza"""
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame

    @staticmethod
    def collision_test(rect, tiles):
        hit_list = []
        for tile_collision in tiles:
            if rect.colliderect(tile_collision):
                hit_list.append(tile_collision)
        return hit_list

    def move(self, rect, movement, tiles):
        """Dotyczy platform"""
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)

        for tile_img in hit_list:
            if movement[0] > 0:
                rect.right = tile_img.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile_img.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile_obj in hit_list:
            if movement[1] > 0:
                rect.bottom = tile_obj.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile_obj.bottom
                collision_types['top'] = True
        return rect, collision_types

    def touch(self, rect, tiles):
        """Dotyczy obiektów do zdobycia i przeciwników niezniszczalnych"""
        collision_data = self.collision_test(rect, tiles)
        return collision_data

    def stomp_on_or_touch(self, rect, tiles):
        """Dotyczy przeciwników, na których da się skoczyć (funkcja do napisania)"""
        collision_data = self.collision_test(rect, tiles)
        return collision_data

    def restart(self):
        self.lvl_map = self.load_level()
        self.player1_rect.x, self.player1_rect.y = SIMBA_RECT[0], SIMBA_RECT[1]
        self.player1_health = 4
        if self.number_of_players == 2:
            self.player2_rect.x, self.player2_rect.y = RYAN_RECT[0], RYAN_RECT[1]
            self.player2_health = 4
        self.true_scroll = [0, 0]
        self.time_left = 400

    @staticmethod
    def disp_score(value):
        """Wyświetlanie zer w polu liczby punktów"""
        if value >= 100000:
            return str(value)
        elif value >= 10000:
            return "0" + str(value)
        elif value >= 1000:
            return "00" + str(value)
        elif value >= 100:
            return "000" + str(value)
        elif value >= 10:
            return "0000" + str(value)
        else:
            return "00000" + str(value)

    def disp_time_left(self):
        if self.time_left >= 100:
            return str(int(self.time_left))
        elif self.time_left >= 10:
            return "0" + str(int(self.time_left))
        elif self.time_left >= 1:
            return "00" + str(int(self.time_left))
        else:
            return "000"

    @staticmethod
    def disp_lives_or_rings(number):
        if number >= 10:
            return str(number)
        else:
            return "0" + str(number)

    def ring_collect(self, player):
        """Zdobycie pierścienia"""
        ring.play()
        if player == 'simba':
            self.player1_score += 100
            if self.player1_rings < 99:
                self.player1_rings += 1
            else:
                self.player1_rings = 0
                self.extra_life('simba')
        else:
            self.player2_score += 100
            if self.player2_rings < 99:
                self.player2_rings += 1
            else:
                self.player2_rings = 0
                self.extra_life('ryan')

    def heal(self, player):
        """Zdobycie serca"""
        power_up.play()
        if player == 'simba':
            self.player1_score += 200
            if self.player1_health < 4:
                self.player1_health += 1
        else:
            self.player2_score += 200
            if self.player2_health < 4:
                self.player2_health += 1

    def extra_life(self, player):
        """Dodatkowe życie"""
        one_up.play()
        if player == 'simba' and self.player1_lives < 99:  # Limit ilości żyć
            self.player1_lives += 1
        else:
            self.player2_lives += 1

    def enemy_defeat(self, player):
        """Pokonanie przeciwnika"""
        if player == 'simba':
            self.simba_combo += 1
            if self.simba_combo < 9:
                defeat.play()
            self.simba_vertical_momentum = -4  # odbicie się od przeciwnika
            self.simba_score_disp = 2     # czas wyświetlania punktów lub "1UP"
            if self.simba_combo == 1:
                self.simba_enemy_bonus = 100
            if self.simba_combo == 2:
                self.simba_enemy_bonus = 200
            if self.simba_combo == 3:
                self.simba_enemy_bonus = 400
            if self.simba_combo == 4:
                self.simba_enemy_bonus = 800
            if self.simba_combo == 5:
                self.simba_enemy_bonus = 1000
            if self.simba_combo == 6:
                self.simba_enemy_bonus = 2000
            if self.simba_combo == 7:
                self.simba_enemy_bonus = 4000
            if self.simba_combo == 8:
                self.simba_enemy_bonus = 8000
            if self.simba_combo >= 9:
                self.simba_enemy_bonus = 0
                self.extra_life('simba')
            self.player1_score += self.simba_enemy_bonus
        else:
            self.ryan_combo += 1
            if self.ryan_combo < 9:
                defeat.play()
            self.ryan_vertical_momentum = -4  # odbicie się od przeciwnika
            self.ryan_score_disp = 2  # czas wyświetlania punktów lub "1UP"
            if self.ryan_combo == 1:
                self.ryan_enemy_bonus = 100
            if self.ryan_combo == 2:
                self.ryan_enemy_bonus = 200
            if self.ryan_combo == 3:
                self.ryan_enemy_bonus = 400
            if self.ryan_combo == 4:
                self.ryan_enemy_bonus = 800
            if self.ryan_combo == 5:
                self.ryan_enemy_bonus = 1000
            if self.ryan_combo == 6:
                self.ryan_enemy_bonus = 2000
            if self.ryan_combo == 7:
                self.ryan_enemy_bonus = 4000
            if self.ryan_combo == 8:
                self.ryan_enemy_bonus = 8000
            if self.ryan_combo >= 9:
                self.ryan_enemy_bonus = 0
                self.extra_life('ryan')
            self.player2_score += self.ryan_enemy_bonus

    def hurt(self, player):
        """Otrzymanie obrażenia"""
        hurt.play()
        if player == 'simba':
            if self.player1_health > 1:
                self.player1_health -= 1
            else:
                self.player1_health = 4
                self.death('simba')
        else:
            if self.player2_health > 1:
                self.player2_health -= 1
            else:
                self.player2_health = 4
                self.death('ryan')

    def death(self, player):
        """Utrata życia"""
        if player == 'simba':
            self.player1_lives -= 1
            pygame.mixer.music.stop()
            death.play()
            self.screen_state = DEATH1_STATE
            self.start_time = time.time()
            if self.player1_lives > 0:
                self.player1_health = 4
                self.platform_x, self.platform_y, self.enemy_x = 0, 0, 0
                self.switch_pressed = False
        else:
            self.player2_lives -= 1
            pygame.mixer.music.stop()
            death.play()
            self.screen_state = DEATH2_STATE
            self.start_time = time.time()
            if self.player2_lives > 0:
                self.player2_health = 4
                self.platform_x, self.platform_y, self.enemy_x, self.switch_pressed = 0, 0, 0, False

    def level_complete(self):
        """Ukończenie poziomu"""
        self.complete_screen = True
        pygame.mixer.music.stop()
        lvl_complete.play()
        self.start_time = time.time()

    def next_level(self):
        self.complete_screen = False
        self.platform_x, self.platform_y, self.enemy_x, self.switch_pressed = 0, 0, 0, False
        if self.level < 4:
            self.level += 1
            self.lvl_map = self.load_level()
            self.player1_rect.x, self.player1_rect.y = SIMBA_RECT[0], SIMBA_RECT[1]
            if self.number_of_players == 2:
                self.player2_rect.x, self.player2_rect.y = RYAN_RECT[0], RYAN_RECT[1]
            self.true_scroll = [0, 0]
            self.time_left = 400
            self.player1_health = 4
            if self.number_of_players == 2:
                self.player2_health = 4
        elif self.world < 8:
            self.level = 1
            self.world += 1
            self.lvl_map = self.load_level()
            self.player1_rect.x, self.player1_rect.y = SIMBA_RECT[0], SIMBA_RECT[1]
            if self.number_of_players == 2:
                self.player2_rect.x, self.player2_rect.y = RYAN_RECT[0], RYAN_RECT[1]
            self.true_scroll = [0, 0]
            self.time_left = 400
        else:
            self.screen_state = GAME_COMPLETED_STATE
            self.world = None
            self.level = None
            self.player1_lives, self.player2_lives = None, None
            self.player1_health, self.player2_health = None, None
            # Nie ustawiać self.score na None, gdyż trzeba wyświetlić wynik na ekranie ukończenia gry!
            self.player1_rings, self.player2_rings = None, None
            self.time_left = None

    def selection_in_menu(self):
        sel_sound.play()
        if self.selected == 1:
            self.number_of_players = 1
            self.screen_state = INTRO_STATE
            self.change_music("music/intro.mp3")
            self.time_left = 400
        if self.selected == 2:
            self.number_of_players = 2
            self.screen_state = INTRO_STATE
            self.change_music("music/intro.mp3")
            self.time_left = 400
        elif self.selected == 3:
            self.screen_state = TUTORIAL_STATE
        elif self.selected == 4:
            self.screen_state = HIGHSCORES_STATE
        elif self.selected == 5:
            exit()

    def looking_up(self):
        self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'up')

    def looking_down(self):
        self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'crouch')

    def back_to_idle(self):
        self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'idle')

    def lion_cub_roar(self):
        roar.play()
        self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'roar')

    def lion_cub_spin(self):
        spin.play()
        self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'roll')

    # ================================================ STANY GRY ================================================
    def game_start(self):
        if 0.25 < abs(self.start_time - time.time()) < 2.25:
            self.canvas.blit(self.font2.render("LISEK TOD PRESENTS", True, GREEN), (58, 140))
        if abs(self.start_time - time.time()) > 2.5:
            self.canvas.blit(start_background, (0, 0))
            if int(abs(self.start_time - time.time())) % 4 == 0:
                a_color = RED
            elif int(abs(self.start_time - time.time())) % 4 == 1:
                a_color = GREEN
            elif int(abs(self.start_time - time.time())) % 4 == 2:
                a_color = YELLOW
            else:
                a_color = CYAN
            text1 = self.font2.render("A R C A D E", False, a_color)
            self.canvas.blit(text1, (100, 58))

            if int(abs(self.start_time - time.time()) * 2) % 2 == 0:
                text2 = self.font2.render("PRESS ENTER!", False, YELLOW)
                self.canvas.blit(text2, (24, 240))

            for s_event in events:
                if s_event.type == KEYDOWN:
                    if s_event.key == K_RETURN:
                        sel_sound.play()
                        self.screen_state = MENU_STATE

    def main_menu(self):
        """Menu główne"""
        self.canvas.blit(start_background, (0, 0))
        if int(abs(self.start_time - time.time())) % 4 == 0:
            a_color = RED
        elif int(abs(self.start_time - time.time())) % 4 == 1:
            a_color = GREEN
        elif int(abs(self.start_time - time.time())) % 4 == 2:
            a_color = YELLOW
        else:
            a_color = CYAN
        text1 = self.font2.render("A R C A D E", False, a_color)
        self.canvas.blit(text1, (100, 58))

        text2 = self.font2.render("1 PLAYER GAME", True, RED if self.selected == 1 else GREEN)
        self.canvas.blit(text2, (8, 158))
        text3 = self.font2.render("2 PLAYER GAME", True, RED if self.selected == 2 else GREEN)
        self.canvas.blit(text3, (8, 188))
        text4 = self.font2.render("HOW TO PLAY?", True, RED if self.selected == 3 else GREEN)
        self.canvas.blit(text4, (8, 218))
        text5 = self.font2.render("HIGHSCORES", True, RED if self.selected == 4 else GREEN)
        self.canvas.blit(text5, (8, 248))
        text6 = self.font2.render("EXIT", True, RED if self.selected == 5 else GREEN)
        self.canvas.blit(text6, (8, 278))

        # pętla eventów
        for m_event in events:
            # klawiatura
            if m_event.type == KEYDOWN:
                if m_event.key == K_UP:
                    my_sound.play()
                    if self.selected != 1:
                        self.selected -= 1
                    else:
                        self.selected = 5
                if m_event.key == K_DOWN:
                    my_sound.play()
                    if self.selected != 5:
                        self.selected += 1
                    else:
                        self.selected = 1
                if m_event.key == K_RETURN:  # przycisk 'Enter'
                    self.selection_in_menu()

            # ruch myszką
            if m_event.type == MOUSEMOTION:
                if 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 316 <= pygame.mouse.get_pos()[1] <= 343:
                    self.selected = 1
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 376 <= pygame.mouse.get_pos()[1] <= 403:
                    self.selected = 2
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 436 <= pygame.mouse.get_pos()[1] <= 463:
                    self.selected = 3
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 496 <= pygame.mouse.get_pos()[1] <= 526:
                    self.selected = 4
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 556 <= pygame.mouse.get_pos()[1] <= 586:
                    self.selected = 5

            # kliknięcie myszką
            if m_event.type == MOUSEBUTTONDOWN:
                if 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 316 <= pygame.mouse.get_pos()[1] <= 343:
                    sel_sound.play()
                    self.selection_in_menu()
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 376 <= pygame.mouse.get_pos()[1] <= 403:
                    sel_sound.play()
                    self.selection_in_menu()
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 436 <= pygame.mouse.get_pos()[1] <= 463:
                    sel_sound.play()
                    self.selection_in_menu()
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 496 <= pygame.mouse.get_pos()[1] <= 526:
                    sel_sound.play()
                    self.selection_in_menu()
                elif 20 <= pygame.mouse.get_pos()[0] <= 395 \
                        and 556 <= pygame.mouse.get_pos()[1] <= 586:
                    exit()

    def intro(self):
        self.time_left -= 1 / FPS * 10  # Co 0.1 sekundy
        self.canvas.blit(pridelands, (0, 0))
        intro_disp = intro_text[0:400 - int(self.time_left)].splitlines()  # Wyświetlaj po 1 znaku stringu
        for r, c in enumerate(intro_disp):
            self.canvas.blit(self.font.render(c, False, BLACK), (2, 2 + (self.font.get_height() + 4) * r))
        for i_event in events:
            if i_event.type == KEYDOWN:
                if i_event.key == K_RETURN:
                    self.screen_state = SINGLE_PLAYER_STATE if self.number_of_players == 1 else MULTI_PLAYER_STATE
                    self.world = 1
                    self.level = 1
                    self.player1_lives = 4
                    self.player1_health = 4
                    self.player1_score = 0
                    self.player1_rings = 0
                    if self.number_of_players == 2:
                        self.player2_lives = 4
                        self.player2_health = 4
                        self.player2_score = 0
                        self.player2_rings = 0
                    self.lvl_map = self.load_level()

    def playing_level_1_player_mode(self):
        """Funkcja odpowiedzialna za poziom w trybie 1 gracza"""
        self.time_left -= 1 / FPS * 2
        self.canvas.blit(self.lvl_background, (0, 0))

        if self.simba_underwater_time is not None:
            self.simba_underwater_time -= 1 / FPS * 0.5

        if self.simba_flashing_time is not None:
            self.simba_flashing_time -= 1 / FPS
            if self.simba_flashing_time <= 0:
                self.simba_flashing_time = None

        if self.simba_score_disp is not None:
            self.simba_score_disp -= 1 / FPS
            if self.simba_score_disp < 0:
                self.simba_score_disp = None

        if self.ryan_score_disp is not None:
            self.ryan_score_disp -= 1 / FPS
            if self.ryan_score_disp < 0:
                self.ryan_score_disp = None

        # ruch platform i przeciwników
        if not self.complete_screen:
            if int(self.time_left) % 8 >= 4:
                self.platform_x += PLATFORM_SPEED
            else:
                self.platform_x -= PLATFORM_SPEED
            if int(self.time_left) % 4 >= 2:
                self.platform_y += PLATFORM_SPEED
                self.enemy_x += ENEMY_SPEED
                # obracanie przeciwników, gdy idą w prawo
                enemy1 = pygame.transform.flip(tileF, True, False)
                enemy2 = pygame.transform.flip(tileG, True, False)
            else:
                self.platform_y -= PLATFORM_SPEED
                self.enemy_x -= ENEMY_SPEED
                enemy1 = tileF
                enemy2 = tileG
        else:
            enemy1 = tileF
            enemy2 = tileG

        # animacje
        if not self.complete_screen:
            if int(self.time_left * 2) % 4 == 0:
                ring_tile = tileB1
                barrel_tile = tileI1
            elif int(self.time_left * 2) % 4 == 1:
                ring_tile = tileB2
                barrel_tile = tileI2
            elif int(self.time_left * 2) % 4 == 2:
                ring_tile = tileB3
                barrel_tile = tileI3
            else:
                ring_tile = tileB4
                barrel_tile = tileI4
        else:
            ring_tile = tileB1
            barrel_tile = tileI1

        green_blocks = tile6_1 if not self.switch_pressed else tile6_2
        switch = tileS1 if not self.switch_pressed else tileS2

        # Tekst i piktogramy
        self.canvas.blit(simba_lives, (8, 0))
        text1 = self.font.render(f'X {self.disp_lives_or_rings(self.player1_lives)}', True, WHITE)
        self.canvas.blit(text1, (36, 2))
        for hp in range(self.player1_health):
            self.canvas.blit(heart, (36 + 10 * hp, 14))
        text2 = self.font.render(self.disp_score(self.player1_score), True, WHITE)
        self.canvas.blit(text2, (36, 26))
        self.canvas.blit(tileB1, (8, 38))
        text3 = self.font.render(f'X {self.disp_lives_or_rings(self.player1_rings)}', True, WHITE)
        self.canvas.blit(text3, (36, 44))
        text4 = self.font.render("WORLD", True, WHITE)
        self.canvas.blit(text4, (136, 8))
        text5 = self.font.render(f'{self.world}-{self.level}', True, WHITE)
        self.canvas.blit(text5, (142, 20))
        text6 = self.font.render("TIME", True, WHITE)
        self.canvas.blit(text6, (218, 8))
        text7 = self.font.render(self.disp_time_left(), True, WHITE)
        self.canvas.blit(text7, (223, 20))

        if self.simba_underwater_time is not None:
            text9 = self.font.render("SIMBA", True, BLUE)
            self.canvas.blit(text9, (8, 48))
            for o2 in range(int(self.simba_underwater_time)):
                pygame.draw.rect(self.canvas, BLUE, (64 + (o2 * 12), 48, 8, 8))

        # Przewijanie ekranu
        if not self.camera_switched:
            self.true_scroll[0] += (self.player1_rect.x - self.true_scroll[0] - 180) / 20
            self.true_scroll[1] += (self.player1_rect.y - self.true_scroll[1] - 119) / 20
        scroll = self.true_scroll.copy()

        if self.simba_up_pressed:
            self.looking_time += 1 / FPS * 2
            if 2 < self.looking_time < 2.5:
                scroll[1] -= LOOK_UP_DOWN * (self.looking_time - 2)
            elif self.looking_time >= 2.5:
                scroll[1] -= LOOK_UP_DOWN
        if self.simba_down_pressed:
            self.looking_time += 1 / FPS * 2
            if 2 < self.looking_time < 2.5:
                scroll[1] += LOOK_UP_DOWN * (self.looking_time - 2)
            elif self.looking_time >= 2.5:
                scroll[1] += LOOK_UP_DOWN

        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # Obiekty na mapie poziomu
        self.tile_rects = []
        self.ring_rects = []
        self.heart_rects = []
        self.one_up_rects = []
        self.enemy_rects = []
        self.switch_rects = []
        self.spring_rects = []
        self.flag_rects = []

        # Wyświetlanie obiektów na mapie poziomu
        y = 0
        for layer in self.lvl_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    self.canvas.blit(tile1, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == '2':
                    self.canvas.blit(tile2, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == '3':
                    self.canvas.blit(tile3, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == '4':
                    self.canvas.blit(tile4, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == '5':
                    self.canvas.blit(tile5, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == '6':
                    self.canvas.blit(green_blocks, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    if not self.switch_pressed:
                        self.tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == '9':
                    self.canvas.blit(tile9, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.spring_rects.append(pygame.Rect(x * 16, y * 16, 16, 32))
                if tile == 'A':
                    self.canvas.blit(tileA, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.one_up_rects.append(pygame.Rect(x * 16, y * 16, 23, 16))
                if tile == 'B':
                    self.canvas.blit(ring_tile, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.ring_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == 'C':
                    self.canvas.blit(tileC, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.heart_rects.append(pygame.Rect(x * 16, y * 16, 20, 32))
                if tile == 'D':
                    self.canvas.blit(tileD, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.flag_rects.append(pygame.Rect(x * 16, y * 16, 24, 32))
                if tile == 'E':
                    self.canvas.blit(tileE, (x * 16 - scroll[0], y * 16 - scroll[1]))
                if tile == 'F':
                    self.canvas.blit(enemy1, ((x + self.enemy_x) * 16 - scroll[0], y * 16 - scroll[1]))
                    self.enemy_rects.append(pygame.Rect((x + self.enemy_x) * 16, y * 16, 35, 32))
                if tile == 'G':
                    self.canvas.blit(enemy2, ((x + self.enemy_x) * 16 - scroll[0], y * 16 - scroll[1]))
                    self.enemy_rects.append(pygame.Rect((x + self.enemy_x) * 16, y * 16, 33, 32))
                if tile == 'H':
                    self.canvas.blit(tileH, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.enemy_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == 'I':
                    self.canvas.blit(barrel_tile, (x * 16 - scroll[0], (y + self.platform_y) * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, (y + self.platform_y) * 16, 64, 64))
                if tile == 'J':
                    self.canvas.blit(tileJ, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 28, 32))
                if tile == 'K':
                    self.canvas.blit(tileK, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 28, 32))
                if tile == 'L':
                    self.canvas.blit(tileL, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 28, 32))
                if tile == 'M':
                    self.canvas.blit(tileM, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 28, 32))
                if tile == 'N':
                    self.canvas.blit(tileN, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, y * 16, 32, 32))
                if tile == 'P':
                    self.canvas.blit(tileP, ((x + self.platform_x) * 16 - scroll[0], y * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect((x + self.platform_x) * 16, y * 16, 48, 8))
                if tile == 'p':
                    self.canvas.blit(tileP, (x * 16 - scroll[0], (y + self.platform_y) * 16 - scroll[1]))
                    self.tile_rects.append(pygame.Rect(x * 16, (y + self.platform_y) * 16, 48, 8))
                if tile == 'S':
                    self.canvas.blit(switch, (x * 16 - scroll[0], y * 16 - scroll[1]))
                    self.switch_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
                if tile == 'W':
                    self.canvas.blit(tileW, (x * 16 - scroll[0], y * 16 - scroll[1]))
                x += 1
            y += 1

        # Poruszanie się postaci gracza
        simba_movement = [0, 0]
        if not self.complete_screen:
            if self.simba_moving_left:
                simba_movement[0] -= PLAYER_SPEED if self.simba_underwater_time is None else PLAYER_UNDERWATER_SPEED
            if self.simba_moving_right:
                simba_movement[0] += PLAYER_SPEED if self.simba_underwater_time is None else PLAYER_UNDERWATER_SPEED
            simba_movement[1] += self.simba_vertical_momentum
            self.simba_vertical_momentum += 0.16 if self.simba_underwater_time is None else 0.32
            if self.simba_underwater_time is None:
                if self.simba_vertical_momentum > 3:
                    self.simba_vertical_momentum = 3
            else:
                if self.simba_vertical_momentum > 1.5:
                    self.simba_vertical_momentum = 1.5

        # Zmiana animacji postaci gracza
        if simba_movement[0] > 0:
            self.simba_flip = False
            self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'run')
        if simba_movement[0] < 0:
            self.simba_flip = True
            self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'run')
        if simba_movement[1] < 0:
            self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'jump')
        if simba_movement[0] == simba_movement[1] == 0 and not self.simba_up_pressed and not self.simba_down_pressed \
                and not self.simba_roaring and not self.simba_rolling:
            self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'idle')

        # Rodzaje kolizji
        player1_rect, self.simba_collisions = self.move(self.player1_rect, simba_movement, self.tile_rects)
        self.simba_ring_collisions = self.touch(self.player1_rect, self.ring_rects)
        self.simba_heart_collisions = self.touch(self.player1_rect, self.heart_rects)
        self.simba_one_up_collisions = self.touch(self.player1_rect, self.one_up_rects)
        self.simba_enemy_collisions = self.touch(self.player1_rect, self.enemy_rects)
        self.simba_switch_collisions = self.touch(self.player1_rect, self.switch_rects)
        self.simba_spring_collisions = self.touch(self.player1_rect, self.spring_rects)
        self.simba_flag_collisions = self.touch(self.player1_rect, self.flag_rects)

        # Kolizje z powierzchnią
        if self.simba_collisions['bottom']:
            self.simba_air_timer = 0
            self.simba_vertical_momentum = 0
            self.simba_combo = 0
        else:
            self.simba_air_timer += 1

        if self.simba_collisions['top']:
            self.simba_air_timer += 0
            self.simba_vertical_momentum = 0

        # Kolizje z pierścieniami i powerupami
        if self.simba_ring_collisions:  # Jeśli lista ring_collisions[] nie jest pusta
            self.ring_collect('simba')
            # usunięcie obiektu z lvl_map
            x = int(self.simba_ring_collisions[0][0] / 16)
            y = int(self.simba_ring_collisions[0][1] / 16)
            self.lvl_map[y][x] = '0'
        if self.simba_heart_collisions:
            self.heal('simba')
            x = int(self.simba_heart_collisions[0][0] / 16)
            y = int(self.simba_heart_collisions[0][1] / 16)
            self.lvl_map[y][x] = '0'
        if self.simba_one_up_collisions:
            self.extra_life('simba')
            x = int(self.simba_one_up_collisions[0][0] / 16)
            y = int(self.simba_one_up_collisions[0][1] / 16)
            self.lvl_map[y][x] = '0'
        if self.simba_enemy_collisions and not self.simba_flashing_time:
            self.hurt('simba')
            if self.player1_health in (1, 2, 3):
                self.simba_flashing_time = 3
        if self.simba_spring_collisions:
            self.simba_vertical_momentum = -8
        if self.simba_flag_collisions and not self.complete_screen:
            self.level_complete()

        # Wyświetlanie animacji postaci gracza
        if not self.simba_flashing_time or (self.simba_flashing_time and (int(self.time_left * 10) % 2 == 0)):
            self.simba_frame += 1
            if self.simba_frame >= len(self.animation_database1[self.simba_action]):
                self.simba_frame = 0
            simba_img_id = self.animation_database1[self.simba_action][self.simba_frame]
            simba_img = self.simba_animation_frames[simba_img_id]
            self.canvas.blit(pygame.transform.flip(simba_img, self.simba_flip, False),
                             (player1_rect.x - scroll[0], player1_rect.y - scroll[1]))

        # Wyświetlanie punktów po pokonaniu przeciwnika
        if self.simba_score_disp:
            if self.simba_combo < 9:
                score_text = self.font.render(str(self.simba_enemy_bonus), True, WHITE)
            else:
                score_text = self.font.render("1UP", True, YELLOW)
            self.canvas.blit(score_text, (player1_rect.x - scroll[0], player1_rect.y - scroll[1] - 50))

        # Pole ukończenia poziomu
        if self.complete_screen:
            self.draw_transparent_rect(GREEN_TRANSPARENT, (30, 70, 340, 180))
            text10 = self.font2.render(f"WORLD {self.world}-{self.level} COMPLETED!", True, ORANGE)
            self.canvas.blit(text10, (45, 85))

        # śmierć przez spadnięcie lub utonięcie, lub koniec czasu
        # UWAGA: Jeśli warunek self.underwater_time is not None nie jest spełniony, to program nie sprawdza warunku
        # po "and", w przeciwnym wypadku zgłosiłby błąd.
        if not self.complete_screen:
            if self.player1_rect.y > 400 or (self.simba_underwater_time is not None
                                             and self.simba_underwater_time < 0) or self.time_left <= 0:
                self.death('simba')

        # pętla eventów
        for l_event in events:
            # klawiatura
            if l_event.type == KEYDOWN:
                if l_event.key == K_UP:
                    self.simba_up_pressed = True
                    self.looking_up()
                    self.looking_time = 0
                if l_event.key == K_DOWN:
                    self.simba_down_pressed = True
                    self.looking_down()
                    self.looking_time = 0
                if l_event.key == K_LEFT:
                    self.simba_moving_left = True
                if l_event.key == K_RIGHT:
                    self.simba_moving_right = True
                if l_event.key == K_z:
                    if self.simba_air_timer < 6:
                        self.simba_vertical_momentum = -5
                if l_event.key == K_x:
                    self.simba_roaring = True
                    self.lion_cub_roar()
                if l_event.key == K_c:
                    self.simba_rolling = True
                    self.lion_cub_spin()
                if l_event.key == K_F2:
                    self.enemy_defeat('simba')
                if self.simba_switch_collisions and l_event.key == K_LCTRL:
                    my_sound.play()
                    self.switch_pressed = not self.switch_pressed
                if l_event.key == K_F4:
                    self.simba_underwater_time = 8

            if l_event.type == KEYUP:
                if l_event.key == K_UP:
                    self.simba_up_pressed = False
                    self.back_to_idle()
                    self.looking_time = None
                if l_event.key == K_DOWN:
                    self.simba_down_pressed = False
                    self.back_to_idle()
                    self.looking_time = None
                if l_event.key == K_LEFT:
                    self.simba_moving_left = False
                    self.back_to_idle()
                if l_event.key == K_RIGHT:
                    self.simba_moving_right = False
                    self.back_to_idle()
                if l_event.key == K_x:
                    self.back_to_idle()
                    self.simba_roaring = False
                if l_event.key == K_a:
                    self.back_to_idle()
                    self.simba_rolling = False

    def playing_level_2_player_mode(self):
        self.playing_level_1_player_mode()  # wykonywanie wszystkiego, co robi poprzednia funkcja

        if self.ryan_flashing_time is not None:
            self.ryan_flashing_time -= 1 / FPS
            if self.ryan_flashing_time <= 0:
                self.ryan_flashing_time = None

        self.canvas.blit(ryan_lives, (318, 0))
        text8 = self.font.render(f'X {self.disp_lives_or_rings(self.player2_lives)}', True, WHITE)
        self.canvas.blit(text8, (346, 2))
        for hp in range(self.player2_health):
            self.canvas.blit(heart, (346 + 10 * hp, 14))
        text9 = self.font.render(self.disp_score(self.player2_score), True, WHITE)
        self.canvas.blit(text9, (346, 26))
        self.canvas.blit(tileB1, (318, 38))
        text10 = self.font.render(f'X {self.disp_lives_or_rings(self.player2_rings)}', True, WHITE)
        self.canvas.blit(text10, (346, 44))

        if self.camera_switched:
            self.true_scroll[0] += (self.player2_rect.x - self.true_scroll[0] - 180) / 20
            self.true_scroll[1] += (self.player2_rect.y - self.true_scroll[1] - 119) / 20
        scroll = self.true_scroll.copy()

        if self.simba_up_pressed:
            self.looking_time += 1 / FPS * 2
            if 2 < self.looking_time < 2.5:
                scroll[1] -= LOOK_UP_DOWN * (self.looking_time - 2)
            elif self.looking_time >= 2.5:
                scroll[1] -= LOOK_UP_DOWN
        if self.simba_down_pressed:
            self.looking_time += 1 / FPS * 2
            if 2 < self.looking_time < 2.5:
                scroll[1] += LOOK_UP_DOWN * (self.looking_time - 2)
            elif self.looking_time >= 2.5:
                scroll[1] += LOOK_UP_DOWN

        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        # Poruszanie się postaci drugiego gracza
        ryan_movement = [0, 0]
        if not self.complete_screen:
            if self.ryan_moving_left:
                ryan_movement[0] -= PLAYER_SPEED if self.ryan_underwater_time is None else PLAYER_UNDERWATER_SPEED
            if self.ryan_moving_right:
                ryan_movement[0] += PLAYER_SPEED if self.ryan_underwater_time is None else PLAYER_UNDERWATER_SPEED
            ryan_movement[1] += self.ryan_vertical_momentum
            self.ryan_vertical_momentum += 0.16 if self.ryan_underwater_time is None else 0.32
            if self.ryan_underwater_time is None:
                if self.ryan_vertical_momentum > 3:
                    self.ryan_vertical_momentum = 3
            else:
                if self.ryan_vertical_momentum > 1.5:
                    self.ryan_vertical_momentum = 1.5

        # Zmiana animacji postaci drugiego gracza
        if ryan_movement[0] > 0:
            self.ryan_flip = False
            self.ryan_action, self.ryan_frame = self.change_action(self.ryan_action, self.ryan_frame, 'h_run')
        if ryan_movement[0] < 0:
            self.ryan_flip = True
            self.ryan_action, self.ryan_frame = self.change_action(self.ryan_action, self.ryan_frame, 'h_run')
        if ryan_movement[0] == 0:
            self.ryan_action, self.ryan_frame = self.change_action(self.ryan_action, self.ryan_frame, 'h_idle')

        # Rodzaje kolizji
        player2_rect, self.ryan_collisions = self.move(self.player2_rect, ryan_movement, self.tile_rects)
        self.ryan_ring_collisions = self.touch(self.player2_rect, self.ring_rects)
        self.ryan_heart_collisions = self.touch(self.player2_rect, self.heart_rects)
        self.ryan_one_up_collisions = self.touch(self.player2_rect, self.one_up_rects)
        self.ryan_enemy_collisions = self.touch(self.player2_rect, self.enemy_rects)
        self.ryan_switch_collisions = self.touch(self.player2_rect, self.switch_rects)
        self.ryan_spring_collisions = self.touch(self.player2_rect, self.spring_rects)
        self.ryan_flag_collisions = self.touch(self.player2_rect, self.flag_rects)

        # Kolizje z powierzchnią
        if self.ryan_collisions['bottom']:
            self.ryan_air_timer = 0
            self.ryan_vertical_momentum = 0
            self.ryan_combo = 0
        else:
            self.ryan_air_timer += 1

        if self.ryan_collisions['top']:
            self.ryan_air_timer += 0
            self.ryan_vertical_momentum = 0

        # Kolizje z pierścieniami i powerupami
        if self.ryan_ring_collisions:  # Jeśli lista ring_collisions[] nie jest pusta
            self.ring_collect('ryan')
            # usunięcie obiektu z lvl_map
            x = int(self.ryan_ring_collisions[0][0] / 16)
            y = int(self.ryan_ring_collisions[0][1] / 16)
            self.lvl_map[y][x] = '0'
        if self.ryan_heart_collisions:
            self.heal('ryan')
            x = int(self.ryan_heart_collisions[0][0] / 16)
            y = int(self.ryan_heart_collisions[0][1] / 16)
            self.lvl_map[y][x] = '0'
        if self.ryan_one_up_collisions:
            self.extra_life('ryan')
            x = int(self.ryan_one_up_collisions[0][0] / 16)
            y = int(self.ryan_one_up_collisions[0][1] / 16)
            self.lvl_map[y][x] = '0'
        if self.ryan_enemy_collisions and not self.ryan_flashing_time:
            self.hurt('ryan')
            if self.player2_health in (1, 2, 3):
                self.ryan_flashing_time = 3
        if self.ryan_spring_collisions:
            self.ryan_vertical_momentum = -8
        if self.ryan_flag_collisions and not self.complete_screen:
            self.level_complete()

        # Wyświetlanie animacji postaci drugiego gracza
        if not self.ryan_flashing_time or (self.ryan_flashing_time and (int(self.time_left * 10) % 2 == 0)):
            self.ryan_frame += 1
            if self.ryan_frame >= len(self.animation_database2[self.ryan_action]):
                self.ryan_frame = 0
            ryan_img_id = self.animation_database2[self.ryan_action][self.ryan_frame]
            ryan_img = self.ryan_animation_frames[ryan_img_id]
            ryan_img_scaled = pygame.transform.scale(ryan_img, (int(ryan_img.get_size()[0] * 0.75),
                                                                int(ryan_img.get_size()[1] * 0.75)))
            self.canvas.blit(pygame.transform.flip(ryan_img_scaled, self.ryan_flip, False),
                             (player2_rect.x - scroll[0], player2_rect.y - scroll[1]))

        # Wyświetlanie punktów po pokonaniu przeciwnika
        if self.ryan_score_disp:
            if self.ryan_combo < 9:
                score_text = self.font.render(str(self.ryan_enemy_bonus), True, WHITE)
            else:
                score_text = self.font.render("1UP", True, YELLOW)
            self.canvas.blit(score_text, (player2_rect.x - scroll[0], player2_rect.y - scroll[1] - 50))

        if self.player2_rect.y > 400:
            self.death('ryan')

        # pętla eventów
        for l_event in events:
            # klawiatura
            if l_event.type == KEYDOWN:
                if l_event.key == K_a:
                    self.ryan_moving_left = True
                if l_event.key == K_d:
                    self.ryan_moving_right = True
                if l_event.key == K_w:
                    if self.ryan_air_timer < 6:
                        self.ryan_vertical_momentum = -5
                if l_event.key == K_SPACE:
                    self.camera_switched = not self.camera_switched
                if l_event.key == K_F3:
                    self.enemy_defeat('ryan')
            if l_event.type == KEYUP:
                if l_event.key == K_a:
                    self.ryan_moving_left = False
                if l_event.key == K_d:
                    self.ryan_moving_right = False

    def death1_animation(self):
        if abs(self.start_time - time.time()) < 5:
            self.simba_frame += 1
            self.simba_action, self.simba_frame = self.change_action(self.simba_action, self.simba_frame, 'die')
            if self.simba_frame >= len(self.animation_database1[self.simba_action]):
                self.simba_frame = 0
            player_img_id = self.animation_database1[self.simba_action][self.simba_frame]
            player_img = self.simba_animation_frames[player_img_id]
            self.canvas.blit(player_img, (180, 125))

        if abs(self.start_time - time.time()) >= 8:
            if self.player1_lives > 0:
                self.screen_state = SINGLE_PLAYER_STATE if self.number_of_players == 1 else MULTI_PLAYER_STATE
                self.restart()
            else:
                self.screen_state = GAME_OVER_STATE
                game_over.play()

    def death2_animation(self):
        if abs(self.start_time - time.time()) < 5:
            self.ryan_frame += 1
            self.ryan_action, self.ryan_frame = self.change_action(self.ryan_action, self.ryan_frame, 'h_die')
            if self.ryan_frame >= len(self.animation_database2[self.ryan_action]):
                self.ryan_frame = 0
            player_img_id = self.animation_database2[self.ryan_action][self.ryan_frame]
            player_img = self.ryan_animation_frames[player_img_id]
            player_img_scaled = pygame.transform.scale(player_img, (int(player_img.get_size()[0] * 0.75),
                                                                    int(player_img.get_size()[1] * 0.75)))
            self.canvas.blit(player_img_scaled, (180, 125))

        if abs(self.start_time - time.time()) >= 8:
            if self.player2_lives > 0:
                self.screen_state = MULTI_PLAYER_STATE
                self.restart()
            else:
                self.screen_state = GAME_OVER_STATE
                game_over.play()

    def game_over(self):
        pass

    def game_completed(self):
        pass

    def how_to_play(self):
        self.canvas.blit(tutorial_background, (0, 0))
        for h_event in events:
            if h_event.type == KEYDOWN:
                if h_event.key == K_RETURN:
                    self.screen_state = MENU_STATE
            if h_event.type == JOYBUTTONUP:
                if h_event.button == 9:
                    self.screen_state = MENU_STATE

    def highscores_table(self):
        for hi_event in events:
            if hi_event.type == KEYDOWN:
                if hi_event.key == K_RETURN:
                    self.screen_state = MENU_STATE
            if hi_event.type == JOYBUTTONUP:
                if hi_event.button == 9:
                    self.screen_state = MENU_STATE

    def main_loop(self):
        """Funkcja, która zawiera główną pętlę gry"""
        global events

        while True:
            self.canvas.fill(BLACK)

            # FINITE STATEMENT MACHINES
            if self.screen_state == START_STATE:
                self.game_start()
            elif self.screen_state == MENU_STATE:
                self.main_menu()
            elif self.screen_state == INTRO_STATE:
                self.intro()
            elif self.screen_state == SINGLE_PLAYER_STATE:
                self.playing_level_1_player_mode()
            elif self.screen_state == MULTI_PLAYER_STATE:
                self.playing_level_2_player_mode()
            elif self.screen_state == DEATH1_STATE:
                self.death1_animation()
            elif self.screen_state == DEATH2_STATE:
                self.death2_animation()
            elif self.screen_state == GAME_OVER_STATE:
                self.game_over()
            elif self.screen_state == GAME_COMPLETED_STATE:
                self.game_completed()
            elif self.screen_state == TUTORIAL_STATE:
                self.how_to_play()
            elif self.screen_state == HIGHSCORES_STATE:
                self.highscores_table()

            events = pygame.event.get()
            for event in events:  # pętla eventów
                if event.type == QUIT:
                    exit()

                if event.type == MOUSEBUTTONDOWN:
                    self.mouse_pressed = True
                if event.type == MOUSEBUTTONUP:
                    self.mouse_pressed = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    if event.key == K_F1:  # pełny ekran / widok w oknie
                        if self.fullscreen_mode:
                            self.screen = pygame.display.set_mode(self.screen_size, 0, SRCALPHA)
                        else:
                            self.screen = pygame.display.set_mode(self.screen_size, self.fullscreen, SRCALPHA)
                        self.fullscreen_mode = not self.fullscreen_mode

            self.screen.blit(pygame.transform.scale(self.canvas, self.screen_size), (0, 0))

            # łapkowy kursor
            if self.screen_state == MENU_STATE:
                self.screen.blit(cursor_1 if not self.mouse_pressed else cursor_2,
                                 (pygame.mouse.get_pos()[0] - 8, pygame.mouse.get_pos()[1] - 8))

            pygame.display.update()
            self.clock.tick(FPS)


instance = TheLionKingArcade()
