# # data/weather_api.py
# import requests
# import os
# from datetime import datetime, timedelta
# from dotenv import load_dotenv

# load_dotenv()

# class WeatherAPI:
#     """Fetch weather data from OpenWeather API"""
    
#     def __init__(self):
#         self.api_key = os.getenv("OPENWEATHER_API_KEY")
#         self.city = os.getenv("CITY", "Bangalore")
#         self.base_url = "http://api.openweathermap.org/data/2.5"
        
#         if not self.api_key:
#             print("⚠️  Warning: OPENWEATHER_API_KEY not found in .env")
    
#     def get_current_weather(self):
#         """Get current weather"""
#         url = f"{self.base_url}/weather"
#         params = {
#             'q': self.city,
#             'appid': self.api_key,
#             'units': 'metric'  # Celsius
#         }
        
#         try:
#             response = requests.get(url, params=params, timeout=5)
#             response.raise_for_status()
#             data = response.json()
            
#             return {
#                 'temperature': data['main']['temp'],
#                 'feels_like': data['main']['feels_like'],
#                 'weather': data['weather'][0]['main'],
#                 'description': data['weather'][0]['description'],
#                 'humidity': data['main']['humidity'],
#                 'wind_speed': data['wind']['speed'],
#                 'rain': data.get('rain', {}).get('1h', 0),
#                 'timestamp': datetime.now().isoformat()
#             }
#         except Exception as e:
#             print(f"❌ Error fetching current weather: {e}")
#             return None
    
#     def get_forecast(self, days=7):
#         """
#         Get weather forecast for next N days
#         OpenWeather free tier: 5 days, 3-hour intervals
#         """
#         # Limit to 5 days max for free tier
#         days = min(days, 5)
        
#         if not self.api_key:
#             print("⚠️  Using mock weather data (no API key)")
#             return self._get_mock_forecast(days)
        
#         url = f"{self.base_url}/forecast"
#         params = {
#             'q': self.city,
#             'appid': self.api_key,
#             'units': 'metric',
#             'cnt': 40  # 5 days * 8 intervals
#         }
        
#         try:
#             response = requests.get(url, params=params, timeout=10)
#             response.raise_for_status()
#             data = response.json()
            
#             # Process forecast into daily summaries
#             daily_forecast = self._process_forecast_to_daily(data['list'])
            
#             result = daily_forecast[:days]
            
#             # If we need more than 5 days, extend with mock data
#             if days > len(result):
#                 mock_extension = self._get_mock_forecast(days - len(result))
#                 result.extend(mock_extension)
            
#             return result
            
#         except Exception as e:
#             print(f"❌ Error fetching forecast: {e}")
#             print(f"    Using mock data instead")
#             return self._get_mock_forecast(days)
    
#     def _process_forecast_to_daily(self, forecast_list):
#         """Convert 3-hour intervals to daily summaries"""
#         daily = {}
        
#         for item in forecast_list:
#             date = item['dt_txt'].split(' ')[0]  # Extract date
            
#             if date not in daily:
#                 daily[date] = {
#                     'date': date,
#                     'temps': [],
#                     'rain_prob': [],
#                     'weather_conditions': [],
#                     'rain_mm': []
#                 }
            
#             daily[date]['temps'].append(item['main']['temp'])
#             daily[date]['rain_prob'].append(item.get('pop', 0) * 100)  # Probability of precipitation
#             daily[date]['weather_conditions'].append(item['weather'][0]['main'])
#             daily[date]['rain_mm'].append(item.get('rain', {}).get('3h', 0))
        
#         # Calculate daily aggregates
#         result = []
#         for date, data in daily.items():
#             result.append({
#                 'date': date,
#                 'avg_temp': round(sum(data['temps']) / len(data['temps']), 1),
#                 'max_temp': round(max(data['temps']), 1),
#                 'min_temp': round(min(data['temps']), 1),
#                 'rain_probability': round(max(data['rain_prob']), 0),  # Max probability
#                 'total_rain_mm': round(sum(data['rain_mm']), 1),
#                 'weather': max(set(data['weather_conditions']), 
#                              key=data['weather_conditions'].count),  # Most common
#                 'will_rain': max(data['rain_prob']) > 50 or sum(data['rain_mm']) > 1
#             })
        
