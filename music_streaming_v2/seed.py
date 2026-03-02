import asyncio
from datetime import datetime
from music_streaming_v2.database import AsyncSessionLocal
from music_streaming_v2.models.artist import Artist
from music_streaming_v2.models.album import Album
from music_streaming_v2.models.song import Song
from music_streaming_v2.models.user import User
from music_streaming_v2.models.playlist import Playlist, PlaylistSong
from music_streaming_v2.models.play_history import PlayHistory

async def seed():
    print("Seeding data...")
    async with AsyncSessionLocal() as session:
        # Create Artists
        artist1 = Artist(
            name='The Midnight',
            bio='Synthwave band from Los Angeles.',
            genre='Synthwave',
            image_url='https://example.com/the-midnight.jpg'
        )
        artist2 = Artist(
            name='Gunship',
            bio='Retrowave band from the UK.',
            genre='Retrowave',
            image_url='https://example.com/gunship.jpg'
        )
        session.add_all([artist1, artist2])
        await session.commit()
        print(f"Created artists: {artist1.name}, {artist2.name}")

        # Create Album
        album1 = Album(
            title='Endless Summer',
            release_date=datetime(2016, 8, 5),
            cover_url='https://example.com/endless-summer.jpg',
            artist_id=artist1.id
        )
        session.add(album1)
        await session.commit()
        print(f"Created album: {album1.title}")

        # Create Songs
        song1 = Song(
            title='Endless Summer',
            duration=345,
            track_number=1,
            album_id=album1.id,
            artist_id=artist1.id,
            play_count=1500
        )
        song2 = Song(
            title='Sunset',
            duration=327,
            track_number=2,
            album_id=album1.id,
            artist_id=artist1.id,
            play_count=2000
        )
        song3 = Song(
            title='Jason',
            duration=335,
            track_number=3,
            album_id=album1.id,
            artist_id=artist1.id,
            play_count=1200
        )
        session.add_all([song1, song2, song3])
        await session.commit()
        print(f"Created songs for album: {album1.title}")

        # Create User
        user = User(
            username='johndoe',
            email='john@example.com'
        )
        session.add(user)
        await session.commit()
        print(f"Created user: {user.username}")

        # Create Playlist
        playlist = Playlist(
            name='Retro Vibes',
            user_id=user.id,
            is_public=True
        )
        session.add(playlist)
        await session.commit()
        print(f"Created playlist: {playlist.name}")

        # Add songs to playlist
        ps = PlaylistSong(
            playlist_id=playlist.id,
            song_id=song2.id
        )
        session.add(ps)

        # Create Play History
        history = PlayHistory(
            user_id=user.id,
            song_id=song2.id,
            completion_percentage=100
        )
        session.add(history)
        
        await session.commit()
        print("Playlist and History populated.")

    print("Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed())
