# title: "Shocked Bee Detector for Electric Shock Avoidance Assay"
# date: "07/30/2023"
# author: "Babur Erdem"
# update date: "08/06/2024"


# Import necessary libraries
import cv2
import numpy as np
from shapely.geometry import Point, Polygon
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import sys

# Define variables for the experiment video and shock timings
video_name = "SampleVideo.mp4"  # Write the name of the experiment video
begin_min = 0   # Shock was applied at that time in experiment video (minute)
begin_sec = 20  # Shock was applied at that time in experiment video (second)

exp_duration_min = 5  # Duration of the shock (minute)
exp_duration_sec = 1  # Duration of the shock (second)




# Following parts are used for analysis; do not write anything below.
# Cut the video in the shock interval
# This code uses moviepy to extract a subclip of the original video containing the shock interval.
cutvideo_name = str((video_name.replace(".mp4", "")) + "_Cut.mp4")
ffmpeg_extract_subclip(
    video_name,
    (begin_min * 60 + begin_sec),
    ((begin_min * 60 + begin_sec) + (exp_duration_min * 60 + exp_duration_sec)),
    targetname=cutvideo_name,)


# Measure the size of a bee and estimate max and min of bee area.
print("\n--- \nMeasure the length of a bee with left click \nIf you accept the measurement press (a) \nClick right to measure again \nPress (q) to quit\n")

# Open the cut video and capture the first frame
video = cv2.VideoCapture(cutvideo_name)
ret, frame = video.read()

line_coordinates = []
new_measurement_line = frame.copy()

cv2.namedWindow("Measure a bee", cv2.WINDOW_NORMAL)
cv2.imshow("Measure a bee", frame)

# Mouse callback function to measure a bee on the frame
def draw_line(event, x, y, flags, param):
    global frame, line_coordinates, new_measurement_line
    if event == cv2.EVENT_LBUTTONDOWN:
        line_coordinates.append((x, y))
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
        if len(line_coordinates) == 2:
            cv2.polylines(frame, [np.array(line_coordinates)], True, (0, 0, 255), 2)
                   
    elif event == cv2.EVENT_RBUTTONDOWN:                     
        line_coordinates = []  
        frame = new_measurement_line 
            
    cv2.imshow("Measure a bee", frame)

cv2.setMouseCallback("Measure a bee", draw_line)

# Wait for the user to press 'a' to continue or 'q' to exit
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("a"):
        break
    elif key == ord("q"):
        video.release()
        cv2.destroyAllWindows()
        sys.exit()

measure_x = list(zip(*line_coordinates))[0]
measure_y = list(zip(*line_coordinates))[1]

bee_lenght = (abs(measure_x[0]-measure_x[1])**2 + abs(measure_y[0]-measure_y[1])**2)**(1/2)

# We determined the width/length ratio of a bee is around 1/3. You can change the ratio according to your organism.
bee_width = bee_lenght / 3   

# We assigned the extremum areas that a bee can cover. You can change them according to your organism.
min_bee_size = 0.5 * bee_lenght * bee_width 
max_bee_size = 4 * bee_lenght * bee_width 

video.release()
cv2.destroyAllWindows()


# Drawing the shock boxes. Bees take the IDs according to the drawing order of the boxes.
# The coordinates of these boxes are stored for later tracking.
print("\n--- \nDraw shuttle box areas with left click \nIf you have completed drawing the boxes, press (a) \nClick right to redraw the last box \nPress (q) to quit\n")

# Open the cut video and capture the first frame
video = cv2.VideoCapture(cutvideo_name)
ret, frame = video.read()

box_coordinates = []
boxes = []
box_counter = 1  
catches = []

cv2.namedWindow("Draw shuttle boxes", cv2.WINDOW_NORMAL)
cv2.imshow("Draw shuttle boxes", frame)

