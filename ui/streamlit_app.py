# ui/streamlit_app.py
# import streamlit as st
# import plotly.graph_objects as go
# import plotly.express as px
# import pandas as pd
# import sys
# import os
# from datetime import datetime, timedelta

# # Add parent directory to path FIRST
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# if parent_dir not in sys.path:
#     sys.path.insert(0, parent_dir)

# from data.storage import UserStorage
# from data.simulator import GigWorkerSimulator
# from agents.orchestrator_agent import OrchestratorAgent

# # Page configuration
# st.set_page_config(
#     page_title="StormGuard India - AI Financial Coach",
#     page_icon="🌦️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Initialize storage
# storage = UserStorage()

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 2.5rem;
#         font-weight: bold;
#         color: #1f77b4;
#         text-align: center;
#         margin-bottom: 1rem;
#     }
#     .onboarding-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 1rem;
#         color: white;
#         margin: 1rem 0;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin: 0.5rem 0;
#     }
#     .risk-high { background-color: #ffebee; border-left: 4px solid #f44336; padding: 1rem; }
#     .risk-medium { background-color: #fff8e1; border-left: 4px solid #ff9800; padding: 1rem; }
#     .risk-low { background-color: #e8f5e9; border-left: 4px solid #4caf50; padding: 1rem; }
# </style>
# """, unsafe_allow_html=True)


# def show_onboarding():
#     """New user onboarding flow"""
#     st.markdown('<p class="main-header">🌦️ Welcome to StormGuard India!</p>', unsafe_allow_html=True)
#     st.markdown("<h4 style='text-align: center; color: gray;'>AI-Powered Financial Coach for Gig Workers</h4>", unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Check for existing users
#     existing_users = storage.list_users()
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown("### 🆕 New User? Let's Get Started!")
#         st.markdown("Create your profile in 2 minutes")
        
#         with st.form("onboarding_form"):
#             name = st.text_input("👤 Your Name *", placeholder="e.g., Rajesh Kumar")
#             age = st.number_input("🎂 Age", min_value=18, max_value=65, value=25)
#             city = st.selectbox("📍 City *", [
#                 "Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", 
#                 "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Other"
#             ])
            
#             platform = st.multiselect("🚚 Platforms You Work With *", [
#                 "Swiggy", "Zomato", "Dunzo", "Amazon Flex", 
#                 "Uber Eats", "Ola", "Uber", "Rapido", "Other"
#             ], default=["Swiggy"])
            
#             phone = st.text_input("📱 Phone (Optional)", placeholder="9876543210")
            
#             st.markdown("#### 🎯 Your Financial Goals")
#             goal1 = st.text_input("Goal 1", placeholder="e.g., Save ₹20,000 emergency fund")
#             goal2 = st.text_input("Goal 2 (Optional)", placeholder="e.g., Buy bike in 8 months")
            
#             savings_rate = st.slider(
#                 "💰 Auto-Save Rate (% of daily income)",
#                 min_value=2, max_value=10, value=5,
#                 help="We'll automatically save this % from your earnings"
#             )
            
#             st.markdown("#### 📊 Initial Data (Optional)")
#             has_history = st.checkbox("I want to enter my past income data")
#             generate_demo = st.checkbox("Generate demo data to explore the app", value=True)
            
#             submitted = st.form_submit_button("🚀 Create My Account", type="primary", use_container_width=True)
            
#             if submitted:
#                 if not name or not city or not platform:
#                     st.error("Please fill in all required fields (*)")
#                 else:
#                     # Create user
#                     goals = [g for g in [goal1, goal2] if g]
#                     if not goals:
#                         goals = ["Build emergency fund"]
                    
#                     user_data = {
#                         'name': name,
#                         'age': age,
#                         'city': city,
#                         'platform': " + ".join(platform),
#                         'platforms': platform,
#                         'phone': phone,
#                         'goals': goals,
#                         'savings_rate': savings_rate / 100,
#                         'language': 'hinglish'
#                     }
                    
#                     user_id = storage.create_user(user_data)
                    
#                     # Generate demo data if requested
#                     if generate_demo:
#                         simulator = GigWorkerSimulator(name, city)
#                         demo_income = simulator.generate_income_history(90)
#                         demo_spending = simulator.generate_spending_data(30)
                        
#                         # Save demo data
#                         for _, row in demo_income.iterrows():
#                             storage.add_income(user_id, row.to_dict())
#                         for _, row in demo_spending.iterrows():
#                             storage.add_expense(user_id, row.to_dict())
                    
#                     st.session_state.user_id = user_id
#                     st.session_state.onboarding_complete = True
#                     st.success(f"✅ Welcome aboard, {name}! Your account is ready.")
#                     st.rerun()
    
#     with col2:
#         st.markdown("### 👋 Returning User?")
#         st.markdown("Select your profile to continue")
        
#         if existing_users:
#             for user in existing_users:
#                 if st.button(
#                     f"👤 {user['name']} ({user['city']})", 
#                     key=f"user_{user['user_id']}",
#                     use_container_width=True
#                 ):
#                     st.session_state.user_id = user['user_id']
#                     st.session_state.onboarding_complete = True
#                     st.rerun()
#         else:
#             st.info("No existing users found. Create a new account!")
        
#         st.markdown("---")
#         st.markdown("### ✨ Why StormGuard?")
#         st.markdown("""
#         - 🔮 **Predict** your income for the week
#         - ⚠️ **Get alerts** before slow weeks
#         - 💰 **Auto-save** small amounts daily
#         - 🎯 **Track** progress toward your goals
#         - 💬 **Chat** with your AI financial coach
#         """)


