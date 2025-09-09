#!/usr/bin/env python3
"""
Advanced AI Chatbot Application - Full Production Version
Complete file upload, real API integration, and multi-personality system
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
import traceback
from io import StringIO, BytesIO
import base64
import tempfile
import mimetypes

# Core imports with error handling
try:
    from openai import OpenAI
    import tiktoken
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import PyPDF2
    from PIL import Image
    import docx
    from openpyxl import load_workbook
    PDF_PROCESSING = True
except ImportError:
    PDF_PROCESSING = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# App Configuration
st.set_page_config(
    page_title="AI Chatbot Platform",
    page_icon="🤖",
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
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        border-radius: 25px;
        border: none;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        padding: 0.5rem 2rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f3e5f5 0%, #e8f5e8 100%);
        border-left: 4px solid #9c27b0;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
        text-align: center;
    }
    
    .file-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid #dee2e6;
    }
    
    .bot-personality {
        background: linear-gradient(135deg, #fff3e0 0%, #fce4ec 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# BOT PERSONALITIES - ENHANCED
# ======================================================

BOT_PERSONALITIES = {
    "Business Strategist": {
        "description": "Expert in business strategy, planning, market analysis, and growth optimization",
        "system_prompt": """You are a senior business strategist with 15+ years of experience in Fortune 500 companies. 
        You specialize in:
        - Strategic planning and execution
        - Market analysis and competitive intelligence
        - Business model innovation
        - Growth strategies and scaling
        - Financial planning and ROI optimization
        - Risk assessment and mitigation
        
        Provide actionable, data-driven advice with specific frameworks and methodologies. Always consider market conditions, competitive landscape, and financial implications.""",
        "emoji": "📊",
        "category": "Business",
        "color": "#2196F3"
    },
    
    "Technical Consultant": {
        "description": "Software architecture, development best practices, and technical problem solving",
        "system_prompt": """You are a senior technical consultant and software architect with expertise in:
        - Full-stack development and system architecture
        - Cloud platforms (AWS, Azure, GCP)
        - DevOps and CI/CD pipelines
        - Database design and optimization
        - Security best practices
        - Performance optimization and scalability
        - Modern frameworks and technologies
        
        Provide detailed technical guidance with code examples, architectural diagrams concepts, and best practices. Focus on scalable, maintainable solutions.""",
        "emoji": "💻",
        "category": "Technology",
        "color": "#4CAF50"
    },
    
    "Data Analyst": {
        "description": "Advanced data analysis, machine learning, and business intelligence",
        "system_prompt": """You are a senior data analyst and data scientist with expertise in:
        - Statistical analysis and hypothesis testing
        - Machine learning and predictive modeling
        - Data visualization and storytelling
        - Business intelligence and KPI development
        - Python, R, SQL, and advanced analytics tools
        - A/B testing and experimentation
        - Big data processing and analytics
        
        Help users analyze data, create insights, and make data-driven decisions. Provide specific methodologies and visualization recommendations.""",
        "emoji": "📈",
        "category": "Analytics",
        "color": "#FF9800"
    },
    
    "Marketing Expert": {
        "description": "Digital marketing strategy, growth hacking, and brand development",
        "system_prompt": """You are a marketing expert specializing in digital growth strategies with experience in:
        - Digital marketing campaigns and optimization
        - Content marketing and SEO strategies
        - Social media marketing and community building
        - Email marketing and marketing automation
        - Paid advertising (Google Ads, Facebook Ads, etc.)
        - Conversion rate optimization
        - Brand positioning and messaging
        - Growth hacking and viral marketing
        
        Provide data-driven marketing strategies with specific tactics, metrics, and ROI considerations.""",
        "emoji": "🎯",
        "category": "Marketing",
        "color": "#E91E63"
    },
    
    "Financial Advisor": {
        "description": "Investment strategy, financial planning, and economic analysis",
        "system_prompt": """You are a certified financial advisor and investment strategist with expertise in:
        - Investment portfolio management and asset allocation
        - Financial planning and retirement strategies
        - Risk management and insurance planning
        - Tax optimization strategies
        - Corporate finance and valuation
        - Economic analysis and market trends
        - Alternative investments and emerging markets
        
        Provide balanced financial advice considering risk tolerance, time horizons, and market conditions. Always emphasize diversification and long-term thinking.""",
        "emoji": "💰",
        "category": "Finance",
        "color": "#795548"
    },
    
    "Project Manager": {
        "description": "Project planning, team coordination, and delivery optimization",
        "system_prompt": """You are a certified PMP project manager with experience in Agile, Scrum, and traditional methodologies:
        - Project planning and scope management
        - Resource allocation and team coordination
        - Risk management and issue resolution
        - Stakeholder communication and management
        - Budget and timeline optimization
        - Quality assurance and delivery
        - Change management and process improvement
        
        Help with project planning, team dynamics, and delivery optimization using proven methodologies and best practices.""",
        "emoji": "🗂️",
        "category": "Management",
        "color": "#9C27B0"
    },
    
    "Creative Director": {
        "description": "Brand design, creative strategy, and content development",
        "system_prompt": """You are a creative director with expertise in:
        - Brand identity and visual design
        - Creative strategy and concept development
        - Content creation and storytelling
        - User experience and interface design
        - Campaign ideation and execution
        - Team leadership and creative processes
        
        Provide creative solutions with strategic thinking, focusing on brand consistency and audience engagement.""",
        "emoji": "🎨",
        "category": "Creative",
        "color": "#FF5722"
    },
    
    "HR Consultant": {
        "description": "Human resources, talent management, and organizational development",
        "system_prompt": """You are an HR consultant specializing in:
        - Talent acquisition and retention strategies
        - Performance management systems
        - Organizational development and culture
        - Employee engagement and satisfaction
        - Compensation and benefits design
        - Training and development programs
        - Conflict resolution and mediation
        
        Provide people-focused solutions that balance business needs with employee wellbeing.""",
        "emoji": "👥",
        "category": "Human Resources",
        "color": "#607D8B"
    }
}

# ======================================================
# PRICING AND PLANS
# ======================================================

PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006}
}

SUBSCRIPTION_PLANS = {
    "Starter": {
        "monthly_budget": 10.00,
        "daily_budget": 1.00,
        "max_tokens": 4000,
        "max_file_size": 10,
        "max_files": 5,
        "models": ["gpt-3.5-turbo", "gpt-4o-mini"],
        "features": ["Basic chat", "File upload", "Export conversations"]
    },
    "Professional": {
        "monthly_budget": 50.00,
        "daily_budget": 5.00,
        "max_tokens": 8000,
        "max_file_size": 50,
        "max_files": 20,
        "models": ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
        "features": ["Advanced chat", "Large file processing", "Analytics dashboard", "API access"]
    },
    "Enterprise": {
        "monthly_budget": 200.00,
        "daily_budget": 20.00,
        "max_tokens": 16000,
        "max_file_size": 200,
        "max_files": 100,
        "models": ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4"],
        "features": ["Unlimited chat", "Bulk processing", "Custom integrations", "Priority support"]
    }
}

# ======================================================
# API MANAGER - ENHANCED
# ======================================================

class APIManager:
    def __init__(self):
        self.client = None
        self.encoding = None
        self.initialized = False
        self.current_model = "gpt-3.5-turbo"
        
    def initialize(self, api_key: str, model: str = "gpt-3.5-turbo") -> bool:
        """Initialize OpenAI client with enhanced error handling"""
        try:
            if not OPENAI_AVAILABLE:
                st.error("⚠️ OpenAI package not installed. Install with: `pip install openai`")
                return False
                
            if not api_key or len(api_key) < 10:
                st.error("❌ Please enter a valid OpenAI API key")
                return False
                
            if not api_key.startswith('sk-'):
                st.error("❌ Invalid API key format. OpenAI keys start with 'sk-'")
                return False
                
            # Initialize client with timeout and retry settings
            self.client = OpenAI(
                api_key=api_key,
                timeout=60.0,
                max_retries=3
            )
            
            # Test connection with minimal token usage
            test_response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5,
                temperature=0
            )
            
            if test_response.choices and test_response.choices[0].message:
                try:
                    self.encoding = tiktoken.encoding_for_model(model)
                except:
                    self.encoding = tiktoken.get_encoding("cl100k_base")
                    
                self.current_model = model
                self.initialized = True
                logger.info(f"✅ API initialized successfully with {model}")
                return True
                
        except Exception as e:
            error_msg = str(e).lower()
            if "401" in error_msg or "authentication" in error_msg:
                st.error("❌ Invalid API key - Please check your OpenAI API key")
            elif "429" in error_msg or "rate" in error_msg:
                st.error("⚠️ Rate limit exceeded - Please try again in a moment")
            elif "insufficient_quota" in error_msg or "quota" in error_msg:
                st.error("💳 Insufficient OpenAI credits - Please add credits to your account")
            elif "model" in error_msg:
                st.error(f"❌ Model {model} not available - Please select a different model")
            else:
                st.error(f"❌ API Error: {error_msg}")
                
            logger.error(f"API initialization failed: {error_msg}")
            self.initialized = False
            return False
    
    def count_tokens(self, text: str) -> int:
        """Accurate token counting"""
        try:
            if self.encoding and text:
                return len(self.encoding.encode(str(text)))
            # Fallback estimation
            return max(int(len(str(text).split()) * 1.3), 1)
        except:
            return max(int(len(str(text).split()) * 1.3), 1)
    
    def generate_response(self, messages: List[Dict], model: str, max_tokens: int = 2000, 
                         temperature: float = 0.7) -> Tuple[str, Dict]:
        """Generate AI response with comprehensive error handling"""
        try:
            if not self.client or not self.initialized:
                return "❌ API not initialized. Please configure your OpenAI API key in the sidebar.", {
                    "model": "error",
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "cost": 0.0,
                    "error": True
                }
            
            # Validate inputs
            if not messages:
                return "❌ No messages to process.", {"error": True}
            
            # Real API call with streaming support
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=min(max_tokens, 4000),  # Safety limit
                temperature=max(0, min(temperature, 1)),  # Clamp temperature
                stream=False  # Set to True for streaming in future versions
            )
            
            if not response.choices or not response.choices[0].message:
                return "❌ No response generated from API", {"error": True}
            
            content = response.choices[0].message.content or "Empty response received"
            usage = response.usage
            
            # Calculate accurate cost
            pricing = PRICING.get(model, PRICING["gpt-3.5-turbo"])
            cost = (usage.prompt_tokens * pricing["input"] + 
                   usage.completion_tokens * pricing["output"]) / 1000
            
            metadata = {
                "model": model,
                "input_tokens": usage.prompt_tokens,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "cost": cost,
                "timestamp": datetime.now().isoformat(),
                "finish_reason": response.choices[0].finish_reason
            }
            
            logger.info(f"Response generated: {usage.total_tokens} tokens, ${cost:.4f}")
            return content, metadata
                
        except Exception as e:
            error_msg = str(e).lower()
            
            if "context_length_exceeded" in error_msg:
                error_response = f"❌ Message too long for {model}. Please shorten your input or try a model with larger context."
            elif "rate_limit_exceeded" in error_msg:
                error_response = "⚠️ Rate limit exceeded. Please wait a moment before sending another message."
            elif "insufficient_quota" in error_msg:
                error_response = "💳 Insufficient OpenAI credits. Please add credits to your account."
            elif "invalid_api_key" in error_msg:
                error_response = "❌ Invalid API key. Please check your OpenAI API key."
            else:
                error_response = f"❌ Error generating response: {str(e)}"
            
            logger.error(f"Response generation failed: {str(e)}")
            
            return error_response, {
                "model": "error",
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost": 0.0,
                "error": True,
                "error_message": str(e)
            }

# Initialize API manager
api_manager = APIManager()

# ======================================================
# FILE PROCESSOR - ENHANCED
# ======================================================

class FileProcessor:
    def __init__(self):
        self.supported_types = {
            'text': ['.txt', '.md', '.csv', '.json', '.py', '.js', '.html', '.css', '.xml', '.yaml', '.yml'],
            'document': ['.pdf', '.docx', '.doc', '.rtf'],
            'spreadsheet': ['.xlsx', '.xls', '.csv', '.ods'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'data': ['.json', '.xml', '.yaml', '.yml', '.sql']
        }
        self.max_content_length = 10000  # Limit content length for context
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type with enhanced detection"""
        ext = os.path.splitext(filename.lower())[1]
        for file_type, extensions in self.supported_types.items():
            if ext in extensions:
                return file_type
        return 'unknown'
    
    def is_supported(self, filename: str) -> bool:
        """Check if file type is supported"""
        return self.get_file_type(filename) != 'unknown'
    
    def process_file(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded file with comprehensive error handling"""
        try:
            file_info = {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': self.get_file_type(uploaded_file.name),
                'content': '',
                'summary': '',
                'error': None,
                'processed_at': datetime.now().isoformat()
            }
            
            if not self.is_supported(uploaded_file.name):
                file_info['error'] = f"Unsupported file type: {os.path.splitext(uploaded_file.name)[1]}"
                return file_info
            
            # Process based on file type
            if file_info['file_type'] == 'text':
                file_info['content'] = self._process_text_file(uploaded_file)
            elif file_info['file_type'] == 'document':
                file_info['content'] = self._process_document(uploaded_file)
            elif file_info['file_type'] == 'spreadsheet':
                file_info['content'] = self._process_spreadsheet(uploaded_file)
            elif file_info['file_type'] == 'image':
                file_info['content'] = self._process_image(uploaded_file)
            
            # Generate summary
            if file_info['content'] and not file_info['error']:
                file_info['summary'] = self._generate_summary(file_info)
                
            return file_info
            
        except Exception as e:
            logger.error(f"File processing error for {uploaded_file.name}: {str(e)}")
            return {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': 'error',
                'content': '',
                'summary': '',
                'error': f"Processing failed: {str(e)}",
                'processed_at': datetime.now().isoformat()
            }
    
    def _process_text_file(self, uploaded_file) -> str:
        """Process text files with encoding detection"""
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                uploaded_file.seek(0)
                content = uploaded_file.read().decode(encoding)
                # Limit content length
                if len(content) > self.max_content_length:
                    content = content[:self.max_content_length] + f"\n... (truncated from {len(content)} characters)"
                return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Text file processing error: {str(e)}")
                continue
        
        return "❌ Could not decode file content with any supported encoding"
    
    def _process_document(self, uploaded_file) -> str:
        """Process document files with enhanced extraction"""
        if not PDF_PROCESSING:
            return "❌ Document processing libraries not available. Install: pip install PyPDF2 python-docx pillow openpyxl"
            
        try:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext == '.pdf':
                return self._extract_pdf_content(uploaded_file)
            elif file_ext in ['.docx', '.doc']:
                return self._extract_docx_content(uploaded_file)
            else:
                return f"❌ Unsupported document format: {file_ext}"
                
        except Exception as e:
            logger.error(f"Document processing error: {str(e)}")
            return f"❌ Error processing document: {str(e)}"
    
    def _extract_pdf_content(self, uploaded_file) -> str:
        """Extract text from PDF with page limits"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            total_pages = len(pdf_reader.pages)
            
            text = f"📄 PDF Document: {total_pages} pages\n\n"
            
            # Process first 10 pages or all pages if less
            pages_to_process = min(10, total_pages)
            
            for i in range(pages_to_process):
                page_text = pdf_reader.pages[i].extract_text()
                if page_text.strip():
                    text += f"--- Page {i+1} ---\n{page_text.strip()}\n\n"
            
            if total_pages > 10:
                text += f"... (showing first 10 of {total_pages} pages)"
            
            # Limit total length
            if len(text) > self.max_content_length:
                text = text[:self.max_content_length] + "\n... (content truncated)"
                
            return text
            
        except Exception as e:
            return f"❌ PDF extraction failed: {str(e)}"
    
    def _extract_docx_content(self, uploaded_file) -> str:
        """Extract text from Word documents"""
        try:
            doc = docx.Document(uploaded_file)
            
            text = "📝 Word Document Content:\n\n"
            
            # Extract paragraphs
            paragraphs_processed = 0
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text.strip() + "\n\n"
                    paragraphs_processed += 1
                    
                    # Limit number of paragraphs
                    if paragraphs_processed >= 50:
                        text += "... (content truncated to first 50 paragraphs)"
                        break
            
            # Extract tables
            if doc.tables:
                text += "\n📊 Tables found in document:\n"
                for i, table in enumerate(doc.tables[:3]):  # First 3 tables
                    text += f"\nTable {i+1}:\n"
                    for row in table.rows[:5]:  # First 5 rows
                        row_text = " | ".join([cell.text.strip() for cell in row.cells])
                        text += f"{row_text}\n"
            
            # Limit total length
            if len(text) > self.max_content_length:
                text = text[:self.max_content_length] + "\n... (content truncated)"
                
            return text
            
        except Exception as e:
            return f"❌ Word document extraction failed: {str(e)}"
    
    def _process_spreadsheet(self, uploaded_file) -> str:
        """Process spreadsheet files with data analysis"""
        try:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext == '.csv':
                return self._process_csv_file(uploaded_file)
            else:
                return self._process_excel_file(uploaded_file)
                
        except Exception as e:
            logger.error(f"Spreadsheet processing error: {str(e)}")
            return f"❌ Error processing spreadsheet: {str(e)}"
    
    def _process_csv_file(self, uploaded_file) -> str:
        """Process CSV files with analysis"""
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, nrows=1000)  # Limit rows
            
            analysis = f"📊 CSV Analysis: {uploaded_file.name}\n\n"
            analysis += f"📏 Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
            analysis += f"📋 Columns: {', '.join(df.columns.tolist())}\n\n"
            
            # Data types
            analysis += "📊 Data Types:\n"
            for col, dtype in df.dtypes.items():
                analysis += f"  • {col}: {dtype}\n"
            
            # Basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                analysis += f"\n📈 Numeric Summary:\n"
                summary_stats = df[numeric_cols].describe()
                analysis += summary_stats.to_string()
            
            # Sample data
            analysis += f"\n\n📋 Sample Data (first 5 rows):\n"
            analysis += df.head().to_string()
            
            # Check for missing values
            missing_values = df.isnull().sum()
            if missing_values.sum() > 0:
                analysis += f"\n\n⚠️ Missing Values:\n"
                for col, missing in missing_values.items():
                    if missing > 0:
                        analysis += f"  • {col}: {missing} missing\n"
            
            return analysis
            
        except Exception as e:
            return f"❌ CSV processing failed: {str(e)}"
    
    def _process_excel_file(self, uploaded_file) -> str:
        """Process Excel files with sheet analysis"""
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            
            analysis = f"📊 Excel Analysis: {uploaded_file.name}\n\n"
            analysis += f"📑 Sheets: {len(sheet_names)} ({', '.join(sheet_names)})\n\n"
            
            # Process first sheet or up to 3 sheets
            sheets_to_process = min(3, len(sheet_names))
            
            for i in range(sheets_to_process):
                sheet_name = sheet_names[i]
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name, nrows=100)
                
                analysis += f"📋 Sheet: '{sheet_name}'\n"
                analysis += f"  📏 Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"
                analysis += f"  📊 Columns: {', '.join(df.columns.tolist()[:10])}\n"
                
                if len(df.columns) > 10:
                    analysis += f"  ... and {len(df.columns) - 10} more columns\n"
                
                # Sample data from first sheet
                if i == 0:
                    analysis += f"\n📋 Sample Data:\n"
                    analysis += df.head(3).to_string()
                
                analysis += "\n\n"
            
            if len(sheet_names) > 3:
                analysis += f"... and {len(sheet_names) - 3} more sheets\n"
            
            return analysis
            
        except Exception as e:
            return f"❌ Excel processing failed: {str(e)}"
    
    def _process_image(self, uploaded_file) -> str:
        """Process image files with metadata extraction"""
        try:
            if PDF_PROCESSING:
                image = Image.open(uploaded_file)
                
                analysis = f"🖼️ Image Analysis: {uploaded_file.name}\n\n"
                analysis += f"📏 Dimensions: {image.size[0]} × {image.size[1]} pixels\n"
                analysis += f"🎨 Format: {image.format}\n"
                analysis += f"🎭 Mode: {image.mode}\n"
                
                # File size
                file_size_mb = uploaded_file.size / (1024 * 1024)
                analysis += f"💾 Size: {file_size_mb:.2f} MB\n"
                
                # Additional metadata if available
                if hasattr(image, '_getexif') and image._getexif():
                    analysis += "\n📊
