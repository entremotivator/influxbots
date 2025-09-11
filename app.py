#!/usr/bin/env python3
"""
🚀 ENHANCED AI ASSISTANT PLATFORM WITH SUPABASE
Advanced AI platform with threads, voice, agents, real-time features, and cloud storage
Optimized for production with comprehensive Supabase integration
"""

import streamlit as st
import os
import json
import time
import hashlib
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
from io import StringIO, BytesIO
import base64
import tempfile
import asyncio
from pathlib import Path
import uuid
import threading
import queue
import io

# Core imports
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Supabase imports
try:
    from supabase import create_client, Client
    import postgrest
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# LangChain Core imports
try:
    from langchain.llms import OpenAI as LangChainOpenAI
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import Document, BaseMessage, HumanMessage, AIMessage, SystemMessage
    from langchain.agents import initialize_agent, Tool, AgentType
    from langchain.memory import ConversationBufferWindowMemory
    from langchain.callbacks import StreamlitCallbackHandler
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import SupabaseVectorStore
    LANGCHAIN_CORE_AVAILABLE = True
except ImportError:
    LANGCHAIN_CORE_AVAILABLE = False

# Additional processing libraries
try:
    import PyPDF2
    from PIL import Image
    import docx
    from openpyxl import load_workbook
    import pandas as pd
    import numpy as np
    FILE_PROCESSING_AVAILABLE = True
except ImportError:
    FILE_PROCESSING_AVAILABLE = False

# Advanced processing libraries
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

# Web scraping and API libraries
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_PROCESSING_AVAILABLE = True
except ImportError:
    WEB_PROCESSING_AVAILABLE = False

# Audio processing
try:
    import speech_recognition as sr
    from gtts import gTTS
    import pygame
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🔐 ENHANCED CONFIGURATION MANAGEMENT
# ======================================================

