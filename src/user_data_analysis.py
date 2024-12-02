import redis
import json
import pandas as pd
import matplotlib.pyplot as plt

class UserDataAnalyzer:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    
    def fetch_user_data(self):
        # Fetch all user keys from Redis
        user_keys = self.redis_client.keys('postgres.public.users:*')
        
        # Collect user data
        users = []
        for key in user_keys:
            user_data = self.redis_client.get(key)
            if user_data:
                try:
                    user = json.loads(user_data)
                    users.append(user)
                except json.JSONDecodeError:
                    print(f"Could not parse user data from key {key}")
        
        return pd.DataFrame(users)
    
    def analyze_users(self):
        # Fetch user data
        df = self.fetch_user_data()
        
        if df.empty:
            print("No user data found in Redis")
            return
        
        # Average Age by City
        avg_age_by_city = df.groupby('city')['age'].mean()
        print("Average Age by City:")
        print(avg_age_by_city)
        
        # Age Distribution
        plt.figure(figsize=(10, 6))
        df['age'].hist(bins=20)
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.savefig('age_distribution.png')
        plt.close()
        
        # City-wise Age Distribution
        plt.figure(figsize=(12, 6))
        df.boxplot(column='age', by='city')
        plt.title('Age Distribution by City')
        plt.suptitle('')
        plt.xlabel('City')
        plt.ylabel('Age')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('age_distribution_by_city.png')
        plt.close()

if __name__ == "__main__":
    analyzer = UserDataAnalyzer()
    analyzer.analyze_users()