# Mouse callback function to draw boxes on the frame and give numbers
def draw_box(event, x, y, flags, param):
    global frame, box_coordinates, box_counter, catches
    if event == cv2.EVENT_LBUTTONDOWN:
        box_coordinates.append((x, y))
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
        if len(box_coordinates) == 4:
            # Draw boxes
            cv2.polylines(frame, [np.array(box_coordinates)], True, (0, 255, 0), 2)

            # Calculate the center of the box
            center_x = int(sum(point[0] for point in box_coordinates) / 4)
            center_y = int(sum(point[1] for point in box_coordinates) / 4)

            # Display the box number at the center of the box
            cv2.putText(frame, str(box_counter), (center_x, center_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            boxes.append(box_coordinates)
            box_coordinates = []
            box_counter += 1
            
            catches.append(frame.copy())
            
    elif event == cv2.EVENT_RBUTTONDOWN:                     
        del boxes[-1]  
        del catches[-1]
        frame = catches[-1] 
        box_counter -= 1
            
    cv2.imshow("Draw shuttle boxes", frame)
        
cv2.setMouseCallback("Draw shuttle boxes", draw_box)

# Wait for the user to press 'a' to continue or 'q' to exit
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("a"):
        break
    elif key == ord("q"):
        video.release()
        cv2.destroyAllWindows()
        sys.exit()

cv2.imwrite(str((video_name.replace(".mp4", "")) + "_BeeNo.jpg"), frame)

video.release()
cv2.destroyAllWindows()

# Drawing the shock area.
# This part of the code allows the user to draw the shock area on the frame.
print("\n--- \nDraw shock area with left click \nIf you have completed drawing the shock area, press (a) \nClick right to redraw the shock area \nPress (q) to quit\n")

# Open the cut video and capture the first frame
video = cv2.VideoCapture(cutvideo_name)
ret, frame = video.read()

area_coordinates = []
new_shock_area = frame.copy()

cv2.namedWindow("Draw shock area", cv2.WINDOW_NORMAL)
cv2.imshow("Draw shock area", frame)

# Mouse callback function to draw the shock area on the frame
def draw_area(event, x, y, flags, param):
    global frame, area_coordinates, new_shock_area
    if event == cv2.EVENT_LBUTTONDOWN:
        area_coordinates.append((x, y))
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
        if len(area_coordinates) == 4:
            cv2.polylines(frame, [np.array(area_coordinates)], True, (0, 255, 0), 2)
     
    elif event == cv2.EVENT_RBUTTONDOWN:                     
        area_coordinates = []  
        frame = new_shock_area 
         
    cv2.imshow("Draw shock area", frame)

cv2.setMouseCallback("Draw shock area", draw_area)

# Wait for the user to press 'a' to continue or 'q' to exit
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("a"):
        break
    elif key == ord("q"):
        video.release()
        cv2.destroyAllWindows()
        sys.exit()

video.release()
cv2.destroyAllWindows()

# TRACKING BEGIN
# This part of the code initiates the tracking process.
# It creates a video capture object for the cut video and sets up the parameters.
video = cv2.VideoCapture(cutvideo_name)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Create a background subtractor to detect motion
background_subtractor = cv2.createBackgroundSubtractorMOG2()

previous_frame = None
bees_coord = [[(-1, -1)] * len(boxes)]
bc = 1

# TRACKING LOOP
# This part of the code processes each frame of the video and tracks the bees within the defined boxes.
while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fg_mask = background_subtractor.apply(gray)
    fg_mask = cv2.resize(fg_mask, (width, height))
    _, motion_mask = cv2.threshold(fg_mask, 30, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    motion_mask = cv2.dilate(motion_mask, kernel, iterations=2)

    contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    points = []

    # Draw bounding boxes around motion areas and store the center coordinates
    for contour in contours:
        if cv2.contourArea(contour) > min_bee_size and cv2.contourArea(contour) < max_bee_size:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center_x = x + w // 2
            center_y = y + h // 2
            coord = (center_x, center_y)
            points.append(coord)

    # Select the center coordinates found in the boxes
    in_points = []
    n = 0
    while n < len(boxes):
        m = 0
        pol1 = boxes[n]
        polyg = Polygon(pol1)
        inner_points = []
        while m < len(points):
            p1 = points[m]
            pointy = Point(p1)
            if polyg.contains(pointy) == True:
                inner_points.append(p1)
            m = m + 1

        # Take the previous center coordinate if no or more than one center coordinate were found in the shock box area
        if len(inner_points) > 1:
            inner_points = [bees_coord[(bc - 1)][n]]
        elif len(inner_points) == 0:
            inner_points = [bees_coord[(bc - 1)][n]]
        in_points.append(inner_points)
        n = n + 1
    in_dots = []
    in_dots = sum(in_points, [])

    bees_coord.append(in_dots)

    # If no center coordinate is found at the beginning of the tracking, use the next available center coordinate.
    nopointlist = np.where((np.array(bees_coord[0])) == (-1, -1))[0]
    for k in nopointlist:
        if bees_coord[bc][k] != (-1, -1):
            for poi in range(0, bc):
                bees_coord[poi][k] = bees_coord[(bc - 1)][k]

    bc = bc + 1

    # Create a combined output frame by horizontally concatenating the original frame and the motion mask
    output_frame = cv2.hconcat([frame, cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR)])
    cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
    cv2.imshow("Video", output_frame)
    previous_frame = gray
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

# Analyze whether bees are shocked or not
# This part of the code checks if each bee's tracked position falls within the shock area or not.
# If the bee is in the shock area, it is defined as TRUE.
shocked_bees = []
for bee in bees_coord:
    shocked_bee = []
    for shock_bee in bee:
        shocked_bee.append((Point(shock_bee)).within(Polygon(area_coordinates)))
    shocked_bees.append(shocked_bee)

# Create a shock indicator file to save the results of the shock analysis.
title_row = []
n = 1
while n <= len(shocked_bee):
    Xn = str("Bee" + str(n))
    title_row.append(Xn)
    n = n + 1
shock_file_name = str((video_name.replace(".mp4", "")) + "_Shock.txt")
with open(shock_file_name, "w") as shock_file:
    shock_file.write("\t".join(title_row) + "\n")
    for sbees in shocked_bees:
        scBees = sbees * 1
        shbees = [str(x) for x in scBees]
        shock_file.write("\t".join(shbees) + "\n")

# Create a track video showing the tracked positions of the bees
cap = cv2.VideoCapture(cutvideo_name)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(str((video_name.replace(".mp4", "")) + "_DotVideo.mp4"), fourcc, fps, (width, height))

for frame_index in range(len(bees_coord)):
    ret, dotframe = cap.read()
    if not ret:
        break

    coords = bees_coord[frame_index]
    for coord in coords:
        x, y = coord
        cv2.circle(dotframe, (x, y), 4, (0, 0, 255), -1)

    out.write(dotframe)

cap.release()
out.release()
cv2.destroyAllWindows()
