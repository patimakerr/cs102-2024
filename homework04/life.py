import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        if not randomize:
            return grid
        for i in range(self.rows):
            for j in range(self.cols):
                grid[i][j] = random.choice((0, 1))
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.rows and 0 <= j < self.cols:
                    cells.append(self.curr_generation[i][j])
        return cells

    def get_next_generation(self) -> Grid:
        next_grid = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                alive_neighbours = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1 and alive_neighbours in (2, 3):
                    next_grid[i][j] = 1
                elif self.curr_generation[i][j] == 0 and alive_neighbours == 3:
                    next_grid[i][j] = 1
        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1


@property
def is_max_generations_exceeded(self) -> bool:
    """
    Не превысило ли текущее число поколений максимально допустимое.
    """
    if self.max_generations:
        return self.generations >= self.max_generations
    return False

    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with filename.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    row = [int(char) for char in line]
                    grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w") as f:
            for row in self.curr_generation:
                f.write("".join(map(str, row)) + "\n")
