from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from music_streaming_v2.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    playlists = relationship("Playlist", back_populates="user")
    play_history = relationship("PlayHistory", back_populates="user")
