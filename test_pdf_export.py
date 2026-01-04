#!/usr/bin/env python3
"""
Test script to verify PDF export functionality
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.agents.academic_agent import academic_agent
from app.models import NotesParseRequest, SummarizeRequest
from app.utils.pdf_exporter import pdf_exporter


async def test_pdf_export():
    """Test PDF export functionality"""
    
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
    print("TESTING PDF EXPORT FUNCTIONALITY")
    print("=" * 60)
    
    # Test 1: Parse and export to PDF
    print("\n1. Testing Parse Results PDF Export...")
    try:
        parse_request = NotesParseRequest(
            content=test_content,
            extract_keywords=True,
            extract_concepts=True,
            extract_questions=True
        )
        
        result = await academic_agent.parse_and_summarize(parse_request)
        
        if result.success:
            pdf_content = pdf_exporter.export_parse_results(result, "test_document.txt")
            
            # Save to file for testing
            filename = "test_parse_results.pdf"
            with open(filename, "wb") as f:
                f.write(pdf_content)
            
            print(f"✅ Parse PDF generated successfully: {filename} ({len(pdf_content)} bytes)")
        else:
            print(f"❌ Parse failed: {result.message}")
            
    except Exception as e:
        print(f"❌ PDF export failed: {str(e)}")
    
    # Test 2: Summary and export to PDF
    print("\n2. Testing Summary Results PDF Export...")
    try:
        summary_request = SummarizeRequest(
            content=test_content,
            summary_type="comprehensive",
            max_length=300
        )
        
        result = await academic_agent.summarize_only(summary_request)
        
        if result.success:
            pdf_content = pdf_exporter.export_summary_results(result, "test_document.txt")
            
            # Save to file for testing
            filename = "test_summary_results.pdf"
            with open(filename, "wb") as f:
                f.write(pdf_content)
            
            print(f"✅ Summary PDF generated successfully: {filename} ({len(pdf_content)} bytes)")
        else:
            print(f"❌ Summary failed: {result.message}")
            
    except Exception as e:
        print(f"❌ PDF export failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("PDF EXPORT TESTING COMPLETE!")
    print("Check the generated PDF files in the current directory.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_pdf_export())
