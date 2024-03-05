import copy
import logging
import os
from collections import deque
from dataclasses import dataclass
from typing import NewType, Tuple, Union, Literal

# logging.basicConfig(level=logging.DEBUG)

Maze = NewType('Maze', list[list[int]])


@dataclass
class Coordinates:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


def parse_lines(lines: list[str], maze: Maze) -> Tuple[Coordinates, Coordinates, Coordinates, Maze]:
    """
    Goes through lines of input and returns base maze and important coordinates
    :param lines: list of lines of input that represent the maze
    :param maze: unfilled maze
    :return: player position, monster position, exit position, maze with walls
    """
    player_position = Coordinates(0, 0)
    monster_position = Coordinates(0, 0)
    exit_position = Coordinates(0, 0)
    for num_line, line in enumerate(lines):
        for num_char, char in enumerate(line):
            if char in ('.', 'P', 'M'):
                maze[num_line][num_char] = -1
                if char == 'P':
                    player_position = Coordinates(num_line, num_char)
                elif char == 'M':
                    monster_position = Coordinates(num_line, num_char)
            if char == '#':
                maze[num_line][num_char] = -2
            if char == 'E':
                exit_position = Coordinates(num_line, num_char)
    return player_position, monster_position, exit_position, maze


def get_from_file(filename: str = 'input.txt') -> Tuple[Coordinates, Coordinates, Coordinates, Maze]:
    """
    Reads input from file
    :param filename: name of the input file
    :return: player position, monster position, exit position, base maze with walls
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        cords = lines[0].split()
        max_x = int(cords[0])
        max_y = int(cords[1])
        grid = Maze([[0 for _ in range(max_x)] for _ in range(max_y)])
        player_position, monster_position, exit_position, grid = parse_lines(lines[1:], grid)
        for line in grid:
            logging.debug(line)
        logging.debug(f'Player position {player_position}')
        logging.debug(f'Monster position {monster_position}')
        logging.debug(f'Exit position {exit_position}')
        return player_position, monster_position, exit_position, grid


def get_from_input() -> Tuple[Coordinates, Coordinates, Coordinates, Maze]:
    """
    Reads input from console
    :return: player position, monster position, exit position, base maze with walls
    """
    user_input = input()
    split_input = user_input.split()
    x, y = int(split_input[0]), int(split_input[1])
    grid = Maze([[0 for _ in range(x)] for _ in range(y)])
    input_lines = []
    for lines in range(y):
        input_lines.append(input())
    player_position, monster_position, exit_position, grid = parse_lines(input_lines, grid)
    for line in grid:
        logging.debug(line)
    return player_position, monster_position, exit_position, grid


def check_square_to_fill(cords: Coordinates,
                         exit_cords: Coordinates,
                         current_steps: int,
                         grid: Maze) -> bool:
    """
    Checks if the position should be filled with new distance integer
    :param cords: coordinates in the maze
    :param exit_cords: coordinates of the exit in the maze
    :param current_steps: current amount of steps taken from the exit
    :param grid: current maze
    :return: True or False depending if the position should be filled with new distance
    """
    x, y = cords.x, cords.y
    not_wall = grid[x][y] != -2
    not_filled = grid[x][y] == -1
    shorter_distance = grid[x][y] > current_steps
    not_exit = (x, y) != exit_cords
    return not_wall and (not_filled or shorter_distance) and not_exit


def fill_squares(exit_cords: Coordinates, max_cords: Coordinates, grid: Maze) -> Maze:
    """
    Fills individual nodes in the maze with int of the shortest distance to the exit of the maze
    :param exit_cords: coordinates of the exit
    :param max_cords: maximum coordinates of the maze
    :param grid: maze not filled with int of the shortest distance to the exit
    :return: Maze filled with the shortest distance to the exit on each node
    """
    start_x, start_y = exit_cords.x, exit_cords.y
    max_x, max_y = max_cords.x, max_cords.y
    nodes_to_fill = deque()
    steps = 0
    nodes_to_fill.append((start_x, start_y, steps))
    while nodes_to_fill:
        current_x, current_y, current_steps = nodes_to_fill.popleft()
        grid[current_x][current_y] = current_steps

        if current_y > 0:
            if check_square_to_fill(Coordinates(current_x, current_y - 1), exit_cords, current_steps, grid):
                new_steps = current_steps + 1
                nodes_to_fill.append((current_x, current_y - 1, new_steps))

        if current_y < max_y:
            if check_square_to_fill(Coordinates(current_x, current_y + 1), exit_cords, current_steps, grid):
                new_steps = current_steps + 1
                nodes_to_fill.append((current_x, current_y + 1, new_steps))

        if current_x > 0:
            if check_square_to_fill(Coordinates(current_x - 1, current_y), exit_cords, current_steps, grid):
                new_steps = current_steps + 1
                nodes_to_fill.append((current_x - 1, current_y, new_steps))

        if current_x < max_x:
            if check_square_to_fill(Coordinates(current_x + 1, current_y), exit_cords, current_steps, grid):
                new_steps = current_steps + 1
                nodes_to_fill.append((current_x + 1, current_y, new_steps))
    return grid


def fill_distances(grid: Maze, exit_position: Coordinates) -> Maze:
    """
    This function fills the maze with the shortest distances to the exit on each of the nodes in the maze
    :param grid: maze without filled distances
    :param exit_position: coordinates of the exit
    :return: maze filled with the shortest distances
    """
    max_cords = Coordinates(len(grid) - 1, len(grid[0]) - 1)
    grid[exit_position.x][exit_position.y] = 0
    fill_squares(exit_position, max_cords, grid)
    for line in grid:
        logging.debug(line)
    return grid


def check_spot(cords: Coordinates, grid: Maze) -> bool:
    """
    Checks if player or monster can step on the spot
    :param cords: coordinates of the spot to check
    :param grid: maze
    :return: True or False
    """
    max_cords = (len(grid), len(grid[0]))
    if 0 <= cords.x < max_cords[0] and 0 <= cords.y < max_cords[1] and grid[cords.x][cords.y] != -2:
        return True
    else:
        return False


def monster_movement(monster_position: Coordinates, player_position: Coordinates, grid: Maze) -> Coordinates:
    """
    Moves the monster in a deterministic manner
    :param monster_position: current monster position
    :param player_position: current player position
    :param grid: the maze
    :return: new monster position
    """
    monster_position = copy.copy(monster_position)
    vertical_difference = player_position.x - monster_position.x
    horizontal_difference = player_position.y - monster_position.y
    direction = lambda x: 1 if x > 0 else -1
    horizontal_step = direction(horizontal_difference)
    vertical_step = direction(vertical_difference)

    # vertical is on x-axis and horizontal on y-axis due to how input file gets parsed into list of lists
    check_horizontal = check_spot(Coordinates(monster_position.x, monster_position.y + horizontal_step), grid)
    check_vertical = check_spot(Coordinates(monster_position.x + vertical_step, monster_position.y), grid)

    if horizontal_difference != 0 and check_horizontal:
        monster_position.y += horizontal_step

    elif vertical_difference != 0 and check_vertical:
        monster_position.x += vertical_step

    return monster_position


def find_path(player_position: Coordinates,
              monster_position: Coordinates,
              exit_position: Coordinates,
              grid: Maze) -> Union[int, Literal['Impossible']]:
    """
    Finds the shortest possible path to reach the exit in the maze or determines if it's impossible to exit
    :param player_position: starting player position
    :param monster_position: starting monster position
    :param exit_position: position of exit in the maze
    :param grid: maze with filled distances to exit
    :return: The shortest amount of steps to exit or 'Impossible' if you can't escape
    """
    if grid[player_position.x][player_position.y] == -1:
        return 'Impossible'

    to_explore = deque()
    current_steps = 0
    to_explore.append((player_position, monster_position, current_steps))
    checked_cases = set()

    while to_explore:
        player_position, monster_position, current_steps = to_explore.popleft()
        checked_cases.add((player_position, monster_position))
        logging.debug(f'Checked case: {checked_cases}')
        logging.debug(f'Queue: {to_explore}')
        potential_movements = [Coordinates(player_position.x - 1, player_position.y),
                               Coordinates(player_position.x + 1, player_position.y),
                               Coordinates(player_position.x, player_position.y - 1),
                               Coordinates(player_position.x, player_position.y + 1),
                               Coordinates(player_position.x, player_position.y)]  # 4 directions and staying in place

        possible_movements = [check_spot(position, grid) for position in potential_movements]
        available_spots = [spot for index, spot in enumerate(potential_movements) if possible_movements[index]]
        ordered_movements = sorted(available_spots,
                                   key=lambda x: grid[x.x][x.y])  # ordered by which tile is closest to exit

        for spot in ordered_movements:
            new_player_position = spot
            new_monster_position = monster_movement(monster_position, new_player_position, grid)
            logging.debug(f'Player {new_player_position} monster {new_monster_position} exit {exit_position}')

            if new_player_position == exit_position:
                logging.debug('Path found')
                return current_steps + 1

            elif (new_player_position,
                  new_monster_position) not in checked_cases and new_player_position != new_monster_position:
                to_explore.append((new_player_position, new_monster_position, current_steps + 1))

    return 'Impossible'


def main():
    if os.path.isfile('input.txt'):
        player_position, monster_position, exit_position, grid = get_from_file()
    else:
        player_position, monster_position, exit_position, grid = get_from_input()
    grid = fill_distances(grid, exit_position)
    print(find_path(player_position, monster_position, exit_position, grid))


if __name__ == '__main__':
    main()
