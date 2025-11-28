import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

class UserStorage:
    """
    Persistent storage system for StormGuard
    - Stores user profiles, income, spending, savings
    - Uses JSON files (simple, no database needed)
    - Each user gets their own data folder
    """
    
    def __init__(self, base_dir="user_data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        print(f"📁 Storage initialized at: {self.base_dir.absolute()}")
    
    # ==================== USER PROFILE ====================
    
    def create_user(self, user_data):
        """Create new user profile"""
        user_id = user_data.get('user_id') or self._generate_user_id(user_data['name'])
        user_data['user_id'] = user_id
        user_data['created_at'] = datetime.now().isoformat()
        user_data['last_active'] = datetime.now().isoformat()
        
        # Create user folder
        user_folder = self.base_dir / user_id
        user_folder.mkdir(exist_ok=True)
        
        # Save profile
        self._save_json(user_folder / "profile.json", user_data)
        
        # Initialize empty data files
        self._save_json(user_folder / "income_history.json", [])
        self._save_json(user_folder / "spending_history.json", [])
        self._save_json(user_folder / "savings_history.json", [])
        self._save_json(user_folder / "goals.json", user_data.get('goals', []))
        
        print(f"✅ User created: {user_data['name']} ({user_id})")
        return user_id
    
    def get_user(self, user_id):
        """Get user profile"""
        profile_path = self.base_dir / user_id / "profile.json"
        if profile_path.exists():
            return self._load_json(profile_path)
        return None
    
    def update_user(self, user_id, updates):
        """Update user profile"""
        profile = self.get_user(user_id)
        if profile:
            profile.update(updates)
            profile['last_active'] = datetime.now().isoformat()
            self._save_json(self.base_dir / user_id / "profile.json", profile)
            return True
        return False
    
    def list_users(self):
        """List all users"""
        users = []
        for folder in self.base_dir.iterdir():
            if folder.is_dir():
                profile = self.get_user(folder.name)
                if profile:
                    users.append({
                        'user_id': profile['user_id'],
                        'name': profile['name'],
                        'city': profile.get('city', 'Unknown'),
                        'last_active': profile.get('last_active', 'Unknown')
                    })
        return users
    
    def user_exists(self, user_id):
        """Check if user exists"""
        return (self.base_dir / user_id / "profile.json").exists()
    
    # ==================== INCOME DATA ====================
    
    def add_income(self, user_id, income_data):
        """Add daily income entry"""
        income_path = self.base_dir / user_id / "income_history.json"
        history = self._load_json(income_path) or []
        
        # Add metadata
        income_data['recorded_at'] = datetime.now().isoformat()
        if 'date' not in income_data:
            income_data['date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Check for duplicate date (update instead of add)
        existing_idx = next(
            (i for i, x in enumerate(history) if x['date'] == income_data['date']), 
            None
        )
        
        if existing_idx is not None:
            history[existing_idx] = income_data
            print(f"📝 Updated income for {income_data['date']}")
        else:
            history.append(income_data)
            print(f"✅ Added income for {income_data['date']}: ₹{income_data['income']}")
        
        self._save_json(income_path, history)
        return income_data
    
    def get_income_history(self, user_id, days=90):
        """Get income history as DataFrame"""
        income_path = self.base_dir / user_id / "income_history.json"
        history = self._load_json(income_path) or []
        
        if not history:
            return pd.DataFrame()
        
        df = pd.DataFrame(history)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=True)
        
        # Filter to last N days
        cutoff = datetime.now() - timedelta(days=days)
        df = df[df['date'] >= cutoff]
        
        return df
    
    def get_income_summary(self, user_id, days=30):
        """Get income summary stats"""
        df = self.get_income_history(user_id, days)
        
        if df.empty:
            return {
                'total_income': 0,
                'avg_daily': 0,
                'days_worked': 0,
                'best_day': 0,
                'worst_day': 0
            }
        
        return {
            'total_income': round(df['income'].sum(), 2),
            'avg_daily': round(df['income'].mean(), 2),
            'days_worked': len(df),
            'best_day': round(df['income'].max(), 2),
            'worst_day': round(df['income'].min(), 2),
            'total_hours': df['hours_worked'].sum() if 'hours_worked' in df else 0
        }
    
    # ==================== SPENDING DATA ====================
    
    def add_expense(self, user_id, expense_data):
        """Add expense entry"""
        spending_path = self.base_dir / user_id / "spending_history.json"
        history = self._load_json(spending_path) or []
        
        expense_data['recorded_at'] = datetime.now().isoformat()
        if 'date' not in expense_data:
            expense_data['date'] = datetime.now().strftime('%Y-%m-%d')
        
        history.append(expense_data)
        self._save_json(spending_path, history)
        
        print(f"✅ Added expense: ₹{expense_data['amount']} ({expense_data.get('category', 'misc')})")
        return expense_data
    
    def get_spending_history(self, user_id, days=30):
        """Get spending history as DataFrame"""
        spending_path = self.base_dir / user_id / "spending_history.json"
        history = self._load_json(spending_path) or []
        
        if not history:
            return pd.DataFrame()
        
        df = pd.DataFrame(history)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=True)
        
        cutoff = datetime.now() - timedelta(days=days)
        df = df[df['date'] >= cutoff]
        
        return df
    
    def get_spending_summary(self, user_id, days=30):
        """Get spending summary"""
        df = self.get_spending_history(user_id, days)
        
        if df.empty:
            return {
                'total_spent': 0,
                'daily_average': 0,
                'by_category': {},
                'top_category': 'None'
            }
        
        by_category = df.groupby('category')['amount'].sum().to_dict()
        top_cat = max(by_category, key=by_category.get) if by_category else 'None'
        
        return {
            'total_spent': round(df['amount'].sum(), 2),
            'daily_average': round(df['amount'].sum() / days, 2),
            'by_category': by_category,
            'top_category': top_cat,
            'transaction_count': len(df)
        }
    
    # ==================== SAVINGS DATA ====================
    
    def add_savings(self, user_id, savings_data):
        """Add savings entry"""
        savings_path = self.base_dir / user_id / "savings_history.json"
        history = self._load_json(savings_path) or []
        
        savings_data['recorded_at'] = datetime.now().isoformat()
        if 'date' not in savings_data:
            savings_data['date'] = datetime.now().strftime('%Y-%m-%d')
        
        history.append(savings_data)
        self._save_json(savings_path, history)
        
        print(f"💰 Saved: ₹{savings_data['amount']}")
        return savings_data
    
    def get_savings_history(self, user_id, days=90):
        """Get savings history"""
        savings_path = self.base_dir / user_id / "savings_history.json"
        history = self._load_json(savings_path) or []
        
        if not history:
            return pd.DataFrame()
        
        df = pd.DataFrame(history)
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date', ascending=True)
    
    def get_total_savings(self, user_id):
        """Get total savings"""
        df = self.get_savings_history(user_id)
        if df.empty:
            return 0
        return round(df['amount'].sum(), 2)
    
    # ==================== GOALS ====================
    
    def set_goals(self, user_id, goals):
        """Set user goals"""
        goals_path = self.base_dir / user_id / "goals.json"
        
        # Format goals with progress tracking
        formatted_goals = []
        for goal in goals:
            if isinstance(goal, str):
                formatted_goals.append({
                    'description': goal,
                    'target_amount': self._extract_amount(goal),
                    'current_amount': 0,
                    'created_at': datetime.now().isoformat(),
                    'status': 'active'
                })
            else:
                formatted_goals.append(goal)
        
        self._save_json(goals_path, formatted_goals)
        return formatted_goals
    
    def get_goals(self, user_id):
        """Get user goals"""
        goals_path = self.base_dir / user_id / "goals.json"
        return self._load_json(goals_path) or []
    
    def update_goal_progress(self, user_id, goal_index, amount):
        """Update progress on a goal"""
        goals = self.get_goals(user_id)
        if 0 <= goal_index < len(goals):
            goals[goal_index]['current_amount'] = amount
            if goals[goal_index]['target_amount'] > 0:
                progress = (amount / goals[goal_index]['target_amount']) * 100
                goals[goal_index]['progress_percent'] = round(progress, 1)
                if progress >= 100:
                    goals[goal_index]['status'] = 'completed'
            self._save_json(self.base_dir / user_id / "goals.json", goals)
        return goals
    
    # ==================== HELPER METHODS ====================
    
    def _generate_user_id(self, name):
        """Generate unique user ID"""
        base = name.lower().replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        return f"{base}_{timestamp}"
    
    def _extract_amount(self, text):
        """Extract amount from goal text (e.g., 'Save ₹20,000' → 20000)"""
        import re
        numbers = re.findall(r'₹?([\d,]+)', text)
        if numbers:
            return int(numbers[0].replace(',', ''))
        return 0
    
    def _save_json(self, path, data):
        """Save data to JSON file"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json(self, path):
        """Load data from JSON file"""
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    # ==================== DATA EXPORT ====================
    
    def export_user_data(self, user_id):
        """Export all user data"""
        user_folder = self.base_dir / user_id
        
        return {
            'profile': self.get_user(user_id),
            'income_history': self._load_json(user_folder / "income_history.json"),
            'spending_history': self._load_json(user_folder / "spending_history.json"),
            'savings_history': self._load_json(user_folder / "savings_history.json"),
            'goals': self.get_goals(user_id)
        }
    
    def get_data_for_agents(self, user_id, income_days=90, spending_days=30):
        """
        Get data formatted for agent initialization
        Returns: (user_profile, income_df, spending_df)
        """
        profile = self.get_user(user_id)
        income_df = self.get_income_history(user_id, income_days)
        spending_df = self.get_spending_history(user_id, spending_days)
        
        return profile, income_df, spending_df


# Test
if __name__ == "__main__":
    print("🧪 Testing Storage System\n")
    
    storage = UserStorage()
    
    # Create test user
    user_data = {
        'name': 'Rajesh Kumar',
        'age': 28,
        'city': 'Bangalore',
        'platform': 'Swiggy',
        'phone': '9876543210',
        'goals': ['Save ₹20,000 emergency fund', 'Buy bike ₹60,000'],
        'savings_rate': 0.05
    }
    
    user_id = storage.create_user(user_data)
    print(f"\n✅ Created user: {user_id}")
    
    # Add some income
    for i in range(5):
        storage.add_income(user_id, {
            'date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            'income': 500 + (i * 50),
            'hours_worked': 8,
            'orders': 20 + i,
            'platform': 'Swiggy'
        })
    
    # Add some expenses
    storage.add_expense(user_id, {'amount': 150, 'category': 'food', 'description': 'Lunch'})
    storage.add_expense(user_id, {'amount': 100, 'category': 'fuel', 'description': 'Petrol'})
    
    # Add savings
    storage.add_savings(user_id, {'amount': 50, 'source': 'auto_save'})
    
    # Get summaries
    print("\n📊 Income Summary:")
    print(storage.get_income_summary(user_id))
    
    print("\n💸 Spending Summary:")
    print(storage.get_spending_summary(user_id))
    
    print("\n💰 Total Savings:", storage.get_total_savings(user_id))
    
    print("\n🎯 Goals:")
    print(storage.get_goals(user_id))
    
    print("\n✅ Storage test complete!")