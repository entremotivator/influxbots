#!/usr/bin/env python3
"""
🚀 ENHANCED CHAT BOT WITH FILE UPLOADS
Real API integration, personal system prompts, and comprehensive file upload capabilities
"""

import streamlit as st
import os
import json
import time
import hashlib
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from io import StringIO, BytesIO
import base64
import tempfile
import mimetypes

# OpenAI imports (modern API)
from openai import OpenAI
import tiktoken

# File processing imports
import PyPDF2
from PIL import Image
import docx
from openpyxl import load_workbook
import csv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🤖 ENHANCED BOT PERSONALITIES WITH SHORTER PROMPTS
# ======================================================

ENHANCED_BOT_PERSONALITIES = {
    # ENTREPRENEURSHIP & STARTUPS
    "Startup Strategist": {
        "description": "Expert startup advisor helping with strategy, MVP development, and scaling. I guide you through every stage from idea to IPO.",
        "system_prompt": "You're a startup strategist with 15+ years experience. Be direct, actionable, and focus on practical solutions. Ask clarifying questions and provide step-by-step guidance.",
        "emoji": "🚀",
        "category": "Entrepreneurship",
        "specialties": ["Business Strategy", "MVP Development", "Scaling", "Product-Market Fit"]
    },
    "Business Plan Writer": {
        "description": "I create investor-ready business plans with market analysis, financial projections, and strategic roadmaps.",
        "system_prompt": "You're a business plan expert. Create comprehensive, professional plans. Focus on market opportunity, competitive advantage, and financial viability.",
        "emoji": "📋",
        "category": "Entrepreneurship", 
        "specialties": ["Business Plans", "Market Analysis", "Financial Projections", "Investment Proposals"]
    },
    "Venture Capital Advisor": {
        "description": "Guide startups through fundraising with pitch deck creation, investor relations, and valuation strategies.",
        "system_prompt": "You're a VC advisor who helps startups raise funding. Be strategic about investor matching and pitch optimization. Focus on what investors want to see.",
        "emoji": "💰",
        "category": "Entrepreneurship",
        "specialties": ["Fundraising", "Pitch Decks", "Investor Relations", "Valuation"]
    },
    
    # SALES & MARKETING
    "Sales Performance Coach": {
        "description": "Maximize sales potential through proven methodologies, funnel optimization, and conversion improvement.",
        "system_prompt": "You're a sales coach focused on results. Provide actionable techniques for closing deals, handling objections, and building pipelines. Be motivational but practical.",
        "emoji": "📈",
        "category": "Sales & Marketing",
        "specialties": ["Sales Funnels", "Conversion", "Objection Handling", "Closing Techniques"]
    },
    "Digital Marketing Specialist": {
        "description": "Drive measurable results through SEO, PPC, social media, and conversion optimization strategies.",
        "system_prompt": "You're a digital marketing expert focused on ROI. Provide data-driven strategies for online growth. Always include metrics and measurement approaches.",
        "emoji": "📱",
        "category": "Sales & Marketing",
        "specialties": ["SEO", "PPC", "Social Media", "Conversion Optimization"]
    },
    "Content Marketing Strategist": {
        "description": "Create engaging content that attracts, educates, and converts audiences through strategic storytelling.",
        "system_prompt": "You're a content strategist who creates compelling narratives. Focus on audience engagement and conversion. Provide content calendars and distribution strategies.",
        "emoji": "✍️",
        "category": "Sales & Marketing",
        "specialties": ["Content Strategy", "Storytelling", "Content Calendars", "Distribution"]
    },
    
    # FINANCE & ACCOUNTING
    "Financial Controller": {
        "description": "Optimize financial operations through budgeting, planning, and cost control measures.",
        "system_prompt": "You're a financial controller focused on operational efficiency. Provide clear financial guidance and cost optimization strategies. Be detail-oriented but practical.",
        "emoji": "💼",
        "category": "Finance",
        "specialties": ["Financial Planning", "Budgeting", "Cost Control", "Financial Analysis"]
    },
    "Investment Advisor": {
        "description": "Provide investment guidance and portfolio management with focus on risk assessment and returns.",
        "system_prompt": "You're an investment advisor focused on building wealth. Provide balanced investment strategies considering risk tolerance and goals. Always mention risk factors.",
        "emoji": "📊",
        "category": "Finance",
        "specialties": ["Portfolio Management", "Risk Assessment", "Investment Strategy", "Wealth Building"]
    },
    "Tax Strategy Consultant": {
        "description": "Minimize tax liability while ensuring compliance through strategic planning and optimization.",
        "system_prompt": "You're a tax strategist focused on legal optimization. Provide tax-efficient strategies while ensuring compliance. Always recommend consulting a tax professional.",
        "emoji": "🧾",
        "category": "Finance",
        "specialties": ["Tax Planning", "Tax Optimization", "Compliance", "Business Structure"]
    },
    
    # FORMAT SPECIALISTS
    "PDF Document Specialist": {
        "description": "Expert in PDF creation, analysis, and optimization with focus on security and accessibility.",
        "system_prompt": "You're a PDF expert who optimizes document workflows. Focus on security, accessibility, and automation. Provide technical solutions for document management.",
        "emoji": "📄",
        "category": "Format Specialists",
        "specialties": ["PDF Security", "Accessibility", "Document Automation", "Form Design"]
    },
    "CSV Data Analyst": {
        "description": "Extract insights from CSV data through cleaning, analysis, and visualization.",
        "system_prompt": "You're a data analyst who turns CSV data into insights. Focus on data cleaning, statistical analysis, and actionable recommendations. Always validate data quality.",
        "emoji": "📊",
        "category": "Format Specialists",
        "specialties": ["Data Cleaning", "Statistical Analysis", "Data Visualization", "Insights"]
    },
    "SQL Database Consultant": {
        "description": "Optimize database performance through design, query optimization, and architecture planning.",
        "system_prompt": "You're a database expert focused on performance and scalability. Provide optimized queries and database design recommendations. Consider security and best practices.",
        "emoji": "🗄️",
        "category": "Format Specialists",
        "specialties": ["Database Design", "Query Optimization", "Performance Tuning", "Data Modeling"]
    },
    "API Integration Specialist": {
        "description": "Connect systems through REST APIs, webhooks, and scalable integration patterns.",
        "system_prompt": "You're an API expert who connects systems efficiently. Focus on RESTful design, security, and scalability. Provide code examples and best practices.",
        "emoji": "🔗",
        "category": "Format Specialists",
        "specialties": ["REST APIs", "System Integration", "API Security", "Webhooks"]
    },
    "Image Processing Expert": {
        "description": "Optimize visual content through format conversion, batch processing, and automated workflows.",
        "system_prompt": "You're an image processing expert focused on optimization and automation. Provide solutions for format conversion, compression, and batch processing.",
        "emoji": "🖼️",
        "category": "Format Specialists",
        "specialties": ["Image Optimization", "Format Conversion", "Batch Processing", "Visual Content"]
    },
    
    # OPERATIONS & MANAGEMENT
    "Operations Excellence Manager": {
        "description": "Streamline processes and maximize efficiency through lean methodologies and optimization.",
        "system_prompt": "You're an operations expert focused on efficiency and quality. Provide process improvements and lean solutions. Always consider cost-benefit analysis.",
        "emoji": "⚙️",
        "category": "Operations",
        "specialties": ["Process Improvement", "Lean Methods", "Efficiency", "Quality Management"]
    },
    "Project Management Expert": {
        "description": "Deliver projects on time and within budget through planning, resource allocation, and stakeholder management.",
        "system_prompt": "You're a project manager focused on successful delivery. Provide structured approaches to planning, execution, and risk management. Use proven methodologies.",
        "emoji": "📋",
        "category": "Operations",
        "specialties": ["Project Planning", "Resource Management", "Risk Management", "Stakeholder Communication"]
    },
    "Supply Chain Strategist": {
        "description": "Optimize end-to-end supply chain operations through vendor management and logistics planning.",
        "system_prompt": "You're a supply chain expert focused on optimization and cost reduction. Provide strategies for vendor management, inventory control, and logistics efficiency.",
        "emoji": "🚛",
        "category": "Operations",
        "specialties": ["Supply Chain", "Vendor Management", "Inventory Control", "Logistics"]
    },
    
    # TECHNOLOGY & INNOVATION
    "Digital Transformation Consultant": {
        "description": "Guide organizations through technology transformation with strategic planning and change management.",
        "system_prompt": "You're a digital transformation expert focused on strategic technology adoption. Provide roadmaps for digital change and innovation frameworks.",
        "emoji": "💻",
        "category": "Technology",
        "specialties": ["Digital Strategy", "Technology Adoption", "Change Management", "Innovation"]
    },
    "AI Strategy Consultant": {
        "description": "Help businesses leverage AI technologies through strategic implementation and governance.",
        "system_prompt": "You're an AI strategist focused on practical AI implementation. Provide guidance on AI adoption, use cases, and governance. Consider ethical implications.",
        "emoji": "🤖",
        "category": "Technology",
        "specialties": ["AI Strategy", "Machine Learning", "AI Governance", "Automation"]
    },
    "Cybersecurity Specialist": {
        "description": "Protect organizations from digital threats through security architecture and risk assessment.",
        "system_prompt": "You're a cybersecurity expert focused on threat protection. Provide security strategies, risk assessments, and incident response plans. Prioritize practical security.",
        "emoji": "🔒",
        "category": "Technology",
        "specialties": ["Security Architecture", "Threat Assessment", "Incident Response", "Risk Management"]
    },
    
    # HUMAN RESOURCES
    "HR Director": {
        "description": "Provide strategic HR leadership through organizational development and employee engagement.",
        "system_prompt": "You're an HR leader focused on people and culture. Provide strategies for talent management, employee engagement, and organizational development.",
        "emoji": "👥",
        "category": "Human Resources",
        "specialties": ["HR Strategy", "Talent Management", "Employee Engagement", "Culture Development"]
    },
    "Talent Acquisition Manager": {
        "description": "Attract and hire top talent through recruitment strategy and employer branding.",
        "system_prompt": "You're a talent acquisition expert focused on finding great people. Provide recruitment strategies, interview techniques, and employer branding advice.",
        "emoji": "🎯",
        "category": "Human Resources",
        "specialties": ["Recruitment", "Employer Branding", "Interview Process", "Talent Pipeline"]
    },
    
    # CUSTOMER RELATIONS
    "Customer Success Manager": {
        "description": "Ensure customers achieve desired outcomes through relationship management and value realization.",
        "system_prompt": "You're a customer success expert focused on customer outcomes. Provide strategies for onboarding, retention, and value delivery. Always think customer-first.",
        "emoji": "🤝",
        "category": "Customer Relations",
        "specialties": ["Customer Onboarding", "Retention", "Value Realization", "Relationship Management"]
    },
    "Customer Experience Director": {
        "description": "Design exceptional customer experiences through journey mapping and touchpoint optimization.",
        "system_prompt": "You're a CX expert focused on creating amazing customer experiences. Provide journey maps, touchpoint optimization, and experience measurement strategies.",
        "emoji": "⭐",
        "category": "Customer Relations",
        "specialties": ["Experience Design", "Journey Mapping", "Touchpoint Optimization", "CX Measurement"]
    }
}

