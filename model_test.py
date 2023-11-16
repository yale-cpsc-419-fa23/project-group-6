from app import create_app
from app.models.song import Song
from app.models.user import User
from app.models.genre import Genre
from app.utils.recommendation_utils import recommend_songs

from app.utils.audio_feature_utils import audio_feature_extractor

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')
    with app.app_context():
        print("User Create Test:")
        U = User()
        user = U.find_by_email("vo9kq@dkr.com")
        print(user)
        print(user.get_created_songs())

        for song in user.get_created_songs():
            print(song.get_creators())
            print(song.get_upload_date())

        print(Song.search_by_name("love"))
        song = Song.search_by_name("stupid")[0]
        print([genre.get_genre_name() for genre in song.get_genres()])

        genre = Genre.find_by_id(0)
        print([song.get_name() for song in genre.get_songs()][:10])

        genres = Genre.find_by_name("hip hop")
        for genre in genres[0:1]:
            print(genre.get_genre_name())

        genres = Genre.create_genres(["test_genre"])
        song.add_genres(genres)
        print(song.get_genres())

        user = U.find_by_username('t')
        for song in Song.search_by_name("test"):
            user.add_liked(song.get_id())
        print(user.get_liked_songs(5))

        for song in recommend_songs(71437):
            print(song.get_name())
            genres = song.get_genres()
            if len(genres) != 0:
                for genre in genres:
                    print(genre.get_genre_name(), end=", ")








    # audio_path = "app/static/uploads/sample-12s.mp3"
    # features = audio_feature_extractor(audio_path)
    # song_details = {
    #     "name": "Song Name Here",
    #     "duration_ms": 200000,  # Example duration in ms
    #     "filepath": audio_path
    # }
    # song_data = {**song_details, **features}

    #     # add song example
    #     S = Song()
    #     print(S.create(2085537, **song_data))
    #     # search song by name example
    #     matching_songs = Song.search_by_name("Song Name Here", limit=10)
    #     for song in matching_songs:
    #         print(song.name)
    #     # query song by id example
    #     print(song.search_by_id(1).name)

