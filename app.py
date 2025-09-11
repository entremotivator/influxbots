#!/usr/bin/env python3
"""
🚀 ULTIMATE AI ASSISTANT PLATFORM
Advanced AI platform with comprehensive voice features, optional cloud storage, and real-time capabilities
Production-ready with extensive customization and professional-grade features
"""

import streamlit as st
import os
import json
import time
import hashlib
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union, Callable
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
import sqlite3
import pickle
import wave
import audioop
import struct
import math

# Core imports
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Optional Supabase imports
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
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_CORE_AVAILABLE = True
except ImportError:
    LANGCHAIN_CORE_AVAILABLE = False

# Advanced processing libraries
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

# Enhanced audio processing
try:
    import speech_recognition as sr
    from gtts import gTTS
    import pygame
    import pyaudio
    import webrtcvad
    import librosa
    import soundfile as sf
    from pydub import AudioSegment
    from pydub.playback import play
    ADVANCED_AUDIO_AVAILABLE = True
except ImportError:
    ADVANCED_AUDIO_AVAILABLE = False

# Web scraping and API libraries
try:
    import requests
    from bs4 import BeautifulSoup
    WEB_PROCESSING_AVAILABLE = True
except ImportError:
    WEB_PROCESSING_AVAILABLE = False

# Real-time processing
try:
    import websockets
    import asyncio
    REALTIME_AVAILABLE = True
except ImportError:
    REALTIME_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🔐 ENHANCED CONFIGURATION MANAGEMENT
# ======================================================