# def initialize_app():
#     """Initialize app with user data"""
#     user_id = st.session_state.user_id
    
#     # Load user data
#     profile, income_df, spending_df = storage.get_data_for_agents(user_id)
    
#     # Check if we have enough data
#     if income_df.empty:
#         # Generate some initial data
#         simulator = GigWorkerSimulator(profile['name'], profile['city'])
#         income_df = simulator.generate_income_history(90)
#         spending_df = simulator.generate_spending_data(30)
        
#         # Save generated data
#         for _, row in income_df.iterrows():
#             storage.add_income(user_id, row.to_dict())
#         for _, row in spending_df.iterrows():
#             storage.add_expense(user_id, row.to_dict())
    
#     # Initialize orchestrator
#     orchestrator = OrchestratorAgent(profile, income_df, spending_df)
    
#     return profile, income_df, spending_df, orchestrator


# def show_data_entry_sidebar(user_id, profile):
#     """Sidebar with data entry forms"""
#     st.sidebar.markdown("---")
#     st.sidebar.markdown("### 📝 Quick Entry")
    
#     entry_type = st.sidebar.selectbox("Add New:", ["💰 Today's Income", "💸 Expense", "🎯 New Goal"])
    
#     if entry_type == "💰 Today's Income":
#         with st.sidebar.form("income_form"):
#             income_date = st.date_input("Date", datetime.now())
#             income_amount = st.number_input("Income (₹)", min_value=0, value=500, step=50)
#             hours_worked = st.number_input("Hours Worked", min_value=1, max_value=16, value=8)
#             orders = st.number_input("Orders Completed", min_value=0, value=20)
#             platform = st.selectbox("Platform", profile.get('platforms', ['Swiggy', 'Zomato']))
            
#             if st.form_submit_button("💾 Save Income", use_container_width=True):
#                 storage.add_income(user_id, {
#                     'date': income_date.strftime('%Y-%m-%d'),
#                     'income': income_amount,
#                     'hours_worked': hours_worked,
#                     'orders_completed': orders,
#                     'platform': platform,
#                     'efficiency': round(income_amount / hours_worked, 2),
#                     'weather': 'clear',
#                     'is_festival': False,
#                     'is_weekend': income_date.weekday() >= 5
#                 })
                
#                 # Auto-save
#                 savings_rate = profile.get('savings_rate', 0.05)
#                 savings_amount = income_amount * savings_rate
#                 storage.add_savings(user_id, {
#                     'date': income_date.strftime('%Y-%m-%d'),
#                     'amount': savings_amount,
#                     'source': 'auto_save',
#                     'income_ref': income_amount
#                 })
                
#                 st.sidebar.success(f"✅ Saved! Auto-saved ₹{savings_amount:.0f}")
#                 st.rerun()
    
#     elif entry_type == "💸 Expense":
#         with st.sidebar.form("expense_form"):
#             exp_date = st.date_input("Date", datetime.now())
#             exp_amount = st.number_input("Amount (₹)", min_value=0, value=100, step=10)
#             exp_category = st.selectbox("Category", [
#                 "food", "fuel", "phone", "rent", "entertainment", 
#                 "family_support", "medical", "shopping", "other"
#             ])
#             exp_desc = st.text_input("Description", placeholder="e.g., Lunch")
            
#             if st.form_submit_button("💾 Save Expense", use_container_width=True):
#                 storage.add_expense(user_id, {
#                     'date': exp_date.strftime('%Y-%m-%d'),
#                     'amount': exp_amount,
#                     'category': exp_category,
#                     'description': exp_desc
#                 })
#                 st.sidebar.success("✅ Expense saved!")
#                 st.rerun()
    
#     else:  # New Goal
#         with st.sidebar.form("goal_form"):
#             new_goal = st.text_input("Goal Description", placeholder="e.g., Save ₹50,000 for bike")
            
#             if st.form_submit_button("🎯 Add Goal", use_container_width=True):
#                 current_goals = storage.get_goals(user_id)
#                 goals_text = [g['description'] if isinstance(g, dict) else g for g in current_goals]
#                 goals_text.append(new_goal)
#                 storage.set_goals(user_id, goals_text)
#                 st.sidebar.success("✅ Goal added!")
#                 st.rerun()


# def show_main_app():
#     """Main application"""
#     user_id = st.session_state.user_id
    
#     # Initialize
#     if 'orchestrator' not in st.session_state:
#         with st.spinner("🔧 Loading your data..."):
#             profile, income_df, spending_df, orchestrator = initialize_app()
#             st.session_state.profile = profile
#             st.session_state.income_data = income_df
#             st.session_state.spending_data = spending_df
#             st.session_state.orchestrator = orchestrator
#             st.session_state.savings_rate = profile.get('savings_rate', 0.05)
#             st.session_state.daily_report = None
#             st.session_state.chat_history = []
    
#     profile = st.session_state.profile
#     orchestrator = st.session_state.orchestrator
    
#     # Header
#     st.markdown('<p class="main-header">🌦️ StormGuard India</p>', unsafe_allow_html=True)
#     st.markdown("<h4 style='text-align: center; color: gray;'>AI-Powered Financial Weather System for Gig Workers</h4>", unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={profile['name']}", width=120)
#         st.markdown(f"### 👋 {profile['name']}")
#         st.markdown(f"📍 {profile.get('city', 'Unknown')}")
#         st.markdown(f"🚚 {profile.get('platform', 'Delivery Partner')}")
        
#         # Quick Stats
#         income_summary = storage.get_income_summary(user_id, 30)
#         total_savings = storage.get_total_savings(user_id)
        
