import time
import mss
import os
import cv2
import numpy as np
import pyautogui
import pydirectinput
import random
from PIL import Image, ImageGrab
import pytesseract
import re



def capture_screen():
    screenshot = ImageGrab.grab()

    # Convert the screenshot to a numpy array
    screenshot_np = np.array(screenshot)

    # Debug print statements
    # print(f"Screenshot shape: {screenshot_np.shape}")
    # print(f"Screenshot data type: {screenshot_np.dtype}")

    return screenshot_np


def locate_and_move(image_path, threshold=0.4):
    # Load the target image as a color image (RGB)
    target_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Capture the screenshot
    screenshot = capture_screen()

    # Debug print statementssup
    # print(f"Target image shape: {target_image.shape}")
    # print(f"Target image data type: {target_image.dtype}")

    # Find the position of the target image in the screenshot
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    print(max_val)
    # Check if the similarity score exceeds the threshold
    if max_val >= threshold:
        # Get the center of the target image
        target_center = (max_loc[0] + target_image.shape[1] // 2, max_loc[1] + target_image.shape[0] // 2)

        print(f"tuple to moveto = {target_center}")
        # Move the cursor to the located position
        move_with_randomness(*target_center, max_offset=random.randint(3, 7), duration=random.uniform(0.1, 0.4))
        return target_center
    else:
        return False




def random_delay(start, end):
    # Generate a random delay between the specified range
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
    locate_and_move(f"{IMG_PATH}/Select_keyword.png")
    if isFirstRun:
        random_delay(1, 1.3)
        pydirectinput.click()
    random_delay(1, 1.3)
    pydirectinput.click()
    random_delay(1, 1.3)
    locate_and_move(f"{IMG_PATH}/Select_exactmatch.png")
    random_delay(1, 1.3)
    pydirectinput.click()


def get_int_from_img(image):
    # Set the path to the Tesseract OCR executable (replace this with your Tesseract installation path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
        screenshot = sct.shot(output="fullscreen")

    # Convert the mss screenshot to a PIL Image
    image = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

    integers = get_int_from_img(image)

    # Delete the image data (optional, but recommended if you don't need the screenshot)
    del image

    print(f"Extracted integers from the screenshot: {integers}")
    return integers


def move_lowest_to_top():
    random_delay(0.6, 1.3)
    locate_and_move(f"{IMG_PATH}/Select_search.png")
    random_delay(1, 1.3)
    pydirectinput.click()
    random_delay(0.6, 1.3)
    locate_and_move(f"{IMG_PATH}/Select_unit_price.png")
    random_delay(0.6, 1.3)
    pydirectinput.click()
    low_high = make_screenshot_and_get_ints()
    random_delay(0.6, 1.3)
    pydirectinput.click()
    low_high_2nd = make_screenshot_and_get_ints()

    lowest_price = min(low_high, low_high_2nd)
    print(lowest_price)
    return lowest_price


def search_item(item):
    random_delay(1, 1.3)
    locate_and_move(f"{IMG_PATH}/Select_searchbar.png")
    random_delay(0.6, 1.3)
    pydirectinput.click()
    random_delay(0.6, 1.3)
    make_keystrokes(item)
    random_delay(0.6, 1.3)


def buy_item():
    random_delay(1, 1.3)
    current_x_y = locate_and_move(f"{IMG_PATH}/Select_price.png")
    random_delay(0.6, 1.3)
    new_value = current_x_y[1] + 30
    updated_tuple = current_x_y[0], new_value
    move_with_randomness(*updated_tuple)
    random_delay(0.6, 1.3)
    pydirectinput.rightClick()
    random_delay(0.6, 1.3)
    locate_and_move(f"{IMG_PATH}/Select_ok.png")
    random_delay(0.6, 1.3)
    pydirectinput.click()


def reset():
    locate_and_move(f"{IMG_PATH}/Select_reset.png")
    random_delay(0.6, 1.3)
    pydirectinput.click()


if __name__ == "__main__":
    isFirstRun = False
    IMG_PATH = "Laptop_Images"

    random_delay(3, 4)
    dict_search_items = {
        "superb accessorz flux": 13001
        # "hard balaur horn": 35000,
        # "hard balaur scale": 25000
    }

    for key, value in dict_search_items.items():
        print(key, value)
        select_exact_match(isFirstRun)
        search_item(key)
        while True:
            price = move_lowest_to_top()
            if price < value:
                buy_item()
                print("bought")
                isFirstRun = False
            else:
                print("price too high")
                isFirstRun = False
                reset()
                break
