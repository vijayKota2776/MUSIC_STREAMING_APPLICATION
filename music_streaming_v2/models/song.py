from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from music_streaming_v2.database import Base

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    track_number = Column(Integer, nullable=False)
    play_count = Column(Integer, default=0)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    
    album = relationship("Album", back_populates="songs")
    artist = relationship("Artist", back_populates="songs")
    playlists = relationship("PlaylistSong", back_populates="song")
    play_history = relationship("PlayHistory", back_populates="song")
