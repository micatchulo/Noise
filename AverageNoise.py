"""
This Average noise wraps along world
"""

import random


def generate_data(x, y):
    """ Generates a 2D array of random data points """
    return [[random.randint(0, 100) for x in range(x)] for y in range(y)]


def numeric_data(data):
    """ Visualise data in numbers"""
    for row in data:
        # Empty line
        line = ''
        for tile in row:
            # Add data to line
            line += f'[{tile:002}]'
        # Print complete row
        print(line)


def smooth_average(data, tweak: int = 8):
    """ Smooth map by calculating average between neighbours """
    # Data size
    cols = len(data)
    rows = len(data[0])

    # Neighbour average
    smoothed_data = []  # List to store the rows
    for y in range(cols):
        smoothed_row = []   # List to store values
        for x in range(rows):
            # Get values in 3x3 grid
            neighbours = [
                data[y - 2][x], data[y - 2][x - 1], data[y - 2][x - 2],
                data[y - 1][x], data[y - 1][x - 1], data[y - 1][x - 2],
                data[y][x], data[y][x - 1], data[y][x - 2],
            ]

            # Calculate the average between neighbours
            average = sum(neighbours) / len(neighbours)
            if average >= 50:
                # Divided value by (tweek / 10) or (tweek * 0.1)
                average /= (tweak * 0.1)

            elif average < 50:
                average *= (tweak * 0.1)

            value = max(0, min(int(average), 100))
            smoothed_row.append(value)
        smoothed_data.append(smoothed_row)

    return smoothed_data

def normalize_data(data):
    """ Normalize values in range 0 to 1 """
    for y in range(len(data)):
        for x in range(len(data[y])):
            data[y][x] = (data[y][x] - 50) * 0.01

    return data

# Batch format
'''
[
data[y-3][x],    data[y-3][x-1],    data[y-3][x-2],    data[y-3][x-3],
data[y-2][x],    data[y-2][x-1],    data[y-2][x-2],    data[y-2][x-3],
data[y-1][x],    data[y-1][x-1],    data[y-1][x-2],    data[y-1][x-3],
data[y][x],      data[y][x-1],      data[y][x-2],      data[y][x-3]
]
'''


def visualize_data(data):
    # Visualize colored ascii data
    for y in data:
        line = ''
        for x in y:
            # Scale based on value ranges
            if x < 0:
                line += f'\033[34m▮\033[0m'  # Water (Blue)
            elif 0 <= x <= 0.3:
                line += f'\033[33m▮\033[0m'  # Grass (Yellow)
            elif x > 0.3:
                line += f'\033[32m▮\033[0m'  # Mountain (Green)
        print(line)


# Initialization
map_data = generate_data(200, 150)

for iteration in range(3):
    map_data = smooth_average(map_data, tweak=1)
    map_data = smooth_average(map_data, tweak=2)
    map_data = smooth_average(map_data, tweak=4)
    map_data = smooth_average(map_data, tweak=8)

normalize_data(map_data)

numeric_data(map_data)

'''
visualize_data(map_data)
'''