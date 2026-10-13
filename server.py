"""Deploy a Flask application for Watson NLP emotion detection."""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emotion_analyzer():
    """Analyze text from the user and return emotion scores."""
    text_to_analyse = request.args.get("textToAnalyze")

    if text_to_analyse is None or text_to_analyse.strip() == "":
        return "Invalid text! Please try again"

    emotion_result = emotion_detector(text_to_analyse)
    anger = emotion_result["anger"]
    disgust = emotion_result["disgust"]
    fear = emotion_result["fear"]
    joy = emotion_result["joy"]
    sadness = emotion_result["sadness"]
    dominant_emotion = emotion_result["dominant_emotion"]

    if dominant_emotion is None:
        return "Invalid text! Please try again"

    response_str = (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy}, 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )
    return response_str


@app.route("/")
def render_index_page():
    """Render the main page for text input."""
    return render_template("index.html")


if __name__ == "__main__":
    # Static code analysis command:
    # pylint --disable=R,C,W1503 --enable=E --output-format=txt server.py
    import os

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
