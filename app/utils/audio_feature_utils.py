import random


def audio_feature_extractor(audio_path):
    # Load audio file
    features = {
        "explicit": random.randint(0, 1),
        "mode": random.randint(0, 1),
        "key": random.randint(0, 11),
        "tempo": random.uniform(50, 200),
        "energy": random.random(),
        "danceability": random.random(),
        "loudness": random.uniform(-60, 0),
        "acousticness": random.random(),
        "instrumentalness": random.random(),
        "liveness": random.random(),
        "speechiness": random.random(),
        "valence": random.random(),
    }
    return features


if __name__ == "__main__":
    features = audio_feature_extractor("/Users/kai/Documents/Study/CPSC519 Web/project-group-6/data/sample-15s.mp3")
    print(features)
