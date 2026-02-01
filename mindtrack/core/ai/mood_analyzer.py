from transformers import pipeline

emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None   #replaces return_all_scores
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

def analyze_mood(text: str):
    results = emotion_analyzer(text)[0]

    top_emotion = max(results, key=lambda x: x["score"])
    emotion_label = top_emotion["label"]
    confidence = round(top_emotion["score"], 3)

    mood = EMOTION_TO_MOOD.get(emotion_label, "neutral")

    return {
        "mood": mood,
        "confidence": confidence,
        "emotion": emotion_label
    }
