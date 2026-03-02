import strawberry
from typing import List, Annotated

@strawberry.type
class UserType:
    id: strawberry.ID
    username: str
    email: str

    @strawberry.field
    async def playlists(self, info: strawberry.Info) -> List[Annotated["PlaylistType", strawberry.lazy("music_streaming_v2.types.playlist")]]:
        from music_streaming_v2.models.playlist import Playlist
        from sqlalchemy import select
        async with info.context["db"]() as session:
            result = await session.execute(select(Playlist).where(Playlist.user_id == self.id))
            return result.scalars().all()

    @strawberry.field
    async def play_history(self, info: strawberry.Info) -> List[Annotated["PlayHistoryType", strawberry.lazy("music_streaming_v2.types.play_history")]]:
        from music_streaming_v2.models.play_history import PlayHistory
        from sqlalchemy import select
        async with info.context["db"]() as session:
            result = await session.execute(
                select(PlayHistory).where(PlayHistory.user_id == self.id).order_by(PlayHistory.played_at.desc())
            )
            return result.scalars().all()
