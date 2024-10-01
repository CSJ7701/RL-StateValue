import unittest
import numpy as np
from rl_statevalue import Agent, Grid

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.grid_size = 3
        self.mock_grid = Grid.Grid(self.grid_size)
        self.agent = Agent.Agent(self.mock_grid)

    def test_initial_position(self):
        self.assertEqual(self.agent.position, [0, 0])
        self.assertEqual(self.mock_grid.coords[0, 0], 1)

    def test_move_north(self):
        self.agent.move(Agent.Direction.N)
        self.assertEqual(self.agent.position, [0, 0])  # Should remain in the same position due to boundary
        self.assertEqual(self.mock_grid.coords[0, 0], 1)

    def test_move_south(self):
        self.agent.move(Agent.Direction.S)
        self.assertEqual(self.agent.position, [1, 0])
        self.assertEqual(self.mock_grid.coords[1, 0], 1)
        self.assertEqual(self.mock_grid.coords[0, 0], 0)

    def test_move_east(self):
        self.agent.move(Agent.Direction.E)
        self.assertEqual(self.agent.position, [0, 1])
        self.assertEqual(self.mock_grid.coords[0, 1], 1)
        self.assertEqual(self.mock_grid.coords[0, 0], 0)

    def test_move_west(self):
        self.agent.move(Agent.Direction.E)  # Move East first to change position
        self.agent.move(Agent.Direction.W)
        self.assertEqual(self.agent.position, [0, 0])
        self.assertEqual(self.mock_grid.coords[0, 0], 1)
        self.assertEqual(self.mock_grid.coords[0, 1], 0)

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            self.agent.move("X")

    def test_move_out_of_bounds(self):
        # Attempt to move north out of bounds
        self.agent.move(Agent.Direction.N)  # Should not move out of bounds
        self.agent.move(Agent.Direction.N)  # Again, should stay at [0, 0]
        self.assertEqual(self.agent.position, [0, 0])
        self.assertEqual(self.mock_grid.coords[0, 0], 1)

if __name__ == "__main__":
    unittest.main()



