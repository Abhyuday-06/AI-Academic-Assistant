"""
Question Paper Generator Agent for Academic Assistant
Generates exam question papers based on syllabus content, test type, and selected modules
Follows the QueGenerator_Prompt.docx specifications
"""
import time
import json
import re
from typing import List, Dict, Any, Optional
import structlog
from app.utils.ollama_client import ollama_client
from app.models import (
    QuestionGenerationRequest, QuestionGenerationResponse, GeneratedQuestionPaper,
    QuestionPaperMetadata, Question, QuestionPart, QuestionPaperValidation,
    TestType
)

logger = structlog.get_logger()


class QuestionPaperGenerator:
    """Agent for generating academic question papers using Ollama Mistral 7B"""
    
    def __init__(self, primary_provider: str = "ollama"):
        self.primary_provider = primary_provider
        self.question_limits = {
            TestType.CAT1: {"count": 5, "marks_each": 10, "total": 50},
            TestType.CAT2: {"count": 5, "marks_each": 10, "total": 50},
            TestType.FAT: {"count": 10, "marks_each": 10, "total": 100}
        }
    
    async def generate_question_paper(self, request: QuestionGenerationRequest) -> QuestionGenerationResponse:
        """
        Main method to generate question papers based on syllabus and test type
        """
        start_time = time.time()
        
        try:
            # Generate the prompt based on the request
            prompt = self._create_generation_prompt(request)
            
            # Call Ollama to generate the question paper
            raw_response = await self._generate_with_ollama(prompt, request.test_type)
            
            # Parse and validate the JSON response
            question_paper = self._parse_and_validate_response(raw_response, request)
            
            processing_time = time.time() - start_time
            
            return QuestionGenerationResponse(
                success=True,
                message="Question paper generated successfully",
                question_paper=question_paper,
                processing_time=processing_time,
                agent_used="ollama_question_generator"
            )
            
        except Exception as e:
            logger.error("Question paper generation failed", error=str(e))
            return QuestionGenerationResponse(
                success=False,
                message=f"Generation failed: {str(e)}",
                question_paper=None,
                processing_time=time.time() - start_time,
                agent_used="none"
            )
    
    def _create_generation_prompt(self, request: QuestionGenerationRequest) -> str:
        """
        Create the prompt for question paper generation based on QueGenerator_Prompt.docx
        """
        test_config = self.question_limits[request.test_type]
        
        # Extract module-specific content from syllabus
        module_content = self._extract_module_content(request.syllabus_text, request.modules)
        modules_str = ', '.join(request.modules)
        
        prompt = f"""You are an expert exam paper generator. Generate a {request.test_type.value} question paper with EXACTLY {test_config['count']} questions.

🚨 CRITICAL RESTRICTION 🚨
ONLY GENERATE QUESTIONS FROM: {modules_str}
DO NOT USE ANY OTHER MODULES OR CONTENT
DO NOT USE YOUR BACKGROUND KNOWLEDGE - ONLY USE THE CONTENT SHOWN BELOW

STRICT REQUIREMENTS:
- Each question must be exactly {test_config['marks_each']} marks  
- Total paper marks: {test_config['total']}
- Generate questions EXCLUSIVELY from the module content provided below
- Each question must be tagged with ONLY these modules: {modules_str}
- FORBIDDEN: Using content from any other modules
- FORBIDDEN: Using concepts not explicitly mentioned in the module content below
- FORBIDDEN: Using any topic, concept, or terminology not explicitly listed in the provided content
- Output ONLY valid JSON, no explanations

{self._get_test_type_rules(request.test_type)}

ALLOWED MODULE CONTENT (USE ONLY THIS):
{module_content}

🔒 ABSOLUTE MODULE RESTRICTION 🔒
ALLOWED MODULES: {modules_str}
FORBIDDEN: All other modules
FORBIDDEN: Your general knowledge about any subject

ULTRA-STRICT CONTENT RULES:
- Read the module content above carefully
- ONLY create questions about topics explicitly mentioned in that content  
- If you're not sure if a concept is mentioned, DON'T use it
- Stick to the exact words and topics from the provided content
- Examples: If "LED" is mentioned, you can ask about LED. If "timer" is NOT mentioned, you CANNOT ask about timers

MODULE REQUIREMENTS:
- Distribute questions ONLY across: {modules_str}
- Each question "module" field must contain ONLY: {modules_str}
- Zero tolerance for other module content or external knowledge

REQUIRED JSON FORMAT (copy exactly, replace content):
{{
  "metadata": {{
    "title": "{request.test_type.value} Question Paper - {modules_str}",
    "test_type": "{request.test_type.value}",
    "modules": {json.dumps(request.modules)},
    "total_marks": {test_config['total']},
    "notes": "Generated EXCLUSIVELY from {modules_str}"
  }},
  "paper": [
    {{
      "q_no": 1,
      "marks": {test_config['marks_each']},
      "parts": [
        {{
          "label": null,
          "marks": {test_config['marks_each']},
          "text": "Question based STRICTLY on {modules_str} content only...",
          "module": ["{request.modules[0] if request.modules else 'Module 1'}"]
        }}
      ],
      "instructions": null
    }}
  ],
  "validation": {{
    "total_marks_check": {test_config['total']},
    "unique_questions": true
  }}
}}

⚠️ FINAL WARNING ⚠️
Generate {test_config['count']} questions with ABSOLUTE compliance:
1. Content source: ONLY the {modules_str} content above
2. Module tags: ONLY from {modules_str} 
3. Forbidden: Any reference to other modules
4. Follow {request.test_type.value} complexity rules
5. If in doubt, prefer basic questions from allowed modules over advanced questions from forbidden modules"""
        
        return prompt
    
    def _get_test_type_rules(self, test_type: TestType) -> str:
        """Get the specific rules for each test type from QueGenerator_Prompt.docx"""
        
        if test_type == TestType.CAT1:
            return """
CAT-1 RULES:
- Level 1: Generate one opinion-based general question from syllabus scenario
- Level 2: Generate one 10-mark no-subdivision question based on basic module knowledge  
- Level 3: Generate one or two derivation-based or solving-based 10-mark no-subdivision questions
- Level 4: Generate one or two questions with 2+ subdivisions, each logically connected and formula-based
- All questions must be directly based on the syllabus content provided
- Focus on practical application scenarios from the modules
"""
        
        elif test_type == TestType.CAT2:
            return """
CAT-2 RULES:
- Level 1: Generate one or two real-world scenario-based questions without specifying algorithms/methods
- Level 2: For coding modules, generate complex coding scenarios requiring lengthy solutions
- Level 3: Generate two scenario-based questions with 2-3 subdivisions requiring deep logical analysis
- Questions should force students to think about what concepts to apply
- Higher-order thinking and analytical skills required
- Scenarios must be realistic and challenging
"""
        
        elif test_type == TestType.FAT:
            return """
FAT RULES:
- 7 out of 10 questions must follow CAT-1 rules and be syllabus-based
- Remaining 3 questions must follow CAT-2 rules requiring deeper logical thinking
- Mix of basic knowledge, derivations, and advanced analytical questions
- Comprehensive coverage of all selected modules
- Balance between theoretical knowledge and practical application
"""
        
        return ""
    
    def _extract_module_content(self, syllabus_text: str, selected_modules: List[str]) -> str:
        """
        Extract ONLY content from selected modules - extremely strict parsing
        """
        logger.info(f"Extracting content for modules: {selected_modules}")
        
        try:
            # Parse ALL modules from syllabus first
            all_modules = self._parse_all_modules_from_syllabus(syllabus_text)
            
            logger.info("Found modules in syllabus", modules=list(all_modules.keys()))
            
            # Extract content ONLY from selected modules
            selected_content = []
            found_modules = []
            
            for module_name in selected_modules:
                # Try exact match first
                if module_name in all_modules:
                    selected_content.append(f"\n=== {module_name} CONTENT ONLY ===")
                    selected_content.append(all_modules[module_name])
                    selected_content.append("")
                    found_modules.append(module_name)
                else:
                    # Try alternative module name formats
                    module_num = self._extract_module_number(module_name)
                    if module_num:
                        for key in all_modules.keys():
                            if self._extract_module_number(key) == module_num:
                                selected_content.append(f"\n=== {module_name} CONTENT ONLY ===")
                                selected_content.append(all_modules[key])
                                selected_content.append("")
                                found_modules.append(module_name)
                                break
            
            if not found_modules:
                logger.error("No selected modules found in syllabus", 
                           selected=selected_modules, 
                           available=list(all_modules.keys()))
                return self._create_error_response(selected_modules, list(all_modules.keys()))
            
            logger.info(f"Successfully extracted content for: {found_modules}")
            
            result = '\n'.join(selected_content)
            
            # Create ultra-strict prompt content
            strict_content = f"""
ULTRA STRICT INSTRUCTION: You MUST generate questions ONLY from the specific module content below.

SELECTED MODULES: {', '.join(selected_modules)}
AVAILABLE CONTENT: {', '.join(found_modules)}

=== MODULE-SPECIFIC CONTENT ===
{result}

CRITICAL RULES:
1. Generate questions ONLY from the content above
2. DO NOT use any knowledge outside this content
3. Each question must relate to topics mentioned in the selected modules
4. Tag each question with the correct module name from: {', '.join(selected_modules)}
5. IGNORE all other syllabus content not shown above
6. DO NOT mention any concepts, terms, or topics not explicitly listed in the content above
7. STICK STRICTLY to the topics shown: only use words and concepts that appear in the content above

FORBIDDEN: Questions about topics not explicitly mentioned in the selected module content above.
ABSOLUTELY FORBIDDEN: Using your general knowledge about any subject beyond the provided content."""

            return strict_content
            
        except Exception as e:
            logger.error("Module extraction failed", error=str(e))
            return self._create_error_response(selected_modules, [])
    
    def _parse_all_modules_from_syllabus(self, syllabus_text: str) -> Dict[str, str]:
        """
        Parse ALL modules from the syllabus and return a dictionary mapping module names to content
        """
        import re
        
        modules = {}
        current_module = None
        current_content = []
        
        lines = syllabus_text.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            line_lower = line_stripped.lower()
            
            # Look for module headers with various patterns
            module_patterns = [
                r'module\s*(\d+)\s*[:.\-]?\s*(.*)',
                r'module\s*[:.\-]?\s*(\d+)\s*(.*)',
                r'chapter\s*(\d+)\s*[:.\-]?\s*(.*)',
                r'unit\s*(\d+)\s*[:.\-]?\s*(.*)',
                r'(\d+)\s*[:.\-]\s*(.*)',  # Just number with colon/dash
            ]
            
            module_found = False
            for pattern in module_patterns:
                match = re.match(pattern, line_lower)
                if match:
                    # Save previous module content if exists
                    if current_module and current_content:
                        modules[current_module] = '\n'.join(current_content)
                    
                    # Start new module
                    module_num = match.group(1)
                    current_module = f"Module {module_num}"
                    current_content = [line_stripped]  # Include the header
                    module_found = True
                    break
            
            # If not a module header, add to current module content
            if not module_found and current_module:
                current_content.append(line_stripped)
        
        # Don't forget the last module
        if current_module and current_content:
            modules[current_module] = '\n'.join(current_content)
        
        return modules
    
    def _extract_module_number(self, module_name: str) -> str:
        """Extract module number from module name"""
        import re
        match = re.search(r'(\d+)', module_name)
        return match.group(1) if match else None
    
    def _create_error_response(self, selected_modules: List[str], available_modules: List[str]) -> str:
        """Create error response when modules are not found"""
        return f"""
ERROR: Cannot generate questions for the selected modules.

SELECTED MODULES: {', '.join(selected_modules)}
AVAILABLE MODULES IN SYLLABUS: {', '.join(available_modules)}

Please check that the module names are correct and exist in the uploaded syllabus.
Supported formats: "Module 1", "Module 2", etc.
"""
    
    def _extract_by_paragraph_analysis(self, syllabus_text: str, selected_modules: List[str]) -> str:
        """
        Alternative extraction method using paragraph analysis when structured extraction fails
        """
        logger.info("Attempting paragraph-based module extraction")
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in syllabus_text.split('\n\n') if p.strip()]
        
        # Extract module numbers
        selected_numbers = []
        for module in selected_modules:
            import re
            match = re.search(r'(\d+)', module)
            if match:
                selected_numbers.append(match.group(1))
        
        module_paragraphs = {}
        
        for paragraph in paragraphs:
            para_lower = paragraph.lower()
            
            # Check if this paragraph belongs to any selected module
            for i, module in enumerate(selected_modules):
                module_num = selected_numbers[i] if i < len(selected_numbers) else ""
                
                # Look for module references in the paragraph
                if (f"module {module_num}" in para_lower or 
                    f"chapter {module_num}" in para_lower or
                    f"unit {module_num}" in para_lower):
                    
                    if module not in module_paragraphs:
                        module_paragraphs[module] = []
                    module_paragraphs[module].append(paragraph)
                    break
        
        # Build result
        if module_paragraphs:
            result = []
            for module in selected_modules:
                if module in module_paragraphs:
                    result.append(f"\n=== {module.upper()} CONTENT ===")
                    result.extend(module_paragraphs[module])
                    result.append("")
            
            if result:
                content = '\n'.join(result)
                return f"""STRICT MODULE FILTER: Use ONLY the content below for question generation.

ALLOWED MODULES: {', '.join(selected_modules)}

EXTRACTED CONTENT:
{content}

INSTRUCTION: Generate questions ONLY from the above content. Do not reference any other modules or topics."""
        
        # If paragraph analysis also fails, return minimal content
        return self._create_minimal_module_content(selected_modules)
    
    def _create_minimal_module_content(self, selected_modules: List[str]) -> str:
        """
        Create minimal module-specific content when extraction fails
        """
        logger.warning(f"Creating minimal content for modules: {selected_modules}")
        
        return f"""CRITICAL: Generate questions for {', '.join(selected_modules)} ONLY.

SELECTED MODULES: {', '.join(selected_modules)}

INSTRUCTIONS FOR AI:
1. Generate questions ONLY for the modules specified above
2. Do NOT include content from other modules  
3. If you cannot identify specific content for these modules, generate basic conceptual questions appropriate for these module numbers
4. Each question must be tagged with the correct module from the selected list
5. Focus on fundamental concepts typically covered in these specific modules

STRICT RULE: Questions must relate only to {', '.join(selected_modules)}. Ignore all other modules completely."""
    
    def _create_strict_module_prompt(self, selected_modules: List[str]) -> str:
        """
        Create strict module-only prompt when no content can be extracted
        """
        modules_str = ', '.join(selected_modules)
        
        return f"""ABSOLUTE RESTRICTION: Generate questions ONLY for {modules_str}.

SELECTED MODULES: {modules_str}

CRITICAL INSTRUCTIONS:
1. Generate questions ONLY for the modules listed above
2. Do NOT use any content from other modules
3. If unsure about module content, generate basic academic questions appropriate for these specific module numbers
4. Each question MUST be tagged with one of: {modules_str}
5. Completely ignore all other modules and topics

EXAMPLES of what to do:
- Generate questions based only on the topics mentioned in each selected module
- Use the exact terminology and concepts from the provided content
- Create questions that directly relate to the module-specific content shown above

STRICT RULE: Only {modules_str} content allowed. Zero tolerance for other modules."""
    
    async def _generate_with_ollama(self, prompt: str, test_type: TestType) -> str:
        """Generate question paper using Ollama Mistral 7B"""
        
        system_message = "You are an expert exam question generator. Respond ONLY with valid JSON format. No explanations, no additional text, just the JSON object as requested."
        
        try:
            response = await ollama_client.generate_completion(
                prompt=prompt,
                system_message=system_message,
                temperature=0.3,  # Lower for more consistent JSON structure
                max_tokens=4000   # More tokens for multiple questions
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error("Ollama generation failed", error=str(e))
            raise Exception(f"Question generation failed: {str(e)}")
    
    def _parse_and_validate_response(self, raw_response: str, request: QuestionGenerationRequest) -> GeneratedQuestionPaper:
        """Parse and validate the JSON response from Ollama"""
        
        try:
            logger.info("Raw AI response", response=raw_response[:1000])
            
            # Clean the response - remove any non-JSON content
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No valid JSON found in response")
            
            clean_json = raw_response[json_start:json_end]
            logger.info("Cleaned JSON", json=clean_json[:500])
            
            # Parse JSON
            parsed_data = json.loads(clean_json)
            
            # Check and log missing fields
            required_fields = ['metadata', 'paper', 'validation']
            missing_fields = [field for field in required_fields if field not in parsed_data]
            if missing_fields:
                logger.error("Missing top-level fields", missing=missing_fields, available=list(parsed_data.keys()))
                raise ValueError(f"Missing required top-level fields: {missing_fields}")
            
            # Create fallback data if AI response is incomplete
            if 'paper' in parsed_data and isinstance(parsed_data['paper'], list):
                test_config = self.question_limits[request.test_type]
                
                # Ensure metadata is complete
                if 'metadata' not in parsed_data or not isinstance(parsed_data['metadata'], dict):
                    parsed_data['metadata'] = {}
                
                metadata = parsed_data['metadata']
                metadata.setdefault('title', f"{request.test_type.value} Question Paper")
                metadata.setdefault('test_type', request.test_type.value)
                metadata.setdefault('modules', request.modules)
                metadata.setdefault('total_marks', test_config['total'])
                metadata.setdefault('notes', "Generated based on provided syllabus")
                
                # Ensure validation is complete
                if 'validation' not in parsed_data or not isinstance(parsed_data['validation'], dict):
                    parsed_data['validation'] = {}
                
                validation = parsed_data['validation']
                validation.setdefault('total_marks_check', test_config['total'])
                validation.setdefault('unique_questions', True)
                
                # Fix question structure if needed
                for i, question in enumerate(parsed_data['paper']):
                    if not isinstance(question, dict):
                        continue
                        
                    question.setdefault('q_no', i + 1)
                    question.setdefault('marks', test_config['marks_each'])
                    question.setdefault('instructions', None)
                    
                    if 'parts' not in question or not isinstance(question['parts'], list):
                        question['parts'] = []
                    
                    # Ensure each part has required fields
                    for part in question['parts']:
                        if isinstance(part, dict):
                            part.setdefault('label', None)
                            part.setdefault('marks', question.get('marks', test_config['marks_each']))
                            part.setdefault('text', f"Question {question.get('q_no', i+1)} content")
                            part.setdefault('module', request.modules[:1])  # Default to first module
            
            # Create and validate the question paper object
            question_paper = GeneratedQuestionPaper(**parsed_data)
            
            # Additional validation
            self._validate_question_paper(question_paper, request)
            
            return question_paper
            
        except json.JSONDecodeError as e:
            logger.error("JSON parsing failed", error=str(e), response=raw_response[:500])
            raise ValueError(f"Invalid JSON response: {str(e)}")
        
        except Exception as e:
            logger.error("Response validation failed", error=str(e), parsed_data=parsed_data if 'parsed_data' in locals() else None)
            raise ValueError(f"Response validation failed: {str(e)}")
    
    def _validate_question_paper(self, question_paper: GeneratedQuestionPaper, request: QuestionGenerationRequest):
        """Validate the generated question paper against requirements"""
        
        test_config = self.question_limits[request.test_type]
        
        # Check question count
        if len(question_paper.paper) != test_config['count']:
            raise ValueError(f"Expected {test_config['count']} questions, got {len(question_paper.paper)}")
        
        # Check total marks
        actual_total = sum(q.marks for q in question_paper.paper)
        if actual_total != test_config['total']:
            raise ValueError(f"Expected {test_config['total']} total marks, got {actual_total}")
        
        # Check each question has 10 marks
        for q in question_paper.paper:
            if q.marks != test_config['marks_each']:
                raise ValueError(f"Question {q.q_no} has {q.marks} marks, expected {test_config['marks_each']}")
        
        # Validate that questions cover the requested modules
        covered_modules = set()
        for question in question_paper.paper:
            for part in question.parts:
                covered_modules.update(part.module)
        
        # Check if at least some requested modules are covered
        requested_modules = set(request.modules)
        if not covered_modules.intersection(requested_modules):
            logger.warning("Generated questions don't cover any requested modules", 
                         requested=request.modules, covered=list(covered_modules))
        
        logger.info("Question paper validation passed", 
                   questions=len(question_paper.paper), 
                   total_marks=actual_total,
                   modules_covered=list(covered_modules))


# Global question generator instance
question_generator = QuestionPaperGenerator(primary_provider="ollama")