import unittest
import numpy as np
import sys

sys.path.append('..')
from rl_statevalue.Grid import Grid

class TestGrid(unittest.TestCase):
    def test_grid_initialization(self):
        for dim in range(1,10):
            grid = Grid(dim)
            self.assertEqual(grid.DIMENSION, dim)
            self.assertEqual(grid.coords.shape, (dim, dim))
            self.assertEqual(grid.states.shape, (dim, dim))
            self.assertTrue(np.all(grid.coords == 0))
            self.assertTrue(np.all(grid.states == 0))

    def test_zero_dimension(self):
        grid = Grid(0)
        self.assertEqual(grid.DIMENSION, 0)
        self.assertEqual(grid.coords.shape, (0,0))
        self.assertEqual(grid.states.shape, (0,0))

    def test_negative_dimension(self):
        with self.assertRaises(ValueError):
            Grid(-1)

if __name__ == '__main__':
    unittest.main()