#         st.markdown("---")
#         st.markdown("### 📊 Last 30 Days")
#         st.metric("Total Income", f"₹{income_summary['total_income']:,.0f}")
#         st.metric("Daily Average", f"₹{income_summary['avg_daily']:,.0f}")
#         st.metric("Total Saved", f"₹{total_savings:,.0f}")
        
#         # Daily Check Button
#         st.markdown("---")
#         if st.button("🔄 Run Daily Check", type="primary", use_container_width=True):
#             with st.spinner("🔮 Analyzing... (15-20 sec)"):
#                 st.session_state.daily_report = orchestrator.run_daily_check()
#             st.success("✅ Analysis complete!")
#             st.rerun()
        
#         # Data Entry
#         show_data_entry_sidebar(user_id, profile)
        
#         # Logout
#         st.markdown("---")
#         if st.button("🚪 Switch User", use_container_width=True):
#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]
#             st.rerun()
    
#     # Main Content Tabs
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
#         "📊 Dashboard", "💬 AI Coach", "📈 My Data", "🎯 Goals", "⚙️ Settings"
#     ])
    
#     # TAB 1: DASHBOARD
#     with tab1:
#         if st.session_state.daily_report is None:
#             st.info("👆 Click **'Run Daily Check'** to see your financial forecast!")
            
#             # Show recent income chart
#             st.markdown("### 📈 Your Recent Income")
#             income_df = st.session_state.income_data
#             if not income_df.empty:
#                 recent = income_df.tail(30)
#                 fig = px.line(recent, x='date', y='income', title='Last 30 Days Income')
#                 fig.update_traces(line_color='#1f77b4', line_width=3)
#                 st.plotly_chart(fig, use_container_width=True)
#         else:
#             report = st.session_state.daily_report
#             dash = report['dashboard']
            
#             # Health Score
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 score = dash['summary']['financial_health_score']
#                 emoji = "💚" if score >= 75 else "💛" if score >= 50 else "🔴"
#                 st.metric("Health Score", f"{emoji} {score}/100")
#             with col2:
#                 st.metric("Weekly Forecast", f"₹{dash['summary']['weekly_income_forecast']:,.0f}")
#             with col3:
#                 st.metric("Savings Rate", f"{dash['summary']['savings_rate']:.1f}%")
#             with col4:
#                 st.metric("Risk Level", dash['risks']['level'])
            
#             st.markdown("---")
            
#             # Coaching
#             st.markdown("### 💬 Today's Advice")
#             st.success(report['coaching'])
            
#             # Alerts
#             if report['interventions']:
#                 st.markdown("### ⚠️ Alerts")
#                 for alert in report['interventions']:
#                     if alert['severity'] == 'HIGH':
#                         st.error(f"🔴 {alert['category']}: {alert['message'][:200]}...")
#                     elif alert['severity'] == 'MEDIUM':
#                         st.warning(f"🟡 {alert['category']}: {alert['message'][:200]}...")
#                     else:
#                         st.info(f"🟢 {alert['category']}: {alert['message'][:200]}...")
    
#     # TAB 2: AI COACH
#     with tab2:
#         st.markdown("### 💬 Chat with Your AI Coach")
        
#         # Chat history
#         for chat in st.session_state.get('chat_history', []):
#             with st.chat_message("user"):
#                 st.markdown(chat['question'])
#             with st.chat_message("assistant"):
#                 st.markdown(chat['answer'])
        
#         # Chat input
#         user_q = st.chat_input("Ask anything... (e.g., 'Should I work Sunday?')")
#         if user_q:
#             with st.chat_message("user"):
#                 st.markdown(user_q)
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     response = orchestrator.chat(user_q)
#                 st.markdown(response)
            
#             st.session_state.chat_history.append({'question': user_q, 'answer': response})
    
#     # TAB 3: MY DATA
#     with tab3:
#         st.markdown("### 📈 Your Financial Data")
        
#         data_view = st.radio("View:", ["Income History", "Spending History", "Savings"], horizontal=True)
        
#         if data_view == "Income History":
#             income_df = storage.get_income_history(user_id, 90)
#             if not income_df.empty:
#                 st.dataframe(income_df.tail(30), use_container_width=True)
                
#                 fig = px.line(income_df, x='date', y='income', title='Income Over Time')
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("No income data yet. Add your first entry!")
        
#         elif data_view == "Spending History":
#             spending_df = storage.get_spending_history(user_id, 30)
#             if not spending_df.empty:
#                 summary = storage.get_spending_summary(user_id, 30)
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.metric("Total Spent", f"₹{summary['total_spent']:,.0f}")
#                 with col2:
#                     st.metric("Daily Average", f"₹{summary['daily_average']:,.0f}")
                
#                 # Category breakdown
#                 fig = px.pie(
#                     values=list(summary['by_category'].values()),
#                     names=list(summary['by_category'].keys()),
#                     title='Spending by Category'
#                 )
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.info("No spending data yet.")
        
#         else:  # Savings
#             total = storage.get_total_savings(user_id)
#             st.metric("Total Saved", f"₹{total:,.0f}")
            
#             savings_df = storage.get_savings_history(user_id, 90)
#             if not savings_df.empty:
#                 savings_df['cumulative'] = savings_df['amount'].cumsum()
#                 fig = px.area(savings_df, x='date', y='cumulative', title='Savings Growth')
#                 st.plotly_chart(fig, use_container_width=True)
    
#     # TAB 4: GOALS
#     with tab4:
#         st.markdown("### 🎯 Your Goals")
        
#         goals = storage.get_goals(user_id)
#         total_savings = storage.get_total_savings(user_id)
        
