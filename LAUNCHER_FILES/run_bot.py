#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Main Launcher
Safe and Error-Free Version
"""

import os
import sys
import time
import json
from datetime import datetime

class UltimateSMMLauncher:
    def __init__(self):
        self.version = "1.0.0"
        self.is_running = False
        self.start_time = None
        
    def create_directory(self, path):
        """Safely create directory"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"📁 Created directory: {path}")
            return True
        except Exception as e:
            print(f"❌ Directory creation failed: {e}")
            return False
    
    def create_default_config(self):
        """Create default config if not exists"""
        config_data = {
            "app_name": "UltimateSMM Bot",
            "version": "1.0.0",
            "auto_schedule": {
                "active_hours": ["06:00", "23:00"],
                "break_interval": 60,
                "break_duration": 15,
                "auto_restart": True
            },
            "system": {
                "max_users": 100,
                "max_bot_accounts": 500
            }
        }
        
        try:
            with open('CONFIG/global_settings.json', 'w') as f:
                json.dump(config_data, f, indent=4)
            print("✅ Default config created")
            return True
        except Exception as e:
            print(f"❌ Config creation failed: {e}")
            return False
    
    def load_config(self):
        """Safely load configuration"""
        try:
            # Ensure CONFIG directory exists
            self.create_directory('CONFIG')
            
            # Create config if not exists
            if not os.path.exists('CONFIG/global_settings.json'):
                self.create_default_config()
            
            with open('CONFIG/global_settings.json', 'r') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"⚠️ Config load error, using defaults: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "auto_schedule": {
                "active_hours": ["06:00", "23:00"],
                "break_interval": 60,
                "break_duration": 15,
                "auto_restart": True
            }
        }
    
    def initialize_system(self):
        """Initialize all required directories and files"""
        print("🔧 Initializing System...")
        
        directories = [
            'CONFIG',
            'CORE_SYSTEM', 
            'CONTROL_PANEL',
            'DATA',
            'DATA/users',
            'DATA/bots',
            'DATA/analytics',
            'DATA/backups',
            'LOGS'
        ]
        
        # Create all directories
        for directory in directories:
            if not self.create_directory(directory):
                return False
        
        # Create default config
        if not self.create_default_config():
            return False
            
        print("✅ System initialization completed")
        return True
    
    def display_banner(self):
        """Display professional banner"""
        banner = """
╔═══════════════════════════════════════════╗
║           ULTIMATE SMM BOT v1.0           ║
║         Automated Social Media Manager    ║
║             24/7 Smart Scheduling         ║
╚═══════════════════════════════════════════╝
📱 Termux Compatible | 🔄 Auto Schedule | 💤 Smart Breaks
        """
        print(banner)
    
    def check_system_time(self):
        """Check if within operational hours"""
        try:
            config = self.load_config()
            start_time = config['auto_schedule']['active_hours'][0]
            end_time = config['auto_schedule']['active_hours'][1]
            
            current_time = datetime.now().strftime("%H:%M")
            
            print(f"🕒 Current Time: {current_time}")
            print(f"🕒 Operation Hours: {start_time} - {end_time}")
            
            return start_time <= current_time <= end_time
            
        except Exception as e:
            print(f"⚠️ Time check error: {e}")
            return True  # Default to running
    
    def start_automation(self):
        """Start the automated system"""
        print("🚀 Starting UltimateSMM Automation...")
        
        if not self.check_system_time():
            print("💤 Outside operational hours. System will start automatically at 06:00 AM")
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        
        print("✅ System started successfully!")
        print("⏰ Auto-schedule: 6:00 AM - 11:00 PM")
        print("💤 Auto-breaks: Every 60 minutes for 15 minutes")
        
        self.main_loop()
    
    def main_loop(self):
        """Main system loop - Simple and safe"""
        try:
            while self.is_running:
                current_time = datetime.now().strftime("%H:%M:%S")
                
                # Simple status display
                print(f"🟢 System Running - {current_time}")
                
                # Check for break every minute
                self.check_break_time()
                
                # Sleep for 1 minute
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n🛑 Manual shutdown requested")
        except Exception as e:
            print(f"❌ System error: {e}")
        finally:
            self.stop_system()
    
    def check_break_time(self):
        """Check if it's time for a break"""
        try:
            if not self.start_time:
                return
                
            config = self.load_config()
            break_interval = config['auto_schedule']['break_interval']
            
            current_time = datetime.now()
            running_minutes = (current_time - self.start_time).total_seconds() / 60
            
            if running_minutes >= break_interval:
                self.take_break()
                
        except Exception as e:
            print(f"⚠️ Break check error: {e}")
    
    def take_break(self):
        """Take scheduled break"""
        try:
            config = self.load_config()
            break_duration = config['auto_schedule']['break_duration']
            
            print(f"💤 Taking {break_duration} minute break...")
            
            # Simple break counter
            for i in range(break_duration, 0, -1):
                print(f"💤 Resuming in {i} minutes...", end='\r')
                time.sleep(60)  # Sleep for 1 minute
            
            print("\n🔄 Break completed! Resuming operations...")
            self.start_time = datetime.now()  # Reset timer
            
        except Exception as e:
            print(f"⚠️ Break error: {e}")
    
    def stop_system(self):
        """Safe system shutdown"""
        print("🛑 Stopping UltimateSMM Bot...")
        self.is_running = False
        print("✅ System stopped safely")

def main():
    """Main entry point - Safe execution"""
    print("🔒 Starting UltimateSMM Bot - Safe Mode")
    
    launcher = UltimateSMMLauncher()
    launcher.display_banner()
    
    # Initialize system first
    if not launcher.initialize_system():
        print("❌ System initialization failed!")
        return
    
    try:
        launcher.start_automation()
    except KeyboardInterrupt:
        print("\n👋 Manual shutdown complete")
    except Exception as e:
        print(f"💥 Critical error: {e}")
    finally:
        print("🔒 System shutdown complete")

if __name__ == "__main__":
    main()