# agents/opportunity_scout_agent.py
from phi.agent import Agent
from phi.model.google import Gemini
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.weather_api import WeatherAPI

class OpportunityScoutAgent:
    """
    Opportunity Scout Agent
    - Detects real-time surge pricing opportunities
    - Identifies high-demand zones during festivals/events
    - Recommends optimal work times to maximize earnings
    - Sends proactive alerts when opportunities arise
    """
    
    def __init__(self, user_location="Bangalore"):
        self.location = user_location
        self.weather_api = WeatherAPI()
        
        # Initialize Phidata Agent
        self.agent = Agent(
            name="Opportunity Scout Agent",
            model=Gemini(id="gemini-2.0-flash"),
            instructions=[
                "You are an opportunity scout for gig workers in India.",
                "Your job: Find and alert users about earning opportunities.",
                "Focus on: surge pricing, high-demand zones, optimal work times.",
                "Be specific with locations, timings, and expected earnings.",
                "Speak in Hinglish - natural and actionable.",
                "Always include: WHERE, WHEN, HOW MUCH.",
                "Keep alerts urgent and concise (under 100 words)."
            ],
            markdown=True,
            show_tool_calls=False
        )
        
        print(f"✅ Opportunity Scout Agent initialized for {user_location}")
    
    def scan_real_time_opportunities(self):
        """
        Scan for immediate earning opportunities
        """
        print("🔍 Scanning for opportunities...")
        
        opportunities = []
        current_time = datetime.now()
        current_hour = current_time.hour
        day_of_week = current_time.weekday()
        
        # Opportunity 1: Time-based surge detection
        surge_opportunity = self._detect_surge_timing(current_hour, day_of_week)
        if surge_opportunity:
            opportunities.append(surge_opportunity)
        
        # Opportunity 2: Weather-based demand
        weather_opportunity = self._detect_weather_opportunity()
        if weather_opportunity:
            opportunities.append(weather_opportunity)
        
        # Opportunity 3: Festival/Event detection
        event_opportunity = self._detect_event_opportunities()
        if event_opportunity:
            opportunities.append(event_opportunity)
        
        # Opportunity 4: Zone optimization
        zone_opportunity = self._recommend_optimal_zone(current_time)
        if zone_opportunity:
            opportunities.append(zone_opportunity)
        
        # Prioritize by urgency and earning potential
        opportunities.sort(key=lambda x: x['priority'])
        
        return opportunities
    
    def _detect_surge_timing(self, hour, day_of_week):
        """
        Detect if current time is surge period
        """
        # Define surge periods
        surge_periods = {
            'lunch_peak': {'hours': [12, 13, 14], 'multiplier': 1.3, 'zones': ['Koramangala', 'Indiranagar', 'Whitefield']},
            'dinner_peak': {'hours': [19, 20, 21], 'multiplier': 1.5, 'zones': ['HSR Layout', 'BTM', 'Jayanagar']},
            'late_night': {'hours': [22, 23, 0], 'multiplier': 1.4, 'zones': ['Airport', 'Outer Ring Road']},
            'weekend_brunch': {'hours': [10, 11, 12], 'multiplier': 1.2, 'zones': ['MG Road', 'Church Street']}
        }
        
        is_weekend = day_of_week >= 5
        
        for period_name, period_data in surge_periods.items():
            if hour in period_data['hours']:
                # Skip weekend_brunch if not weekend
                if period_name == 'weekend_brunch' and not is_weekend:
                    continue
                
                return {
                    'type': 'surge_timing',
                    'priority': 1,
                    'urgency': 'HIGH',
                    'period': period_name,
                    'multiplier': period_data['multiplier'],
                    'zones': period_data['zones'],
                    'expected_earnings': f"₹{int(600 * period_data['multiplier'])}-{int(800 * period_data['multiplier'])}",
                    'duration': '2-3 hours',
                    'message': self._generate_surge_alert(period_name, period_data)
                }
        
        return None
    
    def _generate_surge_alert(self, period_name, data):
        """Generate urgent surge alert"""
        zones_str = ", ".join(data['zones'][:2])
        
        context = f"""
🔥 SURGE ALERT! {period_name.replace('_', ' ').title()} happening NOW!

Details:
- Zones: {zones_str}
- Multiplier: {data['multiplier']}x
- Expected: {int(600 * data['multiplier'])}-{int(800 * data['multiplier'])} per hour
- Duration: Next 2-3 hours

Generate URGENT alert in Hinglish (under 80 words):
1. Where to go (specific zone)
2. How much they can earn
3. Why RIGHT NOW

Be exciting and actionable!
"""
        
        response = self.agent.run(context)
        return response.content
    
    def _detect_weather_opportunity(self):
        """
        Detect weather-based opportunities
        """
        weather = self.weather_api.get_current_weather()
        
        if not weather:
            return None
        
        # Rain = more delivery orders
        if weather.get('rain', 0) > 0 or weather.get('weather') == 'Rain':
            return {
                'type': 'weather_boost',
                'priority': 1,
                'urgency': 'HIGH',
                'condition': 'Rain',
                'boost': '+25%',
                'expected_earnings': '₹750-950/hour',
                'message': self._generate_weather_alert('rain', weather)
            }
        
        # Extreme heat = fewer riders = opportunity
        if weather.get('temperature', 30) > 38:
            return {
                'type': 'weather_boost',
                'priority': 2,
                'urgency': 'MEDIUM',
                'condition': 'Extreme Heat',
                'boost': '+15%',
                'expected_earnings': '₹690-850/hour',
                'message': self._generate_weather_alert('heat', weather)
            }
        
        return None
    
    def _generate_weather_alert(self, condition, weather_data):
        """Generate weather-based opportunity alert"""
        
        if condition == 'rain':
            context = f"""
🌧️ RAIN OPPORTUNITY!

Current weather: {weather_data['weather']}, {weather_data['temperature']}°C
Rain detected: {weather_data.get('rain', 0)}mm

Generate alert in Hinglish (under 70 words):
1. Rain = 25% more orders expected
2. Focus on food delivery (Swiggy/Zomato)
3. Stay safe but maximize this window

Be excited but mention safety!
"""
        else:  # heat
            context = f"""
🔥 HEAT OPPORTUNITY!

Temperature: {weather_data['temperature']}°C (very hot!)
Fewer riders working = more orders for you

Generate alert in Hinglish (under 70 words):
1. Fewer competitors today
2. 15% boost expected
3. Stay hydrated, take breaks

Encourage but emphasize health!
"""
        
        response = self.agent.run(context)
        return response.content
    
    def _detect_event_opportunities(self):
        """
        Detect festivals, events, special occasions
        """
        current_date = datetime.now()
        
        # Indian festivals calendar (2024-2025)
        festivals = {
            (11, 1): {'name': 'Kannada Rajyotsava', 'boost': 1.4, 'zones': ['Malleshwaram', 'Jayanagar']},
            (11, 15): {'name': 'Guru Nanak Jayanti', 'boost': 1.3, 'zones': ['All zones']},
            (12, 25): {'name': 'Christmas', 'boost': 1.6, 'zones': ['Church Street', 'Brigade Road', 'MG Road']},
            (12, 31): {'name': 'New Year Eve', 'boost': 1.8, 'zones': ['Indiranagar', 'Koramangala', 'Whitefield']},
            (1, 14): {'name': 'Makar Sankranti', 'boost': 1.3, 'zones': ['Traditional areas']},
            (1, 26): {'name': 'Republic Day', 'boost': 1.2, 'zones': ['All zones']},
        }
        
        # Check if today is a festival
        today_key = (current_date.month, current_date.day)
        if today_key in festivals:
            festival = festivals[today_key]
            return {
                'type': 'festival',
                'priority': 1,
                'urgency': 'HIGH',
                'festival_name': festival['name'],
                'boost': f"+{int((festival['boost'] - 1) * 100)}%",
                'zones': festival['zones'],
                'expected_earnings': f"₹{int(700 * festival['boost'])}-{int(900 * festival['boost'])}",
                'message': self._generate_festival_alert(festival)
            }
        
        # Check upcoming festivals (next 7 days)
        for days_ahead in range(1, 8):
            future_date = current_date + timedelta(days=days_ahead)
            future_key = (future_date.month, future_date.day)
            
            if future_key in festivals:
                festival = festivals[future_key]
                return {
                    'type': 'upcoming_festival',
                    'priority': 3,
                    'urgency': 'LOW',
                    'festival_name': festival['name'],
                    'days_away': days_ahead,
                    'boost': f"+{int((festival['boost'] - 1) * 100)}%",
                    'message': f"📅 {festival['name']} in {days_ahead} days! High demand expected. Plan ahead to maximize earnings."
                }
        
        # Weekend party zones (Friday/Saturday nights)
        if current_date.weekday() in [4, 5] and current_date.hour >= 20:
            return {
                'type': 'weekend_party',
                'priority': 2,
                'urgency': 'MEDIUM',
                'expected_earnings': '₹850-1100/hour',
                'zones': ['Indiranagar', 'Koramangala', 'MG Road'],
                'message': "🎉 Weekend party zone active! High demand in pub areas. Indiranagar/Koramangala surging now!"
            }
        
        return None
    
    def _generate_festival_alert(self, festival):
        """Generate festival opportunity alert"""
        
        zones_str = ", ".join(festival['zones']) if isinstance(festival['zones'], list) else festival['zones']
        
        context = f"""
🎉 FESTIVAL OPPORTUNITY! {festival['name']} TODAY!

Boost: {festival['boost']}x normal demand
Zones: {zones_str}

Generate exciting alert in Hinglish (under 90 words):
1. Festival means HIGH orders
2. Where to focus (zones)
3. Expected earnings today
4. Festival greeting

Be celebratory and motivating!
"""
        
        response = self.agent.run(context)
        return response.content
    
    def _recommend_optimal_zone(self, current_time):
        """
        Recommend best zone based on time and patterns
        """
        hour = current_time.hour
        day = current_time.weekday()
        
        # Zone recommendations based on time
        zone_patterns = {
            'morning_office': {
                'hours': [8, 9, 10],
                'zones': ['Whitefield', 'Electronic City', 'Outer Ring Road'],
                'reason': 'Office breakfast rush',
                'boost': 1.2
            },
            'lunch_corporate': {
                'hours': [12, 13, 14],
                'zones': ['MG Road', 'Koramangala', 'Indiranagar'],
                'reason': 'Corporate lunch orders',
                'boost': 1.3
            },
            'evening_residential': {
                'hours': [18, 19, 20, 21],
                'zones': ['HSR Layout', 'BTM', 'Jayanagar', 'JP Nagar'],
                'reason': 'Residential dinner peak',
                'boost': 1.4
            },
            'late_night': {
                'hours': [22, 23, 0, 1],
                'zones': ['Airport Road', 'Marathahalli', 'Bellandur'],
                'reason': 'Late night tech workers',
                'boost': 1.3
            }
        }
        
        for pattern_name, pattern in zone_patterns.items():
            if hour in pattern['hours']:
                return {
                    'type': 'zone_recommendation',
                    'priority': 2,
                    'urgency': 'MEDIUM',
                    'recommended_zones': pattern['zones'],
                    'reason': pattern['reason'],
                    'boost': f"+{int((pattern['boost'] - 1) * 100)}%",
                    'expected_earnings': f"₹{int(600 * pattern['boost'])}-{int(800 * pattern['boost'])}",
                    'message': f"📍 Best zones now: {', '.join(pattern['zones'][:2])}. {pattern['reason']} - {int((pattern['boost'] - 1) * 100)}% boost expected!"
                }
        
        return None
    
    def generate_daily_opportunity_plan(self):
        """
        Generate optimized work plan for the day
        """
        print("📋 Generating daily opportunity plan...")
        
        current_time = datetime.now()
        plan = []
        
        # Morning slot (8-11 AM)
        if current_time.hour < 11:
            plan.append({
                'time_slot': '8:00 AM - 11:00 AM',
                'recommendation': 'Office areas breakfast rush',
                'zones': ['Whitefield', 'Electronic City'],
                'expected': '₹600-800/hour',
                'priority': 'MEDIUM'
            })
        
        # Lunch slot (12-2 PM)
        plan.append({
            'time_slot': '12:00 PM - 2:00 PM',
            'recommendation': 'Peak lunch demand',
            'zones': ['Koramangala', 'Indiranagar', 'MG Road'],
            'expected': '₹750-950/hour',
            'priority': 'HIGH'
        })
        
        # Evening slot (7-9 PM)
        plan.append({
            'time_slot': '7:00 PM - 9:00 PM',
            'recommendation': 'Dinner peak (BEST)',
            'zones': ['HSR Layout', 'BTM', 'Jayanagar'],
            'expected': '₹800-1100/hour',
            'priority': 'HIGHEST'
        })
        
        # Late night (if applicable)
        if current_time.weekday() >= 4:  # Friday/Saturday
            plan.append({
                'time_slot': '10:00 PM - 12:00 AM',
                'recommendation': 'Weekend party orders',
                'zones': ['Indiranagar pubs', 'Koramangala'],
                'expected': '₹850-1100/hour',
                'priority': 'HIGH'
            })
        
        return plan
    
    def get_opportunity_summary(self):
        """
        Quick summary of current opportunities
        """
        opportunities = self.scan_real_time_opportunities()
        
        summary = {
            'total_opportunities': len(opportunities),
            'urgent_count': len([o for o in opportunities if o['urgency'] == 'HIGH']),
            'top_opportunity': opportunities[0] if opportunities else None,
            'all_opportunities': opportunities
        }
        
        return summary