class UltimateConfigurationManager:
    """Ultimate configuration management with flexible storage options"""
    
    def __init__(self):
        self.config = self.load_configuration()
        self.storage_mode = self.determine_storage_mode()
        self.supabase_client = None
        self.local_db_path = "ultimate_ai_assistant.db"
        self.initialize_storage()
    
    def load_configuration(self) -> Dict[str, Any]:
        """Load comprehensive configuration from multiple sources"""
        try:
            config = {
                # Storage Configuration
                "storage_mode": self._get_config_value("STORAGE_MODE", "local"),  # local, supabase, hybrid
                "supabase_url": self._get_config_value("SUPABASE_URL", ""),
                "supabase_key": self._get_config_value("SUPABASE_ANON_KEY", ""),
                "supabase_service_key": self._get_config_value("SUPABASE_SERVICE_KEY", ""),
                "auto_backup": self._get_config_value("AUTO_BACKUP", "true").lower() == "true",
                
                # OpenAI Configuration
                "openai_api_key": self._get_config_value("OPENAI_API_KEY", ""),
                "openai_model": self._get_config_value("OPENAI_MODEL", "gpt-4-turbo-preview"),
                "openai_temperature": float(self._get_config_value("OPENAI_TEMPERATURE", "0.7")),
                "openai_max_tokens": int(self._get_config_value("OPENAI_MAX_TOKENS", "4000")),
                "openai_organization": self._get_config_value("OPENAI_ORGANIZATION", ""),
                
                # Advanced Voice Configuration
                "voice_enabled": self._get_config_value("VOICE_ENABLED", "true").lower() == "true",
                "voice_model": self._get_config_value("VOICE_MODEL", "tts-1-hd"),
                "voice_type": self._get_config_value("VOICE_TYPE", "alloy"),
                "voice_speed": float(self._get_config_value("VOICE_SPEED", "1.0")),
                "voice_pitch": float(self._get_config_value("VOICE_PITCH", "1.0")),
                "whisper_model": self._get_config_value("WHISPER_MODEL", "whisper-1"),
                "voice_activity_detection": self._get_config_value("VOICE_ACTIVITY_DETECTION", "true").lower() == "true",
                "noise_suppression": self._get_config_value("NOISE_SUPPRESSION", "true").lower() == "true",
                "echo_cancellation": self._get_config_value("ECHO_CANCELLATION", "true").lower() == "true",
                "auto_gain_control": self._get_config_value("AUTO_GAIN_CONTROL", "true").lower() == "true",
                
                # Real-time Voice Features
                "realtime_voice_enabled": self._get_config_value("REALTIME_VOICE_ENABLED", "true").lower() == "true",
                "voice_interruption_enabled": self._get_config_value("VOICE_INTERRUPTION_ENABLED", "true").lower() == "true",
                "voice_commands_enabled": self._get_config_value("VOICE_COMMANDS_ENABLED", "true").lower() == "true",
                "voice_emotions_enabled": self._get_config_value("VOICE_EMOTIONS_ENABLED", "true").lower() == "true",
                "voice_cloning_enabled": self._get_config_value("VOICE_CLONING_ENABLED", "false").lower() == "true",
                "background_listening": self._get_config_value("BACKGROUND_LISTENING", "false").lower() == "true",
                
                # Voice Processing Settings
                "sample_rate": int(self._get_config_value("SAMPLE_RATE", "16000")),
                "chunk_size": int(self._get_config_value("CHUNK_SIZE", "1024")),
                "channels": int(self._get_config_value("CHANNELS", "1")),
                "voice_threshold": float(self._get_config_value("VOICE_THRESHOLD", "0.5")),
                "silence_timeout": float(self._get_config_value("SILENCE_TIMEOUT", "2.0")),
                "max_recording_time": float(self._get_config_value("MAX_RECORDING_TIME", "30.0")),
                
                # Assistant API Configuration
                "assistant_api_enabled": self._get_config_value("ASSISTANT_API_ENABLED", "true").lower() == "true",
                "assistant_model": self._get_config_value("ASSISTANT_MODEL", "gpt-4-turbo-preview"),
                "function_calling_enabled": self._get_config_value("FUNCTION_CALLING_ENABLED", "true").lower() == "true",
                "code_interpreter_enabled": self._get_config_value("CODE_INTERPRETER_ENABLED", "true").lower() == "true",
                "retrieval_enabled": self._get_config_value("RETRIEVAL_ENABLED", "true").lower() == "true",
                
                # File Processing Configuration
                "max_file_size_mb": int(self._get_config_value("MAX_FILE_SIZE_MB", "500")),
                "max_files_per_session": int(self._get_config_value("MAX_FILES_PER_SESSION", "200")),
                "supported_file_types": self._get_config_value("SUPPORTED_FILE_TYPES", "pdf,docx,txt,csv,json,xlsx,html,md,py,js,mp3,wav,mp4,mov,jpg,jpeg,png,gif,svg,pptx,zip,rar").split(","),
                "auto_transcription": self._get_config_value("AUTO_TRANSCRIPTION", "true").lower() == "true",
                "auto_translation": self._get_config_value("AUTO_TRANSLATION", "false").lower() == "true",
                
                # Vector Database Configuration
                "vector_store_enabled": self._get_config_value("VECTOR_STORE_ENABLED", "true").lower() == "true",
                "embedding_model": self._get_config_value("EMBEDDING_MODEL", "text-embedding-3-large"),
                "chunk_size": int(self._get_config_value("CHUNK_SIZE", "1000")),
                "chunk_overlap": int(self._get_config_value("CHUNK_OVERLAP", "200")),
                "similarity_threshold": float(self._get_config_value("SIMILARITY_THRESHOLD", "0.7")),
                
                # Application Configuration
                "app_name": self._get_config_value("APP_NAME", "Ultimate AI Assistant Platform"),
                "app_description": self._get_config_value("APP_DESCRIPTION", "Advanced AI platform with comprehensive voice features and intelligent assistance"),
                "app_version": self._get_config_value("APP_VERSION", "2.0.0"),
                "debug_mode": self._get_config_value("DEBUG_MODE", "false").lower() == "true",
                "environment": self._get_config_value("ENVIRONMENT", "production"),
                "max_concurrent_users": int(self._get_config_value("MAX_CONCURRENT_USERS", "100")),
                
                # UI Configuration - Enhanced Red Theme
                "theme_primary_color": "#dc2626",
                "theme_secondary_color": "#991b1b",
                "theme_accent_color": "#fef2f2",
                "theme_text_color": "#000000",
                "theme_background": "#ffebee",
                "theme_success_color": "#dc2626",
                "theme_warning_color": "#f59e0b",
                "theme_error_color": "#7f1d1d",
                
                # Real-time Features
                "websocket_enabled": self._get_config_value("WEBSOCKET_ENABLED", "true").lower() == "true",
                "streaming_enabled": self._get_config_value("STREAMING_ENABLED", "true").lower() == "true",
                "auto_save_enabled": self._get_config_value("AUTO_SAVE_ENABLED", "true").lower() == "true",
                "real_time_collaboration": self._get_config_value("REAL_TIME_COLLABORATION", "false").lower() == "true",
                
                # Analytics Configuration
                "analytics_enabled": self._get_config_value("ANALYTICS_ENABLED", "true").lower() == "true",
                "usage_tracking": self._get_config_value("USAGE_TRACKING", "true").lower() == "true",
                "performance_monitoring": self._get_config_value("PERFORMANCE_MONITORING", "true").lower() == "true",
                "error_reporting": self._get_config_value("ERROR_REPORTING", "true").lower() == "true",
                
                # Security Configuration
                "encryption_enabled": self._get_config_value("ENCRYPTION_ENABLED", "true").lower() == "true",
                "session_timeout": int(self._get_config_value("SESSION_TIMEOUT", "3600")),
                "max_login_attempts": int(self._get_config_value("MAX_LOGIN_ATTEMPTS", "5")),
                "rate_limiting": self._get_config_value("RATE_LIMITING", "true").lower() == "true",
                
                # Advanced Features
                "multi_language_support": self._get_config_value("MULTI_LANGUAGE_SUPPORT", "true").lower() == "true",
                "plugin_system_enabled": self._get_config_value("PLUGIN_SYSTEM_ENABLED", "true").lower() == "true",
                "custom_themes_enabled": self._get_config_value("CUSTOM_THEMES_ENABLED", "true").lower() == "true",
                "api_access_enabled": self._get_config_value("API_ACCESS_ENABLED", "false").lower() == "true",
            }
            
            return config
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            return self._get_default_configuration()
    
    def determine_storage_mode(self) -> str:
        """Determine the best storage mode based on available services"""
        storage_mode = self.config.get("storage_mode", "local")
        
        if storage_mode == "supabase" and not SUPABASE_AVAILABLE:
            logger.warning("Supabase requested but not available, falling back to local storage")
            return "local"
        
        if storage_mode == "supabase" and not (self.config.get("supabase_url") and self.config.get("supabase_key")):
            logger.warning("Supabase credentials not found, falling back to local storage")
            return "local"
        
        return storage_mode
    
    def initialize_storage(self):
        """Initialize storage based on determined mode"""
        try:
            if self.storage_mode == "supabase" and SUPABASE_AVAILABLE:
                supabase_url = self.config.get("supabase_url")
                supabase_key = self.config.get("supabase_key")
                
                if supabase_url and supabase_key:
                    self.supabase_client = create_client(supabase_url, supabase_key)
                    logger.info("Supabase client initialized successfully")
                else:
                    logger.warning("Supabase credentials missing, using local storage")
                    self.storage_mode = "local"
            
            # Always initialize local storage as backup
            self.initialize_local_storage()
            
        except Exception as e:
            logger.error(f"Error initializing storage: {str(e)}")
            self.storage_mode = "local"
            self.initialize_local_storage()
    
    def initialize_local_storage(self):
        """Initialize local SQLite database"""
        try:
            with sqlite3.connect(self.local_db_path) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        username TEXT UNIQUE,
                        email TEXT,
                        preferences TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Threads table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS threads (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        title TEXT NOT NULL,
                        assistant_id TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Messages table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id TEXT PRIMARY KEY,
                        thread_id TEXT NOT NULL,
                        user_id TEXT,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        voice_data BLOB,
                        FOREIGN KEY (thread_id) REFERENCES threads (id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Custom assistants table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS custom_assistants (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        name TEXT NOT NULL,
                        description TEXT,
                        system_prompt TEXT,
                        emoji TEXT,
                        category TEXT,
                        specialties TEXT,
                        expertise_level TEXT,
                        temperature REAL,
                        max_tokens INTEGER,
                        voice_settings TEXT,
                        tools TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Files table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS files (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        thread_id TEXT,
                        filename TEXT NOT NULL,
                        file_path TEXT,
                        file_size INTEGER,
                        file_type TEXT,
                        processed_content TEXT,
                        embeddings BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (thread_id) REFERENCES threads (id)
                    )
                """)
                
                # Voice recordings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS voice_recordings (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        thread_id TEXT,
                        message_id TEXT,
                        audio_data BLOB,
                        transcription TEXT,
                        duration REAL,
                        sample_rate INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (thread_id) REFERENCES threads (id),
                        FOREIGN KEY (message_id) REFERENCES messages (id)
                    )
                """)
                
                # Analytics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analytics (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        event_type TEXT NOT NULL,
                        event_data TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        session_id TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Settings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS settings (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        setting_key TEXT NOT NULL,
                        setting_value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                # Voice profiles table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS voice_profiles (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        profile_name TEXT NOT NULL,
                        voice_model TEXT,
                        voice_settings TEXT,
                        sample_audio BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                
                conn.commit()
                logger.info("Local database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing local database: {str(e)}")
    
    def _get_config_value(self, key: str, default: str) -> str:
        """Get configuration value from multiple sources"""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
            
            # Fall back to environment variables
            return os.getenv(key, default)
            
        except Exception:
            return default
    
    def _get_default_configuration(self) -> Dict[str, Any]:
        """Get comprehensive default configuration"""
        return {
            # Storage
            "storage_mode": "local",
            "supabase_url": "",
            "supabase_key": "",
            "auto_backup": True,
            
            # OpenAI
            "openai_api_key": "",
            "openai_model": "gpt-4-turbo-preview",
            "openai_temperature": 0.7,
            "openai_max_tokens": 4000,
            
            # Voice
            "voice_enabled": True,
            "voice_model": "tts-1-hd",
            "voice_type": "alloy",
            "voice_speed": 1.0,
            "voice_pitch": 1.0,
            "whisper_model": "whisper-1",
            "voice_activity_detection": True,
            "noise_suppression": True,
            "echo_cancellation": True,
            "auto_gain_control": True,
            "realtime_voice_enabled": True,
            "voice_interruption_enabled": True,
            "voice_commands_enabled": True,
            "voice_emotions_enabled": True,
            "voice_cloning_enabled": False,
            "background_listening": False,
            
            # Voice Processing
            "sample_rate": 16000,
            "chunk_size": 1024,
            "channels": 1,
            "voice_threshold": 0.5,
            "silence_timeout": 2.0,
            "max_recording_time": 30.0,
            
            # Assistant API
            "assistant_api_enabled": True,
            "assistant_model": "gpt-4-turbo-preview",
            "function_calling_enabled": True,
            "code_interpreter_enabled": True,
            "retrieval_enabled": True,
            
            # Files
            "max_file_size_mb": 500,
            "max_files_per_session": 200,
            "supported_file_types": ["pdf", "docx", "txt", "csv", "json", "xlsx", "html", "md", "py", "js", "mp3", "wav", "mp4", "mov", "jpg", "jpeg", "png", "gif", "svg", "pptx", "zip", "rar"],
            "auto_transcription": True,
            "auto_translation": False,
            
            # Vector Store
            "vector_store_enabled": True,
            "embedding_model": "text-embedding-3-large",
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "similarity_threshold": 0.7,
            
            # Application
            "app_name": "Ultimate AI Assistant Platform",
            "app_description": "Advanced AI platform with comprehensive voice features and intelligent assistance",
            "app_version": "2.0.0",
            "debug_mode": False,
            "environment": "production",
            "max_concurrent_users": 100,
            
            # Theme
            "theme_primary_color": "#dc2626",
            "theme_secondary_color": "#991b1b",
            "theme_accent_color": "#fef2f2",
            "theme_text_color": "#000000",
            "theme_background": "#ffebee",
            
            # Real-time
            "websocket_enabled": True,
            "streaming_enabled": True,
            "auto_save_enabled": True,
            "real_time_collaboration": False,
            
            # Analytics
            "analytics_enabled": True,
            "usage_tracking": True,
            "performance_monitoring": True,
            "error_reporting": True,
            
            # Security
            "encryption_enabled": True,
            "session_timeout": 3600,
            "max_login_attempts": 5,
            "rate_limiting": True,
            
            # Advanced
            "multi_language_support": True,
            "plugin_system_enabled": True,
            "custom_themes_enabled": True,
            "api_access_enabled": False
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        self.config[key] = value
    
    def get_storage_client(self):
        """Get storage client (Supabase or None for local)"""
        return self.supabase_client
    
    def is_supabase_enabled(self) -> bool:
        """Check if Supabase is enabled and available"""
        return self.storage_mode == "supabase" and self.supabase_client is not None

# Initialize configuration manager
ultimate_config = UltimateConfigurationManager()

# ======================================================
# 🎙️ ULTIMATE VOICE PROCESSING SYSTEM
# ======================================================

class UltimateVoiceProcessor:
    """Ultimate voice processing system with comprehensive features"""
    
    def __init__(self, config_manager: UltimateConfigurationManager):
        self.config = config_manager
        self.client = None
        self.recognizer = None
        self.microphone = None
        self.vad = None
        self.audio_queue = queue.Queue()
        self.voice_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.is_listening = False
        self.is_speaking = False
        self.current_recording = None
        self.voice_profiles = {}
        self.emotion_detector = None
        self.background_listener = None
        self.initialize_voice_services()
    
    def initialize_voice_services(self):
        """Initialize comprehensive voice services"""
        try:
            # Initialize OpenAI client
            api_key = self.config.get("openai_api_key")
            if api_key and OPENAI_AVAILABLE:
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI voice client initialized")
            
            # Initialize speech recognition
            if ADVANCED_AUDIO_AVAILABLE:
                self.recognizer = sr.Recognizer()
                
                # Configure recognizer settings
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8
                self.recognizer.operation_timeout = None
                self.recognizer.phrase_threshold = 0.3
                self.recognizer.non_speaking_duration = 0.8
                
                try:
                    self.microphone = sr.Microphone(
                        sample_rate=self.config.get("sample_rate", 16000),
                        chunk_size=self.config.get("chunk_size", 1024)
                    )
                    
                    # Adjust for ambient noise
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    
                    logger.info("Microphone initialized and calibrated")
                    
                except Exception as e:
                    logger.warning(f"Microphone initialization failed: {str(e)}")
                
                # Initialize Voice Activity Detection
                if self.config.get("voice_activity_detection"):
                    try:
                        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 0-3
                        logger.info("Voice Activity Detection initialized")
                    except Exception as e:
                        logger.warning(f"VAD initialization failed: {str(e)}")
                
                # Initialize pygame for audio playback
                try:
                    pygame.mixer.init(
                        frequency=self.config.get("sample_rate", 16000),
                        size=-16,
                        channels=self.config.get("channels", 1),
                        buffer=512
                    )
                    logger.info("Audio playback system initialized")
                except Exception as e:
                    logger.warning(f"Audio playback initialization failed: {str(e)}")
            
            # Load voice profiles
            self.load_voice_profiles()
            
            # Initialize background listening if enabled
            if self.config.get("background_listening"):
                self.start_background_listening()
            
            logger.info("Ultimate voice services initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing voice services: {str(e)}")
    
    def text_to_speech(self, text: str, voice: str = None, model: str = None, 
                      speed: float = None, emotion: str = None) -> Optional[bytes]:
        """Advanced text-to-speech with emotion and customization"""
        try:
            if not self.client:
                return self.fallback_tts(text, voice)
            
            # Use provided parameters or defaults
            voice = voice or self.config.get("voice_type", "alloy")
            model = model or self.config.get("voice_model", "tts-1-hd")
            speed = speed or self.config.get("voice_speed", 1.0)
            
            # Apply emotion if supported
            if emotion and self.config.get("voice_emotions_enabled"):
                text = self.apply_emotion_to_text(text, emotion)
            
            # Generate speech
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=speed
            )
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return self.fallback_tts(text, voice)
    
    def fallback_tts(self, text: str, voice: str = None) -> Optional[bytes]:
        """Fallback TTS using gTTS"""
        try:
            if not ADVANCED_AUDIO_AVAILABLE:
                return None
            
            # Use gTTS as fallback
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                tts.save(temp_file.name)
                
                # Read the file content
                with open(temp_file.name, "rb") as f:
                    audio_data = f.read()
                
                # Clean up
                os.unlink(temp_file.name)
                
                return audio_data
                
        except Exception as e:
            logger.error(f"Error in fallback TTS: {str(e)}")
            return None
    
    def speech_to_text(self, audio_data, model: str = None, language: str = "en") -> Optional[str]:
        """Advanced speech-to-text with language detection"""
        try:
            if not self.client:
                return self.fallback_stt(audio_data)
            
            model = model or self.config.get("whisper_model", "whisper-1")
            
            # Prepare audio file
            if isinstance(audio_data, bytes):
                audio_file = io.BytesIO(audio_data)
                audio_file.name = "speech.wav"
            else:
                audio_file = audio_data
            
            # Transcribe with advanced options
            transcript = self.client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="verbose_json",
                language=language if language != "auto" else None,
                temperature=0.0
            )
            
            # Extract text and metadata
            if hasattr(transcript, 'text'):
                return transcript.text
            else:
                return transcript.get('text', '')
            
        except Exception as e:
            logger.error(f"Error in speech-to-text: {str(e)}")
            return self.fallback_stt(audio_data)
    
    def fallback_stt(self, audio_data) -> Optional[str]:
        """Fallback STT using speech_recognition"""
        try:
            if not self.recognizer:
                return None
            
            # Convert audio data to AudioData object
            if isinstance(audio_data, bytes):
                # Assume WAV format
                audio = sr.AudioData(audio_data, self.config.get("sample_rate", 16000), 2)
            else:
                audio = audio_data
            
            # Try multiple recognition services
            try:
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                try:
                    return self.recognizer.recognize_sphinx(audio)
                except:
                    return "Could not understand audio"
            except sr.RequestError as e:
                return f"Speech recognition error: {str(e)}"
                
        except Exception as e:
            logger.error(f"Error in fallback STT: {str(e)}")
            return None
    
    def start_real_time_listening(self, callback: Callable = None) -> bool:
        """Start advanced real-time voice listening"""
        try:
            if not self.recognizer or not self.microphone:
                return False
            
            self.is_listening = True
            
            def listen_continuously():
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                
                while self.is_listening:
                    try:
                        # Listen for audio with VAD
                        with self.microphone as source:
                            if self.config.get("voice_activity_detection") and self.vad:
                                audio = self.listen_with_vad(source)
                            else:
                                audio = self.recognizer.listen(
                                    source, 
                                    timeout=1, 
                                    phrase_time_limit=self.config.get("max_recording_time", 30.0)
                                )
                        
                        if audio:
                            # Process audio in background
                            threading.Thread(
                                target=self.process_audio_async,
                                args=(audio, callback),
                                daemon=True
                            ).start()
                        
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Error in continuous listening: {str(e)}")
                        break
            
            # Start listening in background thread
            listening_thread = threading.Thread(target=listen_continuously, daemon=True)
            listening_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Error starting real-time listening: {str(e)}")
            return False
    
    def listen_with_vad(self, source) -> Optional[sr.AudioData]:
        """Listen with Voice Activity Detection"""
        try:
            frames = []
            is_speech = False
            silence_count = 0
            max_silence = int(self.config.get("silence_timeout", 2.0) * 10)  # 100ms chunks
            
            while True:
                # Read audio chunk
                chunk = source.stream.read(source.CHUNK)
                frames.append(chunk)
                
                # Check for voice activity
                if self.vad and len(chunk) == source.CHUNK * 2:  # 16-bit audio
                    is_voice = self.vad.is_speech(chunk, source.SAMPLE_RATE)
                    
                    if is_voice:
                        is_speech = True
                        silence_count = 0
                    elif is_speech:
                        silence_count += 1
                        
                        if silence_count > max_silence:
                            break
                
                # Prevent infinite recording
                if len(frames) > source.SAMPLE_RATE * self.config.get("max_recording_time", 30.0) / source.CHUNK:
                    break
            
            if frames and is_speech:
                audio_data = b''.join(frames)
                return sr.AudioData(audio_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
            
            return None
            
        except Exception as e:
            logger.error(f"Error in VAD listening: {str(e)}")
            return None
    
    def process_audio_async(self, audio: sr.AudioData, callback: Callable = None):
        """Process audio asynchronously"""
        try:
            # Convert to text
            text = self.speech_to_text(audio.get_wav_data())
            
            if text and text.strip():
                # Check for voice commands
                if self.config.get("voice_commands_enabled"):
                    command = self.detect_voice_command(text)
                    if command:
                        self.command_queue.put(command)
                        return
                
                # Add to voice queue
                self.voice_queue.put({
                    'text': text,
                    'timestamp': datetime.now(),
                    'audio_data': audio.get_wav_data(),
                    'confidence': 1.0  # Placeholder
                })
                
                # Execute callback if provided
                if callback:
                    callback(text)
            
        except Exception as e:
            logger.error(f"Error processing audio async: {str(e)}")
    
    def detect_voice_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Detect and parse voice commands"""
        try:
            text_lower = text.lower().strip()
            
            # Define voice commands
            commands = {
                'new_chat': ['new chat', 'start new conversation', 'new thread'],
                'stop_listening': ['stop listening', 'stop recording', 'mute'],
                'start_listening': ['start listening', 'start recording', 'unmute'],
                'switch_assistant': ['switch assistant', 'change assistant'],
                'save_conversation': ['save conversation', 'save chat'],
                'clear_chat': ['clear chat', 'clear conversation', 'delete chat'],
                'read_last_message': ['read last message', 'repeat last message'],
                'help': ['help', 'what can you do', 'commands'],
                'settings': ['open settings', 'show settings'],
                'volume_up': ['volume up', 'louder'],
                'volume_down': ['volume down', 'quieter'],
                'pause': ['pause', 'stop talking'],
                'resume': ['resume', 'continue'],
            }
            
            for command, phrases in commands.items():
                for phrase in phrases:
                    if phrase in text_lower:
                        return {
                            'command': command,
                            'original_text': text,
                            'confidence': 1.0,
                            'timestamp': datetime.now()
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"Error detecting voice command: {str(e)}")
            return None
    
    def apply_emotion_to_text(self, text: str, emotion: str) -> str:
        """Apply emotional context to text for better TTS"""
        try:
            emotion_prefixes = {
                'happy': "In a cheerful and upbeat tone: ",
                'sad': "In a somber and melancholic tone: ",
                'excited': "With great enthusiasm and energy: ",
                'calm': "In a peaceful and relaxed manner: ",
                'serious': "With gravity and importance: ",
                'friendly': "In a warm and welcoming way: ",
                'professional': "In a business-like and formal tone: ",
                'empathetic': "With understanding and compassion: "
            }
            
            prefix = emotion_prefixes.get(emotion.lower(), "")
            return prefix + text
            
        except Exception as e:
            logger.error(f"Error applying emotion to text: {str(e)}")
            return text
    
    def create_voice_profile(self, profile_name: str, sample_audio: bytes, 
                           voice_settings: Dict[str, Any]) -> bool:
        """Create custom voice profile (placeholder for voice cloning)"""
        try:
            if not self.config.get("voice_cloning_enabled"):
                return False
            
            # Store voice profile
            self.voice_profiles[profile_name] = {
                'sample_audio': sample_audio,
                'settings': voice_settings,
                'created_at': datetime.now(),
                'usage_count': 0
            }
            
            # Save to database
            self.save_voice_profile_to_db(profile_name, sample_audio, voice_settings)
            
            logger.info(f"Voice profile '{profile_name}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating voice profile: {str(e)}")
            return False
    
    def save_voice_profile_to_db(self, profile_name: str, sample_audio: bytes, 
                                voice_settings: Dict[str, Any]):
        """Save voice profile to database"""
        try:
            user_id = st.session_state.get("user_id", "default_user")
            
            with sqlite3.connect(self.config.local_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO voice_profiles 
                    (id, user_id, profile_name, voice_settings, sample_audio)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()),
                    user_id,
                    profile_name,
                    json.dumps(voice_settings),
                    sample_audio
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error saving voice profile to database: {str(e)}")
    
    def load_voice_profiles(self):
        """Load voice profiles from database"""
        try:
            user_id = st.session_state.get("user_id", "default_user")
            
            with sqlite3.connect(self.config.local_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT profile_name, voice_settings, sample_audio 
                    FROM voice_profiles WHERE user_id = ?
                """, (user_id,))
                
                for row in cursor.fetchall():
                    profile_name, settings_json, sample_audio = row
                    self.voice_profiles[profile_name] = {
                        'sample_audio': sample_audio,
                        'settings': json.loads(settings_json) if settings_json else {},
                        'usage_count': 0
                    }
                
                logger.info(f"Loaded {len(self.voice_profiles)} voice profiles")
                
        except Exception as e:
            logger.error(f"Error loading voice profiles: {str(e)}")
    
    def start_background_listening(self):
        """Start background listening for wake words"""
        try:
            if not self.config.get("background_listening"):
                return
            
            def background_listen():
                wake_words = ['hey assistant', 'hello ai', 'wake up']
                
                while self.config.get("background_listening"):
                    try:
                        with self.microphone as source:
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                        
                        text = self.speech_to_text(audio.get_wav_data())
                        
                        if text and any(wake_word in text.lower() for wake_word in wake_words):
                            # Wake word detected, start active listening
                            self.voice_queue.put({
                                'text': 'WAKE_WORD_DETECTED',
                                'timestamp': datetime.now(),
                                'wake_word': True
                            })
                        
                        time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                        
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        logger.error(f"Error in background listening: {str(e)}")
                        time.sleep(1)
            
            self.background_listener = threading.Thread(target=background_listen, daemon=True)
            self.background_listener.start()
            
            logger.info("Background listening started")
            
        except Exception as e:
            logger.error(f"Error starting background listening: {str(e)}")
    
    def stop_real_time_listening(self):
        """Stop real-time voice listening"""
        self.is_listening = False
    
    def get_voice_input(self) -> Optional[Dict[str, Any]]:
        """Get voice input from queue"""
        try:
            return self.voice_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_voice_command(self) -> Optional[Dict[str, Any]]:
        """Get voice command from queue"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
    
    def play_audio(self, audio_data: bytes, format: str = "mp3"):
        """Play audio with advanced controls"""
        try:
            if not ADVANCED_AUDIO_AVAILABLE:
                return False
            
            self.is_speaking = True
            
            # Convert audio if needed
            if format == "mp3":
                audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_data))
            elif format == "wav":
                audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            else:
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
            
            # Apply audio processing
            if self.config.get("noise_suppression"):
                audio_segment = self.apply_noise_suppression(audio_segment)
            
            if self.config.get("auto_gain_control"):
                audio_segment = self.apply_auto_gain_control(audio_segment)
            
            # Play audio
            play(audio_segment)
            
            self.is_speaking = False
            return True
            
        except Exception as e:
            logger.error(f"Error playing audio: {str(e)}")
            self.is_speaking = False
            return False
    
    def apply_noise_suppression(self, audio_segment: AudioSegment) -> AudioSegment:
        """Apply noise suppression to audio"""
        try:
            # Simple noise gate implementation
            threshold = -30  # dB
            return audio_segment.apply_gain_stereo(threshold, threshold)
        except Exception as e:
            logger.error(f"Error applying noise suppression: {str(e)}")
            return audio_segment
    
    def apply_auto_gain_control(self, audio_segment: AudioSegment) -> AudioSegment:
        """Apply automatic gain control"""
        try:
            # Normalize audio to target level
            target_dBFS = -20.0
            change_in_dBFS = target_dBFS - audio_segment.dBFS
            return audio_segment.apply_gain(change_in_dBFS)
        except Exception as e:
            logger.error(f"Error applying auto gain control: {str(e)}")
            return audio_segment
    
    def get_available_voices(self) -> List[str]:
        """Get list of available TTS voices"""
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        
        # Add custom voice profiles
        voices.extend(list(self.voice_profiles.keys()))
        
        return voices
    
    def get_voice_models(self) -> List[str]:
        """Get list of available voice models"""
        return ["tts-1", "tts-1-hd"]
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages for STT"""
        return [
            "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh", 
            "ar", "hi", "tr", "pl", "nl", "sv", "da", "no", "fi"
        ]
    
    def analyze_audio_quality(self, audio_data: bytes) -> Dict[str, Any]:
        """Analyze audio quality metrics"""
        try:
            if not ADVANCED_AUDIO_AVAILABLE:
                return {}
            
            # Load audio data
            audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))
            
            # Calculate metrics
            duration = len(audio_segment) / 1000.0  # seconds
            sample_rate = audio_segment.frame_rate
            channels = audio_segment.channels
            bit_depth = audio_segment.sample_width * 8
            
            # Audio level analysis
            rms = audio_segment.rms
            max_amplitude = audio_segment.max
            
            # Signal-to-noise ratio (simplified)
            snr = 20 * math.log10(rms / (max_amplitude * 0.01)) if rms > 0 else 0
            
            return {
                'duration': duration,
                'sample_rate': sample_rate,
                'channels': channels,
                'bit_depth': bit_depth,
                'rms_level': rms,
                'max_amplitude': max_amplitude,
                'snr_estimate': snr,
                'quality_score': min(100, max(0, (snr + 20) * 2))  # 0-100 scale
            }
            
        except Exception as e:
            logger.error(f"Error analyzing audio quality: {str(e)}")
            return {}
    
    def cleanup(self):
        """Cleanup voice processing resources"""
        try:
            self.stop_real_time_listening()
            
            if hasattr(pygame.mixer, 'quit'):
                pygame.mixer.quit()
            
            logger.info("Voice processor cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during voice processor cleanup: {str(e)}")

