# Consumer-Vision-Tracking

## Pre Requisite
Make sure following are installed on your system
### Hardware
- Nvidia GPU (if not running on jetson)

or
- Jetson Nano

### Software
- Linux/Ubuntu
- Docker
- Dokcer Compose
- Nvidia Cuda Toolkit
- Jetpack sdk(only for jetson)


## Executing Code on Laptop (with built-in webcam)
To run the code on laptop execute the following command in terminal

`docker-compose run`

## Executing Code on Jetson Nano
To run the code on jetson Nano run the following command

`docker-compose -f docker-compose-nano.yaml run`
