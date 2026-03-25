# Footwear Biomechanics Comaprison App

## Overview
This is a prototype app built for an MSc coursework assessment, comparing the kinematics, kinetics and ground reaction forces in 3 different shoes. Data was captured on an instrumented treadmill, processed in Qualisys track manager, post processed in visual 3D and finally means, standard deviations and full trials were exported to CSV files to input into the repository for app purposes. 

The primary aim of this project was to demonstrate the development of footwear assessment skills, with this application acting as a tool to support data exploration and visualisation. 

## Structure
- Variables and constants are defined in the config file. 
- Data is loaded via the data loader file. 
- Additional metrics include peak, trough, and range for all variables, as well as loading rate for ground reaction force and are defined in the metrics file. 
- The gui of the app is built in the app file.   

## Notebook
Before developing the application, a Jupyter notebook was used to explore the dataset and design the initial backend structure. This notebook is included in the repository to demonstrate the early stages of the project.

## Application Preview
A preview of the application can be seen at https://7115-footwear-repository-p99ez7xmgdwyfiq3psbpsk.streamlit.app/. 

## Use of AI Tools
Claude AI was used to assist in the creation of the interactive application after all data had been collected, processed and formatted, and the backend structure was developed. From here, claude primarily helped with the structuring of data for the streamlit interface and improve development efficiency. 