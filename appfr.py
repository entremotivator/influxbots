#!/usr/bin/env python3
"""
🚀 ENHANCED LANGCHAIN STREAMLIT CHAT BOT
Advanced AI platform with editable assistant profiles, threads, voice features, and agent builder
Optimized for Streamlit with comprehensive AI ecosystem integration
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
import sqlite3
import threading

# Core imports
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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

# Web scraping and API libraries
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_PROCESSING_AVAILABLE = True
except ImportError:
    WEB_PROCESSING_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🔐 CONFIGURATION MANAGEMENT
# ======================================================

class ConfigurationManager:
    """Enhanced configuration management for LangChain Streamlit app"""
    
    def __init__(self):
        self.config = self.load_configuration()
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load configuration from multiple sources"""
        try:
            config = {
                # OpenAI Configuration
                "openai_api_key": self._get_config_value("OPENAI_API_KEY", ""),
                "openai_model": self._get_config_value("OPENAI_MODEL", "gpt-4"),
                "openai_temperature": float(self._get_config_value("OPENAI_TEMPERATURE", "0.7")),
                "openai_max_tokens": int(self._get_config_value("OPENAI_MAX_TOKENS", "2000")),
                
                # Real-time API Configuration
                "openai_realtime_model": self._get_config_value("OPENAI_REALTIME_MODEL", "gpt-4o-realtime-preview"),
                "voice_enabled": self._get_config_value("VOICE_ENABLED", "true").lower() == "true",
                "voice_model": self._get_config_value("VOICE_MODEL", "tts-1"),
                "voice_speed": float(self._get_config_value("VOICE_SPEED", "1.0")),
                
                # File Processing Configuration
                "max_file_size_mb": int(self._get_config_value("MAX_FILE_SIZE_MB", "100")),
                "max_files_per_session": int(self._get_config_value("MAX_FILES_PER_SESSION", "50")),
                "supported_file_types": self._get_config_value("SUPPORTED_FILE_TYPES", "pdf,docx,txt,csv,json,xlsx,html,md,py,js").split(","),
                
                # Application Configuration
                "app_name": self._get_config_value("APP_NAME", "Enhanced AI Assistant Platform"),
                "app_description": self._get_config_value("APP_DESCRIPTION", "Advanced AI platform with threads, voice, and agent builder"),
                "debug_mode": self._get_config_value("DEBUG_MODE", "false").lower() == "true",
                
                # UI Configuration - Red Theme
                "theme_primary_color": "#dc3545",  # Red
                "theme_secondary_color": "#c82333",  # Darker red
                "theme_accent_color": "#ff6b6b",  # Light red
                "chat_card_color": "#dc3545",  # Red chat cards
                "text_color": "#000000",  # Black text
            }
            
            return config
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return self._get_default_configuration()
    
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
            "openai_api_key": "",
            "openai_model": "gpt-4",
            "openai_temperature": 0.7,
            "openai_max_tokens": 2000,
            "openai_realtime_model": "gpt-4o-realtime-preview",
            "voice_enabled": True,
            "voice_model": "tts-1",
            "voice_speed": 1.0,
            "max_file_size_mb": 100,
            "max_files_per_session": 50,
            "supported_file_types": ["pdf", "docx", "txt", "csv", "json", "xlsx", "html", "md", "py", "js"],
            "app_name": "Enhanced AI Assistant Platform",
            "app_description": "Advanced AI platform with threads, voice, and agent builder",
            "debug_mode": False,
            "theme_primary_color": "#dc3545",
            "theme_secondary_color": "#c82333",
            "theme_accent_color": "#ff6b6b",
            "chat_card_color": "#dc3545",
            "text_color": "#000000"
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        self.config[key] = value

# Initialize configuration manager
config_manager = ConfigurationManager()

# ======================================================
# 🗄️ DATABASE MANAGER
# ======================================================

class DatabaseManager:
    """Database manager for threads, conversations, and assistant profiles"""
    
    def __init__(self, db_path: str = "ai_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Threads table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS threads (
                        id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        assistant_id TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                # Messages table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY,
                        thread_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        FOREIGN KEY (thread_id) REFERENCES threads (id)
                    )
                """)
                
                # Custom assistants table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS custom_assistants (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        system_prompt TEXT,
                        emoji TEXT,
                        category TEXT,
                        specialties TEXT,
                        expertise_level TEXT,
                        temperature REAL,
                        max_tokens INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
    
    def create_thread(self, title: str, assistant_id: str, metadata: Dict = None) -> str:
        """Create a new thread"""
        try:
            thread_id = str(uuid.uuid4())
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO threads (id, title, assistant_id, metadata)
                    VALUES (?, ?, ?, ?)
                """, (thread_id, title, assistant_id, json.dumps(metadata or {})))
                conn.commit()
            return thread_id
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}")
            return None
    
    def get_threads(self, assistant_id: str = None) -> List[Dict]:
        """Get all threads, optionally filtered by assistant"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if assistant_id:
                    cursor.execute("""
                        SELECT * FROM threads WHERE assistant_id = ?
                        ORDER BY updated_at DESC
                    """, (assistant_id,))
                else:
                    cursor.execute("""
                        SELECT * FROM threads ORDER BY updated_at DESC
                    """)
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting threads: {str(e)}")
            return []
    
    def add_message(self, thread_id: str, role: str, content: str, metadata: Dict = None) -> str:
        """Add a message to a thread"""
        try:
            message_id = str(uuid.uuid4())
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO messages (id, thread_id, role, content, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (message_id, thread_id, role, content, json.dumps(metadata or {})))
                
                # Update thread timestamp
                cursor.execute("""
                    UPDATE threads SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (thread_id,))
                
                conn.commit()
            return message_id
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            return None
    
    def get_messages(self, thread_id: str) -> List[Dict]:
        """Get all messages in a thread"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM messages WHERE thread_id = ?
                    ORDER BY timestamp ASC
                """, (thread_id,))
                
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            return []
    
    def save_custom_assistant(self, assistant_data: Dict) -> str:
        """Save a custom assistant"""
        try:
            assistant_id = assistant_data.get('id', str(uuid.uuid4()))
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO custom_assistants 
                    (id, name, description, system_prompt, emoji, category, 
                     specialties, expertise_level, temperature, max_tokens)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    assistant_id,
                    assistant_data.get('name'),
                    assistant_data.get('description'),
                    assistant_data.get('system_prompt'),
                    assistant_data.get('emoji'),
                    assistant_data.get('category'),
                    json.dumps(assistant_data.get('specialties', [])),
                    assistant_data.get('expertise_level'),
                    assistant_data.get('temperature'),
                    assistant_data.get('max_tokens')
                ))
                conn.commit()
            return assistant_id
        except Exception as e:
            logger.error(f"Error saving custom assistant: {str(e)}")
            return None
    
    def get_custom_assistants(self) -> List[Dict]:
        """Get all custom assistants"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM custom_assistants ORDER BY created_at DESC")
                
                columns = [desc[0] for desc in cursor.description]
                assistants = []
                for row in cursor.fetchall():
                    assistant = dict(zip(columns, row))
                    # Parse JSON fields
                    if assistant.get('specialties'):
                        assistant['specialties'] = json.loads(assistant['specialties'])
                    assistants.append(assistant)
                return assistants
        except Exception as e:
            logger.error(f"Error getting custom assistants: {str(e)}")
            return []

# Initialize database manager
db_manager = DatabaseManager()

# ======================================================
# 🤖 ENHANCED AI ASSISTANT PROFILES
# ======================================================

class AIAssistantProfiles:
    """Enhanced AI assistant profiles with editing and expansion capabilities"""
    
    def __init__(self):
        self.db_manager = db_manager
        self.built_in_assistants = self._get_built_in_assistants()
    
    def _get_built_in_assistants(self) -> Dict[str, Dict[str, Any]]:
        """Get all built-in AI assistants (keeping original structure)"""
        return {
            "Strategic Business Consultant": {
                "description": "Senior strategic consultant with expertise in business transformation and growth strategy.",
                "system_prompt": "You are a strategic business consultant with 20+ years of experience. Provide data-driven insights, actionable recommendations, and strategic frameworks. Focus on both short-term tactics and long-term strategic implications.",
                "emoji": "🎯",
                "category": "Business Strategy",
                "specialties": ["Strategic Planning", "Market Analysis", "Business Transformation"],
                "expertise_level": "Senior Partner",
                "temperature": 0.3,
                "max_tokens": 3000,
                "editable": False,
                "built_in": True
            },
            
            "Startup Growth Advisor": {
                "description": "Experienced startup mentor specializing in scaling early-stage companies.",
                "system_prompt": "You are a startup growth advisor who has mentored 200+ startups. Be practical, action-oriented, and focused on measurable results. Provide specific tactics for resource-constrained environments.",
                "emoji": "🚀",
                "category": "Entrepreneurship",
                "specialties": ["Product-Market Fit", "Growth Hacking", "Fundraising"],
                "expertise_level": "Serial Entrepreneur",
                "temperature": 0.7,
                "max_tokens": 2500,
                "editable": False,
                "built_in": True
            },
            
            "Digital Marketing Strategist": {
                "description": "Performance marketing expert driving growth through data-driven campaigns.",
                "system_prompt": "You are a digital marketing strategist focused on performance marketing and growth analytics. Provide measurable ROI strategies, specific metrics, and testing frameworks.",
                "emoji": "📈",
                "category": "Marketing & Growth",
                "specialties": ["Performance Marketing", "Customer Acquisition", "Conversion Optimization"],
                "expertise_level": "VP Marketing",
                "temperature": 0.4,
                "max_tokens": 2800,
                "editable": False,
                "built_in": True
            },
            
            "Sales Performance Coach": {
                "description": "Elite sales trainer helping maximize revenue through proven methodologies.",
                "system_prompt": "You are a sales performance coach with expertise in consultative selling and sales psychology. Provide practical, actionable sales techniques focused on long-term relationships.",
                "emoji": "💰",
                "category": "Sales & Revenue",
                "specialties": ["Consultative Selling", "Objection Handling", "Pipeline Management"],
                "expertise_level": "VP Sales",
                "temperature": 0.5,
                "max_tokens": 2500,
                "editable": False,
                "built_in": True
            },
            
            "Financial Strategy Advisor": {
                "description": "CFO-level financial expert optimizing business finances and strategic planning.",
                "system_prompt": "You are a financial strategy advisor with CFO-level expertise. Provide detailed financial analysis with calculations, focus on sustainable growth and risk mitigation.",
                "emoji": "💼",
                "category": "Finance & Investment",
                "specialties": ["Financial Planning", "Investment Strategy", "Risk Management"],
                "expertise_level": "CFO",
                "temperature": 0.2,
                "max_tokens": 3500,
                "editable": False,
                "built_in": True
            },
            
            "AI & Machine Learning Specialist": {
                "description": "Advanced AI researcher helping organizations leverage artificial intelligence.",
                "system_prompt": "You are an AI and machine learning specialist with deep expertise. Provide technically accurate guidance while making concepts accessible. Focus on practical applications and business value.",
                "emoji": "🤖",
                "category": "Artificial Intelligence",
                "specialties": ["Machine Learning", "Natural Language Processing", "Data Science"],
                "expertise_level": "AI Research Director",
                "temperature": 0.3,
                "max_tokens": 3500,
                "editable": False,
                "built_in": True
            },
            
            "Technology Strategy Consultant": {
                "description": "CTO-level technology advisor guiding digital transformation and innovation.",
                "system_prompt": "You are a technology strategy consultant with CTO-level expertise. Balance technical feasibility with business value, provide implementation roadmaps with risk assessments.",
                "emoji": "💻",
                "category": "Technology & Innovation",
                "specialties": ["Digital Transformation", "Technology Architecture", "Innovation Strategy"],
                "expertise_level": "CTO",
                "temperature": 0.4,
                "max_tokens": 3200,
                "editable": False,
                "built_in": True
            },
            
            "Product Management Expert": {
                "description": "Senior product leader with expertise in product strategy and user-centered design.",
                "system_prompt": "You are a product management expert with extensive experience in product strategy. Focus on user needs and business value with data-driven decisions and clear prioritization.",
                "emoji": "📱",
                "category": "Product Management",
                "specialties": ["Product Strategy", "User Research", "Product-Market Fit"],
                "expertise_level": "VP Product",
                "temperature": 0.4,
                "max_tokens": 2900,
                "editable": False,
                "built_in": True
            },
            
            "Data Science Consultant": {
                "description": "Senior data scientist turning complex data into actionable business insights.",
                "system_prompt": "You are a senior data scientist with expertise in advanced analytics. Provide statistically sound analysis with clear business implications. Make complex analyses accessible through clear explanations.",
                "emoji": "📊",
                "category": "Data & Analytics",
                "specialties": ["Statistical Analysis", "Predictive Modeling", "Data Visualization"],
                "expertise_level": "Senior Data Scientist",
                "temperature": 0.2,
                "max_tokens": 3200,
                "editable": False,
                "built_in": True
            },
            
            "Content Strategy Director": {
                "description": "Content marketing leader creating engaging, conversion-focused content strategies.",
                "system_prompt": "You are a content strategy director with expertise in content marketing and brand storytelling. Focus on creating content that drives business results and audience engagement.",
                "emoji": "✍️",
                "category": "Content & Communication",
                "specialties": ["Content Strategy", "Brand Storytelling", "Multi-channel Distribution"],
                "expertise_level": "VP Content",
                "temperature": 0.6,
                "max_tokens": 2800,
                "editable": False,
                "built_in": True
            }
        }
    
    def get_all_assistants(self) -> Dict[str, Dict[str, Any]]:
        """Get all available AI assistants (built-in + custom)"""
        try:
            # Start with built-in assistants
            all_assistants = self.built_in_assistants.copy()
            
            # Add custom assistants from database
            custom_assistants = self.db_manager.get_custom_assistants()
            for assistant in custom_assistants:
                assistant_name = assistant['name']
                all_assistants[assistant_name] = {
                    "id": assistant['id'],
                    "description": assistant['description'],
                    "system_prompt": assistant['system_prompt'],
                    "emoji": assistant['emoji'],
                    "category": assistant['category'],
                    "specialties": assistant['specialties'] or [],
                    "expertise_level": assistant['expertise_level'],
                    "temperature": assistant['temperature'],
                    "max_tokens": assistant['max_tokens'],
                    "editable": True,
                    "built_in": False,
                    "created_at": assistant['created_at']
                }
            
            return all_assistants
            
        except Exception as e:
            logger.error(f"Error getting all assistants: {str(e)}")
            return self.built_in_assistants
    
    def create_custom_assistant(self, assistant_data: Dict[str, Any]) -> str:
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
            
            # Save to database
            assistant_id = self.db_manager.save_custom_assistant(assistant_data)
            
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
            assistant_data['id'] = assistant_id
            updated_id = self.db_manager.save_custom_assistant(assistant_data)
            
            if updated_id:
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
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM custom_assistants WHERE id = ?", (assistant_id,))
                conn.commit()
                
                if cursor.rowcount > 0:
                    logger.info(f"Deleted custom assistant: {assistant_id}")
                    return True
                else:
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting custom assistant: {str(e)}")
            return False
    
    def get_assistant_categories(self) -> List[str]:
        """Get all unique assistant categories"""
        try:
            all_assistants = self.get_all_assistants()
            categories = list(set([assistant["category"] for assistant in all_assistants.values()]))
            return sorted(categories)
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return []
    
    def search_assistants(self, query: str) -> Dict[str, Dict[str, Any]]:
        """Search assistants by name, description, or specialties"""
        try:
            all_assistants = self.get_all_assistants()
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

# Initialize assistant profiles
assistant_profiles = AIAssistantProfiles()

# ======================================================
# 🎙️ VOICE AND REAL-TIME API MANAGER
# ======================================================

class VoiceManager:
    """Voice and real-time API manager"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.client = None
        self.voice_enabled = config_manager.get("voice_enabled", True)
        
        if OPENAI_AVAILABLE and config_manager.get("openai_api_key"):
            try:
                self.client = OpenAI(api_key=config_manager.get("openai_api_key"))
            except Exception as e:
                logger.error(f"Error initializing OpenAI client for voice: {str(e)}")
    
    def text_to_speech(self, text: str, voice: str = "alloy") -> bytes:
        """Convert text to speech using OpenAI TTS"""
        try:
            if not self.client:
                raise Exception("OpenAI client not available")
            
            response = self.client.audio.speech.create(
                model=self.config_manager.get("voice_model", "tts-1"),
                voice=voice,
                input=text,
                speed=self.config_manager.get("voice_speed", 1.0)
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return None
    
    def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text using OpenAI Whisper"""
        try:
            if not self.client:
                raise Exception("OpenAI client not available")
            
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                with open(temp_file_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                return transcript.text
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Error in speech-to-text: {str(e)}")
            return ""
    
    def get_available_voices(self) -> List[str]:
        """Get list of available TTS voices"""
        return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Initialize voice manager
voice_manager = VoiceManager(config_manager)

# ======================================================
# 💬 ENHANCED AI CHAT MANAGER
# ======================================================

class EnhancedAIChatManager:
    """Enhanced AI chat manager with thread support"""
    
    def __init__(self, config_manager, db_manager):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.client = None
        
        if OPENAI_AVAILABLE and config_manager.get("openai_api_key"):
            try:
                self.client = OpenAI(api_key=config_manager.get("openai_api_key"))
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {str(e)}")
    
    def generate_response(self, thread_id: str, messages: List[Dict[str, str]], assistant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI response and save to thread"""
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
            
            response = self.client.chat.completions.create(
                model=self.config_manager.get("openai_model", "gpt-4"),
                messages=openai_messages,
                temperature=assistant_config.get("temperature", 0.7),
                max_tokens=assistant_config.get("max_tokens", 2000)
            )
            
            response_time = time.time() - start_time
            
            # Extract response content
            content = response.choices[0].message.content
            
            # Calculate cost
            total_tokens = response.usage.total_tokens
            cost = self.calculate_cost(total_tokens, self.config_manager.get("openai_model", "gpt-4"))
            
            # Save assistant response to thread
            self.db_manager.add_message(
                thread_id=thread_id,
                role="assistant",
                content=content,
                metadata={
                    "model": self.config_manager.get("openai_model"),
                    "total_tokens": total_tokens,
                    "cost": cost,
                    "response_time": response_time,
                    "assistant_config": assistant_config
                }
            )
            
            return {
                "content": content,
                "metadata": {
                    "model": self.config_manager.get("openai_model"),
                    "total_tokens": total_tokens,
                    "cost": cost,
                    "response_time": response_time
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return self.generate_demo_response(messages, assistant_config)
    
    def generate_demo_response(self, messages: List[Dict[str, str]], assistant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate demo response when API is not available"""
        try:
            assistant_name = assistant_config.get("emoji", "🤖") + " " + "AI Assistant"
            
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
                
                f"Great question about '{user_message[:50]}...'. As {assistant_name} with {assistant_config.get('expertise_level', 'professional')} experience, I would break this down into actionable steps and provide comprehensive recommendations."
            ]
            
            import random
            content = random.choice(demo_responses)
            
            # Add demo-specific guidance
            content += f"\n\n**🎮 Demo Mode Active**\n\nTo get real AI responses:\n1. Add your OpenAI API key to Streamlit secrets\n2. The assistant will provide comprehensive, personalized guidance\n3. Full document analysis and context integration will be available"
            
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
                "content": "I apologize, but I'm experiencing technical difficulties. Please try again or check your configuration.",
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
            # Pricing per 1K tokens (approximate)
            pricing = {
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
            }
            
            # Use average pricing for simplicity
            if model in pricing:
                avg_price = (pricing[model]["input"] + pricing[model]["output"]) / 2
                return (total_tokens / 1000) * avg_price
            else:
                # Default pricing
                return (total_tokens / 1000) * 0.01
                
        except Exception as e:
            logger.error(f"Error calculating cost: {str(e)}")
            return 0.0

# Initialize enhanced AI chat manager
enhanced_ai_chat_manager = EnhancedAIChatManager(config_manager, db_manager)

# ======================================================
# 🎨 ENHANCED UI COMPONENTS
# ======================================================

def render_custom_css():
    """Render custom CSS with red theme"""
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {config_manager.get('theme_primary_color')} 0%, {config_manager.get('theme_secondary_color')} 100%);
        color: {config_manager.get('text_color')};
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }}
    
    .stSelectbox > div > div {{
        background: {config_manager.get('chat_card_color')};
        border-radius: 10px;
        color: {config_manager.get('text_color')};
    }}
    
    .stTextInput > div > div > input {{
        border-radius: 10px;
        background: {config_manager.get('chat_card_color')};
        color: {config_manager.get('text_color')};
        border: 2px solid {config_manager.get('theme_primary_color')};
    }}
    
    .stFileUploader > div {{
        border-radius: 10px;
        border: 2px dashed {config_manager.get('theme_primary_color')};
        background: {config_manager.get('chat_card_color')};
    }}
    
    .stMetric {{
        background: {config_manager.get('chat_card_color')};
        color: {config_manager.get('text_color')};
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(220, 53, 69, 0.2);
    }}
    
    .stExpander {{
        background: {config_manager.get('chat_card_color')};
        color: {config_manager.get('text_color')};
        border-radius: 10px;
        border: 1px solid {config_manager.get('theme_primary_color')};
    }}
    
    .stChatMessage {{
        background: {config_manager.get('chat_card_color')} !important;
        color: {config_manager.get('text_color')} !important;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(220, 53, 69, 0.2);
        border: 1px solid {config_manager.get('theme_primary_color')};
    }}
    
    .stChatMessage p {{
        color: {config_manager.get('text_color')} !important;
    }}
    
    .stSidebar {{
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
    }}
    
    .stSidebar .stSelectbox > div > div {{
        background: {config_manager.get('chat_card_color')};
        color: {config_manager.get('text_color')};
    }}
    
    .thread-card {{
        background: {config_manager.get('chat_card_color')};
        color: {config_manager.get('text_color')};
        border: 2px solid {config_manager.get('theme_primary_color')};
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .thread-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }}
    
    .assistant-card {{
        background: linear-gradient(135deg, {config_manager.get('theme_primary_color')} 0%, {config_manager.get('theme_secondary_color')} 100%);
        padding: 20px;
        border-radius: 15px;
        color: {config_manager.get('text_color')};
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }}
    
    .menu-item {{
        background: {config_manager.get('chat_card_color')};
        color: {config_manager.get('text_color')};
        border: 1px solid {config_manager.get('theme_primary_color')};
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .menu-item:hover {{
        background: {config_manager.get('theme_accent_color')};
        transform: translateX(5px);
    }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render enhanced application header"""
    st.title(f"🚀 {config_manager.get('app_name')}")
    st.markdown(f"**{config_manager.get('app_description')}**")
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if config_manager.get("openai_api_key"):
            if enhanced_ai_chat_manager.client:
                st.success("✅ OpenAI Connected")
            else:
                st.error("❌ OpenAI Failed")
        else:
            st.warning("🔑 API Key Required")
    
    with col2:
        if voice_manager.voice_enabled and voice_manager.client:
            st.success("✅ Voice Ready")
        else:
            st.warning("🎙️ Voice Limited")
    
    with col3:
        if FILE_PROCESSING_AVAILABLE:
            st.success("✅ Files Ready")
        else:
            st.warning("⚠️ Limited Files")
    
    with col4:
        thread_count = len(db_manager.get_threads())
        st.metric("Threads", thread_count)

def render_main_menu():
    """Render main navigation menu"""
    st.sidebar.markdown("### 🎛️ Main Menu")
    
    menu_options = [
        ("💬", "Chat", "chat"),
        ("🧵", "Threads", "threads"),
        ("🤖", "Assistants", "assistants"),
        ("🔧", "Agent Builder", "agent_builder"),
        ("🎙️", "Voice Settings", "voice"),
        ("📁", "File Manager", "files"),
        ("📊", "Analytics", "analytics"),
        ("⚙️", "Settings", "settings")
    ]
    
    current_page = st.session_state.get("current_page", "chat")
    
    for emoji, label, page_key in menu_options:
        if st.sidebar.button(f"{emoji} {label}", key=f"menu_{page_key}", use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()
    
    return current_page

def render_thread_management():
    """Render thread management interface"""
    st.sidebar.markdown("### 🧵 Thread Management")
    
    # New thread button
    if st.sidebar.button("➕ New Thread", use_container_width=True):
        current_assistant = st.session_state.get("current_assistant", "Strategic Business Consultant")
        thread_title = f"New Chat - {datetime.now().strftime('%m/%d %H:%M')}"
        thread_id = db_manager.create_thread(thread_title, current_assistant)
        if thread_id:
            st.session_state.current_thread_id = thread_id
            st.rerun()
    
    # Get threads for current assistant
    current_assistant = st.session_state.get("current_assistant", "Strategic Business Consultant")
    threads = db_manager.get_threads(current_assistant)
    
    if threads:
        st.sidebar.markdown("**Recent Threads:**")
        
        for thread in threads[:5]:  # Show last 5 threads
            thread_id = thread['id']
            thread_title = thread['title']
            updated_at = thread['updated_at']
            
            # Parse datetime
            try:
                dt = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                time_str = dt.strftime('%m/%d %H:%M')
            except:
                time_str = "Recent"
            
            # Thread button
            button_text = f"📝 {thread_title[:20]}..."
            if st.sidebar.button(button_text, key=f"thread_{thread_id}", help=f"Updated: {time_str}"):
                st.session_state.current_thread_id = thread_id
                st.rerun()
    
    # Current thread info
    current_thread_id = st.session_state.get("current_thread_id")
    if current_thread_id:
        messages = db_manager.get_messages(current_thread_id)
        st.sidebar.info(f"💬 Messages: {len(messages)}")

def render_assistant_selector():
    """Render enhanced assistant selector"""
    st.sidebar.markdown("### 🤖 AI Assistants")
    
    # Get all assistants
    all_assistants = assistant_profiles.get_all_assistants()
    
    # Search functionality
    search_query = st.sidebar.text_input("🔍 Search Assistants", placeholder="Search by name or specialty...")
    
    if search_query:
        filtered_assistants = assistant_profiles.search_assistants(search_query)
    else:
        # Category filter
        categories = assistant_profiles.get_assistant_categories()
        selected_category = st.sidebar.selectbox(
            "Filter by Category", 
            ["All Categories"] + categories
        )
        
        # Filter assistants
        filtered_assistants = {}
        for name, assistant in all_assistants.items():
            if selected_category == "All Categories" or assistant["category"] == selected_category:
                filtered_assistants[name] = assistant
    
    # Assistant selection
    assistant_names = list(filtered_assistants.keys())
    
    if not assistant_names:
        st.sidebar.warning("No assistants match the selected filters.")
        return None
    
    current_assistant = st.session_state.get("current_assistant", assistant_names[0])
    
    if current_assistant not in assistant_names:
        current_assistant = assistant_names[0]
    
    selected_assistant = st.sidebar.selectbox(
        "Select Your AI Assistant", 
        assistant_names, 
        index=assistant_names.index(current_assistant) if current_assistant in assistant_names else 0
    )
    
    # Update session state if changed
    if selected_assistant != st.session_state.get("current_assistant"):
        st.session_state.current_assistant = selected_assistant
        # Create new thread for new assistant
        thread_title = f"Chat with {selected_assistant} - {datetime.now().strftime('%m/%d %H:%M')}"
        thread_id = db_manager.create_thread(thread_title, selected_assistant)
        if thread_id:
            st.session_state.current_thread_id = thread_id
        st.rerun()
    
    # Display assistant profile
    if selected_assistant in all_assistants:
        assistant_config = all_assistants[selected_assistant]
        
        st.sidebar.markdown(f"""
        <div class="assistant-card">
            <h3 style="margin: 0; color: {config_manager.get('text_color')};">{assistant_config['emoji']} {selected_assistant}</h3>
            <p style="margin: 8px 0; opacity: 0.9; font-weight: bold;">{assistant_config['expertise_level']}</p>
            <p style="margin: 8px 0; opacity: 0.8;">{assistant_config['category']}</p>
            <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 0.9em;">{assistant_config['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed profile
        with st.sidebar.expander("📋 Assistant Details"):
            st.write(f"**🎯 Specialties:**")
            for specialty in assistant_config['specialties']:
                st.write(f"• {specialty}")
            
            st.write(f"\n**⚙️ Configuration:**")
            st.write(f"• Temperature: {assistant_config.get('temperature', 0.7)}")
            st.write(f"• Max Tokens: {assistant_config.get('max_tokens', 2000):,}")
            
            # Edit button for custom assistants
            if assistant_config.get('editable', False):
                if st.button("✏️ Edit Assistant", key=f"edit_{selected_assistant}"):
                    st.session_state.editing_assistant = selected_assistant
                    st.session_state.current_page = "agent_builder"
                    st.rerun()
        
        return selected_assistant
    
    return None

def render_file_upload_sidebar():
    """Render enhanced file upload in sidebar"""
    st.sidebar.markdown("### 📁 File Upload")
    
    # Upload configuration
    max_size_mb = config_manager.get("max_file_size_mb", 100)
    max_files = config_manager.get("max_files_per_session", 50)
    supported_types = config_manager.get("supported_file_types", [])
    
    st.sidebar.info(f"""
    **📊 Upload Limits**
    • Max file size: {max_size_mb}MB
    • Max files: {max_files}
    • Supported: {len(supported_types)} formats
    """)
    
    # File uploader
    uploaded_files = st.sidebar.file_uploader(
        "📤 Upload Files for Analysis",
        accept_multiple_files=True,
        type=supported_types if supported_types else None,
        help="Upload documents, data files, images, or code for AI analysis"
    )
    
    # Process uploaded files
    if uploaded_files:
        st.sidebar.success(f"✅ {len(uploaded_files)} files uploaded")
        
        # Store files in session state
        st.session_state.uploaded_files = uploaded_files
        
        # Display file list
        with st.sidebar.expander("📋 Uploaded Files"):
            for file in uploaded_files:
                st.write(f"📄 {file.name} ({file.size:,} bytes)")

def render_voice_controls():
    """Render voice controls in sidebar"""
    if voice_manager.voice_enabled:
        st.sidebar.markdown("### 🎙️ Voice Controls")
        
        # Voice settings
        available_voices = voice_manager.get_available_voices()
        selected_voice = st.sidebar.selectbox("Voice", available_voices, index=0)
        
        # Voice speed
        voice_speed = st.sidebar.slider("Speed", 0.5, 2.0, 1.0, 0.1)
        
        # Update config
        config_manager.update("voice_speed", voice_speed)
        
        # Voice input button
        if st.sidebar.button("🎤 Voice Input", use_container_width=True):
            st.sidebar.info("Voice input feature coming soon!")
        
        # Text-to-speech for last message
        if st.sidebar.button("🔊 Read Last Message", use_container_width=True):
            current_thread_id = st.session_state.get("current_thread_id")
            if current_thread_id:
                messages = db_manager.get_messages(current_thread_id)
                if messages:
                    last_message = messages[-1]
                    if last_message['role'] == 'assistant':
                        audio_data = voice_manager.text_to_speech(last_message['content'], selected_voice)
                        if audio_data:
                            st.sidebar.audio(audio_data, format='audio/mp3')

# ======================================================
# 📱 PAGE RENDERERS
# ======================================================

def render_chat_page():
    """Render main chat interface"""
    # Initialize current thread if not exists
    current_thread_id = st.session_state.get("current_thread_id")
    current_assistant = st.session_state.get("current_assistant", "Strategic Business Consultant")
    
    if not current_thread_id:
        thread_title = f"Chat with {current_assistant} - {datetime.now().strftime('%m/%d %H:%M')}"
        thread_id = db_manager.create_thread(thread_title, current_assistant)
        if thread_id:
            st.session_state.current_thread_id = thread_id
            current_thread_id = thread_id
    
    # Get assistant config
    all_assistants = assistant_profiles.get_all_assistants()
    assistant_config = all_assistants.get(current_assistant, {})
    
    # Display conversation
    if current_thread_id:
        messages = db_manager.get_messages(current_thread_id)
        
        # Display messages
        for message in messages:
            role = message['role']
            content = message['content']
            
            with st.chat_message(role):
                st.markdown(content)
        
        # Chat input
        if prompt := st.chat_input("Ask your AI assistant anything..."):
            # Add user message to thread
            db_manager.add_message(current_thread_id, "user", prompt)
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Prepare messages for AI
                    conversation_messages = []
                    for msg in messages:
                        conversation_messages.append({
                            "role": msg['role'],
                            "content": msg['content']
                        })
                    
                    # Add current user message
                    conversation_messages.append({"role": "user", "content": prompt})
                    
                    # Generate response
                    response_data = enhanced_ai_chat_manager.generate_response(
                        current_thread_id, conversation_messages, assistant_config
                    )
                    
                    # Display response
                    st.markdown(response_data["content"])
            
            st.rerun()

def render_threads_page():
    """Render threads management page"""
    st.header("🧵 Thread Management")
    
    # Get all threads
    threads = db_manager.get_threads()
    
    if not threads:
        st.info("No threads found. Start a new conversation to create your first thread!")
        return
    
    # Thread statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Threads", len(threads))
    with col2:
        total_messages = sum(len(db_manager.get_messages(thread['id'])) for thread in threads)
        st.metric("Total Messages", total_messages)
    with col3:
        active_threads = len([t for t in threads if len(db_manager.get_messages(t['id'])) > 0])
        st.metric("Active Threads", active_threads)
    
    # Thread list
    st.subheader("📋 All Threads")
    
    for thread in threads:
        thread_id = thread['id']
        thread_title = thread['title']
        assistant_id = thread['assistant_id']
        updated_at = thread['updated_at']
        
        # Get message count
        messages = db_manager.get_messages(thread_id)
        message_count = len(messages)
        
        # Parse datetime
        try:
            dt = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            time_str = dt.strftime('%Y-%m-%d %H:%M')
        except:
            time_str = "Unknown"
        
        # Thread card
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if st.button(f"💬 {thread_title}", key=f"open_thread_{thread_id}"):
                    st.session_state.current_thread_id = thread_id
                    st.session_state.current_assistant = assistant_id
                    st.session_state.current_page = "chat"
                    st.rerun()
                
                st.caption(f"Assistant: {assistant_id} | Updated: {time_str}")
            
            with col2:
                st.metric("Messages", message_count)
            
            with col3:
                if st.button("🗑️", key=f"delete_thread_{thread_id}", help="Delete thread"):
                    # Delete thread and messages
                    with sqlite3.connect(db_manager.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM messages WHERE thread_id = ?", (thread_id,))
                        cursor.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
                        conn.commit()
                    st.rerun()
        
        st.divider()

def render_assistants_page():
    """Render assistants management page"""
    st.header("🤖 Assistant Management")
    
    # Get all assistants
    all_assistants = assistant_profiles.get_all_assistants()
    
    # Assistant statistics
    built_in_count = len([a for a in all_assistants.values() if a.get('built_in', True)])
    custom_count = len([a for a in all_assistants.values() if not a.get('built_in', True)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Assistants", len(all_assistants))
    with col2:
        st.metric("Built-in", built_in_count)
    with col3:
        st.metric("Custom", custom_count)
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📋 All Assistants", "➕ Create New"])
    
    with tab1:
        # Category filter
        categories = assistant_profiles.get_assistant_categories()
        selected_category = st.selectbox("Filter by Category", ["All Categories"] + categories)
        
        # Filter assistants
        filtered_assistants = {}
        for name, assistant in all_assistants.items():
            if selected_category == "All Categories" or assistant["category"] == selected_category:
                filtered_assistants[name] = assistant
        
        # Display assistants
        for name, assistant in filtered_assistants.items():
            with st.expander(f"{assistant['emoji']} {name}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Category:** {assistant['category']}")
                    st.write(f"**Expertise:** {assistant['expertise_level']}")
                    st.write(f"**Description:** {assistant['description']}")
                    st.write(f"**Specialties:** {', '.join(assistant['specialties'])}")
                
                with col2:
                    st.write(f"**Temperature:** {assistant.get('temperature', 0.7)}")
                    st.write(f"**Max Tokens:** {assistant.get('max_tokens', 2000):,}")
                    st.write(f"**Type:** {'Custom' if assistant.get('editable', False) else 'Built-in'}")
                    
                    if assistant.get('editable', False):
                        if st.button("✏️ Edit", key=f"edit_assistant_{name}"):
                            st.session_state.editing_assistant = name
                            st.session_state.current_page = "agent_builder"
                            st.rerun()
    
    with tab2:
        st.subheader("➕ Create New Assistant")
        st.info("Use the Agent Builder to create custom assistants with specific capabilities.")
        
        if st.button("🔧 Open Agent Builder", use_container_width=True):
            st.session_state.current_page = "agent_builder"
            st.rerun()

def render_agent_builder_page():
    """Render agent builder page"""
    st.header("🔧 Agent Builder")
    
    # Check if editing existing assistant
    editing_assistant = st.session_state.get("editing_assistant")
    if editing_assistant:
        st.info(f"Editing: {editing_assistant}")
        all_assistants = assistant_profiles.get_all_assistants()
        assistant_data = all_assistants.get(editing_assistant, {})
    else:
        st.info("Creating new custom assistant")
        assistant_data = {}
    
    # Assistant form
    with st.form("assistant_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Assistant Name", value=assistant_data.get('name', ''))
            emoji = st.text_input("Emoji", value=assistant_data.get('emoji', '🤖'))
            category = st.text_input("Category", value=assistant_data.get('category', ''))
            expertise_level = st.text_input("Expertise Level", value=assistant_data.get('expertise_level', 'Professional'))
        
        with col2:
            temperature = st.slider("Temperature", 0.0, 2.0, assistant_data.get('temperature', 0.7), 0.1)
            max_tokens = st.number_input("Max Tokens", 100, 4000, assistant_data.get('max_tokens', 2000))
            
            # Specialties
            specialties_text = st.text_area(
                "Specialties (one per line)", 
                value='\n'.join(assistant_data.get('specialties', []))
            )
        
        description = st.text_area("Description", value=assistant_data.get('description', ''))
        system_prompt = st.text_area(
            "System Prompt", 
            value=assistant_data.get('system_prompt', ''),
            height=200,
            help="This defines how the assistant behaves and responds"
        )
        
        # Form buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            submitted = st.form_submit_button("💾 Save Assistant", use_container_width=True)
        
        with col2:
            if st.form_submit_button("🧪 Test Assistant", use_container_width=True):
                st.session_state.testing_assistant = True
        
        with col3:
            if editing_assistant and st.form_submit_button("🗑️ Delete", use_container_width=True):
                # Delete custom assistant
                all_assistants = assistant_profiles.get_all_assistants()
                assistant_config = all_assistants.get(editing_assistant, {})
                if assistant_config.get('id'):
                    assistant_profiles.delete_custom_assistant(assistant_config['id'])
                    st.success(f"Deleted assistant: {editing_assistant}")
                    st.session_state.editing_assistant = None
                    st.rerun()
        
        # Handle form submission
        if submitted:
            try:
                # Validate required fields
                if not name or not description or not system_prompt:
                    st.error("Please fill in all required fields (Name, Description, System Prompt)")
                else:
                    # Prepare assistant data
                    new_assistant_data = {
                        'name': name,
                        'description': description,
                        'system_prompt': system_prompt,
                        'emoji': emoji,
                        'category': category,
                        'specialties': [s.strip() for s in specialties_text.split('\n') if s.strip()],
                        'expertise_level': expertise_level,
                        'temperature': temperature,
                        'max_tokens': max_tokens
                    }
                    
                    if editing_assistant:
                        # Update existing assistant
                        assistant_config = all_assistants.get(editing_assistant, {})
                        if assistant_config.get('id'):
                            success = assistant_profiles.update_custom_assistant(
                                assistant_config['id'], new_assistant_data
                            )
                            if success:
                                st.success(f"Updated assistant: {name}")
                                st.session_state.editing_assistant = None
                            else:
                                st.error("Failed to update assistant")
                    else:
                        # Create new assistant
                        assistant_id = assistant_profiles.create_custom_assistant(new_assistant_data)
                        if assistant_id:
                            st.success(f"Created new assistant: {name}")
                        else:
                            st.error("Failed to create assistant")
                    
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error saving assistant: {str(e)}")
    
    # Test assistant
    if st.session_state.get("testing_assistant"):
        st.subheader("🧪 Test Assistant")
        
        test_prompt = st.text_input("Test prompt:", "Hello, can you introduce yourself?")
        
        if st.button("Send Test Message"):
            # Create temporary assistant config
            temp_config = {
                'system_prompt': system_prompt,
                'temperature': temperature,
                'max_tokens': max_tokens,
                'emoji': emoji,
                'specialties': [s.strip() for s in specialties_text.split('\n') if s.strip()],
                'expertise_level': expertise_level
            }
            
            # Generate test response
            test_messages = [{"role": "user", "content": test_prompt}]
            response_data = enhanced_ai_chat_manager.generate_demo_response(test_messages, temp_config)
            
            st.markdown("**Assistant Response:**")
            st.markdown(response_data["content"])

def render_voice_page():
    """Render voice settings page"""
    st.header("🎙️ Voice Settings")
    
    if not voice_manager.voice_enabled:
        st.warning("Voice features are not enabled. Please check your OpenAI API configuration.")
        return
    
    # Voice configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔊 Text-to-Speech")
        
        # Voice selection
        available_voices = voice_manager.get_available_voices()
        selected_voice = st.selectbox("Select Voice", available_voices)
        
        # Voice speed
        voice_speed = st.slider("Speech Speed", 0.5, 2.0, config_manager.get("voice_speed", 1.0), 0.1)
        config_manager.update("voice_speed", voice_speed)
        
        # Test TTS
        test_text = st.text_area("Test Text", "Hello! This is a test of the text-to-speech feature.")
        
        if st.button("🔊 Generate Speech"):
            if test_text:
                audio_data = voice_manager.text_to_speech(test_text, selected_voice)
                if audio_data:
                    st.audio(audio_data, format='audio/mp3')
                else:
                    st.error("Failed to generate speech")
    
    with col2:
        st.subheader("🎤 Speech-to-Text")
        
        st.info("Speech-to-text functionality coming soon!")
        
        # Placeholder for future STT features
        st.write("**Planned Features:**")
        st.write("• Real-time voice input")
        st.write("• Voice commands")
        st.write("• Audio file transcription")
        st.write("• Multi-language support")

def render_files_page():
    """Render file management page"""
    st.header("📁 File Management")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload Files",
        accept_multiple_files=True,
        type=config_manager.get("supported_file_types", [])
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} files")
        
        # Display file information
        for file in uploaded_files:
            with st.expander(f"📄 {file.name}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Size:** {file.size:,} bytes")
                    st.write(f"**Type:** {file.type}")
                
                with col2:
                    if st.button(f"📖 Analyze", key=f"analyze_{file.name}"):
                        st.info("File analysis feature coming soon!")

def render_analytics_page():
    """Render analytics page"""
    st.header("📊 Analytics Dashboard")
    
    # Get analytics data
    threads = db_manager.get_threads()
    all_messages = []
    for thread in threads:
        messages = db_manager.get_messages(thread['id'])
        all_messages.extend(messages)
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Threads", len(threads))
    
    with col2:
        st.metric("Total Messages", len(all_messages))
    
    with col3:
        user_messages = [m for m in all_messages if m['role'] == 'user']
        st.metric("User Messages", len(user_messages))
    
    with col4:
        assistant_messages = [m for m in all_messages if m['role'] == 'assistant']
        st.metric("AI Responses", len(assistant_messages))
    
    # Usage over time
    if all_messages:
        st.subheader("📈 Usage Over Time")
        
        # Create daily usage chart
        message_dates = []
        for message in all_messages:
            try:
                dt = datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
                message_dates.append(dt.date())
            except:
                continue
        
        if message_dates:
            # Count messages per day
            from collections import Counter
            daily_counts = Counter(message_dates)
            
            # Create DataFrame for chart
            df = pd.DataFrame(list(daily_counts.items()), columns=['Date', 'Messages'])
            df = df.sort_values('Date')
            
            st.line_chart(df.set_index('Date'))
    
    # Assistant usage
    st.subheader("🤖 Assistant Usage")
    
    assistant_usage = {}
    for thread in threads:
        assistant_id = thread['assistant_id']
        assistant_usage[assistant_id] = assistant_usage.get(assistant_id, 0) + 1
    
    if assistant_usage:
        df_assistants = pd.DataFrame(list(assistant_usage.items()), columns=['Assistant', 'Threads'])
        st.bar_chart(df_assistants.set_index('Assistant'))

def render_settings_page():
    """Render settings page"""
    st.header("⚙️ Settings")
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    
    with st.form("api_settings"):
        api_key = st.text_input("OpenAI API Key", type="password", value=config_manager.get("openai_api_key", ""))
        model = st.selectbox("Default Model", ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"], 
                           index=0 if config_manager.get("openai_model") == "gpt-4" else 1)
        
        if st.form_submit_button("💾 Save API Settings"):
            config_manager.update("openai_api_key", api_key)
            config_manager.update("openai_model", model)
            st.success("API settings saved!")
    
    # UI Configuration
    st.subheader("🎨 UI Configuration")
    
    with st.form("ui_settings"):
        theme_color = st.color_picker("Primary Color", config_manager.get("theme_primary_color", "#dc3545"))
        
        if st.form_submit_button("💾 Save UI Settings"):
            config_manager.update("theme_primary_color", theme_color)
            st.success("UI settings saved! Refresh the page to see changes.")
    
    # Data Management
    st.subheader("🗄️ Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export Data", use_container_width=True):
            st.info("Data export feature coming soon!")
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.warning("This will delete all threads and messages. This action cannot be undone.")

# ======================================================
# 🚀 MAIN APPLICATION
# ======================================================

def main():
    """Main application function"""
    try:
        # Configure Streamlit page
        st.set_page_config(
            page_title=config_manager.get("app_name", "Enhanced AI Assistant Platform"),
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Render custom CSS
        render_custom_css()
        
        # Initialize session state
        if "current_page" not in st.session_state:
            st.session_state.current_page = "chat"
        if "current_assistant" not in st.session_state:
            st.session_state.current_assistant = "Strategic Business Consultant"
        
        # Render header
        render_header()
        
        # Render sidebar
        with st.sidebar:
            current_page = render_main_menu()
            
            if current_page == "chat":
                render_assistant_selector()
                render_thread_management()
                render_file_upload_sidebar()
                render_voice_controls()
        
        # Render main content based on current page
        if current_page == "chat":
            render_chat_page()
        elif current_page == "threads":
            render_threads_page()
        elif current_page == "assistants":
            render_assistants_page()
        elif current_page == "agent_builder":
            render_agent_builder_page()
        elif current_page == "voice":
            render_voice_page()
        elif current_page == "files":
            render_files_page()
        elif current_page == "analytics":
            render_analytics_page()
        elif current_page == "settings":
            render_settings_page()
        else:
            render_chat_page()  # Default fallback
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()

