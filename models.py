"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.init_app=(app)



class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    songs = db.relationship("PlaylistSong", back_populates="playlist")


class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)
    playlists = db.relationship("PlaylistSong", back_populates="song")


class PlaylistSong(db.Model):
    __tablename__ = "playlists_songs"
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)
    playlist = db.relationship("Playlist", back_populates="songs")
    song = db.relationship("Song", back_populates="playlists")
