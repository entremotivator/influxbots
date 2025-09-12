#!/usr/bin/env python3
"""
🤖 ENHANCED BUSINESS AI ASSISTANTS - COMPLETE APPLICATION
A comprehensive Streamlit application featuring 110+ specialized AI business assistants
with OpenAI API integration (text + image generation) and streamlined authentication.
Enhanced with hidden Streamlit settings and advanced features.
"""

import streamlit as st
import openai
import tiktoken
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Tuple, Optional
import logging
import hashlib
import os
import pandas as pd
import io
import base64
import requests
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🎨 STREAMLIT CONFIGURATION & STYLING
# ======================================================

# Hide Streamlit settings and menu
st.set_page_config(
    page_title="🤖 Enhanced Business AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Hide Streamlit style elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
.stDecoration {display:none;}

/* Custom styling */
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.bot-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
}

.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}

.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 2rem;
}

.assistant-message {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    margin-right: 2rem;
}

.stButton > button {
    border-radius: 20px;
    border: none;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.stSelectbox > div > div {
    border-radius: 10px;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

.sidebar-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #667eea;
}

.success-message {
    background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.error-message {
    background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.info-message {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

/* Animation for loading */
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.loading {
    animation: pulse 2s infinite;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header {
        padding: 0.5rem;
        font-size: 1.2rem;
    }
    
    .user-message, .assistant-message {
        margin-left: 0;
        margin-right: 0;
    }
}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ======================================================
# 🔑 API CONFIGURATION WITH STREAMLIT SECRETS
# ======================================================

def initialize_openai():
    """Initialize OpenAI with API key from secrets or environment"""
    try:
        # Try Streamlit secrets first
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            api_key = st.secrets['OPENAI_API_KEY']
            openai.api_key = api_key
            return api_key
        
        # Fallback to environment variable
        elif 'OPENAI_API_KEY' in os.environ:
            api_key = os.environ['OPENAI_API_KEY']
            openai.api_key = api_key
            return api_key
        
        # No API key found
        return None
        
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI: {str(e)}")
        return None

# ======================================================
# 🤖 COMPREHENSIVE BUSINESS BOT PERSONALITIES (110+ Total)
# ======================================================

BOT_PERSONALITIES = {
    # ENTREPRENEURSHIP & STARTUPS (15 bots)
    "Startup Strategist": {
        "description": "You specialize in helping new businesses with planning and execution. From MVP development to scaling strategies, I guide entrepreneurs through every stage of their startup journey with practical advice on product-market fit, business model validation, and growth hacking techniques.",
        "emoji": "🚀",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.7,
        "specialties": ["Business Planning", "MVP Development", "Product-Market Fit", "Growth Hacking"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "SaaS", "E-commerce"]
    },
    "Business Plan Writer": {
        "description": "I am a Business Plan Writer specializing in creating comprehensive, investor-ready business plans. I help entrepreneurs articulate their vision, analyze markets, define strategies, and present financial projections that attract investors.",
        "emoji": "📝",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.6,
        "specialties": ["Business Plans", "Market Analysis", "Financial Projections", "Investor Presentations"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Venture Capital Advisor": {
        "description": "As a Venture Capital Advisor, I guide startups through fundraising and investment landscapes. I specialize in pitch deck creation, investor relations, due diligence preparation, and valuation strategies.",
        "emoji": "💼",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.6,
        "specialties": ["Fundraising", "Pitch Decks", "Investor Relations", "Valuation"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Fintech"]
    },
    "Tech Entrepreneur Advisor": {
        "description": "As a Tech Entrepreneur Advisor, I guide technology startups through unique challenges. I provide expertise in product development, technical scaling, IP protection, and technology commercialization strategies.",
        "emoji": "💻",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.7,
        "specialties": ["Tech Startups", "Product Development", "IP Protection", "Scaling"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Software", "Hardware"]
    },
    "Lean Startup Expert": {
        "description": "As a Lean Startup Expert, I help entrepreneurs build businesses using validated learning and iterative development. I focus on build-measure-learn cycles, MVPs, customer feedback, and pivot strategies.",
        "emoji": "🔄",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.7,
        "specialties": ["Lean Methodology", "MVP Development", "Customer Validation", "Pivot Strategies"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Consumer Products"]
    },
    "Incubator Program Director": {
        "description": "As an Incubator Program Director, I help early-stage startups accelerate their growth through structured programs, mentorship, and resource allocation. I specialize in startup acceleration, program design, and ecosystem building.",
        "emoji": "🏢",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.7,
        "specialties": ["Startup Acceleration", "Program Design", "Mentorship", "Ecosystem Building"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Angel Investor Advisor": {
        "description": "As an Angel Investor Advisor, I help individual investors make informed decisions about startup investments. I provide expertise in deal evaluation, due diligence, portfolio management, and exit strategies.",
        "emoji": "👼",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.6,
        "specialties": ["Deal Evaluation", "Due Diligence", "Portfolio Management", "Exit Strategies"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Consumer"]
    },
    "Startup Legal Advisor": {
        "description": "As a Startup Legal Advisor, I provide legal guidance for emerging businesses. I specialize in entity formation, intellectual property, contracts, compliance, and regulatory matters specific to startups.",
        "emoji": "⚖️",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.5,
        "specialties": ["Entity Formation", "IP Law", "Contracts", "Compliance"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Fintech"]
    },
    "Growth Hacking Specialist": {
        "description": "As a Growth Hacking Specialist, I focus on rapid, scalable growth strategies for startups. I use data-driven experiments, viral marketing, and unconventional tactics to achieve exponential user acquisition and retention.",
        "emoji": "📈",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.8,
        "specialties": ["Growth Experiments", "Viral Marketing", "User Acquisition", "Retention"],
        "expertise_level": "Expert",
        "industry_focus": ["SaaS", "Mobile Apps", "E-commerce"]
    },
    "Product-Market Fit Consultant": {
        "description": "As a Product-Market Fit Consultant, I help startups find the sweet spot between their product and market demand. I specialize in customer discovery, product validation, market research, and iterative development.",
        "emoji": "🎯",
        "category": "Entrepreneurship & Startups",
        "temperature": 0.7,
        "specialties": ["Customer Discovery", "Product Validation", "Market Research", "Iterative Development"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Consumer Products"]
    },

    # SALES & MARKETING (20 bots)
    "Sales Performance Coach": {
        "description": "As a Sales Performance Coach, I help individuals and teams maximize sales potential through proven methodologies. I specialize in sales funnel optimization, conversion improvement, objection handling, and closing techniques.",
        "emoji": "💼",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Sales Funnels", "Conversion Optimization", "Objection Handling", "Closing Techniques"],
        "expertise_level": "Expert",
        "industry_focus": ["B2B", "B2C", "SaaS"]
    },
    "Marketing Strategy Expert": {
        "description": "I am a Marketing Strategy Expert with deep expertise in digital marketing, brand positioning, and customer acquisition. I help businesses build compelling campaigns that drive engagement and revenue growth.",
        "emoji": "📱",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Digital Marketing", "Brand Positioning", "Customer Acquisition", "Campaign Strategy"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "E-commerce", "Services"]
    },
    "Digital Marketing Specialist": {
        "description": "As a Digital Marketing Specialist, I focus on online strategies that drive measurable results. I specialize in SEO, PPC advertising, social media marketing, and conversion optimization.",
        "emoji": "🌐",
        "category": "Sales & Marketing",
        "temperature": 0.7,
        "specialties": ["SEO", "PPC Advertising", "Social Media", "Conversion Optimization"],
        "expertise_level": "Expert",
        "industry_focus": ["E-commerce", "SaaS", "Local Business"]
    },
    "Content Marketing Strategist": {
        "description": "I am a Content Marketing Strategist creating engaging content that attracts and converts audiences. I develop content strategies, editorial calendars, and storytelling frameworks for sustainable growth.",
        "emoji": "✍️",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Content Strategy", "Editorial Calendars", "Storytelling", "Brand Authority"],
        "expertise_level": "Expert",
        "industry_focus": ["B2B", "Technology", "Professional Services"]
    },
    "Brand Development Strategist": {
        "description": "I am a Brand Development Strategist helping businesses create compelling brand identities. I focus on brand architecture, messaging frameworks, and visual identity systems.",
        "emoji": "🎨",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Brand Identity", "Brand Architecture", "Messaging", "Visual Design"],
        "expertise_level": "Expert",
        "industry_focus": ["Consumer", "B2B", "Luxury"]
    },
    "Social Media Marketing Manager": {
        "description": "As a Social Media Marketing Manager, I create and execute social media strategies that build communities and drive business results. I specialize in platform-specific strategies, influencer marketing, and social commerce.",
        "emoji": "📱",
        "category": "Sales & Marketing",
        "temperature": 0.8,
        "specialties": ["Social Strategy", "Community Building", "Influencer Marketing", "Social Commerce"],
        "expertise_level": "Expert",
        "industry_focus": ["Consumer", "E-commerce", "Entertainment"]
    },
    "Email Marketing Specialist": {
        "description": "As an Email Marketing Specialist, I design and optimize email campaigns that nurture leads and drive conversions. I focus on automation, segmentation, personalization, and deliverability optimization.",
        "emoji": "📧",
        "category": "Sales & Marketing",
        "temperature": 0.7,
        "specialties": ["Email Automation", "Segmentation", "Personalization", "Deliverability"],
        "expertise_level": "Expert",
        "industry_focus": ["E-commerce", "SaaS", "B2B"]
    },
    "SEO Optimization Expert": {
        "description": "As an SEO Optimization Expert, I help businesses improve their search engine visibility and organic traffic. I specialize in technical SEO, content optimization, link building, and local SEO strategies.",
        "emoji": "🔍",
        "category": "Sales & Marketing",
        "temperature": 0.6,
        "specialties": ["Technical SEO", "Content Optimization", "Link Building", "Local SEO"],
        "expertise_level": "Expert",
        "industry_focus": ["E-commerce", "Local Business", "SaaS"]
    },
    "PPC Campaign Manager": {
        "description": "As a PPC Campaign Manager, I create and optimize paid advertising campaigns across multiple platforms. I specialize in Google Ads, Facebook Ads, campaign optimization, and ROI maximization.",
        "emoji": "💰",
        "category": "Sales & Marketing",
        "temperature": 0.7,
        "specialties": ["Google Ads", "Facebook Ads", "Campaign Optimization", "ROI Analysis"],
        "expertise_level": "Expert",
        "industry_focus": ["E-commerce", "Lead Generation", "SaaS"]
    },
    "Marketing Analytics Specialist": {
        "description": "As a Marketing Analytics Specialist, I help businesses measure and optimize their marketing performance. I specialize in data analysis, attribution modeling, customer journey mapping, and ROI measurement.",
        "emoji": "📊",
        "category": "Sales & Marketing",
        "temperature": 0.6,
        "specialties": ["Data Analysis", "Attribution Modeling", "Customer Journey", "ROI Measurement"],
        "expertise_level": "Expert",
        "industry_focus": ["E-commerce", "SaaS", "B2B"]
    },

    # FINANCE & ACCOUNTING (20 bots)
    "Financial Controller": {
        "description": "As a Financial Controller, I specialize in business financial management, budgeting, and financial planning. I help optimize financial operations, manage cash flow, and implement cost control measures.",
        "emoji": "💰",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Financial Planning", "Budget Management", "Cash Flow", "Cost Control"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Investment Banking Advisor": {
        "description": "As an Investment Banking Advisor, I provide expertise in corporate finance, M&A, and capital raising. I help evaluate opportunities, structure deals, and conduct financial valuations.",
        "emoji": "🏦",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Corporate Finance", "M&A", "Capital Raising", "Valuations"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Manufacturing"]
    },
    "Financial Analyst": {
        "description": "As a Financial Analyst, I provide comprehensive financial modeling and analysis for business decisions. I specialize in forecasting, investment analysis, and performance measurement.",
        "emoji": "📈",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Financial Modeling", "Forecasting", "Investment Analysis", "Performance Metrics"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Tax Strategy Consultant": {
        "description": "As a Tax Strategy Consultant, I help businesses optimize their tax position through strategic planning. I specialize in tax compliance, planning, international tax, and tax-efficient structures.",
        "emoji": "📋",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Tax Planning", "Compliance", "International Tax", "Tax Structures"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Risk Management Specialist": {
        "description": "As a Risk Management Specialist, I help organizations identify, assess, and mitigate financial and operational risks. I specialize in risk assessment, compliance, insurance, and crisis management.",
        "emoji": "🛡️",
        "category": "Finance & Accounting",
        "temperature": 0.5,
        "specialties": ["Risk Assessment", "Compliance", "Insurance", "Crisis Management"],
        "expertise_level": "Expert",
        "industry_focus": ["Financial Services", "Healthcare", "Manufacturing"]
    },

    # OPERATIONS & MANAGEMENT (20 bots)
    "Operations Excellence Manager": {
        "description": "I am an Operations Excellence Manager focused on streamlining processes and maximizing efficiency. I specialize in process improvement, supply chain optimization, and lean methodologies.",
        "emoji": "⚙️",
        "category": "Operations & Management",
        "temperature": 0.6,
        "specialties": ["Process Improvement", "Supply Chain", "Lean Methodologies", "Efficiency"],
        "expertise_level": "Expert",
        "industry_focus": ["Manufacturing", "Logistics", "Healthcare"]
    },
    "Project Management Expert": {
        "description": "I am a Project Management Expert helping organizations deliver projects on time and within budget. I specialize in planning, resource allocation, risk management, and stakeholder communication.",
        "emoji": "📋",
        "category": "Operations & Management",
        "temperature": 0.6,
        "specialties": ["Project Planning", "Resource Management", "Risk Management", "Stakeholder Communication"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Construction", "Consulting"]
    },
    "Supply Chain Optimizer": {
        "description": "As a Supply Chain Optimizer, I help businesses streamline their supply chain operations for maximum efficiency and cost-effectiveness. I specialize in logistics, vendor management, inventory optimization, and procurement.",
        "emoji": "🚚",
        "category": "Operations & Management",
        "temperature": 0.6,
        "specialties": ["Logistics", "Vendor Management", "Inventory Optimization", "Procurement"],
        "expertise_level": "Expert",
        "industry_focus": ["Manufacturing", "Retail", "E-commerce"]
    },
    "Quality Assurance Director": {
        "description": "As a Quality Assurance Director, I ensure products and services meet the highest standards. I specialize in quality systems, process control, compliance, and continuous improvement.",
        "emoji": "✅",
        "category": "Operations & Management",
        "temperature": 0.5,
        "specialties": ["Quality Systems", "Process Control", "Compliance", "Continuous Improvement"],
        "expertise_level": "Expert",
        "industry_focus": ["Manufacturing", "Healthcare", "Software"]
    },

    # TECHNOLOGY & INNOVATION (20 bots)
    "Digital Transformation Consultant": {
        "description": "As a Digital Transformation Consultant, I help organizations leverage technology to transform business models and operations. I specialize in digital strategy and change management.",
        "emoji": "🔄",
        "category": "Technology & Innovation",
        "temperature": 0.7,
        "specialties": ["Digital Strategy", "Technology Adoption", "Change Management", "Innovation"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "AI Strategy Consultant": {
        "description": "I am an AI Strategy Consultant helping businesses leverage artificial intelligence for competitive advantage. I specialize in AI implementation, automation, and machine learning applications.",
        "emoji": "🤖",
        "category": "Technology & Innovation",
        "temperature": 0.7,
        "specialties": ["AI Implementation", "Machine Learning", "Automation", "AI Strategy"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Finance"]
    },
    "Cybersecurity Specialist": {
        "description": "I am a Cybersecurity Specialist protecting organizations from digital threats. I specialize in security architecture, threat assessment, incident response, and compliance management.",
        "emoji": "🛡️",
        "category": "Technology & Innovation",
        "temperature": 0.5,
        "specialties": ["Security Architecture", "Threat Assessment", "Incident Response", "Compliance"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Financial Services", "Healthcare"]
    },
    "Cloud Architecture Consultant": {
        "description": "As a Cloud Architecture Consultant, I help organizations design and implement scalable cloud solutions. I specialize in cloud migration, architecture design, cost optimization, and security.",
        "emoji": "☁️",
        "category": "Technology & Innovation",
        "temperature": 0.6,
        "specialties": ["Cloud Migration", "Architecture Design", "Cost Optimization", "Cloud Security"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Enterprise", "Startups"]
    },
    "Data Science Consultant": {
        "description": "As a Data Science Consultant, I help organizations extract insights from data to drive business decisions. I specialize in data analytics, machine learning, predictive modeling, and data visualization.",
        "emoji": "📊",
        "category": "Technology & Innovation",
        "temperature": 0.6,
        "specialties": ["Data Analytics", "Machine Learning", "Predictive Modeling", "Data Visualization"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Finance"]
    },

    # HUMAN RESOURCES (15 bots)
    "Human Resources Director": {
        "description": "As an HR Director, I provide strategic HR leadership aligning human capital with business objectives. I specialize in HR strategy, organizational development, and talent management.",
        "emoji": "👥",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["HR Strategy", "Organizational Development", "Talent Management", "Employee Engagement"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Talent Acquisition Manager": {
        "description": "I am a Talent Acquisition Manager specializing in attracting and hiring top talent. I focus on recruitment strategy, candidate sourcing, and employer branding.",
        "emoji": "🎯",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["Recruitment Strategy", "Candidate Sourcing", "Employer Branding", "Hiring Process"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Healthcare", "Finance"]
    },
    "Employee Engagement Specialist": {
        "description": "As an Employee Engagement Specialist, I help organizations create positive work environments that motivate and retain employees. I specialize in engagement surveys, culture development, and retention strategies.",
        "emoji": "💪",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["Engagement Surveys", "Culture Development", "Retention Strategies", "Employee Satisfaction"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Learning & Development Manager": {
        "description": "As a Learning & Development Manager, I design and implement training programs that develop employee skills and capabilities. I specialize in training design, skill assessment, and career development.",
        "emoji": "📚",
        "category": "Human Resources",
        "temperature": 0.7,
        "specialties": ["Training Design", "Skill Assessment", "Career Development", "Leadership Development"],
        "expertise_level": "Expert",
        "industry_focus": ["All Industries"]
    },
    "Compensation & Benefits Analyst": {
        "description": "As a Compensation & Benefits Analyst, I design competitive compensation packages that attract and retain talent. I specialize in salary benchmarking, benefits design, and equity compensation.",
        "emoji": "💵",
        "category": "Human Resources",
        "temperature": 0.6,
        "specialties": ["Salary Benchmarking", "Benefits Design", "Equity Compensation", "Total Rewards"],
        "expertise_level": "Expert",
        "industry_focus": ["Technology", "Finance", "Healthcare"]
    },

    # CUSTOMER RELATIONS (10 bots)
    "Customer Success Manager": {
        "description": "As a Customer Success Manager, I ensure customers achieve desired outcomes. I specialize in customer onboarding, relationship management, and retention strategies.",
        "emoji": "🤝",
        "category": "Customer Relations",
        "temperature": 0.8,
        "specialties": ["Customer Onboarding", "Relationship Management", "Retention", "Value Realization"],
        "expertise_level": "Expert",
        "industry_focus": ["SaaS", "Technology", "Services"]
    },
    "Customer Experience Director": {
        "description": "I am a Customer Experience Director designing exceptional customer journeys. I specialize in experience design, journey mapping, and touchpoint optimization.",
        "emoji": "⭐",
        "category": "Customer Relations",
        "temperature": 0.8,
        "specialties": ["Experience Design", "Journey Mapping", "Touchpoint Optimization", "Customer Satisfaction"],
        "expertise_level": "Expert",
        "industry_focus": ["Retail", "Hospitality", "Financial Services"]
    },
    "Customer Support Specialist": {
        "description": "As a Customer Support Specialist, I help organizations deliver exceptional customer service. I specialize in support processes, team training, technology implementation, and service quality.",
        "emoji": "🎧",
        "category": "Customer Relations",
        "temperature": 0.7,
        "specialties": ["Support Processes", "Team Training", "Technology Implementation", "Service Quality"],
        "expertise_level": "Expert",
        "industry_focus": ["SaaS", "E-commerce", "Technology"]
    },
    "Customer Retention Strategist": {
        "description": "As a Customer Retention Strategist, I develop programs to keep customers engaged and loyal. I specialize in churn analysis, loyalty programs, customer lifecycle management, and win-back campaigns.",
        "emoji": "🔄",
        "category": "Customer Relations",
        "temperature": 0.7,
        "specialties": ["Churn Analysis", "Loyalty Programs", "Lifecycle Management", "Win-back Campaigns"],
        "expertise_level": "Expert",
        "industry_focus": ["SaaS", "Subscription", "E-commerce"]
    },
}

# ======================================================
# 💰 TOKEN MANAGEMENT & COST CALCULATION
# ======================================================

# OpenAI Pricing (updated rates)
OPENAI_PRICING = {
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4-turbo-preview": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    "dall-e-3": {"1024x1024": 0.040, "1024x1792": 0.080, "1792x1024": 0.080},
    "dall-e-2": {"1024x1024": 0.020, "512x512": 0.018, "256x256": 0.016}
}

class TokenManager:
    def __init__(self, model="gpt-4-turbo"):
        self.model = model
        self.encoding = None
        self.initialize_encoding()
    
    def initialize_encoding(self):
        """Initialize token encoding with error handling"""
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            try:
                self.encoding = tiktoken.get_encoding("cl100k_base")
                logger.warning(f"Model {self.model} not found, using cl100k_base encoding")
            except Exception as e:
                logger.error(f"Failed to initialize encoding: {str(e)}")
                self.encoding = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text with error handling"""
        if not self.encoding:
            return max(1, len(text) // 4)  # Fallback estimation
        
        try:
            return len(self.encoding.encode(str(text)))
        except Exception as e:
            logger.error(f"Token counting error: {str(e)}")
            return max(1, len(text) // 4)
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost based on token usage"""
        if model not in OPENAI_PRICING:
            return 0.0
        
        pricing = OPENAI_PRICING[model]
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost

# ======================================================
# 🎯 ENHANCED CHAT MANAGER WITH ADVANCED FEATURES
# ======================================================

class EnhancedChatManager:
    def __init__(self):
        self.token_manager = TokenManager()
        self.conversation_history = []
        self.session_stats = {
            "total_tokens": 0,
            "total_cost": 0.0,
            "messages_count": 0,
            "session_start": datetime.now()
        }
    
    def generate_response(self, messages: List[Dict], model: str = "gpt-4-turbo", temperature: float = 0.7) -> Tuple[str, Dict]:
        """Generate response with enhanced error handling and analytics"""
        try:
            # Count input tokens
            input_text = "\n".join([msg["content"] for msg in messages])
            input_tokens = self.token_manager.count_tokens(input_text)
            
            # Make API call
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
                stream=False
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            output_tokens = self.token_manager.count_tokens(assistant_message)
            total_tokens = input_tokens + output_tokens
            
            # Calculate cost
            cost = self.token_manager.calculate_cost(input_tokens, output_tokens, model)
            
            # Update session stats
            self.session_stats["total_tokens"] += total_tokens
            self.session_stats["total_cost"] += cost
            self.session_stats["messages_count"] += 1
            
            # Store conversation
            self.conversation_history.append({
                "timestamp": datetime.now(),
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "messages": messages,
                "response": assistant_message
            })
            
            metadata = {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost": cost,
                "temperature": temperature,
                "timestamp": datetime.now().isoformat()
            }
            
            return assistant_message, metadata
            
        except Exception as e:
            logger.error(f"Chat generation error: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}", {"error": True, "message": str(e)}
    
    def generate_image(self, prompt: str, model: str = "dall-e-3", size: str = "1024x1024") -> Tuple[str, Dict]:
        """Generate image with cost tracking"""
        try:
            response = openai.Image.create(
                prompt=prompt,
                model=model,
                size=size,
                n=1
            )
            
            image_url = response.data[0].url
            cost = OPENAI_PRICING.get(model, {}).get(size, 0.0)
            
            # Update session stats
            self.session_stats["total_cost"] += cost
            
            metadata = {
                "model": model,
                "size": size,
                "cost": cost,
                "timestamp": datetime.now().isoformat()
            }
            
            return image_url, metadata
            
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            return None, {"error": True, "message": str(e)}
    
    def get_session_analytics(self) -> Dict:
        """Get comprehensive session analytics"""
        session_duration = datetime.now() - self.session_stats["session_start"]
        
        return {
            "session_duration": str(session_duration).split('.')[0],
            "total_messages": self.session_stats["messages_count"],
            "total_tokens": self.session_stats["total_tokens"],
            "total_cost": self.session_stats["total_cost"],
            "avg_tokens_per_message": self.session_stats["total_tokens"] / max(1, self.session_stats["messages_count"]),
            "avg_cost_per_message": self.session_stats["total_cost"] / max(1, self.session_stats["messages_count"]),
            "conversation_history_length": len(self.conversation_history)
        }

# ======================================================
# 📊 ADVANCED ANALYTICS AND VISUALIZATION
# ======================================================

def create_usage_analytics_chart(chat_manager: EnhancedChatManager):
    """Create comprehensive usage analytics visualization"""
    if not chat_manager.conversation_history:
        return None
    
    # Prepare data
    df_data = []
    for conv in chat_manager.conversation_history:
        df_data.append({
            'timestamp': conv['timestamp'],
            'model': conv['model'],
            'input_tokens': conv['input_tokens'],
            'output_tokens': conv['output_tokens'],
            'total_tokens': conv['input_tokens'] + conv['output_tokens'],
            'cost': conv['cost']
        })
    
    df = pd.DataFrame(df_data)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Token Usage Over Time', 'Cost Distribution by Model', 
                       'Tokens by Message Type', 'Cumulative Cost'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Token usage over time
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['total_tokens'], 
                  mode='lines+markers', name='Total Tokens',
                  line=dict(color='#667eea')),
        row=1, col=1
    )
    
    # Cost by model
    cost_by_model = df.groupby('model')['cost'].sum()
    fig.add_trace(
        go.Bar(x=cost_by_model.index, y=cost_by_model.values,
               name='Cost by Model', marker_color='#764ba2'),
        row=1, col=2
    )
    
    # Input vs Output tokens
    fig.add_trace(
        go.Bar(x=['Input Tokens', 'Output Tokens'], 
               y=[df['input_tokens'].sum(), df['output_tokens'].sum()],
               name='Token Distribution', marker_color=['#667eea', '#764ba2']),
        row=2, col=1
    )
    
    # Cumulative cost
    df['cumulative_cost'] = df['cost'].cumsum()
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['cumulative_cost'],
                  mode='lines', name='Cumulative Cost',
                  line=dict(color='#ff6b6b')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, 
                     title_text="Session Analytics Dashboard")
    
    return fig

def render_model_selector():
    """Enhanced model selector with descriptions"""
    st.markdown("### 🤖 Model Selection")
    
    model_info = {
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "description": "Most capable, best for complex tasks",
            "cost": "Medium",
            "speed": "Fast"
        },
        "gpt-4": {
            "name": "GPT-4",
            "description": "High quality, slower but very capable",
            "cost": "High",
            "speed": "Slow"
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "description": "Fast and cost-effective",
            "cost": "Low",
            "speed": "Very Fast"
        }
    }
    
    selected_model = st.selectbox(
        "Choose Model",
        list(model_info.keys()),
        format_func=lambda x: f"{model_info[x]['name']} - {model_info[x]['description']}"
    )
    
    # Show model details
    model_details = model_info[selected_model]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cost", model_details["cost"])
    with col2:
        st.metric("Speed", model_details["speed"])
    with col3:
        pricing = OPENAI_PRICING.get(selected_model, {"input": 0, "output": 0})
        st.metric("Input/1K", f"${pricing['input']:.3f}")
    
    return selected_model

def render_usage_dashboard():
    """Enhanced usage dashboard with visualizations"""
    st.markdown("### 📊 Usage Dashboard")
    
    if "chat_manager" not in st.session_state:
        st.info("Start chatting to see usage statistics")
        return
    
    analytics = st.session_state.chat_manager.get_session_analytics()
    
    # Main metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Cost", f"${analytics['total_cost']:.4f}")
        st.metric("Messages", analytics['total_messages'])
    with col2:
        st.metric("Total Tokens", f"{analytics['total_tokens']:,}")
        st.metric("Session Time", analytics['session_duration'])
    
    # Advanced metrics
    with st.expander("📈 Advanced Analytics", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg Tokens/Message", f"{analytics['avg_tokens_per_message']:.1f}")
        with col2:
            st.metric("Avg Cost/Message", f"${analytics['avg_cost_per_message']:.4f}")
        
        # Usage chart
        if st.session_state.chat_manager.conversation_history:
            chart = create_usage_analytics_chart(st.session_state.chat_manager)
            if chart:
                st.plotly_chart(chart, use_container_width=True)

# ======================================================
# 🎨 ENHANCED UI COMPONENTS
# ======================================================

def render_bot_card(bot_name: str, bot_info: Dict):
    """Render enhanced bot information card"""
    st.markdown(f"""
    <div class="bot-card">
        <h4>{bot_info['emoji']} {bot_name}</h4>
        <p><strong>Category:</strong> {bot_info['category']}</p>
        <p><strong>Expertise:</strong> {bot_info['expertise_level']}</p>
        <p><strong>Industries:</strong> {', '.join(bot_info['industry_focus'])}</p>
        <p><strong>Specialties:</strong> {', '.join(bot_info['specialties'])}</p>
        <p>{bot_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)

def render_conversation_export():
    """Enhanced conversation export with multiple formats"""
    st.markdown("### 💾 Export Conversation")
    
    if not st.session_state.messages:
        st.info("No conversation to export")
        return
    
    export_format = st.selectbox("Export Format", ["JSON", "TXT", "CSV", "PDF"])
    
    if st.button("📥 Generate Export"):
        if export_format == "JSON":
            export_data = {
                "session_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "assistant": st.session_state.get("current_bot", "Unknown"),
                "model": st.session_state.get("selected_model", "Unknown"),
                "messages": st.session_state.messages,
                "analytics": st.session_state.chat_manager.get_session_analytics() if "chat_manager" in st.session_state else {}
            }
            
            json_str = json.dumps(export_data, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_str,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        elif export_format == "CSV":
            csv_data = []
            for i, msg in enumerate(st.session_state.messages):
                csv_data.append({
                    "Message_ID": i + 1,
                    "Role": msg["role"],
                    "Content": msg["content"],
                    "Timestamp": msg.get("timestamp", datetime.now().isoformat()),
                    "Cost": msg.get("metadata", {}).get("cost", 0),
                    "Tokens": msg.get("metadata", {}).get("total_tokens", 0)
                })
            
            df = pd.DataFrame(csv_data)
            csv_string = df.to_csv(index=False)
            
            st.download_button(
                label="📊 Download CSV",
                data=csv_string,
                file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

# ======================================================
# 🚀 MAIN CHAT INTERFACE WITH ENHANCED FEATURES
# ======================================================

def main_chat_interface():
    """Enhanced main chat interface with advanced features"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Enhanced Business AI Assistant</h1>
        <p>Chat with 110+ specialized AI business consultants with advanced analytics and features</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    api_key = initialize_openai()
    if not api_key:
        st.markdown("""
        <div class="error-message">
            <h3>⚠️ OpenAI API Key Required</h3>
            <p>Please configure your OpenAI API key to use this application.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📋 API Key Configuration Guide", expanded=True):
            st.markdown("""
            **Option 1: Using Streamlit Secrets (Recommended)**
            1. Create a `.streamlit/secrets.toml` file in your project root
            2. Add your API key:
            ```toml
            OPENAI_API_KEY = "sk-your-api-key-here"
            ```
            3. Restart the application
            
            **Option 2: Using Environment Variables**
            1. Set the environment variable:
            ```bash
            export OPENAI_API_KEY="sk-your-api-key-here"
            ```
            2. Restart the application
            
            **Get Your API Key:**
            - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
            - Create a new API key
            - Copy and paste it using one of the methods above
            """)
        return
    
    st.markdown("""
    <div class="success-message">
        <p>✅ OpenAI API configured successfully!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat manager
    if "chat_manager" not in st.session_state:
        st.session_state.chat_manager = EnhancedChatManager()
    
    # Sidebar controls
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🤖 Assistant Selection")
        
        # Search and filter
        search_term = st.text_input("🔍 Search Assistants", placeholder="Type to search...")
        
        categories = list(set([bot["category"] for bot in BOT_PERSONALITIES.values()]))
        selected_category = st.selectbox("Filter by Category", ["All"] + sorted(categories))
        
        # Filter bots
        if selected_category == "All":
            available_bots = list(BOT_PERSONALITIES.keys())
        else:
            available_bots = [name for name, bot in BOT_PERSONALITIES.items() 
                            if bot["category"] == selected_category]
        
        if search_term:
            available_bots = [bot for bot in available_bots 
                            if search_term.lower() in bot.lower() or 
                            search_term.lower() in BOT_PERSONALITIES[bot]["description"].lower()]
        
        st.caption(f"📊 {len(available_bots)} assistants available")
        
        current_bot = st.selectbox("Choose Assistant", available_bots)
        st.session_state.current_bot = current_bot
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model selection
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        selected_model = render_model_selector()
        st.session_state.selected_model = selected_model
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Usage dashboard
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        render_usage_dashboard()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced features
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 🎨 Advanced Features")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🖼️ Generate Image"):
                st.session_state.show_image_generator = True
        with col2:
            if st.button("📊 Analytics"):
                st.session_state.show_analytics = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Export Chat"):
                st.session_state.show_export = True
        with col2:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.session_state.chat_manager = EnhancedChatManager()
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display current bot info
        if current_bot in BOT_PERSONALITIES:
            bot_info = BOT_PERSONALITIES[current_bot]
            render_bot_card(current_bot, bot_info)
        
        # Chat interface
        st.markdown("### 💬 Conversation")
        
        # Display chat messages with enhanced styling
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>{bot_info['emoji']} {current_bot}:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                if "metadata" in message and message["metadata"] and not message["metadata"].get("error"):
                    metadata = message["metadata"]
                    st.caption(f"💰 ${metadata['cost']:.4f} | 🔢 {metadata.get('total_tokens', 0)} tokens | 🤖 {metadata.get('model', 'N/A')} | ⏰ {metadata.get('timestamp', '')}")
        
        # Chat input
        if prompt := st.chat_input("Ask your AI assistant anything..."):
            # Add user message
            user_message = {"role": "user", "content": prompt, "timestamp": datetime.now().isoformat()}
            st.session_state.messages.append(user_message)
            
            # Generate assistant response
            with st.spinner("🤔 Thinking..."):
                bot_info = BOT_PERSONALITIES[current_bot]
                system_prompt = f"""You are a {current_bot}. {bot_info['description']}

Your role is to provide expert, actionable advice with specific examples and implementation strategies. Always:
- Ask clarifying questions to understand the business context
- Provide practical, implementable recommendations
- Share relevant industry best practices and case studies
- Consider both short-term tactics and long-term strategic implications
- Offer specific metrics and KPIs to measure success
- Use data and examples when possible
- Maintain a professional yet approachable tone

Tailor your advice to the specific business size, industry, and maturity level. Your expertise areas include: {', '.join(bot_info['specialties'])}."""
                
                messages_for_api = [
                    {"role": "system", "content": system_prompt}
                ] + st.session_state.messages
                
                response, metadata = st.session_state.chat_manager.generate_response(
                    messages_for_api,
                    selected_model,
                    bot_info["temperature"]
                )
                
                # Add assistant message
                assistant_message = {
                    "role": "assistant",
                    "content": response,
                    "metadata": metadata,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.messages.append(assistant_message)
            
            st.rerun()
    
    with col2:
        # Side features
        if st.session_state.get("show_image_generator", False):
            st.markdown("### 🎨 AI Image Generation")
            
            image_prompt = st.text_area("Describe the image:", 
                                       placeholder="A professional business meeting in a modern office...")
            
            col1, col2 = st.columns(2)
            with col1:
                image_size = st.selectbox("Size", ["1024x1024", "1024x1792", "1792x1024"])
            with col2:
                image_model = st.selectbox("Model", ["dall-e-3", "dall-e-2"])
            
            if st.button("🎨 Generate") and image_prompt:
                with st.spinner("🎨 Creating image..."):
                    image_url, metadata = st.session_state.chat_manager.generate_image(
                        image_prompt, image_model, image_size
                    )
                    
                    if image_url and not metadata.get("error"):
                        st.image(image_url, caption=f"Generated: {image_prompt}")
                        st.success(f"Cost: ${metadata['cost']:.3f}")
                    else:
                        st.error(f"Error: {metadata.get('message', 'Unknown error')}")
            
            if st.button("❌ Close"):
                st.session_state.show_image_generator = False
                st.rerun()
        
        if st.session_state.get("show_analytics", False):
            st.markdown("### 📊 Session Analytics")
            
            if st.session_state.chat_manager.conversation_history:
                analytics = st.session_state.chat_manager.get_session_analytics()
                
                st.metric("Session Duration", analytics['session_duration'])
                st.metric("Total Messages", analytics['total_messages'])
                st.metric("Total Cost", f"${analytics['total_cost']:.4f}")
                st.metric("Total Tokens", f"{analytics['total_tokens']:,}")
                
                # Mini chart
                chart = create_usage_analytics_chart(st.session_state.chat_manager)
                if chart:
                    st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("No analytics data available yet")
            
            if st.button("❌ Close Analytics"):
                st.session_state.show_analytics = False
                st.rerun()
        
        if st.session_state.get("show_export", False):
            render_conversation_export()
            
            if st.button("❌ Close Export"):
                st.session_state.show_export = False
                st.rerun()

# ======================================================
# 🚀 MAIN APPLICATION ENTRY POINT
# ======================================================

def main():
    """Enhanced main application entry point"""
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "usage_stats" not in st.session_state:
        st.session_state.usage_stats = {
            "total_cost": 0.0,
            "daily_cost": 0.0,
            "total_tokens": 0,
            "requests_count": 0,
            "images_generated": 0,
            "last_reset": datetime.now().date()
        }
    
    # Run main chat interface
    main_chat_interface()

if __name__ == "__main__":
    main()

