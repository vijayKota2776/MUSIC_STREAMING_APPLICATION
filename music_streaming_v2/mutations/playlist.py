import strawberry
from typing import Optional
from music_streaming_v2.models.playlist import Playlist, PlaylistSong
from music_streaming_v2.types.playlist import PlaylistType

@strawberry.input
class CreatePlaylistInput:
    name: str
    user_id: int
    is_public: bool = True

@strawberry.input
class AddSongToPlaylistInput:
    playlist_id: int
    song_id: int

@strawberry.type
class PlaylistPayload:
    playlist: Optional[PlaylistType]

@strawberry.type
class PlaylistMutation:
    @strawberry.mutation
    async def create_playlist(self, info: strawberry.Info, input: CreatePlaylistInput) -> PlaylistPayload:
        async with info.context["db"]() as session:
            playlist = Playlist(name=input.name, user_id=input.user_id, is_public=input.is_public)
            session.add(playlist)
            await session.commit()
            await session.refresh(playlist)
            return PlaylistPayload(playlist=playlist)

    @strawberry.mutation
    async def add_song_to_playlist(self, info: strawberry.Info, input: AddSongToPlaylistInput) -> PlaylistPayload:
        async with info.context["db"]() as session:
            ps = PlaylistSong(playlist_id=input.playlist_id, song_id=input.song_id)
            session.add(ps)
            await session.commit()
            playlist = await session.get(Playlist, input.playlist_id)
            return PlaylistPayload(playlist=playlist)

    @strawberry.mutation
    async def remove_song_from_playlist(self, info: strawberry.Info, playlist_id: int, song_id: int) -> PlaylistPayload:
        from sqlalchemy import delete
        async with info.context["db"]() as session:
            stmt = delete(PlaylistSong).where(
                PlaylistSong.playlist_id == playlist_id,
                PlaylistSong.song_id == song_id
            )
            await session.execute(stmt)
            await session.commit()
            playlist = await session.get(Playlist, playlist_id)
            return PlaylistPayload(playlist=playlist)
