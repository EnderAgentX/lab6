import math
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from celluloid import Camera


# figure = [[2, 0], [4, 2], [4, 4], [2, 6], [0, 4], [0, 2]]


def NewWindow(arr):
    fig, axes = plt.subplots()
    plt.grid()
    plt.xlim([-20, 20])
    plt.ylim([-20, 20])

    window_x = [arr[0], arr[0], arr[2], arr[2], arr[0]]
    window_y = [arr[1], arr[3], arr[3], arr[1], arr[1]]

    plt.plot(window_x, window_y, c='black')
    #plt.axis('equal')
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
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        randArr.append([x,y])
    print(randArr)
    return randArr


def main():
    fig, ax = settings()
    camera = Camera(fig)
    variant = 1
    #figure = [[0, 0], [4, 4], [-3, 4], [4, 3], [-4, 3], [-5, 5]]
    figure = [[4, 5], [8, 0], [5, 10], [7, 5]]
    num = 4


    variant = input("Ввод из файла - 1, случайные числа - 2: ")
    if variant == "2":
        num = int(input("Введите количество точек: "))
        figure = randomGeneration(num)


    matrixDispStart = [[0.0 for j in range(2)] for i in range(num)]
    matrixStart = [[0.0 for j in range(3)] for i in range(num)]
    for i in range(len(figure)):
        for j in range(2):
            matrixStart[i][j] = figure[i][j]


    for i in range(num):
        for j in range(i + 1, num):
            for l in range(j + 1, num):
                for k in range(num):
                    if matrixStart[k][2] == 1:
                        ax.scatter(matrixStart[k][0], matrixStart[k][1], c='red')
                    else:
                        ax.scatter(matrixStart[k][0], matrixStart[k][1], c='green')
                ax.add_patch(Polygon([[matrixStart[i][0], matrixStart[i][1]], [matrixStart[j][0], matrixStart[j][1]], [matrixStart[l][0], matrixStart[l][1]]],linewidth=2, fc='none', ec='black'))
                camera.snap()

                for m in range(num):
                    if m == i or m == j or m == l:
                        continue
                    if isInside(matrixStart[i][0], matrixStart[i][1], matrixStart[j][0], matrixStart[j][1],
                                matrixStart[l][0], matrixStart[l][1], matrixStart[m][0], matrixStart[m][1]):
                        if not (IsPointOnLine(matrixStart[i][0], matrixStart[i][1], matrixStart[j][0],
                                              matrixStart[j][1], matrixStart[m][0], matrixStart[m][1])
                                or IsPointOnLine(matrixStart[j][0], matrixStart[j][1], matrixStart[l][0],
                                                 matrixStart[l][1], matrixStart[m][0], matrixStart[m][1])
                                or IsPointOnLine(matrixStart[l][0], matrixStart[l][1], matrixStart[i][0],
                                                 matrixStart[i][1], matrixStart[m][0], matrixStart[m][1])):
                            matrixStart[m][2] = 1

    for i in range(num):
        if matrixStart[i][2] == 1:
            ax.scatter(matrixStart[i][0], matrixStart[i][1], c='red')
        else:
            ax.scatter(matrixStart[i][0], matrixStart[i][1], c='green')
    camera.snap()
    finMatrix = []
    for i in range(num):
        if matrixStart[i][2] != 1:
            elem = [matrixStart[i][0], matrixStart[i][1]]
            finMatrix.append(elem)
    print(finMatrix)
    sortedMatrix = sort_points1(finMatrix)
    print(sortedMatrix)
    for i in range(6):
        for i in range(num):
            if matrixStart[i][2] == 1:
                ax.scatter(matrixStart[i][0], matrixStart[i][1], c='red')
            else:
                ax.scatter(matrixStart[i][0], matrixStart[i][1], c='green')
        ax.add_patch(Polygon(sortedMatrix, linewidth=2, fc='none', ec='black'))
        camera.snap()











    anim = camera.animate(interval=500)
    anim.save("g.gif")
    plt.show()

def sort_points(points):
    # Начинаем с первой точки из списка
    start_point = points[0]

    # Находим ближайшую точку к начальной точке
    closest_point = min(points[1:], key=lambda point: (point[0] - start_point[0])**2 + (point[1] - start_point[1])**2)

    # Определяем вектор между начальной и ближайшей точками
    vector = (closest_point[0] - start_point[0], closest_point[1] - start_point[1])

    # Определяем угол между этим вектором и осью X
    angle = math.atan2(vector[1], vector[0])

    # Сортируем остальные точки по углу от начальной точки
    sorted_points = sorted(points[1:], key=lambda point: math.atan2(point[1] - start_point[1], point[0] - start_point[0]) - angle)

    # Возвращаем отсортированные точки
    return [start_point] + sorted_points




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

def isInside(x1, y1, x2, y2, x3, y3, x, y):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(x, y, x2, y2, x3, y3)
    A2 = area(x1, y1, x, y, x3, y3)
    A3 = area(x1, y1, x2, y2, x, y)
    return A == A1 + A2 + A3

def IsPointOnLine(x1, y1, x2, y2, x, y):
    return (y - y1) * (x2 - x1) == (y2 - y1) * (x - x1)



if __name__ == "__main__":
    main()