#         for i, goal in enumerate(goals):
#             desc = goal['description'] if isinstance(goal, dict) else goal
#             target = goal.get('target_amount', 0) if isinstance(goal, dict) else storage._extract_amount(goal)
            
#             if target > 0:
#                 progress = min((total_savings / target) * 100, 100)
#                 st.markdown(f"**{desc}**")
#                 st.progress(progress / 100)
#                 st.markdown(f"₹{total_savings:,.0f} / ₹{target:,} ({progress:.1f}%)")
#             else:
#                 st.markdown(f"**{desc}**")
#             st.markdown("")
    
#     # TAB 5: SETTINGS
#     with tab5:
#         st.markdown("### ⚙️ Settings")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown("#### 💰 Savings Rate")
#             new_rate = st.slider(
#                 "Auto-save percentage",
#                 min_value=1, max_value=20,
#                 value=int(st.session_state.savings_rate * 100)
#             )
            
#             if st.button("Update Savings Rate"):
#                 storage.update_user(user_id, {'savings_rate': new_rate / 100})
#                 st.session_state.savings_rate = new_rate / 100
#                 orchestrator.adjust_savings_rate(new_rate / 100)
#                 st.success(f"✅ Updated to {new_rate}%")
        
#         with col2:
#             st.markdown("#### 👤 Profile")
#             profile = storage.get_user(user_id)
#             st.write(f"**Name:** {profile['name']}")
#             st.write(f"**City:** {profile.get('city', 'N/A')}")
#             st.write(f"**Platform:** {profile.get('platform', 'N/A')}")
#             st.write(f"**Member since:** {profile.get('created_at', 'N/A')[:10]}")


# # ==================== MAIN ====================

# def main():
#     # Check if user is logged in
#     if 'onboarding_complete' not in st.session_state or not st.session_state.onboarding_complete:
#         show_onboarding()
#     else:
#         show_main_app()

# if __name__ == "__main__":
#     main()


import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sys
import os
import time
import json
from datetime import datetime, timedelta

# --- 1. PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# --- 2. LOCAL IMPORTS ---
try:
    from data.storage import UserStorage
    from data.simulator import GigWorkerSimulator
    from agents.orchestrator_agent import OrchestratorAgent
except ModuleNotFoundError as e:
    st.error(f"System Error: {e}")
    st.stop()

# --- 3. CRASH FIX: SAFE ORCHESTRATOR ---
class SafeOrchestrator(OrchestratorAgent):
    def run_daily_check(self):
        """Patched run_daily_check to handle NoneType errors."""
        # 1. Forecast
        forecast_report = self.weather_agent.generate_complete_forecast(7)
        # 2. Spending
        spending_patterns = self.coach_agent.analyze_spending_patterns()
        # 3. Coaching
        coaching_advice = self.coach_agent.coach_on_forecast(forecast_report)
        if coaching_advice is None: 
            coaching_advice = "System update: Financial data processed. Advice currently unavailable."
        # 4. Analysis
        spending_analysis = self.coach_agent.analyze_spending_vs_income(forecast_report, spending_patterns)
        if spending_analysis is None: spending_analysis = "Analysis pending."
        # 5. Interventions
        interventions = self._check_and_prioritize_interventions(forecast_report, spending_patterns)
        # 6. Savings
        savings_plan = self.coach_agent.generate_savings_recommendation(forecast_report, spending_patterns)
        if savings_plan is None: savings_plan = "Savings plan pending."
        # 7. Scout & Savings
        opportunities = self.scout_agent.scan_real_time_opportunities()
        savings_summary = self.savings_agent.get_savings_summary(30)
        savings_recommendation = self.savings_agent.smart_savings_recommendation(forecast_report, spending_patterns)
        # 8. Dashboard
        dashboard = self._create_dashboard_summary(forecast_report, spending_patterns, interventions)
        
        return {
            'forecast': forecast_report,
            'spending': spending_patterns,
            'coaching': coaching_advice,
            'spending_analysis': spending_analysis,
            'interventions': interventions,
            'savings_plan': savings_plan,
            'dashboard': dashboard,
            'opportunities': opportunities,
            'savings_summary': savings_summary,
            'savings_recommendation': savings_recommendation,
            'opportunity_plan': self.scout_agent.generate_daily_opportunity_plan(),
            'metadata': {'user_id': self.user_id, 'patched': True}
        }

