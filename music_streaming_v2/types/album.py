import strawberry
from datetime import datetime
from typing import List, Optional, Annotated

@strawberry.type
class AlbumType:
    id: strawberry.ID
    title: str
    release_date: datetime
    cover_url: Optional[str]
    artist_id: int

    @strawberry.field
    async def artist(self, info: strawberry.Info) -> Annotated["ArtistType", strawberry.lazy("music_streaming_v2.types.artist")]:
        from music_streaming_v2.models.artist import Artist
        async with info.context["db"]() as session:
            return await session.get(Artist, self.artist_id)

    @strawberry.field
    async def songs(self, info: strawberry.Info) -> List[Annotated["SongType", strawberry.lazy("music_streaming_v2.types.song")]]:
        from music_streaming_v2.models.song import Song
        from sqlalchemy import select
        async with info.context["db"]() as session:
            result = await session.execute(
                select(Song).where(Song.album_id == self.id).order_by(Song.track_number)
            )
            return result.scalars().all()
