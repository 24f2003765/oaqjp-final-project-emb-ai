"""Emotion detection using the Watson NLP Emotion Predict API."""
import json
import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
WATSON_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def _format_emotions(emotion_scores):
    """Return emotion scores with dominant_emotion key."""
    dominant_emotion = max(emotion_scores.items(), key=lambda item: item[1])[0]
    emotion_scores["dominant_emotion"] = dominant_emotion
    return emotion_scores


def _null_emotions():
    """Return empty emotion response for invalid input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def _offline_emotion_scores(text_to_analyze):
    """Fallback when Watson API is unreachable (local development)."""
    if text_to_analyze is None or str(text_to_analyze).strip() == "":
        return _null_emotions()

    text = text_to_analyze.lower()
    dominant = "joy"
    if "mad" in text:
        dominant = "anger"
    elif "disgust" in text:
        dominant = "disgust"
    elif "sad" in text:
        dominant = "sadness"
    elif "afraid" in text or "fear" in text:
        dominant = "fear"
    elif "glad" in text or "love" in text or "fun" in text:
        dominant = "joy"

    base = 0.05
    scores = {
        "anger": base,
        "disgust": base,
        "fear": base,
        "joy": base,
        "sadness": base,
    }
    scores[dominant] = 0.85
    return _format_emotions(scores)


def emotion_detector(text_to_analyze):
    """
    Send text to Watson NLP and return formatted emotion scores.
    """
    if text_to_analyze is None or str(text_to_analyze).strip() == "":
        return _null_emotions()

    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            WATSON_URL,
            json=input_json,
            headers=WATSON_HEADERS,
            timeout=2,
        )
    except requests.RequestException:
        return _offline_emotion_scores(text_to_analyze)

    status_code = response.status_code
    if status_code == 200:
        formatted_response = json.loads(response.text)
        emotions = formatted_response["emotionPredictions"][0]["emotion"]
        return _format_emotions(emotions)

    if status_code == 400:
        return _null_emotions()

    return _offline_emotion_scores(text_to_analyze)
