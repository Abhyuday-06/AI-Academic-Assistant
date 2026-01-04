from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum
import re


class AgentType(str, Enum):
    NOTES_PARSER = "notes_parser"
    SUMMARIZER = "summarizer"


class FileFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"


class NotesParseRequest(BaseModel):
    """Request model for parsing notes"""
    content: str = Field(..., min_length=1, max_length=50000, description="Content to parse")
    file_format: Optional[FileFormat] = Field(default=FileFormat.TXT, description="Format of the input content")
    extract_keywords: bool = Field(default=True, description="Whether to extract keywords")
    extract_concepts: bool = Field(default=True, description="Whether to extract concepts")
    extract_questions: bool = Field(default=False, description="Whether to generate study questions")
    
    @field_validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty or only whitespace')
        return v.strip()


class SummarizeRequest(BaseModel):
    """Request model for summarizing content"""
    content: str = Field(..., min_length=1, max_length=100000, description="Content to summarize")
    summary_type: str = Field(default="comprehensive", description="Type of summary: bullet_points, comprehensive, abstract")
    max_length: int = Field(default=500, ge=50, le=2000, description="Maximum length of summary in words")
    focus_areas: Optional[List[str]] = Field(default=None, description="Specific areas to focus on")
    include_examples: bool = Field(default=False, description="Whether to include examples in summary")
    
    @field_validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty or only whitespace')
        return v.strip()
    
    @field_validator('summary_type')
    def validate_summary_type(cls, v):
        allowed_types = ["bullet_points", "comprehensive", "abstract", "key_points"]
        if v not in allowed_types:
            raise ValueError(f'Summary type must be one of: {", ".join(allowed_types)}')
        return v


class KeywordExtraction(BaseModel):
    """Model for extracted keywords"""
    keyword: str
    importance_score: float = Field(ge=0.0, le=1.0)
    context: Optional[str] = None


class ConceptExtraction(BaseModel):
    """Model for extracted concepts"""
    concept: str
    definition: Optional[str] = None
    related_terms: List[str] = Field(default_factory=list)
    importance_score: float = Field(ge=0.0, le=1.0)


class StudyQuestion(BaseModel):
    """Model for generated study questions"""
    question: str
    difficulty_level: str = Field(description="easy, medium, hard")
    question_type: str = Field(description="multiple_choice, short_answer, essay")
    suggested_answer: Optional[str] = None


class NotesParseResponse(BaseModel):
    """Response model for parsed notes"""
    success: bool
    message: str
    parsed_content: str
    keywords: List[KeywordExtraction] = Field(default_factory=list)
    concepts: List[ConceptExtraction] = Field(default_factory=list)
    study_questions: List[StudyQuestion] = Field(default_factory=list)
    processing_time: float
    agent_used: str


class SummaryResponse(BaseModel):
    """Response model for summarized content"""
    success: bool
    message: str
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float
    key_points: List[str] = Field(default_factory=list)
    processing_time: float
    agent_used: str


class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str
    agents_status: Dict[str, str]


# Question Paper Generation Models

class TestType(str, Enum):
    """Test types supported by the question generator"""
    CAT1 = "CAT-1"
    CAT2 = "CAT-2"
    FAT = "FAT"


class QuestionPart(BaseModel):
    """Model for a part of a question (subdivision)"""
    label: Optional[str] = Field(None, description="Part label like 'a', 'b', 'c' or None if no parts")
    marks: int = Field(..., ge=1, le=10, description="Marks for this part")
    text: str = Field(..., min_length=10, description="Question text")
    module: List[str] = Field(..., description="Module(s) this part covers")


class Question(BaseModel):
    """Model for a single question"""
    q_no: int = Field(..., ge=1, description="Question number")
    marks: int = Field(..., ge=1, le=10, description="Total marks for this question")
    parts: List[QuestionPart] = Field(..., min_items=1, description="Question parts/subdivisions")
    instructions: Optional[str] = Field(None, description="Special instructions for this question")


class QuestionPaperMetadata(BaseModel):
    """Metadata for the question paper"""
    title: str = Field(..., min_length=1, description="Title of the question paper")
    test_type: TestType = Field(..., description="Type of test")
    modules: List[str] = Field(..., min_items=1, description="Modules covered")
    total_marks: int = Field(..., ge=1, description="Total marks for the paper")
    notes: Optional[str] = Field(None, description="Additional notes")


class QuestionPaperValidation(BaseModel):
    """Validation results for the question paper"""
    total_marks_check: int = Field(..., description="Calculated total marks")
    unique_questions: bool = Field(..., description="Whether all questions are unique")


class GeneratedQuestionPaper(BaseModel):
    """Complete generated question paper"""
    metadata: QuestionPaperMetadata
    paper: List[Question]
    validation: QuestionPaperValidation


class QuestionGenerationRequest(BaseModel):
    """Request model for generating question papers"""
    syllabus_text: str = Field(..., min_length=10, description="Syllabus content")
    test_type: TestType = Field(..., description="Type of test to generate")
    modules: List[str] = Field(..., min_items=1, max_items=10, description="Selected modules (1-10)")
    
    @field_validator('modules')
    def validate_modules(cls, v):
        # Handle both list and comma-separated string inputs
        if isinstance(v, str):
            v = [module.strip() for module in v.split(',') if module.strip()]
        
        validated_modules = []
        for module in v:
            module = module.strip()
            if not module:
                continue
                
            # Normalize case and format - handle "module 1", "Module 1", "MODULE 1"
            module_normalized = re.sub(r'module\s+(\d+)', r'Module \1', module, flags=re.IGNORECASE)
            
            # Also handle just numbers like "1", "2", etc.
            if re.match(r'^\d+$', module):
                module_normalized = f"Module {module}"
            
            # Check if module follows "Module X" format where X is 1-10
            if not re.match(r'^Module\s+([1-9]|10)$', module_normalized):
                raise ValueError(f'Invalid module: {module}. Must be Module 1 through Module 10')
            
            validated_modules.append(module_normalized)
        
        if not validated_modules:
            raise ValueError('At least one module must be selected')
        
        return validated_modules


class QuestionGenerationResponse(BaseModel):
    """Response model for question paper generation"""
    success: bool
    message: str
    question_paper: Optional[GeneratedQuestionPaper] = None
    processing_time: float
    agent_used: str
