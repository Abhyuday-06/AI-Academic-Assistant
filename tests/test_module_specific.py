"""
Test script for module-specific question generation
"""
import asyncio
from app.agents.question_generator import question_generator
from app.models import QuestionGenerationRequest, TestType

async def test_module_specific_generation():
    """Test if question generator properly focuses on selected modules"""
    
    # Create a structured syllabus with clear module divisions
    structured_syllabus = """
Computer Networks Syllabus

Module 1: Introduction to Computer Networks
- Basic networking concepts and terminology
- Network topology types (star, ring, mesh, bus)
- OSI Reference Model - 7 layers and their functions
- TCP/IP Protocol Suite overview
- Network hardware components (routers, switches, hubs)

Module 2: Physical Layer and Data Link Layer
- Physical transmission media (copper, fiber, wireless)
- Data encoding and modulation techniques
- Error detection and correction methods
- Frame synchronization and framing techniques  
- Ethernet protocols and standards
- MAC addresses and ARP protocol

Module 3: Network Layer and Routing
- IP addressing and subnetting concepts
- IPv4 vs IPv6 comparison
- Routing algorithms (distance vector, link state)
- Routing protocols (RIP, OSPF, BGP)
- Network Address Translation (NAT)
- ICMP protocol and network troubleshooting

Module 4: Transport Layer Protocols
- TCP vs UDP comparison and use cases
- Connection establishment and termination
- Flow control and congestion control
- Port numbers and socket programming
- Reliable data transfer mechanisms
- Multiplexing and demultiplexing

Module 5: Application Layer Services
- Domain Name System (DNS) architecture
- Web protocols (HTTP, HTTPS)
- Email protocols (SMTP, POP3, IMAP)
- File transfer protocols (FTP, SFTP)
- Network security protocols (SSL/TLS)
- Network management protocols (SNMP)
"""
    
    print("=== Testing Module-Specific Question Generation ===\n")
    
    # Test 1: Generate questions for only Module 1 and Module 2
    print("Test 1: Generating CAT-1 questions for Module 1 and Module 2 only")
    print("Expected: Questions should focus only on basic concepts and physical/data link layers")
    
    request1 = QuestionGenerationRequest(
        syllabus_text=structured_syllabus,
        test_type=TestType.CAT1,
        modules=["Module 1", "Module 2"]
    )
    
    try:
        result1 = await question_generator.generate_question_paper(request1)
        
        if result1.success:
            print("✅ Generation successful!")
            print(f"Generated {len(result1.question_paper.paper)} questions")
            
            # Analyze which modules the questions cover
            modules_covered = set()
            for question in result1.question_paper.paper:
                for part in question.parts:
                    modules_covered.update(part.module)
            
            print(f"Modules covered in questions: {sorted(modules_covered)}")
            
            # Show first question as example
            if result1.question_paper.paper:
                q1 = result1.question_paper.paper[0]
                print(f"\nExample Question 1:")
                print(f"Text: {q1.parts[0].text}")
                print(f"Module: {q1.parts[0].module}")
            
        else:
            print(f"❌ Generation failed: {result1.message}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Test 2: Generate questions for only Module 3
    print("Test 2: Generating CAT-2 questions for Module 3 only")
    print("Expected: Questions should focus only on network layer and routing")
    
    request2 = QuestionGenerationRequest(
        syllabus_text=structured_syllabus,
        test_type=TestType.CAT2,
        modules=["Module 3"]
    )
    
    try:
        result2 = await question_generator.generate_question_paper(request2)
        
        if result2.success:
            print("✅ Generation successful!")
            print(f"Generated {len(result2.question_paper.paper)} questions")
            
            # Analyze content
            for i, question in enumerate(result2.question_paper.paper, 1):
                part = question.parts[0]
                print(f"Q{i}: {part.text[:100]}... [Module: {part.module}]")
        
        else:
            print(f"❌ Generation failed: {result2.message}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n=== Module Extraction Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_module_specific_generation())