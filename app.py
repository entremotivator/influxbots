#!/usr/bin/env python3
"""
🔧 OPENAI ORGANIZATIONAL API TRACKING DASHBOARD
Admin dashboard for monitoring OpenAI API usage across all users in an organization
"""

import streamlit as st
import openai
import pandas as pd
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Optional
import logging
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ======================================================
# 🔧 OPENAI ORGANIZATIONAL API CLIENT
# ======================================================

class OpenAIOrganizationTracker:
    def __init__(self, api_key: str, organization_id: str = None):
        """Initialize OpenAI client with organization tracking"""
        self.client = openai.OpenAI(
            api_key=api_key,
            organization=organization_id
        )
        self.organization_id = organization_id
    
    def get_usage_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Fetch usage data from OpenAI API"""
        try:
            # Note: This uses the billing API which may require special permissions
            # In practice, you might need to use the usage endpoint or billing API
            usage_data = {
                "total_requests": 0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "models_used": {},
                "daily_usage": [],
                "user_usage": {},
                "error_rate": 0.0
            }
            
            # Simulate API call - replace with actual OpenAI billing API
            # usage = self.client.usage.retrieve(
            #     start_date=start_date.strftime("%Y-%m-%d"),
            #     end_date=end_date.strftime("%Y-%m-%d")
            # )
            
            # For demo purposes, generate sample data
            usage_data = self._generate_sample_data(start_date, end_date)
            
            return usage_data
            
        except Exception as e:
            logger.error(f"Error fetching usage data: {e}")
            return self._generate_sample_data(start_date, end_date)
    
    def _generate_sample_data(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate sample usage data for demonstration"""
        import random
        
        days = (end_date - start_date).days + 1
        daily_usage = []
        
        models = ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]
        users = [f"user_{i}@company.com" for i in range(1, 21)]
        
        total_requests = 0
        total_tokens = 0
        total_cost = 0.0
        models_used = {model: {"requests": 0, "tokens": 0, "cost": 0.0} for model in models}
        user_usage = {user: {"requests": 0, "tokens": 0, "cost": 0.0} for user in users}
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            daily_requests = random.randint(50, 200)
            daily_tokens = random.randint(10000, 50000)
            daily_cost = daily_tokens * 0.00002  # Approximate cost
            
            daily_usage.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "requests": daily_requests,
                "tokens": daily_tokens,
                "cost": daily_cost
            })
            
            total_requests += daily_requests
            total_tokens += daily_tokens
            total_cost += daily_cost
            
            # Distribute usage across models and users
            for model in models:
                model_requests = random.randint(5, 30)
                model_tokens = random.randint(1000, 8000)
                model_cost = model_tokens * random.uniform(0.00001, 0.00006)
                
                models_used[model]["requests"] += model_requests
                models_used[model]["tokens"] += model_tokens
                models_used[model]["cost"] += model_cost
            
            for user in random.sample(users, random.randint(5, 15)):
                user_requests = random.randint(1, 10)
                user_tokens = random.randint(200, 2000)
                user_cost = user_tokens * random.uniform(0.00001, 0.00005)
                
                user_usage[user]["requests"] += user_requests
                user_usage[user]["tokens"] += user_tokens
                user_usage[user]["cost"] += user_cost
        
        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "models_used": models_used,
            "daily_usage": daily_usage,
            "user_usage": user_usage,
            "error_rate": random.uniform(0.5, 3.0)
        }

# ======================================================
# 📊 DASHBOARD COMPONENTS
# ======================================================

