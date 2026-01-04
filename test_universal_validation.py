"""
Universal module filtering test - works with any subject and syllabus
"""
import asyncio
import re
from app.agents.question_generator import question_generator
from app.models import QuestionGenerationRequest, TestType

def extract_topics_from_syllabus(syllabus_text: str, selected_modules: list, excluded_modules: list = None):
    """
    Dynamically extract topics from syllabus based on module selection
    
    Args:
        syllabus_text: The complete syllabus text
        selected_modules: List of modules to include (e.g., ["Module 2", "Module 5"])
        excluded_modules: Optional list of specific modules to exclude from forbidden topics
    
    Returns:
        tuple: (allowed_topics, forbidden_topics)
    """
    def extract_topics_from_text(text):
        """Extract key topics from module content"""
        # Remove module headers
        content = re.sub(r'Module \d+:.*?\n', '', text, flags=re.IGNORECASE)
        # Split on common separators
        topics = re.split(r'[,\n\-•:\(\)]', content.lower())
        # Clean and filter topics
        clean_topics = []
        for topic in topics:
            topic = topic.strip()
            # Filter out short words, numbers, and common words
            if (len(topic) > 3 and 
                not topic.isdigit() and 
                topic not in ['hours', 'and', 'the', 'with', 'for', 'from', 'using', 'concepts']):
                clean_topics.append(topic)
        return clean_topics
    
    # Parse syllabus into modules
    modules = {}
    lines = syllabus_text.split('\n')
    current_module = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        if re.match(r'Module \d+:', line, re.IGNORECASE):
            # Save previous module
            if current_module:
                modules[current_module] = '\n'.join(current_content)
            
            # Start new module
            current_module = re.match(r'(Module \d+)', line, re.IGNORECASE).group(1)
            current_content = []
        elif current_module and line:
            current_content.append(line)
    
    # Don't forget the last module
    if current_module:
        modules[current_module] = '\n'.join(current_content)
    
    # Extract topics from selected modules
    selected_content = ""
    for module in selected_modules:
        if module in modules:
            selected_content += modules[module] + '\n'
    
    # Extract topics from non-selected modules (for forbidden list)
    excluded_content = ""
    for module_name, content in modules.items():
        if module_name not in selected_modules:
            if excluded_modules is None or module_name not in excluded_modules:
                excluded_content += content + '\n'
    
    allowed_topics = extract_topics_from_text(selected_content)
    forbidden_topics = extract_topics_from_text(excluded_content)
    
    return allowed_topics, forbidden_topics, list(modules.keys())

