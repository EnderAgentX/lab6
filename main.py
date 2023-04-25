import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from celluloid import Camera

figure = [[2, 0], [4, 2], [4, 4], [2, 6], [0, 4], [0, 2]]

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

def main():
    fig, ax = settings()
    camera = Camera(fig)

    num = 6
    coordinates = []
    matrixStart = [[0.0 for j in range(2)] for i in range(num)]

    for i in range(num):
        for j in range(i + 1, num):
            for l in range(j + 1, num):
                for k in range(num):
                    ax.scatter(figure[k][0], figure[k][1], c='green')
                ax.add_patch(Polygon([[figure[i][0], figure[i][1]], [figure[j][0], figure[j][1]], [figure[l][0], figure[l][1]]],linewidth=2, fc='none', ec='black'))
                camera.snap()

                for m in range(num):
                    if m == i or m == j or m == l:
                        continue

    anim = camera.animate(interval=150)
    anim.save("g.gif")
    plt.show()

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def isInside(x1, y1, x2, y2, x3, y3, x, y):
    A = area(x1, y1, x2, y2, x3, y3)
    A1 = area(x, y, x2, y2, x3, y3)
    A2 = area(x1, y1, x, y, x3, y3)
    A3 = area(x1, y1, x2, y2, x, y)
    return A == A1 + A2 + A3



if __name__ == "__main__":
    main()

