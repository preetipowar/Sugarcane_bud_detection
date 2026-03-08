# Sugarcane Bud Detection System

A computer vision system designed to detect sugarcane buds for automated planting systems.

## Overview
This project uses a trained deep learning model to detect viable sugarcane buds through a webcam feed and assists automated planting.

## Components
• PyTorch bud detection model  
• Webcam-based detection interface  
• Arduino-based planting mechanism  
• 3D printed mechanical structure

## Project Structure
src/ → Python detection code  
model/ → trained detection model  
arduino/ → microcontroller code  
cad/ → 3D design for the mechanism  

## Requirements

Python 3.10+
torch
opencv-python
ultralytics

## Run

python src/webcam.py
