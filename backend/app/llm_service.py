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
            You are an expert AI assistant that deeply analyzes user requests for jokes by understanding the full context, intent, and emotional state of the user.

            Available joke categories: Programming, Dark, Misc, Pun, Spooky, Christmas, Any

            Your task is to perform a comprehensive contextual analysis:

            1. **Context Understanding**: Analyze the full sentence structure, tone, and implied meaning
            2. **Intent Recognition**: Understand what the user is really asking for, not just keywords
            3. **Emotional Analysis**: Detect the user's mood, stress level, or emotional state
            4. **Situational Context**: Consider the context (work, social, holiday, etc.)
            5. **Category Selection**: Choose the most appropriate joke category based on context
            6. **Keyword Extraction**: Identify relevant themes and topics for better joke matching

            **Context Analysis Guidelines:**
            - "I'm having a bad day" → Consider uplifting or relatable humor (Misc, or Dark if they seem to want edgy humor)
            - "I'm stuck debugging code" → Programming jokes with relatable developer experiences
            - "I need something clever" → Pun or witty humor
            - "It's been a stressful week" → Consider stress-relief humor (Misc, or Dark for cathartic humor)
            - "I want to impress my friends" → Clever or impressive humor (Pun, Programming)
            - "I'm feeling festive" → Christmas or celebratory humor
            - "I need a laugh" → Any category, focus on humor quality
            - "Tell me something funny about work" → Programming (if tech work) or Misc (general work)
            - "I'm bored" → Engaging, varied humor (Misc, Programming)
            - "I want something different" → Consider less common categories (Spooky, Dark, Pun)

            **Category Selection Logic:**
            - Programming: Tech work, coding, computers, software, developer life
            - Dark: When user seems to want edgy, cathartic, or boundary-pushing humor
            - Misc: General humor, everyday situations, relatable content
            - Pun: When user wants clever wordplay or intellectual humor
            - Spooky: Halloween, horror themes, supernatural interests
            - Christmas: Holiday cheer, festive mood, seasonal humor
            - Any: When context is unclear or user wants variety

            Return a JSON object with the following structure:
            {
                "category": "string (one of the available categories)",
                "keywords": ["array of relevant keywords and themes"],
                "reasoning": "detailed explanation of your contextual analysis",
                "user_mood": "string describing the user's apparent mood, emotional state, or context",
                "suggested_amount": "number (1-10) of jokes to fetch based on context"
            }

            **Important**: Focus on understanding the user's situation, emotional state, and intent rather than just matching keywords. Consider the broader context of their request.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please analyze this request with full contextual understanding: {user_request}"}
                ],
                temperature=0.4,
                max_tokens=400
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
        Intelligent fallback analysis using enhanced NLP techniques with better context understanding.
        """
        # Extract meaningful words
        words = self._extract_meaningful_words(user_request)
        
        # Enhanced context analysis
        context_analysis = self._analyze_context(user_request, words)
        
        # Calculate scores for each category with context weighting
        category_scores = {}
        for category in self.semantic_groups.keys():
            score = self._calculate_category_score(words, category)
            # Apply context-based adjustments
            context_adjustment = self._get_context_adjustment(category, context_analysis)
            category_scores[category] = score * context_adjustment
        
        # Select best category
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            if category_scores[best_category] > 0:
                category = best_category
            else:
                category = 'Any'
        else:
            category = 'Any'
        
        # Enhanced mood detection with context
        user_mood = self._detect_user_mood_with_context(user_request, words, context_analysis)
        
        # Suggest amount based on context
        suggested_amount = self._suggest_amount_with_context(words, category, user_request, context_analysis)
        
        # Create detailed reasoning
        reasoning = self._generate_contextual_reasoning(user_request, category, context_analysis, words)
        
        return {
            "category": category,
            "keywords": words[:10],  # Return more keywords
            "reasoning": reasoning,
            "user_mood": user_mood,
            "suggested_amount": suggested_amount
        }
    
    def _analyze_context(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Analyze the context of the user request."""
        text_lower = text.lower()
        
        context = {
            'is_question': '?' in text,
            'is_exclamation': '!' in text,
            'has_emotional_words': False,
            'situation': 'general',
            'intensity': 'normal',
            'formality': 'casual'
        }
        
        # Detect emotional context
        emotional_indicators = {
            'stress': ['stress', 'stressed', 'overwhelmed', 'busy', 'tired', 'exhausted'],
            'sadness': ['sad', 'depressed', 'down', 'blue', 'unhappy', 'miserable'],
            'frustration': ['frustrated', 'angry', 'mad', 'annoyed', 'irritated'],
            'excitement': ['excited', 'thrilled', 'amazing', 'awesome', 'fantastic'],
            'boredom': ['bored', 'boring', 'dull', 'monotonous'],
            'celebration': ['celebrate', 'party', 'festive', 'happy', 'joy']
        }
        
        for emotion, indicators in emotional_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                context['has_emotional_words'] = True
                context['situation'] = emotion
                break
        
        # Detect intensity
        intensity_words = {
            'high': ['really', 'very', 'extremely', 'super', 'incredibly'],
            'low': ['just', 'only', 'barely', 'hardly', 'slightly']
        }
        
        for intensity, indicators in intensity_words.items():
            if any(indicator in text_lower for indicator in indicators):
                context['intensity'] = intensity
                break
        
        # Detect formality
        formal_indicators = ['please', 'kindly', 'would you', 'could you']
        if any(indicator in text_lower for indicator in formal_indicators):
            context['formality'] = 'formal'
        
        return context
    
    def _get_context_adjustment(self, category: str, context: Dict[str, Any]) -> float:
        """Get context-based adjustment for category scoring."""
        adjustment = 1.0
        
        # Emotional context adjustments
        if context['situation'] == 'stress':
            if category in ['Misc', 'Programming']:
                adjustment *= 1.3  # Relatable humor for stress relief
            elif category == 'Dark':
                adjustment *= 1.2  # Cathartic humor
        elif context['situation'] == 'sadness':
            if category in ['Misc', 'Christmas']:
                adjustment *= 1.4  # Uplifting humor
            elif category == 'Dark':
                adjustment *= 1.1  # Cathartic humor
        elif context['situation'] == 'frustration':
            if category in ['Programming', 'Misc']:
                adjustment *= 1.3  # Relatable humor
        elif context['situation'] == 'excitement':
            if category in ['Pun', 'Programming']:
                adjustment *= 1.2  # Clever humor
        elif context['situation'] == 'boredom':
            if category in ['Misc', 'Programming', 'Pun']:
                adjustment *= 1.3  # Engaging humor
        elif context['situation'] == 'celebration':
            if category == 'Christmas':
                adjustment *= 1.5  # Festive humor
            elif category in ['Misc', 'Pun']:
                adjustment *= 1.2  # Fun humor
        
        # Intensity adjustments
        if context['intensity'] == 'high':
            adjustment *= 1.2  # More jokes for high intensity
        elif context['intensity'] == 'low':
            adjustment *= 0.8  # Fewer jokes for low intensity
        
        return adjustment
    
    def _detect_user_mood_with_context(self, text: str, words: List[str], context: Dict[str, Any]) -> str:
        """Enhanced mood detection with context analysis."""
        # Start with keyword-based mood detection
        base_mood = self._detect_user_mood(words)
        
        # Override with context-based mood if context is stronger
        if context['has_emotional_words']:
            situation_mood_map = {
                'stress': 'stressed',
                'sadness': 'sad',
                'frustration': 'frustrated',
                'excitement': 'excited',
                'boredom': 'bored',
                'celebration': 'happy'
            }
            return situation_mood_map.get(context['situation'], base_mood)
        
        return base_mood
    
    def _suggest_amount_with_context(self, words: List[str], category: str, original_text: str, context: Dict[str, Any]) -> int:
        """Enhanced amount suggestion with context consideration."""
        base_amount = self._suggest_amount(words, category, original_text)
        
        # Context-based adjustments
        if context['intensity'] == 'high':
            base_amount = min(10, base_amount + 2)
        elif context['intensity'] == 'low':
            base_amount = max(1, base_amount - 1)
        
        if context['has_emotional_words']:
            if context['situation'] in ['stress', 'sadness', 'frustration']:
                base_amount = min(10, base_amount + 1)  # More jokes for emotional relief
            elif context['situation'] == 'boredom':
                base_amount = min(10, base_amount + 2)  # More jokes to combat boredom
        
        return base_amount
    
    def _generate_contextual_reasoning(self, user_request: str, category: str, context: Dict[str, Any], words: List[str]) -> str:
        """Generate detailed reasoning based on context analysis."""
        reasoning_parts = []
        
        # Base reasoning
        reasoning_parts.append(f"Selected '{category}' category based on contextual analysis.")
        
        # Context-specific reasoning
        if context['has_emotional_words']:
            reasoning_parts.append(f"Detected {context['situation']} context - suggesting appropriate humor type.")
        
        if context['intensity'] != 'normal':
            reasoning_parts.append(f"Request intensity: {context['intensity']} - adjusted joke quantity accordingly.")
        
        # Keyword reasoning
        if words:
            top_keywords = words[:5]
            reasoning_parts.append(f"Key themes identified: {', '.join(top_keywords)}")
        
        # Formality reasoning
        if context['formality'] == 'formal':
            reasoning_parts.append("Formal request detected - focusing on appropriate humor.")
        
        return " ".join(reasoning_parts)
    
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
            You are a friendly, empathetic AI assistant that provides jokes with personalized context. 
            
            Your task is to create a brief, contextual response that:
            1. Acknowledges the user's specific situation, mood, or request
            2. Shows understanding of their context
            3. Introduces the jokes naturally and appropriately
            4. Maintains a warm, supportive tone
            
            **Context Guidelines:**
            - If user is stressed/tired: Offer stress relief and understanding
            - If user is sad: Provide uplifting, supportive context
            - If user is bored: Make it engaging and exciting
            - If user is excited: Match their enthusiasm
            - If user is frustrated: Offer relatable, cathartic humor
            - If user is celebrating: Match the festive mood
            - If user is asking for work-related humor: Acknowledge the work context
            - If user wants clever humor: Emphasize the wit and intelligence
            
            Keep your response concise (1-2 sentences) and conversational.
            Don't repeat the jokes - just provide personalized context for them.
            Be empathetic and understanding of the user's situation.
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
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response context: {e}")
            return f"Here are some jokes based on your request: '{user_request}'" 