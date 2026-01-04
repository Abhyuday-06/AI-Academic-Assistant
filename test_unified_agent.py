#!/usr/bin/env python3
"""
Test script to verify the unified academic agent functionality
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.agents.academic_agent import academic_agent
from app.models import NotesParseRequest, SummarizeRequest


async def test_unified_functionality():
    """Test the unified parsing and summarizing functionality"""
    
    # Test content
    test_content = """
    Machine Learning Fundamentals
    
    Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. 
    
    Key concepts include:
    - Supervised learning: Learning with labeled data
    - Unsupervised learning: Finding patterns in unlabeled data  
    - Neural networks: Computing systems inspired by biological neural networks
    - Deep learning: ML with multiple layers of neural networks
    
    Applications:
    - Image recognition and computer vision
    - Natural language processing
    - Recommendation systems
    - Autonomous vehicles
    
    Questions to consider:
    Q: What is the difference between supervised and unsupervised learning?
    Q: How do neural networks process information?
    """
    
    print("=" * 60)
    print("TESTING UNIFIED ACADEMIC AGENT")
    print("=" * 60)
    
    # Test 1: Parse and Summarize (Unified functionality)
    print("\n1. Testing Parse and Summarize (Unified)...")
    parse_request = NotesParseRequest(
        content=test_content,
        extract_keywords=True,
        extract_concepts=True,
        extract_questions=True
    )
    
    try:
        result = await academic_agent.parse_and_summarize(parse_request)
        print(f"✅ Success: {result.success}")
        print(f"📝 Summary Length: {len(result.parsed_content)} chars")
        print(f"🔑 Keywords Found: {len(result.keywords)}")
        print(f"💡 Concepts Found: {len(result.concepts)}")
        print(f"❓ Questions Found: {len(result.study_questions)}")
        print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
        print(f"🤖 Agent Used: {result.agent_used}")
        
        if result.keywords:
            print(f"\nSample Keywords: {', '.join([kw.keyword for kw in result.keywords[:3]])}")
        if result.concepts:
            print(f"Sample Concepts: {', '.join([c.concept for c in result.concepts[:3]])}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: Summarize Only
    print("\n" + "=" * 60)
    print("2. Testing Summarize Only...")
    summarize_request = SummarizeRequest(
        content=test_content,
        summary_type="comprehensive",
        max_length=300
    )
    
    try:
        result = await academic_agent.summarize_only(summarize_request)
        print(f"✅ Success: {result.success}")
        print(f"📝 Summary: {result.summary[:200]}...")
        print(f"📊 Compression: {result.compression_ratio:.2f}")
        print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
        print(f"🤖 Agent Used: {result.agent_used}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: Parse Only (Backward compatibility)
    print("\n" + "=" * 60)
    print("3. Testing Parse Only (Backward Compatibility)...")
    
    try:
        result = await academic_agent.parse_only(parse_request)
        print(f"✅ Success: {result.success}")
        print(f"📝 Parsed Content Length: {len(result.parsed_content)} chars")
        print(f"🔑 Keywords Found: {len(result.keywords)}")
        print(f"💡 Concepts Found: {len(result.concepts)}")
        print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_unified_functionality())