#         return result
    
#     def _get_mock_forecast(self, days=7):
#         """Fallback mock forecast if API fails"""
#         print("⚠️  Using mock weather data (API unavailable)")
        
#         forecast = []
#         for i in range(days):
#             date = datetime.now() + timedelta(days=i+1)
#             forecast.append({
#                 'date': date.strftime('%Y-%m-%d'),
#                 'avg_temp': 25 + (i % 3),
#                 'max_temp': 30,
#                 'min_temp': 20,
#                 'rain_probability': 20 if i % 3 == 0 else 10,
#                 'total_rain_mm': 0,
#                 'weather': 'Rain' if i % 3 == 0 else 'Clear',
#                 'will_rain': i % 3 == 0
#             })
        
#         return forecast
    
#     def get_weather_impact_score(self, forecast_day):
#         """
#         Calculate weather impact on delivery income
#         Rain = more orders (positive impact)
#         Extreme heat = fewer riders (negative impact)
#         """
#         impact_score = 1.0  # Neutral
        
#         # Rain boost (people order more food delivery)
#         if forecast_day['will_rain']:
#             impact_score += 0.25
        
#         # Extreme heat penalty (fewer riders, customer sympathy)
#         if forecast_day['max_temp'] > 38:
#             impact_score -= 0.10
        
#         # Perfect weather (mild boost)
#         if 20 <= forecast_day['avg_temp'] <= 30 and not forecast_day['will_rain']:
#             impact_score += 0.05
        
#         return round(impact_score, 2)


# # Test function
# if __name__ == "__main__":
#     weather = WeatherAPI()
    
#     print("🌤️  Testing Weather API\n")
    
#     # Test current weather
#     current = weather.get_current_weather()
#     if current:
#         print(f"📍 Current weather in {weather.city}:")
#         print(f"  Temperature: {current['temperature']}°C")
#         print(f"  Condition: {current['weather']} - {current['description']}")
#         print(f"  Rain: {current['rain']}mm\n")
    
#     # Test forecast
#     forecast = weather.get_forecast(7)
#     print(f"🔮 7-Day Forecast:")
#     for day in forecast:
#         impact = weather.get_weather_impact_score(day)
#         print(f"  {day['date']}: {day['weather']}, {day['avg_temp']}°C, "
#               f"Rain: {day['rain_probability']}%, Impact: {impact}x")


# data/weather_api.py
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    """Fetch weather data from OpenWeather API"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.city = os.getenv("CITY", "Bangalore")
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        if not self.api_key:
            print("⚠️  Warning: OPENWEATHER_API_KEY not found in .env")
            print("    Using mock weather data for demo")
    
    def get_current_weather(self):
        """Get current weather"""
        if not self.api_key:
            return self._get_mock_current()
        
        url = f"{self.base_url}/weather"
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'rain': data.get('rain', {}).get('1h', 0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error fetching current weather: {e}")
            return self._get_mock_current()
    
    def get_forecast(self, days=7):
        """
        Get weather forecast for next N days
        OpenWeather free tier: 5 days, 3-hour intervals
        """
        # Limit to 5 days max for free tier
        days = min(days, 5)
        
        if not self.api_key:
            print("⚠️  Using mock weather data (no API key)")
            return self._get_mock_forecast(days)
        
        url = f"{self.base_url}/forecast"
        params = {
            'q': self.city,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': 40  # 5 days * 8 intervals
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process forecast into daily summaries
            daily_forecast = self._process_forecast_to_daily(data['list'])
            
            result = daily_forecast[:days]
            
            # If we need more than 5 days, extend with mock data
            if days > len(result):
                mock_extension = self._get_mock_forecast(days - len(result))
                result.extend(mock_extension)
            
            return result
            
        except Exception as e:
            print(f"❌ Error fetching forecast: {e}")
            print(f"    Using mock data instead")
            return self._get_mock_forecast(days)
    
    def _process_forecast_to_daily(self, forecast_list):
        """Convert 3-hour intervals to daily summaries"""
        daily = {}
        
        for item in forecast_list:
            date = item['dt_txt'].split(' ')[0]
            
            if date not in daily:
                daily[date] = {
                    'date': date,
                    'temps': [],
                    'rain_prob': [],
                    'weather_conditions': [],
                    'rain_mm': []
                }
            
            daily[date]['temps'].append(item['main']['temp'])
            daily[date]['rain_prob'].append(item.get('pop', 0) * 100)
            daily[date]['weather_conditions'].append(item['weather'][0]['main'])
            daily[date]['rain_mm'].append(item.get('rain', {}).get('3h', 0))
        
        # Calculate daily aggregates
        result = []
        for date, data in sorted(daily.items()):
            result.append({
                'date': date,
                'avg_temp': round(sum(data['temps']) / len(data['temps']), 1),
                'max_temp': round(max(data['temps']), 1),
                'min_temp': round(min(data['temps']), 1),
                'rain_probability': round(max(data['rain_prob']), 0),
                'total_rain_mm': round(sum(data['rain_mm']), 1),
                'weather': max(set(data['weather_conditions']), 
                             key=data['weather_conditions'].count),
                'will_rain': max(data['rain_prob']) > 50 or sum(data['rain_mm']) > 1
            })
        
        return result
    
    def _get_mock_current(self):
        """Mock current weather"""
        return {
            'temperature': 26,
            'feels_like': 28,
            'weather': 'Clear',
            'description': 'clear sky',
            'humidity': 65,
            'wind_speed': 3.5,
            'rain': 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_mock_forecast(self, days=7):
        """Fallback mock forecast"""
        forecast = []
        base_date = datetime.now()
        
        for i in range(days):
            date = base_date + timedelta(days=i+1)
            
            # Create realistic patterns
            is_weekend = date.weekday() >= 5
            rain_chance = 30 if i % 3 == 0 else 10
            will_rain = i % 3 == 0
            
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'avg_temp': 25 + (i % 3) + (2 if is_weekend else 0),
                'max_temp': 30 + (i % 3),
                'min_temp': 20 + (i % 2),
                'rain_probability': rain_chance,
                'total_rain_mm': 5.0 if will_rain else 0,
                'weather': 'Rain' if will_rain else 'Clear',
                'will_rain': will_rain
            })
        
        return forecast
    
    def get_weather_impact_score(self, forecast_day):
        """Calculate weather impact on delivery income"""
        if not forecast_day:
            return 1.0
        
        impact_score = 1.0
        
        # Rain boost (more delivery orders)
        if forecast_day.get('will_rain', False):
            impact_score += 0.25
        
        # Extreme heat penalty
        if forecast_day.get('max_temp', 30) > 38:
            impact_score -= 0.10
        
        # Perfect weather boost
        avg_temp = forecast_day.get('avg_temp', 26)
        if 20 <= avg_temp <= 30 and not forecast_day.get('will_rain', False):
            impact_score += 0.05
        
        return round(impact_score, 2)


# Test function
if __name__ == "__main__":
    weather = WeatherAPI()
    
    print("🌤️  Testing Weather API\n")
    
    # Test current
    current = weather.get_current_weather()
    if current:
        print(f"📍 Current weather in {weather.city}:")
        print(f"  Temperature: {current['temperature']}°C")
        print(f"  Condition: {current['weather']}")
        print()
    
    # Test forecast
    print("🔮 Testing 7-Day Forecast:")
    forecast = weather.get_forecast(7)
    print(f"✅ Received {len(forecast)} days of forecast\n")
    
    for day in forecast:
        impact = weather.get_weather_impact_score(day)
        rain_icon = "🌧️" if day['will_rain'] else "☀️"
        print(f"{rain_icon} {day['date']}: {day['weather']:8s} | "
              f"{day['avg_temp']}°C | Rain: {day['rain_probability']}% | "
              f"Impact: {impact}x")
    
    print("\n✅ Weather API test complete")