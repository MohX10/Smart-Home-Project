# Smart Home Project

## Project Description

A smart dual-ESP32 system that ensures safety of people inside their houses by scanning for gas leaks and measuring the physical phenomena around people. If a gas leak is detected, it will alert people and tell them to evacuate the house.
Key features:
It scans for gas leaks automatically from the first ESP32
It sends data via UART to the second ESP32
 It also sends this data via Wi-Fi to Blynk, So you can check on anything from the phone
Technologies: MQ2 Gas sensor, HC-SR04 ultrasonic sensor, DHT22 sensor
Two ESP32s, An LED, Two servo motors, I2C LCD Display, Blynk IOT platform.

> **DISCLAIMER** : This project is only a simulation.

[License](LICENSE)

## Table of contents

- [System Architecture Diagram](System%20Architecture.pdf)
- [Data Flow Diagram](Data%20Flow.pdf)
- [Connection Diagram](Connection%20Diagram.pdf)
- [Board 1 Source Code](Smart%20Home%20Project%20Board%201)
- [Board 2 Source Code](Smart%20Home%20Project%20Board%202)
