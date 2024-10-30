import pyautogui
from PIL import ImageGrab
import time

CROP = None # (0, 0, 1920, 1080)
def print_in_square(any):
    for i in range(5):
        for j in range(5):
            print(any[i*5+j], end=" ")
        print()
    print()

def init_position():
    print("请移动鼠标到红区左上角格子中央。然后按回车键。")
    input()
    x1, y1 = pyautogui.position()
    print(f"红区左上角鼠标位置：{x1}, {y1}")

    print("请移动鼠标到红区右下角格子中央。然后按回车键。")
    input()
    x2, y2 = pyautogui.position()
    print(f"红区右下角鼠标位置：{x2}, {y2}")

    POSITION_red = []
    for i in range(5):
        for j in range(5):
            x = x1 + (x2 - x1) * i / 4
            y = y1 + (y2 - y1) * j / 4
            POSITION_red.append((x, y))

    POSITION_purple = []
    for i in range(5):
        for j in range(5):
            x = x1 + (x2 - x1) * (i-0.2) / 4
            y = y1 + (y2 - y1) * (j+6.25) / 4
            POSITION_purple.append((x, y))
    return POSITION_red, POSITION_purple

def init_counts_position():
    print("请移动鼠标到0格子中央。然后按回车键。")
    input()
    x1, y1 = pyautogui.position()
    print(f"红区左上角鼠标位置：{x1}, {y1}")

    print("请移动鼠标到9格子中央。然后按回车键。")
    input()
    x2, y2 = pyautogui.position()
    print(f"红区右下角鼠标位置：{x2}, {y2}")

    POSITION_numbers = [None]*10
    POSITION_numbers[0] = (x1, y1)
    for i in range(5):
        x = x1 + (x2 - x1) * (i-0.5) / 3
        y = (y1 + y2) / 2
        POSITION_numbers[i+1] = (x, y)

    for i in range(4):
        x = x1 + (x2 - x1) * i / 3
        y = y2
        POSITION_numbers[6+i] = (x, y2)

    for i in range(10):
        print(f"{i}: {POSITION_numbers[i]}")
    return POSITION_numbers

POSITION_numbers = init_counts_position()
POSITION_red,POSITION_purple =  init_position() 

def get_pixel_color(position):
    screenshot = ImageGrab.grab()
    color = screenshot.getpixel(position)
    return color
def get_all_pixel_color(positions):
    screenshot = ImageGrab.grab().crop(CROP)
    screenshot.save("./screenshot/"+time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())+".png")
    colors = [False] * 25
    for i in range(25):
        colors[i] =  screenshot.getpixel(positions[i])
    return colors

def check_pixel_color(colors):
    check_red = [False] * 25
    for i in range(25):
        check_red[i] =  colors[i][1] < 100
    return check_red

def count_colors(check_red,check_purple):
    count = 0
    for i in range(25):
        if (check_red[i] or check_purple[i]):
            count += 1
    return count

def get_counts():
    colors_red = get_all_pixel_color(POSITION_red)
    colors_purple = get_all_pixel_color(POSITION_purple)
    check_red = check_pixel_color(colors_red)
    check_purple = check_pixel_color(colors_purple)
    print_in_square(colors_red)
    print_in_square(colors_purple)
    print_in_square(check_red)
    print_in_square(check_purple)
    counts = count_colors(check_red, check_purple)
    return counts
def click(counts):
    pyautogui.click(POSITION_red[0])
    if counts > 9:
        pyautogui.click(POSITION_numbers[counts//10])
        time.sleep(1)
        pyautogui.click(POSITION_numbers[counts%10])
    else:
        pyautogui.click(POSITION_numbers[counts])


if __name__ == "__main__":
    run = 0
    start_time = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    wiat_time = 10
    while True:
        while (get_pixel_color(POSITION_red[0])[0]<100):
            time.sleep(0.5)
            print(".", end=" ")

        print("waiting(3s)")
        time.sleep(3)
        counts = get_counts()
        print("counts = ", counts)
        click(counts)

        run += 1
        print(f"start time: {start_time}")
        print(f"run : {run}")

        while (get_pixel_color(POSITION_red[0])[0]>100):
            time.sleep(0.5)
            print(".", end=" ")
