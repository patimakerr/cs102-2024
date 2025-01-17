import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed

        self.button = pygame.Rect(0, 0, 150, 50)

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        self.status = False

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i, row in enumerate(self.life.curr_generation):
            for j, val in enumerate(row):
                if val == 1:
                    for x in range(i * self.cell_size, (i + 1) * self.cell_size):
                        pygame.draw.line(
                            self.screen, pygame.Color("red"), (j * self.cell_size, x), ((j + 1) * self.cell_size, x)
                        )
                else:
                    for x in range(i * self.cell_size, (i + 1) * self.cell_size + 1):
                        pygame.draw.line(
                            self.screen, pygame.Color("white"), (j * self.cell_size, x), ((j + 1) * self.cell_size, x)
                        )
    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.button.collidepoint(mouse_pos):
                        self.status = not self.status  # смена паузы и продолжения игры

                    if self.status:  # если пауза, можно менять клетки
                        pos_x = mouse_pos[1] // self.cell_size
                        pos_y = mouse_pos[0] // self.cell_size
                        if 0 <= pos_x < self.life.rows and 0 <= pos_y < self.life.cols:
                            self.life.curr_generation[pos_x][pos_y] = 1 - self.life.curr_generation[pos_x][pos_y]

            self.screen.fill(pygame.Color("white"))  # очистка экрана
            self.draw_grid()
            self.draw_lines()

            # кнопка паузы
            button_color = pygame.Color("light steel blue") if self.status else (pygame.Color("lavender"))
            pygame.draw.rect(self.screen, "indigo", self.button_frame, border_radius=15)
            pygame.draw.rect(self.screen, button_color, self.button, border_radius=15)
            button_text = self.font.render("Pause" if not self.status else "Resume", True, pygame.Color("indigo"))
            if not self.status:
                self.screen.blit(button_text, (self.button.x + 20, self.button.y + 15))
            else:
                self.screen.blit(button_text, (self.button.x + 10, self.button.y + 15))

            # сообщения об ошибках
            if self.life.is_max_generations_exceeded:
                pygame.draw.rect(self.screen, "black", self.error_frame, border_radius=0)
                pygame.draw.rect(self.screen, "white", self.error_button, border_radius=0)
                error_msg = self.font.render("Max generations exceeded", True, pygame.Color("red"))
                self.screen.blit(error_msg, (self.width // 3, self.height // 2))
                self.status = True
            if not self.life.is_changing:
                error_msg = self.font.render("No changes", True, pygame.Color("red"))
                self.screen.blit(error_msg, (self.width // 4, self.height // 2 + 30))

            pygame.display.flip()
            clock.tick(self.speed)

            if not self.status:
                self.life.step()  # если не пауза, поле меняется

        pygame.quit()

    game = GameOfLife((30, 70), max_generations=100)
    ui = GUI(game)
    ui.run()GUI(life)
    ui.run()
