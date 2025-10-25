#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Bot Manager
Professional Bot Account Management
"""

import os
import json
import hashlib
from datetime import datetime, timedelta

class BotManager:
    def __init__(self):
        self.bots_dir = "DATA/bots"
        self.platforms = ["facebook", "instagram", "twitter", "youtube", "tiktok"]
    
    def ensure_directory(self):
        """Ensure bots directory exists"""
        os.makedirs(self.bots_dir, exist_ok=True)
    
    def encrypt_password(self, password):
        """Simple password encryption (for demo purposes)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_bot_account(self, platform, username, password, email="", extra_info=None):
        """Add new bot account"""
        try:
            self.ensure_directory()
            
            if platform not in self.platforms:
                return False, f"Unsupported platform. Supported: {', '.join(self.platforms)}"
            
            bot_id = f"{platform}_{username}"
            bot_file = os.path.join(self.bots_dir, f"{bot_id}.json")
            
            if os.path.exists(bot_file):
                return False, "Bot account already exists"
            
            bot_data = {
                "id": bot_id,
                "platform": platform,
                "username": username,
                "password": self.encrypt_password(password),
                "email": email,
                "status": "active",
                "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_used": None,
                "success_rate": 100,
                "total_actions": 0,
                "failed_actions": 0,
                "extra_info": extra_info or {}
            }
            
            with open(bot_file, 'w') as f:
                json.dump(bot_data, f, indent=4)
            
            return True, f"Bot account added for {platform}"
            
        except Exception as e:
            return False, f"Error adding bot: {str(e)}"
    
    def remove_bot_account(self, bot_id):
        """Remove bot account"""
        try:
            bot_file = os.path.join(self.bots_dir, f"{bot_id}.json")
            
            if not os.path.exists(bot_file):
                return False, "Bot account not found"
            
            os.remove(bot_file)
            return True, f"Bot account '{bot_id}' removed"
            
        except Exception as e:
            return False, f"Error removing bot: {str(e)}"
    
    def get_bot_account(self, bot_id):
        """Get bot account information"""
        try:
            bot_file = os.path.join(self.bots_dir, f"{bot_id}.json")
            
            if not os.path.exists(bot_file):
                return None
            
            with open(bot_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error reading bot account: {e}")
            return None
    
    def list_bot_accounts(self, platform=None):
        """List all bot accounts"""
        try:
            self.ensure_directory()
            
            bots = []
            for filename in os.listdir(self.bots_dir):
                if filename.endswith('.json'):
                    bot_file = os.path.join(self.bots_dir, filename)
                    with open(bot_file, 'r') as f:
                        bot_data = json.load(f)
                    
                    if platform is None or bot_data.get('platform') == platform:
                        bots.append(bot_data)
            
            return bots
            
        except Exception as e:
            print(f"Error listing bots: {e}")
            return []
    
    def update_bot_status(self, bot_id, status):
        """Update bot account status"""
        try:
            bot_file = os.path.join(self.bots_dir, f"{bot_id}.json")
            
            if not os.path.exists(bot_file):
                return False, "Bot account not found"
            
            with open(bot_file, 'r') as f:
                bot_data = json.load(f)
            
            bot_data['status'] = status
            bot_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(bot_file, 'w') as f:
                json.dump(bot_data, f, indent=4)
            
            return True, f"Bot '{bot_id}' status updated to '{status}'"
            
        except Exception as e:
            return False, f"Error updating bot status: {str(e)}"
    
    def check_bot_health(self, bot_id):
        """Check bot account health"""
        try:
            bot_data = self.get_bot_account(bot_id)
            if not bot_data:
                return False, "Bot account not found"
            
            # Simulate health check
            import random
            is_healthy = random.choice([True, True, True, False])  # 75% healthy
            
            if is_healthy:
                return True, "Bot is healthy and active"
            else:
                # Mark as dead if unhealthy
                self.update_bot_status(bot_id, "dead")
                return False, "Bot is not responding"
                
        except Exception as e:
            return False, f"Error checking bot health: {str(e)}"
    
    def get_bot_stats(self):
        """Get bot account statistics"""
        bots = self.list_bot_accounts()
        
        stats = {
            "total_bots": len(bots),
            "active_bots": len([b for b in bots if b.get('status') == 'active']),
            "dead_bots": len([b for b in bots if b.get('status') == 'dead']),
            "suspended_bots": len([b for b in bots if b.get('status') == 'suspended']),
            "by_platform": {},
            "total_actions": 0,
            "success_rate": 0
        }
        
        # Calculate platform distribution
        for bot in bots:
            platform = bot.get('platform', 'unknown')
            stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1
            
            stats['total_actions'] += bot.get('total_actions', 0)
        
        # Calculate overall success rate
        if bots:
            total_success = sum(b.get('success_rate', 0) for b in bots)
            stats['success_rate'] = total_success / len(bots)
        
        return stats
    
    def clean_dead_bots(self):
        """Clean dead bot accounts"""
        try:
            dead_bots = [b for b in self.list_bot_accounts() if b.get('status') == 'dead']
            
            for bot in dead_bots:
                self.remove_bot_account(bot['id'])
            
            return True, f"Cleaned {len(dead_bots)} dead bot accounts"
            
        except Exception as e:
            return False, f"Error cleaning dead bots: {str(e)}"
    
    def rotate_accounts(self):
        """Rotate bot accounts for better distribution"""
        try:
            active_bots = [b for b in self.list_bot_accounts() if b.get('status') == 'active']
            
            # Simulate account rotation
            print(f"🔄 Rotating {len(active_bots)} active bot accounts...")
            
            return True, f"Account rotation completed for {len(active_bots)} bots"
            
        except Exception as e:
            return False, f"Error rotating accounts: {str(e)}"

# Test function
def test_bot_manager():
    """Test bot manager functionality"""
    manager = BotManager()
    
    # Add test bot
    success, message = manager.add_bot_account(
        "facebook", 
        "test_user", 
        "test_password", 
        "test@example.com"
    )
    print(f"Add bot: {success} - {message}")
    
    # List bots
    bots = manager.list_bot_accounts()
    print(f"Total bots: {len(bots)}")
    
    # Get stats
    stats = manager.get_bot_stats()
    print(f"Bot stats: {stats}")
    
    # Check health
    if bots:
        health, health_msg = manager.check_bot_health(bots[0]['id'])
        print(f"Health check: {health} - {health_msg}")
    
    # Clean dead bots
    success, message = manager.clean_dead_bots()
    print(f"Clean dead bots: {success} - {message}")
    
    # Remove test bot
    if bots:
        success, message = manager.remove_bot_account(bots[0]['id'])
        print(f"Remove bot: {success} - {message}")

if __name__ == "__main__":
    test_bot_manager()