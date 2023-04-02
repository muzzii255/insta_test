from fastapi import FastAPI
from pydantic import BaseModel
from instascraper import profile_scraper

class Username(BaseModel):
    username: str

app = FastAPI()

@app.post('/userprofile')
async def get_profile(text: Username):
    username = text.username
    print(username)
    return profile_scraper(username)
    