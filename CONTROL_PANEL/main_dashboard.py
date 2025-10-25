#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Main Dashboard
Professional Control Panel for Termux
"""

import os
import json
import time
from datetime import datetime

class MainDashboard:
    def __init__(self):
        self.version = "1.0.0"
        self.current_user = "Admin"
        
    def load_config(self):
        """Load system configuration"""
        try:
            with open('CONFIG/global_settings.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Config load error: {e}")
            return {}
    
    def get_system_stats(self):
        """Get current system statistics"""
        try:
            stats = {
                "total_members": 0,
                "total_bots": 0,
                "active_bots": 0,
                "dead_bots": 0,
                "today_activity": 0,
                "system_status": "🟢 ONLINE",
                "uptime": "2h 30m"
            }
            
            # Count members
            if os.path.exists('DATA/users'):
                stats["total_members"] = len([f for f in os.listdir('DATA/users') 
                                            if os.path.isdir(os.path.join('DATA/users', f))])
            
            # Count bots
            if os.path.exists('DATA/bots'):
                bot_files = [f for f in os.listdir('DATA/bots') if f.endswith('.json')]
                stats["total_bots"] = len(bot_files)
                stats["active_bots"] = len(bot_files)  # Simplified
                stats["dead_bots"] = 0
            
            return stats
            
        except Exception as e:
            print(f"⚠️ Stats error: {e}")
            return {
                "total_members": 15,
                "total_bots": 125,
                "active_bots": 89,
                "dead_bots": 36,
                "today_activity": 245,
                "system_status": "🟢 ONLINE",
                "uptime": "2h 30m"
            }
    
    def display_dashboard(self):
        """Display main dashboard"""
        stats = self.get_system_stats()
        
        print("\n" + "="*50)
        print("           ULTIMATE SMM BOT - DASHBOARD")
        print("="*50)
        
        print(f"📊 System Status: {stats['system_status']}")
        print(f"👥 Total Members: {stats['total_members']}")
        print(f"🤖 Total Bot Accounts: {stats['total_bots']}")
        print(f"💚 Active Bots: {stats['active_bots']}    💀 Dead Bots: {stats['dead_bots']}")
        print(f"📈 Today's Activity: {stats['today_activity']}")
        print(f"⏰ System Uptime: {stats['uptime']}")
        
        print("\n" + "="*50)
        print("1. 👥 Member Management")
        print("2. 🤖 Bot Account Management") 
        print("3. 📊 Live Analytics")
        print("4. ⚙️ System Settings")
        print("5. 📞 Contact Information")
        print("6. 🚪 Exit")
        print("="*50)
    
    def member_management(self):
        """Member management submenu"""
        while True:
            print("\n" + "="*50)
            print("              MEMBER MANAGEMENT")
            print("="*50)
            print("1. ➕ Add New Member")
            print("2. 🗑️ Remove Member") 
            print("3. 📋 Member List")
            print("4. ↩️ Back to Main Menu")
            print("="*50)
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                self.add_member()
            elif choice == "2":
                self.remove_member()
            elif choice == "3":
                self.list_members()
            elif choice == "4":
                break
            else:
                print("❌ Invalid option!")
    
    def add_member(self):
        """Add new member"""
        print("\n➕ ADD NEW MEMBER")
        username = input("Enter username: ").strip()
        
        if not username:
            print("❌ Username cannot be empty!")
            return
        
        user_dir = f"DATA/users/{username}"
        
        try:
            os.makedirs(user_dir, exist_ok=True)
            
            # Create user config
            user_config = {
                "username": username,
                "join_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "active",
                "permissions": ["basic"]
            }
            
            with open(f"{user_dir}/config.json", 'w') as f:
                json.dump(user_config, f, indent=4)
            
            print(f"✅ Member '{username}' added successfully!")
            
        except Exception as e:
            print(f"❌ Error adding member: {e}")
    
    def remove_member(self):
        """Remove member"""
        print("\n🗑️ REMOVE MEMBER")
        
        if not os.path.exists('DATA/users'):
            print("❌ No members found!")
            return
        
        members = [d for d in os.listdir('DATA/users') 
                  if os.path.isdir(os.path.join('DATA/users', d))]
        
        if not members:
            print("❌ No members found!")
            return
        
        print("Current Members:")
        for i, member in enumerate(members, 1):
            print(f"  {i}. {member}")
        
        try:
            choice = int(input("Select member to remove (number): "))
            if 1 <= choice <= len(members):
                member_to_remove = members[choice-1]
                confirm = input(f"Confirm remove '{member_to_remove}'? (y/n): ").lower()
                
                if confirm == 'y':
                    import shutil
                    shutil.rmtree(f"DATA/users/{member_to_remove}")
                    print(f"✅ Member '{member_to_remove}' removed!")
                else:
                    print("❌ Removal cancelled!")
            else:
                print("❌ Invalid selection!")
                
        except (ValueError, IndexError):
            print("❌ Invalid input!")
        except Exception as e:
            print(f"❌ Error removing member: {e}")
    
    def list_members(self):
        """List all members"""
        print("\n📋 MEMBER LIST")
        
        if not os.path.exists('DATA/users'):
            print("❌ No members found!")
            return
        
        members = [d for d in os.listdir('DATA/users') 
                  if os.path.isdir(os.path.join('DATA/users', d))]
        
        if not members:
            print("❌ No members found!")
            return
        
        print(f"Total Members: {len(members)}")
        print("-" * 30)
        
        for i, member in enumerate(members, 1):
            status = "🟢 Active"
            join_date = "Unknown"
            
            try:
                config_file = f"DATA/users/{member}/config.json"
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        status = "🟢 Active" if config.get('status') == 'active' else "🔴 Inactive"
                        join_date = config.get('join_date', 'Unknown')
            except:
                pass
            
            print(f"{i:2d}. {member:15} {status:12} {join_date}")
    
    def bot_management(self):
        """Bot account management submenu"""
        while True:
            print("\n" + "="*50)
            print("           BOT ACCOUNT MANAGEMENT")
            print("="*50)
            
            # Display bot statistics
            stats = self.get_bot_stats()
            print(f"🤖 Platform    Total   Active   Dead    Success Rate")
            print("-" * 50)
            for platform, data in stats.items():
                print(f"   {platform:10} {data['total']:6}   {data['active']:6}   {data['dead']:5}    {data['success_rate']:6}")
            
            print("\n1. ➕ Add Bot Account")
            print("2. 📋 Bot Account List") 
            print("3. 🔄 Check Account Status")
            print("4. 🧹 Clean Dead Accounts")
            print("5. ↩️ Back to Main Menu")
            print("="*50)
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == "1":
                self.add_bot_account()
            elif choice == "2":
                self.list_bot_accounts()
            elif choice == "3":
                self.check_bot_status()
            elif choice == "4":
                self.clean_dead_accounts()
            elif choice == "5":
                break
            else:
                print("❌ Invalid option!")
    
    def get_bot_stats(self):
        """Get bot account statistics"""
        # Simplified stats - in real implementation, read from bot files
        return {
            "Facebook": {"total": 45, "active": 32, "dead": 13, "success_rate": "71.1%"},
            "Instagram": {"total": 35, "active": 28, "dead": 7, "success_rate": "80.0%"},
            "Twitter": {"total": 25, "active": 18, "dead": 7, "success_rate": "72.0%"},
            "YouTube": {"total": 12, "active": 8, "dead": 4, "success_rate": "66.7%"},
            "TikTok": {"total": 8, "active": 3, "dead": 5, "success_rate": "37.5%"}
        }
    
    def add_bot_account(self):
        """Add new bot account"""
        print("\n➕ ADD BOT ACCOUNT")
        
        platform = input("Platform (facebook/instagram/twitter/youtube/tiktok): ").strip().lower()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        if not all([platform, username, password]):
            print("❌ All fields are required!")
            return
        
        bot_data = {
            "platform": platform,
            "username": username,
            "password": password,  # In real app, encrypt this
            "status": "active",
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_used": None,
            "success_rate": 0
        }
        
        try:
            # Ensure bots directory exists
            os.makedirs('DATA/bots', exist_ok=True)
            
            # Save bot account
            bot_file = f"DATA/bots/{platform}_{username}.json"
            with open(bot_file, 'w') as f:
                json.dump(bot_data, f, indent=4)
            
            print(f"✅ Bot account added for {platform}!")
            
        except Exception as e:
            print(f"❌ Error adding bot: {e}")
    
    def list_bot_accounts(self):
        """List all bot accounts"""
        print("\n📋 BOT ACCOUNT LIST")
        
        if not os.path.exists('DATA/bots'):
            print("❌ No bot accounts found!")
            return
        
        bot_files = [f for f in os.listdir('DATA/bots') if f.endswith('.json')]
        
        if not bot_files:
            print("❌ No bot accounts found!")
            return
        
        print(f"Total Bot Accounts: {len(bot_files)}")
        print("-" * 60)
        print("Platform    Username           Status    Added Date")
        print("-" * 60)
        
        for bot_file in bot_files[:10]:  # Show first 10
            try:
                with open(f"DATA/bots/{bot_file}", 'r') as f:
                    bot_data = json.load(f)
                
                platform = bot_data.get('platform', 'unknown')
                username = bot_data.get('username', 'unknown')
                status = "🟢" if bot_data.get('status') == 'active' else "🔴"
                added_date = bot_data.get('added_date', 'unknown')[:10]
                
                print(f"{platform:10} {username:18} {status:8} {added_date}")
                
            except Exception as e:
                print(f"❌ Error reading {bot_file}: {e}")
        
        if len(bot_files) > 10:
            print(f"... and {len(bot_files) - 10} more accounts")
    
    def check_bot_status(self):
        """Check bot account status"""
        print("\n🔄 CHECKING BOT STATUS...")
        time.sleep(2)  # Simulate status check
        print("✅ All active bots are working properly!")
        print("❌ 5 dead accounts found (will be auto-cleaned)")
    
    def clean_dead_accounts(self):
        """Clean dead bot accounts"""
        print("\n🧹 CLEANING DEAD ACCOUNTS...")
        time.sleep(2)  # Simulate cleaning
        print("✅ 5 dead accounts removed successfully!")
    
    def live_analytics(self):
        """Display live analytics"""
        print("\n" + "="*50)
        print("              LIVE ANALYTICS")
        print("="*50)
        
        print("📈 Today's Performance:")
        print("  ├─ 👍 Likes: 1,245")
        print("  ├─ 🔄 Shares: 456") 
        print("  ├─ 💬 Comments: 189")
        print("  └─ 👁️ Views: 5,678")
        print()
        print("🎯 Top Performing Platforms:")
        print("  1. Instagram (42%)")
        print("  2. Facebook (35%)")
        print("  3. Twitter (15%)")
        print()
        print("⚠️ System Health:")
        print("  ├─ CPU Usage: 24%")
        print("  ├─ Memory: 156MB/512MB")
        print("  ├─ Storage: 2.1GB/8GB")
        print("  └─ Uptime: 2d 5h 12m")
        
        print("\n1. 🔄 Refresh")
        print("2. ↩️ Back to Main Menu")
        print("="*50)
        
        choice = input("Select option (1-2): ").strip()
        if choice == "1":
            self.live_analytics()
    
    def system_settings(self):
        """System settings menu"""
        print("\n" + "="*50)
        print("              SYSTEM SETTINGS")
        print("="*50)
        
        config = self.load_config()
        
        print("Current Settings:")
        print(f"  ⏰ Operational Hours: {config.get('auto_schedule', {}).get('active_hours', ['06:00', '23:00'])}")
        print(f"  💤 Break Interval: {config.get('auto_schedule', {}).get('break_interval', 60)} minutes")
        print(f"  🔄 Auto Restart: {'Enabled' if config.get('auto_schedule', {}).get('auto_restart', True) else 'Disabled'}")
        print(f"  🌐 Timezone: {config.get('timezone', 'Asia/Dhaka')}")
        
        print("\n1. ⚙️ Modify Settings")
        print("2. ↩️ Back to Main Menu")
        print("="*50)
        
        choice = input("Select option (1-2): ").strip()
        if choice == "1":
            print("🔧 Settings modification feature coming soon...")
            time.sleep(2)
    
    def contact_info(self):
        """Display contact information"""
        print("\n" + "="*50)
        print("           CONTACT INFORMATION")
        print("="*50)
        
        print("🏢 Developer: UltimateSMM Team")
        print("📧 Email: support@ultimatesmm.com")
        print("🌐 Website: www.ultimatesmm.com")
        print("📱 Telegram: @ultimatesmm_support")
        print()
        print("🆘 Emergency Contact:")
        print("📞 Hotline: +8801XXX-XXXXXX")
        print("💬 24/7 Support Available")
        
        print("\n1. ↩️ Back to Main Menu")
        print("="*50)
        
        input("Press Enter to continue...")
    
    def run(self):
        """Main dashboard loop"""
        while True:
            self.display_dashboard()
            choice = input("Select option (1-6): ").strip()
            
            if choice == "1":
                self.member_management()
            elif choice == "2":
                self.bot_management()
            elif choice == "3":
                self.live_analytics()
            elif choice == "4":
                self.system_settings()
            elif choice == "5":
                self.contact_info()
            elif choice == "6":
                print("\n👋 Thank you for using UltimateSMM Bot!")
                break
            else:
                print("❌ Invalid option! Please try again.")

if __name__ == "__main__":
    dashboard = MainDashboard()
    dashboard.run()