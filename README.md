# Emotion Detector — Final Project

**Project name:** Emotion Detector (IBM Developing AI Applications with Python and Flask)  
**Author:** 24f2003765@ds.study.iitm.ac.in

AI-based Flask web application that analyzes customer feedback text and returns emotion scores (anger, disgust, fear, joy, sadness) using the Watson NLP Emotion Predict API.

## Features

- Watson NLP emotion detection
- Formatted JSON-style emotion output with dominant emotion
- Packaged `EmotionDetection` Python module
- Unit tests with `unittest`
- Flask web deployment at `/emotionDetector`
- Error handling for invalid or blank input
- Static code analysis with Pylint

## Setup

```bash
pip install -r requirements.txt
pip install -e .
python3 server.py
```

Open `http://localhost:5000/` in your browser.
