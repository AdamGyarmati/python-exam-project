import pygame
from board.game_board import GameBoard
from game_objects.mosquito import Mosquito
from game_objects.bee import Bee
from game_objects.stinky_bug import StinkyBug


class Engine:
    def __init__(self, gameboard: GameBoard):
        self.gameboard = gameboard

    def start_game(self):
        game_started = False
        while True:
            if not game_started:
                start_button_rect = self.gameboard.draw_start_screen(pygame.mouse.get_pos())

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if start_button_rect.collidepoint(event.pos):
                            game_started = True  # Játék elindítása

            else:
                self.run()  # Játék főciklus
                break

    def run(self):
        start_ticks = pygame.time.get_ticks()
        last_spawn_mosquito_time = pygame.time.get_ticks()
        last_spawn_bee_time = pygame.time.get_ticks()
        last_spawn_stinky_bug_time = pygame.time.get_ticks()
        while self.gameboard.is_running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.gameboard.is_running = False
                    case pygame.MOUSEBUTTONDOWN:
                        self.game_object_die_process(pygame.mouse.get_pos())

            # Ellenőrizzük, hogy eltelt-e 500 ms ( .5 másodperc) az utolsó moszkító létrehozása óta
            current_time = pygame.time.get_ticks()
            if current_time - last_spawn_mosquito_time > 800:  # 500 ms = 0.5 másodperc
                self.gameboard.add_game_object(Mosquito())  # Új moszkító létrehozása
                last_spawn_mosquito_time = current_time  # Frissítsd az utolsó létrehozás időpontját

            if current_time - last_spawn_bee_time > 8000:  # 8000 ms = 8 másodperc
                self.gameboard.add_game_object(Bee())  # Új bee létrehozása
                last_spawn_bee_time = current_time  # Frissítsd az utolsó létrehozás időpontját

            if current_time - last_spawn_stinky_bug_time > 10000:  # 10000 ms = 10 másodperc
                self.gameboard.add_game_object(StinkyBug())  # Új bee létrehozása
                last_spawn_stinky_bug_time = current_time  # Frissítsd az utolsó létrehozás időpontját

            self.gameboard.check_score_board_timer_up(start_ticks)

            # Screen update
            self.gameboard.update_screen()

            # Sprite Frissítés
            self.gameboard.update_sprites()

            # Sprite Rajzolás
            self.gameboard.draw_sprites()

            # Sprite megjelenítés
            self.gameboard.display_sprites()

            if not self.gameboard.is_running:
                pygame.quit()

    def game_object_die_process(self, mouse_pos):
        for game_object in self.gameboard.get_game_objects_sprites():
            if game_object.rect.collidepoint(mouse_pos) and game_object.is_alive:
                game_object.is_alive = False
                game_object.play_sound()
                self.gameboard.remove_game_object(game_object)
                if isinstance(game_object, Mosquito):
                    self.gameboard.score_board.increment_score()
                elif isinstance(game_object, Bee):
                    game_object.background_sound.stop()
                    self.gameboard.score_board.decrement_score()
                    self.gameboard.score_board.decrement_remaining_time()
                elif isinstance(game_object, StinkyBug):
                    self.gameboard.score_board.increment_remaining_time()
