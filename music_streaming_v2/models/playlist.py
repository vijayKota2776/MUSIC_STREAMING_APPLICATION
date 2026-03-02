from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from music_streaming_v2.database import Base

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="playlists")
    songs = relationship("PlaylistSong", back_populates="playlist")

class PlaylistSong(Base):
    __tablename__ = "playlist_songs"
    playlist_id = Column(Integer, ForeignKey("playlists.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    playlist = relationship("Playlist", back_populates="songs")
    song = relationship("Song", back_populates="playlists")
