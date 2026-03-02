from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from music_streaming_v2.database import Base

class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    cover_url = Column(String)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")
