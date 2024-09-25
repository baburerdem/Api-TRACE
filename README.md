Api-TRACE: Honey Bee Tracking in Constrained Environments, a computer vision-aided system to analyze the avoidance assays. Api-TRACE tracks individual bees from the video footage of the assay and detects the moments when they were exposed to the stimulus. The algorithm provides stimulus exposure duration and profiles of each individual bee, enabling fast and detailed analysis of the results. When you use the codes found here, please reference the relevant article.

First, run the Api-TRACE Video Processing Module (VPM), the Python code, to create exposure event data and a tracking video from the experiment video, then run the Api-TRACE Data Analysis and Visualization Module (DAVM), the R code, to visualize the exposure event data and create a tab-delimited .txt file for further statistical analysis.

When you use the codes found here, please reference the relevant article: Erdem, B., Ince, A., Sevin, S., Arslan, O.C., Gozen, A. G.,  Tugrul, G., & Alemdar, H. (2024). Api-TRACE: A System for honey bee tracking in a constrained environment to study bee learning process and the effect of lithium on learning. bioRxiv. https://doi.org/10.1101/2024.09.24.614513

---
Title: Api-TRACE Video Processing Module
- Author: Babur Erdem
- Date: 07/30/2023
- Update Date: 08/16/2024

Description:
This Python script is designed to detect and analyze the response of bees to a stimulus from the experiment video. 
The code performs several tasks, including:	 
- Extracting a subclip from the experiment video is spanned from the trial beginning time to a defined trial duration. 
- Measuring the size of a bee, defining ROIs by drawing shuttle box areas and the area of the exposure.
- Tracking the movement of bees within defined boxes.
- Analyzing whether bees are exposed to the stimulus or not based on their tracked positions.
- Generating output files, including the exposure event data file and a track video.

Instructions:
1. Ensure that the necessary Python libraries are installed:
	- OpenCV (cv2)
	- NumPy (np)
	- Shapely
	- MoviePy
	- ffmpeg

3. Run the script in a Python environment.
4. Enter the following variables on the prompt:
	- `Write the name of the experiment video:` : Name of the experiment video such as SampleVideo.mp4.
	- `Trial begin time (hh:mm:ss):`: Time when the stimulus was initiated in the experiment video.
	- `Trial duration (hh:mm:ss):`: Duration of the trial.

5. Follow the instructions prompted in the console window to measure a bee, draw box areas, and define the exposure area on the video frames.

Files: 
- {ExperimentVideoName}.mp4 : Experiment video, which is the input for the code.
- {ExperimentVideoName}_Exposure.txt : Output .txt file includes exposure event data, the input of DAVM (R code).
- {ExperimentVideoName}_DotVideo.mp4 : Output .mp4 video is showing the tracked positions of the bees.
- {ExperimentVideoName}_BeeNo.jpg : Output .jpg image shows the numbers assigned to boxes.
- {ExperimentVideoName}_ExposureArea.jpg : Output .jpg image indicates stimulus side.

Notes: 
- Ensure the experiment video is accessible and properly named. Do not use spaces, mathematical symbols (+, -, /, *, %, etc.), or characters that do not exist in English.
- The script utilizes various image processing techniques and interactive functionalities to facilitate analysis and tracking of bee movements.

For further inquiries or assistance, please contact Babur Erdem (author of the script) at ebabur@metu.edu.tr.

---
Title: Api-TRACE Data Analysis and Visualization Module
- Author: Babur Erdem
- Date: 2023-07-26
- Update Date: 2024-08-17

Description:
This R script is designed to analyze exposure event data and visualization. 
The code performs several tasks, including:
- Data preprocessing, converting exposure event data, came from VPM (Python code), to binary data.
- Creating a structured data frame.
- Generating a tab-delimited text file for further statistical analysis.
- Drawing two plots: individuals' and group exposure curves.

Instructions:
1. Prepare a metadata file in tab-delimited .txt format. The first column should be `BeeNo`. Numbers should be given according to {ExperimentVideoName}_BeeNo.jpg image. Then, enter the attributes of the experiment and bees, such as `Treatment`, `Dose`, `Unit`, `Replicate`, `Phase`, `Subspecies`. Named the file as {ExperimentVideoName}_Metadata.txt

2. Ensure that the necessary R libraries are installed:
	- ggplot2
	- dplyr
	- ggpubr

3. Update the following variables with appropriate values:
	- `VideoName` : Name of the experiment video. Do not write the .mp4 extension.
	- `IndVars` : Independent variables.
	- `fps` : fps of the experiment video.
	- `SamplingRate` : Downsample the data. Data points in the plots are determined according to this variable.

4. Run the R markdown (.Rmd) script.

Files: 
- {ExperimentVideoName}_Exposure.txt : Input data, which is created by VPM (Python code), indicating whether animals are exposed to the stimulus or not.
- {ExperimentVideoName}_Data.txt : The output .txt file containing exposure duration for each bee.
- {ExperimentVideoName}_IndividualsProfiles.jpg : Exposure curves of each individual.
- {ExperimentVideoName}_ExposurePlot.jpg : Group exposure curve plot.

Additionally, if you run the script with the .R extension, you can enter variables according to the prompts in the console. 
In this case, pay attention to these:
- `Write the name of the experiment video:` Do not write the .mp4 extension when you enter the response. 
- `Define the independent variables:` Separate independent variables with commas only, no spaces. 

Note: 
- Make sure to replace {FileName} with the actual name of your data file.
- Make sure that the independent variables you enter are consistent with the column names in the metadata file.

For further inquiries or assistance, please contact Babur Erdem (author of the script) at ebabur@metu.edu.tr.
