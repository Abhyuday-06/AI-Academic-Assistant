"""
Simple API test for module-specific question generation
"""
import requests
import json

def test_api_module_specific():
    """Test the API endpoint with module-specific generation"""
    
    # Create test syllabus with clear module divisions
    test_syllabus = """Computer Networks Course

Module 1: Introduction to Networking
- Network types and topologies
- OSI Model layers
- Basic networking hardware

Module 2: Physical and Data Link Layer  
- Transmission media
- Error detection methods
- Ethernet protocols

Module 3: Network Layer and Routing
- IP addressing concepts
- Routing algorithms
- NAT and network troubleshooting

Module 4: Transport Layer
- TCP vs UDP protocols
- Port numbers and sockets
- Flow control mechanisms

Module 5: Application Layer
- DNS and web protocols  
- Email and file transfer
- Network security basics
"""

    url = "http://localhost:8000/generate-question-paper"
    
    # Test 1: Only Module 1 and Module 3
    print("Testing API with Module 1 and Module 3 selection...")
    
    data = {
        'syllabus_text': test_syllabus,
        'test_type': 'CAT-1', 
        'modules': 'Module 1,Module 3'  # Comma-separated as expected by API
    }
    
    try:
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ API call successful!")
                
                # Check which modules are covered
                questions = result['question_paper']['paper']
                modules_found = set()
                
                for question in questions:
                    for part in question['parts']:
                        modules_found.update(part['module'])
                
                print(f"Modules covered: {sorted(modules_found)}")
                
                # Check if questions are module-specific
                print(f"Generated {len(questions)} questions")
                for i, q in enumerate(questions, 1):
                    text_preview = q['parts'][0]['text'][:80] + "..."
                    module = q['parts'][0]['module']
                    print(f"Q{i}: {text_preview} [Module: {module}]")
                    
                if modules_found.issubset({'Module 1', 'Module 3'}):
                    print("✅ SUCCESS: Questions generated only from selected modules!")
                else:
                    print(f"❌ ISSUE: Found questions from unselected modules: {modules_found}")
                    
            else:
                print(f"❌ Generation failed: {result['message']}")
                
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Please start the server first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api_module_specific()