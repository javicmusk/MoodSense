from transformers import pipeline

emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

EMOTION_TO_MOOD = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "angry",
    "fear": "anxious",
    "surprise": "neutral",
    "disgust": "stressed",
    "neutral": "neutral"
}

def analyze_mood(text):
    results = emotion_analyzer(text)[0]

    top_emotion = max(results, key=lambda x: x["score"])
    emotion_label = top_emotion["label"]
    confidence = top_emotion["score"]

    mood = EMOTION_TO_MOOD.get(emotion_label, "neutral")

    return mood, confidence
