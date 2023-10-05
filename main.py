import cv2
import numpy as np
import pyautogui
import time


# Function to perform the image detection and single click
def detect_and_single_click(target_image_path, alt_image_path, roi_coords):
    try:
        print("Loading screenshot...")
        screenshot = pyautogui.screenshot(region=roi_coords)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        print("Loading target image...")
        target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
    except Exception as e:
        print(f"Error loading images: {e}")
        return

    # Match the template (target_image) within the screenshot
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)

    # Define a threshold for matching (adjust as needed)
    threshold = 0.9

    # Find locations where the template matches the screenshot
    locations = np.where(result >= threshold)

    if len(locations[0]) > 0:
        print(f"Found {len(locations[0])} matching locations.")

        # Single click on all detected locations with a delay
        for pt in zip(*locations[::-1]):
            x, y = pt[0] + roi_coords[0], pt[1] + roi_coords[1]
            pyautogui.click(x, y)
            time.sleep(1)  # Add a delay between clicks

        print("Clicked on matching locations.")
    else:
        print("Original image not found, searching for alternative image...")

        try:
            print("Loading alternative image...")
            alt_screenshot = pyautogui.screenshot(region=roi_coords)
            alt_screenshot = np.array(alt_screenshot)
            alt_screenshot = cv2.cvtColor(alt_screenshot, cv2.COLOR_BGR2GRAY)

            alt_image = cv2.imread(alt_image_path, cv2.IMREAD_GRAYSCALE)
        except Exception as e:
            print(f"Error loading alternative images: {e}")
            return

        alt_result = cv2.matchTemplate(alt_screenshot, alt_image, cv2.TM_CCOEFF_NORMED)
        alt_locations = np.where(alt_result >= threshold)

        if len(alt_locations[0]) > 0:
            print(f"Found {len(alt_locations[0])} matching locations for alternative image.")
            # Single click on all detected locations with a delay
            for pt in zip(*alt_locations[::-1]):
                x, y = pt[0] + roi_coords[0], pt[1] + roi_coords[1]
                pyautogui.click(x, y)
                time.sleep(1)  # Add a delay between clicks
            print("Clicked on matching locations for alternative image.")
        else:
            print("No matching locations found for alternative image.")


# Path to the original target image and alternative image
target_image_path = 'C:\\Users\\idang\\PycharmProjects\\pythonProject2\\screenshots\\START.png'
alt_image_path = 'C:\\Users\\idang\\PycharmProjects\\pythonProject2\\screenshots\\UNLOCK.png'

# Define the coordinates of the region of interest (x, y, width, height)
roi_coords = (7, 4, 1593, 709)  # Example coordinates, adjust as needed

while True:
    # Detect and single click on the original or alternative image within the ROI
    detect_and_single_click(target_image_path, alt_image_path, roi_coords)

    # Wait for 10 minutes before repeating the process
    time.sleep(1800)