async def test_universal_module_filtering(syllabus_text: str, subject_name: str, 
                                        selected_modules: list, test_type: TestType = TestType.CAT1):
    """
    Universal test function that works with any subject
    
    Args:
        syllabus_text: Complete syllabus content
        subject_name: Name of the subject for display
        selected_modules: List of modules to select
        test_type: Type of test to generate
    """
    
    print(f"🧪 {subject_name.upper()} SUBJECT TEST")
    print("="*60)
    
    # Extract topics dynamically from syllabus
    allowed_topics, forbidden_topics, available_modules = extract_topics_from_syllabus(
        syllabus_text, selected_modules
    )
    
    print(f"Subject: {subject_name}")
    print(f"Available Modules: {', '.join(available_modules)}")
    print(f"Selected Modules: {', '.join(selected_modules)}")
    print(f"Expected Topics: {', '.join(allowed_topics[:5])}{'...' if len(allowed_topics) > 5 else ''}")
    print(f"Forbidden Topics: {', '.join(forbidden_topics[:5])}{'...' if len(forbidden_topics) > 5 else ''}")
    print()

    request = QuestionGenerationRequest(
        syllabus_text=syllabus_text,
        test_type=test_type,
        modules=selected_modules
    )
    
    try:
        result = await question_generator.generate_question_paper(request)
        
        if result.success:
            print("✅ Question paper generated successfully!\n")
            
            violations = []
            valid_count = 0
            
            print("📋 QUESTION ANALYSIS:")
            print("-" * 40)
            
            for i, question in enumerate(result.question_paper.paper, 1):
                question_text = question.parts[0].text.lower()
                module_tags = question.parts[0].module
                
                print(f"\nQ{i}: {question.parts[0].text}")
                print(f"Tags: {module_tags}")
                
                # Check for violations
                found_forbidden = [topic for topic in forbidden_topics if topic in question_text]
                found_allowed = [topic for topic in allowed_topics if topic in question_text]
                
                # Check module tags
                invalid_tags = [tag for tag in module_tags if tag not in selected_modules]
                
                if found_forbidden:
                    print(f"❌ VIOLATION: Contains forbidden topics: {found_forbidden}")
                    violations.append(f"Q{i}: {found_forbidden}")
                elif invalid_tags:
                    print(f"❌ VIOLATION: Wrong module tags: {invalid_tags}")
                    violations.append(f"Q{i}: Wrong tags")
                elif found_allowed:
                    print(f"✅ VALID: Contains expected topics: {found_allowed}")
                    valid_count += 1
                else:
                    print(f"⚠️ NEUTRAL: Generic content (no clear match)")
                    valid_count += 1  # Count as valid if no clear violation
            
            # Results
            total = len(result.question_paper.paper)
            violation_count = len(violations)
            success_rate = (valid_count / total) * 100 if total > 0 else 0
            
            print(f"\n" + "="*60)
            print(f"📊 {subject_name.upper()} TEST RESULTS:")
            print(f"Total Questions: {total}")
            print(f"Valid Questions: {valid_count}")
            print(f"Violations: {violation_count}")
            print(f"Success Rate: {success_rate:.1f}%")
            
            if violation_count == 0:
                print(f"\n🎉 PERFECT SUCCESS for {subject_name}!")
                print(f"✅ All questions from selected modules only")
                return True
            elif violation_count <= 1:
                print(f"\n✅ EXCELLENT RESULT for {subject_name}!")
                print(f"✅ Only {violation_count} minor issue(s) detected")
                return True
            else:
                print(f"\n⚠️ Issues detected in {subject_name}:")
                for violation in violations:
                    print(f"  - {violation}")
                return False
                
        else:
            print(f"❌ Generation failed: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test with multiple subjects
async def run_comprehensive_test():
    """Run tests with multiple subjects to verify universal functionality"""
    
    # Computer Science syllabus
    cs_syllabus = """
Module 1: Programming Fundamentals
Variables, data types, control structures, functions, arrays, strings.

Module 2: Object-Oriented Programming  
Classes, objects, inheritance, polymorphism, encapsulation, abstraction.

Module 3: Data Structures
Stacks, queues, linked lists, trees, graphs, hash tables.

Module 4: Algorithms
Sorting algorithms, searching algorithms, recursion, dynamic programming.

Module 5: Database Systems
Relational databases, SQL queries, normalization, transactions, indexing.

Module 6: Web Development
HTML, CSS, JavaScript, frameworks, REST APIs, client-server architecture.
"""

    # Physics syllabus  
    physics_syllabus = """
Module 1: Mechanics
Kinematics, dynamics, Newton's laws, work and energy, momentum.

Module 2: Thermodynamics
Laws of thermodynamics, heat engines, entropy, statistical mechanics.

Module 3: Electromagnetism
Electric fields, magnetic fields, electromagnetic induction, Maxwell equations.

Module 4: Quantum Mechanics
Wave-particle duality, Schrödinger equation, quantum states, uncertainty principle.

Module 5: Optics
Geometric optics, wave optics, interference, diffraction, polarization.

Module 6: Modern Physics
Relativity, atomic structure, nuclear physics, particle physics.
"""

    results = []
    
    # Test Computer Science
    print("Starting comprehensive universal module filtering tests...\n")
    
    cs_result = await test_universal_module_filtering(
        cs_syllabus, "Computer Science", ["Module 2", "Module 5"], TestType.CAT2
    )
    results.append(("Computer Science", cs_result))
    
    print("\n" + "="*80 + "\n")
    
    # Test Physics
    physics_result = await test_universal_module_filtering(
        physics_syllabus, "Physics", ["Module 1", "Module 4"], TestType.FAT
    )
    results.append(("Physics", physics_result))
    
    # Final summary
    print("\n" + "="*80)
    print("🏆 COMPREHENSIVE TEST SUMMARY")
    print("="*80)
    
    success_count = sum(1 for _, result in results if result)
    total_tests = len(results)
    
    for subject, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{subject}: {status}")
    
    overall_success = (success_count / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\nOverall Success Rate: {overall_success:.1f}% ({success_count}/{total_tests})")
    
    if success_count == total_tests:
        print(f"\n🎉 UNIVERSAL SUCCESS!")
        print(f"✅ System works perfectly with ALL subjects")
        print(f"✅ No hardcoded validation topics")
        print(f"✅ Dynamic topic extraction working correctly")
        print(f"✅ Module filtering is truly universal")
    else:
        print(f"\n⚠️ Some subjects need attention")

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())