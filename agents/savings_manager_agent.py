# agents/savings_manager_agent.py
from phi.agent import Agent
from phi.model.google import Gemini
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SavingsManagerAgent:
    """
    Daily Savings Manager (Inspired by Pigmy Deposit Scheme)
    - Auto-saves 2-5% of daily/weekly earnings
    - User can adjust allocation dynamically
    - Tracks savings progress toward goals
    - Provides motivation and celebrates milestones
    - Smart allocation based on income variability
    """
    
    def __init__(self, user_id, user_goals, default_rate=0.03):
        self.user_id = user_id
        self.goals = user_goals
        self.savings_rate = default_rate  # Default 3%
        self.savings_history = []
        self.total_saved = 0
        self.goal_progress = {}
        
        # Initialize Phidata Agent
        self.agent = Agent(
            name="Savings Manager Agent",
            model=Gemini(id="gemini-2.0-flash"),
            instructions=[
                "You are a savings coach for gig workers in India.",
                "Help them save small amounts consistently (Pigmy-style).",
                "Be encouraging - even ₹20/day adds up to ₹7,300/year!",
                "Celebrate every milestone, no matter how small.",
                "Speak in Hinglish - simple and motivating.",
                "Focus on progress, not perfection.",
                "Make saving feel achievable and rewarding."
            ],
            markdown=True,
            show_tool_calls=False
        )
        
        print(f"✅ Savings Manager initialized - {int(self.savings_rate*100)}% auto-save rate")
    
    def process_daily_income(self, date, income_amount, platform="Swiggy"):
        """
        Process daily income and auto-save percentage
        """
        # Calculate savings amount
        savings_amount = income_amount * self.savings_rate
        
        # Save the amount
        savings_record = {
            'date': date,
            'income': income_amount,
            'savings_rate': self.savings_rate,
            'saved_amount': round(savings_amount, 2),
            'platform': platform,
            'timestamp': datetime.now().isoformat()
        }
        
        self.savings_history.append(savings_record)
        self.total_saved += savings_amount
        
        # Update goal progress
        self._update_goal_progress(savings_amount)
        
        return savings_record
    
    def adjust_savings_rate(self, new_rate, reason="User requested"):
        """
        Allow user to change savings rate (2-10%)
        """
        # Validate rate
        if new_rate < 0.02:
            return {
                'success': False,
                'message': "Minimum savings rate is 2% (₹20 per ₹1,000 earned)"
            }
        
        if new_rate > 0.10:
            return {
                'success': False,
                'message': "Maximum savings rate is 10% (₹100 per ₹1,000 earned)"
            }
        
        old_rate = self.savings_rate
        self.savings_rate = new_rate
        
        return {
            'success': True,
            'old_rate': f"{int(old_rate*100)}%",
            'new_rate': f"{int(new_rate*100)}%",
            'reason': reason,
            'message': f"Savings rate updated: {int(old_rate*100)}% → {int(new_rate*100)}%"
        }
    
    def smart_savings_recommendation(self, income_forecast, spending_patterns):
        """
        AI recommends optimal savings rate based on financial situation
        """
        predicted_income = income_forecast.get('weekly_total', 5000)
        avg_spending = spending_patterns.get('daily_average', 600) * 7
        
        surplus = predicted_income - avg_spending
        surplus_rate = (surplus / predicted_income) if predicted_income > 0 else 0
        
        # Recommend savings rate
        if surplus_rate >= 0.30:  # 30%+ surplus
            recommended_rate = 0.05  # Save 5%
            message = "You have good surplus! Increase to 5% savings."
        elif surplus_rate >= 0.15:  # 15-30% surplus
            recommended_rate = 0.04  # Save 4%
            message = "Decent surplus. 4% savings is optimal."
        elif surplus_rate >= 0.05:  # 5-15% surplus
            recommended_rate = 0.03  # Save 3%
            message = "Moderate surplus. Stick to 3% savings."
        elif surplus_rate > 0:  # Small surplus
            recommended_rate = 0.02  # Save 2%
            message = "Tight budget. 2% savings is safe."
        else:  # Deficit
            recommended_rate = 0.02  # Minimum
            message = "Challenging week. Save minimum 2% for future."
        
        context = f"""
Smart Savings Recommendation:

Current situation:
- Weekly income forecast: ₹{predicted_income:.0f}
- Weekly spending: ₹{avg_spending:.0f}
- Surplus: ₹{surplus:.0f} ({surplus_rate*100:.1f}%)
- Current savings rate: {int(self.savings_rate*100)}%
- Recommended rate: {int(recommended_rate*100)}%

Explain in Hinglish (under 100 words):
1. Why this rate makes sense for them
2. What they'll save per month at this rate
3. How it helps their goals
4. Encouragement

Be specific with numbers and realistic.
"""
        
        ai_recommendation = self.agent.run(context)
        
        return {
            'current_rate': self.savings_rate,
            'recommended_rate': recommended_rate,
            'monthly_savings_at_recommended': round(predicted_income * 4 * recommended_rate, 0),
            'reasoning': message,
            'ai_advice': ai_recommendation.content,
            'should_adjust': abs(recommended_rate - self.savings_rate) >= 0.01
        }
    
    def _update_goal_progress(self, amount_saved):
        """Update progress toward savings goals"""
        for goal in self.goals:
            if goal not in self.goal_progress:
                # Extract target amount from goal string
                # E.g., "Save ₹20,000 emergency fund" → 20000
                import re
                numbers = re.findall(r'₹?([\d,]+)', goal)
                if numbers:
                    target = int(numbers[0].replace(',', ''))
                    self.goal_progress[goal] = {
                        'target': target,
                        'saved': 0,
                        'progress_pct': 0
                    }
            
            if goal in self.goal_progress:
                self.goal_progress[goal]['saved'] += amount_saved
                self.goal_progress[goal]['progress_pct'] = (
                    self.goal_progress[goal]['saved'] / 
                    self.goal_progress[goal]['target']
                ) * 100
    
    def get_savings_summary(self, days=30):
        """Get savings summary for last N days"""
        if not self.savings_history:
            return {
                'total_saved': 0,
                'days_tracked': 0,
                'avg_daily_savings': 0,
                'consistency': 0,
                'current_rate': f"{int(self.savings_rate*100)}%",  # String format
                'current_rate_decimal': self.savings_rate,          # Decimal format (NEW)
                'projected_yearly': 0,
                'message': "Start saving today! Even ₹20/day = ₹7,300/year 💰"
            }
        
        recent = self.savings_history[-days:] if len(self.savings_history) > days else self.savings_history
        
        total_saved_period = sum([s['saved_amount'] for s in recent])
        days_saved = len(recent)
        avg_daily = total_saved_period / days_saved if days_saved > 0 else 0
        consistency = (days_saved / days) * 100 if days > 0 else 0
        
        return {
            'total_saved': round(self.total_saved, 2),
            'period_saved': round(total_saved_period, 2),
            'days_tracked': days_saved,
            'avg_daily_savings': round(avg_daily, 2),
            'consistency': round(consistency, 1),
            'current_rate': f"{int(self.savings_rate*100)}%",       # String
            'current_rate_decimal': self.savings_rate,               # Decimal (NEW)
            'projected_yearly': round(avg_daily * 365, 0)
        }
    
    def celebrate_milestone(self, milestone_amount):
        """Celebrate when reaching savings milestone"""
        
        context = f"""
🎉 MILESTONE ACHIEVED! User saved ₹{milestone_amount}!

This is their total savings so far.

Generate celebration message in Hinglish (under 80 words):
1. Congratulate specifically (mention ₹{milestone_amount})
2. Show what this means (X days of consistency)
3. Motivate for next milestone
4. Use celebrating emojis

Be genuinely excited and proud!
"""
        
        response = self.agent.run(context)
        return response.content
    
    def visualize_progress(self):
        """Create progress visualization data"""
        if not self.savings_history:
            return None
        
        df = pd.DataFrame(self.savings_history)
        
        # Cumulative savings over time
        df['cumulative_savings'] = df['saved_amount'].cumsum()
        
        # Weekly aggregates
        df['date'] = pd.to_datetime(df['date'])
        df['week'] = df['date'].dt.isocalendar().week
        weekly = df.groupby('week').agg({
            'saved_amount': 'sum',
            'income': 'sum'
        }).reset_index()
        
        return {
            'daily_savings': df[['date', 'saved_amount', 'cumulative_savings']].to_dict('records'),
            'weekly_savings': weekly.to_dict('records'),
            'goal_progress': self.goal_progress
        }
    
    def get_motivation_message(self):
        """Daily motivation for saving"""
        
        summary = self.get_savings_summary(30)
        
        context = f"""
Daily savings motivation for user:

Stats:
- Total saved so far: ₹{summary['total_saved']}
- Avg daily savings: ₹{summary['avg_daily_savings']:.0f}
- Consistency: {summary['consistency']:.0f}%
- Current rate: {summary['current_rate']}

Generate motivational message in Hinglish (under 70 words):
1. Acknowledge their consistency
2. Show compound effect ("₹20/day = ₹7,300/year")
3. Encourage them to keep going
4. Make it feel achievable

Be warm and encouraging!
"""
        
        response = self.agent.run(context)
        return response.content


# Utility functions
def print_savings_summary(summary):
    """Pretty print savings summary"""
    print("\n" + "="*70)
    print("💰 SAVINGS SUMMARY")
    print("="*70 + "\n")
    
    print(f"📊 Total Saved:        ₹{summary['total_saved']:,.0f}")
    print(f"📅 Days Tracked:       {summary['days_tracked']}")
    print(f"💵 Avg Daily Savings:  ₹{summary['avg_daily_savings']:.0f}")
    print(f"✅ Consistency:        {summary['consistency']:.1f}%")
    print(f"📈 Current Rate:       {summary['current_rate']}")
    print(f"🎯 Projected Yearly:   ₹{summary['projected_yearly']:,.0f}")
    print("\n" + "="*70 + "\n")


# Test function
if __name__ == "__main__":
    print("🧪 Testing Savings Manager Agent\n")
    
    # Initialize
    goals = ["Save ₹20,000 emergency fund", "Buy bike ₹60,000"]
    manager = SavingsManagerAgent("test_user", goals, default_rate=0.03)
    print()
    
    # Simulate 30 days of savings
    print("📊 Simulating 30 days of savings...")

