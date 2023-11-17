import random


def audio_feature_extractor(audio_path):
    # Load audio file
    features = {
        "Explicit": random.randint(0, 1),
        "Mode": random.randint(0, 1),
        "Key": random.randint(0, 11),
        "Tempo": random.uniform(50, 200),
        "Energy": random.random(),
        "Danceability": random.random(),
        "Loudness": random.uniform(-60, 0),
        "Acousticness": random.random(),
        "Instrumentalness": random.random(),
        "Liveness": random.random(),
        "Speechiness": random.random(),
        "Valence": random.random(),
    }
    return features


if __name__ == "__main__":
    features = audio_feature_extractor("/Users/kai/Documents/Study/CPSC519 Web/project-group-6/data/sample-15s.mp3")
    print(features)
