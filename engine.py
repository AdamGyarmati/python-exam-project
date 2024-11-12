import pygame
from board.game_board import GameBoard
from game_objects.mosquito import Mosquito
from game_objects.bee import Bee
from game_objects.stinky_bug import StinkyBug
from own_io.save_score import WriteJsonData
from utils.utils import FILE_TO_WRITE


class Engine:
    def __init__(self, gameboard: GameBoard):
        self._gameboard = gameboard
        self._write_json = WriteJsonData(FILE_TO_WRITE)

    def start_game(self):
        mouse_game = False
        hand_game = False
        while True:
            if not mouse_game and not hand_game:
                start_button_mouse_rect, start_button_hand_rect = self._gameboard.draw_start_screen(pygame.mouse.get_pos())

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if start_button_mouse_rect.collidepoint(event.pos):
                            mouse_game = True  # Játék elindítása
                        elif start_button_hand_rect.collidepoint(event.pos):
                            hand_game = True  # Játék elindítása

            elif mouse_game:
                self.run_mouse()
                break
            elif hand_game:
                self.run_hand()
                break

    def run_mouse(self):
        self.init_timing()
        while self._gameboard.is_running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self._gameboard.is_running = False
                    case pygame.MOUSEBUTTONDOWN:
                        self.game_object_die_click_process(pygame.mouse.get_pos())

            self.process_game_step()

            if not self._gameboard.is_running:
                self._gameboard.draw_end_screen()  # End screen megjelenítése
                self.wait_for_quit()

    def run_hand(self):
        self.init_timing()
        while self._gameboard.is_running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self._gameboard.is_running = False

            self.process_game_step(is_hand=True)

            if not self._gameboard.is_running:
                self._gameboard.draw_end_screen()
                self.wait_for_quit()

    def process_game_step(self, is_hand=False):
        if is_hand:
            self.game_object_die_hand_process()

        self.generate_game_objects(
            pygame.time.get_ticks(),
            self._last_spawn_mosquito_time,
            self._last_spawn_bee_time,
            self._last_spawn_stinky_bug_time,
        )

        self._gameboard.check_score_board_timer_up(self._start_ticks)

        # Screen update
        self._gameboard.update_screen()

        if is_hand:
            self._gameboard.hand.update()

        # Sprite Frissítés
        self._gameboard.update_sprites()

        # Sprite Rajzolás
        self._gameboard.draw_sprites()

        if is_hand:
            self._gameboard.draw_hand()

        # Sprite megjelenítés
        self._gameboard.display_sprites()

    def init_timing(self):
        self._start_ticks = pygame.time.get_ticks()
        self._last_spawn_mosquito_time = pygame.time.get_ticks()
        self._last_spawn_bee_time = pygame.time.get_ticks()
        self._last_spawn_stinky_bug_time = pygame.time.get_ticks()

    def generate_game_objects(self, current_time, last_spawn_mosquito_time, last_spawn_bee_time, last_spawn_stinky_bug_time):
        if current_time - last_spawn_mosquito_time > 800:  # 800 ms = 0.8 másodperc
            self._gameboard.add_game_object(Mosquito())  # Új moszkító létrehozása
            self._last_spawn_mosquito_time = current_time

        if current_time - last_spawn_bee_time > 8000:  # 8000 ms = 8 másodperc
            self._gameboard.add_game_object(Bee())  # Új bee létrehozása
            self._last_spawn_bee_time = current_time

        if current_time - last_spawn_stinky_bug_time > 10000:  # 10000 ms = 10 másodperc
            self._gameboard.add_game_object(StinkyBug())  # Új bee létrehozása
            self._last_spawn_stinky_bug_time = current_time

    def wait_for_quit(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._write_json.write_score(self._gameboard.score_board.score)
                    break
            else:
                continue
            break

    def game_object_die_click_process(self, mouse_pos=(-1000, -1000)):
        for game_object in self._gameboard.get_game_objects_sprites():
            if game_object.rect.collidepoint(mouse_pos) and game_object.is_alive:
                game_object.is_alive = False
                game_object.play_sound()
                self._gameboard.remove_game_object(game_object)
                if isinstance(game_object, Mosquito):
                    self._gameboard.score_board.increment_score()
                elif isinstance(game_object, Bee):
                    game_object.background_sound.stop()
                    self._gameboard.score_board.decrement_score()
                    self._gameboard.score_board.decrement_remaining_time()
                elif isinstance(game_object, StinkyBug):
                    self._gameboard.score_board.increment_remaining_time()

    def game_object_die_hand_process(self):
        overlap_threshold = 1000  # Átfedés küszöbértéke, amelyet beállíthatsz
        for game_object in self._gameboard.get_game_objects_sprites():
            if game_object.is_alive and self._gameboard.hand.rect.colliderect(game_object.rect):
                overlap_rect = self._gameboard.hand.rect.clip(game_object.rect)
                overlap_area = overlap_rect.width * overlap_rect.height  # Átfedés területe

                if overlap_area >= overlap_threshold and self._gameboard.hand.is_closed():  # Ellenőrizzük az átfedés területét
                    game_object.is_alive = False
                    game_object.play_sound()
                    self._gameboard.remove_game_object(game_object)
                    if isinstance(game_object, Mosquito):
                        self._gameboard.score_board.increment_score()
                    elif isinstance(game_object, Bee):
                        game_object.background_sound.stop()
                        self._gameboard.score_board.decrement_score()
                        self._gameboard.score_board.decrement_remaining_time()
                    elif isinstance(game_object, StinkyBug):
                        self._gameboard.score_board.increment_remaining_time()
                    game_object = None
