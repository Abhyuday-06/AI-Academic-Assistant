import openai
from typing import Dict, Any, Optional
import asyncio
import structlog
from app.utils.config import settings

logger = structlog.get_logger()


class OpenAIClient:
    """OpenAI client wrapper for the application"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, default_model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or settings.openai_api_key
        self.default_model = default_model
        # OpenRouter (and others) compatible instantiation
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
    
    async def generate_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_message: Optional[str] = None
    ) -> str:
        """Generate completion using OpenAI API"""
        model_to_use = model or self.default_model
        
        # Log which model is being used
        logger.info(f"Generating completion using model: {model_to_use}")
        print(f"\n[DEBUG] Generative AI Request Started")
        print(f"[DEBUG] Provider URL: {self.client.base_url}")
        print(f"[DEBUG] Model: {model_to_use}")
        
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = await self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            print(f"[DEBUG] Request Successful")
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"[DEBUG] Request Failed: {str(e)}")
            logger.error(f"OpenAI API error with model {model_to_use}", error=str(e))
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def parse_notes_with_openai(self, content: str, extract_keywords: bool = True, 
                                    extract_concepts: bool = True, extract_questions: bool = False) -> Dict[str, Any]:
        """Parse notes using OpenAI"""
        system_message = """You are an expert academic assistant specialized in parsing and analyzing educational content.
        Your task is to analyze the provided content and extract structured information."""
        
        prompt_parts = [
            f"Please analyze the following content and provide a structured response:",
            f"\nContent: {content}",
            "\nPlease provide the following analysis:"
        ]
        
        if extract_keywords:
            prompt_parts.append("1. Extract 5-10 important keywords with importance scores (0.0-1.0)")
        
        if extract_concepts:
            prompt_parts.append("2. Identify key concepts with definitions and related terms")
        
        if extract_questions:
            prompt_parts.append("3. Generate 3-5 study questions with different difficulty levels")
        
        prompt_parts.append("\nFormat your response as a clear, structured analysis.")
        
        prompt = "\n".join(prompt_parts)
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=1500,
            temperature=0.3
        )
        
        return {"parsed_content": response}
    
    async def summarize_with_openai(self, content: str, summary_type: str = "comprehensive",
                                  max_length: int = 500, focus_areas: Optional[list] = None) -> Dict[str, Any]:
        """Summarize content using OpenAI"""
        system_message = f"""You are an expert summarization assistant. Create a {summary_type} summary 
        of the provided content in approximately {max_length} words."""
        
        prompt_parts = [
            f"Please create a {summary_type} summary of the following content:",
            f"\nContent: {content}",
            f"\nSummary requirements:",
            f"- Type: {summary_type}",
            f"- Maximum length: {max_length} words",
        ]
        
        if focus_areas:
            prompt_parts.append(f"- Focus on these areas: {', '.join(focus_areas)}")
        
        prompt_parts.append("\nProvide a clear, concise summary that captures the main points.")
        
        prompt = "\n".join(prompt_parts)
        
        response = await self.generate_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=max_length + 200,
            temperature=0.3
        )
        
        return {"summary": response}


# Global OpenAI client instance
openai_client = OpenAIClient()