# ======================================================
# 💰 PRICING & USAGE TRACKING
# ======================================================

PRICING = {
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
}

SUBSCRIPTION_PLANS = {
    "Basic": {
        "monthly_budget": 25.00,
        "daily_budget": 5.00,
        "max_tokens_per_request": 4000,
        "max_requests_per_hour": 50,
        "available_models": ["gpt-3.5-turbo"],
        "max_file_size_mb": 10,
        "max_files_per_chat": 5
    },
    "Pro": {
        "monthly_budget": 100.00,
        "daily_budget": 20.00,
        "max_tokens_per_request": 8000,
        "max_requests_per_hour": 200,
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo"],
        "max_file_size_mb": 50,
        "max_files_per_chat": 10
    },
    "Plus": {
        "monthly_budget": 200.00,
        "daily_budget": 40.00,
        "max_tokens_per_request": 16000,
        "max_requests_per_hour": 500,
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"],
        "max_file_size_mb": 100,
        "max_files_per_chat": 20
    },
    "Enterprise": {
        "monthly_budget": 1000.00,
        "daily_budget": 200.00,
        "max_tokens_per_request": 32000,
        "max_requests_per_hour": 2000,
        "available_models": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"],
        "max_file_size_mb": 500,
        "max_files_per_chat": 50
    }
}

