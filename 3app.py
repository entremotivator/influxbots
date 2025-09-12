#!/usr/bin/env python3
"""
Advanced AI Chatbot Application
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
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .chat-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# BOT PERSONALITIES
# ======================================================

BOT_PERSONALITIES = {
    "Business Strategist": {
        "description": "Expert in business strategy, planning, and growth optimization",
        "system_prompt": "You are a business strategist with 15+ years of experience. Provide actionable advice on strategy, planning, and growth. Be direct and focus on practical solutions.",
        "emoji": "📊",
        "category": "Business"
    },
    "Technical Consultant": {
        "description": "Software development, architecture, and technical problem solving",
        "system_prompt": "You are a senior technical consultant specializing in software development and system architecture. Provide clear technical guidance with code examples when helpful.",
        "emoji": "💻",
        "category": "Technology"
    },
    "Data Analyst": {
        "description": "Data analysis, visualization, and insights extraction",
        "system_prompt": "You are a data analyst expert. Help users understand their data, create visualizations, and extract actionable insights. Focus on practical analysis techniques.",
        "emoji": "📈",
        "category": "Analytics"
    },
    "Marketing Expert": {
        "description": "Digital marketing, content strategy, and growth marketing",
        "system_prompt": "You are a marketing expert focused on digital growth strategies. Provide data-driven marketing advice with emphasis on ROI and measurable results.",
        "emoji": "🎯",
        "category": "Marketing"
    },
    "Financial Advisor": {
        "description": "Financial planning, investment strategy, and economic analysis",
        "system_prompt": "You are a financial advisor with expertise in investment strategy and financial planning. Provide balanced advice considering risk management and growth objectives.",
        "emoji": "💰",
        "category": "Finance"
    },
    "Project Manager": {
        "description": "Project planning, team coordination, and delivery optimization",
        "system_prompt": "You are an experienced project manager. Help with project planning, risk management, and team coordination using proven methodologies like Agile and Waterfall.",
        "emoji": "🗂️",
        "category": "Management"
    }
}

# ======================================================
# PRICING CONFIGURATION
# ======================================================

PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002}
}

SUBSCRIPTION_PLANS = {
    "Free": {
        "monthly_budget": 5.00,
        "daily_budget": 0.50,
        "max_tokens": 2000,
        "max_file_size": 5,
        "max_files": 3,
        "models": ["gpt-3.5-turbo"]
    },
    "Pro": {
        "monthly_budget": 50.00,
        "daily_budget": 5.00,
        "max_tokens": 8000,
        "max_file_size": 25,
        "max_files": 10,
        "models": ["gpt-3.5-turbo", "gpt-4-turbo"]
    },
    "Enterprise": {
        "monthly_budget": 200.00,
        "daily_budget": 20.00,
        "max_tokens": 16000,
        "max_file_size": 100,
        "max_files": 50,
        "models": ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4"]
    }
}

# ======================================================
# API MANAGER
# ======================================================

class APIManager:
    def __init__(self):
        self.client = None
        self.encoding = None
        self.initialized = False
        
    def initialize(self, api_key: str, model: str = "gpt-3.5-turbo") -> bool:
        """Initialize OpenAI client"""
        try:
            if not OPENAI_AVAILABLE:
                st.error("OpenAI package not installed. Please install: pip install openai")
                return False
                
            if not api_key or api_key == "demo_key":
                self.client = None
                self.encoding = None
                self.initialized = True
                logger.info("Demo mode initialized")
                return True
                
            if not api_key.startswith('sk-'):
                st.error("Invalid API key format. OpenAI keys start with 'sk-'")
                return False
                
            # Initialize client
            self.client = OpenAI(
                api_key=api_key,
                timeout=30.0,
                max_retries=2
            )
            
            # Test connection
            test_response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            if test_response.choices:
                try:
                    self.encoding = tiktoken.encoding_for_model(model)
                except:
                    self.encoding = tiktoken.get_encoding("cl100k_base")
                    
                self.initialized = True
                logger.info(f"API initialized successfully with {model}")
                return True
                
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                st.error("Invalid API key")
            elif "429" in error_msg:
                st.error("Rate limit exceeded")
            elif "insufficient_quota" in error_msg:
                st.error("Insufficient OpenAI credits")
            else:
                st.error(f"API Error: {error_msg}")
                
            logger.error(f"API initialization failed: {error_msg}")
            self.initialized = False
            return False
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            if self.encoding:
                return len(self.encoding.encode(str(text)))
            return int(len(str(text).split()) * 1.3)
        except:
            return int(len(str(text).split()) * 1.3)
    
    def generate_response(self, messages: List[Dict], model: str, max_tokens: int = 2000, 
                         temperature: float = 0.7) -> Tuple[str, Dict]:
        """Generate AI response"""
        try:
            if self.client and self.initialized:
                # Real API call
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                content = response.choices[0].message.content or "No response generated"
                usage = response.usage
                
                # Calculate cost
                pricing = PRICING.get(model, PRICING["gpt-3.5-turbo"])
                cost = (usage.prompt_tokens * pricing["input"] + 
                       usage.completion_tokens * pricing["output"]) / 1000
                
                metadata = {
                    "model": model,
                    "input_tokens": usage.prompt_tokens,
                    "output_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                    "cost": cost,
                    "demo_mode": False
                }
                
                return content, metadata
                
            else:
                # Demo response
                user_msg = messages[-1]["content"] if messages else ""
                return self._demo_response(user_msg), {
                    "model": "demo",
                    "input_tokens": self.count_tokens(user_msg),
                    "output_tokens": 150,
                    "total_tokens": self.count_tokens(user_msg) + 150,
                    "cost": 0.0,
                    "demo_mode": True
                }
                
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return error_msg, {
                "model": "error",
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost": 0.0,
                "error": True
            }
    
    def _demo_response(self, user_message: str) -> str:
        """Generate demo response"""
        return f"""Thank you for your message: "{user_message[:50]}..."

