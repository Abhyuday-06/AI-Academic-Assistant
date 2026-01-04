#!/usr/bin/env python3
"""
Test script for Question Paper Generator
Tests the generation of CAT-1, CAT-2, and FAT question papers
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.agents.question_generator import question_generator
from app.models import QuestionGenerationRequest, TestType
from app.utils.pdf_exporter import pdf_exporter


async def test_question_generation():
    """Test question paper generation functionality"""
    
    # Sample syllabus content
    sample_syllabus = """
    COMPUTER SCIENCE SYLLABUS
    
    Module 1: Introduction to Programming
    - Basic programming concepts
    - Variables, data types, and operators
    - Control structures: if-else, loops
    - Functions and procedures
    - Problem-solving techniques
    
    Module 2: Data Structures
    - Arrays and strings
    - Linked lists: single, double, circular
    - Stacks and queues
    - Trees: binary trees, BST, AVL
    - Graphs and graph algorithms
    
    Module 3: Object-Oriented Programming
    - Classes and objects
    - Inheritance and polymorphism
    - Encapsulation and abstraction
    - Design patterns
    - Exception handling
    
    Module 4: Database Management
    - Relational database concepts
    - SQL queries and operations
    - Normalization and design
    - Transactions and concurrency
    - Database optimization
    
    Module 5: Computer Networks
    - OSI and TCP/IP models
    - Network protocols and services
    - Routing and switching
    - Network security
    - Wireless networks
    """
    
    print("=" * 80)
    print("TESTING QUESTION PAPER GENERATOR")
    print("=" * 80)
    
    # Test different test types
    test_cases = [
        {
            "type": TestType.CAT1,
            "modules": ["Module 1", "Module 2", "Module 3"],
            "title": "CAT-1 Computer Science"
        },
        {
            "type": TestType.CAT2,
            "modules": ["Module 2", "Module 3", "Module 4"],
            "title": "CAT-2 Computer Science"
        },
        {
            "type": TestType.FAT,
            "modules": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"],
            "title": "FAT Computer Science"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['type'].value} Generation...")
        
        try:
            # Create request
            request = QuestionGenerationRequest(
                syllabus_text=sample_syllabus,
                test_type=test_case["type"],
                modules=test_case["modules"],
                title=test_case["title"]
            )
            
            # Generate question paper
            result = await question_generator.generate_question_paper(request)
            
            if result.success:
                qp = result.question_paper
                print(f"✅ Success: {test_case['type'].value}")
                print(f"   📄 Title: {qp.metadata.title}")
                print(f"   📊 Questions: {len(qp.paper)}")
                print(f"   📋 Total Marks: {qp.metadata.total_marks}")
                print(f"   📚 Modules: {', '.join(qp.metadata.modules)}")
                print(f"   ⏱️  Processing Time: {result.processing_time:.2f}s")
                
                # Show sample question
                if qp.paper:
                    sample_q = qp.paper[0]
                    print(f"   📝 Sample Question: Q{sample_q.q_no} - {sample_q.parts[0].text[:100]}...")
                
                # Generate PDF
                try:
                    pdf_content = pdf_exporter.export_question_paper(qp)
                    filename = f"test_{test_case['type'].value.lower()}_question_paper.pdf"
                    
                    with open(filename, "wb") as f:
                        f.write(pdf_content)
                    
                    print(f"   📄 PDF Generated: {filename} ({len(pdf_content)} bytes)")
                    
                except Exception as pdf_error:
                    print(f"   ❌ PDF Generation Failed: {str(pdf_error)}")
                
            else:
                print(f"❌ Failed: {result.message}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 60)
    
    print("\n" + "=" * 80)
    print("QUESTION PAPER GENERATOR TESTING COMPLETE!")
    print("Check the generated PDF files for formatted question papers.")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_question_generation())