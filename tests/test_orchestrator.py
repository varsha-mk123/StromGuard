# tests/test_orchestrator.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator_agent import OrchestratorAgent, print_orchestrator_report
from data.simulator import GigWorkerSimulator

def test_orchestrator():
    """Comprehensive orchestrator test"""
    
    print("\n" + "="*80)
    print("🧪 ORCHESTRATOR AGENT COMPREHENSIVE TEST")
    print("="*80 + "\n")
    
    # Setup
    print("📊 Generating test data...")
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    income_data = simulator.generate_income_history(90)
    spending_data = simulator.generate_spending_data(30)
    
    user_profile = {
        'user_id': 'test_001',
        'name': 'Rajesh',
        'city': 'Bangalore',
        'platform': 'Swiggy + Zomato',
        'language': 'hinglish',
        'goals': ['Emergency fund ₹20K', 'Buy bike']
    }
    
    print("✅ Test data ready\n")
    
    # Test 1: Initialization
    print("TEST 1: Orchestrator Initialization")
    print("-" * 80)
    orchestrator = OrchestratorAgent(user_profile, income_data, spending_data)
    assert orchestrator.weather_agent is not None
    assert orchestrator.coach_agent is not None
    print("✅ PASSED: All sub-agents initialized\n")
    
    # Test 2: Daily Check (Full workflow)
    print("TEST 2: Daily Financial Health Check")
    print("-" * 80)
    print("⏳ This will take 10-15 seconds (running all agents)...\n")
    
    report = orchestrator.run_daily_check()
    
    assert 'forecast' in report
    assert 'spending' in report
    assert 'coaching' in report
    assert 'interventions' in report
    assert 'dashboard' in report
    
    print("✅ PASSED: Daily check completed successfully")
    print(f"   - Forecast: ₹{report['dashboard']['summary']['weekly_income_forecast']:.0f}")
    print(f"   - Health Score: {report['dashboard']['summary']['financial_health_score']}/100")
    print(f"   - Interventions: {len(report['interventions'])}")
    print(f"   - Risk Level: {report['dashboard']['risks']['level']}\n")
    
    # Test 3: Dashboard creation
    print("TEST 3: Dashboard Summary")
    print("-" * 80)
    dashboard = report['dashboard']
    assert 'summary' in dashboard
    assert 'income' in dashboard
    assert 'spending' in dashboard
    assert 'risks' in dashboard
    print("✅ PASSED: Dashboard created with all sections")
    print(f"   - Health Score: {dashboard['summary']['financial_health_score']}")
    print(f"   - Savings Rate: {dashboard['summary']['savings_rate']:.1f}%\n")
    
    # Test 4: Intervention prioritization
    print("TEST 4: Intervention Prioritization")
    print("-" * 80)
    interventions = report['interventions']
    if interventions:
        # Check priority ordering
        priorities = [i['priority'] for i in interventions]
        assert priorities == sorted(priorities), "Should be sorted by priority"
        print(f"✅ PASSED: {len(interventions)} interventions prioritized")
        for i, inter in enumerate(interventions, 1):
            print(f"   {i}. {inter['category']} (Priority: {inter['priority']}, Severity: {inter['severity']})")
    else:
        print("✅ PASSED: No interventions needed (healthy state)")
    print()
    
    # Test 5: Quick summary (faster)
    print("TEST 5: Quick Summary (No Full Check)")
    print("-" * 80)
    quick = orchestrator.get_quick_summary()
    assert 'weekly_forecast' in quick
    assert 'risk_level' in quick
    print("✅ PASSED: Quick summary generated")
    print(f"   - Weekly: ₹{quick['weekly_forecast']:.0f}")
    print(f"   - Risk: {quick['risk_level']}\n")
    
    # Test 6: Chat routing
    print("TEST 6: Chat Interface")
    print("-" * 80)
    test_questions = [
        "How much will I earn next week?",
        "Should I buy a new phone?",
        "How can I save more money?"
    ]
    
    for q in test_questions:
        response = orchestrator.chat(q)
        assert len(response) > 20, "Response should be substantial"
        print(f"✅ Q: {q}")
        print(f"   A: {response[:80]}...\n")
    
    # Test 7: Learning mechanism
    print("TEST 7: Intervention Tracking")
    print("-" * 80)
    effectiveness = orchestrator.track_intervention_effectiveness(
        'test_intervention_1',
        'followed',
        'positive'
    )
    assert effectiveness['total'] == 1
    assert effectiveness['followed'] == 1
    print("✅ PASSED: Learning mechanism working")
    print(f"   - Tracked: {effectiveness}\n")
    
    # Display full report
    print("\n" + "="*80)
    print("📊 COMPLETE FINANCIAL HEALTH REPORT")
    print("="*80)
    print_orchestrator_report(report)
    
    print("\n" + "="*80)
    print("✅ ALL ORCHESTRATOR TESTS PASSED!")
    print("="*80 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        test_orchestrator()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise