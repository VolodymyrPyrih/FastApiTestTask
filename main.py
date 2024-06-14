from fastapi import FastAPI
import uvicorn
from routers import user, post

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, reload=True)
