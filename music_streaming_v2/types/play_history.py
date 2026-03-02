import strawberry
from datetime import datetime
from typing import Annotated

@strawberry.type
class PlayHistoryType:
    id: strawberry.ID
    user_id: int
    song_id: int
    played_at: datetime
    completion_percentage: int

    @strawberry.field
    async def song(self, info: strawberry.Info) -> Annotated["SongType", strawberry.lazy("music_streaming_v2.types.song")]:
        from music_streaming_v2.models.song import Song
        async with info.context["db"]() as session:
            return await session.get(Song, self.song_id)
