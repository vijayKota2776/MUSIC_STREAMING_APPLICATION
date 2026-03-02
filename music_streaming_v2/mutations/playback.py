import strawberry
from sqlalchemy import update
from music_streaming_v2.models.play_history import PlayHistory
from music_streaming_v2.models.song import Song
from music_streaming_v2.types.play_history import PlayHistoryType

@strawberry.type
class PlaybackMutation:
    @strawberry.mutation
    async def record_play(self, info: strawberry.Info, user_id: int, song_id: int, completion_percentage: int) -> PlayHistoryType:
        async with info.context["db"]() as session:
            # Create PlayHistory
            history = PlayHistory(
                user_id=user_id,
                song_id=song_id,
                completion_percentage=completion_percentage
            )
            session.add(history)
            
            # Increment play_count
            stmt = update(Song).where(Song.id == song_id).values(play_count=Song.play_count + 1)
            await session.execute(stmt)
            
            await session.commit()
            await session.refresh(history)
            return history
