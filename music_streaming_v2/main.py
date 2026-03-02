from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
from music_streaming_v2.queries.root import Query, Mutation
from music_streaming_v2.database import AsyncSessionLocal

schema = strawberry.Schema(query=Query, mutation=Mutation)

async def get_context():
    return {"db": AsyncSessionLocal}

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "Music Streaming GraphQL API (Restructured) is running. Go to /graphql"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
