# Import required libraries
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from functions import skipFrame

# Count Frames
frameCount = 0

# Window Name.
winName = "Deforestation Analysis"
cv.namedWindow(winName)

# Path of the video file.
path = "/Users/gauravsingh/Desktop/AI ENGINEER/Deforestation Analysis/input.mp4"

# Video Capture Object.
cap = cv.VideoCapture(path)
if not cap.isOpened():
    print("error while accessing the video...")

# Shape of  the cap object.
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv.CAP_PROP_FPS)

# Black canvas of the cap.
canvas_blk = np.zeros([height, width], "uint8")

# Area of the frame.
total_area = int(width) * int(height)

# Area for inRange function.
lw_fr = (20, 50, 100)
up_fr = (60, 100, 255)

lw_wt = (90, 180, 70)
up_wt = (130, 230, 130)

# Create Video Writer object for different videos.
output_1 = cv.VideoWriter("output_1.mp4", cv.VideoWriter_fourcc(*'MP4V'), fps, (width, height))
output_2 = cv.VideoWriter("output_2.mp4", cv.VideoWriter_fourcc(*'MP4V'), fps, (width, height))

# Main loop
while True:

    # Frame Count.
    frameCount += 1

    # Read the frame one by one.
    has_frame, frame = cap.read()
    if not has_frame:
        print("No frame to read.")
        break

    frameStatus = skipFrame(frameCount, frameStatus = True)

    # Convert the frame to HSV color space.
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)


    if frameStatus == True:
        
        mask_df = cv.inRange(frame_hsv, lw_fr, up_fr)
        mask_wt = cv.inRange(frame_hsv, lw_wt, up_wt)

        # Calculate white pixels.
        nonZero_pixel = cv.countNonZero(mask_df)
        nonZero_pixel_wt = cv.countNonZero(mask_wt)

        # Deforested area in percentage.
        wt_area = int((nonZero_pixel_wt / total_area) * 100)
        df_area = int((nonZero_pixel / (total_area - wt_area) * 100))

        # Find all the contours and draw them on the original frame.
        contours, hierarchy = cv.findContours(mask_df, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        # Draw Contour on every fifth frame
        if frameCount % 5 == 0:
            cv.drawContours(frame, contours, -1, (0, 0, 255), -1)
        else:
            cv.drawContours(frame, contours, -1, (125, 100, 200), 1)

        # Draw a banner to show deforestation level, and water Level.
        cv.rectangle(frame, (160, 20), (450, 60), (169, 169, 169), thickness = -1)

        # Draw a banner for water level if there is any water present in the frame.
        if  wt_area >= 2:
            cv.rectangle(frame, (160, 60), (450, 100), (169, 169, 169), thickness = -1)
            cv.putText(frame, f"Water Level: {wt_area}%", (160, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)
            

        # Add Deforestation percentage on top of the banner.
        cv.putText(frame, f"Deforestation: {df_area}%", (160, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv.LINE_AA)

    # Testing
    if frameStatus == True:
        mask_df = cv.merge([mask_df, mask_df, mask_df])
        canvas_blk = mask_df 

    # Display frame.
    cv.imshow(winName, canvas_blk)

    # Key value to slow down video while showing the deforestation aprt.
    keyValue = 1
    if frameStatus == True:
        keyValue = 1
    key = cv.waitKey(keyValue)

    # Store the output locally
    output_1.write(frame)
    output_2.write(canvas_blk)

    # Break the loop if 'q', 'Q' or esc key is pressed.
    if key == ord('q') or key == ord('Q') or key == 27:
        print("Video ended by user...")
        break


cap.release()
cv.destroyAllWindows()
