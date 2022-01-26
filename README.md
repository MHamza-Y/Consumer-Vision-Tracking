# Consumer-Vision-Tracking

## Pre Requisite
Improtant note: This project uses cuda cores to accelerate the project. Make sure to run it on device with cuda cores (with GPU) if running on desktop/laptop. The docker-compose-nano is also included to run the code on jetson nano (which also have cuda cores). But for jetson nano it has not been tested yet and their may be dependency conflicts due to the CPU architecture being different. Make sure following are installed on your system
### Hardware
- Nvidia GPU (if not running on jetson)
- Webcam

or
- Jetson Nano
- imx219 camera

### Software
- Linux/Ubuntu
- Docker
- Dokcer Compose
- Nvidia Cuda Toolkit
- Jetpack sdk(only for jetson)


## Executing Code on Laptop (with built-in webcam)
To run the code on laptop execute the following terminal command while in the root directory of the project,

`docker-compose run`

## Executing Code on Jetson Nano
To run the code on jetson Nano run the following terminal command while in the root directory of the project,

`docker-compose -f docker-compose-nano.yaml run`
