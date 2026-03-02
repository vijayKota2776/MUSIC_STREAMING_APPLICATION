from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from music_streaming_v2.database import Base

class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    bio = Column(String)
    genre = Column(String)
    image_url = Column(String)
    
    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", back_populates="artist")
