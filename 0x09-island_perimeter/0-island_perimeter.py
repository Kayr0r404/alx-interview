#!/usr/bin/python3


def island_perimeter(grid):
    """find the parameter of an island"""
    grid_height = len(grid)
    grid_width = len(grid[0])
    param = 0

    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:
                # check top cell
                if row == 0 or grid[row - 1][col] == 0:
                    param += 1
                # bottom
                if row == grid_height - 1 or grid[row + 1][col] == 0:
                    param += 1
                # right
                if col == grid_width - 1 or grid[row][col + 1] == 0:
                    param += 1
                # left
                if col == 0 or grid[row][col - 1] == 0:
                    param += 1

    return param
