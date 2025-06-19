import os
import openai
from typing import Dict, Any, Optional, List, Tuple
import json
import re
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMService:
    """Service for handling LLM interactions to understand user requests."""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
        self._initialize_nlp_data()
    
    def _initialize_client(self):
        """Initialize OpenAI client only if API key is available."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.client = openai.OpenAI(api_key=api_key)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.client = None
        else:
            print("OpenAI API key not found. LLM features will use fallback mode.")
            self.client = None
    
    def _initialize_nlp_data(self):
        """Initialize NLP data for intelligent keyword extraction."""
        # Semantic word groups for better understanding
        self.semantic_groups = {
            'programming': {
                'direct': ['programming', 'programmer', 'code', 'computer', 'software', 'developer', 'coding', 'tech'],
                'related': ['algorithm', 'bug', 'debug', 'function', 'variable', 'database', 'server', 'api', 'git', 'terminal'],
                'context': ['work', 'office', 'computer', 'laptop', 'coding', 'development', 'project']
            },
            'dark': {
                'direct': ['dark', 'black', 'morbid', 'twisted', 'disturbing'],
                'related': ['death', 'sad', 'depressing', 'gloomy', 'moody', 'cynical', 'pessimistic'],
                'context': ['feeling', 'mood', 'emotion', 'sad', 'depressed', 'angry', 'frustrated']
            },
            'misc': {
                'direct': ['misc', 'miscellaneous', 'general', 'random', 'various'],
                'related': ['fun', 'funny', 'humorous', 'hilarious', 'entertaining', 'amusing', 'comedy'],
                'context': ['laugh', 'smile', 'happy', 'joy', 'entertainment', 'fun']
            },
            'pun': {
                'direct': ['pun', 'puns', 'wordplay', 'play', 'words'],
                'related': ['clever', 'smart', 'witty', 'intelligent', 'word', 'language', 'double', 'meaning'],
                'context': ['clever', 'smart', 'intelligent', 'witty', 'wordplay', 'language']
            },
            'spooky': {
                'direct': ['spooky', 'scary', 'horror', 'frightening', 'creepy'],
                'related': ['ghost', 'monster', 'haunted', 'night', 'dark', 'shadow', 'mystery'],
                'context': ['halloween', 'night', 'dark', 'scary', 'fear', 'mystery']
            },
            'christmas': {
                'direct': ['christmas', 'holiday', 'festive', 'xmas'],
                'related': ['santa', 'gift', 'tree', 'snow', 'winter', 'cheer', 'joy', 'family'],
                'context': ['holiday', 'celebration', 'family', 'gift', 'winter', 'december']
            }
        }
        
        # Stop words for filtering
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours',
            'give', 'get', 'want', 'need', 'tell', 'show', 'make', 'let', 'help',
            'some', 'any', 'all', 'every', 'each', 'much', 'more',
            'most', 'other', 'another', 'such', 'what', 'which', 'who', 'whom',
            'whose', 'where', 'when', 'why', 'how', 'if', 'then', 'else', 'than',
            'too', 'also', 'even', 'still', 'again',
            'here', 'there', 'now', 'then', 'so', 'up', 'down', 'out', 'off',
            'over', 'under', 'again', 'further', 'then', 'once'
        }
    
    def _is_llm_available(self) -> bool:
        """Check if LLM is available for use."""
        return self.client is not None
    
    def _extract_meaningful_words(self, text: str) -> List[str]:
        """Extract meaningful words using NLP techniques."""
        # Clean and normalize text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter out stop words and very short/long words
        meaningful_words = []
        for word in words:
            if (word not in self.stop_words and 
                len(word) >= 2 and 
                len(word) <= 15 and
                word.isalpha()):
                meaningful_words.append(word)
        
        return meaningful_words
    
    def _calculate_category_score(self, words: List[str], category: str) -> float:
        """Calculate a score for how well words match a category."""
        if category not in self.semantic_groups:
            return 0.0
        
        category_data = self.semantic_groups[category]
        score = 0.0
        
        # Direct matches get highest score
        for word in words:
            if word in category_data['direct']:
                score += 3.0
            elif word in category_data['related']:
                score += 2.0
            elif word in category_data['context']:
                score += 1.0
        
        # Bonus for multiple matches
        if score > 0:
            score += len([w for w in words if w in category_data['direct'] + category_data['related']]) * 0.5
        
        return score
    
    def _detect_user_mood(self, words: List[str]) -> str:
        """Detect user mood from keywords."""
        mood_indicators = {
            'happy': ['fun', 'funny', 'happy', 'joy', 'cheer', 'laugh', 'smile', 'good', 'great'],
            'sad': ['sad', 'depressed', 'gloomy', 'moody', 'down', 'blue', 'unhappy'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'irritated'],
            'excited': ['excited', 'thrilled', 'amazing', 'awesome', 'fantastic'],
            'relaxed': ['calm', 'peaceful', 'relaxed', 'chill', 'easy'],
            'stressed': ['stressed', 'worried', 'anxious', 'nervous', 'tense']
        }
        
        mood_scores = {}
        for mood, indicators in mood_indicators.items():
            score = sum(1 for word in words if word in indicators)
            if score > 0:
                mood_scores[mood] = score
        
        if mood_scores:
            return max(mood_scores, key=mood_scores.get)
        return "neutral"
    
    def _suggest_amount(self, words: List[str], category: str, original_text: str = "") -> int:
        """Suggest number of jokes based on request intensity and context."""
        # Base intensity from explicit words
        intensity = 3  # default
        
        # Check for explicit quantity indicators
        quantity_indicators = {
            'many': 6, 'lots': 6, 'bunch': 5, 'several': 4, 'few': 2, 
            'couple': 2, 'one': 1, 'single': 1, 'two': 2, 'three': 3,
            'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
            'nine': 9, 'ten': 10
        }
        
        # Check for intensity modifiers
        intensity_modifiers = {
            'really': 2, 'very': 2, 'super': 2, 'extremely': 2,
            'just': -1, 'only': -1, 'barely': -1, 'hardly': -1
        }
        
        # Check for mood-based adjustments
        mood_adjustments = {
            'happy': 1, 'excited': 2, 'thrilled': 2, 'amazing': 1,
            'sad': 1, 'depressed': 1, 'angry': 1, 'frustrated': 1,
            'relaxed': -1, 'calm': -1, 'peaceful': -1
        }
        
        # Use both filtered words and original text for better detection
        all_words = words + original_text.lower().split()
        
        # Find explicit quantity
        for word in all_words:
            if word in quantity_indicators:
                intensity = quantity_indicators[word]
                break
        
        # Apply intensity modifiers
        modifier = 0
        for word in all_words:
            if word in intensity_modifiers:
                modifier += intensity_modifiers[word]
        
        # Apply mood adjustments
        for word in all_words:
            if word in mood_adjustments:
                modifier += mood_adjustments[word]
        
        # Apply category-specific adjustments
        category_adjustments = {
            'Programming': 1,  # Programming jokes work well in groups
            'Dark': 1,         # Dark humor often works better with variety
            'Misc': 0,         # Misc is neutral
            'Pun': -1,         # Puns can be overwhelming in large numbers
            'Spooky': 0,       # Spooky is neutral
            'Christmas': 1,    # Christmas jokes are festive
            'Any': 0           # Any is neutral
        }
        
        category_modifier = category_adjustments.get(category, 0)
        
        # Calculate final amount
        final_amount = intensity + modifier + category_modifier
        
        # Ensure reasonable bounds
        final_amount = max(1, min(final_amount, 10))
        
        return final_amount
    
    async def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """
        Use LLM to analyze user request and extract relevant information for joke fetching.
        
        Args:
            user_request: The natural language request from the user
            
        Returns:
            Dictionary containing extracted parameters for joke API
        """
        if not self._is_llm_available():
            return self._fallback_analysis(user_request)
        
        try:
            system_prompt = """
            You are a helpful AI assistant that analyzes user requests for jokes and extracts relevant information to fetch appropriate jokes from an API.
            
            Available joke categories: Programming, Dark, Misc, Pun, Spooky, Christmas, Any
            
            Your task is to:
            1. Understand the user's intent and mood
            2. Determine the most appropriate joke category
            3. Extract any specific keywords or themes
            4. Reason about the context and user preferences
            
            Return a JSON object with the following structure:
            {
                "category": "string (one of the available categories)",
                "keywords": ["array of relevant keywords"],
                "reasoning": "string explaining your analysis",
                "user_mood": "string describing the user's apparent mood or context",
                "suggested_amount": "number (1-10) of jokes to fetch"
            }
            
            Be thoughtful in your analysis. Consider:
            - If someone asks for "programming jokes", use Programming category
            - If someone mentions feeling sad, consider Dark or Misc categories
            - If someone wants holiday cheer, consider Christmas category
            - If someone asks for wordplay, use Pun category
            - If the request is vague, use Any category
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this request: {user_request}"}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            # Extract and parse the JSON response
            content = response.choices[0].message.content
            try:
                # Try to extract JSON from the response
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start != -1 and json_end != 0:
                    json_str = content[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback if no JSON found
                    result = self._fallback_analysis(user_request)
                
                return result
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return self._fallback_analysis(user_request)
                
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            return self._fallback_analysis(user_request)
    
    def _fallback_analysis(self, user_request: str) -> Dict[str, Any]:
        """
        Intelligent fallback analysis using NLP techniques.
        """
        # Extract meaningful words
        words = self._extract_meaningful_words(user_request)
        
        # Calculate scores for each category
        category_scores = {}
        for category in self.semantic_groups.keys():
            score = self._calculate_category_score(words, category)
            category_scores[category] = score
        
        # Select best category
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                category = best_category
            else:
                category = 'Any'
        else:
            category = 'Any'
        
        # Detect user mood
        user_mood = self._detect_user_mood(words)
        
        # Suggest amount
        suggested_amount = self._suggest_amount(words, category, user_request)
        
        # Create reasoning
        top_keywords = words[:5] if words else []
        reasoning = f"Intelligent analysis: Selected '{category}' category based on semantic analysis of keywords: {', '.join(top_keywords)}"
        
        return {
            "category": category,
            "keywords": words[:10],  # Return more keywords
            "reasoning": reasoning,
            "user_mood": user_mood,
            "suggested_amount": suggested_amount
        }
    
    async def generate_response_context(self, user_request: str, jokes_data: list) -> str:
        """
        Use LLM to generate contextual response based on user request and fetched jokes.
        
        Args:
            user_request: Original user request
            jokes_data: List of jokes fetched from API
            
        Returns:
            Contextual response string
        """
        if not self._is_llm_available():
            return f"Here are some jokes based on your request: '{user_request}'"
        
        try:
            system_prompt = """
            You are a friendly AI assistant that provides jokes with context. 
            Based on the user's original request and the jokes provided, create a brief, 
            friendly response that acknowledges their request and presents the jokes naturally.
            
            Keep your response concise (1-2 sentences) and conversational.
            Don't repeat the jokes - just provide context for them.
            """
            
            jokes_text = "\n".join([
                f"Joke {i+1}: {joke.get('setup', joke.get('joke', ''))} {joke.get('delivery', '')}"
                for i, joke in enumerate(jokes_data)
            ])
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User request: {user_request}\n\nJokes:\n{jokes_text}"}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response context: {e}")
            return f"Here are some jokes based on your request: '{user_request}'" 