**Demo Mode Active**

This is a demonstration response. With a real OpenAI API key, you would receive:

• Detailed, contextual analysis of your question
• Professional expertise tailored to the selected bot personality  
• File analysis and processing capabilities
• Real-time interaction with advanced AI models

**To activate full functionality:**
1. Get an OpenAI API key from platform.openai.com
2. Enter it in the API Configuration section
3. Start getting real AI-powered responses

The interface you see is fully functional - only the AI responses are simulated in demo mode."""

# Initialize API manager
api_manager = APIManager()

# ======================================================
# FILE PROCESSOR
# ======================================================

class FileProcessor:
    def __init__(self):
        self.supported_types = {
            'text': ['.txt', '.md', '.csv', '.json', '.py', '.js', '.html', '.css'],
            'document': ['.pdf', '.docx', '.doc'],
            'spreadsheet': ['.xlsx', '.xls', '.csv'],
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'data': ['.json', '.xml', '.yaml', '.yml']
        }
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type"""
        ext = os.path.splitext(filename)[1].lower()
        for file_type, extensions in self.supported_types.items():
            if ext in extensions:
                return file_type
        return 'unknown'
    
    def process_file(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded file"""
        try:
            file_info = {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': self.get_file_type(uploaded_file.name),
                'content': '',
                'error': None
            }
            
            if file_info['file_type'] == 'text':
                file_info['content'] = self._process_text_file(uploaded_file)
            elif file_info['file_type'] == 'document':
                file_info['content'] = self._process_document(uploaded_file)
            elif file_info['file_type'] == 'spreadsheet':
                file_info['content'] = self._process_spreadsheet(uploaded_file)
            elif file_info['file_type'] == 'image':
                file_info['content'] = self._process_image(uploaded_file)
            else:
                file_info['content'] = f"File type not supported: {uploaded_file.name}"
                
            return file_info
            
        except Exception as e:
            logger.error(f"File processing error: {str(e)}")
            return {
                'name': uploaded_file.name,
                'size': uploaded_file.size,
                'type': uploaded_file.type,
                'file_type': 'error',
                'content': '',
                'error': str(e)
            }
    
    def _process_text_file(self, uploaded_file) -> str:
        """Process text files"""
        try:
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            return content[:5000]  # Limit content length
        except UnicodeDecodeError:
            try:
                uploaded_file.seek(0)
                content = uploaded_file.read().decode('latin-1')
                uploaded_file.seek(0)
                return content[:5000]
            except:
                return "Could not decode file content"
    
    def _process_document(self, uploaded_file) -> str:
        """Process document files"""
        if not PDF_PROCESSING:
            return "PDF processing libraries not available"
            
        try:
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_ext == '.pdf':
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages[:5]:  # Limit to first 5 pages
                    text += page.extract_text() + "\n"
                return text[:5000]
                
            elif file_ext == '.docx':
                doc = docx.Document(uploaded_file)
                text = ""
                for paragraph in doc.paragraphs[:50]:  # Limit paragraphs
                    text += paragraph.text + "\n"
                return text[:5000]
                
        except Exception as e:
            return f"Error processing document: {str(e)}"
    
    def _process_spreadsheet(self, uploaded_file) -> str:
        """Process spreadsheet files"""
        try:
            if uploaded_file.name.endswith('.csv'):
                content = uploaded_file.read().decode('utf-8')
                uploaded_file.seek(0)
                lines = content.split('\n')[:20]  # First 20 rows
                return f"CSV Preview (first 20 rows):\n" + "\n".join(lines)
            else:
                df = pd.read_excel(uploaded_file, nrows=20)
                return f"Excel Preview:\nShape: {df.shape}\nColumns: {list(df.columns)}\n\nFirst 5 rows:\n{df.head().to_string()}"
        except Exception as e:
            return f"Error processing spreadsheet: {str(e)}"
    
    def _process_image(self, uploaded_file) -> str:
        """Process image files"""
        try:
            if PDF_PROCESSING:
                image = Image.open(uploaded_file)
                return f"Image Info:\n- Format: {image.format}\n- Size: {image.size}\n- Mode: {image.mode}\n\nImage processing available in full version"
            else:
                return f"Image uploaded: {uploaded_file.name}\nProcessing libraries not available"
        except Exception as e:
            return f"Error processing image: {str(e)}"

file_processor = FileProcessor()

# ======================================================
# SESSION MANAGEMENT
# ======================================================

def initialize_session():
    """Initialize session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_plan" not in st.session_state:
        st.session_state.user_plan = "Free"
    if "current_bot" not in st.session_state:
        st.session_state.current_bot = "Business Strategist"
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = {}
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = {
            "total_cost": 0.0,
            "daily_cost": 0.0,
            "total_tokens": 0,
            "requests": 0,
            "files_processed": 0,
            "last_reset": datetime.now().date()
        }

def update_usage(metadata: Dict):
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
    stats["requests"] += 1

# ======================================================
# UI COMPONENTS
# ======================================================

def render_sidebar():
    """Render sidebar components"""
    st.sidebar.title("AI Chatbot Platform")
    
    # API Configuration
    with st.sidebar.expander("🔑 API Configuration"):
        api_key = st.text_input("OpenAI API Key", type="password", 
                               help="Enter your OpenAI API key for full functionality")
        model = st.selectbox("AI Model", 
                           SUBSCRIPTION_PLANS[st.session_state.user_plan]["models"])
        
        if st.button("Initialize API"):
            if api_manager.initialize(api_key, model):
                st.success("API initialized successfully!")
            else:
                st.error("Failed to initialize API")
    
    # Bot Selection
    st.sidebar.subheader("🤖 Assistant Selection")
    categories = list(set([bot["category"] for bot in BOT_PERSONALITIES.values()]))
    selected_category = st.sidebar.selectbox("Category", ["All"] + categories)
    
    # Filter bots by category
    available_bots = {}
    for name, bot in BOT_PERSONALITIES.items():
        if selected_category == "All" or bot["category"] == selected_category:
            available_bots[name] = bot
    
    current_bot = st.sidebar.selectbox("Select Assistant", 
                                      list(available_bots.keys()),
                                      index=0)
    
    if current_bot != st.session_state.current_bot:
        st.session_state.current_bot = current_bot
        st.rerun()
    
    # Show bot info
    if current_bot in BOT_PERSONALITIES:
        bot = BOT_PERSONALITIES[current_bot]
        st.sidebar.info(f"{bot['emoji']} {bot['description']}")
    
    # File Upload
    st.sidebar.subheader("📁 File Upload")
    plan_limits = SUBSCRIPTION_PLANS[st.session_state.user_plan]
    
    st.sidebar.caption(f"Max: {plan_limits['max_file_size']}MB, {plan_limits['max_files']} files")
    
    uploaded_files = st.sidebar.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        help="Upload documents, spreadsheets, images for analysis"
    )
    
    if uploaded_files:
        processed_files = []
        for file in uploaded_files:
            if file.size > plan_limits['max_file_size'] * 1024 * 1024:
                st.sidebar.error(f"File {file.name} too large")
                continue
            
            processed_file = file_processor.process_file(file)
            processed_files.append(processed_file)
        
        st.session_state.uploaded_files[current_bot] = processed_files
        st.session_state.usage_stats["files_processed"] += len(processed_files)
        st.sidebar.success(f"Processed {len(processed_files)} files")
    
    # Usage Dashboard
    st.sidebar.subheader("📊 Usage")
    stats = st.session_state.usage_stats
    plan = SUBSCRIPTION_PLANS[st.session_state.user_plan]
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Cost Today", f"${stats['daily_cost']:.3f}")
        st.metric("Total Requests", stats['requests'])
    with col2:
        st.metric("Total Tokens", f"{stats['total_tokens']:,}")
        st.metric("Files", stats['files_processed'])
    
    # Daily budget progress
    if plan["daily_budget"] > 0:
        progress = min(stats["daily_cost"] / plan["daily_budget"], 1.0)
        st.sidebar.progress(progress)
        st.sidebar.caption(f"Daily budget: ${stats['daily_cost']:.3f} / ${plan['daily_budget']:.2f}")
    
    # Controls
    st.sidebar.subheader("🔧 Controls")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Clear Chat"):
            if current_bot in st.session_state.messages:
                del st.session_state.messages[current_bot]
            st.rerun()
    with col2:
        if st.button("Reset Stats"):
            st.session_state.usage_stats = {
                "total_cost": 0.0,
                "daily_cost": 0.0,
                "total_tokens": 0,
                "requests": 0,
                "files_processed": 0,
                "last_reset": datetime.now().date()
            }
            st.rerun()

