# tests/test_financial_coach.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.financial_coach_agent import FinancialCoachAgent, print_coaching_session
from agents.weather_forecast_agent import WeatherForecastAgent
from data.simulator import GigWorkerSimulator

def test_financial_coach():
    """Test Financial Coach Agent"""
    
    print("\n" + "="*80)
    print("🧪 FINANCIAL COACH AGENT TEST")
    print("="*80 + "\n")
    
    # Setup
    print("📊 Setting up test data...")
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    income_data = simulator.generate_income_history(90)
    spending_data = simulator.generate_spending_data(30)
    
    user_profile = {
        'name': 'Rajesh',
        'city': 'Bangalore',
        'platform': 'Swiggy + Zomato',
        'language': 'hinglish',
        'goals': ['Save ₹20,000 for emergency', 'Buy bike']
    }
    
    # Get forecast
    weather_agent = WeatherForecastAgent(income_data)
    forecast = weather_agent.predict_income(7)
    forecast_full = {
        'predictions': forecast,
        'patterns': weather_agent.identify_patterns(),
        'risks': weather_agent.identify_risks(forecast)
    }
    
    print("✅ Test data ready\n")
    
    # Initialize coach
    coach = FinancialCoachAgent(user_profile, spending_data)
    print()
    
    # Test spending analysis
    print("TEST 1: Spending Analysis")
    print("-" * 80)
    patterns = coach.analyze_spending_patterns()
    assert 'total_spent' in patterns
    assert 'by_category' in patterns
    print(f"✅ PASSED")
    print(f"   Total: ₹{patterns['total_spent']}")
    print(f"   Categories: {len(patterns['by_category'])}\n")
    
    # Test coaching
    print("TEST 2: Forecast Coaching")
    print("-" * 80)
    coaching = coach.coach_on_forecast(forecast_full)
    assert len(coaching) > 50
    print(f"✅ PASSED")
    print(f"   Response length: {len(coaching)} chars\n")
    print_coaching_session(coaching)
    
    # Test proactive warning
    print("TEST 3: Proactive Warnings")
    print("-" * 80)
    warning = coach.generate_proactive_warning(
        'slow_week_ahead',
        {'forecast': forecast['weekly_total'], 'drop': '30%'}
    )
    assert len(warning) > 50
    print(f"✅ PASSED\n")
    print_coaching_session(warning)
    
    # Test chat
    print("TEST 4: Chat Interface")
    print("-" * 80)
    response = coach.chat("Should I work extra hours this week?")
    assert len(response) > 30
    print(f"✅ PASSED")
    print(f"   Conversation history: {len(coach.conversation_history)} messages\n")
    
    print("="*80)
    print("✅ ALL TESTS PASSED!")
    print("="*80 + "\n")


if __name__ == "__main__":
    test_financial_coach()