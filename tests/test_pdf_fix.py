"""
Test script to verify question paper PDF export formatting fixes
"""
from app.models import GeneratedQuestionPaper, QuestionPaperMetadata, Question, QuestionPart, QuestionPaperValidation, TestType
from app.utils.pdf_exporter import pdf_exporter

def test_question_paper_pdf_fixes():
    """Test PDF export with proper formatting fixes"""
    
    print("Testing Question Paper PDF Export Fixes...")
    
    # Create a sample question paper
    metadata = QuestionPaperMetadata(
        title="CAT-1 Question Paper",
        test_type=TestType.CAT1,
        modules=["Module 1", "Module 2"],
        total_marks=50,
        notes="Generated from Computer Networks syllabus"
    )
    
    questions = [
        Question(
            q_no=1,
            marks=10,
            parts=[
                QuestionPart(
                    label=None,
                    marks=10,
                    text="Explain the OSI model layers and their functions.",
                    module=["Module 1"]
                )
            ],
            instructions=None
        ),
        Question(
            q_no=2,
            marks=10,
            parts=[
                QuestionPart(
                    label=None,
                    marks=10,
                    text="Compare TCP and UDP protocols.",
                    module=["Module 2"]
                )
            ],
            instructions=None
        )
    ]
    
    validation = QuestionPaperValidation(
        total_marks_check=20,
        unique_questions=True
    )
    
    question_paper = GeneratedQuestionPaper(
        metadata=metadata,
        paper=questions[:2],  # Just 2 questions for testing
        validation=validation
    )
    
    # Test 1: Without filename (should show "Unknown Subject")
    print("Test 1: PDF export without filename...")
    pdf_content1 = pdf_exporter.export_question_paper(question_paper, None)
    with open("test_question_paper_no_subject.pdf", "wb") as f:
        f.write(pdf_content1)
    print(f"✅ Generated: test_question_paper_no_subject.pdf ({len(pdf_content1)} bytes)")
    
    # Test 2: With filename (should extract subject name)
    print("Test 2: PDF export with filename...")
    pdf_content2 = pdf_exporter.export_question_paper(question_paper, "Computer_Networks_Syllabus.pdf")
    with open("test_question_paper_with_subject.pdf", "wb") as f:
        f.write(pdf_content2)
    print(f"✅ Generated: test_question_paper_with_subject.pdf ({len(pdf_content2)} bytes)")
    
    # Test 3: Test different test types
    print("Test 3: Testing different test types...")
    for test_type in [TestType.CAT2, TestType.FAT]:
        metadata.test_type = test_type
        question_paper.metadata = metadata
        
        pdf_content = pdf_exporter.export_question_paper(question_paper, f"Operating_Systems_{test_type.value}.pdf")
        filename = f"test_{test_type.value.lower().replace('-', '_')}_paper.pdf"
        
        with open(filename, "wb") as f:
            f.write(pdf_content)
        print(f"✅ Generated: {filename} ({len(pdf_content)} bytes)")
    
    print("\n🎉 All tests completed successfully!")
    print("Check the generated PDF files to verify:")
    print("- Test Type shows 'CAT-1', 'CAT-2', 'FAT' (not TestType.CAT1)")
    print("- Subject name extracted from filename")
    print("- Proper formatting maintained")

if __name__ == "__main__":
    test_question_paper_pdf_fixes()