def render_chat_interface():
    """Render main chat interface"""
    current_bot = st.session_state.current_bot
    
    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        bot_info = BOT_PERSONALITIES[current_bot]
        st.title(f"{bot_info['emoji']} {current_bot}")
        st.caption(bot_info['description'])
    with col2:
        st.metric("Plan", st.session_state.user_plan)
    with col3:
        if api_manager.initialized and api_manager.client:
            st.success("🟢 API Connected")
        else:
            st.warning("🟡 Demo Mode")
    
    # Initialize messages for current bot
    if current_bot not in st.session_state.messages:
        st.session_state.messages[current_bot] = []
    
    messages = st.session_state.messages[current_bot]
    
    # Display chat history
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
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
    
    # Show uploaded files
    if current_bot in st.session_state.uploaded_files:
        files = st.session_state.uploaded_files[current_bot]
        if files:
            st.subheader("📁 Uploaded Files")
            cols = st.columns(min(len(files), 4))
            for i, file_info in enumerate(files):
                with cols[i % 4]:
                    st.info(f"📄 {file_info['name']}\n{file_info['file_type']} • {file_info['size']:,} bytes")
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages[current_bot].append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Prepare messages
                api_messages = []
                
                # System prompt
                bot_config = BOT_PERSONALITIES[current_bot]
                system_content = bot_config["system_prompt"]
                
                # Add file context
                if current_bot in st.session_state.uploaded_files:
                    files = st.session_state.uploaded_files[current_bot]
                    if files:
                        file_context = "\n\nFile Context:\n"
                        for file_info in files:
                            if not file_info.get('error'):
                                file_context += f"\n--- {file_info['name']} ---\n"
                                file_context += file_info['content'][:1000]
                        system_content += file_context
                
                api_messages.append({"role": "system", "content": system_content})
                
                # Add conversation history (last 10 messages)
                recent_messages = messages[-10:]
                for msg in recent_messages:
                    api_messages.append({"role": msg["role"], "content": msg["content"]})
                
                # Generate response
                plan = SUBSCRIPTION_PLANS[st.session_state.user_plan]
                model = plan["models"][0]  # Use first available model
                
                response, metadata = api_manager.generate_response(
                    api_messages,
                    model=model,
                    max_tokens=plan["max_tokens"]
                )
                
                st.markdown(response)
                
                # Show response metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"💰 ${metadata.get('cost', 0):.4f}")
                with col2:
                    st.caption(f"🔢 {metadata.get('total_tokens', 0)} tokens")
                with col3:
                    if metadata.get('demo_mode'):
                        st.caption("🎮 Demo")
                    else:
                        st.caption("⚡ Live")
                
                # Save assistant message
                st.session_state.messages[current_bot].append({
                    "role": "assistant",
                    "content": response,
                    "metadata": metadata
                })
                
                # Update usage
                update_usage(metadata)
        
        st.rerun()

