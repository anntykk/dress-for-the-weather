# Dress for the weather app (work in progress)

## About this project
This project fetches data from the Location Forecast API by Yr.no (https://developer.yr.no) which is then used to create and app using Flask with suggestions on what to wear based on weather conditions. 

## Get started
### Build Docker image
docker build -t dress-for-the-weather .

### Run Docker container
docker run -p 5000:5000 --name dress-for-the-weather-container dress-for-the-weather

## Main goals
- [X] Understand the API
- [X] Fetch some data from the API
- [X] Subset data to relevant day and time
- [X] Clean data (obtain relevant parameters)
- [X] Create logic for selecting what to wear
- [X] Create definition for types of clothes, based on temperature and rain
- [X] Create function to decide what clothes 
- [X] Create flask web application
- [X] Create htlm-file for some basic output and font
- [ ] Run in Docker
- [ ] Deploy to an online server (Azure?)

