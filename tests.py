import unittest

from main import parse_lines, Maze, Coordinates, fill_distances, find_path, get_from_file, check_spot, monster_movement


class GeneralTestCase(unittest.TestCase):
    def test_parse_lines(self):
        grid = Maze([[0 for _ in range(3)] for _ in range(3)])
        lines = ['E..', '.#.', 'P.M']
        player_pos, monster_pos, exit_pos, maze = parse_lines(lines, grid)
        self.assertEqual(player_pos, Coordinates(2, 0))
        self.assertEqual(monster_pos, Coordinates(2, 2))
        self.assertEqual(exit_pos, Coordinates(0, 0))
        self.assertEqual(maze, Maze([[0, -1, -1], [-1, -2, -1], [-1, -1, -1]]))

    def test_fill_distances(self):
        maze = fill_distances(Maze([[0, -1, -1], [-1, -2, -1], [-1, -1, -1]]), Coordinates(0, 0))
        self.assertEqual(maze, Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]]))

    def test_fill_distances_2by2(self):
        maze = fill_distances(Maze([[-1, 0], [-1, -1]]), Coordinates(0, 1))
        self.assertEqual(maze, Maze([[1, 0], [2, 1]]))

    def test_fill_distances_with_wall(self):
        maze = fill_distances(Maze([[-1, 0], [-1, -2]]), Coordinates(0, 1))
        self.assertEqual(maze, Maze([[1, 0], [2, -2]]))

    def test_fill_distances_no_path(self):
        maze = fill_distances(Maze([[-1, -1, -1, -1],
                                    [-1, -1, -1, -1],
                                    [-1, -1, -2, -1],
                                    [-1, -2, 0, -2]]), Coordinates(3, 2))
        self.assertEqual(maze, Maze([[-1, -1, -1, -1],
                                     [-1, -1, -1, -1],
                                     [-1, -1, -2, -1],
                                     [-1, -2, 0, -2]]))

    def test_file_input(self):
        test_file = 'test_input.txt'
        player_position, monster_position, exit_position, grid = get_from_file(test_file)
        self.assertEqual(player_position, Coordinates(1, 0))
        self.assertEqual(monster_position, Coordinates(0, 1))
        self.assertEqual(exit_position, Coordinates(0, 0))
        self.assertEqual(grid, [[0, -1, -1, -1], [-1, -2, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]])

    def test_check_spot_empty_spot(self):
        check = check_spot(Coordinates(1, 0), Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]]))
        self.assertEqual(check, True)

    def test_check_spot_wall(self):
        check = check_spot(Coordinates(1, 1), Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]]))
        self.assertEqual(check, False)

    def test_check_spot_out_of_range(self):
        check = check_spot(Coordinates(4, 1), Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]]))
        self.assertEqual(check, False)

    def test_monster_move_y_plus(self):
        maze = Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]])
        new_pos = monster_movement(Coordinates(0, 1), Coordinates(0, 2), maze)
        self.assertEqual(new_pos, Coordinates(0, 2))

    def test_monster_move_x_plus(self):
        maze = Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]])
        new_pos = monster_movement(Coordinates(0, 2), Coordinates(1, 2), maze)
        self.assertEqual(new_pos, Coordinates(1, 2))

    def test_monster_move_x_minus(self):
        maze = Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]])
        new_pos = monster_movement(Coordinates(2, 2), Coordinates(0, 2), maze)
        self.assertEqual(new_pos, Coordinates(1, 2))

    def test_monster_move_y_minus(self):
        maze = Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]])
        new_pos = monster_movement(Coordinates(0, 2), Coordinates(0, 1), maze)
        self.assertEqual(new_pos, Coordinates(0, 1))

    def test_find_path_possible(self):
        maze = Maze([[0, 1, 2], [1, -2, 3], [2, 3, 4]])
        player_pos = Coordinates(2, 0)
        monster_pos = Coordinates(2, 2)
        exit_pos = Coordinates(0, 0)
        steps = find_path(player_pos, monster_pos, exit_pos, maze)
        self.assertEqual(steps, 2)

    def test_find_path_impossible(self):
        maze = Maze([[0, 1, 2], [1, 2, 3], [2, 3, 4]])
        player_pos = Coordinates(2, 2)
        monster_pos = Coordinates(1, 1)
        exit_pos = Coordinates(0, 0)
        steps = find_path(player_pos, monster_pos, exit_pos, maze)
        self.assertEqual(steps, 'Impossible')


if __name__ == '__main__':
    unittest.main()
