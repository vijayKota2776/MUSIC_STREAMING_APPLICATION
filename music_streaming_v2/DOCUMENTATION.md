# Project Documentation: Music Streaming GraphQL API (v2)

## 1. Overview
The Music Streaming GraphQL API is a fast, asynchronous Python-based web service designed to manage music metadata (Artists, Albums, Songs), User profiles, Playlists, and Play History. 

This version (v2) features a strictly modular architecture, separating database concerns, business logic (mutations), and the GraphQL schema.

## 2. Technology Stack
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance ASGI framework)
- **GraphQL Engine**: [Strawberry GraphQL](https://strawberry.rocks/) (Code-first GraphQL)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Asynchronous mode)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Driver**: `asyncpg` (Asynchronous PostgreSQL client)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)

## 3. Architecture & Project Structure

The project follows a modular design to ensure scalability and maintainability.

```text
music_streaming_v2/
├── models/              # SQLAlchemy Database Models
│   ├── artist.py        # Artist entity & relationships
│   ├── album.py         # Album entity (belongs to Artist)
│   ├── song.py          # Song entity (belongs to Album/Artist)
│   ├── user.py          # User entity
│   ├── playlist.py      # Playlist & association table (PlaylistSong)
│   └── play_history.py  # User listening history records
├── types/               # Strawberry GraphQL Types
│   ├── artist.py        # GraphQL representation of Artist
│   ├── album.py         # GraphQL representation of Album
│   ├── song.py          # GraphQL representation of Song
│   ├── user.py          # GraphQL representation of User
│   ├── playlist.py      # GraphQL representation of Playlist
│   └── play_history.py  # GraphQL representation of Playhistory
├── mutations/           # Business Logic (Write Operations)
│   ├── playlist.py      # Create, update, and manage playlists
│   └── playback.py      # Record playback events
├── queries/             # Data Fetching (Read Operations)
│   └── root.py          # Aggregates all queries into a single root
├── database.py          # DB Engine & Asynchronous Session Configuration
├── main.py              # Application initialization & Router setup
├── seed.py              # Script to populate initial development data
└── alembic.ini          # Migrations configuration
```

### Key Architectural Decisions
- **Absolute Imports**: Every module uses absolute imports (e.g., `from music_streaming_v2.models...`) to ensure stability across different execution contexts.
- **Lazy Loading Types**: Strawberry `lazy` loading is used between circularly dependent types (e.g., Artist <-> Album) to prevent import errors.
- **Async-First**: Every database interaction is awaited using `AsyncSession`, ensuring the API remains non-blocking.
- **Context Injection**: The database session factory is injected into the GraphQL context, allowing resolvers to manage their own unit-of-work.

## 4. Database Schema

The database uses a relational schema with the following core entities:
1. **Artists**: The creators.
2. **Albums**: Collections of songs, linked to an artist.
3. **Songs**: Individual tracks with duration and play counts.
4. **Users**: Platform members.
5. **Playlists**: User-generated collections of songs.
6. **Play History**: Automated logs of what songs users played.

### Migration Management
Database changes are handled via **Alembic**. To apply changes:
```bash
./music_streaming_v2/venv/bin/alembic -c music_streaming_v2/alembic.ini upgrade head
```

## 5. API Documentation (GraphQL)

The API is accessible via a single endpoint: `/graphql`.

### Common Queries

**Fetch Popular Songs:**
```graphql
query {
  popularSongs(limit: 5) {
    title
    playCount
    artist {
      name
    }
  }
}
```

**Get Artist Details with Albums:**
```graphql
query {
  artist(id: 1) {
    name
    bio
    albums {
      title
      releaseDate
    }
  }
}
```

### Common Mutations

**Create a Playlist:**
```graphql
mutation {
  createPlaylist(input: {
    name: "My Favorites",
    userId: 1,
    isPublic: true
  }) {
    playlist {
      id
      name
    }
  }
}
```

**Record a song play:**
```graphql
mutation {
  recordPlay(userId: 1, songId: 10, completionPercentage: 100) {
    playedAt
    song {
      title
    }
  }
}
```

## 6. Setup and Development

### Local Requirements
- Python 3.12+
- PostgreSQL (Homebrew recommended on Mac: `brew install postgresql@14`)

### Installation & Run
1. **Install Dependencies**:
   ```bash
   python3 -m venv music_streaming_v2/venv
   ./music_streaming_v2/venv/bin/pip install -r music_streaming_v2/requirements.txt
   ```
2. **Setup Database**:
   ```bash
   brew services start postgresql@14
   createdb music_db
   ```
3. **Run Migrations & Seed**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   ./music_streaming_v2/venv/bin/alembic -c music_streaming_v2/alembic.ini upgrade head
   ./music_streaming_v2/venv/bin/python3 music_streaming_v2/seed.py
   ```
4. **Start Development Server**:
   ```bash
   ./music_streaming_v2/venv/bin/uvicorn music_streaming_v2.main:app --reload
   ```
