import structlog
from typing import Dict, Any, Optional, List
from app.utils.config import settings
from app.utils.openai_client import OpenAIClient

logger = structlog.get_logger()

class HybridClient:
    """
    Hybrid client that prioritizes OpenRouter (Mimo v2 Flash) and falls back to local Ollama (Mistral).
    Both connections use the OpenAI SDK.
    """
    
    def __init__(self):
        # Initialize OpenRouter client
        self.openrouter_client = OpenAIClient(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            default_model=settings.openrouter_model
        )
        
        # Initialize Ollama client using OpenAI SDK compatibility
        # Ollama endpoint usually defaults to localhost:11434/v1 for OpenAI compatibility
        self.ollama_client = OpenAIClient(
            api_key="ollama", # API key can be anything for local Ollama
            base_url=settings.ollama_base_url,
            default_model=settings.ollama_model
        )

    async def parse_notes(self, content: str, extract_keywords: bool = True, 
                         extract_concepts: bool = True, extract_questions: bool = False) -> Dict[str, Any]:
        """
        Parse notes using Hybrid approach.
        Tries OpenRouter first, falls back to Ollama.
        """
        try:
            logger.info("Attempting to parse notes with OpenRouter", model=self.openrouter_client.default_model)
            return await self.openrouter_client.parse_notes_with_openai(
                content=content,
                extract_keywords=extract_keywords,
                extract_concepts=extract_concepts,
                extract_questions=extract_questions
            )
        except Exception as e:
            logger.warning(f"OpenRouter parsing failed (model: {self.openrouter_client.default_model}), falling back to local Ollama (model: {self.ollama_client.default_model})", error=str(e))
            try:
                # Fallback to Ollama using OpenAI SDK method
                return await self.ollama_client.parse_notes_with_openai(
                    content=content,
                    extract_keywords=extract_keywords,
                    extract_concepts=extract_concepts,
                    extract_questions=extract_questions
                )
            except Exception as e2:
                logger.error("Both OpenRouter and Ollama parsing failed", error_primary=str(e), error_secondary=str(e2))
                raise e2

    async def summarize(self, content: str, summary_type: str = "comprehensive",
                       max_length: int = 500, focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Summarize content using Hybrid approach.
        Tries OpenRouter first, falls back to Ollama.
        """
        try:
            logger.info("Attempting to summarize with OpenRouter", model=self.openrouter_client.default_model)
            return await self.openrouter_client.summarize_with_openai(
                content=content,
                summary_type=summary_type,
                max_length=max_length,
                focus_areas=focus_areas
            )
        except Exception as e:
            logger.warning(f"OpenRouter summarization failed (model: {self.openrouter_client.default_model}), falling back to local Ollama (model: {self.ollama_client.default_model})", error=str(e))
            try:
                # Fallback to Ollama using OpenAI SDK method
                return await self.ollama_client.summarize_with_openai(
                    content=content,
                    summary_type=summary_type,
                    max_length=max_length,
                    focus_areas=focus_areas
                )
            except Exception as e2:
                logger.error("Both OpenRouter and Ollama summarization failed", error_primary=str(e), error_secondary=str(e2))
                raise e2

    async def generate_completion(self, prompt: str, system_message: Optional[str] = None, 
                                 temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Generate completion using Hybrid approach.
        Tries OpenRouter first, falls back to Ollama.
        """
        try:
            logger.info("Attempting to generate completion with OpenRouter", model=self.openrouter_client.default_model)
            return await self.openrouter_client.generate_completion(
                prompt=prompt,
                model=None, # Use default
                max_tokens=max_tokens,
                temperature=temperature,
                system_message=system_message
            )
        except Exception as e:
            logger.warning(f"OpenRouter generation failed (model: {self.openrouter_client.default_model}), falling back to local Ollama (model: {self.ollama_client.default_model})", error=str(e))
            try:
                # Fallback to Ollama
                return await self.ollama_client.generate_completion(
                    prompt=prompt,
                    system_message=system_message,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            except Exception as e2:
                logger.error("Both OpenRouter and Ollama generation failed", error_primary=str(e), error_secondary=str(e2))
                raise e2

# Global instance
hybrid_client = HybridClient()