from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from app.models.user import User
from app.models.song import Song


def recommend_songs(user_id, n_likes=5, n_recommendations=5, n_samples=100):
    user = User.find_by_id(user_id)
    liked_songs = [song.get_id() for song in user.get_liked_songs(n_likes)]
    if len(liked_songs) == 0:
        return None
    songs = Song.get_all_songs()
    songs_data = [song.__dict__ for song in songs]
    songs_df = pd.DataFrame(songs_data)
    songs_df = songs_df.drop('_sa_instance_state', axis=1)
    recommended_songs = recommend_songs_helper(songs_df, liked_songs, n_recommendations, n_samples)
    return Song.get_songs_by_ids(recommended_songs)


def recommend_songs_helper(songs_df, liked_songs, n_recommendations, n_samples):
    feature_cols = ['Duration_ms', 'Explicit', 'Mode', 'Key', 'Tempo', 'Energy',
                    'Danceability', 'Loudness', 'Acousticness', 'Instrumentalness',
                    'Liveness', 'Speechiness', 'Valence']

    liked_songs_df = songs_df.loc[songs_df['SongId'].isin(liked_songs)]
    candidate_songs_df = songs_df.loc[~songs_df['SongId'].isin(liked_songs)]
    n_recommendations = min(n_recommendations, len(candidate_songs_df), n_samples)

    if len(candidate_songs_df) < n_samples:
        candidate_songs_df = candidate_songs_df.sample(n=100, replace=True)
    else:
        candidate_songs_df = candidate_songs_df.sample(n=100)

    liked_features = liked_songs_df[feature_cols]
    liked_features = liked_features.fillna(liked_features.mean())
    mean_vector = liked_features.mean().values.reshape(1, -1)
    candidate_features = candidate_songs_df[feature_cols]
    candidate_features = candidate_features.fillna(candidate_features.mean())
    song_matrix = candidate_features.values

    similarity = cosine_similarity(mean_vector, song_matrix)

    indices = np.argsort(similarity[0])[::-1][:n_recommendations]

    return candidate_songs_df.iloc[indices]['SongId'].values.tolist()
