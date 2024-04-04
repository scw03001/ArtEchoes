import numpy as np
import cv2
import requests
from pathlib import Path

# Initialize a global list to store points selected by the user
points = []

def imread(path_or_url, flag=cv2.IMREAD_COLOR, rgb=False, normalize=False):
    """
    Read an image from a file or URL. If 'rgb' is True, convert image to RGB.
    If 'normalize' is True, normalize the image pixel values to range 0 to 1.
    """
    # Check if 'path_or_url' is a URL
    if path_or_url.startswith('http'):
        # Download the image from the URL
        response = requests.get(path_or_url)
        # Check if the request was successful
        if response.status_code == 200:
            # Convert the image to a NumPy array and decode to OpenCV format
            img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, flag)
        else:
            # Raise an exception if the image could not be retrieved
            raise Exception(f"Error loading image from URL, status code: {response.status_code}")
    else:
        # Check if the file exists locally
        if not Path(path_or_url).is_file():
            raise FileNotFoundError(f"File not found: {path_or_url}")
        # Read the image from a local file
        img = cv2.imread(str(path_or_url), flag)

    # Convert image to RGB color space if requested
    if rgb:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Normalize image pixel values if requested
    if normalize:
        img = img.astype(np.float64) / 255.0
    return img

def click_event(event, x, y, flags, param):
    """
    Mouse callback function to capture and store points clicked by the user.
    Draws a circle at each clicked point and displays the updated image.
    """
    global points, img_copy
    # Check if the left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the (x, y) coordinates to the 'points' list
        points.append((x, y))
        # Draw a green circle at the clicked position
        cv2.circle(img_copy, (x, y), 5, (0, 255, 0), -1)
        # Show the updated image
        cv2.imshow('image', img_copy)
        # Close the window if four points have been selected
        if len(points) == 4:
            cv2.destroyAllWindows()

def calculate_distance(p1, p2):
    """
    Calculate and return the Euclidean distance between two points 'p1' and 'p2'.
    """
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_target_dimensions(points):
    """
    Determine and return the dimensions of the new image based on the four selected points.
    Calculates the maximum width and height from the distances between the points.
    """
    # Calculate widths and heights between points
    width_a = calculate_distance(points[0], points[1])
    width_b = calculate_distance(points[2], points[3])
    height_a = calculate_distance(points[0], points[2])
    height_b = calculate_distance(points[1], points[3])
    # Determine the maximum width and height for the new image
    max_width = max(int(width_a), int(width_b))
    max_height = max(int(height_a), int(height_b))
    return max_width, max_height

def reorder_points(points):
    """
    Reorder the provided four points into the order required for perspective transformation:
    top-left, top-right, bottom-left, bottom-right based on their coordinates.
    """
    # Sort points based on the sum of their coordinates (x + y)
    points = sorted(points, key=lambda x: x[0] + x[1])
    # Extract top-left point and other points
    top_left, *others = points
    # Determine remaining points based on their coordinates
    bottom_right = max(others, key=lambda x: x[0] + x[1])
    top_right = min(others, key=lambda x: x[1] - x[0])
    bottom_left = max(others, key=lambda x: x[1] - x[0])
    # Return the reordered points
    return [top_left, top_right, bottom_left, bottom_right]

def crop_and_warp(img_path):
    """
    Function to display an image, let the user select four points, and perform a perspective transform.
    """
    global img, points, img_copy
    # Read and display the original image
    img = imread(img_path)
    img_copy = img.copy()
    # Create a window and set a mouse callback function for capturing points
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', click_event)
    cv2.imshow('image', img_copy)
    cv2.waitKey(0)  # Wait until any key is pressed

    # Reorder the points for perspective transformation
    points = reorder_points(points)
    # Convert points to a NumPy array for the transformation
    src_pts = np.array(points, dtype=np.float32)
    # Calculate the dimensions of the target image
    max_width, max_height = find_target_dimensions(points)
    # Define the destination points (corners of the target image)
    dst_pts = np.array([[0, 0], [max_width - 1, 0], [0, max_height - 1], [max_width - 1, max_height - 1]], dtype='float32')
    # Compute the perspective transformation matrix and apply it
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img, M, (max_width, max_height))
    # Display the original and the warped images
    cv2.imshow("Original Image", img)
    cv2.imshow("Cropped and Warped Image", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Save the warped image
    cv2.imwrite('warped_image.jpg', warped)

if __name__ == "__main__":
    # Example usage with a local image file
    image_path = 'mona.png'  
    # image_path = "https://img.etimg.com/thumb/msid-83663367,width-650,height-488,imgsize-866221,resizemode-75/this-copy-is-known-as-the-hekking-mona-lisa-.jpg"  

    crop_and_warp(image_path)
