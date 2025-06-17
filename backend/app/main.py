from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
from typing import Optional, List, Union
import re

app = FastAPI(title="Joke Search API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JokeResponse(BaseModel):
    error: bool
    category: str
    type: str
    setup: Optional[str] = None
    delivery: Optional[str] = None
    joke: Optional[str] = None
    flags: dict
    id: int
    safe: bool
    lang: str

class JokeRequest(BaseModel):
    request: str

# Common category mappings
CATEGORY_MAPPINGS = {
    'programming': 'Programming',
    'programmer': 'Programming',
    'code': 'Programming',
    'computer': 'Programming',
    'dark': 'Dark',
    'misc': 'Misc',
    'miscellaneous': 'Misc',
    'pun': 'Pun',
    'puns': 'Pun',
    'spooky': 'Spooky',
    'christmas': 'Christmas',
    'holiday': 'Christmas',
    'any': 'Any'
}

def extract_category(request: str) -> str:
    """Extract category from natural language request."""
    request = request.lower()
    
    # Check for explicit category mentions
    for keyword, category in CATEGORY_MAPPINGS.items():
        if keyword in request:
            return category
    
    # Check for common patterns
    if re.search(r'(tell|give|share|want).*(joke|jokes)', request):
        return 'Any'
    
    return 'Any'

@app.get("/")
async def root():
    return {"message": "Welcome to Joke Search API"}

@app.post("/api/ask")
async def ask_for_joke(joke_request: JokeRequest):
    """Handle natural language requests for jokes."""
    try:
        category = extract_category(joke_request.request)
        response = requests.get(f"https://v2.jokeapi.dev/joke/{category}")
        response.raise_for_status()
        joke_data = response.json()
        
        # Format the response based on joke type
        if joke_data.get('type') == 'twopart':
            return {
                "category": joke_data['category'],
                "setup": joke_data['setup'],
                "delivery": joke_data['delivery'],
                "is_safe": joke_data['safe']
            }
        else:
            return {
                "category": joke_data['category'],
                "joke": joke_data['joke'],
                "is_safe": joke_data['safe']
            }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching joke")

@app.get("/api/joke/{joke_id}", response_model=JokeResponse)
async def get_joke(joke_id: int):
    try:
        response = requests.get(f"https://v2.jokeapi.dev/joke/Any?idRange={joke_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail="Joke not found")

@app.get("/api/search")
async def search_joke(query: str, category: Optional[str] = None):
    try:
        # Build the URL with parameters
        base_url = "https://v2.jokeapi.dev/joke/"
        category = category or "Any"
        url = f"{base_url}{category}?contains={query}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error searching for joke")

@app.get("/api/categories")
async def get_categories():
    try:
        response = requests.get("https://v2.jokeapi.dev/categories")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching categories")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 