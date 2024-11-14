from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_username)


#this code creates all the table in sqlalchemy but it won't help us in modifying the table
# models.Base.metadata.create_all(bind = engine)

xyz = FastAPI()

origins = ["*"]

xyz.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


xyz.include_router(post.router)
xyz.include_router(user.router)
xyz.include_router(auth.router)
xyz.include_router(votes.router)

# my_posts = [{"title" : "title for post 1", "content":"content for post 1","id" : 1},{"title" : "Favourite Foods","content" : "i love biriyani", "id" : 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id :
#             return p

# def find_post_index(id):
#     for index, post in enumerate(my_posts):
#             if post["id"] == id:
#                 return index
            