# Demo users with enhanced capabilities
DEMO_USERS = {
    "demo": {
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
        "plan": "Pro",
        "api_key": "",
        "created_date": datetime.now() - timedelta(days=30)
    },
    "premium": {
        "password_hash": hashlib.sha256("premium123".encode()).hexdigest(),
        "plan": "Plus",
        "api_key": "",
        "created_date": datetime.now() - timedelta(days=15)
    },
    "enterprise": {
        "password_hash": hashlib.sha256("enterprise123".encode()).hexdigest(),
        "plan": "Enterprise",
        "api_key": "",
        "created_date": datetime.now() - timedelta(days=60)
    }
}

# ======================================================
# 🔧 ENHANCED API MANAGER WITH REAL INTEGRATION
# ======================================================

class EnhancedAPIManager:
    def __init__(self):
        self.client = None
        self.encoding = None
        
    def initialize(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize OpenAI client with proper error handling"""
        try:
            if api_key and api_key != "demo_key":
                # Real API initialization
                self.client = OpenAI(api_key=api_key)
                self.encoding = tiktoken.encoding_for_model(model)
                
                # Test the connection
                test_response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10
                )
                
                logger.info(f"OpenAI API initialized successfully with model: {model}")
                return True
            else:
                # Demo mode
                self.client = None
                self.encoding = None
                logger.info("Running in demo mode")
                return True
                
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI API: {str(e)}")
            self.client = None
            self.encoding = None
            return False
    
    def count_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """Count tokens in text"""
        try:
            if self.encoding:
                return len(self.encoding.encode(text))
            else:
                # Fallback estimation
                return len(text.split()) * 1.3
        except Exception:
            return len(text.split()) * 1.3
    
    def generate_response(self, messages: List[Dict], model: str = "gpt-3.5-turbo", 
                         max_tokens: int = 2000, temperature: float = 0.7) -> Tuple[str, Dict]:
        """Generate response using OpenAI API"""
        try:
            if self.client:
                # Real API call
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                # Extract response
                content = response.choices[0].message.content
                
                # Calculate usage and cost
                usage = response.usage
                input_tokens = usage.prompt_tokens
                output_tokens = usage.completion_tokens
                total_tokens = usage.total_tokens
                
                # Calculate cost
                pricing = PRICING.get(model, PRICING["gpt-3.5-turbo"])
                cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1000
                
                metadata = {
                    "model": model,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    "cost": cost,
                    "demo_mode": False
                }
                
                return content, metadata
                
            else:
                # Demo mode response
                return self.generate_demo_response(messages), {
                    "model": "demo",
                    "input_tokens": 50,
                    "output_tokens": 100,
                    "total_tokens": 150,
                    "cost": 0.0,
                    "demo_mode": True
                }
                
        except Exception as e:
            logger.error(f"API generation error: {str(e)}")
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            
            return error_response, {
                "model": "error",
                "input_tokens": 0,
                "output_tokens": len(error_response.split()),
                "total_tokens": len(error_response.split()),
                "cost": 0.0,
                "error": True,
                "demo_mode": True
            }
    
    def generate_demo_response(self, messages: List[Dict]) -> str:
        """Generate demo response"""
        user_message = messages[-1]["content"] if messages else "Hello"
        
        return f"""Thank you for your message: "{user_message[:100]}..."

🎮 **Demo Mode Response**

In the full version with your OpenAI API key, I would provide:

✅ **Personalized Analysis**: Detailed insights based on your specific situation and uploaded files
✅ **File Processing**: Analysis of your uploaded documents, images, and data files  
✅ **Actionable Recommendations**: Step-by-step guidance tailored to your needs
✅ **Real-time Interaction**: Dynamic conversation with context awareness
✅ **Professional Expertise**: Specialized knowledge in my domain area

**To get real AI responses:**
1. Get an OpenAI API key from platform.openai.com
2. Enter it in the sidebar API key field
3. Experience full AI-powered conversations with file upload support

This demo shows the interface. Real responses will be much more detailed and helpful!"""

# Initialize API manager
api_manager = EnhancedAPIManager()

# ======================================================
# 📁 COMPREHENSIVE FILE UPLOAD SYSTEM
# ======================================================

class FileProcessor:
    def __init__(self):
        self.supported_types = {
            'text': ['.txt', '.md', '.csv', '.json', '.xml', '.html', '.css', '.js', '.py', '.sql'],
            'document': ['.pdf', '.docx', '.doc', '.odt', '.rtf'],
            'spreadsheet': ['.xlsx', '.xls', '.ods'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'data': ['.json', '.xml', '.yaml', '.yml']
        }
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type from extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        for file_type, extensions in self.supported_types.items():
            if ext in extensions:
                return file_type
        
        return 'unknown'
    
    def process_uploaded_file(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded file and extract content"""
        try:
            file_info = {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': self.get_file_type(uploaded_file.name),
                'content': '',
                'metadata': {},
                'error': None
            }
            
            # Read file content based on type
            if file_info['file_type'] == 'text':
                content = self.process_text_file(uploaded_file)
            elif file_info['file_type'] == 'document':
                content = self.process_document_file(uploaded_file)
            elif file_info['file_type'] == 'spreadsheet':
                content = self.process_spreadsheet_file(uploaded_file)
            elif file_info['file_type'] == 'image':
                content = self.process_image_file(uploaded_file)
            elif file_info['file_type'] == 'data':
                content = self.process_data_file(uploaded_file)
            else:
                content = f"File type not supported for content extraction: {uploaded_file.name}"
            
            file_info['content'] = content
            return file_info
            
        except Exception as e:
            logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
            return {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': 'error',
                'content': '',
                'metadata': {},
                'error': str(e)
            }
    
    def process_text_file(self, uploaded_file) -> str:
        """Process text-based files"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    content = uploaded_file.read().decode(encoding)
                    uploaded_file.seek(0)  # Reset file pointer
                    return content
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    continue
            
            return "Could not decode file content"
            
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def process_document_file(self, uploaded_file) -> str:
        """Process document files (PDF, DOCX, etc.)"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.pdf':
                return self.process_pdf(uploaded_file)
            elif file_extension in ['.docx', '.doc']:
                return self.process_docx(uploaded_file)
            else:
                return f"Document type {file_extension} not yet supported"
                
        except Exception as e:
            return f"Error processing document: {str(e)}"
    
    def process_pdf(self, uploaded_file) -> str:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text.strip():
                    text_content.append(f"--- Page {page_num + 1} ---\n{text}")
            
            return "\n\n".join(text_content) if text_content else "No text content found in PDF"
            
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    def process_docx(self, uploaded_file) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(uploaded_file)
            text_content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            return "\n\n".join(text_content) if text_content else "No text content found in document"
            
        except Exception as e:
            return f"Error processing DOCX: {str(e)}"
    
    def process_spreadsheet_file(self, uploaded_file) -> str:
        """Process spreadsheet files"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.csv':
                return self.process_csv(uploaded_file)
            elif file_extension in ['.xlsx', '.xls']:
                return self.process_excel(uploaded_file)
            else:
                return f"Spreadsheet type {file_extension} not yet supported"
                
        except Exception as e:
            return f"Error processing spreadsheet: {str(e)}"
    
    def process_csv(self, uploaded_file) -> str:
        """Process CSV file"""
        try:
            # Try to read as CSV
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            
            # Parse CSV
            csv_reader = csv.reader(StringIO(content))
            rows = list(csv_reader)
            
            if not rows:
                return "Empty CSV file"
            
            # Format output
            result = f"CSV File Analysis:\n"
            result += f"- Rows: {len(rows)}\n"
            result += f"- Columns: {len(rows[0]) if rows else 0}\n\n"
            
            # Show first few rows
            result += "First 5 rows:\n"
            for i, row in enumerate(rows[:5]):
                result += f"Row {i+1}: {', '.join(str(cell) for cell in row)}\n"
            
            if len(rows) > 5:
                result += f"... and {len(rows) - 5} more rows"
            
            return result
            
        except Exception as e:
            return f"Error processing CSV: {str(e)}"
    
    def process_excel(self, uploaded_file) -> str:
        """Process Excel file"""
        try:
            workbook = load_workbook(uploaded_file)
            result = f"Excel File Analysis:\n"
            result += f"- Worksheets: {len(workbook.sheetnames)}\n"
            result += f"- Sheet names: {', '.join(workbook.sheetnames)}\n\n"
            
            # Process first sheet
            first_sheet = workbook.active
            result += f"First sheet '{first_sheet.title}':\n"
            result += f"- Max row: {first_sheet.max_row}\n"
            result += f"- Max column: {first_sheet.max_column}\n\n"
            
            # Show first few rows
            result += "First 5 rows:\n"
            for row_num in range(1, min(6, first_sheet.max_row + 1)):
                row_data = []
                for col_num in range(1, min(6, first_sheet.max_column + 1)):
                    cell_value = first_sheet.cell(row=row_num, column=col_num).value
                    row_data.append(str(cell_value) if cell_value is not None else "")
                result += f"Row {row_num}: {', '.join(row_data)}\n"
            
            return result
            
        except Exception as e:
            return f"Error processing Excel: {str(e)}"
    
    def process_image_file(self, uploaded_file) -> str:
        """Process image files"""
        try:
            image = Image.open(uploaded_file)
            
            result = f"Image Analysis:\n"
            result += f"- Format: {image.format}\n"
            result += f"- Size: {image.size[0]} x {image.size[1]} pixels\n"
            result += f"- Mode: {image.mode}\n"
            
            # Basic image info
            if hasattr(image, 'info'):
                if 'dpi' in image.info:
                    result += f"- DPI: {image.info['dpi']}\n"
            
            result += f"\nImage uploaded successfully. In full version, I can analyze image content, extract text (OCR), and provide detailed visual analysis."
            
            return result
            
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def process_data_file(self, uploaded_file) -> str:
        """Process data files (JSON, XML, etc.)"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.json':
                return self.process_json(uploaded_file)
            elif file_extension == '.xml':
                return self.process_xml(uploaded_file)
            else:
                return f"Data type {file_extension} not yet supported"
                
        except Exception as e:
            return f"Error processing data file: {str(e)}"
    
    def process_json(self, uploaded_file) -> str:
        """Process JSON file"""
        try:
            content = uploaded_file.read().decode('utf-8')
            data = json.loads(content)
            
            result = f"JSON File Analysis:\n"
            result += f"- Type: {type(data).__name__}\n"
            
            if isinstance(data, dict):
                result += f"- Keys: {len(data.keys())}\n"
                result += f"- Top-level keys: {', '.join(list(data.keys())[:10])}\n"
            elif isinstance(data, list):
                result += f"- Items: {len(data)}\n"
                if data and isinstance(data[0], dict):
                    result += f"- Item keys: {', '.join(list(data[0].keys())[:10])}\n"
            
            result += f"\nFirst 500 characters of content:\n{json.dumps(data, indent=2)[:500]}..."
            
            return result
            
        except Exception as e:
            return f"Error processing JSON: {str(e)}"
    
    def process_xml(self, uploaded_file) -> str:
        """Process XML file"""
        try:
            content = uploaded_file.read().decode('utf-8')
            
            result = f"XML File Analysis:\n"
            result += f"- Size: {len(content)} characters\n"
            
            # Basic XML structure analysis
            root_tag_start = content.find('<')
            root_tag_end = content.find('>', root_tag_start)
            if root_tag_start != -1 and root_tag_end != -1:
                root_tag = content[root_tag_start:root_tag_end+1]
                result += f"- Root element: {root_tag}\n"
            
            result += f"\nFirst 500 characters:\n{content[:500]}..."
            
            return result
            
        except Exception as e:
            return f"Error processing XML: {str(e)}"

# Initialize file processor
file_processor = FileProcessor()

# ======================================================
# 🔐 AUTHENTICATION SYSTEM
# ======================================================

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Authenticate user with enhanced capabilities"""
    if username in DEMO_USERS:
        user_data = DEMO_USERS[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if password_hash == user_data["password_hash"]:
            return {
                "username": username,
                "plan": user_data["plan"],
                "plan_details": SUBSCRIPTION_PLANS[user_data["plan"]],
                "api_key": user_data.get("api_key", ""),
                "session_start": datetime.now(),
                "created_date": user_data["created_date"]
            }
    return None

def initialize_session(user):
    """Initialize enhanced session"""
    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.messages = {}
    st.session_state.uploaded_files = {}
    st.session_state.current_bot = "Startup Strategist"
    st.session_state.usage_stats = {
        "total_cost": 0.0,
        "daily_cost": 0.0,
        "total_tokens": 0,
        "requests_count": 0,
        "files_processed": 0,
        "last_reset": datetime.now().date()
    }
    
    # Initialize API
    api_key = user.get("api_key", "demo_key")
    model = user.get("model_preference", "gpt-3.5-turbo")
    api_manager.initialize(api_key, model)

# ======================================================
# 🎨 ENHANCED UI COMPONENTS
# ======================================================

def render_file_upload_section():
    """Render comprehensive file upload section"""
    st.sidebar.markdown("### 📁 File Upload")
    
    user = st.session_state.user
    plan_details = user["plan_details"]
    
    # Upload limits info
    st.sidebar.info(f"""
    **Upload Limits ({user['plan']} Plan)**
    • Max file size: {plan_details['max_file_size_mb']}MB
    • Max files per chat: {plan_details['max_files_per_chat']}
    """)
    
    # File uploader
    uploaded_files = st.sidebar.file_uploader(
        "Upload files for analysis",
        accept_multiple_files=True,
        type=['txt', 'pdf', 'docx', 'csv', 'xlsx', 'json', 'xml', 'jpg', 'png', 'py', 'sql'],
        help="Upload documents, data files, images, or code for AI analysis"
    )
    
    current_bot = st.session_state.current_bot
    
    if uploaded_files:
        # Check limits
        if len(uploaded_files) > plan_details['max_files_per_chat']:
            st.sidebar.error(f"Too many files! Max {plan_details['max_files_per_chat']} files per chat.")
            return
        
        # Process files
        if current_bot not in st.session_state.uploaded_files:
            st.session_state.uploaded_files[current_bot] = []
        
        processed_files = []
        
        for uploaded_file in uploaded_files:
            # Check file size
            if uploaded_file.size > plan_details['max_file_size_mb'] * 1024 * 1024:
                st.sidebar.error(f"File {uploaded_file.name} too large! Max {plan_details['max_file_size_mb']}MB")
                continue
            
            # Process file
            with st.sidebar.spinner(f"Processing {uploaded_file.name}..."):
                file_info = file_processor.process_uploaded_file(uploaded_file)
                processed_files.append(file_info)
        
        # Update session state
        st.session_state.uploaded_files[current_bot] = processed_files
        st.session_state.usage_stats["files_processed"] += len(processed_files)
        
        # Show processed files
        st.sidebar.success(f"✅ Processed {len(processed_files)} files")
        
        for file_info in processed_files:
            with st.sidebar.expander(f"📄 {file_info['name']}"):
                st.write(f"**Type:** {file_info['file_type']}")
                st.write(f"**Size:** {file_info['size']:,} bytes")
                if file_info['error']:
                    st.error(f"Error: {file_info['error']}")
                else:
                    st.write(f"**Content preview:**")
                    st.text(file_info['content'][:200] + "..." if len(file_info['content']) > 200 else file_info['content'])
    
    # Show current files
    if current_bot in st.session_state.uploaded_files and st.session_state.uploaded_files[current_bot]:
        st.sidebar.markdown("**Current Files:**")
        for file_info in st.session_state.uploaded_files[current_bot]:
            st.sidebar.write(f"📄 {file_info['name']} ({file_info['file_type']})")
        
        if st.sidebar.button("🗑️ Clear Files"):
            st.session_state.uploaded_files[current_bot] = []
            st.rerun()

def render_usage_dashboard():
    """Render enhanced usage dashboard"""
    user = st.session_state.user
    stats = st.session_state.usage_stats
    plan_details = user["plan_details"]
    
    st.sidebar.markdown("### 📊 Usage Dashboard")
    
    # Plan info
    st.sidebar.info(f"**{user['plan']} Plan**")
    
    # Daily budget progress
    if plan_details["daily_budget"] != float('inf'):
        daily_progress = min(stats["daily_cost"] / plan_details["daily_budget"], 1.0)
        st.sidebar.progress(daily_progress)
        st.sidebar.caption(f"Daily: ${stats['daily_cost']:.3f} / ${plan_details['daily_budget']:.2f}")
    
    # Metrics
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Total Cost", f"${stats['total_cost']:.3f}")
        st.metric("Files", stats['files_processed'])
    
    with col2:
        st.metric("Tokens", f"{stats['total_tokens']:,}")
        st.metric("Requests", stats['requests_count'])

def render_bot_selector():
    """Render enhanced bot selector"""
    st.sidebar.markdown("### 🤖 AI Assistant")
    
    # Category filter
    categories = list(set([bot["category"] for bot in ENHANCED_BOT_PERSONALITIES.values()]))
    selected_category = st.sidebar.selectbox("Category", ["All"] + sorted(categories))
    
    # Filter bots
    filtered_bots = {}
    for name, bot in ENHANCED_BOT_PERSONALITIES.items():
        if selected_category == "All" or bot["category"] == selected_category:
            filtered_bots[name] = bot
    
    # Bot selection
    bot_names = list(filtered_bots.keys())
    current_bot = st.session_state.current_bot
    
    if current_bot not in bot_names:
        current_bot = bot_names[0] if bot_names else "Startup Strategist"
    
    selected_bot = st.sidebar.selectbox("Select Assistant", bot_names, 
                                       index=bot_names.index(current_bot) if current_bot in bot_names else 0)
    
    if selected_bot != st.session_state.current_bot:
        st.session_state.current_bot = selected_bot
        st.rerun()
    
    # Bot info
    if selected_bot in ENHANCED_BOT_PERSONALITIES:
        bot_config = ENHANCED_BOT_PERSONALITIES[selected_bot]
        
        st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        ">
            <h4 style="margin: 0; color: white;">{bot_config['emoji']} {selected_bot}</h4>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9em;">{bot_config['category']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.sidebar.expander("ℹ️ Assistant Details"):
            st.write(f"**Description:** {bot_config['description']}")
            st.write(f"**Specialties:** {', '.join(bot_config['specialties'])}")

# ======================================================
# 🔐 AUTHENTICATION PAGE
# ======================================================

def authentication_page():
    """Enhanced authentication page"""
    st.title("🚀 Enhanced AI Chat Platform")
    st.markdown("**Real API Integration • File Upload • Personal AI Assistants**")
    
    # Features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🤖 **Personal AI Assistants**
        - 25+ specialized experts
        - Shorter, focused prompts
        - Real personality traits
        """)
    
    with col2:
        st.markdown("""
        ### 📁 **File Upload Support**
        - PDF, Word, Excel, CSV
        - Images and data files
        - Real-time processing
        """)
    
    with col3:
        st.markdown("""
        ### ⚡ **Real API Integration**
        - OpenAI GPT-4 & GPT-3.5
        - Accurate token counting
        - Cost tracking
        """)
    
    # Login form
    with st.form("login_form"):
        st.markdown("### 🔐 Login")
        
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
        
        with col2:
            api_key = st.text_input("OpenAI API Key (Optional)", type="password")
            model = st.selectbox("AI Model", ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"])
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            demo_button = st.form_submit_button("🎮 Demo Mode", use_container_width=True)
    
    # Handle authentication
    if login_button and username and password:
        user = authenticate_user(username, password)
        if user:
            user["api_key"] = api_key if api_key else "demo_key"
            user["model_preference"] = model
            initialize_session(user)
            st.rerun()
        else:
            st.error("Invalid credentials")
    
    elif demo_button:
        demo_user = {
            "username": "demo_user",
            "plan": "Pro",
            "plan_details": SUBSCRIPTION_PLANS["Pro"],
            "api_key": "demo_key",
            "model_preference": "gpt-3.5-turbo",
            "session_start": datetime.now(),
            "created_date": datetime.now() - timedelta(days=7)
        }
        initialize_session(demo_user)
        st.rerun()
    
    # Demo credentials
    st.markdown("---")
    st.markdown("### 🎯 Demo Credentials")
    
    cred_cols = st.columns(3)
    credentials = [
        ("Basic", "demo", "demo123"),
        ("Pro", "premium", "premium123"),
        ("Enterprise", "enterprise", "enterprise123")
    ]
    
    for i, (plan, user, pwd) in enumerate(credentials):
        with cred_cols[i]:
            st.info(f"**{plan} Plan**\nUser: `{user}`\nPass: `{pwd}`")
    
    # Subscription plans
    st.markdown("### 💎 Subscription Plans")
    
    plan_cols = st.columns(len(SUBSCRIPTION_PLANS))
    for idx, (plan_name, plan_details) in enumerate(SUBSCRIPTION_PLANS.items()):
        with plan_cols[idx]:
            st.markdown(f"""
            <div style="
                border: 2px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                height: 250px;
                background: white;
                margin-bottom: 10px;
            ">
                <h3>{plan_name}</h3>
                <p><strong>${plan_details['monthly_budget']:.0f}/mo</strong></p>
                <p>{plan_details['max_tokens_per_request']:,} tokens/request</p>
                <p>{plan_details['max_file_size_mb']}MB max file size</p>
                <p>{plan_details['max_files_per_chat']} files per chat</p>
                <p>{len(plan_details['available_models'])} AI models</p>
            </div>
            """, unsafe_allow_html=True)

# ======================================================
# 💬 ENHANCED CHAT INTERFACE
# ======================================================

def chat_interface():
    """Enhanced chat interface with file upload"""
    user = st.session_state.user
    
    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("💬 AI Chat with File Upload")
    with col2:
        if st.button("📊 Analytics"):
            st.session_state.current_page = "analytics"
            st.rerun()
    with col3:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # User info
    is_demo = user.get("api_key") == "demo_key"
    demo_badge = " 🎮 (Demo)" if is_demo else " ⚡ (Live API)"
    st.caption(f"Welcome **{user['username']}**{demo_badge} | Plan: **{user['plan']}**")
    
    if is_demo:
        st.info("🎮 **Demo Mode** - Add your OpenAI API key in the sidebar for real AI responses!")
    
    # Sidebar
    with st.sidebar:
        # API Key input for live users
        if is_demo:
            st.markdown("### 🔑 API Configuration")
            new_api_key = st.text_input("OpenAI API Key", type="password", 
                                       help="Enter your OpenAI API key for real responses")
            new_model = st.selectbox("AI Model", ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"])
            
            if st.button("🔄 Update API"):
                if new_api_key:
                    user["api_key"] = new_api_key
                    user["model_preference"] = new_model
                    if api_manager.initialize(new_api_key, new_model):
                        st.success("✅ API updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to initialize API")
        
        # Bot selector
        render_bot_selector()
        
        # File upload
        render_file_upload_section()
        
        # Usage dashboard
        render_usage_dashboard()
        
        # Chat controls
        st.markdown("### 🔧 Chat Controls")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat"):
                current_bot = st.session_state.current_bot
                if current_bot in st.session_state.messages:
                    del st.session_state.messages[current_bot]
                if current_bot in st.session_state.uploaded_files:
                    del st.session_state.uploaded_files[current_bot]
                st.rerun()
        
        with col2:
            if st.button("💾 Export"):
                current_bot = st.session_state.current_bot
                export_data = {
                    "bot": current_bot,
                    "messages": st.session_state.messages.get(current_bot, []),
                    "files": st.session_state.uploaded_files.get(current_bot, []),
                    "timestamp": datetime.now().isoformat(),
                    "user": user["username"]
                }
                st.download_button(
                    "📥 Download",
                    json.dumps(export_data, indent=2),
                    file_name=f"chat_{current_bot}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    # Main chat area
    current_bot = st.session_state.current_bot
    
    # Initialize messages if not exists
    if current_bot not in st.session_state.messages:
        st.session_state.messages[current_bot] = []
    
    messages = st.session_state.messages[current_bot]
    uploaded_files = st.session_state.uploaded_files.get(current_bot, [])
    
    # Display messages
    if messages:
        st.markdown(f"### 💬 Chat with {current_bot}")
        
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show metadata for assistant messages
                if message["role"] == "assistant" and "metadata" in message:
                    metadata = message["metadata"]
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                    with col2:
                        st.caption(f"🔢 {metadata.get('total_tokens', 0)} tokens")
                    with col3:
                        st.caption(f"🤖 {metadata.get('model', 'demo')}")
                    with col4:
                        if metadata.get('demo_mode'):
                            st.caption("🎮 Demo")
                        else:
                            st.caption("⚡ Live")
    else:
        st.markdown(f"### 💬 Start chatting with {current_bot}")
        
        # Show bot info and suggestions
        if current_bot in ENHANCED_BOT_PERSONALITIES:
            bot_config = ENHANCED_BOT_PERSONALITIES[current_bot]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                margin: 20px 0;
            ">
                <h3 style="margin: 0; color: white;">{bot_config['emoji']} {current_bot}</h3>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">{bot_config['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Suggested questions
            st.markdown("**💡 Try asking:**")
            suggestions = [
                f"How can you help me with {bot_config['specialties'][0].lower()}?",
                "What's your approach to solving problems in this area?",
                "Can you analyze my situation and provide recommendations?"
            ]
            
            if uploaded_files:
                suggestions.append("Can you analyze my uploaded files?")
            
            for suggestion in suggestions:
                if st.button(suggestion, key=f"suggestion_{suggestion[:20]}"):
                    # Add as user message
                    st.session_state.messages[current_bot].append({
                        "role": "user",
                        "content": suggestion
                    })
                    st.rerun()
    
    # Show uploaded files info
    if uploaded_files:
        st.markdown("### 📁 Uploaded Files")
        file_cols = st.columns(min(len(uploaded_files), 4))
        
        for i, file_info in enumerate(uploaded_files):
            with file_cols[i % 4]:
                st.markdown(f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 10px;
                    margin: 5px 0;
                    background: #f8f9fa;
                ">
                    <strong>📄 {file_info['name']}</strong><br>
                    <small>{file_info['file_type']} • {file_info['size']:,} bytes</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input(f"Ask {current_bot} anything... (files will be included automatically)"):
        # Add user message
        st.session_state.messages[current_bot].append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                # Prepare messages for API
                api_messages = []
                
                # Add system prompt
                bot_config = ENHANCED_BOT_PERSONALITIES[current_bot]
                system_content = bot_config["system_prompt"]
                
                # Add file context if files are uploaded
                if uploaded_files:
                    file_context = "\n\nUploaded Files Context:\n"
                    for file_info in uploaded_files:
                        if not file_info.get('error'):
                            file_context += f"\n--- {file_info['name']} ({file_info['file_type']}) ---\n"
                            file_context += file_info['content'][:2000]  # Limit content length
                            if len(file_info['content']) > 2000:
                                file_context += "\n[Content truncated...]"
                            file_context += "\n"
                    
                    system_content += file_context
                
                api_messages.append({"role": "system", "content": system_content})
                
                # Add conversation history (last 10 messages to stay within limits)
                recent_messages = messages[-10:] if len(messages) > 10 else messages
                for msg in recent_messages:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                # Add current user message
                api_messages.append({"role": "user", "content": prompt})
                
                # Generate response
                model = user.get("model_preference", "gpt-3.5-turbo")
                max_tokens = user["plan_details"]["max_tokens_per_request"]
                
                response, metadata = api_manager.generate_response(
                    api_messages, 
                    model=model, 
                    max_tokens=max_tokens
                )
                
                st.markdown(response)
                
                # Show metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                with col2:
                    st.caption(f"🔢 {metadata.get('total_tokens', 0)} tokens")
                with col3:
                    if metadata.get('demo_mode'):
                        st.caption("🎮 Demo Mode")
                    else:
                        st.caption("⚡ Live API")
                
                # Add assistant message
                st.session_state.messages[current_bot].append({
                    "role": "assistant",
                    "content": response,
                    "metadata": metadata
                })
                
                # Update usage stats
                update_usage_stats(metadata)
        
        st.rerun()

def update_usage_stats(metadata):
    """Update usage statistics"""
    stats = st.session_state.usage_stats
    
    # Reset daily stats if new day
    if stats["last_reset"] != datetime.now().date():
        stats["daily_cost"] = 0.0
        stats["last_reset"] = datetime.now().date()
    
    # Update stats
    cost = metadata.get("cost", 0.0)
    tokens = metadata.get("total_tokens", 0)
    
    stats["total_cost"] += cost
    stats["daily_cost"] += cost
    stats["total_tokens"] += tokens
    stats["requests_count"] += 1

# ======================================================
# 📊 ANALYTICS PAGE
# ======================================================

def analytics_page():
    """Enhanced analytics page"""
    st.title("📊 Analytics Dashboard")
    st.markdown("Comprehensive insights into your AI chat usage and file processing")
    
    user = st.session_state.user
    stats = st.session_state.usage_stats
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Conversations", stats['requests_count'])
    
    with col2:
        st.metric("Total Cost", f"${stats['total_cost']:.3f}")
    
    with col3:
        st.metric("Files Processed", stats['files_processed'])
    
    with col4:
        avg_tokens = stats['total_tokens'] / max(stats['requests_count'], 1)
        st.metric("Avg Tokens/Chat", f"{avg_tokens:.0f}")
    
    # Usage breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💬 Chat Activity")
        
        # Bot usage
        bot_usage = {}
        for bot_name in st.session_state.messages:
            bot_usage[bot_name] = len(st.session_state.messages[bot_name])
        
        if bot_usage:
            sorted_bots = sorted(bot_usage.items(), key=lambda x: x[1], reverse=True)
            for bot_name, message_count in sorted_bots[:5]:
                st.write(f"🤖 **{bot_name}**: {message_count} messages")
        else:
            st.info("No chat activity yet")
    
    with col2:
        st.markdown("### 📁 File Processing")
        
        # File type breakdown
        file_types = {}
        for bot_files in st.session_state.uploaded_files.values():
            for file_info in bot_files:
                file_type = file_info['file_type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
        
        if file_types:
            for file_type, count in file_types.items():
                st.write(f"📄 **{file_type.title()}**: {count} files")
        else:
            st.info("No files processed yet")
    
    # Plan usage
    st.markdown("### 💎 Plan Usage")
    plan_details = user["plan_details"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        daily_usage = stats["daily_cost"] / plan_details["daily_budget"] * 100
        st.progress(min(daily_usage / 100, 1.0))
        st.caption(f"Daily Budget: {daily_usage:.1f}% used")
    
    with col2:
        st.write(f"**Max File Size**: {plan_details['max_file_size_mb']}MB")
        st.write(f"**Max Files/Chat**: {plan_details['max_files_per_chat']}")
    
    with col3:
        st.write(f"**Available Models**: {len(plan_details['available_models'])}")
        st.write(f"**Max Tokens**: {plan_details['max_tokens_per_request']:,}")
    
    # Export options
    st.markdown("### 📥 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Analytics"):
            analytics_data = {
                "user": user["username"],
                "plan": user["plan"],
                "stats": stats,
                "bot_usage": bot_usage,
                "file_types": file_types,
                "export_timestamp": datetime.now().isoformat()
            }
            st.download_button(
                "Download Analytics",
                json.dumps(analytics_data, indent=2),
                file_name=f"analytics_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("💬 Export All Chats"):
            all_chats = {
                "user": user["username"],
                "chats": st.session_state.messages,
                "files": st.session_state.uploaded_files,
                "export_timestamp": datetime.now().isoformat()
            }
            st.download_button(
                "Download All Chats",
                json.dumps(all_chats, indent=2),
                file_name=f"all_chats_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()

# ======================================================
# 🚀 MAIN APPLICATION
# ======================================================

def main():
    """Enhanced main application"""
    # Page configuration
    st.set_page_config(
        page_title="Enhanced AI Chat with File Upload",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        border-radius: 25px;
        border: none;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "chat"
    
    # Main application logic
    if not st.session_state.authenticated:
        authentication_page()
    else:
        # Navigation
        if st.session_state.current_page == "analytics":
            analytics_page()
        else:
            chat_interface()

if __name__ == "__main__":
    main()

