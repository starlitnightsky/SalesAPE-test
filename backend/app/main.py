from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from pydantic import BaseModel
from typing import Optional, List, Union
import re
from app.llm_service import LLMService

app = FastAPI(title="AI-Powered Joke Search API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
llm_service = LLMService()

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

class JokesResponse(BaseModel):
    jokes: List[JokeResponse]
    total: int
    page: int
    has_more: bool

class JokeRequest(BaseModel):
    request: str

class AIAnalysisResponse(BaseModel):
    category: str
    keywords: List[str]
    reasoning: str
    user_mood: str
    suggested_amount: int

# Legacy category mappings (kept for fallback)
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
    """Legacy function - kept for fallback purposes."""
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
    return {"message": "Welcome to AI-Powered Joke Search API"}

@app.post("/api/ask")
async def ask_for_joke(joke_request: JokeRequest, amount: int = Query(1, ge=1, le=10)):
    """Handle natural language requests for jokes using AI analysis."""
    try:
        # Use LLM to analyze the request
        ai_analysis = await llm_service.analyze_request(joke_request.request)
        
        # Use AI-suggested category and amount, but respect user's amount parameter
        category = ai_analysis.get('category', 'Any')
        suggested_amount = min(ai_analysis.get('suggested_amount', 3), amount)
        
        # Fetch jokes from the API
        response = requests.get(f"https://v2.jokeapi.dev/joke/{category}?amount={suggested_amount}")
        response.raise_for_status()
        joke_data = response.json()
        
        if joke_data.get('error'):
            raise HTTPException(status_code=400, detail=joke_data.get('message', 'Error fetching joke'))
        
        # Handle both single joke and multiple jokes response
        jokes = joke_data.get('jokes', [joke_data])
        
        formatted_jokes = []
        for joke in jokes:
            if joke.get('type') == 'twopart':
                formatted_jokes.append({
                    "category": joke['category'],
                    "setup": joke['setup'],
                    "delivery": joke['delivery'],
                    "is_safe": joke['safe']
                })
            else:
                formatted_jokes.append({
                    "category": joke['category'],
                    "joke": joke['joke'],
                    "is_safe": joke['safe']
                })
        
        # Generate contextual response using LLM
        context_response = await llm_service.generate_response_context(joke_request.request, formatted_jokes)
        
        return {
            "jokes": formatted_jokes,
            "total": len(formatted_jokes),
            "page": 1,
            "has_more": False,
            "ai_analysis": ai_analysis,
            "context_response": context_response
        }
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching joke")
    except Exception as e:
        # Fallback to legacy method if LLM fails
        print(f"LLM error, falling back to legacy method: {e}")
        try:
            category = extract_category(joke_request.request)
            response = requests.get(f"https://v2.jokeapi.dev/joke/{category}?amount={amount}")
            response.raise_for_status()
            joke_data = response.json()
            
            if joke_data.get('error'):
                raise HTTPException(status_code=400, detail=joke_data.get('message', 'Error fetching joke'))
            
            jokes = joke_data.get('jokes', [joke_data])
            
            formatted_jokes = []
            for joke in jokes:
                if joke.get('type') == 'twopart':
                    formatted_jokes.append({
                        "category": joke['category'],
                        "setup": joke['setup'],
                        "delivery": joke['delivery'],
                        "is_safe": joke['safe']
                    })
                else:
                    formatted_jokes.append({
                        "category": joke['category'],
                        "joke": joke['joke'],
                        "is_safe": joke['safe']
                    })
            
            return {
                "jokes": formatted_jokes,
                "total": len(formatted_jokes),
                "page": 1,
                "has_more": False,
                "ai_analysis": {
                    "category": category,
                    "keywords": [],
                    "reasoning": "Fallback to legacy keyword matching",
                    "user_mood": "unknown",
                    "suggested_amount": amount
                },
                "context_response": f"Here are some {category} jokes for you!"
            }
        except Exception as fallback_error:
            raise HTTPException(status_code=500, detail="Error fetching joke")

@app.post("/api/analyze")
async def analyze_request(joke_request: JokeRequest) -> AIAnalysisResponse:
    """Analyze a user request using AI without fetching jokes."""
    try:
        analysis = await llm_service.analyze_request(joke_request.request)
        return AIAnalysisResponse(**analysis)
    except Exception as e:
        # Fallback analysis
        fallback = llm_service._fallback_analysis(joke_request.request)
        return AIAnalysisResponse(**fallback)

@app.get("/api/joke/{joke_id}", response_model=JokeResponse)
async def get_joke(joke_id: int):
    try:
        response = requests.get(f"https://v2.jokeapi.dev/joke/Any?idRange={joke_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=404, detail="Joke not found")

@app.get("/api/search")
async def search_joke(
    query: str,
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    amount: int = Query(5, ge=1, le=10)
):
    try:
        # Build the URL with parameters
        base_url = "https://v2.jokeapi.dev/joke/"
        category = category or "Any"
        url = f"{base_url}{category}?contains={query}&amount={amount}"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('error'):
            raise HTTPException(status_code=400, detail=data.get('message', 'Error searching for joke'))
        
        # Handle both single joke and multiple jokes response
        jokes = data.get('jokes', [data])
        
        formatted_jokes = []
        for joke in jokes:
            if joke.get('type') == 'twopart':
                formatted_jokes.append({
                    "category": joke['category'],
                    "setup": joke['setup'],
                    "delivery": joke['delivery'],
                    "is_safe": joke['safe']
                })
            else:
                formatted_jokes.append({
                    "category": joke['category'],
                    "joke": joke['joke'],
                    "is_safe": joke['safe']
                })
        
        return {
            "jokes": formatted_jokes,
            "total": len(formatted_jokes),
            "page": page,
            "has_more": len(formatted_jokes) == amount
        }
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