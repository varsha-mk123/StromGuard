# tests/test_weather_agent.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.weather_forecast_agent import WeatherForecastAgent, print_forecast_report
from data.simulator import GigWorkerSimulator
from data.weather_api import WeatherAPI

def test_full_workflow():
    """Test complete weather agent workflow"""
    
    print("\n" + "="*80)
    print("🧪 COMPREHENSIVE WEATHER FORECAST AGENT TEST")
    print("="*80 + "\n")
    
    # Test 1: Data Generation
    print("TEST 1: Data Generation")
    print("-" * 80)
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    data = simulator.generate_income_history(90)
    assert len(data) == 90, "Should generate 90 days"
    assert 'income' in data.columns, "Should have income column"
    print("✅ PASSED: Generated 90 days of data")
    print(f"   Average income: ₹{data['income'].mean():.2f}/day")
    print(f"   Range: ₹{data['income'].min():.0f} - ₹{data['income'].max():.0f}\n")
    
    # Test 2: Weather API
    print("TEST 2: Weather API")
    print("-" * 80)
    weather = WeatherAPI()
    current = weather.get_current_weather()
    forecast = weather.get_forecast(7)
    
    # Updated assertion - should handle mock data too
    assert forecast is not None, "Should get forecast"
    assert len(forecast) >= 5, f"Should get at least 5 days, got {len(forecast)}"
    assert len(forecast) <= 7, f"Should get max 7 days, got {len(forecast)}"
    
    print("✅ PASSED: Weather API working")
    if current:
        print(f"   Current: {current['weather']}, {current['temperature']}°C")
    print(f"   Forecast: {len(forecast)} days retrieved")
    
    # Check forecast structure
    first_day = forecast[0]
    assert 'date' in first_day, "Should have date"
    assert 'weather' in first_day, "Should have weather"
    assert 'avg_temp' in first_day, "Should have temperature"
    print(f"   First day: {first_day['date']} - {first_day['weather']}\n")
    
    # Test 3: Agent Initialization
    print("TEST 3: Agent Initialization")
    print("-" * 80)
    agent = WeatherForecastAgent(data, user_id="test_001")
    assert agent.data is not None, "Should have data"
    assert agent.prophet_model is None, "Model not trained yet"
    print("✅ PASSED: Agent initialized successfully\n")
    
    # Test 4: Model Training
    print("TEST 4: Prophet Model Training")
    print("-" * 80)
    success = agent.train_prophet_model()
    assert success == True, "Model should train"
    assert agent.prophet_model is not None, "Model should exist"
    print("✅ PASSED: Prophet model trained\n")
    
    # Test 5: Income Prediction
    print("TEST 5: Income Prediction")
    print("-" * 80)
    predictions = agent.predict_income(7)
    assert 'predictions' in predictions, "Should have predictions"
    assert len(predictions['predictions']) == 7, f"Should predict 7 days, got {len(predictions['predictions'])}"
    assert 'weekly_total' in predictions, "Should have weekly total"
    assert predictions['weekly_total'] > 0, "Weekly total should be positive"
    print("✅ PASSED: Predictions generated")
    print(f"   Weekly forecast: ₹{predictions['weekly_total']:.2f}")
    print(f"   Daily average: ₹{predictions['daily_avg']:.2f}\n")
    
    # Test 6: Pattern Identification
    print("TEST 6: Pattern Identification")
    print("-" * 80)
    patterns = agent.identify_patterns()
    assert 'best_days' in patterns, "Should identify best days"
    assert 'efficiency_trend' in patterns, "Should calculate efficiency"
    assert 'volatility' in patterns, "Should calculate volatility"
    assert len(patterns['best_days']) > 0, "Should have at least one best day"
    print("✅ PASSED: Patterns identified")
    print(f"   Best day: {list(patterns['best_days'].keys())[0]}")
    print(f"   Efficiency: ₹{patterns['efficiency_trend']['current_per_hour']}/hour")
    print(f"   Volatility: {patterns['volatility']['risk_level']}\n")
    
    # Test 7: Risk Identification
    print("TEST 7: Risk Identification")
    print("-" * 80)
    risks = agent.identify_risks(predictions, upcoming_bills=14000)
    assert isinstance(risks, list), "Should return list of risks"
    print(f"✅ PASSED: Risk analysis complete")
    print(f"   Risks detected: {len(risks)}")
    if risks:
        severities = [r['severity'] for r in risks]
        print(f"   Severity levels: {', '.join(set(severities))}")
        print(f"   Risk types: {[r['type'] for r in risks]}")
    else:
        print(f"   No major risks detected")
    print()
    
    # Test 8: Complete Forecast (may be slow due to Ollama)
    print("TEST 8: Complete Forecast Generation (includes AI analysis)")
    print("-" * 80)
    print("⏳ This may take 5-10 seconds (Ollama generating AI insights)...\n")
    
    report = agent.generate_complete_forecast(7)
    assert 'predictions' in report, "Should have predictions"
    assert 'patterns' in report, "Should have patterns"
    assert 'risks' in report, "Should have risks"
    assert 'ai_analysis' in report, "Should have AI analysis"
    assert 'learning_stats' in report, "Should have learning stats"
    assert 'metadata' in report, "Should have metadata"
    print("✅ PASSED: Complete forecast generated")
    print(f"   AI analysis length: {len(report['ai_analysis'])} characters\n")
    
    # Test 9: Continuous Learning
    print("TEST 9: Continuous Learning")
    print("-" * 80)
    accuracy_1 = agent.calculate_prediction_accuracy(500, 520)
    accuracy_2 = agent.calculate_prediction_accuracy(600, 580)
    accuracy_3 = agent.calculate_prediction_accuracy(550, 540)
    assert len(agent.learning_history) == 3, "Should store 3 predictions"
    assert 'current_accuracy' in accuracy_3, "Should have accuracy metric"
    print("✅ PASSED: Learning mechanism working")
    print(f"   Predictions stored: {len(agent.learning_history)}")
    print(f"   Latest accuracy: {accuracy_3['current_accuracy']}%")
    print(f"   Rolling accuracy: {accuracy_3.get('rolling_7day_accuracy', 'N/A')}%\n")
    
    # Display Full Report
    print("\n" + "="*80)
    print("📊 FINAL FORECAST REPORT")
    print("="*80)
    print_forecast_report(report)
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED!")
    print("="*80 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        test_full_workflow()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise