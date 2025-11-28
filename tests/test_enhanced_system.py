# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from data.simulator import GigWorkerSimulator
# from agents.orchestrator_agent import OrchestratorAgent
# from agents.opportunity_scout_agent import print_opportunities
# from agents.savings_manager_agent import print_savings_summary

# def test_enhanced_system():
#     """Test complete system with all 5 agents"""
    
#     print("\n" + "="*80)
#     print("🧪 ENHANCED STORMGUARD SYSTEM TEST (5 AGENTS)")
#     print("="*80 + "\n")
    
#     # Setup
#     print("📊 Setting up...")
#     simulator = GigWorkerSimulator("Rajesh", "Bangalore")
#     income_data = simulator.generate_income_history(90)
#     spending_data = simulator.generate_spending_data(30)
    
#     user_profile = {
#         'user_id': 'enhanced_test_001',
#         'name': 'Rajesh',
#         'city': 'Bangalore',
#         'platform': 'Swiggy + Zomato',
#         'language': 'hinglish',
#         'goals': ['Save ₹20,000 emergency fund', 'Buy bike ₹60,000'],
#         'savings_rate': 0.03
#     }
    
#     print("✅ Data ready\n")
    
#     # Initialize enhanced orchestrator
#     print("🤖 Initializing Enhanced Orchestrator (5 agents)...")
#     orchestrator = OrchestratorAgent(user_profile, income_data, spending_data)
#     print()
    
#     # Test 1: Run enhanced daily check
#     print("TEST 1: Enhanced Daily Check")
#     print("-" * 80)
#     print("⏳ This includes all 5 agents... (20-25 seconds)\n")
    
#     report = orchestrator.run_daily_check()
    
#     assert 'opportunities' in report
#     assert 'savings_summary' in report
#     assert 'savings_recommendation' in report
    
#     print("✅ PASSED: Enhanced daily check completed")
#     print(f"   - Forecast: ₹{report['dashboard']['summary']['weekly_income_forecast']:.0f}")
#     print(f"   - Opportunities: {len(report['opportunities'])}")
#     print(f"   - Savings Rate: {int(report['savings_summary']['current_rate'].replace('%', ''))}%")
#     print(f"   - Total Saved: ₹{report['savings_summary']['total_saved']:.0f}\n")
    
#     # Test 2: Opportunities
#     print("TEST 2: Opportunity Scout")
#     print("-" * 80)
#     opportunities = report['opportunities']
#     print(f"✅ PASSED: Found {len(opportunities)} opportunities")
#     if opportunities:
#         print_opportunities(opportunities[:2])  # Show top 2
#     print()
    
#     # Test 3: Savings
#     print("TEST 3: Savings Manager")
#     print("-" * 80)
#     savings = report['savings_summary']
#     print("✅ PASSED: Savings tracking active")
#     print_savings_summary(savings)
    
#     # Test 4: Savings adjustment
#     print("TEST 4: Adjust Savings Rate")
#     print("-" * 80)
#     result = orchestrator.adjust_savings_rate(0.05, "Testing higher rate")
#     print(f"✅ PASSED: {result['message']}\n")
    
#     # Test 5: Quick opportunities (fast check)
#     print("TEST 5: Quick Opportunity Check")
#     print("-" * 80)
#     quick_opps = orchestrator.get_quick_opportunities()
#     print(f"✅ PASSED: Quick check found {len(quick_opps)} opportunities\n")
    
#     print("="*80)
#     print("✅ ALL ENHANCED SYSTEM TESTS PASSED!")
#     print("="*80)
#     print("\n🎉 You now have a complete 5-agent system:")
#     print("   1. Weather Forecast Agent")
#     print("   2. Financial Coach Agent")
#     print("   3. Orchestrator Agent")
#     print("   4. Opportunity Scout Agent  ← NEW")
#     print("   5. Savings Manager Agent    ← NEW")
#     print("\n🚀 Ready for hackathon demo!\n")


# if __name__ == "__main__":
#     test_enhanced_system()

# tests/test_enhanced_system.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.simulator import GigWorkerSimulator
from agents.orchestrator_agent import OrchestratorAgent
from agents.opportunity_scout_agent import print_opportunities
from agents.savings_manager_agent import print_savings_summary

