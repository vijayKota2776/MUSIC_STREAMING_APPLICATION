from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from music_streaming_v2.database import Base

class PlayHistory(Base):
    __tablename__ = "play_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    played_at = Column(DateTime, default=datetime.utcnow)
    completion_percentage = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="play_history")
    song = relationship("Song", back_populates="play_history")
