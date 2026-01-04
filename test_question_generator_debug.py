"""
Debug script for question generator to see what Ollama is actually returning
"""
import asyncio
import json
from app.agents.question_generator import question_generator
from app.models import QuestionGenerationRequest, TestType

async def test_question_generator():
    """Test the question generator with a simple request"""
    
    # Create a simple test request
    request = QuestionGenerationRequest(
        syllabus_text="""
        Computer Networks: 
        1. Introduction to networking concepts
        2. OSI Model and TCP/IP stack
        3. Data transmission and protocols
        4. Network topologies and architectures
        5. Routing algorithms and protocols
        """,
        test_type=TestType.CAT1,
        modules=["Module 1", "Module 2"]
    )
    
    try:
        print("Testing question generator...")
        print(f"Request: {request}")
        
        # Generate the prompt to see what we're sending
        prompt = question_generator._create_generation_prompt(request)
        print(f"\nGenerated Prompt:\n{prompt[:500]}...")
        
        # Try to get raw response from Ollama
        raw_response = await question_generator._generate_with_ollama(prompt, request.test_type)
        print(f"\nRaw Ollama Response:\n{raw_response[:1000]}...")
        
        # Try to parse the response
        question_paper = question_generator._parse_and_validate_response(raw_response, request)
        print(f"\nParsed Question Paper: {question_paper}")
        
        # Try the full generation
        result = await question_generator.generate_question_paper(request)
        print(f"\nFinal Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_question_generator())