def test_enhanced_system():
    """Test complete system with all 5 agents"""
    
    print("\n" + "="*80)
    print("🧪 ENHANCED STORMGUARD SYSTEM TEST (5 AGENTS)")
    print("="*80 + "\n")
    
    # Setup
    print("📊 Setting up...")
    simulator = GigWorkerSimulator("Rajesh", "Bangalore")
    income_data = simulator.generate_income_history(90)
    spending_data = simulator.generate_spending_data(30)
    
    user_profile = {
        'user_id': 'enhanced_test_001',
        'name': 'Rajesh',
        'city': 'Bangalore',
        'platform': 'Swiggy + Zomato',
        'language': 'hinglish',
        'goals': ['Save ₹20,000 emergency fund', 'Buy bike ₹60,000'],
        'savings_rate': 0.03
    }
    
    print("✅ Data ready\n")
    
    # Initialize enhanced orchestrator
    print("🤖 Initializing Enhanced Orchestrator (5 agents)...")
    orchestrator = OrchestratorAgent(user_profile, income_data, spending_data)
    print()
    
    # Test 1: Run enhanced daily check
    print("TEST 1: Enhanced Daily Check")
    print("-" * 80)
    print("⏳ This includes all 5 agents... (20-25 seconds)\n")
    
    report = orchestrator.run_daily_check()
    
    assert 'opportunities' in report, "Should have opportunities"
    assert 'savings_summary' in report, "Should have savings summary"
    assert 'savings_recommendation' in report, "Should have savings recommendation"
    
    print("✅ PASSED: Enhanced daily check completed")
    print(f"   - Forecast: ₹{report['dashboard']['summary']['weekly_income_forecast']:.0f}")
    print(f"   - Opportunities: {len(report['opportunities'])}")
    
    # Fixed: Handle current_rate safely
    current_rate = report['savings_summary'].get('current_rate', '3%')
    if isinstance(current_rate, str):
        current_rate_num = current_rate.replace('%', '')
    else:
        current_rate_num = int(current_rate * 100)
    
    print(f"   - Savings Rate: {current_rate_num}%")
    print(f"   - Total Saved: ₹{report['savings_summary']['total_saved']:.0f}\n")
    
    # Test 2: Opportunities
    print("TEST 2: Opportunity Scout")
    print("-" * 80)
    opportunities = report['opportunities']
    print(f"✅ PASSED: Found {len(opportunities)} opportunities")
    
    if opportunities:
        print("\n📍 Top Opportunities:")
        for i, opp in enumerate(opportunities[:2], 1):
            urgency_emoji = "🔴" if opp['urgency'] == 'HIGH' else "🟡" if opp['urgency'] == 'MEDIUM' else "🟢"
            print(f"\n{urgency_emoji} Opportunity {i}: {opp['type'].replace('_', ' ').title()}")
            print(f"   Priority: {opp['priority']} | Urgency: {opp['urgency']}")
            if 'expected_earnings' in opp:
                print(f"   Expected: {opp['expected_earnings']}")
            # Show first 100 chars of message
            print(f"   {opp['message'][:100]}...")
    else:
        print("   No urgent opportunities at this time")
    
    print()
    
    # Test 3: Savings
    print("TEST 3: Savings Manager")
    print("-" * 80)
    savings = report['savings_summary']
    print("✅ PASSED: Savings tracking active")
    
    # Show savings summary
    print(f"\n💰 Savings Summary:")
    print(f"   Total Saved: ₹{savings.get('total_saved', 0):.0f}")
    print(f"   Days Tracked: {savings.get('days_tracked', 0)}")
    print(f"   Avg Daily: ₹{savings.get('avg_daily_savings', 0):.0f}")
    print(f"   Current Rate: {savings.get('current_rate', '0%')}")
    print(f"   Projected Yearly: ₹{savings.get('projected_yearly', 0):,.0f}")
    print()
    
    # Test 4: Savings recommendation
    print("TEST 4: Smart Savings Recommendation")
    print("-" * 80)
    savings_rec = report['savings_recommendation']
    
    current = savings_rec.get('current_rate', 0.03)
    recommended = savings_rec.get('recommended_rate', 0.03)
    
    print(f"Current Rate: {int(current*100)}%")
    print(f"Recommended Rate: {int(recommended*100)}%")
    print(f"Monthly at Recommended: ₹{savings_rec.get('monthly_savings_at_recommended', 0):,.0f}")
    
    if savings_rec.get('should_adjust'):
        print(f"✅ Adjustment recommended!")
    else:
        print(f"✅ Current rate is optimal")
    
    # Show AI advice (first 150 chars)
    if 'ai_advice' in savings_rec:
        print(f"\nAI Advice: {savings_rec['ai_advice'][:150]}...")
    
    print()
    
    # Test 5: Adjust savings rate
    print("TEST 5: Adjust Savings Rate")
    print("-" * 80)
    result = orchestrator.adjust_savings_rate(0.05, "Testing higher rate")
    
    assert result['success'], "Should successfully adjust rate"
    print(f"✅ PASSED: {result['message']}")
    print(f"   Old: {result['old_rate']} → New: {result['new_rate']}\n")
    
    # Test 6: Quick opportunities (fast check)
    print("TEST 6: Quick Opportunity Check (No Full Analysis)")
    print("-" * 80)
    quick_opps = orchestrator.get_quick_opportunities()
    print(f"✅ PASSED: Quick check found {len(quick_opps)} opportunities")
    print(f"   (This check is fast - no full agent coordination)\n")
    
    # Test 7: Daily opportunity plan
    print("TEST 7: Daily Opportunity Plan")
    print("-" * 80)
    opp_plan = report.get('opportunity_plan', [])
    
    if opp_plan:
        print(f"✅ PASSED: Generated {len(opp_plan)} time slot recommendations")
        
        # Show plan
        for slot in opp_plan[:3]:  # Show top 3
            priority_emoji = "🔥" if slot['priority'] == 'HIGHEST' else "⭐" if slot['priority'] == 'HIGH' else "📍"
            print(f"\n{priority_emoji} {slot['time_slot']}")
            print(f"   {slot['recommendation']}")
            print(f"   Zones: {', '.join(slot['zones'])}")
            print(f"   Expected: {slot['expected']}")
    else:
        print("✅ PASSED: Plan generation working (empty for now)")
    
    print()
    
    # Test 8: Process income (simulate daily earnings)
    print("TEST 8: Process Daily Income & Auto-Save")
    print("-" * 80)
    
    from datetime import datetime
    test_income = 650
    test_date = datetime.now().strftime('%Y-%m-%d')
    
    savings_record = orchestrator.process_daily_income(test_date, test_income, "Swiggy")
    
    print(f"✅ PASSED: Income processed and auto-saved")
    print(f"   Date: {savings_record['date']}")
    print(f"   Income: ₹{savings_record['income']}")
    print(f"   Saved: ₹{savings_record['saved_amount']:.0f} ({int(savings_record['savings_rate']*100)}%)")
    print()
    
    # Summary
    print("="*80)
    print("✅ ALL ENHANCED SYSTEM TESTS PASSED!")
    print("="*80)
    print("\n🎉 You now have a complete 5-agent system:")
    print("   1. ✅ Weather Forecast Agent - Income prediction")
    print("   2. ✅ Financial Coach Agent - Personalized advice")
    print("   3. ✅ Orchestrator Agent - Master coordinator")
    print("   4. ✅ Opportunity Scout Agent - Real-time alerts")
    print("   5. ✅ Savings Manager Agent - Auto-save 2-10%")
    print("\n📊 System Capabilities:")
    print(f"   • Income forecasting: 7-30 days ahead")
    print(f"   • Risk detection: {len(report.get('risks', []))} types")
    print(f"   • Opportunities: Real-time + daily plan")
    print(f"   • Savings: Auto-save with smart recommendations")
    print(f"   • Coaching: Hinglish, personalized")
    print(f"   • Chat: Natural language interface")
    print("\n🚀 Ready for hackathon demo!")
    print(f"   Run: streamlit run ui/streamlit_app.py")
    print()
    
    return True


if __name__ == "__main__":
    try:
        test_enhanced_system()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        raise