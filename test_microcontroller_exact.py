"""
Test with the exact microcontroller syllabus example user mentioned
"""
import asyncio
from app.agents.question_generator import question_generator
from app.models import QuestionGenerationRequest, TestType

async def test_microcontroller_example():
    """Test the exact case user mentioned: Modules 2 and 5 from microcontroller syllabus"""
    
    # The exact syllabus structure user mentioned
    microcontroller_syllabus = """
Module 1: Introduction to Microprocessors
Basic concepts of microprocessors, evolution from 4-bit to 64-bit processors, 
comparison between microprocessors and microcontrollers.

Module 2: Microprocessor Architecture and Interfacing: Intel x86
16-bit Microprocessor: 8086 - Architecture and Addressing modes, Memory Segmentation,
Instruction Set, Assembly Language Processing, Programming with DOS and BIOS function
calls, minimum and maximum mode configuration, Programmable Peripheral Interface
(8255), Programmable Timer Controller (8254), Memory Interface to 8086.

Module 3: Intel 8051 Microcontroller
Architecture of 8051, Pin diagram, Memory organization, Addressing modes,
Instruction set, Assembly language programming, Interrupts and interrupt handling.

Module 4: Advanced Features of 8051
Timers and counters, Serial communication, Power control modes,
Real-time clock implementation, Watchdog timer concepts.

Module 5: I/O Interfacing with Microcontroller 8051
LCD, LED, Keypad, Analog-to-Digital Convertors, Digital-to-Analog Convertors, Sensor with
Signal Conditioning Interface.

Module 6: ARM Architecture and Programming
ARM processor architecture, instruction set, programming model, exception handling,
ARM assembly language programming, thumb instruction set.

Module 7: Embedded System Design
Embedded system components, design methodology, real-time operating systems,
embedded software development, testing and debugging techniques.
"""

    print("=== MICROCONTROLLER SYLLABUS TEST ===\n")
    print("User's issue: Selected Modules 2 and 5 but got ARM processor questions from Module 6")
    print("Expected: Only 8086 architecture (Module 2) and I/O interfacing (Module 5) questions")
    print("Should NOT include: ARM processors, embedded systems, timers, interrupts, etc.\n")

    request = QuestionGenerationRequest(
        syllabus_text=microcontroller_syllabus,
        test_type=TestType.CAT1,
        modules=["Module 2", "Module 5"]
    )
    
    try:
        result = await question_generator.generate_question_paper(request)
        
        if result.success:
            print("✅ Generation successful!\n")
            
            # Dynamically extract topics from syllabus
            def extract_topics_from_module(module_text):
                """Extract key topics from a module's content"""
                import re
                # Remove module header and extract content
                content = re.sub(r'Module \d+:.*?\n', '', module_text, flags=re.IGNORECASE)
                # Split on common separators and clean up
                topics = re.split(r'[,\n\-•]', content.lower())
                # Clean and filter topics
                clean_topics = []
                for topic in topics:
                    topic = topic.strip()
                    if len(topic) > 3 and not any(char.isdigit() for char in topic):
                        clean_topics.append(topic)
                return clean_topics
            
            # Extract allowed topics from selected modules (Module 2 and Module 5)
            selected_modules_text = ""
            other_modules_text = ""
            
            lines = microcontroller_syllabus.split('\n')
            current_module = None
            current_content = []
            
            for line in lines:
                if 'module' in line.lower() and ':' in line:
                    # Save previous module
                    if current_module:
                        content = '\n'.join(current_content)
                        if current_module in ['Module 2', 'Module 5']:
                            selected_modules_text += content + '\n'
                        else:
                            other_modules_text += content + '\n'
                    
                    # Start new module
                    current_module = line.split(':')[0].strip()
                    current_content = []
                elif current_module:
                    current_content.append(line)
            
            # Don't forget the last module
            if current_module:
                content = '\n'.join(current_content)
                if current_module in ['Module 2', 'Module 5']:
                    selected_modules_text += content + '\n'
                else:
                    other_modules_text += content + '\n'
            
            # Extract topics dynamically
            allowed_topics = extract_topics_from_module(selected_modules_text)
            forbidden_topics = extract_topics_from_module(other_modules_text)
            
            violations = []
            valid_questions = []
            
            print("DETAILED QUESTION ANALYSIS:")
            print("-" * 50)
            
            for i, question in enumerate(result.question_paper.paper, 1):
                q_text = question.parts[0].text.lower()
                q_module = question.parts[0].module
                
                print(f"\nQ{i}: {question.parts[0].text}")
                print(f"Module Tag: {q_module}")
                
                # Check for violations
                found_forbidden = []
                found_allowed = []
                
                for topic in forbidden_topics:
                    if topic in q_text:
                        found_forbidden.append(topic)
                
                for topic in allowed_topics:
                    if topic in q_text:
                        found_allowed.append(topic)
                
                # Analyze result
                if found_forbidden:
                    violations.append({
                        'question': i,
                        'forbidden_topics': found_forbidden,
                        'text': question.parts[0].text
                    })
                    print(f"❌ VIOLATION: Contains forbidden topics: {found_forbidden}")
                    print(f"   This suggests content from non-selected modules!")
                
                elif found_allowed:
                    valid_questions.append(i)
                    print(f"✅ VALID: Contains expected topics: {found_allowed}")
                    
                else:
                    print(f"⚠️  UNCLEAR: No clear topic indicators")
                    # Check if it's too generic
                    generic_terms = ["microprocessor", "microcontroller", "programming", "system", "design"]
                    found_generic = [term for term in generic_terms if term in q_text]
                    if found_generic:
                        print(f"   Possibly too generic: {found_generic}")

            # Final verdict
            print("\n" + "="*60)
            print("FINAL RESULTS:")
            print(f"Total Questions: {len(result.question_paper.paper)}")
            print(f"Valid Questions: {len(valid_questions)}")
            print(f"Violations: {len(violations)}")
            
            if violations:
                print("\n❌ CRITICAL VIOLATIONS DETECTED:")
                for violation in violations:
                    print(f"  Q{violation['question']}: {violation['forbidden_topics']}")
                    print(f"    Text: {violation['text']}")
                print(f"\n🚨 SYSTEM STILL HAS MODULE FILTERING ISSUES!")
                print(f"   Questions include content from non-selected modules")
                return False
            else:
                print(f"\n🎉 SUCCESS: All questions are from selected modules only!")
                print(f"   No ARM processor or other forbidden content detected")
                return True
                
        else:
            print(f"❌ Generation failed: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_microcontroller_example())
    if success:
        print(f"\n✅ TEST PASSED: Module filtering is working correctly!")
    else:
        print(f"\n❌ TEST FAILED: Module filtering needs more improvement")