# Automated-Student-Entrance-Behavior-Monitoring-System-Using-AI
Real-time AI campus surveillance system using YOLO, MediaPipe &amp; OpenCV . It detects fights and recognizes faces from live webcam with Streamlit UI.
# Campus Vision — AI-Powered Campus Security System
Final Year Project | Bachelor of Science in Artificial Intelligence

A real-time computer vision system designed for automated campus 
security and monitoring using live webcam feeds.

## What it does
- Face Recognition — identifies and verifies individuals in 
  real-time from live webcam stream
- Fight Detection — detects violent behavior/fights using 
  pose estimation and motion analysis
- On-screen alerts triggered instantly when a threat is detected
- Streamlit dashboard for live monitoring

## How it works
1. Live webcam feed captured using OpenCV
2. YOLO runs object/person detection on each frame
3. MediaPipe extracts body pose keypoints for behavior analysis
4. Fight detection logic analyzes pose patterns to classify 
   violent vs normal activity
5. Face recognition identifies known individuals from the stream
6. On-screen alert popup triggered on fight detection
7. Streamlit UI displays the live feed and detection results

## Tech Stack
- Object Detection: YOLOv (person detection)
- Pose Estimation: MediaPipe
- Video Processing: OpenCV
- UI: Streamlit
- Language: Python

## Run Locally
pip install -r requirements.txt
streamlit run app.py
