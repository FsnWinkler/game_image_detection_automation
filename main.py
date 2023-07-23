import time
import mss
import mss.tools
import os
from screeninfo import get_monitors
import cv2
import numpy as np
import pyautogui
import pydirectinput
import random
from PIL import Image
import pytesseract
import re

def capture_screen(screen_number=2):
    with mss.mss() as sct:
        monitors = sct.monitors

        # Check if the provided screen_number is valid
        if 0 <= screen_number < len(monitors):
            # Capture the screenshot of the specified screen
            monitor = monitors[screen_number]
            screenshot = sct.grab(monitor)

            # Convert the screenshot to a numpy array
            screenshot_np = np.array(screenshot)

            return screenshot_np
        else:
            print(f"Invalid screen_number. Available screens: {len(monitors)}")
            return None


def locate_and_move(image_path, searchOnSecoundScreen, threshold=0.5):
    # Load the target image and the screenshotd
    target_image = cv2.imread(image_path)
    if searchOnSecoundScreen:
        screenshot = capture_screen()
    else:
        screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Find the position of the target image in the screenshot
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    # Check if the similarity score exceeds the threshold
    if max_val >= threshold:
        # Get the center of the target image
        target_center = (max_loc[0] + target_image.shape[1] // 2, max_loc[1] + target_image.shape[0] // 2)

        # Get the resolution of the primary screen
        primary_screen = get_monitors()[1]
        primary_width, primary_height = primary_screen.width, primary_screen.height

        # Get the resolution of the second screen (assuming it is the rightmost screen)
        second_screen = get_monitors()[2]
        second_width, second_height = second_screen.width, second_screen.height

        # Calculate the absolute position of the target center on the second screen
        if searchOnSecoundScreen:
            target_center_on_second_screen = (
                target_center[0] + primary_width,
                target_center[1]
            )
        else:
            target_center_on_second_screen = (
                target_center[0],
                target_center[1]
            )

        print(f"tuple to moveto = {target_center_on_second_screen}")
        # Move the cursor to the located position on the second screen
        move_with_randomness(*target_center_on_second_screen, max_offset=random.randint(3, 7), duration=random.uniform(0.1, 0.4))
        # pydirectinput.moveTo(*target_center_on_second_screen, duration=random_delay(0.2, 0.5))
        return target_center_on_second_screen
    else:
        return False



def random_delay(start, end):
    # Generate a random delay between 300ms and 600ms (0.3 seconds and 0.6 seconds)
    delay = random.uniform(start, end)

    # Pause the program execution for the random delay
    time.sleep(delay)


def move_with_randomness(x, y, max_offset=None, duration=None):
    # Set default values for max_offset and duration if not provided
    if max_offset is None:
        max_offset = random.randint(3, 7)
    if duration is None:
        duration = 0.2

    # Calculate the target position with added randomness
    target_x = x + random.randint(-max_offset, max_offset)
    target_y = y + random.randint(-max_offset, max_offset)

    # Move the cursor to the target position with a smooth duration
    pyautogui.moveTo(target_x, target_y, duration)

def make_keystrokes(string):
    for char in string:
        pydirectinput.press(char)
        random_delay(0.1, 0.2)

def select_exact_match(isFirstRun):
    locate_and_move("Images/Select_keyword2.png", True)
    if isFirstRun:
        random_delay(1, 1.3)
        pydirectinput.click()
    random_delay(1, 1.3)
    pydirectinput.click()
    random_delay(1, 1.3)
    locate_and_move("Images/Select_exactmatch.png", True)
    random_delay(1, 1.3)
    pydirectinput.click()


def get_int_from_img(image):
    # Set the path to the Tesseract OCR executable (replace this with your Tesseract installation path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Load the image using PIL (Python Imaging Library)


    # Perform OCR on the image and extract the text
    extracted_text = pytesseract.image_to_string(image)

    # Use regular expressions to find all integers in the extracted text
    integers = re.findall(r'\b\d+\b', extracted_text)

    # Join the individual strings and convert the concatenated string to an integer
    combined_integer = int(''.join(integers))

    # Print the combined integer
    return combined_integer


def make_screenshot_and_get_ints():
    with mss.mss() as sct:
        monitors = sct.monitors

        # Check if the provided screen_number is valid
        screen_number = 2  # Change this to the desired screen number
        if 0 <= screen_number < len(monitors):
            # Get the monitor dictionary for the specified screen
            monitor = monitors[screen_number]

            # Define the coordinates of the area you want to capture
            x, y = pyautogui.position()
            # Define the size of the area you want to capture
            width, height = 80, 40

            # Calculate the starting point (left, top) of the area based on the mouse position
            left = x - 1920 - (width / 2) -5
            top = y + 15

            # Adjust the monitor dictionary to capture the specified region
            monitor["left"] += int(left)
            monitor["top"] += int(top)
            monitor["width"] = int(width)
            monitor["height"] = int(height)

            # Capture the screenshot of the specified region
            screenshot = sct.grab(monitor)

            # Convert the mss screenshot to a PIL Image
            image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            # image.save("testleft-5.png")

            integers = get_int_from_img(image)

            # Delete the image data (optional, but recommended if you don't need the screenshot)
            del image

            print(f"Extracted integers from the screenshot: {integers}")
            return integers
        # Save the screenshot to a file
        # filename = "temp_screen_{}.png"
        # counter = 1
        #
        # # Check if the file already exists and increment the counter if needed
        # while os.path.exists(filename.format(counter)):
        #     counter += 1
        #
        # # Save the screenshot to the file with the incremented number
        # filename = filename.format(counter)
        # image.save(filename)
        # price = get_int_from_img(filename)

def move_lowest_to_top(searchOnSecoundScreen):
    random_delay(0.6, 1.3)
    locate_and_move("Images/Select_search.png", searchOnSecoundScreen)
    random_delay(1, 1.3)
    pydirectinput.click()
    random_delay(0.6, 1.3)
    locate_and_move("Images/Select_unit_price.png", searchOnSecoundScreen)
    random_delay(0.6, 1.3)
    pydirectinput.click()
    low_high = make_screenshot_and_get_ints()
    random_delay(0.6, 1.3)
    pydirectinput.click()
    low_high_2nd = make_screenshot_and_get_ints()

    if low_high < low_high_2nd:
        random_delay(0.6, 1.3)
        pydirectinput.click()
        lowest_price = low_high
    else:
        lowest_price = low_high_2nd

    print(lowest_price)
    return lowest_price

def search_item(item, searchOnSecoundScreen):
    random_delay(1, 1.3)
    locate_and_move("Images/Select_searchbar.png", searchOnSecoundScreen)
    random_delay(0.6, 1.3)
    pydirectinput.click()
    random_delay(0.6, 1.3)
    make_keystrokes(item)
    random_delay(0.6, 1.3)


def buy_item(searchOnSecoundScreen):
    random_delay(1, 1.3)
    current_x_y = locate_and_move("Images/Select_price.png", searchOnSecoundScreen)
    random_delay(0.6, 1.3)
    new_value = current_x_y[1] + 30
    updated_tuple = current_x_y[0], new_value
    move_with_randomness(*updated_tuple)
    random_delay(0.6, 1.3)
    pydirectinput.rightClick()
    random_delay(0.6, 1.3)
    locate_and_move("Images/Select_ok.png", searchOnSecoundScreen)
    random_delay(0.6, 1.3)
    pydirectinput.click()

def reset(searchOnSecoundScreen):
    locate_and_move("Images/Select_reset.png", searchOnSecoundScreen)
    random_delay(0.6, 1.3)
    pydirectinput.click()

if __name__ == "__main__":
    isFirstRun = True
    searchOnSecoundScreen = True
    random_delay(3, 4)
    dict_search_items = {
        "superb accessorz flux": 13001
        # "hard balaur horn": 35000,
        # "hard balaur scale": 25000
    }


    for key, value in dict_search_items.items():
        print(key, value)
        select_exact_match(isFirstRun)
        search_item(key, searchOnSecoundScreen)
        while True:
            price = move_lowest_to_top(searchOnSecoundScreen)
            if price < value:
                buy_item(searchOnSecoundScreen)
                print("buyed")
                isFirstRun = False
            else:
                print("price too high")
                isFirstRun = False
                reset(searchOnSecoundScreen)
                break


# random_delay(1, 1.3)
# locate_and_move("Select_searchbar.png", True)
# random_delay(0.6, 1.3)
# pydirectinput.click()
# random_delay(0.6, 1.3)
# make_keystrokes("superb accessorz flux")
# random_delay(0.6, 1.3)