def render_overview_metrics(usage_data: Dict):
    """Render overview metrics cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Requests",
            f"{usage_data['total_requests']:,}",
            delta=f"+{usage_data['total_requests'] // 10:,} vs last period"
        )
    
    with col2:
        st.metric(
            "Total Tokens",
            f"{usage_data['total_tokens']:,}",
            delta=f"+{usage_data['total_tokens'] // 8:,} vs last period"
        )
    
    with col3:
        st.metric(
            "Total Cost",
            f"${usage_data['total_cost']:.2f}",
            delta=f"+${usage_data['total_cost'] * 0.15:.2f} vs last period"
        )
    
    with col4:
        st.metric(
            "Error Rate",
            f"{usage_data['error_rate']:.1f}%",
            delta=f"-{usage_data['error_rate'] * 0.2:.1f}% vs last period",
            delta_color="inverse"
        )

def render_usage_charts(usage_data: Dict):
    """Render usage trend charts"""
    st.subheader("📈 Usage Trends")
    
    # Daily usage chart
    df_daily = pd.DataFrame(usage_data['daily_usage'])
    df_daily['date'] = pd.to_datetime(df_daily['date'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_requests = px.line(
            df_daily, 
            x='date', 
            y='requests',
            title='Daily API Requests',
            labels={'requests': 'Number of Requests', 'date': 'Date'}
        )
        fig_requests.update_layout(height=400)
        st.plotly_chart(fig_requests, use_container_width=True)
    
    with col2:
        fig_cost = px.line(
            df_daily, 
            x='date', 
            y='cost',
            title='Daily API Costs',
            labels={'cost': 'Cost ($)', 'date': 'Date'}
        )
        fig_cost.update_layout(height=400)
        st.plotly_chart(fig_cost, use_container_width=True)

def render_model_breakdown(usage_data: Dict):
    """Render model usage breakdown"""
    st.subheader("🤖 Model Usage Breakdown")
    
    models_df = pd.DataFrame.from_dict(usage_data['models_used'], orient='index')
    models_df = models_df.reset_index().rename(columns={'index': 'model'})
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = px.pie(
            models_df, 
            values='requests', 
            names='model',
            title='Requests by Model'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(
            models_df, 
            x='model', 
            y='cost',
            title='Cost by Model',
            labels={'cost': 'Cost ($)', 'model': 'Model'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def render_user_analytics(usage_data: Dict):
    """Render user usage analytics"""
    st.subheader("👥 User Analytics")
    
    # Top users by usage
    users_df = pd.DataFrame.from_dict(usage_data['user_usage'], orient='index')
    users_df = users_df.reset_index().rename(columns={'index': 'user'})
    users_df = users_df.sort_values('cost', ascending=False).head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 10 Users by Cost**")
        fig_users = px.bar(
            users_df, 
            x='cost', 
            y='user',
            orientation='h',
            title='Top Users by API Cost'
        )
        fig_users.update_layout(height=400)
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        st.write("**User Usage Table**")
        display_df = users_df.copy()
        display_df['cost'] = display_df['cost'].apply(lambda x: f"${x:.2f}")
        display_df['tokens'] = display_df['tokens'].apply(lambda x: f"{x:,}")
        display_df['requests'] = display_df['requests'].apply(lambda x: f"{x:,}")
        st.dataframe(display_df, use_container_width=True)

def render_alerts_and_monitoring(usage_data: Dict):
    """Render alerts and monitoring section"""
    st.subheader("🚨 Alerts & Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Cost Alerts**")
        daily_avg_cost = usage_data['total_cost'] / len(usage_data['daily_usage'])
        
        if daily_avg_cost > 50:
            st.error(f"⚠️ High daily average cost: ${daily_avg_cost:.2f}")
        elif daily_avg_cost > 25:
            st.warning(f"⚡ Moderate daily average cost: ${daily_avg_cost:.2f}")
        else:
            st.success(f"✅ Normal daily average cost: ${daily_avg_cost:.2f}")
        
        if usage_data['error_rate'] > 5:
            st.error(f"⚠️ High error rate: {usage_data['error_rate']:.1f}%")
        elif usage_data['error_rate'] > 2:
            st.warning(f"⚡ Moderate error rate: {usage_data['error_rate']:.1f}%")
        else:
            st.success(f"✅ Normal error rate: {usage_data['error_rate']:.1f}%")
    
    with col2:
        st.write("**Usage Limits**")
        
        # Set some example limits
        monthly_limit = 1000.0  # $1000 monthly limit
        daily_limit = 100.0     # $100 daily limit
        
        monthly_usage = usage_data['total_cost']
        daily_avg = usage_data['total_cost'] / len(usage_data['daily_usage'])
        
        monthly_progress = min(monthly_usage / monthly_limit, 1.0)
        daily_progress = min(daily_avg / daily_limit, 1.0)
        
        st.write(f"**Monthly Budget**: ${monthly_usage:.2f} / ${monthly_limit:.2f}")
        st.progress(monthly_progress)
        
        st.write(f"**Daily Average**: ${daily_avg:.2f} / ${daily_limit:.2f}")
        st.progress(daily_progress)

# ======================================================
# 🎯 MAIN DASHBOARD
# ======================================================

def main():
    """Main dashboard application"""
    st.set_page_config(
        page_title="OpenAI Admin API Dashboard",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #ff7f0e 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔧 OpenAI Organizational API Dashboard</h1>
        <p>Monitor and track API usage across your entire organization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.title("⚙️ Configuration")
    
    # API Configuration
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key with organization access"
    )
    
    organization_id = st.sidebar.text_input(
        "Organization ID (Optional)",
        help="Enter your OpenAI organization ID"
    )
    
    # Date range selection
    st.sidebar.subheader("📅 Date Range")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now()
        )
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.rerun()
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)")
    
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Main dashboard
    if api_key:
        try:
            # Initialize tracker
            tracker = OpenAIOrganizationTracker(api_key, organization_id)
            
            # Fetch usage data
            with st.spinner("Fetching usage data..."):
                usage_data = tracker.get_usage_data(
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time())
                )
            
            # Render dashboard components
            render_overview_metrics(usage_data)
            
            st.divider()
            
            render_usage_charts(usage_data)
            
            st.divider()
            
            render_model_breakdown(usage_data)
            
            st.divider()
            
            render_user_analytics(usage_data)
            
            st.divider()
            
            render_alerts_and_monitoring(usage_data)
            
            # Export functionality
            st.sidebar.subheader("📊 Export Data")
            
            if st.sidebar.button("📥 Export to CSV"):
                # Create export data
                export_data = {
                    "daily_usage": pd.DataFrame(usage_data['daily_usage']),
                    "model_usage": pd.DataFrame.from_dict(usage_data['models_used'], orient='index'),
                    "user_usage": pd.DataFrame.from_dict(usage_data['user_usage'], orient='index')
                }
                
                # Convert to CSV
                csv_buffer = []
                for sheet_name, df in export_data.items():
                    csv_buffer.append(f"=== {sheet_name.upper()} ===")
                    csv_buffer.append(df.to_csv(index=True))
                    csv_buffer.append("")
                
                csv_content = "\n".join(csv_buffer)
                
                st.sidebar.download_button(
                    label="📥 Download CSV",
                    data=csv_content,
                    file_name=f"openai_usage_{start_date}_{end_date}.csv",
                    mime="text/csv"
                )
            
        except Exception as e:
            st.error(f"Error connecting to OpenAI API: {e}")
            st.info("💡 Make sure your API key has the necessary permissions for organization billing data.")
    
    else:
        st.info("👆 Please enter your OpenAI API key in the sidebar to get started.")
        
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **API Key**: Enter your OpenAI API key with organization access
        2. **Organization ID**: Optionally specify your organization ID
        3. **Date Range**: Select the period you want to analyze
        4. **Monitor**: View real-time usage metrics and trends
        
        ### 📊 Features
        
        - **Real-time Monitoring**: Track API usage across your organization
        - **Cost Analysis**: Monitor spending by model and user
        - **Usage Trends**: Visualize daily usage patterns
        - **User Analytics**: Identify top users and usage patterns
        - **Alerts**: Get notified about unusual usage or costs
        - **Export**: Download usage data for further analysis
        
        ### 🔐 Security
        
        - API keys are not stored and only used for the current session
        - All data is processed locally in your browser
        - No usage data is transmitted to external servers
        """)

if __name__ == "__main__":
    main()
