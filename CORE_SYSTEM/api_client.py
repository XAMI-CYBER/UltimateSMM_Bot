#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - API Client
Professional API Integration System
"""

import requests
import json
import time
import random
from datetime import datetime

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.request_timeout = 30
        
    def make_request(self, url, method='GET', headers=None, data=None, retries=3):
        """Make HTTP request with error handling and retries"""
        try:
            request_headers = {**self.base_headers, **(headers or {})}
            
            for attempt in range(retries):
                try:
                    if method.upper() == 'GET':
                        response = self.session.get(
                            url, 
                            headers=request_headers, 
                            timeout=self.request_timeout
                        )
                    elif method.upper() == 'POST':
                        response = self.session.post(
                            url, 
                            headers=request_headers, 
                            json=data,
                            timeout=self.request_timeout
                        )
                    elif method.upper() == 'PUT':
                        response = self.session.put(
                            url, 
                            headers=request_headers, 
                            json=data,
                            timeout=self.request_timeout
                        )
                    else:
                        return False, f"Unsupported HTTP method: {method}"
                    
                    # Check if request was successful
                    if 200 <= response.status_code < 300:
                        return True, response.json() if response.content else {}
                    
                    # If not successful, wait and retry
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        
                except requests.exceptions.Timeout:
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return False, "Request timeout"
                except requests.exceptions.ConnectionError:
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return False, "Connection error"
                except requests.exceptions.RequestException as e:
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return False, f"Request error: {e}"
            
            return False, f"Request failed after {retries} attempts. Status: {response.status_code}"
            
        except Exception as e:
            return False, f"Unexpected error: {e}"
    
    def simulate_facebook_action(self, action_type, target_url, access_token):
        """Simulate Facebook API action"""
        try:
            # Simulate API call delay
            time.sleep(random.uniform(1, 3))
            
            # Simulate success (90% success rate)
            success = random.random() < 0.9
            
            if success:
                return True, {
                    "id": f"fb_{int(time.time())}",
                    "success": True,
                    "action": action_type,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return False, {
                    "error": "Simulated API error",
                    "code": "API_ERROR",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return False, f"Facebook action error: {e}"
    
    def simulate_instagram_action(self, action_type, target_url, access_token):
        """Simulate Instagram API action"""
        try:
            # Simulate API call delay
            time.sleep(random.uniform(1, 4))
            
            # Simulate success (85% success rate)
            success = random.random() < 0.85
            
            if success:
                return True, {
                    "id": f"ig_{int(time.time())}",
                    "success": True,
                    "action": action_type,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return False, {
                    "error": "Simulated API error",
                    "code": "API_ERROR", 
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return False, f"Instagram action error: {e}"
    
    def simulate_twitter_action(self, action_type, target_url, access_token):
        """Simulate Twitter API action"""
        try:
            # Simulate API call delay
            time.sleep(random.uniform(1, 2))
            
            # Simulate success (80% success rate)
            success = random.random() < 0.80
            
            if success:
                return True, {
                    "id": f"tw_{int(time.time())}",
                    "success": True,
                    "action": action_type,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return False, {
                    "error": "Simulated API error",
                    "code": "API_ERROR",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return False, f"Twitter action error: {e}"
    
    def execute_social_action(self, platform, action_type, target_url, access_token):
        """Execute social media action based on platform"""
        try:
            start_time = time.time()
            
            if platform == "facebook":
                success, result = self.simulate_facebook_action(action_type, target_url, access_token)
            elif platform == "instagram":
                success, result = self.simulate_instagram_action(action_type, target_url, access_token)
            elif platform == "twitter":
                success, result = self.simulate_twitter_action(action_type, target_url, access_token)
            else:
                return False, f"Unsupported platform: {platform}"
            
            response_time = time.time() - start_time
            
            # Add response time to result
            if isinstance(result, dict):
                result["response_time"] = round(response_time, 2)
            
            return success, result
            
        except Exception as e:
            return False, f"Social action execution error: {e}"
    
    def check_api_health(self, platform):
        """Check API health for a platform"""
        try:
            # Simulate API health check
            time.sleep(1)
            
            # Simulate health status (95% healthy)
            is_healthy = random.random() < 0.95
            
            health_data = {
                "platform": platform,
                "status": "healthy" if is_healthy else "unhealthy",
                "response_time": round(random.uniform(0.5, 2.0), 2),
                "last_checked": datetime.now().isoformat()
            }
            
            return is_healthy, health_data
            
        except Exception as e:
            return False, f"API health check error: {e}"
    
    def batch_execute_actions(self, actions):
        """Execute multiple actions in batch"""
        try:
            results = []
            
            for action in actions:
                platform = action.get('platform')
                action_type = action.get('action_type')
                target_url = action.get('target_url')
                access_token = action.get('access_token')
                
                success, result = self.execute_social_action(platform, action_type, target_url, access_token)
                
                results.append({
                    "platform": platform,
                    "action_type": action_type,
                    "success": success,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Add delay between actions to avoid rate limiting
                time.sleep(random.uniform(1, 2))
            
            return True, results
            
        except Exception as e:
            return False, f"Batch execution error: {e}"
    
    def get_rate_limits(self, platform):
        """Get rate limit information for platform"""
        try:
            # Simulated rate limit data
            rate_limits = {
                "facebook": {
                    "requests_per_hour": 200,
                    "requests_per_day": 5000,
                    "actions_per_minute": 60
                },
                "instagram": {
                    "requests_per_hour": 150,
                    "requests_per_day": 4000,
                    "actions_per_minute": 50
                },
                "twitter": {
                    "requests_per_hour": 300,
                    "requests_per_day": 10000,
                    "actions_per_minute": 80
                }
            }
            
            return rate_limits.get(platform, {})
            
        except Exception as e:
            print(f"Rate limit check error: {e}")
            return {}

# Test function
def test_api_client():
    """Test API client functionality"""
    client = APIClient()
    
    # Test Facebook action
    success, result = client.execute_social_action(
        "facebook", "like", "https://facebook.com/post/123", "fake_token"
    )
    print(f"Facebook action: {success} - {result}")
    
    # Test Instagram action  
    success, result = client.execute_social_action(
        "instagram", "comment", "https://instagram.com/p/ABC123", "fake_token"
    )
    print(f"Instagram action: {success} - {result}")
    
    # Test batch execution
    actions = [
        {
            "platform": "facebook",
            "action_type": "like",
            "target_url": "https://facebook.com/post/1",
            "access_token": "token1"
        },
        {
            "platform": "instagram", 
            "action_type": "like",
            "target_url": "https://instagram.com/p/1",
            "access_token": "token2"
        }
    ]
    
    success, results = client.batch_execute_actions(actions)
    print(f"Batch execution: {success} - {len(results)} results")
    
    # Test API health check
    healthy, health_data = client.check_api_health("facebook")
    print(f"Facebook API health: {healthy} - {health_data}")

if __name__ == "__main__":
    test_api_client()