def render_auth_page():
    """Render authentication page"""
    st.markdown('<div class="main-header"><h1>🤖 AI Chatbot Platform</h1><p>Advanced conversational AI with file processing capabilities</p></div>', unsafe_allow_html=True)
    
    # Features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 🤖 Multiple AI Personalities
        - Business Strategist
        - Technical Consultant  
        - Data Analyst
        - Marketing Expert
        - Financial Advisor
        - Project Manager
        """)
    
    with col2:
        st.markdown("""
        ### 📁 File Processing
        - PDF documents
        - Word documents
        - Excel spreadsheets
        - Images and data files
        - Real-time analysis
        """)
    
    with col3:
        st.markdown("""
        ### ⚡ Advanced Features
        - Real OpenAI API integration
        - Usage tracking & analytics
        - Multi-plan support
        - Conversation history
        - Export capabilities
        """)
    
    # Plan selection
    st.subheader("🎯 Choose Your Plan")
    
    plan_cols = st.columns(len(SUBSCRIPTION_PLANS))
    for i, (plan_name, plan_details) in enumerate(SUBSCRIPTION_PLANS.items()):
        with plan_cols[i]:
            st.markdown(f"""
            <div style="border: 2px solid #ddd; border-radius: 10px; padding: 20px; text-align: center; height: 280px; background: white;">
                <h3>{plan_name}</h3>
                <p><strong>${plan_details['monthly_budget']}/month</strong></p>
                <p>{plan_details['max_tokens']} max tokens</p>
                <p>{plan_details['max_file_size']}MB file limit</p>
                <p>{plan_details['max_files']} files per chat</p>
                <p>{len(plan_details['models'])} AI models</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Plan selection
    selected_plan = st.selectbox("Select Plan", list(SUBSCRIPTION_PLANS.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start with Selected Plan", use_container_width=True):
            st.session_state.user_plan = selected_plan
            st.session_state.authenticated = True
            st.rerun()
    
    with col2:
        if st.button("Try Demo Mode", use_container_width=True):
            st.session_state.user_plan = "Free"
            st.session_state.authenticated = True
            st.rerun()
    
    # Demo info
    st.info("""
    **Demo Mode Features:**
    - All interface functionality available
    - File upload and processing
    - Multiple AI personalities
    - Usage tracking and analytics
    - Add your OpenAI API key anytime for real AI responses
    """)

# ======================================================
# ANALYTICS PAGE
# ======================================================

def render_analytics():
    """Render analytics dashboard"""
    st.title("Analytics Dashboard")
    st.markdown("Comprehensive insights into your AI usage")
    
    stats = st.session_state.usage_stats
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Conversations", stats['requests'])
    with col2:
        st.metric("Total Cost", f"${stats['total_cost']:.3f}")
    with col3:
        st.metric("Files Processed", stats['files_processed'])
    with col4:
        avg_tokens = stats['total_tokens'] / max(stats['requests'], 1)
        st.metric("Avg Tokens/Request", f"{avg_tokens:.0f}")
    
    # Usage charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Bot Usage")
        bot_usage = {}
        for bot_name in st.session_state.messages:
            bot_usage[bot_name] = len(st.session_state.messages[bot_name])
        
        if bot_usage:
            st.bar_chart(bot_usage)
        else:
            st.info("No chat activity yet")
    
    with col2:
        st.subheader("Daily Usage")
        plan = SUBSCRIPTION_PLANS[st.session_state.user_plan]
        
        # Progress bar for daily budget
        if plan["daily_budget"] > 0:
            usage_pct = (stats["daily_cost"] / plan["daily_budget"]) * 100
            st.progress(min(usage_pct / 100, 1.0))
            st.caption(f"Daily budget usage: {usage_pct:.1f}%")
        
        # Plan details
        st.markdown(f"""
        **Current Plan: {st.session_state.user_plan}**
        - Daily budget: ${plan['daily_budget']:.2f}
        - Max tokens: {plan['max_tokens']:,}
        - File size limit: {plan['max_file_size']}MB
        - Files per chat: {plan['max_files']}
        - Available models: {len(plan['models'])}
        """)
    
    # Export data
    st.subheader("Data Export")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Analytics"):
            analytics_data = {
                "stats": stats,
                "plan": st.session_state.user_plan,
                "bot_usage": bot_usage,
                "export_date": datetime.now().isoformat()
            }
            st.download_button(
                "Download Analytics JSON",
                json.dumps(analytics_data, indent=2),
                file_name=f"analytics_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("Export Conversations"):
            conversation_data = {
                "messages": st.session_state.messages,
                "files": st.session_state.uploaded_files,
                "export_date": datetime.now().isoformat()
            }
            st.download_button(
                "Download Conversations JSON",
                json.dumps(conversation_data, indent=2, default=str),
                file_name=f"conversations_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("Reset All Data"):
            if st.button("Confirm Reset", help="This will delete all data"):
                st.session_state.messages = {}
                st.session_state.uploaded_files = {}
                st.session_state.usage_stats = {
                    "total_cost": 0.0,
                    "daily_cost": 0.0,
                    "total_tokens": 0,
                    "requests": 0,
                    "files_processed": 0,
                    "last_reset": datetime.now().date()
                }
                st.success("All data reset successfully!")
                st.rerun()

# ======================================================
# SETTINGS PAGE
# ======================================================

def render_settings():
    """Render settings page"""
    st.title("Settings")
    
    # Plan management
    st.subheader("Plan Management")
    current_plan = st.session_state.user_plan
    new_plan = st.selectbox("Change Plan", list(SUBSCRIPTION_PLANS.keys()), 
                           index=list(SUBSCRIPTION_PLANS.keys()).index(current_plan))
    
    if new_plan != current_plan:
        if st.button("Update Plan"):
            st.session_state.user_plan = new_plan
            st.success(f"Plan updated to {new_plan}")
            st.rerun()
    
    # API Settings
    st.subheader("API Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        api_key = st.text_input("OpenAI API Key", type="password", 
                               help="Your OpenAI API key for live responses")
        
    with col2:
        available_models = SUBSCRIPTION_PLANS[st.session_state.user_plan]["models"]
        model = st.selectbox("Preferred Model", available_models)
    
    if st.button("Test API Connection"):
        if api_manager.initialize(api_key, model):
            st.success("API connection successful!")
        else:
            st.error("API connection failed")
    
    # App Preferences
    st.subheader("Preferences")
    
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.7,
                               help="Higher values make responses more creative")
        max_tokens = st.number_input("Max Response Length", 
                                   min_value=100, 
                                   max_value=SUBSCRIPTION_PLANS[st.session_state.user_plan]["max_tokens"],
                                   value=2000)
    
    with col2:
        auto_save = st.checkbox("Auto-save conversations", value=True)
        show_tokens = st.checkbox("Show token usage", value=True)
    
    # Data Management
    st.subheader("Data Management")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Clear All Conversations"):
            st.session_state.messages = {}
            st.success("Conversations cleared")
            st.rerun()
    
    with col2:
        if st.button("Clear All Files"):
            st.session_state.uploaded_files = {}
            st.success("Files cleared")
            st.rerun()
    
    with col3:
        if st.button("Reset Usage Stats"):
            st.session_state.usage_stats = {
                "total_cost": 0.0,
                "daily_cost": 0.0,
                "total_tokens": 0,
                "requests": 0,
                "files_processed": 0,
                "last_reset": datetime.now().date()
            }
            st.success("Usage stats reset")
            st.rerun()

# ======================================================
# MAIN APPLICATION
# ======================================================

def main():
    """Main application logic"""
    initialize_session()
    
    if not st.session_state.authenticated:
        render_auth_page()
    else:
        # Navigation
        with st.sidebar:
            st.title("Navigation")
            page = st.selectbox("Go to", 
                               ["Chat", "Analytics", "Settings", "Logout"])
            
            if page == "Logout":
                st.session_state.authenticated = False
                st.rerun()
        
        # Render selected page
        if page == "Chat":
            render_sidebar()
            render_chat_interface()
        elif page == "Analytics":
            render_analytics()
        elif page == "Settings":
            render_settings()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.code(traceback.format_exc())
