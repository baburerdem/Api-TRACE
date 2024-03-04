A computer vision algorithm to analyze videos of electric shock avoidance assay on honey bees and a data processing code to visualize the results.

First, run the Python code (Shocked Bee Detector for Electric Shock Avoidance Assay) to create shock event data and a tracking video from the experiment video, then run the R code (Learning Curve Plotter from Bee Tracker Output) to visualize the shock event data and create an Excel file for further statistical analysis.

---
Title: Shocked Bee Detector for Electric Shock Avoidance Assay 
- Date: 07/30/2023
- Author: Babur Erdem
- Update Date: 02/22/2024

Description:
This Python script is designed to detect and analyze the response of bees to a shock stimulus from the experiment video. 
The code performs several tasks, including:
	- Extracting a subclip from the experiment video is spanned from the experiment beginning time to a defined experiment duration. 
	- Measuring the size of a bee, defining ROIs by drawing shuttle box areas and the shock area.
	- Tracking the movement of bees within defined boxes.
	- Analyzing whether bees are shocked or not based on their tracked positions.
	- Generating output files, including shock event data file and track video.

Instructions:
1. Ensure that the necessary Python libraries are installed:
	- OpenCV (cv2)
	- NumPy (np)
	- Shapely
	- MoviePy
   
2. Update the following variables with appropriate values:
	- `video_name` : Name of the experiment video.
	- `begin_min` and `begin_sec`: Time when the shock was applied in the experiment video.
	- `exp_duration_min` and `exp_duration_sec`: Duration of the shock.

3. Run the script in a Python environment.

4. Follow the instructions prompted in the console window to measure a bee, draw box areas, and define the shock area on the video frames.

Files: 
- {ExperimentVideoName}.mp4 : Experiment video, which is the input for the code.
- {ExperimentVideoName}_Shock.txt : Output .txt file includes shock event data, the input of Learning Curve Plotter (R code).
- {ExperimentVideoName}_DotVideo.mp4 : Output .mp4 video is showing the tracked positions of the bees.

Notes: 
- Ensure the experiment video is accessible and properly named.
- The script utilizes various image processing techniques and interactive functionalities to facilitate analysis and tracking of bee movements.

For further inquiries or assistance, please contact Babur Erdem (author of the script) at ebabur@metu.edu.tr.

---
Title: Learning Curve Plotter from Bee Tracker Output 
- Author: Babur Erdem
- Date: 2023-07-26
- Update Date: 2024-02-27

Description:
This R script is designed to analyze shock event data and visualization. 
The code performs several tasks, including:
	- Data preprocessing, converting shock event data, came from Shocked Bee Detector (Python code), to binary data.
	- Creating a structured data frame.
	- Generating an Excel file for further statistical analysis.
	- Drawing two plots: individuals' and group learning curves.

Instructions:
1. Prepare a metadata file in .txt format. The first column should be `BeeNo`. Then, enter the attributes of the experiment and bees, such as `Treatment`, `Dose`, `Unit`, `Replicate`, `Phase`, `Subspecies`. Named the file as {ExperimentVideoName}_Metadata.txt

2. Ensure that the necessary R libraries are installed:
	- readxl
	- ggplot2
	- dplyr
	- ggpubr
	- writexl

3. Update the following variables with appropriate values:
	- `VideoName` : Name of the experiment video.
	- `fps` : fps of the experiment video.
	- `SamplingRate` : Downsample the data. Data points in the plots are determined according to this variable.

4. Run the R script.

Files: 
- {ExperimentVideoName}_Shock.txt : Input data, which is created by Shocked Bee Detector (Python code), indicating whether bees are shocked or not.
- {ExperimentVideoName}_Data.xlsx : The output .xlsx file containing shock duration for each bee.
- {ExperimentVideoName}_IndividualsProfiles.jpg : Learning curves of each individual.
- {ExperimentVideoName}_ShockPlot.jpg : Group learning curve plot.

Note: 
- Make sure to replace {FileName} with the actual name of your data file.

For further inquiries or assistance, please contact Babur Erdem (author of the script) at ebabur@metu.edu.tr.