# --- CONFIGURATION ---
st.set_page_config(
    page_title="StromGuard | AI Financial Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE STORAGE ---
storage = UserStorage()

# --- THEME COLORS ---
THEME = {
    "bg_dark": "#0B0E14",        # Deepest Navy
    "bg_card": "rgba(20, 25, 40, 0.75)", # Glassy Dark
    "primary": "#00F0FF",        # Neon Cyan
    "secondary": "#7000FF",      # Electric Purple
    "accent": "#00FFA3",         # Neon Green
    "text_main": "#FFFFFF",      # Pure White
    "text_sub": "#A0AEC0"        # Cool Grey
}

# --- CSS & ANIMATIONS ---
def inject_custom_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Outfit', sans-serif;
            color: {THEME['text_main']};
            background-color: {THEME['bg_dark']};
        }}
        
        /* SCROLLBAR */
        ::-webkit-scrollbar {{ width: 8px; background: {THEME['bg_dark']}; }}
        ::-webkit-scrollbar-thumb {{ background: {THEME['bg_card']}; border-radius: 4px; }}

        /* HEADERS */
        h1, h2, h3 {{
            font-weight: 800 !important;
            letter-spacing: -0.5px;
            background: linear-gradient(120deg, #fff, {THEME['primary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        /* BACKGROUND */
        .stApp {{
            background-image: 
                radial-gradient(circle at 0% 0%, rgba(112, 0, 255, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 100% 100%, rgba(0, 240, 255, 0.1) 0%, transparent 40%),
                url('https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2832&auto=format&fit=crop'); 
            background-size: cover;
            background-attachment: fixed;
        }}

        /* SIDEBAR */
        section[data-testid="stSidebar"] {{
            background-color: rgba(11, 14, 20, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}

        /* SIDEBAR NAVIGATION */
        div[data-testid="stRadio"] > label {{ display: none; }}
        div[data-testid="stRadio"] label {{
            background: transparent;
            padding: 12px 20px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            cursor: pointer;
            transition: all 0.3s;
            color: {THEME['text_sub']};
            font-weight: 500;
        }}
        div[data-testid="stRadio"] label:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: white;
            border-color: {THEME['primary']};
        }}
        div[data-testid="stRadio"] label[data-baseweb="radio"] {{
            background: linear-gradient(90deg, rgba(0, 240, 255, 0.15), transparent);
            border-left: 4px solid {THEME['primary']};
            color: white;
            font-weight: 700;
        }}

        /* GLASS CARDS */
        .glass-card {{
            background: {THEME['bg_card']};
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.3);
        }}

        /* BUTTONS */
        .stButton > button {{
            background: linear-gradient(135deg, {THEME['primary']} 0%, #0099FF 100%);
            color: #0B0E14;
            border: none;
            padding: 12px 20px;
            font-weight: 700;
            border-radius: 8px;
            width: 100%;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 15px {THEME['primary']};
        }}
        
        /* FUNKY ANIMATION: CYBER KINETIC CORE (GYROSCOPE) */
        .kinetic-core {{
            position: relative;
            width: 250px;
            height: 250px;
            margin: 0 auto;
            transform-style: preserve-3d;
            animation: float-core 6s ease-in-out infinite;
        }}
        
        .k-ring {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            border: 3px solid transparent;
            border-top: 3px solid {THEME['primary']};
            border-bottom: 3px solid {THEME['secondary']};
            border-radius: 50%;
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
        }}
        
        .k-ring:nth-child(1) {{ animation: rotate-x 3s linear infinite; }}
        .k-ring:nth-child(2) {{ 
            width: 80%; height: 80%; top: 10%; left: 10%; 
            border-color: transparent;
            border-left: 4px solid {THEME['accent']}; 
            border-right: 4px solid {THEME['accent']};
            animation: rotate-y 5s linear infinite; 
        }}
        .k-ring:nth-child(3) {{ 
            width: 60%; height: 60%; top: 20%; left: 20%; 
            border-color: transparent;
            border-top: 4px solid {THEME['primary']};
            animation: rotate-z 7s linear infinite; 
        }}
        
        .k-orb {{
            position: absolute;
            top: 35%; left: 35%;
            width: 30%; height: 30%;
            background: radial-gradient(circle, {THEME['primary']}, transparent);
            border-radius: 50%;
            animation: pulse-core 2s ease-in-out infinite;
            filter: blur(5px);
        }}

        @keyframes rotate-x {{ 0% {{ transform: rotateX(0deg); }} 100% {{ transform: rotateX(360deg); }} }}
        @keyframes rotate-y {{ 0% {{ transform: rotateY(0deg); }} 100% {{ transform: rotateY(360deg); }} }}
        @keyframes rotate-z {{ 0% {{ transform: rotateZ(0deg); }} 100% {{ transform: rotateZ(360deg); }} }}
        @keyframes pulse-core {{ 0%, 100% {{ opacity: 0.5; transform: scale(0.8); }} 50% {{ opacity: 1; transform: scale(1.2); }} }}
        @keyframes float-core {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}

        /* --- LOADING OVERLAY: ROTATING SHIELD --- */
        .loading-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(8, 10, 16, 0.95);
            backdrop-filter: blur(25px);
            z-index: 999999; /* Highest priority */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .shield-container {{
            position: relative;
            width: 180px;
            height: 180px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        /* The Shield Icon */
        .shield-icon-main {{
            font-size: 5rem;
            z-index: 10;
            animation: shield-breath 2s infinite ease-in-out;
            filter: drop-shadow(0 0 20px {THEME['primary']});
        }}
        
        /* Outer Rotating Ring */
        .shield-ring-outer {{
            position: absolute;
            width: 100%; height: 100%;
            border: 4px solid transparent;
            border-top: 4px solid {THEME['primary']};
            border-bottom: 4px solid {THEME['primary']};
            border-radius: 50%;
            animation: spin-cw 2s linear infinite;
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.1);
        }}
        
        /* Inner Rotating Ring */
        .shield-ring-inner {{
            position: absolute;
            width: 70%; height: 70%;
            border: 4px solid transparent;
            border-left: 4px solid {THEME['secondary']};
            border-right: 4px solid {THEME['secondary']};
            border-radius: 50%;
            animation: spin-ccw 1.5s linear infinite;
        }}
        
        .loading-text {{
            margin-top: 40px;
            font-family: 'Outfit', sans-serif;
            letter-spacing: 6px;
            color: {THEME['text_main']};
            font-size: 1.2rem;
            font-weight: 600;
            text-transform: uppercase;
            animation: text-flicker 3s infinite;
        }}
        
        @keyframes spin-cw {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        @keyframes spin-ccw {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(-360deg); }} }}
        @keyframes shield-breath {{ 0%, 100% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.1); opacity: 1; }} }}
        @keyframes text-flicker {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
        
        /* DASHBOARD HEADER */
        .dashboard-header {{
            text-align: center;
            margin-bottom: 40px;
        }}
    </style>
    """, unsafe_allow_html=True)

def apply_neon_theme(fig):
    """Apply neon theme to Plotly charts with distinct background"""
    fig.update_layout(
        font={'family': 'Outfit, sans-serif', 'color': '#A0AEC0', 'size': 12},
        # Distinct Card Background for Charts
        paper_bgcolor='rgba(15, 20, 30, 0.8)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
        hoverlabel=dict(
            bgcolor="#0B0E14",
            bordercolor=THEME['primary'],
            font=dict(color='white')
        )
    )
    return fig

# --- HELPER FUNCTIONS ---

def simulate_loading(message="LOADING...", duration=0.5, auto_clear=True):
    """
    Renders a full-screen shield rotation animation overlay.
    """
    placeholder = st.empty()
    placeholder.markdown(f"""
        <div class="loading-overlay">
            <div class="shield-container">
                <div class="shield-ring-outer"></div>
                <div class="shield-ring-inner"></div>
                <div class="shield-icon-main">🛡️</div>
            </div>
            <div class="loading-text">{message}</div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(duration)
    if auto_clear:
        placeholder.empty()
    return placeholder

@st.cache_resource
def get_orchestrator(_profile, _income_df, _spending_df):
    """Return the SafeOrchestrator instance to prevent crashes"""
    return SafeOrchestrator(_profile, _income_df, _spending_df)

def load_user_session(user_id):
    profile, income_df, spending_df = storage.get_data_for_agents(user_id)
    
    if income_df.empty:
        simulator = GigWorkerSimulator(profile['name'], profile['city'])
        income_df = simulator.generate_income_history(90)
        spending_df = simulator.generate_spending_data(30)
        for _, row in income_df.iterrows():
            storage.add_income(user_id, row.to_dict())
        for _, row in spending_df.iterrows():
            storage.add_expense(user_id, row.to_dict())
            
    st.session_state.profile = profile
    st.session_state.income_data = income_df
    st.session_state.spending_data = spending_df
    st.session_state.orchestrator = get_orchestrator(profile, income_df, spending_df)
    st.session_state.user_id = user_id
    
    goals_path = storage.base_dir / user_id / "goals.json"
    if goals_path.exists():
        with open(goals_path, 'r', encoding='utf-8') as f:
            st.session_state.goals = json.load(f)
    else:
        st.session_state.goals = []

# --- SIDEBAR DATA ENTRY ---
def show_data_entry_sidebar(user_id, profile):
    """Sidebar with data entry forms"""
    st.sidebar.markdown("### ⚡ Quick Fixes")
    
    with st.sidebar.expander("💰 Add Income", expanded=False):
        with st.form("income_form"):
            income_date = st.date_input("Date", datetime.now())
            income_amount = st.number_input("Income (₹)", min_value=0, value=500, step=50)
            hours_worked = st.number_input("Hours", min_value=1, max_value=16, value=8)
            platform = st.selectbox("Platform", profile.get('platforms', ['Swiggy', 'Zomato']))
            
            if st.form_submit_button("Save Income"):
                storage.add_income(user_id, {
                    'date': income_date.strftime('%Y-%m-%d'),
                    'income': income_amount,
                    'hours_worked': hours_worked,
                    'platform': platform,
                    'is_weekend': income_date.weekday() >= 5
                })
                savings_rate = profile.get('savings_rate', 0.05)
                savings_amount = income_amount * savings_rate
                if hasattr(storage, 'add_savings'):
                      storage.add_savings(user_id, {
                        'date': income_date.strftime('%Y-%m-%d'),
                        'amount': savings_amount,
                        'source': 'auto_save'
                    })
                st.success(f"Saved! +₹{savings_amount:.0f} to savings")
                st.rerun()

    with st.sidebar.expander("💸 Add Expense", expanded=False):
        with st.form("expense_form"):
            exp_date = st.date_input("Date", datetime.now())
            exp_amount = st.number_input("Amount (₹)", min_value=0, value=100)
            exp_category = st.selectbox("Category", ["food", "fuel", "rent", "entertainment", "other"])
            
            if st.form_submit_button("Save Expense"):
                storage.add_expense(user_id, {
                    'date': exp_date.strftime('%Y-%m-%d'),
                    'amount': exp_amount,
                    'category': exp_category
                })
                st.success("Expense saved!")
                st.rerun()

# --- PAGE RENDERERS ---

def render_dashboard_landing():
    """Displayed immediately after login, before syncing"""
    
    # 1. Logo and Title at Top Center
    st.markdown(f"""
        <div class="dashboard-header">
            <div style="font-size: 5rem; margin-bottom: 10px;">🛡️</div>
            <h1 style="font-size: 4rem !important; margin: 0; text-shadow: 0 0 40px {THEME['primary']};">STROMGUARD</h1>
            <p style="color: {THEME['text_sub']}; letter-spacing: 5px; font-weight:300;">FINANCIAL PROTECTION SYSTEM</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Funky Animation (Kinetic Core) in Middle
    st.markdown(f"""
        <div class="kinetic-core">
            <div class="k-ring"></div>
            <div class="k-ring"></div>
            <div class="k-ring"></div>
            <div class="k-orb"></div>
        </div>
        <div style="height: 60px;"></div>
    """, unsafe_allow_html=True)
    
    # 3. Sync Button Below Animation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("INITIALIZE SYNC ⚡", use_container_width=True):
            # Trigger the full-screen shield loader
            simulate_loading(message="ANALYSING...", duration=0.5, auto_clear=False)
            st.session_state.daily_report = st.session_state.orchestrator.run_daily_check()
            st.rerun()

def render_forecast_page(report):
    st.markdown("<h2>🔮 FINANCIAL FORECAST</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.8, 1])
    
    with col1:
        if report:
            df_forecast = pd.DataFrame(report['forecast']['predictions']['predictions'])
            
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 7-Day Income Projection")
            
            fig = px.bar(
                df_forecast, 
                x='day_name', 
                y='predicted_income',
                text='predicted_income',
                color='predicted_income',
                color_continuous_scale=[THEME['bg_dark'], THEME['primary']]
            )
            fig.update_traces(texttemplate='₹%{text:.0s}', textposition='outside', marker_line_width=0, opacity=0.9)
            fig.update_layout(height=350, coloraxis_showscale=False, yaxis_title=None, xaxis_title=None)
            st.plotly_chart(apply_neon_theme(fig), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='glass-card' style='display:flex; align-items:center; justify-content:space-between; background: linear-gradient(90deg, rgba(0,240,255,0.1), transparent);'>
                    <div>
                        <div class='metric-label'>7-Day Prediction</div>
                        <div class='metric-value'>₹{report['dashboard']['summary']['weekly_income_forecast']:,}</div>
                    </div>
                    <div style='text-align:right'>
                        <div class='metric-label'>Confidence</div>
                        <div style='font-size:2rem; font-weight:800; color:{THEME['accent']}'>94%</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ⚠️ THREAT DETECTION")
        if report:
            alerts = report.get('interventions', [])
            if not alerts:
                 st.markdown(f"""
                    <div class='glass-card' style='text-align:center; padding:40px;'>
                        <div style='font-size:3rem;'>🛡️</div>
                        <h3 style='color:{THEME['accent']}'>SYSTEM SECURE</h3>
                        <p style='color:{THEME['text_sub']}'>No active financial threats.</p>
                    </div>
                 """, unsafe_allow_html=True)
            
            for alert in alerts:
                sev = alert['severity']
                color = "#FF003C" if sev == 'HIGH' else "#FFB800" if sev == 'MEDIUM' else "#00F0FF"
                
                st.markdown(f"""
                <div class='glass-card' style='border-left: 4px solid {color}; padding: 20px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:5px;'>
                        <strong style='color:{color}; letter-spacing:1px; font-size:0.9rem;'>{alert['category']}</strong>
                        <span style='background:{color}; color:black; font-weight:bold; font-size:0.7rem; padding:2px 8px; border-radius:4px;'>{sev}</span>
                    </div>
                    <p style='color:white; font-size:1.1rem; line-height:1.4;'>{alert['message']}</p>
                </div>
                """, unsafe_allow_html=True)

def render_ai_coach_page():
    st.markdown("<h2>🧠 AI COACH</h2>", unsafe_allow_html=True)
    
    chat_container = st.container()
    
    with chat_container:
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = [{"question": None, "answer": f"Identity Verified: {st.session_state.profile['name']}. Ready for commands."}]
        
        for chat in st.session_state.chat_history:
            if chat['question']:
                st.markdown(f"""
                    <div style='display:flex; justify-content:flex-end; margin-bottom:15px;'>
                        <div style='background:rgba(255,255,255,0.05); padding:15px 25px; border-radius:20px 20px 0 20px; font-size:1.1rem;'>
                            {chat['question']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style='display:flex; justify-content:flex-start; margin-bottom:25px;'>
                    <div style='background:linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(112, 0, 255, 0.15)); padding:20px; border-radius:20px 20px 20px 0; border:1px solid {THEME['primary']}; box-shadow: 0 0 20px rgba(0,240,255,0.1); max-width:85%;'>
                        <div style='color:{THEME['primary']}; font-size:0.8rem; font-weight:700; margin-bottom:8px;'>STROMGUARD AI</div>
                        <div style='font-size:1.1rem; line-height:1.5;'>{chat['answer']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with st.form("ai_chat", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input("Input", placeholder="Enter command...", label_visibility="collapsed")
        with col2:
            submit = st.form_submit_button("SEND")
        
        if submit and user_input:
            orchestrator = st.session_state.orchestrator
            simulate_loading(message="PROCESSING QUERY...", auto_clear=True)
            response = orchestrator.chat(user_input)
            st.session_state.chat_history.append({"question": user_input, "answer": response})
            st.rerun()

def render_trends_page():
    st.markdown("<h2>📈 FINANCIAL STATS</h2>", unsafe_allow_html=True)
    
    income_df = st.session_state.income_data
    spending_df = st.session_state.spending_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""<div class='glass-card'><h3 style='margin-top:0'>Income Velocity</h3>""", unsafe_allow_html=True)
        if not income_df.empty:
            fig = px.area(income_df.sort_values('date'), x='date', y='income', color_discrete_sequence=[THEME['accent']])
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(apply_neon_theme(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""<div class='glass-card'><h3 style='margin-top:0'>Expense Distribution</h3>""", unsafe_allow_html=True)
        if not spending_df.empty:
            fig = px.pie(spending_df, names='category', values='amount', hole=0.6, color_discrete_sequence=px.colors.sequential.Bluyl)
            fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(apply_neon_theme(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_goals_page():
    st.markdown("<h2>🎯 GOALS</h2>", unsafe_allow_html=True)
    goals = st.session_state.get('goals', [])
    
    with st.expander("➕ INITIATE NEW TARGET"):
        with st.form("new_goal"):
            g_name = st.text_input("Target Name")
            g_amount = st.number_input("Target Amount (₹)", 1000)
            if st.form_submit_button("LOCK TARGET"):
                new_goal = {"name": g_name, "target_amount": g_amount, "current_amount": 0}
                goals.append(new_goal)
                st.session_state.goals = goals
                st.success("Target Locked")
                st.rerun()
                
    if not goals:
        st.info("No active targets.")
        
    for goal in goals:
        if isinstance(goal, str):
            g_name, target, current = goal, 1000, 0
        else:
            g_name = goal.get('name', goal.get('description', 'Unknown'))
            target = goal.get('target_amount', 1000)
            current = goal.get('current_amount', 0)
            
        progress = min(current / target, 1.0) if target > 0 else 0
        
        st.markdown(f"""
        <div class='glass-card'>
            <div style='display:flex; justify-content:space-between; margin-bottom:15px;'>
                <span style='font-size:1.5rem; font-weight:700;'>{g_name}</span>
                <span style='color:{THEME['primary']}; font-size:1.2rem; font-weight:600;'>₹{current:,} / ₹{target:,}</span>
            </div>
            <div style='background:rgba(255,255,255,0.1); height:12px; border-radius:6px; overflow:hidden;'>
                <div style='background:linear-gradient(90deg, {THEME['primary']}, {THEME['secondary']}); width:{progress*100}%; height:100%;'></div>
            </div>
            <div style='text-align:right; font-size:0.9rem; color:{THEME['text_sub']}; margin-top:8px;'>
                {int(progress*100)}% COMPLETE
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_settings_page():
    st.markdown("<h2>⚙️ SETTINGS</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Operator Name", value=st.session_state.profile.get('name', ''))
        st.selectbox("Region", ["Bangalore", "Mumbai", "Delhi"])
    with c2:
        st.toggle("Holographic Mode", value=True)
        st.toggle("Voice Synthesis", value=False)
    if st.button("TERMINATE SESSION (LOGOUT)"):
        st.session_state.clear()
        st.session_state.page = "landing"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
def render_dashboard():
    with st.sidebar:
        st.markdown("""
            <div style='text-align:center; padding:10px 0;'>
                <h1 style='font-size:2rem; margin:0; color:#00F0FF; text-shadow:0 0 10px rgba(0,240,255,0.5);'> StromGuard 🛡️ </h1>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='text-align:center; margin-bottom:20px;'>
                <div style='width:80px; height:80px; background:linear-gradient(135deg, {THEME['primary']}, {THEME['secondary']}); border-radius:50%; margin:0 auto 10px auto; display:flex; align-items:center; justify-content:center; font-size:2rem; font-weight:bold; color:black;'>{st.session_state.profile['name'][0]}</div>
                <h3 style='margin:5px 0 0 0; font-size:1.2rem;'>{st.session_state.profile['name']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🧭 Navigation")
        nav = st.radio("NAV", ["Forecast", "AI Coach", "Financial Stats", "Goals", "Settings"], label_visibility="collapsed")
        
        st.markdown("---")
        show_data_entry_sidebar(st.session_state.user_id, st.session_state.profile)

    if nav == "Forecast":
        if 'daily_report' not in st.session_state or st.session_state.daily_report is None:
            render_dashboard_landing()
        else:
            render_forecast_page(st.session_state.daily_report)
            
    elif nav == "AI Coach":
        if st.session_state.get('last_page') != 'AI Coach': simulate_loading(auto_clear=True)
        render_ai_coach_page()
    elif nav == "Financial Stats":
        if st.session_state.get('last_page') != 'Financial Stats': simulate_loading(auto_clear=True)
        render_trends_page()
    elif nav == "Goals":
        if st.session_state.get('last_page') != 'Goals': simulate_loading(auto_clear=True)
        render_goals_page()
    elif nav == "Settings":
        if st.session_state.get('last_page') != 'Settings': simulate_loading(auto_clear=True)
        render_settings_page()
        
    st.session_state.last_page = nav

# --- APP ROUTER ---
def main():
    inject_custom_css()
    if 'page' not in st.session_state: st.session_state.page = "landing"
    
    if st.session_state.page == "landing":
        st.markdown("<div style='height:25vh'></div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style='text-align:center;'>
                <h1 style='font-size:5rem !important; margin-bottom:10px; display:inline-block; text-shadow: 0 0 30px {THEME["primary"]};'>STROMGUARD</h1>
                <p style='color:{THEME['text_sub']}; font-size:1.5rem; letter-spacing:4px;'>FINANCIAL SHIELD ACTIVE</p>
            </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
            if st.button("INITIALIZE SYSTEM", use_container_width=True):
                st.session_state.page = "user_selection"
                st.rerun()
                
    elif st.session_state.page == "user_selection":
        st.markdown("<h2 style='text-align:center; margin-top:50px;'>SELECT OPERATOR</h2>", unsafe_allow_html=True)
        users = storage.list_users()
        cols = st.columns(3)
        for i, user in enumerate(users):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='glass-card' style='text-align:center;'>
                    <h3>{user['name']}</h3>
                    <p style='color:{THEME['text_sub']}'>{user.get('city', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"ACCESS: {user['name']}", key=user['user_id']):
                    load_user_session(user['user_id'])
                    st.session_state.page = "dashboard"
                    st.rerun()
        
        with cols[len(users)%3]:
            st.markdown(f"<div class='glass-card' style='text-align:center; border:2px dashed {THEME['text_sub']}'><h3>+ NEW</h3></div>", unsafe_allow_html=True)
            if st.button("CREATE PROFILE"):
                nid = storage.create_user({"name": "New User", "city": "Bangalore"})
                load_user_session(nid)
                st.session_state.page = "dashboard"
                st.rerun()

    elif st.session_state.page == "dashboard":
        if 'user_id' not in st.session_state:
            st.session_state.page = "landing"
            st.rerun()
        render_dashboard()

if __name__ == "__main__":
    main()