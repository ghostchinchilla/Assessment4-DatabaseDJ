
\c playlist_app


CREATE TABLE IF NOT EXISTS playlists (
    playlist_id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);

INSERT INTO playlists
  (name, description)
VALUES
  ('Playlist 1', 'Description 1'),
  ('Playlist 2', 'Description 2'),
  ('Playlist 3', 'Description 3');




CREATE TABLE IF NOT EXISTS songs (
    song_id SERIAL PRIMARY KEY,
    title TEXT,
    artist TEXT,
    playlist_id INT 
);
INSERT INTO songs
    (title, artist, playlist_id)
VALUES
    ('Song 1', 'Artist 1', 1),
    ('Song 2', 'Artist 2', 2),
    ('Song 3', 'Artist 3', 3);


    

CREATE TABLE IF NOT EXISTS playlists_songs (
    playlist_id INT,
    song_id INT,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id),
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

INSERT INTO playlists_songs 
   (playlist_id, song_id)
VALUES
   (1, 1),
   (2, 2),
   (3, 3)
ON CONFLICT (playlist_id, song_id) DO NOTHING;

    



