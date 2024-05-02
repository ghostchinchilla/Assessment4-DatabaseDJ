# from models import PlaylistSong, Song, Playlist, db
# from app import app
# from flask_sqlalchemy import SQLAlchemy


# def connect_db(app):
#     """Connect to database."""

#     db.app = app
#     db.init_app(app)


# # Create all tables
# db.drop_all()
# db.create_all()

# # Song.query.delete()
# # Playlist.query.delete()
# # PlaylistSong.query.delete()


# s1 = Song(title="s1", artist="a1")
# pl1 = Playlist(name="code", description="for coding")


# db.session.add_all([s1, pl1])
# db.session.commit()

# ps1 = PlaylistSong(song_id=1, playlist_id=1)
# db.session.add_all([ps1])
# db.session.commit()