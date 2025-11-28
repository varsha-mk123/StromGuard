# data/simulator.py
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class GigWorkerSimulator:
    """
    Generates realistic gig worker income data for demo
    Simulates 90 days of Swiggy/Zomato delivery partner earnings
    """
    
    def __init__(self, user_name="Rajesh", city="Bangalore", platform="Swiggy"):
        self.user_name = user_name
        self.city = city
        self.platform = platform
        
    def generate_income_history(self, days=90):
        """
        Generate realistic income data with patterns:
        - Weekend boost (+35%)
        - Festival boost (+60%)
        - Rain boost (+25% for delivery)
        - Day of week patterns
        - Random daily variation
        """
        data = []
        base_daily = 500  # ₹500 base per day
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            
            # Extract patterns
            is_weekend = date.weekday() >= 5  # Saturday, Sunday
            is_festival = self._is_indian_festival(date)
            is_rainy = random.random() < 0.18  # 18% chance of rain
            day_of_week = date.weekday()
            
            # Calculate daily income with patterns
            income = base_daily
            
            # Apply multipliers
            if is_weekend:
                income *= 1.35
            
            if is_festival:
                income *= 1.6
            
            if is_rainy:
                income *= 1.25  # Rain = more delivery orders
            
            # Day of week pattern (Friday > Thursday > Wednesday...)
            day_multipliers = [0.85, 0.88, 0.93, 1.0, 1.15, 1.35, 1.30]
            income *= day_multipliers[day_of_week]
            
            # Month pattern (salary days = more orders)
            if date.day in [1, 2, 3, 28, 29, 30, 31]:
                income *= 1.1  # Salary day boost
            
            # Add realistic random variation (±30%)
            income *= random.uniform(0.7, 1.3)
            
            # Round to realistic ₹10 increments
            income = round(income / 10) * 10
            
            # Calculate derived metrics
            hours_worked = random.randint(6, 11)
            orders_completed = int(income / 25)  # ₹25 avg per order
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'income': income,
                'hours_worked': hours_worked,
                'orders_completed': orders_completed,
                'platform': random.choice(['Swiggy', 'Zomato', self.platform]),
                'weather': 'rain' if is_rainy else 'clear',
                'is_festival': is_festival,
                'is_weekend': is_weekend,
                'efficiency': round(income / hours_worked, 2)  # ₹ per hour
            })
        
        return pd.DataFrame(data)
    
    def _is_indian_festival(self, date):
        
        # Major festivals 2024-2025
        festivals = [
            (2024, 10, 24),  # Diwali
            (2024, 11, 1),   # Kannada Rajyotsava
            (2024, 11, 15),  # Guru Nanak Jayanti
            (2024, 12, 25),  # Christmas
            (2025, 1, 14),   # Makar Sankranti
            (2025, 1, 26),   # Republic Day
            (2025, 3, 14),   # Holi
            (2025, 4, 13),   # Ugadi
            (2025, 8, 15),   # Independence Day
            (2025, 10, 2),   # Gandhi Jayanti
        ]
        
        date_tuple = (date.year, date.month, date.day)
        return date_tuple in festivals
    
    def get_summary_stats(self, df):
        """Calculate summary statistics"""
        return {
            'total_days': len(df),
            'avg_daily_income': round(df['income'].mean(), 2),
            'median_daily_income': round(df['income'].median(), 2),
            'std_deviation': round(df['income'].std(), 2),
            'min_income': round(df['income'].min(), 2),
            'max_income': round(df['income'].max(), 2),
            'total_income': round(df['income'].sum(), 2),
            'avg_efficiency': round(df['efficiency'].mean(), 2),
            'total_orders': df['orders_completed'].sum()
        }
    
    def generate_spending_data(self, days=30):
        """
        Generate realistic spending data for gig worker
        Categories: food, fuel, rent, phone, entertainment, family_support
        """
        data = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            
            # Daily random expenses
            daily_expenses = []
            
            # Food (most days)
            if random.random() < 0.9:  # 90% days
                daily_expenses.append({
                    'amount': random.randint(80, 180),
                    'category': 'food',
                    'description': random.choice([
                        'Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Tea/Coffee'
                    ])
                })
            
            # Fuel (working days)
            if date.weekday() < 6:  # Not Sunday
                daily_expenses.append({
                    'amount': random.randint(60, 150),
                    'category': 'fuel',
                    'description': 'Petrol/Diesel'
                })
            
            # Phone recharge (random days)
            if random.random() < 0.1:  # ~3 times per month
                daily_expenses.append({
                    'amount': random.choice([299, 399, 499, 599]),
                    'category': 'phone',
                    'description': 'Mobile recharge'
                })
            
            # Entertainment (weekends)
            if date.weekday() >= 5 and random.random() < 0.4:
                daily_expenses.append({
                    'amount': random.randint(100, 500),
                    'category': 'entertainment',
                    'description': random.choice([
                        'Movie', 'Restaurant', 'Friends outing', 'Shopping'
                    ])
                })
            
            # Family support (1st of month)
            if date.day == 1:
                daily_expenses.append({
                    'amount': random.randint(3000, 5000),
                    'category': 'family_support',
                    'description': 'Money sent to family'
                })
            
            # Rent (1st of month)
            if date.day == 1:
                daily_expenses.append({
                    'amount': 6000,
                    'category': 'rent',
                    'description': 'Monthly rent'
                })
            
            # Medical/misc (random)
            if random.random() < 0.05:
                daily_expenses.append({
                    'amount': random.randint(200, 1000),
                    'category': 'medical',
                    'description': 'Medical/Emergency'
                })
            
            # Add all daily expenses
            for expense in daily_expenses:
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'amount': expense['amount'],
                    'category': expense['category'],
                    'description': expense['description']
                })
        
        return pd.DataFrame(data)
    
    def get_spending_summary(self, df):
        """Calculate spending summary statistics"""
        return {
            'total_spent': round(df['amount'].sum(), 2),
            'daily_average': round(df['amount'].sum() / 30, 2),
            'by_category': df.groupby('category')['amount'].sum().to_dict(),
            'largest_expense': round(df['amount'].max(), 2),
            'days_with_spending': len(df['date'].unique())
        }


# Test function
if __name__ == "__main__":
    sim = GigWorkerSimulator()
    df = sim.generate_income_history(90)
    
    print("✅ Generated 90 days of data")
    print(f"\n📊 Summary:")
    stats = sim.get_summary_stats(df)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n📅 Sample data (last 5 days):")
    print(df.tail())