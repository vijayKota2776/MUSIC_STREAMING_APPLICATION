import strawberry
from datetime import datetime
from typing import List, Annotated

@strawberry.type
class PlaylistType:
    id: strawberry.ID
    name: str
    user_id: int
    created_at: datetime
    is_public: bool

    @strawberry.field
    async def songs(self, info: strawberry.Info) -> List[Annotated["SongType", strawberry.lazy("music_streaming_v2.types.song")]]:
        from music_streaming_v2.models.playlist import PlaylistSong
        from music_streaming_v2.models.song import Song
        from sqlalchemy import select
        async with info.context["db"]() as session:
            stmt = select(Song).join(PlaylistSong).where(PlaylistSong.playlist_id == self.id)
            result = await session.execute(stmt)
            return result.scalars().all()