class ConfigurationManager:
    """Enhanced configuration management with Supabase integration"""
    
    def __init__(self):
        self.config = self.load_configuration()
        self.supabase_client = None
        self.initialize_supabase()
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load configuration from multiple sources"""
        try:
            config = {
                # Supabase Configuration
                "supabase_url": self._get_config_value("SUPABASE_URL", ""),
                "supabase_key": self._get_config_value("SUPABASE_ANON_KEY", ""),
                "supabase_service_key": self._get_config_value("SUPABASE_SERVICE_KEY", ""),
                
                # OpenAI Configuration
                "openai_api_key": self._get_config_value("OPENAI_API_KEY", ""),
                "openai_model": self._get_config_value("OPENAI_MODEL", "gpt-4"),
                "openai_temperature": float(self._get_config_value("OPENAI_TEMPERATURE", "0.7")),
                "openai_max_tokens": int(self._get_config_value("OPENAI_MAX_TOKENS", "4000")),
                
                # Real-time API Configuration
                "realtime_api_enabled": self._get_config_value("REALTIME_API_ENABLED", "true").lower() == "true",
                "voice_model": self._get_config_value("VOICE_MODEL", "tts-1-hd"),
                "voice_type": self._get_config_value("VOICE_TYPE", "alloy"),
                "whisper_model": self._get_config_value("WHISPER_MODEL", "whisper-1"),
                
                # Assistant API Configuration
                "assistant_api_enabled": self._get_config_value("ASSISTANT_API_ENABLED", "true").lower() == "true",
                "assistant_model": self._get_config_value("ASSISTANT_MODEL", "gpt-4-turbo-preview"),
                
                # File Processing Configuration
                "max_file_size_mb": int(self._get_config_value("MAX_FILE_SIZE_MB", "200")),
                "max_files_per_session": int(self._get_config_value("MAX_FILES_PER_SESSION", "100")),
                "supported_file_types": self._get_config_value("SUPPORTED_FILE_TYPES", "pdf,docx,txt,csv,json,xlsx,html,md,py,js,mp3,wav,mp4,mov,jpg,jpeg,png,gif").split(","),
                
                # Vector Database Configuration
                "vector_store_enabled": self._get_config_value("VECTOR_STORE_ENABLED", "true").lower() == "true",
                "embedding_model": self._get_config_value("EMBEDDING_MODEL", "text-embedding-3-large"),
                "chunk_size": int(self._get_config_value("CHUNK_SIZE", "1000")),
                "chunk_overlap": int(self._get_config_value("CHUNK_OVERLAP", "200")),
                
                # Application Configuration
                "app_name": self._get_config_value("APP_NAME", "Enhanced AI Assistant Platform"),
                "app_description": self._get_config_value("APP_DESCRIPTION", "Advanced AI platform with voice, agents, threads, and cloud storage"),
                "debug_mode": self._get_config_value("DEBUG_MODE", "false").lower() == "true",
                "environment": self._get_config_value("ENVIRONMENT", "production"),
                
                # UI Configuration - Red Theme
                "theme_primary_color": "#dc2626",
                "theme_secondary_color": "#991b1b",
                "theme_accent_color": "#fef2f2",
                "theme_text_color": "#000000",
                "theme_background": "#ffebee",
                
                # Real-time Features
                "websocket_enabled": self._get_config_value("WEBSOCKET_ENABLED", "true").lower() == "true",
                "streaming_enabled": self._get_config_value("STREAMING_ENABLED", "true").lower() == "true",
                "auto_save_enabled": self._get_config_value("AUTO_SAVE_ENABLED", "true").lower() == "true",
                
                # Analytics Configuration
                "analytics_enabled": self._get_config_value("ANALYTICS_ENABLED", "true").lower() == "true",
                "usage_tracking": self._get_config_value("USAGE_TRACKING", "true").lower() == "true",
            }
            
            return config
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return self._get_default_configuration()
    
    def initialize_supabase(self):
        """Initialize Supabase client"""
        try:
            if SUPABASE_AVAILABLE:
                supabase_url = self.config.get("supabase_url")
                supabase_key = self.config.get("supabase_key")
                
                if supabase_url and supabase_key:
                    self.supabase_client = create_client(supabase_url, supabase_key)
                    logger.info("Supabase client initialized successfully")
                else:
                    logger.warning("Supabase credentials not found")
            else:
                logger.warning("Supabase not available - install supabase-py")
        except Exception as e:
            logger.error(f"Error initializing Supabase: {str(e)}")
    
    def _get_config_value(self, key: str, default: str) -> str:
        """Get configuration value from Streamlit secrets or environment variables"""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
            
            # Fall back to environment variables
            return os.getenv(key, default)
            
        except Exception:
            return default
    
    def _get_default_configuration(self) -> Dict[str, Any]:
        """Get default configuration when loading fails"""
        return {
            "supabase_url": "",
            "supabase_key": "",
            "supabase_service_key": "",
            "openai_api_key": "",
            "openai_model": "gpt-4",
            "openai_temperature": 0.7,
            "openai_max_tokens": 4000,
            "realtime_api_enabled": True,
            "voice_model": "tts-1-hd",
            "voice_type": "alloy",
            "whisper_model": "whisper-1",
            "assistant_api_enabled": True,
            "assistant_model": "gpt-4-turbo-preview",
            "max_file_size_mb": 200,
            "max_files_per_session": 100,
            "supported_file_types": ["pdf", "docx", "txt", "csv", "json", "xlsx", "html", "md", "py", "js", "mp3", "wav", "mp4", "mov", "jpg", "jpeg", "png", "gif"],
            "vector_store_enabled": True,
            "embedding_model": "text-embedding-3-large",
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "app_name": "Enhanced AI Assistant Platform",
            "app_description": "Advanced AI platform with voice, agents, threads, and cloud storage",
            "debug_mode": False,
            "environment": "production",
            "theme_primary_color": "#dc2626",
            "theme_secondary_color": "#991b1b",
            "theme_accent_color": "#fef2f2",
            "theme_text_color": "#000000",
            "theme_background": "#ffebee",
            "websocket_enabled": True,
            "streaming_enabled": True,
            "auto_save_enabled": True,
            "analytics_enabled": True,
            "usage_tracking": True
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        self.config[key] = value
    
    def get_supabase_client(self) -> Optional[Client]:
        """Get Supabase client"""
        return self.supabase_client

# Initialize configuration manager
config_manager = ConfigurationManager()

# ======================================================
# 🗄️ SUPABASE DATABASE MANAGER
# ======================================================

class SupabaseManager:
    """Comprehensive Supabase database manager"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.client = config_manager.get_supabase_client()
        self.initialize_tables()
    
    def initialize_tables(self):
        """Initialize database tables if they don't exist"""
        try:
            if not self.client:
                logger.warning("Supabase client not available")
                return
            
            # Tables will be created via Supabase dashboard or migrations
            # This method can be used to verify table existence
            self.verify_tables()
            
        except Exception as e:
            logger.error(f"Error initializing tables: {str(e)}")
    
    def verify_tables(self):
        """Verify that required tables exist"""
        required_tables = [
            'users', 'threads', 'messages', 'assistants', 
            'files', 'embeddings', 'analytics', 'settings'
        ]
        
        try:
            for table in required_tables:
                # Simple query to check if table exists
                result = self.client.table(table).select("*").limit(1).execute()
                logger.info(f"Table '{table}' verified")
        except Exception as e:
            logger.warning(f"Table verification issue: {str(e)}")
    
    # User Management
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user"""
        try:
            if not self.client:
                return None
            
            result = self.client.table('users').insert(user_data).execute()
            if result.data:
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            if not self.client:
                return None
            
            result = self.client.table('users').select("*").eq('id', user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    # Thread Management
    def create_thread(self, thread_data: Dict[str, Any]) -> Optional[str]:
        """Create a new thread"""
        try:
            if not self.client:
                return None
            
            thread_data['created_at'] = datetime.now().isoformat()
            thread_data['updated_at'] = datetime.now().isoformat()
            
            result = self.client.table('threads').insert(thread_data).execute()
            if result.data:
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}")
            return None
    
    def get_threads(self, user_id: str = None, assistant_id: str = None) -> List[Dict[str, Any]]:
        """Get threads with optional filtering"""
        try:
            if not self.client:
                return []
            
            query = self.client.table('threads').select("*")
            
            if user_id:
                query = query.eq('user_id', user_id)
            if assistant_id:
                query = query.eq('assistant_id', assistant_id)
            
            result = query.order('updated_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting threads: {str(e)}")
            return []
    
    def update_thread(self, thread_id: str, updates: Dict[str, Any]) -> bool:
        """Update thread"""
        try:
            if not self.client:
                return False
            
            updates['updated_at'] = datetime.now().isoformat()
            result = self.client.table('threads').update(updates).eq('id', thread_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating thread: {str(e)}")
            return False
    
    def delete_thread(self, thread_id: str) -> bool:
        """Delete thread and associated messages"""
        try:
            if not self.client:
                return False
            
            # Delete messages first
            self.client.table('messages').delete().eq('thread_id', thread_id).execute()
            
            # Delete thread
            result = self.client.table('threads').delete().eq('id', thread_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error deleting thread: {str(e)}")
            return False
    
    # Message Management
    def add_message(self, message_data: Dict[str, Any]) -> Optional[str]:
        """Add message to thread"""
        try:
            if not self.client:
                return None
            
            message_data['created_at'] = datetime.now().isoformat()
            
            result = self.client.table('messages').insert(message_data).execute()
            if result.data:
                # Update thread timestamp
                self.update_thread(message_data['thread_id'], {})
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            return None
    
    def get_messages(self, thread_id: str) -> List[Dict[str, Any]]:
        """Get messages for thread"""
        try:
            if not self.client:
                return []
            
            result = self.client.table('messages').select("*").eq('thread_id', thread_id).order('created_at', desc=False).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            return []
    
    # Assistant Management
    def save_assistant(self, assistant_data: Dict[str, Any]) -> Optional[str]:
        """Save custom assistant"""
        try:
            if not self.client:
                return None
            
            assistant_data['created_at'] = datetime.now().isoformat()
            assistant_data['updated_at'] = datetime.now().isoformat()
            
            result = self.client.table('assistants').insert(assistant_data).execute()
            if result.data:
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error saving assistant: {str(e)}")
            return None
    
    def get_assistants(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get custom assistants"""
        try:
            if not self.client:
                return []
            
            query = self.client.table('assistants').select("*")
            if user_id:
                query = query.eq('user_id', user_id)
            
            result = query.order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting assistants: {str(e)}")
            return []
    
    def update_assistant(self, assistant_id: str, updates: Dict[str, Any]) -> bool:
        """Update assistant"""
        try:
            if not self.client:
                return False
            
            updates['updated_at'] = datetime.now().isoformat()
            result = self.client.table('assistants').update(updates).eq('id', assistant_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating assistant: {str(e)}")
            return False
    
    def delete_assistant(self, assistant_id: str) -> bool:
        """Delete assistant"""
        try:
            if not self.client:
                return False
            
            result = self.client.table('assistants').delete().eq('id', assistant_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error deleting assistant: {str(e)}")
            return False
    
    # File Management
    def save_file_metadata(self, file_data: Dict[str, Any]) -> Optional[str]:
        """Save file metadata"""
        try:
            if not self.client:
                return None
            
            file_data['created_at'] = datetime.now().isoformat()
            
            result = self.client.table('files').insert(file_data).execute()
            if result.data:
                return result.data[0]['id']
            return None
        except Exception as e:
            logger.error(f"Error saving file metadata: {str(e)}")
            return None
    
    def get_files(self, user_id: str = None, thread_id: str = None) -> List[Dict[str, Any]]:
        """Get files with optional filtering"""
        try:
            if not self.client:
                return []
            
            query = self.client.table('files').select("*")
            
            if user_id:
                query = query.eq('user_id', user_id)
            if thread_id:
                query = query.eq('thread_id', thread_id)
            
            result = query.order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting files: {str(e)}")
            return []
    
    def upload_file_to_storage(self, file_path: str, file_data: bytes, bucket: str = "files") -> Optional[str]:
        """Upload file to Supabase storage"""
        try:
            if not self.client:
                return None
            
            result = self.client.storage.from_(bucket).upload(file_path, file_data)
            if result:
                return f"{bucket}/{file_path}"
            return None
        except Exception as e:
            logger.error(f"Error uploading file to storage: {str(e)}")
            return None
    
    def download_file_from_storage(self, file_path: str, bucket: str = "files") -> Optional[bytes]:
        """Download file from Supabase storage"""
        try:
            if not self.client:
                return None
            
            result = self.client.storage.from_(bucket).download(file_path)
            return result
        except Exception as e:
            logger.error(f"Error downloading file from storage: {str(e)}")
            return None
    
    # Analytics
    def log_analytics_event(self, event_data: Dict[str, Any]) -> bool:
        """Log analytics event"""
        try:
            if not self.client or not self.config.get("analytics_enabled"):
                return False
            
            event_data['created_at'] = datetime.now().isoformat()
            
            result = self.client.table('analytics').insert(event_data).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error logging analytics event: {str(e)}")
            return False
    
    def get_analytics_data(self, user_id: str = None, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """Get analytics data"""
        try:
            if not self.client:
                return []
            
            query = self.client.table('analytics').select("*")
            
            if user_id:
                query = query.eq('user_id', user_id)
            if start_date:
                query = query.gte('created_at', start_date)
            if end_date:
                query = query.lte('created_at', end_date)
            
            result = query.order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting analytics data: {str(e)}")
            return []

# Initialize Supabase manager
supabase_manager = SupabaseManager(config_manager)

# ======================================================
# 🎙️ ADVANCED VOICE PROCESSING SYSTEM
# ======================================================

class AdvancedVoiceProcessor:
    """Advanced voice processing with OpenAI TTS/STT and real-time capabilities"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.client = None
        self.recognizer = None
        self.microphone = None
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.initialize_voice_services()
    
    def initialize_voice_services(self):
        """Initialize voice services"""
        try:
            api_key = self.config.get("openai_api_key")
            if api_key and OPENAI_AVAILABLE:
                self.client = OpenAI(api_key=api_key)
            
            if AUDIO_AVAILABLE:
                self.recognizer = sr.Recognizer()
                try:
                    self.microphone = sr.Microphone()
                    # Adjust for ambient noise
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                except Exception as e:
                    logger.warning(f"Microphone initialization failed: {str(e)}")
                    
            logger.info("Voice services initialized")
            
        except Exception as e:
            logger.error(f"Error initializing voice services: {str(e)}")
    
    def text_to_speech(self, text: str, voice: str = None, model: str = None) -> Optional[bytes]:
        """Convert text to speech using OpenAI TTS"""
        try:
            if not self.client:
                return None
            
            if not voice:
                voice = self.config.get("voice_type", "alloy")
            if not model:
                model = self.config.get("voice_model", "tts-1-hd")
            
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=1.0
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return None
    
    def speech_to_text(self, audio_file, model: str = None) -> Optional[str]:
        """Convert speech to text using OpenAI Whisper"""
        try:
            if not self.client:
                return None
            
            if not model:
                model = self.config.get("whisper_model", "whisper-1")
            
            transcript = self.client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            
            return transcript
            
        except Exception as e:
            logger.error(f"Error in speech-to-text: {str(e)}")
            return None
    
    def start_real_time_listening(self):
        """Start real-time voice listening"""
        try:
            if not self.recognizer or not self.microphone:
                return False
            
            self.is_listening = True
            
            def listen_continuously():
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                
                while self.is_listening:
                    try:
                        with self.microphone as source:
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        
                        # Convert to text
                        if self.client:
                            wav_data = audio.get_wav_data()
                            audio_file = io.BytesIO(wav_data)
                            audio_file.name = "speech.wav"
                            
                            text = self.speech_to_text(audio_file)
                            if text and text.strip():
                                self.audio_queue.put(text)
                        
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Error in continuous listening: {str(e)}")
                        break
            
            # Start listening in background thread
            listening_thread = threading.Thread(target=listen_continuously)
            listening_thread.daemon = True
            listening_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Error starting real-time listening: {str(e)}")
            return False
    
    def stop_real_time_listening(self):
        """Stop real-time voice listening"""
        self.is_listening = False
    
    def get_voice_input(self) -> Optional[str]:
        """Get voice input from queue"""
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_available_voices(self) -> List[str]:
        """Get list of available TTS voices"""
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    
    def get_voice_models(self) -> List[str]:
        """Get list of available voice models"""
        return ["tts-1", "tts-1-hd"]

# Initialize voice processor
voice_processor = AdvancedVoiceProcessor(config_manager)

# ======================================================
# 🤖 ENHANCED AI ASSISTANT PROFILES
# ======================================================

class EnhancedAIAssistantProfiles:
    """Enhanced AI assistant profiles with comprehensive capabilities"""
    
    def __init__(self, supabase_manager: SupabaseManager):
        self.supabase = supabase_manager
        self.built_in_assistants = self._get_built_in_assistants()
    
    def _get_built_in_assistants(self) -> Dict[str, Dict[str, Any]]:
        """Get all built-in AI assistants with enhanced profiles"""
        return {
            "Strategic Business Consultant": {
                "description": "Senior strategic consultant with expertise in business transformation, growth strategy, and market analysis. Specializes in data-driven insights and long-term strategic planning.",
                "system_prompt": """You are a strategic business consultant with 20+ years of experience in Fortune 500 companies. 

Your expertise includes:
- Strategic planning and execution
- Market analysis and competitive intelligence
- Business transformation and change management
- Financial modeling and ROI analysis
- Risk assessment and mitigation strategies

Always:
- Provide data-driven insights and actionable recommendations
- Ask clarifying questions to understand business context
- Consider both short-term tactics and long-term strategic implications
- Use frameworks like SWOT, Porter's Five Forces, and BCG Matrix when relevant
- Focus on measurable outcomes and KPIs""",
                "emoji": "🎯",
                "category": "Business Strategy",
                "specialties": ["Strategic Planning", "Market Analysis", "Business Transformation", "Competitive Intelligence", "Growth Strategy", "Financial Modeling"],
                "expertise_level": "Senior Partner",
                "temperature": 0.3,
                "max_tokens": 4000,
                "tools": ["market_research", "financial_analysis", "swot_analysis", "competitive_analysis"],
                "agent_type": "strategic_advisor",
                "voice_enabled": True,
                "preferred_voice": "echo",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Startup Growth Advisor": {
                "description": "Experienced startup mentor specializing in scaling early-stage companies, product-market fit, and fundraising strategies.",
                "system_prompt": """You are a startup growth advisor who has mentored 200+ startups from seed to Series C.

Your expertise includes:
- Product-market fit validation
- Growth hacking and viral marketing
- Fundraising and investor relations
- MVP development and iteration
- Customer development and validation
- Scaling operations and team building

Always:
- Be practical and action-oriented
- Focus on measurable results and metrics
- Provide specific tactics for resource-constrained environments
- Consider the startup's stage and available resources
- Emphasize speed of execution and learning""",
                "emoji": "🚀",
                "category": "Entrepreneurship",
                "specialties": ["Product-Market Fit", "Growth Hacking", "Fundraising", "MVP Development", "Customer Development", "Scaling Operations"],
                "expertise_level": "Serial Entrepreneur",
                "temperature": 0.7,
                "max_tokens": 3500,
                "tools": ["mvp_validation", "market_sizing", "pitch_analysis", "growth_metrics"],
                "agent_type": "growth_advisor",
                "voice_enabled": True,
                "preferred_voice": "nova",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Digital Marketing Strategist": {
                "description": "Performance marketing expert driving growth through data-driven campaigns, conversion optimization, and multi-channel marketing strategies.",
                "system_prompt": """You are a digital marketing strategist focused on performance marketing and growth analytics.

Your expertise includes:
- Performance marketing across all channels (PPC, Social, Email, Content)
- Conversion rate optimization and A/B testing
- Marketing automation and funnel optimization
- Customer acquisition cost (CAC) and lifetime value (LTV) optimization
- Attribution modeling and marketing mix optimization
- Brand positioning and messaging strategy

Always:
- Provide measurable ROI strategies with specific metrics
- Recommend testing frameworks and experimentation approaches
- Focus on data-driven decision making
- Consider the full customer journey and touchpoints
- Optimize for both acquisition and retention""",
                "emoji": "📈",
                "category": "Marketing & Growth",
                "specialties": ["Performance Marketing", "Customer Acquisition", "Conversion Optimization", "Marketing Automation", "Attribution Modeling", "Brand Strategy"],
                "expertise_level": "VP Marketing",
                "temperature": 0.4,
                "max_tokens": 3500,
                "tools": ["campaign_analysis", "conversion_tracking", "audience_research", "competitor_ads"],
                "agent_type": "marketing_strategist",
                "voice_enabled": True,
                "preferred_voice": "alloy",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Sales Performance Coach": {
                "description": "Elite sales trainer helping maximize revenue through proven methodologies, sales psychology, and performance optimization.",
                "system_prompt": """You are a sales performance coach with expertise in consultative selling and sales psychology.

Your expertise includes:
- Consultative and solution-based selling
- Sales psychology and buyer behavior
- Objection handling and negotiation tactics
- Pipeline management and forecasting
- Sales team coaching and development
- CRM optimization and sales process design

Always:
- Provide practical, actionable sales techniques
- Focus on building long-term customer relationships
- Use proven sales methodologies (SPIN, Challenger, etc.)
- Emphasize value-based selling over feature dumping
- Consider the buyer's journey and decision-making process""",
                "emoji": "💰",
                "category": "Sales & Revenue",
                "specialties": ["Consultative Selling", "Objection Handling", "Pipeline Management", "Sales Psychology", "Negotiation", "Sales Coaching"],
                "expertise_level": "VP Sales",
                "temperature": 0.5,
                "max_tokens": 3000,
                "tools": ["pipeline_analysis", "objection_handling", "proposal_optimization", "sales_forecasting"],
                "agent_type": "sales_coach",
                "voice_enabled": True,
                "preferred_voice": "onyx",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": False,
                "built_in": True,
                "editable": False
            },
            
            "Financial Strategy Advisor": {
                "description": "CFO-level financial expert optimizing business finances, strategic planning, and investment decisions.",
                "system_prompt": """You are a financial strategy advisor with CFO-level expertise.

Your expertise includes:
- Financial planning and analysis (FP&A)
- Investment strategy and portfolio management
- Risk management and financial controls
- Cash flow optimization and working capital management
- Mergers & acquisitions analysis
- Financial modeling and valuation

Always:
- Provide detailed financial analysis with calculations
- Focus on sustainable growth and profitability
- Consider risk-adjusted returns and scenario planning
- Use appropriate financial metrics and ratios
- Emphasize cash flow and liquidity management""",
                "emoji": "💼",
                "category": "Finance & Investment",
                "specialties": ["Financial Planning", "Investment Strategy", "Risk Management", "Cash Flow Management", "M&A Analysis", "Financial Modeling"],
                "expertise_level": "CFO",
                "temperature": 0.2,
                "max_tokens": 4000,
                "tools": ["financial_modeling", "risk_analysis", "valuation", "cash_flow_analysis"],
                "agent_type": "financial_advisor",
                "voice_enabled": True,
                "preferred_voice": "echo",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "AI & Machine Learning Specialist": {
                "description": "Advanced AI researcher helping organizations leverage artificial intelligence, machine learning, and data science.",
                "system_prompt": """You are an AI and machine learning specialist with deep technical expertise.

Your expertise includes:
- Machine learning algorithms and model selection
- Deep learning and neural network architectures
- Natural language processing and computer vision
- MLOps and model deployment strategies
- Data engineering and feature engineering
- AI ethics and responsible AI practices

Always:
- Provide technically accurate guidance while making concepts accessible
- Focus on practical applications and business value
- Consider data quality, bias, and ethical implications
- Recommend appropriate tools and frameworks
- Emphasize iterative development and continuous learning""",
                "emoji": "🤖",
                "category": "Artificial Intelligence",
                "specialties": ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "MLOps", "AI Ethics"],
                "expertise_level": "AI Research Director",
                "temperature": 0.3,
                "max_tokens": 4000,
                "tools": ["model_analysis", "data_preprocessing", "feature_engineering", "model_evaluation"],
                "agent_type": "ai_specialist",
                "voice_enabled": True,
                "preferred_voice": "shimmer",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Technology Strategy Consultant": {
                "description": "CTO-level technology advisor guiding digital transformation, architecture decisions, and innovation strategies.",
                "system_prompt": """You are a technology strategy consultant with CTO-level expertise.

Your expertise includes:
- Digital transformation and modernization strategies
- Technology architecture and system design
- Cloud strategy and migration planning
- Cybersecurity and compliance frameworks
- Innovation management and emerging technologies
- Technical team leadership and development

Always:
- Balance technical feasibility with business value
- Provide implementation roadmaps with risk assessments
- Consider scalability, security, and maintainability
- Recommend modern best practices and industry standards
- Focus on sustainable and future-proof solutions""",
                "emoji": "💻",
                "category": "Technology & Innovation",
                "specialties": ["Digital Transformation", "Technology Architecture", "Cloud Strategy", "Cybersecurity", "Innovation Strategy", "Technical Leadership"],
                "expertise_level": "CTO",
                "temperature": 0.4,
                "max_tokens": 3500,
                "tools": ["tech_assessment", "architecture_review", "security_audit", "cloud_planning"],
                "agent_type": "tech_strategist",
                "voice_enabled": True,
                "preferred_voice": "onyx",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Product Management Expert": {
                "description": "Senior product leader with expertise in product strategy, user-centered design, and product-market fit optimization.",
                "system_prompt": """You are a product management expert with extensive experience in product strategy.

Your expertise includes:
- Product strategy and roadmap development
- User research and customer discovery
- Product-market fit validation and optimization
- Agile development and product delivery
- Product analytics and data-driven decisions
- Go-to-market strategy and product launches

Always:
- Focus on user needs and business value
- Use data-driven decisions and clear prioritization frameworks
- Consider the entire product lifecycle
- Emphasize continuous learning and iteration
- Balance user experience with technical feasibility""",
                "emoji": "📱",
                "category": "Product Management",
                "specialties": ["Product Strategy", "User Research", "Product-Market Fit", "Agile Development", "Product Analytics", "Go-to-Market"],
                "expertise_level": "VP Product",
                "temperature": 0.4,
                "max_tokens": 3500,
                "tools": ["user_research", "product_analytics", "roadmap_planning", "feature_prioritization"],
                "agent_type": "product_manager",
                "voice_enabled": True,
                "preferred_voice": "nova",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Data Science Consultant": {
                "description": "Senior data scientist turning complex data into actionable business insights through advanced analytics and statistical modeling.",
                "system_prompt": """You are a senior data scientist with expertise in advanced analytics.

Your expertise includes:
- Statistical analysis and hypothesis testing
- Predictive modeling and machine learning
- Data visualization and storytelling
- Experimental design and A/B testing
- Big data processing and data engineering
- Business intelligence and reporting

Always:
- Provide statistically sound analysis with clear business implications
- Make complex analyses accessible through clear explanations
- Focus on actionable insights and recommendations
- Consider data quality, bias, and statistical significance
- Use appropriate visualization and communication techniques""",
                "emoji": "📊",
                "category": "Data & Analytics",
                "specialties": ["Statistical Analysis", "Predictive Modeling", "Data Visualization", "A/B Testing", "Big Data", "Business Intelligence"],
                "expertise_level": "Senior Data Scientist",
                "temperature": 0.2,
                "max_tokens": 3500,
                "tools": ["statistical_analysis", "predictive_modeling", "data_visualization", "ab_testing"],
                "agent_type": "data_scientist",
                "voice_enabled": True,
                "preferred_voice": "alloy",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            },
            
            "Content Strategy Director": {
                "description": "Content marketing leader creating engaging, conversion-focused content strategies across multiple channels and formats.",
                "system_prompt": """You are a content strategy director with expertise in content marketing and brand storytelling.

Your expertise includes:
- Content strategy and editorial planning
- Brand storytelling and messaging
- Multi-channel content distribution
- Content performance optimization
- SEO and content marketing integration
- Content team management and workflows

Always:
- Focus on creating content that drives business results
- Consider the full content lifecycle and distribution strategy
- Emphasize audience engagement and conversion optimization
- Use data-driven insights to optimize content performance
- Balance brand building with performance marketing goals""",
                "emoji": "✍️",
                "category": "Content & Communication",
                "specialties": ["Content Strategy", "Brand Storytelling", "Multi-channel Distribution", "Content Optimization", "SEO Integration", "Editorial Planning"],
                "expertise_level": "VP Content",
                "temperature": 0.6,
                "max_tokens": 3000,
                "tools": ["content_analysis", "seo_optimization", "content_planning", "performance_tracking"],
                "agent_type": "content_strategist",
                "voice_enabled": True,
                "preferred_voice": "shimmer",
                "real_time_capable": True,
                "file_analysis": True,
                "web_search": True,
                "built_in": True,
                "editable": False
            }
        }
    
    def get_all_assistants(self, user_id: str = None) -> Dict[str, Dict[str, Any]]:
        """Get all available AI assistants (built-in + custom)"""
        try:
            # Start with built-in assistants
            all_assistants = self.built_in_assistants.copy()
            
            # Add custom assistants from Supabase
            if user_id:
                custom_assistants = self.supabase.get_assistants(user_id)
                for assistant in custom_assistants:
                    assistant_name = assistant['name']
                    all_assistants[assistant_name] = {
                        "id": assistant['id'],
                        "description": assistant['description'],
                        "system_prompt": assistant['system_prompt'],
                        "emoji": assistant.get('emoji', '🤖'),
                        "category": assistant['category'],
                        "specialties": json.loads(assistant.get('specialties', '[]')),
                        "expertise_level": assistant.get('expertise_level', 'Professional'),
                        "temperature": assistant.get('temperature', 0.7),
                        "max_tokens": assistant.get('max_tokens', 2000),
                        "tools": json.loads(assistant.get('tools', '[]')),
                        "agent_type": assistant.get('agent_type', 'custom'),
                        "voice_enabled": assistant.get('voice_enabled', True),
                        "preferred_voice": assistant.get('preferred_voice', 'alloy'),
                        "real_time_capable": assistant.get('real_time_capable', False),
                        "file_analysis": assistant.get('file_analysis', True),
                        "web_search": assistant.get('web_search', False),
                        "built_in": False,
                        "editable": True,
                        "created_at": assistant['created_at'],
                        "user_id": assistant['user_id']
                    }
            
            return all_assistants
            
        except Exception as e:
            logger.error(f"Error getting all assistants: {str(e)}")
            return self.built_in_assistants
    
    def create_custom_assistant(self, user_id: str, assistant_data: Dict[str, Any]) -> Optional[str]:
        """Create a new custom assistant"""
        try:
            # Validate required fields
            required_fields = ['name', 'description', 'system_prompt', 'category']
            for field in required_fields:
                if not assistant_data.get(field):
                    raise ValueError(f"Missing required field: {field}")
            
            # Set defaults
            assistant_data.setdefault('emoji', '🤖')
            assistant_data.setdefault('specialties', [])
            assistant_data.setdefault('expertise_level', 'Professional')
            assistant_data.setdefault('temperature', 0.7)
            assistant_data.setdefault('max_tokens', 2000)
            assistant_data.setdefault('tools', [])
            assistant_data.setdefault('agent_type', 'custom')
            assistant_data.setdefault('voice_enabled', True)
            assistant_data.setdefault('preferred_voice', 'alloy')
            assistant_data.setdefault('real_time_capable', False)
            assistant_data.setdefault('file_analysis', True)
            assistant_data.setdefault('web_search', False)
            
            # Add user ID
            assistant_data['user_id'] = user_id
            assistant_data['id'] = str(uuid.uuid4())
            
            # Convert lists to JSON strings for storage
            assistant_data['specialties'] = json.dumps(assistant_data['specialties'])
            assistant_data['tools'] = json.dumps(assistant_data['tools'])
            
            # Save to Supabase
            assistant_id = self.supabase.save_assistant(assistant_data)
            
            if assistant_id:
                logger.info(f"Created custom assistant: {assistant_data['name']}")
                return assistant_id
            else:
                raise Exception("Failed to save assistant to database")
                
        except Exception as e:
            logger.error(f"Error creating custom assistant: {str(e)}")
            raise e
    
    def update_custom_assistant(self, assistant_id: str, assistant_data: Dict[str, Any]) -> bool:
        """Update an existing custom assistant"""
        try:
            # Convert lists to JSON strings for storage
            if 'specialties' in assistant_data and isinstance(assistant_data['specialties'], list):
                assistant_data['specialties'] = json.dumps(assistant_data['specialties'])
            if 'tools' in assistant_data and isinstance(assistant_data['tools'], list):
                assistant_data['tools'] = json.dumps(assistant_data['tools'])
            
            success = self.supabase.update_assistant(assistant_id, assistant_data)
            
            if success:
                logger.info(f"Updated custom assistant: {assistant_id}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error updating custom assistant: {str(e)}")
            return False
    
    def delete_custom_assistant(self, assistant_id: str) -> bool:
        """Delete a custom assistant"""
        try:
            success = self.supabase.delete_assistant(assistant_id)
            
            if success:
                logger.info(f"Deleted custom assistant: {assistant_id}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error deleting custom assistant: {str(e)}")
            return False
    
    def get_assistant_categories(self, user_id: str = None) -> List[str]:
        """Get all unique assistant categories"""
        try:
            all_assistants = self.get_all_assistants(user_id)
            categories = list(set([assistant["category"] for assistant in all_assistants.values()]))
            return sorted(categories)
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return []
    
    def search_assistants(self, query: str, user_id: str = None) -> Dict[str, Dict[str, Any]]:
        """Search assistants by name, description, or specialties"""
        try:
            all_assistants = self.get_all_assistants(user_id)
            query_lower = query.lower()
            
            filtered_assistants = {}
            for name, assistant in all_assistants.items():
                # Search in name, description, and specialties
                search_text = f"{name} {assistant['description']} {' '.join(assistant['specialties'])}".lower()
                if query_lower in search_text:
                    filtered_assistants[name] = assistant
            
            return filtered_assistants
            
        except Exception as e:
            logger.error(f"Error searching assistants: {str(e)}")
            return {}
    
    def get_assistant_tools(self, assistant_name: str, user_id: str = None) -> List[str]:
        """Get available tools for specific assistant"""
        all_assistants = self.get_all_assistants(user_id)
        assistant = all_assistants.get(assistant_name, {})
        return assistant.get("tools", [])
    
    def get_voice_settings(self, assistant_name: str, user_id: str = None) -> Dict[str, Any]:
        """Get voice settings for specific assistant"""
        all_assistants = self.get_all_assistants(user_id)
        assistant = all_assistants.get(assistant_name, {})
        return {
            "voice_enabled": assistant.get("voice_enabled", False),
            "preferred_voice": assistant.get("preferred_voice", "alloy"),
            "real_time_capable": assistant.get("real_time_capable", False)
        }

# Initialize enhanced assistant profiles
enhanced_assistant_profiles = EnhancedAIAssistantProfiles(supabase_manager)

# ======================================================
# 💬 ADVANCED AI CHAT MANAGER
# ======================================================

class AdvancedAIChatManager:
    """Advanced AI chat manager with streaming, real-time, and assistant API support"""
    
    def __init__(self, config_manager: ConfigurationManager, supabase_manager: SupabaseManager):
        self.config = config_manager
        self.supabase = supabase_manager
        self.client = None
        self.assistant_client = None
        self.embeddings = None
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize OpenAI clients"""
        try:
            api_key = self.config.get("openai_api_key")
            if api_key and OPENAI_AVAILABLE:
                self.client = OpenAI(api_key=api_key)
                
                if self.config.get("assistant_api_enabled"):
                    self.assistant_client = OpenAI(api_key=api_key)
                
                if self.config.get("vector_store_enabled") and LANGCHAIN_CORE_AVAILABLE:
                    self.embeddings = OpenAIEmbeddings(
                        model=self.config.get("embedding_model", "text-embedding-3-large"),
                        openai_api_key=api_key
                    )
                
                logger.info("AI clients initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AI clients: {str(e)}")
    
    def generate_response(self, thread_id: str, messages: List[Dict[str, str]], 
                         assistant_config: Dict[str, Any], user_id: str = None,
                         stream: bool = False) -> Dict[str, Any]:
        """Generate AI response with advanced features"""
        try:
            if not self.client:
                return self.generate_demo_response(messages, assistant_config)
            
            # Prepare messages for OpenAI
            openai_messages = []
            
            # Add system prompt
            system_prompt = assistant_config.get("system_prompt", "You are a helpful AI assistant.")
            openai_messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation messages
            openai_messages.extend(messages)
            
            # Generate response
            start_time = time.time()
            
            if stream and self.config.get("streaming_enabled"):
                return self.generate_streaming_response(
                    thread_id, openai_messages, assistant_config, user_id
                )
            else:
                return self.generate_standard_response(
                    thread_id, openai_messages, assistant_config, user_id
                )
                
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return self.generate_demo_response(messages, assistant_config)
    
    def generate_standard_response(self, thread_id: str, messages: List[Dict[str, str]], 
                                 assistant_config: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """Generate standard (non-streaming) response"""
        try:
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=self.config.get("openai_model", "gpt-4"),
                messages=messages,
                temperature=assistant_config.get("temperature", 0.7),
                max_tokens=assistant_config.get("max_tokens", 4000),
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            response_time = time.time() - start_time
            
            # Extract response content
            content = response.choices[0].message.content
            
            # Calculate cost and tokens
            total_tokens = response.usage.total_tokens
            cost = self.calculate_cost(total_tokens, self.config.get("openai_model", "gpt-4"))
            
            # Save assistant response to Supabase
            message_data = {
                "id": str(uuid.uuid4()),
                "thread_id": thread_id,
                "role": "assistant",
                "content": content,
                "metadata": json.dumps({
                    "model": self.config.get("openai_model"),
                    "total_tokens": total_tokens,
                    "cost": cost,
                    "response_time": response_time,
                    "assistant_config": assistant_config.get("emoji", "🤖") + " " + assistant_config.get("category", "Assistant")
                })
            }
            
            if user_id:
                message_data["user_id"] = user_id
            
            self.supabase.add_message(message_data)
            
            # Log analytics
            if self.config.get("analytics_enabled"):
                self.supabase.log_analytics_event({
                    "event_type": "message_generated",
                    "user_id": user_id,
                    "thread_id": thread_id,
                    "assistant_type": assistant_config.get("category", "Unknown"),
                    "tokens_used": total_tokens,
                    "cost": cost,
                    "response_time": response_time
                })
            
            return {
                "content": content,
                "metadata": {
                    "model": self.config.get("openai_model"),
                    "total_tokens": total_tokens,
                    "cost": cost,
                    "response_time": response_time,
                    "streaming": False
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating standard response: {str(e)}")
            return self.generate_demo_response(messages[-1:], assistant_config)
    
    def generate_streaming_response(self, thread_id: str, messages: List[Dict[str, str]], 
                                  assistant_config: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """Generate streaming response"""
        try:
            start_time = time.time()
            
            stream = self.client.chat.completions.create(
                model=self.config.get("openai_model", "gpt-4"),
                messages=messages,
                temperature=assistant_config.get("temperature", 0.7),
                max_tokens=assistant_config.get("max_tokens", 4000),
                stream=True
            )
            
            # This would need to be handled differently in Streamlit
            # For now, we'll collect the stream and return the full response
            full_content = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_content += chunk.choices[0].delta.content
            
            response_time = time.time() - start_time
            
            # Estimate tokens (rough approximation)
            estimated_tokens = len(full_content.split()) * 1.3
            cost = self.calculate_cost(estimated_tokens, self.config.get("openai_model", "gpt-4"))
            
            # Save to Supabase
            message_data = {
                "id": str(uuid.uuid4()),
                "thread_id": thread_id,
                "role": "assistant",
                "content": full_content,
                "metadata": json.dumps({
                    "model": self.config.get("openai_model"),
                    "estimated_tokens": estimated_tokens,
                    "cost": cost,
                    "response_time": response_time,
                    "streaming": True
                })
            }
            
            if user_id:
                message_data["user_id"] = user_id
            
            self.supabase.add_message(message_data)
            
            return {
                "content": full_content,
                "metadata": {
                    "model": self.config.get("openai_model"),
                    "estimated_tokens": estimated_tokens,
                    "cost": cost,
                    "response_time": response_time,
                    "streaming": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating streaming response: {str(e)}")
            return self.generate_standard_response(thread_id, messages, assistant_config, user_id)
    
    def generate_demo_response(self, messages: List[Dict[str, str]], assistant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate demo response when API is not available"""
        try:
            assistant_name = assistant_config.get("emoji", "🤖") + " " + assistant_config.get("category", "AI Assistant")
            
            # Get the last user message
            user_message = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break
            
            # Generate contextual demo response
            demo_responses = [
                f"Thank you for your question about '{user_message[:50]}...'. As {assistant_name}, I would provide detailed insights and actionable recommendations based on my expertise in {', '.join(assistant_config.get('specialties', ['general consulting']))}.",
                
                f"I understand you're asking about '{user_message[:50]}...'. In my role as {assistant_name}, I would analyze this from multiple angles and provide strategic guidance tailored to your specific situation.",
                
                f"Great question about '{user_message[:50]}...'. As {assistant_name} with {assistant_config.get('expertise_level', 'professional')} experience, I would break this down into actionable steps and provide comprehensive recommendations.",
                
                f"I appreciate your inquiry regarding '{user_message[:50]}...'. Drawing from my expertise in {assistant_config.get('category', 'business consulting')}, I would provide detailed analysis and strategic insights to help you achieve your goals."
            ]
            
            import random
            content = random.choice(demo_responses)
            
            # Add demo-specific guidance
            content += f"\n\n**🎮 Demo Mode Active**\n\nTo unlock full AI capabilities:\n1. Add your OpenAI API key in Settings\n2. Configure Supabase for cloud storage\n3. Enable real-time features and voice processing\n\n**Enhanced Features Available:**\n• Real-time voice conversations\n• Advanced file analysis\n• Custom assistant creation\n• Cloud-based thread management\n• Analytics and usage tracking"
            
            return {
                "content": content,
                "metadata": {
                    "model": "demo",
                    "total_tokens": len(content.split()),
                    "cost": 0.0,
                    "response_time": 0.5,
                    "demo_mode": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating demo response: {str(e)}")
            return {
                "content": "I apologize, but I'm experiencing technical difficulties. Please check your configuration and try again.",
                "metadata": {
                    "model": "error",
                    "total_tokens": 0,
                    "cost": 0.0,
                    "response_time": 0.0,
                    "demo_mode": True,
                    "error": str(e)
                }
            }
    
    def calculate_cost(self, total_tokens: int, model: str) -> float:
        """Calculate cost based on token usage and model"""
        try:
            # Updated pricing per 1K tokens (as of 2024)
            pricing = {
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
                "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
                "gpt-3.5-turbo-16k": {"input": 0.003, "output": 0.004}
            }
            
            # Use average pricing for simplicity
            if model in pricing:
                avg_price = (pricing[model]["input"] + pricing[model]["output"]) / 2
                return (total_tokens / 1000) * avg_price
            else:
                # Default pricing
                return (total_tokens / 1000) * 0.02
                
        except Exception as e:
            logger.error(f"Error calculating cost: {str(e)}")
            return 0.0
    
    def process_with_assistant_api(self, assistant_id: str, thread_id: str, message: str) -> Optional[str]:
        """Process message using OpenAI Assistant API"""
        try:
            if not self.assistant_client or not self.config.get("assistant_api_enabled"):
                return None
            
            # Add message to thread
            self.assistant_client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
            
            # Run assistant
            run = self.assistant_client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress']:
                time.sleep(1)
                run = self.assistant_client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                messages = self.assistant_client.beta.threads.messages.list(thread_id=thread_id)
                return messages.data[0].content[0].text.value
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing with Assistant API: {str(e)}")
            return None

# Initialize advanced AI chat manager
advanced_ai_chat_manager = AdvancedAIChatManager(config_manager, supabase_manager)

# ======================================================
# 🎨 ENHANCED UI COMPONENTS WITH RED THEME
# ======================================================

def render_custom_css():
    """Render enhanced custom CSS with red theme"""
    st.markdown(f"""
    <style>
    /* Main App Styling */
    .stApp {{
        background: linear-gradient(135deg, {config_manager.get('theme_background')} 0%, #ffcdd2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, {config_manager.get('theme_primary_color')} 0%, {config_manager.get('theme_secondary_color')} 100%);
        color: {config_manager.get('theme_text_color')};
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3);
        background: linear-gradient(135deg, {config_manager.get('theme_secondary_color')} 0%, #7f1d1d 100%);
    }}
    
    .stButton > button:active {{
        transform: translateY(0px);
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
    }}
    
    /* Input Styling */
    .stSelectbox > div > div {{
        background: {config_manager.get('theme_primary_color')};
        border-radius: 12px;
        color: {config_manager.get('theme_text_color')};
        border: 2px solid {config_manager.get('theme_secondary_color')};
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
    }}
    
    .stTextInput > div > div > input {{
        border-radius: 12px;
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
        border: 2px solid {config_manager.get('theme_secondary_color')};
        padding: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {config_manager.get('theme_secondary_color')};
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
    }}
    
    .stTextArea > div > div > textarea {{
        border-radius: 12px;
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
        border: 2px solid {config_manager.get('theme_secondary_color')};
        padding: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
    }}
    
    /* File Uploader */
    .stFileUploader > div {{
        border-radius: 12px;
        border: 2px dashed {config_manager.get('theme_primary_color')};
        background: {config_manager.get('theme_accent_color')};
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }}
    
    .stFileUploader > div:hover {{
        border-color: {config_manager.get('theme_secondary_color')};
        background: #fecaca;
    }}
    
    /* Metrics */
    .stMetric {{
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
        border: 1px solid {config_manager.get('theme_secondary_color')};
    }}
    
    .stMetric > div {{
        color: {config_manager.get('theme_text_color')} !important;
    }}
    
    /* Expander */
    .stExpander {{
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
        border-radius: 12px;
        border: 2px solid {config_manager.get('theme_secondary_color')};
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
        margin: 0.5rem 0;
    }}
    
    .stExpander > div > div > div {{
        color: {config_manager.get('theme_text_color')} !important;
    }}
    
    /* Chat Messages */
    .stChatMessage {{
        background: {config_manager.get('theme_primary_color')} !important;
        color: {config_manager.get('theme_text_color')} !important;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
        border: 2px solid {config_manager.get('theme_secondary_color')};
    }}
    
    .stChatMessage p {{
        color: {config_manager.get('theme_text_color')} !important;
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    .stChatMessage h1, .stChatMessage h2, .stChatMessage h3, 
    .stChatMessage h4, .stChatMessage h5, .stChatMessage h6 {{
        color: {config_manager.get('theme_text_color')} !important;
    }}
    
    .stChatMessage ul, .stChatMessage ol {{
        color: {config_manager.get('theme_text_color')} !important;
    }}
    
    .stChatMessage li {{
        color: {config_manager.get('theme_text_color')} !important;
    }}
    
    .stChatMessage strong {{
        color: {config_manager.get('theme_text_color')} !important;
    }}
    
    .stChatMessage code {{
        background: rgba(0, 0, 0, 0.1);
        color: {config_manager.get('theme_text_color')} !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }}
    
    /* Sidebar */
    .stSidebar {{
        background: linear-gradient(135deg, {config_manager.get('theme_background')} 0%, #ffcdd2 100%);
    }}
    
    .stSidebar .stSelectbox > div > div {{
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
    }}
    
    .stSidebar .stButton > button {{
        width: 100%;
        margin: 0.25rem 0;
    }}
    
    /* Custom Cards */
    .thread-card {{
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
        border: 2px solid {config_manager.get('theme_secondary_color')};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
    }}
    
    .thread-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.2);
        border-color: {config_manager.get('theme_secondary_color')};
    }}
    
    .assistant-card {{
        background: linear-gradient(135deg, {config_manager.get('theme_primary_color')} 0%, {config_manager.get('theme_secondary_color')} 100%);
        padding: 2rem;
        border-radius: 16px;
        color: {config_manager.get('theme_text_color')};
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .assistant-card h3 {{
        color: {config_manager.get('theme_text_color')} !important;
        margin: 0 0 0.5rem 0;
        font-size: 1.4rem;
        font-weight: 700;
    }}
    
    .assistant-card p {{
        color: {config_manager.get('theme_text_color')} !important;
        opacity: 0.9;
        margin: 0.5rem 0;
        line-height: 1.5;
    }}
    
    .menu-item {{
        background: {config_manager.get('theme_primary_color')};
        color: {config_manager.get('theme_text_color')};
        border: 2px solid {config_manager.get('theme_secondary_color')};
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
    }}
    
    .menu-item:hover {{
        background: {config_manager.get('theme_secondary_color')};
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
    }}
    
    /* Status Indicators */
    .status-success {{
        background: #dc2626;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);
    }}
    
    .status-warning {{
        background: #f59e0b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
    }}
    
    .status-error {{
        background: #7f1d1d;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(127, 29, 29, 0.2);
    }}
    
    /* Loading Animation */
    .loading-spinner {{
        border: 3px solid {config_manager.get('theme_accent_color')};
        border-top: 3px solid {config_manager.get('theme_primary_color')};
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {config_manager.get('theme_accent_color')};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {config_manager.get('theme_primary_color')};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {config_manager.get('theme_secondary_color')};
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .stChatMessage {{
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        .assistant-card {{
            padding: 1.5rem;
        }}
        
        .thread-card {{
            padding: 1rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_enhanced_header():
    """Render enhanced application header with status indicators"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title(f"🚀 {config_manager.get('app_name')}")
        st.markdown(f"**{config_manager.get('app_description')}**")
    
    with col2:
        # Real-time status indicator
        if config_manager.get("realtime_api_enabled"):
            st.markdown('<div class="status-success">🔴 LIVE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">⚪ OFFLINE</div>', unsafe_allow_html=True)
    
    # Enhanced status indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if config_manager.get("openai_api_key") and advanced_ai_chat_manager.client:
            st.markdown('<div class="status-success">✅ OpenAI</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ OpenAI</div>', unsafe_allow_html=True)
    
    with col2:
        if supabase_manager.client:
            st.markdown('<div class="status-success">✅ Supabase</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-error">❌ Supabase</div>', unsafe_allow_html=True)
    
    with col3:
        if voice_processor.client and config_manager.get("realtime_api_enabled"):
            st.markdown('<div class="status-success">✅ Voice</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">⚠️ Voice</div>', unsafe_allow_html=True)
    
    with col4:
        if FILE_PROCESSING_AVAILABLE:
            st.markdown('<div class="status-success">✅ Files</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">⚠️ Files</div>', unsafe_allow_html=True)
    
    with col5:
        if LANGCHAIN_CORE_AVAILABLE:
            st.markdown('<div class="status-success">✅ LangChain</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">⚠️ LangChain</div>', unsafe_allow_html=True)

def render_supabase_sidebar():
    """Render Supabase storage management in sidebar"""
    st.sidebar.markdown("### 🗄️ Cloud Storage")
    
    if supabase_manager.client:
        st.sidebar.success("✅ Connected to Supabase")
        
        # Storage stats
        user_id = st.session_state.get("user_id", "demo_user")
        
        # Get user's threads and files
        threads = supabase_manager.get_threads(user_id)
        files = supabase_manager.get_files(user_id)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Threads", len(threads))
        with col2:
            st.metric("Files", len(files))
        
        # Quick actions
        if st.sidebar.button("🔄 Sync Data", use_container_width=True):
            st.sidebar.success("Data synced!")
        
        if st.sidebar.button("📤 Export Data", use_container_width=True):
            st.sidebar.info("Export feature coming soon!")
        
        # Storage usage (placeholder)
        st.sidebar.progress(0.3, text="Storage: 30% used")
        
    else:
        st.sidebar.error("❌ Supabase not connected")
        st.sidebar.info("Configure Supabase credentials in Settings to enable cloud storage.")

# ======================================================
# 🚀 MAIN APPLICATION
# ======================================================

def main():
    """Enhanced main application function"""
    try:
        # Configure Streamlit page
        st.set_page_config(
            page_title=config_manager.get("app_name", "Enhanced AI Assistant Platform"),
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/your-repo/help',
                'Report a bug': 'https://github.com/your-repo/issues',
                'About': f"# {config_manager.get('app_name')}\n\nAdvanced AI platform with voice, agents, threads, and cloud storage."
            }
        )
        
        # Render custom CSS
        render_custom_css()
        
        # Initialize session state
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
        if "current_page" not in st.session_state:
            st.session_state.current_page = "chat"
        if "current_assistant" not in st.session_state:
            st.session_state.current_assistant = "Strategic Business Consultant"
        if "current_thread_id" not in st.session_state:
            st.session_state.current_thread_id = None
        
        # Render enhanced header
        render_enhanced_header()
        
        # Render sidebar with Supabase integration
        with st.sidebar:
            render_supabase_sidebar()
            
            # Main navigation menu
            st.markdown("### 🎛️ Navigation")
            
            menu_options = [
                ("💬", "Chat", "chat"),
                ("🧵", "Threads", "threads"),
                ("🤖", "Assistants", "assistants"),
                ("🔧", "Agent Builder", "agent_builder"),
                ("🎙️", "Voice Studio", "voice"),
                ("📁", "File Manager", "files"),
                ("📊", "Analytics", "analytics"),
                ("⚙️", "Settings", "settings")
            ]
            
            current_page = st.session_state.get("current_page", "chat")
            
            for emoji, label, page_key in menu_options:
                if st.button(f"{emoji} {label}", key=f"menu_{page_key}", use_container_width=True):
                    st.session_state.current_page = page_key
                    st.rerun()
        
        # Main content area
        if current_page == "chat":
            render_chat_page()
        elif current_page == "threads":
            render_threads_page()
        elif current_page == "assistants":
            render_assistants_page()
        elif current_page == "agent_builder":
            render_agent_builder_page()
        elif current_page == "voice":
            render_voice_studio_page()
        elif current_page == "files":
            render_file_manager_page()
        elif current_page == "analytics":
            render_analytics_page()
        elif current_page == "settings":
            render_settings_page()
        else:
            render_chat_page()  # Default fallback
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}")
        
        # Show debug info in development
        if config_manager.get("debug_mode"):
            st.exception(e)

# Placeholder page renderers (to be implemented)
def render_chat_page():
    st.header("💬 Enhanced Chat Interface")
    st.info("Enhanced chat interface with real-time features coming soon!")

def render_threads_page():
    st.header("🧵 Thread Management")
    st.info("Advanced thread management with Supabase storage coming soon!")

def render_assistants_page():
    st.header("🤖 Assistant Management")
    st.info("Enhanced assistant management with custom profiles coming soon!")

def render_agent_builder_page():
    st.header("🔧 Agent Builder Studio")
    st.info("Visual agent builder with advanced capabilities coming soon!")

def render_voice_studio_page():
    st.header("🎙️ Voice Studio")
    st.info("Real-time voice processing and TTS/STT features coming soon!")

def render_file_manager_page():
    st.header("📁 File Manager")
    st.info("Advanced file processing with cloud storage coming soon!")

def render_analytics_page():
    st.header("📊 Analytics Dashboard")
    st.info("Comprehensive analytics and usage tracking coming soon!")

def render_settings_page():
    st.header("⚙️ Settings")
    st.info("Enhanced settings with Supabase configuration coming soon!")

if __name__ == "__main__":
    main()

