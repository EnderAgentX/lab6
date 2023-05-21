import math
import random

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from celluloid import Camera


# figure = [[2, 0], [4, 2], [4, 4], [2, 6], [0, 4], [0, 2]]

def settings():
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.minorticks_on()
    ax.grid(True, which='major')
    ax.grid(True, which='minor')
    plt.grid()
    plt.xlim([-15, 15])
    plt.ylim([-15, 15])
    plt.axis('equal')
    return fig, ax

def randomGeneration(n):
    randArr = []
    for i in range(n):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        randArr.append([x,y])
    print(randArr)
    return randArr


def main():
    fig, ax = settings()
    camera = Camera(fig)
    anim = camera.animate(interval=150)
    variant = 1
    #figure = [[0, 0], [4, 4], [-3, 4], [4, 3], [-4, 3], [-5, 5]]
    #figure = [[4, 5], [8, 0], [5, 10], [7, 5]]
    figure = [[2, 0], [4, 2], [4, 4], [2, 6], [0, 4], [0, 2]]
    num = len(figure)


    variant = input("Ввод из файла - 1, случайные числа - 2: ")
    if variant == "2":
        num = int(input("Введите количество точек: "))
        figure = randomGeneration(num)


    arr_change = [[0.0 for j in range(2)] for i in range(num)]
    arr_start = [[0.0 for j in range(3)] for i in range(num)]
    for i in range(len(figure)):
        for j in range(2):
            arr_start[i][j] = figure[i][j]


    for i in range(num):
        for j in range(i + 1, num):
            for l in range(j + 1, num):
                for k in range(num):
                    if arr_start[k][2] == 1:
                        ax.scatter(arr_start[k][0], arr_start[k][1], c='red')
                    else:
                        ax.scatter(arr_start[k][0], arr_start[k][1], c='green')
                ax.add_patch(Polygon([[arr_start[i][0], arr_start[i][1]], [arr_start[j][0], arr_start[j][1]], [arr_start[l][0], arr_start[l][1]]],linewidth=2, fc='none', ec='black'))
                camera.snap()

                for m in range(num):
                    if m == i or m == j or m == l:
                        continue
                    if is_out(arr_start[i][0], arr_start[i][1], arr_start[j][0], arr_start[j][1],
                              arr_start[l][0], arr_start[l][1], arr_start[m][0], arr_start[m][1]):
                        if not (is_on_line(arr_start[i][0], arr_start[i][1], arr_start[j][0],
                                           arr_start[j][1], arr_start[m][0], arr_start[m][1])
                                or is_on_line(arr_start[j][0], arr_start[j][1], arr_start[l][0],
                                              arr_start[l][1], arr_start[m][0], arr_start[m][1])
                                or is_on_line(arr_start[l][0], arr_start[l][1], arr_start[i][0],
                                              arr_start[i][1], arr_start[m][0], arr_start[m][1])):
                            arr_start[m][2] = 1

    for i in range(num):
        if arr_start[i][2] == 1:
            ax.scatter(arr_start[i][0], arr_start[i][1], c='red')
        else:
            ax.scatter(arr_start[i][0], arr_start[i][1], c='green')
    camera.snap()
    finMatrix = []
    for i in range(num):
        if arr_start[i][2] != 1:
            elem = [arr_start[i][0], arr_start[i][1]]
            finMatrix.append(elem)
    print(finMatrix)
    sortedMatrix = sort_points1(finMatrix)
    print(sortedMatrix)
    for i in range(6):
        for i in range(num):
            if arr_start[i][2] == 1:
                ax.scatter(arr_start[i][0], arr_start[i][1], c='red')
            else:
                ax.scatter(arr_start[i][0], arr_start[i][1], c='green')
        ax.add_patch(Polygon(sortedMatrix, linewidth=2, fc='none', ec='black'))
        camera.snap()

    anim.save("g.gif")
    plt.show()


def sort_points1(points):
    # Находим центр масс многоугольника
    center_x = sum([p[0] for p in points]) / len(points)
    center_y = sum([p[1] for p in points]) / len(points)
    center = (center_x, center_y)

    # Сортируем остальные точки по углу относительно центра масс
    sorted_points = sorted(points, key=lambda point: math.atan2(point[1] - center[1], point[0] - center[0]))

    return sorted_points

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def is_out(x1, y1, x2, y2, x3, y3, x, y):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(x, y, x2, y2, x3, y3)
    A2 = area(x1, y1, x, y, x3, y3)
    A3 = area(x1, y1, x2, y2, x, y)
    return A == A1 + A2 + A3

def is_on_line(x1, y1, x2, y2, x, y):
    return (y - y1) * (x2 - x1) == (y2 - y1) * (x - x1)



if __name__ == "__main__":
    main()