# Utility function
def print_opportunities(opportunities):
    """Pretty print opportunities"""
    print("\n" + "="*70)
    print("🔍 OPPORTUNITY SCOUT REPORT")
    print("="*70 + "\n")
    
    if not opportunities:
        print("✅ No immediate opportunities right now.")
        print("   Check back during peak hours (12-2 PM, 7-9 PM)\n")
        return
    
    for i, opp in enumerate(opportunities, 1):
        urgency_emoji = "🔴" if opp['urgency'] == 'HIGH' else "🟡" if opp['urgency'] == 'MEDIUM' else "🟢"
        
        print(f"{urgency_emoji} OPPORTUNITY {i}: {opp['type'].upper()}")
        print(f"{'─'*70}")
        print(f"Priority: {opp['priority']} | Urgency: {opp['urgency']}")
        
        if 'expected_earnings' in opp:
            print(f"Expected: {opp['expected_earnings']}")
        
        if 'zones' in opp:
            zones = opp['zones'] if isinstance(opp['zones'], list) else [opp['zones']]
            print(f"Zones: {', '.join(zones)}")
        
        print(f"\n{opp['message']}")
        print(f"{'─'*70}\n")


# Test function
if __name__ == "__main__":
    print("🧪 Testing Opportunity Scout Agent\n")
    
    # Initialize
    scout = OpportunityScoutAgent("Bangalore")
    print()
    
    # Scan opportunities
    opportunities = scout.scan_real_time_opportunities()
    print_opportunities(opportunities)
    
    # Daily plan
    print("\n📋 DAILY OPPORTUNITY PLAN")
    print("="*70)
    plan = scout.generate_daily_opportunity_plan()
    
    for slot in plan:
        priority_emoji = "🔥" if slot['priority'] == 'HIGHEST' else "⭐" if slot['priority'] == 'HIGH' else "📍"
        print(f"\n{priority_emoji} {slot['time_slot']} - {slot['priority']}")
        print(f"   {slot['recommendation']}")
        print(f"   Zones: {', '.join(slot['zones'])}")
        print(f"   Expected: {slot['expected']}")
    
    print("\n" + "="*70)
    print("✅ Opportunity Scout test complete!") 