# Initialize ultimate voice processor
ultimate_voice = UltimateVoiceProcessor(ultimate_config)

# ======================================================
# 🗄️ FLEXIBLE STORAGE MANAGER
# ======================================================

class FlexibleStorageManager:
    """Flexible storage manager supporting both local and cloud storage"""
    
    def __init__(self, config_manager: UltimateConfigurationManager):
        self.config = config_manager
        self.supabase_client = config_manager.get_storage_client()
        self.local_db_path = config_manager.local_db_path
        self.storage_mode = config_manager.storage_mode
    
    # User Management
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create a new user"""
        try:
            user_id = str(uuid.uuid4())
            user_data['id'] = user_id
            user_data['created_at'] = datetime.now().isoformat()
            user_data['updated_at'] = datetime.now().isoformat()
            
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('users').insert(user_data).execute()
                if result.data:
                    return result.data[0]['id']
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO users (id, username, email, preferences, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        user_id,
                        user_data.get('username'),
                        user_data.get('email'),
                        json.dumps(user_data.get('preferences', {})),
                        user_data['created_at'],
                        user_data['updated_at']
                    ))
                    conn.commit()
                    return user_id
            
            return None
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('users').select("*").eq('id', user_id).execute()
                if result.data:
                    return result.data[0]
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                    row = cursor.fetchone()
                    if row:
                        columns = [desc[0] for desc in cursor.description]
                        user_data = dict(zip(columns, row))
                        if user_data.get('preferences'):
                            user_data['preferences'] = json.loads(user_data['preferences'])
                        return user_data
            
            return None
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    # Thread Management
    def create_thread(self, thread_data: Dict[str, Any]) -> Optional[str]:
        """Create a new thread"""
        try:
            thread_id = str(uuid.uuid4())
            thread_data['id'] = thread_id
            thread_data['created_at'] = datetime.now().isoformat()
            thread_data['updated_at'] = datetime.now().isoformat()
            
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('threads').insert(thread_data).execute()
                if result.data:
                    return result.data[0]['id']
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO threads (id, user_id, title, assistant_id, created_at, updated_at, metadata)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        thread_id,
                        thread_data.get('user_id'),
                        thread_data.get('title'),
                        thread_data.get('assistant_id'),
                        thread_data['created_at'],
                        thread_data['updated_at'],
                        json.dumps(thread_data.get('metadata', {}))
                    ))
                    conn.commit()
                    return thread_id
            
            return None
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}")
            return None
    
    def get_threads(self, user_id: str = None, assistant_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get threads with optional filtering"""
        try:
            if self.storage_mode == "supabase" and self.supabase_client:
                query = self.supabase_client.table('threads').select("*")
                
                if user_id:
                    query = query.eq('user_id', user_id)
                if assistant_id:
                    query = query.eq('assistant_id', assistant_id)
                
                result = query.order('updated_at', desc=True).limit(limit).execute()
                return result.data if result.data else []
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    
                    query = "SELECT * FROM threads WHERE 1=1"
                    params = []
                    
                    if user_id:
                        query += " AND user_id = ?"
                        params.append(user_id)
                    if assistant_id:
                        query += " AND assistant_id = ?"
                        params.append(assistant_id)
                    
                    query += " ORDER BY updated_at DESC LIMIT ?"
                    params.append(limit)
                    
                    cursor.execute(query, params)
                    columns = [desc[0] for desc in cursor.description]
                    
                    threads = []
                    for row in cursor.fetchall():
                        thread_data = dict(zip(columns, row))
                        if thread_data.get('metadata'):
                            thread_data['metadata'] = json.loads(thread_data['metadata'])
                        threads.append(thread_data)
                    
                    return threads
            
        except Exception as e:
            logger.error(f"Error getting threads: {str(e)}")
            return []
    
    def update_thread(self, thread_id: str, updates: Dict[str, Any]) -> bool:
        """Update thread"""
        try:
            updates['updated_at'] = datetime.now().isoformat()
            
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('threads').update(updates).eq('id', thread_id).execute()
                return bool(result.data)
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Build dynamic update query
                    set_clauses = []
                    params = []
                    
                    for key, value in updates.items():
                        if key == 'metadata':
                            value = json.dumps(value)
                        set_clauses.append(f"{key} = ?")
                        params.append(value)
                    
                    params.append(thread_id)
                    
                    query = f"UPDATE threads SET {', '.join(set_clauses)} WHERE id = ?"
                    cursor.execute(query, params)
                    conn.commit()
                    
                    return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Error updating thread: {str(e)}")
            return False
    
    def delete_thread(self, thread_id: str) -> bool:
        """Delete thread and associated messages"""
        try:
            if self.storage_mode == "supabase" and self.supabase_client:
                # Delete messages first
                self.supabase_client.table('messages').delete().eq('thread_id', thread_id).execute()
                # Delete thread
                result = self.supabase_client.table('threads').delete().eq('id', thread_id).execute()
                return bool(result.data)
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    # Delete messages first
                    cursor.execute("DELETE FROM messages WHERE thread_id = ?", (thread_id,))
                    # Delete voice recordings
                    cursor.execute("DELETE FROM voice_recordings WHERE thread_id = ?", (thread_id,))
                    # Delete thread
                    cursor.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
                    conn.commit()
                    return cursor.rowcount > 0
            
        except Exception as e:
            logger.error(f"Error deleting thread: {str(e)}")
            return False
    
    # Message Management
    def add_message(self, message_data: Dict[str, Any]) -> Optional[str]:
        """Add message to thread"""
        try:
            message_id = str(uuid.uuid4())
            message_data['id'] = message_id
            message_data['timestamp'] = datetime.now().isoformat()
            
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('messages').insert(message_data).execute()
                if result.data:
                    # Update thread timestamp
                    self.update_thread(message_data['thread_id'], {})
                    return result.data[0]['id']
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO messages (id, thread_id, user_id, role, content, timestamp, metadata, voice_data)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        message_id,
                        message_data.get('thread_id'),
                        message_data.get('user_id'),
                        message_data.get('role'),
                        message_data.get('content'),
                        message_data['timestamp'],
                        json.dumps(message_data.get('metadata', {})),
                        message_data.get('voice_data')
                    ))
                    conn.commit()
                    
                    # Update thread timestamp
                    self.update_thread(message_data['thread_id'], {})
                    
                    return message_id
            
            return None
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            return None
    
    def get_messages(self, thread_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get messages for thread"""
        try:
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('messages').select("*").eq('thread_id', thread_id).order('timestamp', desc=False).limit(limit).execute()
                return result.data if result.data else []
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT * FROM messages WHERE thread_id = ? 
                        ORDER BY timestamp ASC LIMIT ?
                    """, (thread_id, limit))
                    
                    columns = [desc[0] for desc in cursor.description]
                    messages = []
                    
                    for row in cursor.fetchall():
                        message_data = dict(zip(columns, row))
                        if message_data.get('metadata'):
                            message_data['metadata'] = json.loads(message_data['metadata'])
                        messages.append(message_data)
                    
                    return messages
            
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            return []
    
    # Voice Recording Management
    def save_voice_recording(self, recording_data: Dict[str, Any]) -> Optional[str]:
        """Save voice recording"""
        try:
            recording_id = str(uuid.uuid4())
            recording_data['id'] = recording_id
            recording_data['created_at'] = datetime.now().isoformat()
            
            # Local storage (voice recordings are typically stored locally)
            with sqlite3.connect(self.local_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO voice_recordings 
                    (id, user_id, thread_id, message_id, audio_data, transcription, duration, sample_rate, created_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    recording_id,
                    recording_data.get('user_id'),
                    recording_data.get('thread_id'),
                    recording_data.get('message_id'),
                    recording_data.get('audio_data'),
                    recording_data.get('transcription'),
                    recording_data.get('duration'),
                    recording_data.get('sample_rate'),
                    recording_data['created_at'],
                    json.dumps(recording_data.get('metadata', {}))
                ))
                conn.commit()
                return recording_id
            
        except Exception as e:
            logger.error(f"Error saving voice recording: {str(e)}")
            return None
    
    def get_voice_recordings(self, thread_id: str = None, user_id: str = None) -> List[Dict[str, Any]]:
        """Get voice recordings"""
        try:
            with sqlite3.connect(self.local_db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM voice_recordings WHERE 1=1"
                params = []
                
                if thread_id:
                    query += " AND thread_id = ?"
                    params.append(thread_id)
                if user_id:
                    query += " AND user_id = ?"
                    params.append(user_id)
                
                query += " ORDER BY created_at DESC"
                
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                
                recordings = []
                for row in cursor.fetchall():
                    recording_data = dict(zip(columns, row))
                    if recording_data.get('metadata'):
                        recording_data['metadata'] = json.loads(recording_data['metadata'])
                    recordings.append(recording_data)
                
                return recordings
            
        except Exception as e:
            logger.error(f"Error getting voice recordings: {str(e)}")
            return []
    
    # Analytics
    def log_analytics_event(self, event_data: Dict[str, Any]) -> bool:
        """Log analytics event"""
        try:
            if not self.config.get("analytics_enabled"):
                return False
            
            event_id = str(uuid.uuid4())
            event_data['id'] = event_id
            event_data['timestamp'] = datetime.now().isoformat()
            
            if self.storage_mode == "supabase" and self.supabase_client:
                result = self.supabase_client.table('analytics').insert(event_data).execute()
                return bool(result.data)
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO analytics (id, user_id, event_type, event_data, timestamp, session_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        event_id,
                        event_data.get('user_id'),
                        event_data.get('event_type'),
                        json.dumps(event_data.get('event_data', {})),
                        event_data['timestamp'],
                        event_data.get('session_id')
                    ))
                    conn.commit()
                    return True
            
        except Exception as e:
            logger.error(f"Error logging analytics event: {str(e)}")
            return False
    
    def get_analytics_data(self, user_id: str = None, event_type: str = None, 
                          start_date: str = None, end_date: str = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get analytics data"""
        try:
            if self.storage_mode == "supabase" and self.supabase_client:
                query = self.supabase_client.table('analytics').select("*")
                
                if user_id:
                    query = query.eq('user_id', user_id)
                if event_type:
                    query = query.eq('event_type', event_type)
                if start_date:
                    query = query.gte('timestamp', start_date)
                if end_date:
                    query = query.lte('timestamp', end_date)
                
                result = query.order('timestamp', desc=True).limit(limit).execute()
                return result.data if result.data else []
            else:
                # Local storage
                with sqlite3.connect(self.local_db_path) as conn:
                    cursor = conn.cursor()
                    
                    query = "SELECT * FROM analytics WHERE 1=1"
                    params = []
                    
                    if user_id:
                        query += " AND user_id = ?"
                        params.append(user_id)
                    if event_type:
                        query += " AND event_type = ?"
                        params.append(event_type)
                    if start_date:
                        query += " AND timestamp >= ?"
                        params.append(start_date)
                    if end_date:
                        query += " AND timestamp <= ?"
                        params.append(end_date)
                    
                    query += " ORDER BY timestamp DESC LIMIT ?"
                    params.append(limit)
                    
                    cursor.execute(query, params)
                    columns = [desc[0] for desc in cursor.description]
                    
                    events = []
                    for row in cursor.fetchall():
                        event_data = dict(zip(columns, row))
                        if event_data.get('event_data'):
                            event_data['event_data'] = json.loads(event_data['event_data'])
                        events.append(event_data)
                    
                    return events
            
        except Exception as e:
            logger.error(f"Error getting analytics data: {str(e)}")
            return []
    
    # Backup and Sync
    def backup_to_cloud(self) -> bool:
        """Backup local data to cloud storage"""
        try:
            if not self.config.get("auto_backup") or not self.supabase_client:
                return False
            
            # This would implement a full backup strategy
            # For now, just log the attempt
            logger.info("Cloud backup initiated")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up to cloud: {str(e)}")
            return False
    
    def sync_from_cloud(self) -> bool:
        """Sync data from cloud storage"""
        try:
            if not self.supabase_client:
                return False
            
            # This would implement a full sync strategy
            # For now, just log the attempt
            logger.info("Cloud sync initiated")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing from cloud: {str(e)}")
            return False

# Initialize flexible storage manager
flexible_storage = FlexibleStorageManager(ultimate_config)

# ======================================================
# 🎨 ULTIMATE UI COMPONENTS WITH ENHANCED RED THEME
# ======================================================

def render_ultimate_css():
    """Render ultimate custom CSS with enhanced red theme"""
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Root Variables */
    :root {{
        --primary-red: {ultimate_config.get('theme_primary_color')};
        --secondary-red: {ultimate_config.get('theme_secondary_color')};
        --accent-red: {ultimate_config.get('theme_accent_color')};
        --text-black: {ultimate_config.get('theme_text_color')};
        --background-light: {ultimate_config.get('theme_background')};
        --success-red: {ultimate_config.get('theme_success_color')};
        --warning-orange: {ultimate_config.get('theme_warning_color')};
        --error-dark-red: {ultimate_config.get('theme_error_color')};
        --shadow-red: rgba(220, 38, 38, 0.15);
        --shadow-red-hover: rgba(220, 38, 38, 0.25);
        --gradient-red: linear-gradient(135deg, var(--primary-red) 0%, var(--secondary-red) 100%);
        --gradient-bg: linear-gradient(135deg, var(--background-light) 0%, #ffcdd2 100%);
    }}
    
    /* Main App Styling */
    .stApp {{
        background: var(--gradient-bg);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-black);
    }}
    
    /* Enhanced Button Styling */
    .stButton > button {{
        background: var(--gradient-red);
        color: var(--text-black);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px var(--shadow-red);
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--shadow-red-hover);
        background: linear-gradient(135deg, var(--secondary-red) 0%, #7f1d1d 100%);
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:active {{
        transform: translateY(0px);
        box-shadow: 0 4px 12px var(--shadow-red);
    }}
    
    /* Voice Control Buttons */
    .voice-button {{
        background: var(--gradient-red);
        color: var(--text-black);
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px var(--shadow-red);
        margin: 0.5rem;
    }}
    
    .voice-button:hover {{
        transform: scale(1.1);
        box-shadow: 0 6px 20px var(--shadow-red-hover);
    }}
    
    .voice-button.recording {{
        animation: pulse 1.5s infinite;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.7); }}
        70% {{ box-shadow: 0 0 0 10px rgba(220, 38, 38, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }}
    }}
    
    /* Enhanced Input Styling */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {{
        background: var(--primary-red);
        border-radius: 12px;
        color: var(--text-black);
        border: 2px solid var(--secondary-red);
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 8px var(--shadow-red);
        transition: all 0.3s ease;
    }}
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: var(--secondary-red);
        box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1), 0 4px 12px var(--shadow-red);
        outline: none;
    }}
    
    /* Enhanced File Uploader */
    .stFileUploader > div {{
        border-radius: 16px;
        border: 3px dashed var(--primary-red);
        background: var(--accent-red);
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .stFileUploader > div::before {{
        content: '📁';
        font-size: 3rem;
        display: block;
        margin-bottom: 1rem;
        opacity: 0.7;
    }}
    
    .stFileUploader > div:hover {{
        border-color: var(--secondary-red);
        background: #fecaca;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--shadow-red);
    }}
    
    /* Enhanced Metrics */
    .stMetric {{
        background: var(--primary-red);
        color: var(--text-black);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        box-shadow: 0 6px 20px var(--shadow-red);
        border: 2px solid var(--secondary-red);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .stMetric::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-red);
    }}
    
    .stMetric:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 30px var(--shadow-red-hover);
    }}
    
    .stMetric > div {{
        color: var(--text-black) !important;
        font-weight: 600;
    }}
    
    .stMetric [data-testid="metric-value"] {{
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: var(--text-black) !important;
    }}
    
    .stMetric [data-testid="metric-label"] {{
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--text-black) !important;
        opacity: 0.8;
    }}
    
    /* Enhanced Expander */
    .stExpander {{
        background: var(--primary-red);
        color: var(--text-black);
        border-radius: 12px;
        border: 2px solid var(--secondary-red);
        box-shadow: 0 4px 12px var(--shadow-red);
        margin: 1rem 0;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    
    .stExpander:hover {{
        box-shadow: 0 6px 20px var(--shadow-red-hover);
    }}
    
    .stExpander > div > div > div {{
        color: var(--text-black) !important;
        font-weight: 500;
    }}
    
    .stExpander [data-testid="stExpanderToggleIcon"] {{
        color: var(--text-black) !important;
    }}
    
    /* Ultimate Chat Messages */
    .stChatMessage {{
        background: var(--primary-red) !important;
        color: var(--text-black) !important;
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 6px 20px var(--shadow-red);
        border: 2px solid var(--secondary-red);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    
    .stChatMessage::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-red);
    }}
    
    .stChatMessage:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 30px var(--shadow-red-hover);
    }}
    
    .stChatMessage p,
    .stChatMessage h1, .stChatMessage h2, .stChatMessage h3,
    .stChatMessage h4, .stChatMessage h5, .stChatMessage h6,
    .stChatMessage ul, .stChatMessage ol, .stChatMessage li,
    .stChatMessage strong, .stChatMessage em, .stChatMessage span {{
        color: var(--text-black) !important;
        font-family: 'Inter', sans-serif;
    }}
    
    .stChatMessage p {{
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }}
    
    .stChatMessage code {{
        background: rgba(0, 0, 0, 0.1);
        color: var(--text-black) !important;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.9rem;
    }}
    
    .stChatMessage pre {{
        background: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        padding: 1rem;
        overflow-x: auto;
    }}
    
    /* Voice Visualization */
    .voice-visualizer {{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 60px;
        margin: 1rem 0;
    }}
    
    .voice-bar {{
        width: 4px;
        background: var(--gradient-red);
        margin: 0 2px;
        border-radius: 2px;
        animation: voice-wave 1.5s ease-in-out infinite;
    }}
    
    .voice-bar:nth-child(2) {{ animation-delay: 0.1s; }}
    .voice-bar:nth-child(3) {{ animation-delay: 0.2s; }}
    .voice-bar:nth-child(4) {{ animation-delay: 0.3s; }}
    .voice-bar:nth-child(5) {{ animation-delay: 0.4s; }}
    
    @keyframes voice-wave {{
        0%, 100% {{ height: 10px; }}
        50% {{ height: 40px; }}
    }}
    
    /* Enhanced Sidebar */
    .stSidebar {{
        background: var(--gradient-bg);
        border-right: 3px solid var(--primary-red);
    }}
    
    .stSidebar .stSelectbox > div > div,
    .stSidebar .stTextInput > div > div > input {{
        background: var(--primary-red);
        color: var(--text-black);
    }}
    
    .stSidebar .stButton > button {{
        width: 100%;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }}
    
    /* Custom Cards */
    .thread-card {{
        background: var(--primary-red);
        color: var(--text-black);
        border: 2px solid var(--secondary-red);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px var(--shadow-red);
        position: relative;
        overflow: hidden;
    }}
    
    .thread-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-red);
    }}
    
    .thread-card:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 30px var(--shadow-red-hover);
        border-color: var(--secondary-red);
    }}
    
    .assistant-card {{
        background: var(--gradient-red);
        padding: 2.5rem;
        border-radius: 20px;
        color: var(--text-black);
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px var(--shadow-red-hover);
        border: 2px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    
    .assistant-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .assistant-card:hover::before {{
        opacity: 1;
    }}
    
    .assistant-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 35px var(--shadow-red-hover);
    }}
    
    .assistant-card h3 {{
        color: var(--text-black) !important;
        margin: 0 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 800;
        font-family: 'Inter', sans-serif;
    }}
    
    .assistant-card p {{
        color: var(--text-black) !important;
        opacity: 0.9;
        margin: 0.75rem 0;
        line-height: 1.6;
        font-size: 1rem;
    }}
    
    .menu-item {{
        background: var(--primary-red);
        color: var(--text-black);
        border: 2px solid var(--secondary-red);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 12px var(--shadow-red);
        position: relative;
        overflow: hidden;
    }}
    
    .menu-item::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }}
    
    .menu-item:hover {{
        background: var(--secondary-red);
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 20px var(--shadow-red-hover);
    }}
    
    .menu-item:hover::before {{
        left: 100%;
    }}
    
    /* Status Indicators */
    .status-indicator {{
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.9rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }}
    
    .status-success {{
        background: var(--success-red);
        color: white;
        box-shadow: 0 4px 12px var(--shadow-red);
    }}
    
    .status-warning {{
        background: var(--warning-orange);
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
    }}
    
    .status-error {{
        background: var(--error-dark-red);
        color: white;
        box-shadow: 0 4px 12px rgba(127, 29, 29, 0.2);
    }}
    
    .status-indicator:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }}
    
    /* Loading Animations */
    .loading-spinner {{
        border: 4px solid var(--accent-red);
        border-top: 4px solid var(--primary-red);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .loading-dots {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }}
    
    .loading-dot {{
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--primary-red);
        margin: 0 4px;
        animation: loading-bounce 1.4s ease-in-out infinite both;
    }}
    
    .loading-dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .loading-dot:nth-child(2) {{ animation-delay: -0.16s; }}
    
    @keyframes loading-bounce {{
        0%, 80%, 100% {{ transform: scale(0); }}
        40% {{ transform: scale(1); }}
    }}
    
    /* Progress Bars */
    .progress-bar {{
        width: 100%;
        height: 8px;
        background: var(--accent-red);
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }}
    
    .progress-fill {{
        height: 100%;
        background: var(--gradient-red);
        border-radius: 4px;
        transition: width 0.3s ease;
    }}
    
    /* Enhanced Scrollbar */
    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: var(--accent-red);
        border-radius: 6px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--gradient-red);
        border-radius: 6px;
        border: 2px solid var(--accent-red);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, var(--secondary-red) 0%, #7f1d1d 100%);
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .stChatMessage {{
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 16px;
        }}
        
        .assistant-card {{
            padding: 2rem;
            border-radius: 16px;
        }}
        
        .thread-card {{
            padding: 1.5rem;
            border-radius: 12px;
        }}
        
        .voice-button {{
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
        }}
        
        .stButton > button {{
            padding: 0.6rem 1.2rem;
            font-size: 0.9rem;
        }}
    }}
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {{
        .stApp {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
        }}
    }}
    
    /* High contrast mode */
    @media (prefers-contrast: high) {{
        .stButton > button,
        .stChatMessage,
        .thread-card,
        .assistant-card {{
            border-width: 3px;
        }}
    }}
    
    /* Reduced motion */
    @media (prefers-reduced-motion: reduce) {{
        * {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }}
    }}
    
    /* Print styles */
    @media print {{
        .stSidebar,
        .voice-button,
        .stButton {{
            display: none !important;
        }}
        
        .stChatMessage {{
            box-shadow: none;
            border: 2px solid var(--primary-red);
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_ultimate_header():
    """Render ultimate application header with comprehensive status"""
    # Main header
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.title(f"🚀 {ultimate_config.get('app_name')}")
        st.markdown(f"**{ultimate_config.get('app_description')}**")
        st.caption(f"Version {ultimate_config.get('app_version')} | {ultimate_config.storage_mode.title()} Storage")
    
    with col2:
        # Real-time status indicators
        if ultimate_config.get("realtime_voice_enabled"):
            st.markdown('<div class="status-success">🔴 VOICE LIVE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">⚪ VOICE OFFLINE</div>', unsafe_allow_html=True)
        
        if ultimate_config.get("streaming_enabled"):
            st.markdown('<div class="status-success">⚡ STREAMING</div>', unsafe_allow_html=True)
    
    with col3:
        # System health indicator
        health_score = calculate_system_health()
        if health_score >= 80:
            st.markdown(f'<div class="status-success">💚 {health_score}%</div>', unsafe_allow_html=True)
        elif health_score >= 60:
            st.markdown(f'<div class="status-warning">💛 {health_score}%</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-error">❤️ {health_score}%</div>', unsafe_allow_html=True)
    
    # Comprehensive status grid
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if ultimate_config.get("openai_api_key") and OPENAI_AVAILABLE:
            st.markdown('<div class="status-indicator status-success">✅ OpenAI</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-error">❌ OpenAI</div>', unsafe_allow_html=True)
    
    with col2:
        if ultimate_config.is_supabase_enabled():
            st.markdown('<div class="status-indicator status-success">✅ Supabase</div>', unsafe_allow_html=True)
        elif ultimate_config.storage_mode == "local":
            st.markdown('<div class="status-indicator status-success">✅ Local DB</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">⚠️ Storage</div>', unsafe_allow_html=True)
    
    with col3:
        if ultimate_voice.client and ultimate_config.get("voice_enabled"):
            st.markdown('<div class="status-indicator status-success">✅ Voice</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">⚠️ Voice</div>', unsafe_allow_html=True)
    
    with col4:
        if ADVANCED_AUDIO_AVAILABLE:
            st.markdown('<div class="status-indicator status-success">✅ Audio</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">⚠️ Audio</div>', unsafe_allow_html=True)
    
    with col5:
        if FILE_PROCESSING_AVAILABLE:
            st.markdown('<div class="status-indicator status-success">✅ Files</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">⚠️ Files</div>', unsafe_allow_html=True)
    
    with col6:
        if LANGCHAIN_CORE_AVAILABLE:
            st.markdown('<div class="status-indicator status-success">✅ LangChain</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">⚠️ LangChain</div>', unsafe_allow_html=True)

def calculate_system_health() -> int:
    """Calculate overall system health score"""
    try:
        score = 0
        total_checks = 0
        
        # OpenAI API check
        if ultimate_config.get("openai_api_key") and OPENAI_AVAILABLE:
            score += 20
        total_checks += 20
        
        # Storage check
        if ultimate_config.is_supabase_enabled() or ultimate_config.storage_mode == "local":
            score += 20
        total_checks += 20
        
        # Voice check
        if ultimate_voice.client and ultimate_config.get("voice_enabled"):
            score += 15
        total_checks += 15
        
        # Audio processing check
        if ADVANCED_AUDIO_AVAILABLE:
            score += 15
        total_checks += 15
        
        # File processing check
        if FILE_PROCESSING_AVAILABLE:
            score += 15
        total_checks += 15
        
        # LangChain check
        if LANGCHAIN_CORE_AVAILABLE:
            score += 15
        total_checks += 15
        
        return int((score / total_checks) * 100) if total_checks > 0 else 0
        
    except Exception as e:
        logger.error(f"Error calculating system health: {str(e)}")
        return 0

def render_voice_controls_sidebar():
    """Render comprehensive voice controls in sidebar"""
    st.sidebar.markdown("### 🎙️ Voice Studio")
    
    if ultimate_config.get("voice_enabled"):
        # Voice status
        if ultimate_voice.is_listening:
            st.sidebar.markdown('<div class="status-success">🎤 Listening</div>', unsafe_allow_html=True)
        elif ultimate_voice.is_speaking:
            st.sidebar.markdown('<div class="status-warning">🔊 Speaking</div>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown('<div class="status-indicator">⏸️ Ready</div>', unsafe_allow_html=True)
        
        # Voice controls
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("🎤 Listen", key="voice_listen", use_container_width=True):
                if not ultimate_voice.is_listening:
                    ultimate_voice.start_real_time_listening()
                    st.sidebar.success("Started listening")
                else:
                    ultimate_voice.stop_real_time_listening()
                    st.sidebar.info("Stopped listening")
        
        with col2:
            if st.button("🔇 Stop", key="voice_stop", use_container_width=True):
                ultimate_voice.stop_real_time_listening()
                st.sidebar.info("Voice stopped")
        
        # Voice settings
        with st.sidebar.expander("🎛️ Voice Settings"):
            # Voice selection
            available_voices = ultimate_voice.get_available_voices()
            selected_voice = st.selectbox(
                "Voice", 
                available_voices, 
                index=available_voices.index(ultimate_config.get("voice_type", "alloy")) if ultimate_config.get("voice_type", "alloy") in available_voices else 0
            )
            
            # Voice model
            voice_models = ultimate_voice.get_voice_models()
            selected_model = st.selectbox("Model", voice_models, index=0)
            
            # Voice speed
            voice_speed = st.slider("Speed", 0.25, 4.0, ultimate_config.get("voice_speed", 1.0), 0.25)
            
            # Advanced settings
            st.subheader("Advanced")
            
            vad_enabled = st.checkbox("Voice Activity Detection", ultimate_config.get("voice_activity_detection", True))
            noise_suppression = st.checkbox("Noise Suppression", ultimate_config.get("noise_suppression", True))
            echo_cancellation = st.checkbox("Echo Cancellation", ultimate_config.get("echo_cancellation", True))
            
            # Update config
            ultimate_config.update("voice_type", selected_voice)
            ultimate_config.update("voice_model", selected_model)
            ultimate_config.update("voice_speed", voice_speed)
            ultimate_config.update("voice_activity_detection", vad_enabled)
            ultimate_config.update("noise_suppression", noise_suppression)
            ultimate_config.update("echo_cancellation", echo_cancellation)
        
        # Voice commands
        with st.sidebar.expander("🗣️ Voice Commands"):
            st.write("**Available Commands:**")
            commands = [
                "• 'New chat' - Start new conversation",
                "• 'Switch assistant' - Change assistant",
                "• 'Stop listening' - Mute microphone",
                "• 'Start listening' - Unmute microphone",
                "• 'Save conversation' - Save current chat",
                "• 'Clear chat' - Delete conversation",
                "• 'Help' - Show help information",
                "• 'Settings' - Open settings",
                "• 'Volume up/down' - Adjust volume",
                "• 'Pause/Resume' - Control playback"
            ]
            for command in commands:
                st.caption(command)
        
        # Voice profiles
        if ultimate_config.get("voice_cloning_enabled"):
            with st.sidebar.expander("👤 Voice Profiles"):
                st.write("**Custom Voice Profiles:**")
                
                profiles = list(ultimate_voice.voice_profiles.keys())
                if profiles:
                    selected_profile = st.selectbox("Select Profile", profiles)
                    if st.button("Use Profile", use_container_width=True):
                        st.sidebar.success(f"Switched to {selected_profile}")
                else:
                    st.info("No custom profiles created")
                
                # Create new profile
                if st.button("➕ Create Profile", use_container_width=True):
                    st.sidebar.info("Voice profile creation coming soon!")
        
        # Real-time features
        with st.sidebar.expander("⚡ Real-time Features"):
            realtime_enabled = st.checkbox("Real-time Voice", ultimate_config.get("realtime_voice_enabled", True))
            interruption_enabled = st.checkbox("Voice Interruption", ultimate_config.get("voice_interruption_enabled", True))
            background_listening = st.checkbox("Background Listening", ultimate_config.get("background_listening", False))
            
            ultimate_config.update("realtime_voice_enabled", realtime_enabled)
            ultimate_config.update("voice_interruption_enabled", interruption_enabled)
            ultimate_config.update("background_listening", background_listening)
            
            if background_listening and not ultimate_voice.background_listener:
                ultimate_voice.start_background_listening()
            elif not background_listening and ultimate_voice.background_listener:
                ultimate_config.update("background_listening", False)
    
    else:
        st.sidebar.warning("Voice features disabled")
        if st.sidebar.button("Enable Voice", use_container_width=True):
            ultimate_config.update("voice_enabled", True)
            st.rerun()

def render_storage_sidebar():
    """Render flexible storage management in sidebar"""
    st.sidebar.markdown("### 🗄️ Storage Management")
    
    # Storage mode indicator
    storage_mode = ultimate_config.storage_mode
    if storage_mode == "supabase":
        st.sidebar.success("☁️ Cloud Storage (Supabase)")
    else:
        st.sidebar.info("💾 Local Storage (SQLite)")
    
    # Storage stats
    user_id = st.session_state.get("user_id", "demo_user")
    
    try:
        threads = flexible_storage.get_threads(user_id, limit=1000)
        messages_count = sum(len(flexible_storage.get_messages(thread['id'])) for thread in threads[:10])  # Sample
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Threads", len(threads))
        with col2:
            st.metric("Messages", f"{messages_count}+")
        
        # Storage usage (estimated)
        estimated_usage = len(threads) * 0.1 + messages_count * 0.01  # MB estimate
        st.sidebar.progress(min(1.0, estimated_usage / 100), text=f"Usage: {estimated_usage:.1f}MB")
        
    except Exception as e:
        st.sidebar.error(f"Storage error: {str(e)}")
    
    # Storage actions
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🔄 Sync", use_container_width=True):
            if storage_mode == "supabase":
                success = flexible_storage.sync_from_cloud()
                if success:
                    st.sidebar.success("Synced!")
                else:
                    st.sidebar.error("Sync failed")
            else:
                st.sidebar.info("Local storage active")
    
    with col2:
        if st.button("💾 Backup", use_container_width=True):
            if ultimate_config.get("auto_backup"):
                success = flexible_storage.backup_to_cloud()
                if success:
                    st.sidebar.success("Backed up!")
                else:
                    st.sidebar.warning("Backup unavailable")
            else:
                st.sidebar.info("Backup disabled")
    
    # Storage settings
    with st.sidebar.expander("⚙️ Storage Settings"):
        # Storage mode selection
        if SUPABASE_AVAILABLE and ultimate_config.get("supabase_url"):
            new_storage_mode = st.selectbox(
                "Storage Mode", 
                ["local", "supabase"], 
                index=0 if storage_mode == "local" else 1
            )
            
            if new_storage_mode != storage_mode:
                ultimate_config.storage_mode = new_storage_mode
                st.info("Storage mode changed. Restart to apply.")
        
        # Auto-backup setting
        auto_backup = st.checkbox("Auto Backup", ultimate_config.get("auto_backup", True))
        ultimate_config.update("auto_backup", auto_backup)
        
        # Data retention
        retention_days = st.number_input("Data Retention (days)", 1, 365, 90)
        
        # Export options
        if st.button("📤 Export Data", use_container_width=True):
            st.info("Data export feature coming soon!")
        
        if st.button("🗑️ Clear Old Data", use_container_width=True):
            st.warning("This will delete data older than retention period")

# ======================================================
# 🚀 ULTIMATE MAIN APPLICATION
# ======================================================

def main():
    """Ultimate main application function"""
    try:
        # Configure Streamlit page with enhanced settings
        st.set_page_config(
            page_title=ultimate_config.get("app_name", "Ultimate AI Assistant Platform"),
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/your-repo/help',
                'Report a bug': 'https://github.com/your-repo/issues',
                'About': f"""
                # {ultimate_config.get('app_name')}
                
                **Version:** {ultimate_config.get('app_version')}
                
                Advanced AI platform featuring:
                - 🎙️ Comprehensive voice processing
                - ☁️ Flexible cloud/local storage
                - 🤖 Intelligent AI assistants
                - 🧵 Advanced thread management
                - 📁 Multi-format file processing
                - 📊 Real-time analytics
                - 🎨 Customizable interface
                
                **Storage:** {ultimate_config.storage_mode.title()}
                **Voice:** {'Enabled' if ultimate_config.get('voice_enabled') else 'Disabled'}
                **Real-time:** {'Active' if ultimate_config.get('realtime_voice_enabled') else 'Inactive'}
                """
            }
        )
        
        # Render ultimate CSS
        render_ultimate_css()
        
        # Initialize comprehensive session state
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if "current_page" not in st.session_state:
            st.session_state.current_page = "chat"
        if "current_assistant" not in st.session_state:
            st.session_state.current_assistant = "Strategic Business Consultant"
        if "current_thread_id" not in st.session_state:
            st.session_state.current_thread_id = None
        if "voice_enabled" not in st.session_state:
            st.session_state.voice_enabled = ultimate_config.get("voice_enabled", True)
        if "theme_preference" not in st.session_state:
            st.session_state.theme_preference = "red"
        if "analytics_session" not in st.session_state:
            st.session_state.analytics_session = {
                "start_time": datetime.now(),
                "page_views": 0,
                "interactions": 0,
                "voice_usage": 0
            }
        
        # Log session start
        if ultimate_config.get("analytics_enabled"):
            flexible_storage.log_analytics_event({
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id,
                "event_type": "session_start",
                "event_data": {
                    "storage_mode": ultimate_config.storage_mode,
                    "voice_enabled": ultimate_config.get("voice_enabled"),
                    "user_agent": "streamlit_app"
                }
            })
        
        # Render ultimate header
        render_ultimate_header()
        
        # Render comprehensive sidebar
        with st.sidebar:
            render_storage_sidebar()
            render_voice_controls_sidebar()
            
            # Main navigation menu
            st.markdown("### 🎛️ Navigation Hub")
            
            menu_options = [
                ("💬", "Ultimate Chat", "chat"),
                ("🧵", "Thread Manager", "threads"),
                ("🤖", "AI Assistants", "assistants"),
                ("🔧", "Agent Builder", "agent_builder"),
                ("🎙️", "Voice Studio", "voice_studio"),
                ("📁", "File Processor", "file_manager"),
                ("📊", "Analytics Hub", "analytics"),
                ("🎨", "Customization", "customization"),
                ("⚙️", "System Settings", "settings"),
                ("🔬", "Advanced Tools", "advanced_tools")
            ]
            
            current_page = st.session_state.get("current_page", "chat")
            
            for emoji, label, page_key in menu_options:
                button_class = "menu-item-active" if current_page == page_key else "menu-item"
                if st.button(f"{emoji} {label}", key=f"menu_{page_key}", use_container_width=True):
                    st.session_state.current_page = page_key
                    st.session_state.analytics_session["page_views"] += 1
                    st.session_state.analytics_session["interactions"] += 1
                    
                    # Log page navigation
                    if ultimate_config.get("analytics_enabled"):
                        flexible_storage.log_analytics_event({
                            "user_id": st.session_state.user_id,
                            "session_id": st.session_state.session_id,
                            "event_type": "page_navigation",
                            "event_data": {
                                "from_page": current_page,
                                "to_page": page_key,
                                "timestamp": datetime.now().isoformat()
                            }
                        })
                    
                    st.rerun()
            
            # Quick stats
            st.markdown("### 📈 Quick Stats")
            session_duration = (datetime.now() - st.session_state.analytics_session["start_time"]).total_seconds() / 60
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Session", f"{session_duration:.0f}m")
            with col2:
                st.metric("Actions", st.session_state.analytics_session["interactions"])
        
        # Main content area with enhanced routing
        if current_page == "chat":
            render_ultimate_chat_page()
        elif current_page == "threads":
            render_ultimate_threads_page()
        elif current_page == "assistants":
            render_ultimate_assistants_page()
        elif current_page == "agent_builder":
            render_ultimate_agent_builder_page()
        elif current_page == "voice_studio":
            render_ultimate_voice_studio_page()
        elif current_page == "file_manager":
            render_ultimate_file_manager_page()
        elif current_page == "analytics":
            render_ultimate_analytics_page()
        elif current_page == "customization":
            render_ultimate_customization_page()
        elif current_page == "settings":
            render_ultimate_settings_page()
        elif current_page == "advanced_tools":
            render_ultimate_advanced_tools_page()
        else:
            render_ultimate_chat_page()  # Default fallback
        
        # Handle voice input if available
        handle_voice_input()
        
        # Auto-save session data
        if ultimate_config.get("auto_save_enabled"):
            auto_save_session_data()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}")
        
        # Show debug info in development
        if ultimate_config.get("debug_mode"):
            st.exception(e)
            
            # Debug information
            with st.expander("🔍 Debug Information"):
                st.json({
                    "error": str(e),
                    "storage_mode": ultimate_config.storage_mode,
                    "voice_enabled": ultimate_config.get("voice_enabled"),
                    "session_state_keys": list(st.session_state.keys()),
                    "config_keys": list(ultimate_config.config.keys())
                })

def handle_voice_input():
    """Handle voice input processing"""
    try:
        # Check for voice input
        voice_input = ultimate_voice.get_voice_input()
        if voice_input:
            if voice_input.get('wake_word'):
                st.sidebar.success("🎤 Wake word detected!")
                ultimate_voice.start_real_time_listening()
            else:
                text = voice_input.get('text', '')
                if text and text.strip():
                    st.session_state.voice_input = text
                    st.session_state.analytics_session["voice_usage"] += 1
        
        # Check for voice commands
        voice_command = ultimate_voice.get_voice_command()
        if voice_command:
            execute_voice_command(voice_command)
    
    except Exception as e:
        logger.error(f"Error handling voice input: {str(e)}")

def execute_voice_command(command: Dict[str, Any]):
    """Execute voice command"""
    try:
        command_type = command.get('command')
        
        if command_type == 'new_chat':
            st.session_state.current_thread_id = None
            st.sidebar.success("🆕 New chat started")
        
        elif command_type == 'stop_listening':
            ultimate_voice.stop_real_time_listening()
            st.sidebar.info("🔇 Stopped listening")
        
        elif command_type == 'start_listening':
            ultimate_voice.start_real_time_listening()
            st.sidebar.success("🎤 Started listening")
        
        elif command_type == 'help':
            st.sidebar.info("🆘 Voice commands available in Voice Studio")
        
        elif command_type == 'settings':
            st.session_state.current_page = "settings"
            st.rerun()
        
        # Log command execution
        if ultimate_config.get("analytics_enabled"):
            flexible_storage.log_analytics_event({
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id,
                "event_type": "voice_command_executed",
                "event_data": command
            })
    
    except Exception as e:
        logger.error(f"Error executing voice command: {str(e)}")

def auto_save_session_data():
    """Auto-save session data periodically"""
    try:
        # This would implement periodic auto-save
        # For now, just log the attempt
        if hasattr(st.session_state, 'last_auto_save'):
            time_since_save = time.time() - st.session_state.last_auto_save
            if time_since_save > 300:  # 5 minutes
                st.session_state.last_auto_save = time.time()
                logger.info("Auto-save triggered")
        else:
            st.session_state.last_auto_save = time.time()
    
    except Exception as e:
        logger.error(f"Error in auto-save: {str(e)}")

# Enhanced page renderers (placeholders for full implementation)
def render_ultimate_chat_page():
    st.header("💬 Ultimate Chat Interface")
    st.info("🚧 Ultimate chat interface with real-time voice, streaming, and advanced AI features coming soon!")
    
    # Voice input display
    if hasattr(st.session_state, 'voice_input'):
        st.success(f"🎤 Voice Input: {st.session_state.voice_input}")
        del st.session_state.voice_input

def render_ultimate_threads_page():
    st.header("🧵 Advanced Thread Manager")
    st.info("🚧 Advanced thread management with cloud sync and voice annotations coming soon!")

def render_ultimate_assistants_page():
    st.header("🤖 AI Assistant Gallery")
    st.info("🚧 Enhanced assistant management with voice profiles and custom capabilities coming soon!")

def render_ultimate_agent_builder_page():
    st.header("🔧 Ultimate Agent Builder")
    st.info("🚧 Visual agent builder with voice integration and advanced tools coming soon!")

def render_ultimate_voice_studio_page():
    st.header("🎙️ Voice Studio Pro")
    st.info("🚧 Professional voice processing studio with real-time features coming soon!")
    
    # Voice quality analyzer
    st.subheader("🔊 Voice Quality Analyzer")
    if st.button("Test Microphone"):
        st.info("Microphone test feature coming soon!")

def render_ultimate_file_manager_page():
    st.header("📁 Advanced File Processor")
    st.info("🚧 Advanced file processing with voice transcription and AI analysis coming soon!")

def render_ultimate_analytics_page():
    st.header("📊 Analytics Dashboard Pro")
    st.info("🚧 Comprehensive analytics with voice usage tracking coming soon!")
    
    # Show current session stats
    st.subheader("📈 Current Session")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Duration", f"{((datetime.now() - st.session_state.analytics_session['start_time']).total_seconds() / 60):.0f}m")
    with col2:
        st.metric("Page Views", st.session_state.analytics_session["page_views"])
    with col3:
        st.metric("Interactions", st.session_state.analytics_session["interactions"])
    with col4:
        st.metric("Voice Usage", st.session_state.analytics_session["voice_usage"])

def render_ultimate_customization_page():
    st.header("🎨 Ultimate Customization")
    st.info("🚧 Advanced theming and customization options coming soon!")

def render_ultimate_settings_page():
    st.header("⚙️ System Settings Pro")
    st.info("🚧 Comprehensive system settings with voice configuration coming soon!")

def render_ultimate_advanced_tools_page():
    st.header("🔬 Advanced Tools Laboratory")
    st.info("🚧 Advanced AI tools and experimental features coming soon!")

if __name__ == "__main__":
    main()

