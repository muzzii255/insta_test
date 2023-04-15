from fastapi import FastAPI
from pydantic import BaseModel
from instascraper import profile_scraper

# class Username(BaseModel):
#     username: str

app = FastAPI()

@app.get('/profile/{username}')
async def get_profile(username: str):
    print(username)
    data = profile_scraper(username)
    return data
    