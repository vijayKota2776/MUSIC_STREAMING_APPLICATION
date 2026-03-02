import strawberry
from typing import List, Optional, Annotated

@strawberry.type
class ArtistType:
    id: strawberry.ID
    name: str
    bio: Optional[str]
    genre: Optional[str]
    image_url: Optional[str]

    @strawberry.field
    async def albums(self, info: strawberry.Info) -> List[Annotated["AlbumType", strawberry.lazy("music_streaming_v2.types.album")]]:
        from music_streaming_v2.models.album import Album
        from sqlalchemy import select
        async with info.context["db"]() as session:
            result = await session.execute(select(Album).where(Album.artist_id == self.id))
            return result.scalars().all()

    @strawberry.field
    async def songs(self, info: strawberry.Info) -> List[Annotated["SongType", strawberry.lazy("music_streaming_v2.types.song")]]:
        from music_streaming_v2.models.song import Song
        from sqlalchemy import select
        async with info.context["db"]() as session:
            result = await session.execute(select(Song).where(Song.artist_id == self.id))
            return result.scalars().all()
