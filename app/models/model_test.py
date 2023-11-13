from app import create_app
from app.models.song import Song
from app.models.user import User
from app.models.genre import Genre

from app.models.song_genre import SongGenre
from app.utils.audio_feature_utils import audio_feature_extractor

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')
    with app.app_context():
        print("User Create Test:")
        U = User()
        user = U.find_by_email("vo9kq@dkr.com")
        print(user)
        print(user.get_created_songs())

        print("song edit test")
        for song in user.get_created_songs():
            song.rename(song.Name + "rename")

        print(Song.search_by_name("love"))

        for song in Song.search_by_name("love"):
            print([genre.get_genre_name() for genre in song.get_genres()])

        genre = Genre.find_by_id(0)
        print([song.get_name() for song in genre.get_songs()][:10])

        genres = Genre.find_by_name("hip hop")
        for genre in genres:
            print(genre.get_genre_name())








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
