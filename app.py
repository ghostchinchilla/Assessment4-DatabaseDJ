from flask import Flask, redirect, render_template, flash, request
# from flask_debugtoolbar import DebugToolbarExtension
from wtforms import SelectField
from wtforms_alchemy import ModelForm, model_form_factory
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
import config
import logging
logger = logging.getLogger(__name__)

import secrets



app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = secrets.token_hex(24)  # Generates a random 24-byte key
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize SQLAlchemy
connect_db(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    try:
        playlists = Playlist.query.all()
    except Exception as e:
        logger.error("Error fetching playlists: %s", e)  # Log the exception
        flash("Error fetching playlists.", "error")
        return redirect("/")

    return render_template("playlists.html", playlists=playlists)



@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    form = PlaylistForm()

    if form.validate_on_submit():
        try:
            playlist = Playlist(name=form.name.data, description=form.description.data)
            db.session.add(playlist)
            db.session.commit()
            flash("Playlist added!", "success")
            return redirect('/playlists')
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if there's an error
            flash("An error occurred while adding the playlist.", "error")
            return render_template("new_playlist.html", form=form)

    return render_template("new_playlist.html", form=form)




##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    song = Song.query.get(song_id)
    return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:
    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    form = SongForm()

    if form.validate_on_submit():
        song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(song)
        db.session.commit()
        return redirect('/songs')

    return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm(playlist_id=playlist_id)

    if form.validate_on_submit():

        song_id = form.song.data
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
        flash("Song added to the playlist!", "success")

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                           playlist=playlist,
                           form=form)