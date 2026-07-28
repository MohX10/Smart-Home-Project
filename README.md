# Smart Home Project

## Project Description

A smart dual-ESP32 system that ensures safety of people inside their houses by scanning for gas leaks and measuring the physical phenomena around people. If a gas leak is detected, it will alert people and tell them to evacuate the house.

Key features:
- It scans for gas leaks automatically from the first ESP32
- It sends data via UART to the second ESP32
- It also sends this data via Wi-Fi to Blynk, So you can check on anything from the phone


Technologies: MQ2 Gas sensor, HC-SR04 ultrasonic sensor, DHT22 sensor
Two ESP32s, An LED, Two servo motors, I2C LCD Display, Blynk IOT platform.

> **DISCLAIMER** : This project is only a simulation.

[License](LICENSE)

## Table of contents

- [Data Flow Diagram](Data%20Flow.pdf)
- [Connection Diagram](Connection%20Diagram.pdf)
- [Board 1 Source Code](Smart%20Home%20Project%20Board%201)
- [Board 2 Source Code](Smart%20Home%20Project%20Board%202)
- [Blynk Screenshots](Blynk%20Screenshots)
- [Virtual Serial Port Kit Setup](https://drive.google.com/uc?export=download&id=1gvaVHCDlAoVmdg-gA-Xg3URuwipngszB)
- [Project Demonstration Video](https://drive.google.com/uc?export=download&id=146h5DWvjIHckfnF-eAnxQ5mhzHtOq6cW)

## How to use the project
1- First of all here are the wokwi links
- [Smart Home Project Board 1](https://wokwi.com/projects/468421728224135169)
- [Smart Home Project Board 2](https://wokwi.com/projects/468449791726264321)

2- Then you need a tool called virtual serial port kit (This one is free and made by HHD Software)
- [Virtual Serial Port Kit](https://freevirtualserialports.com/)

3- Check this video to know how to set the tool
- [Virtual Serial Port Kit Setup]([How%20to%20setup%20virtual%20serial%20port%kit.mp4](https://drive.google.com/uc?export=download&id=1gvaVHCDlAoVmdg-gA-Xg3URuwipngszB)

4- Then you need to set up blynk (either from the web or from the app)

4.1- Blynk Setup on Web
  - Go to this link and sign up an account: [Blynk](https://www.blynk.io/)
  - After that check this video to create and setup your project: [How to setup blynk on web]

5- After that check this video to know how to use the project
- [Project Demonstration Video](https://drive.google.com/uc?export=download&id=146h5DWvjIHckfnF-eAnxQ5mhzHtOq6cW)
