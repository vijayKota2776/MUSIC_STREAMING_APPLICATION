import strawberry
from typing import List, Optional
from sqlalchemy import select
from music_streaming_v2.models.album import Album
from music_streaming_v2.models.user import User
from music_streaming_v2.models.song import Song
from music_streaming_v2.models.artist import Artist
from music_streaming_v2.models.playlist import Playlist
from music_streaming_v2.types.album import AlbumType
from music_streaming_v2.types.user import UserType
from music_streaming_v2.types.song import SongType
from music_streaming_v2.types.artist import ArtistType
from music_streaming_v2.types.playlist import PlaylistType
from music_streaming_v2.mutations.playlist import PlaylistMutation
from music_streaming_v2.mutations.playback import PlaybackMutation

@strawberry.type
class Query:
    @strawberry.field
    async def album(self, info: strawberry.Info, id: int) -> Optional[AlbumType]:
        async with info.context["db"]() as session:
            return await session.get(Album, id)

    @strawberry.field
    async def user(self, info: strawberry.Info, id: int) -> Optional[UserType]:
        async with info.context["db"]() as session:
            return await session.get(User, id)

    @strawberry.field
    async def popular_songs(self, info: strawberry.Info, limit: int = 10) -> List[SongType]:
        async with info.context["db"]() as session:
            stmt = select(Song).order_by(Song.play_count.desc()).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    @strawberry.field
    async def artist(self, info: strawberry.Info, id: int) -> Optional[ArtistType]:
        async with info.context["db"]() as session:
            return await session.get(Artist, id)

    @strawberry.field
    async def public_playlists(self, info: strawberry.Info) -> List[PlaylistType]:
        async with info.context["db"]() as session:
            stmt = select(Playlist).where(Playlist.is_public == True)
            result = await session.execute(stmt)
            return result.scalars().all()

@strawberry.type
class Mutation(PlaylistMutation, PlaybackMutation):
    pass
