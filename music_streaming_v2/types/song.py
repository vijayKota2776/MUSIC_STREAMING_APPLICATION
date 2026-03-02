import strawberry
from typing import Optional, Annotated
from music_streaming_v2.types.utils import format_duration

@strawberry.type
class SongType:
    id: strawberry.ID
    title: str
    duration: int
    track_number: int
    play_count: int
    album_id: int
    artist_id: int

    @strawberry.field
    def duration_formatted(self) -> str:
        return format_duration(self.duration)

    @strawberry.field
    async def artist(self, info: strawberry.Info) -> Annotated["ArtistType", strawberry.lazy("music_streaming_v2.types.artist")]:
        from music_streaming_v2.models.artist import Artist
        async with info.context["db"]() as session:
            return await session.get(Artist, self.artist_id)

    @strawberry.field
    async def album(self, info: strawberry.Info) -> Annotated["AlbumType", strawberry.lazy("music_streaming_v2.types.album")]:
        from music_streaming_v2.models.album import Album
        async with info.context["db"]() as session:
            return await session.get(Album, self.album_id)
