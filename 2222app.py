#!/usr/bin/env python3
"""
🚀 FIXED CHAT BOT - DEPLOYMENT READY
Real OpenAI API integration with comprehensive file upload and professional AI assistants
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

# OpenAI imports
try:
    from openai import OpenAI
    import tiktoken
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# File processing imports
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from PIL import Image
    IMAGE_AVAILABLE = True
except ImportError:
    IMAGE_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from openpyxl import load_workbook
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

import csv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🔐 CONFIGURATION MANAGEMENT
# ======================================================

def load_config():
    """Load configuration from Streamlit secrets or environment variables"""
    try:
        config = {
            "api_key": st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")),
            "model": st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")),
            "max_tokens": int(st.secrets.get("MAX_TOKENS", os.getenv("MAX_TOKENS", "2000"))),
            "temperature": float(st.secrets.get("TEMPERATURE", os.getenv("TEMPERATURE", "0.7"))),
            "max_file_size_mb": int(st.secrets.get("MAX_FILE_SIZE_MB", os.getenv("MAX_FILE_SIZE_MB", "50"))),
            "max_files_per_chat": int(st.secrets.get("MAX_FILES_PER_CHAT", os.getenv("MAX_FILES_PER_CHAT", "10"))),
            "app_name": st.secrets.get("APP_NAME", os.getenv("APP_NAME", "AI Chat Bot")),
            "debug_mode": st.secrets.get("DEBUG_MODE", os.getenv("DEBUG_MODE", "false")).lower() == "true"
        }
        return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        return {
            "api_key": "",
            "model": "gpt-3.5-turbo",
            "max_tokens": 2000,
            "temperature": 0.7,
            "max_file_size_mb": 50,
            "max_files_per_chat": 10,
            "app_name": "AI Chat Bot",
            "debug_mode": False
        }

CONFIG = load_config()

# ======================================================
# 🤖 AI ASSISTANTS CONFIGURATION
# ======================================================

AI_ASSISTANTS = {
    "Business Strategist": {
        "description": "Strategic business advisor with expertise in growth planning and market analysis.",
        "system_prompt": "You are a strategic business advisor with 15+ years of experience. Provide actionable business insights, strategic recommendations, and growth strategies. Be analytical yet practical.",
        "emoji": "🎯",
        "category": "Strategy",
        "specialties": ["Strategic Planning", "Market Analysis", "Business Growth", "Competitive Intelligence"]
    },
    
    "Marketing Expert": {
        "description": "Digital marketing specialist focused on customer acquisition and growth marketing.",
        "system_prompt": "You are a digital marketing expert focused on measurable results. Provide data-driven marketing strategies, campaign optimization tips, and growth tactics. Always include actionable metrics.",
        "emoji": "📈",
        "category": "Marketing",
        "specialties": ["Digital Marketing", "Customer Acquisition", "Growth Hacking", "Campaign Optimization"]
    },
    
    "Sales Coach": {
        "description": "Sales performance expert helping maximize revenue through proven methodologies.",
        "system_prompt": "You are a sales coach focused on results. Provide practical sales techniques, objection handling strategies, and pipeline management advice. Be motivational and action-oriented.",
        "emoji": "💰",
        "category": "Sales",
        "specialties": ["Sales Process", "Objection Handling", "Pipeline Management", "Closing Techniques"]
    },
    
    "Financial Advisor": {
        "description": "Financial planning expert optimizing business finances and investment strategies.",
        "system_prompt": "You are a financial advisor focused on business growth. Provide financial planning advice, investment guidance, and cost optimization strategies. Be detail-oriented and practical.",
        "emoji": "💼",
        "category": "Finance",
        "specialties": ["Financial Planning", "Investment Strategy", "Cost Optimization", "Budget Management"]
    },
    
    "Operations Manager": {
        "description": "Process optimization expert streamlining operations for maximum efficiency.",
        "system_prompt": "You are an operations manager focused on efficiency. Provide process improvements, workflow optimization, and operational excellence strategies. Think systematically about solutions.",
        "emoji": "⚙️",
        "category": "Operations",
        "specialties": ["Process Optimization", "Workflow Management", "Quality Control", "Efficiency Improvement"]
    },
    
    "Tech Consultant": {
        "description": "Technology advisor helping businesses leverage digital transformation.",
        "system_prompt": "You are a technology consultant focused on practical solutions. Provide guidance on digital transformation, tech strategy, and innovation. Focus on business value and ROI.",
        "emoji": "💻",
        "category": "Technology",
        "specialties": ["Digital Transformation", "Tech Strategy", "Innovation", "System Architecture"]
    },
    
    "HR Specialist": {
        "description": "Human resources expert focused on talent management and organizational development.",
        "system_prompt": "You are an HR specialist focused on people and culture. Provide guidance on talent management, team building, and organizational development. Be people-focused and empathetic.",
        "emoji": "👥",
        "category": "Human Resources",
        "specialties": ["Talent Management", "Team Building", "Performance Management", "Culture Development"]
    },
    
    "Customer Success Manager": {
        "description": "Customer experience expert ensuring satisfaction and value realization.",
        "system_prompt": "You are a customer success manager focused on customer outcomes. Provide strategies for customer retention, satisfaction, and value delivery. Always think customer-first.",
        "emoji": "🤝",
        "category": "Customer Success",
        "specialties": ["Customer Retention", "Value Delivery", "Relationship Management", "Customer Analytics"]
    },
    
    "Data Analyst": {
        "description": "Data science expert turning raw data into actionable business insights.",
        "system_prompt": "You are a data analyst focused on insights. Provide data analysis guidance, visualization recommendations, and actionable insights. Always validate data quality first.",
        "emoji": "📊",
        "category": "Analytics",
        "specialties": ["Data Analysis", "Visualization", "Statistical Modeling", "Business Intelligence"]
    },
    
    "Content Creator": {
        "description": "Content strategy expert creating engaging content across multiple channels.",
        "system_prompt": "You are a content creator focused on engagement. Provide content strategies, creation tips, and distribution guidance. Think about audience value and engagement first.",
        "emoji": "✍️",
        "category": "Content",
        "specialties": ["Content Strategy", "Content Creation", "SEO Optimization", "Multi-channel Distribution"]
    }
}

# ======================================================
# 🔧 API MANAGER
# ======================================================

class APIManager:
    def __init__(self):
        self.client = None
        self.encoding = None
        self.config = CONFIG
        self.initialize_client()
        
    def initialize_client(self):
        """Initialize OpenAI client"""
        try:
            if not OPENAI_AVAILABLE:
                logger.warning("OpenAI library not available")
                return False
                
            if self.config["api_key"]:
                self.client = OpenAI(api_key=self.config["api_key"])
                try:
                    self.encoding = tiktoken.encoding_for_model(self.config["model"])
                except:
                    self.encoding = tiktoken.get_encoding("cl100k_base")
                
                # Test connection
                try:
                    test_response = self.client.chat.completions.create(
                        model=self.config["model"],
                        messages=[{"role": "user", "content": "Test"}],
                        max_tokens=10
                    )
                    logger.info("OpenAI API initialized successfully")
                    return True
                except Exception as e:
                    logger.error(f"API test failed: {str(e)}")
                    return False
            else:
                logger.warning("No OpenAI API key found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI API: {str(e)}")
            self.client = None
            self.encoding = None
            return False
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            if self.encoding:
                return len(self.encoding.encode(text))
            else:
                return len(text) // 4  # Rough estimation
        except:
            return len(text) // 4
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate API usage cost"""
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
        }
        
        model_pricing = pricing.get(model, pricing["gpt-3.5-turbo"])
        input_cost = (input_tokens / 1000) * model_pricing["input"]
        output_cost = (output_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def generate_response(self, messages: List[Dict], assistant_config: Dict) -> Tuple[str, Dict]:
        """Generate response using OpenAI API"""
        try:
            if not self.client:
                return self.generate_demo_response(messages, assistant_config)
            
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            
            response_time = time.time() - start_time
            
            content = response.choices[0].message.content
            usage = response.usage
            
            cost = self.calculate_cost(
                usage.prompt_tokens,
                usage.completion_tokens,
                self.config["model"]
            )
            
            metadata = {
                "model": self.config["model"],
                "input_tokens": usage.prompt_tokens,
                "output_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "cost": cost,
                "response_time": response_time,
                "api_status": "success",
                "demo_mode": False
            }
            
            return content, metadata
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            error_response = f"I apologize, but I encountered an API error: {str(e)}"
            
            return error_response, {
                "model": "error",
                "input_tokens": 0,
                "output_tokens": len(error_response.split()),
                "total_tokens": len(error_response.split()),
                "cost": 0.0,
                "response_time": 0.0,
                "api_status": "error",
                "error": str(e),
                "demo_mode": True
            }
    
    def generate_demo_response(self, messages: List[Dict], assistant_config: Dict) -> Tuple[str, Dict]:
        """Generate demo response when API is not available"""
        user_message = messages[-1]["content"] if messages else "Hello"
        assistant_name = assistant_config.get("emoji", "🤖") + " " + assistant_config.get("category", "Assistant")
        specialties = ", ".join(assistant_config.get("specialties", []))
        
        response = f"""Hello! I'm your {assistant_name} ready to help with {specialties.lower()}.

**Your message:** "{user_message[:100]}..."

🔑 **API Key Required** - Add your OpenAI API key for real AI responses!

**To activate real API:**
1. Add OPENAI_API_KEY to your environment variables or Streamlit secrets
2. Restart the application
3. Experience full AI-powered conversations

**In the full version, I would:**
✅ Provide expert analysis using real AI capabilities
✅ Process your uploaded files with advanced understanding
✅ Generate detailed recommendations based on my expertise
✅ Offer actionable insights tailored to your situation

**My expertise areas:**
{chr(10).join([f"• {specialty}" for specialty in assistant_config.get('specialties', [])])}

This demo shows the interface. Real responses will be comprehensive and valuable!"""

        metadata = {
            "model": "demo",
            "input_tokens": len(user_message.split()),
            "output_tokens": len(response.split()),
            "total_tokens": len(user_message.split()) + len(response.split()),
            "cost": 0.0,
            "response_time": 0.5,
            "api_status": "demo",
            "demo_mode": True
        }
        
        return response, metadata

# Initialize API manager
api_manager = APIManager()

# ======================================================
# 📁 FILE PROCESSOR
# ======================================================

class FileProcessor:
    def __init__(self):
        self.supported_types = {
            'text': ['.txt', '.md', '.csv', '.json', '.xml', '.html', '.css', '.js', '.py', '.sql'],
            'document': ['.pdf', '.docx', '.doc'],
            'spreadsheet': ['.xlsx', '.xls'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'data': ['.json', '.xml', '.yaml', '.yml']
        }
        self.max_file_size = CONFIG["max_file_size_mb"] * 1024 * 1024
        self.max_files_per_chat = CONFIG["max_files_per_chat"]
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type from extension"""
        ext = os.path.splitext(filename)[1].lower()
        
        for file_type, extensions in self.supported_types.items():
            if ext in extensions:
                return file_type
        
        return 'unknown'
    
    def validate_file(self, uploaded_file) -> Tuple[bool, str]:
        """Validate uploaded file"""
        if uploaded_file.size > self.max_file_size:
            return False, f"File too large. Max size: {CONFIG['max_file_size_mb']}MB"
        
        file_type = self.get_file_type(uploaded_file.name)
        if file_type == 'unknown':
            return False, f"Unsupported file type: {os.path.splitext(uploaded_file.name)[1]}"
        
        return True, "Valid file"
    
    def process_uploaded_file(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded file and extract content"""
        try:
            is_valid, validation_message = self.validate_file(uploaded_file)
            if not is_valid:
                return {
                    'name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'type': uploaded_file.type,
                    'file_type': 'error',
                    'content': '',
                    'summary': '',
                    'error': validation_message,
                    'processed_at': datetime.now().isoformat()
                }
            
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
            
            # Extract content based on file type
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
            file_info['summary'] = self.generate_file_summary(file_info)
            
            return file_info
            
        except Exception as e:
            logger.error(f"Error processing file {uploaded_file.name}: {str(e)}")
            return {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': 'error',
                'content': '',
                'summary': '',
                'error': str(e),
                'processed_at': datetime.now().isoformat()
            }
    
    def generate_file_summary(self, file_info: Dict) -> str:
        """Generate a summary of the file content"""
        try:
            content = file_info['content']
            file_type = file_info['file_type']
            
            if file_type == 'text':
                lines = content.split('\n')
                return f"Text file with {len(lines)} lines, {len(content)} characters"
            elif file_type == 'document':
                words = len(content.split())
                return f"Document with approximately {words} words"
            elif file_type == 'spreadsheet':
                return "Spreadsheet data processed and analyzed"
            elif file_type == 'image':
                return "Image file uploaded and metadata extracted"
            elif file_type == 'data':
                return "Data file processed and structure analyzed"
            else:
                return "File processed successfully"
                
        except Exception:
            return "File summary generation failed"
    
    def process_text_file(self, uploaded_file) -> str:
        """Process text-based files"""
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    content = uploaded_file.read().decode(encoding)
                    uploaded_file.seek(0)
                    return content
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    continue
            
            return "Could not decode file content"
            
        except Exception as e:
            return f"Error reading text file: {str(e)}"
    
    def process_document_file(self, uploaded_file) -> str:
        """Process document files"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.pdf' and PDF_AVAILABLE:
                return self.process_pdf(uploaded_file)
            elif file_extension in ['.docx', '.doc'] and DOCX_AVAILABLE:
                return self.process_docx(uploaded_file)
            else:
                return f"Document processing not available for {file_extension}"
                
        except Exception as e:
            return f"Error processing document: {str(e)}"
    
    def process_pdf(self, uploaded_file) -> str:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---\n{text}")
                except Exception as e:
                    text_content.append(f"--- Page {page_num + 1} ---\nError: {str(e)}")
            
            return "\n\n".join(text_content) if text_content else "No text content found"
            
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
            
            return "\n\n".join(text_content) if text_content else "No text content found"
            
        except Exception as e:
            return f"Error processing DOCX: {str(e)}"
    
    def process_spreadsheet_file(self, uploaded_file) -> str:
        """Process spreadsheet files"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.csv':
                return self.process_csv(uploaded_file)
            elif file_extension in ['.xlsx', '.xls'] and EXCEL_AVAILABLE:
                return self.process_excel(uploaded_file)
            else:
                return f"Spreadsheet processing not available for {file_extension}"
                
        except Exception as e:
            return f"Error processing spreadsheet: {str(e)}"
    
    def process_csv(self, uploaded_file) -> str:
        """Process CSV file"""
        try:
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            
            csv_reader = csv.reader(StringIO(content))
            rows = list(csv_reader)
            
            if not rows:
                return "Empty CSV file"
            
            analysis = f"CSV File Analysis:\n"
            analysis += f"- Total rows: {len(rows)}\n"
            analysis += f"- Total columns: {len(rows[0]) if rows else 0}\n\n"
            
            if rows:
                analysis += f"Headers: {', '.join(rows[0])}\n\n"
            
            analysis += "Sample data (first 5 rows):\n"
            for i, row in enumerate(rows[:6]):
                analysis += f"Row {i}: {', '.join(str(cell) for cell in row)}\n"
            
            if len(rows) > 6:
                analysis += f"... and {len(rows) - 6} more rows\n"
            
            return analysis
            
        except Exception as e:
            return f"Error processing CSV: {str(e)}"
    
    def process_excel(self, uploaded_file) -> str:
        """Process Excel file"""
        try:
            workbook = load_workbook(uploaded_file, data_only=True)
            analysis = f"Excel File Analysis:\n"
            analysis += f"- Worksheets: {len(workbook.sheetnames)}\n"
            analysis += f"- Sheet names: {', '.join(workbook.sheetnames)}\n\n"
            
            for sheet_name in workbook.sheetnames[:3]:
                sheet = workbook[sheet_name]
                analysis += f"Sheet '{sheet_name}':\n"
                analysis += f"- Max row: {sheet.max_row}\n"
                analysis += f"- Max column: {sheet.max_column}\n"
                
                analysis += "Sample data (first 5 rows):\n"
                for row_num in range(1, min(6, sheet.max_row + 1)):
                    row_data = []
                    for col_num in range(1, min(6, sheet.max_column + 1)):
                        cell_value = sheet.cell(row=row_num, column=col_num).value
                        row_data.append(str(cell_value) if cell_value is not None else "")
                    analysis += f"Row {row_num}: {' | '.join(row_data)}\n"
                
                analysis += "\n"
            
            return analysis
            
        except Exception as e:
            return f"Error processing Excel: {str(e)}"
    
    def process_image_file(self, uploaded_file) -> str:
        """Process image files"""
        try:
            if not IMAGE_AVAILABLE:
                return "Image processing not available (PIL not installed)"
                
            image = Image.open(uploaded_file)
            
            analysis = f"Image Analysis:\n"
            analysis += f"- Format: {image.format}\n"
            analysis += f"- Size: {image.size[0]} x {image.size[1]} pixels\n"
            analysis += f"- Mode: {image.mode}\n"
            analysis += f"- File size: {uploaded_file.size:,} bytes\n"
            
            width, height = image.size
            aspect_ratio = width / height
            analysis += f"- Aspect ratio: {aspect_ratio:.2f}:1\n"
            
            analysis += "\nImage uploaded successfully for AI analysis."
            
            return analysis
            
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    def process_data_file(self, uploaded_file) -> str:
        """Process data files"""
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.json':
                return self.process_json(uploaded_file)
            elif file_extension in ['.xml']:
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
            
            analysis = f"JSON File Analysis:\n"
            analysis += f"- Root type: {type(data).__name__}\n"
            analysis += f"- File size: {len(content):,} characters\n"
            
            if isinstance(data, dict):
                analysis += f"- Top-level keys: {len(data.keys())}\n"
                analysis += f"- Keys: {', '.join(list(data.keys())[:10])}\n"
            elif isinstance(data, list):
                analysis += f"- Array items: {len(data)}\n"
            
            analysis += f"\nContent preview:\n{json.dumps(data, indent=2)[:500]}"
            if len(json.dumps(data, indent=2)) > 500:
                analysis += "..."
            
            return analysis
            
        except Exception as e:
            return f"Error processing JSON: {str(e)}"
    
    def process_xml(self, uploaded_file) -> str:
        """Process XML file"""
        try:
            content = uploaded_file.read().decode('utf-8')
            
            analysis = f"XML File Analysis:\n"
            analysis += f"- File size: {len(content):,} characters\n"
            
            root_tag_start = content.find('<')
            root_tag_end = content.find('>', root_tag_start)
            if root_tag_start != -1 and root_tag_end != -1:
                root_tag = content[root_tag_start:root_tag_end+1]
                analysis += f"- Root element: {root_tag}\n"
            
            analysis += f"\nContent preview:\n{content[:500]}"
            if len(content) > 500:
                analysis += "..."
            
            return analysis
            
        except Exception as e:
            return f"Error processing XML: {str(e)}"

# Initialize file processor
file_processor = FileProcessor()

# ======================================================
# 🎨 UI COMPONENTS
# ======================================================

def render_app_header():
    """Render application header"""
    st.title(f"🚀 {CONFIG['app_name']}")
    st.markdown("**AI Chat Bot with File Upload • Real OpenAI API Integration**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if CONFIG["api_key"]:
            if api_manager.client:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        else:
            st.warning("🔑 API Key Required")
    
    with col2:
        st.info(f"🤖 Model: {CONFIG['model']}")
    
    with col3:
        st.info(f"🔧 Max Tokens: {CONFIG['max_tokens']:,}")

def render_assistant_selector():
    """Render assistant selector"""
    st.sidebar.markdown("### 🤖 AI Assistants")
    
    categories = list(set([assistant["category"] for assistant in AI_ASSISTANTS.values()]))
    selected_category = st.sidebar.selectbox("Category", ["All"] + sorted(categories))
    
    filtered_assistants = {}
    for name, assistant in AI_ASSISTANTS.items():
        if selected_category == "All" or assistant["category"] == selected_category:
            filtered_assistants[name] = assistant
    
    assistant_names = list(filtered_assistants.keys())
    current_assistant = st.session_state.get("current_assistant", assistant_names[0] if assistant_names else "Business Strategist")
    
    if current_assistant not in assistant_names:
        current_assistant = assistant_names[0] if assistant_names else "Business Strategist"
    
    selected_assistant = st.sidebar.selectbox(
        "Select Assistant", 
        assistant_names, 
        index=assistant_names.index(current_assistant) if current_assistant in assistant_names else 0
    )
    
    if selected_assistant != st.session_state.get("current_assistant"):
        st.session_state.current_assistant = selected_assistant
        st.rerun()
    
    if selected_assistant in AI_ASSISTANTS:
        assistant_config = AI_ASSISTANTS[selected_assistant]
        
        st.sidebar.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 10px;
            color: white;
            margin: 10px 0;
        ">
            <h4 style="margin: 0; color: white;">{assistant_config['emoji']} {selected_assistant}</h4>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9em;">{assistant_config['category']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.sidebar.expander("ℹ️ Assistant Details"):
            st.write(f"**Description:** {assistant_config['description']}")
            st.write(f"**Specialties:** {', '.join(assistant_config['specialties'])}")

def render_file_upload_section():
    """Render file upload section"""
    st.sidebar.markdown("### 📁 File Upload")
    
    st.sidebar.info(f"""
    **Upload Limits**
    • Max file size: {CONFIG['max_file_size_mb']}MB
    • Max files per chat: {CONFIG['max_files_per_chat']}
    """)
    
    uploaded_files = st.sidebar.file_uploader(
        "Upload files for analysis",
        accept_multiple_files=True,
        type=['txt', 'pdf', 'docx', 'csv', 'xlsx', 'json', 'xml', 'jpg', 'png', 'py', 'js', 'html'],
        help="Upload documents, data files, images, or code for AI analysis"
    )
    
    current_assistant = st.session_state.get("current_assistant", "Business Strategist")
    
    if uploaded_files:
        if len(uploaded_files) > CONFIG['max_files_per_chat']:
            st.sidebar.error(f"Too many files! Max {CONFIG['max_files_per_chat']} files per chat.")
            return
        
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = {}
        
        if current_assistant not in st.session_state.uploaded_files:
            st.session_state.uploaded_files[current_assistant] = []
        
        processed_files = []
        
        for uploaded_file in uploaded_files:
            with st.sidebar.spinner(f"Processing {uploaded_file.name}..."):
                file_info = file_processor.process_uploaded_file(uploaded_file)
                processed_files.append(file_info)
        
        st.session_state.uploaded_files[current_assistant] = processed_files
        
        successful_files = [f for f in processed_files if not f.get('error')]
        failed_files = [f for f in processed_files if f.get('error')]
        
        if successful_files:
            st.sidebar.success(f"✅ Processed {len(successful_files)} files")
        
        if failed_files:
            st.sidebar.error(f"❌ Failed {len(failed_files)} files")
        
        for file_info in processed_files:
            with st.sidebar.expander(f"📄 {file_info['name']}"):
                if file_info.get('error'):
                    st.error(f"Error: {file_info['error']}")
                else:
                    st.write(f"**Type:** {file_info['file_type'].title()}")
                    st.write(f"**Size:** {file_info['size']:,} bytes")
                    st.write(f"**Summary:** {file_info['summary']}")
    
    current_files = st.session_state.get("uploaded_files", {}).get(current_assistant, [])
    if current_files:
        st.sidebar.markdown("**Current Files:**")
        for file_info in current_files:
            status_icon = "✅" if not file_info.get('error') else "❌"
            st.sidebar.write(f"{status_icon} {file_info['name']}")
        
        if st.sidebar.button("🗑️ Clear Files"):
            st.session_state.uploaded_files[current_assistant] = []
            st.rerun()

def render_usage_stats():
    """Render usage statistics"""
    st.sidebar.markdown("### 📊 Usage Stats")
    
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "files_processed": 0
        }
    
    stats = st.session_state.usage_stats
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric("Requests", stats["total_requests"])
        st.metric("Files", stats["files_processed"])
    
    with col2:
        st.metric("Tokens", f"{stats['total_tokens']:,}")
        st.metric("Cost", f"${stats['total_cost']:.4f}")

# ======================================================
# 💬 MAIN CHAT INTERFACE
# ======================================================

def main_chat_interface():
    """Main chat interface"""
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if "current_assistant" not in st.session_state:
        st.session_state.current_assistant = "Business Strategist"
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "files_processed": 0
        }
    
    render_app_header()
    
    with st.sidebar:
        render_assistant_selector()
        render_file_upload_section()
        render_usage_stats()
        
        st.markdown("### 🔧 Controls")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear"):
                current_assistant = st.session_state.current_assistant
                if current_assistant in st.session_state.messages:
                    del st.session_state.messages[current_assistant]
                st.rerun()
        
        with col2:
            if st.button("💾 Export"):
                current_assistant = st.session_state.current_assistant
                export_data = {
                    "assistant": current_assistant,
                    "messages": st.session_state.messages.get(current_assistant, []),
                    "files": st.session_state.get("uploaded_files", {}).get(current_assistant, []),
                    "timestamp": datetime.now().isoformat()
                }
                
                st.download_button(
                    "📥 Download",
                    json.dumps(export_data, indent=2),
                    file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    current_assistant = st.session_state.current_assistant
    
    if current_assistant not in st.session_state.messages:
        st.session_state.messages[current_assistant] = []
    
    messages = st.session_state.messages[current_assistant]
    uploaded_files = st.session_state.get("uploaded_files", {}).get(current_assistant, [])
    
    if messages:
        st.markdown(f"### 💬 Chat with {current_assistant}")
        
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                if message["role"] == "assistant" and "metadata" in message:
                    metadata = message["metadata"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                    with col2:
                        st.caption(f"🔢 {metadata.get('total_tokens', 0):,}")
                    with col3:
                        if metadata.get('demo_mode'):
                            st.caption("🎮 Demo")
                        else:
                            st.caption("⚡ API")
    else:
        st.markdown(f"### 💬 Start chatting with {current_assistant}")
        
        if current_assistant in AI_ASSISTANTS:
            assistant_config = AI_ASSISTANTS[current_assistant]
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                margin: 20px 0;
            ">
                <h3 style="margin: 0; color: white;">{assistant_config['emoji']} {current_assistant}</h3>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">{assistant_config['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**💡 Try asking:**")
            suggestions = [
                f"How can you help me with {assistant_config['specialties'][0].lower()}?",
                "What's your approach to solving problems?",
                "Can you analyze my situation?"
            ]
            
            if uploaded_files:
                suggestions.append("Please analyze my uploaded files.")
            
            for i, suggestion in enumerate(suggestions):
                if st.button(suggestion, key=f"suggestion_{i}"):
                    st.session_state.messages[current_assistant].append({
                        "role": "user",
                        "content": suggestion
                    })
                    st.rerun()
    
    if uploaded_files:
        st.markdown("### 📁 Uploaded Files")
        
        for file_info in uploaded_files:
            if not file_info.get('error'):
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
    
    if prompt := st.chat_input(f"Ask {current_assistant} anything..."):
        st.session_state.messages[current_assistant].append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner(f"🤔 {current_assistant} is thinking..."):
                api_messages = []
                
                assistant_config = AI_ASSISTANTS[current_assistant]
                system_content = assistant_config["system_prompt"]
                
                if uploaded_files:
                    successful_files = [f for f in uploaded_files if not f.get('error')]
                    
                    if successful_files:
                        file_context = "\n\nUploaded Files Context:\n"
                        
                        for file_info in successful_files:
                            file_context += f"\n--- {file_info['name']} ({file_info['file_type']}) ---\n"
                            file_context += f"Summary: {file_info['summary']}\n"
                            
                            content = file_info['content']
                            if len(content) > 2000:
                                content = content[:2000] + "\n[Content truncated...]"
                            
                            file_context += f"Content:\n{content}\n"
                        
                        system_content += file_context
                
                api_messages.append({"role": "system", "content": system_content})
                
                recent_messages = messages[-10:] if len(messages) > 10 else messages
                for msg in recent_messages:
                    api_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
                
                api_messages.append({"role": "user", "content": prompt})
                
                response, metadata = api_manager.generate_response(api_messages, assistant_config)
                
                st.markdown(response)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                with col2:
                    st.caption(f"🔢 {metadata.get('total_tokens', 0):,}")
                with col3:
                    if metadata.get('demo_mode'):
                        st.caption("🎮 Demo")
                    else:
                        st.caption("⚡ API")
                
                st.session_state.messages[current_assistant].append({
                    "role": "assistant",
                    "content": response,
                    "metadata": metadata
                })
                
                stats = st.session_state.usage_stats
                stats["total_requests"] += 1
                stats["total_tokens"] += metadata.get("total_tokens", 0)
                stats["total_cost"] += metadata.get("cost", 0.0)
                stats["files_processed"] = len(uploaded_files)
        
        st.rerun()

# ======================================================
# 🚀 MAIN APPLICATION
# ======================================================

def main():
    """Main application"""
    st.set_page_config(
        page_title=CONFIG["app_name"],
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
    <style>
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if CONFIG["debug_mode"]:
        st.sidebar.markdown("### 🐛 Debug Info")
        debug_info = {
            "API Key": "✅ Present" if CONFIG["api_key"] else "❌ Missing",
            "OpenAI Available": "✅ Yes" if OPENAI_AVAILABLE else "❌ No",
            "Client Status": "✅ Connected" if api_manager.client else "❌ Not Connected"
        }
        
        for key, value in debug_info.items():
            st.sidebar.write(f"**{key}:** {value}")
    
    main_chat_interface()

if __name__ == "__main__":
    main()


