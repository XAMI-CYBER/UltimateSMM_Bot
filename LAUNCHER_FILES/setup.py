#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Safe Setup Script
Safe Installation Process
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(command, description):
    """Safely run system command"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    requirements = [
        "colorama==0.4.6",
        "requests==2.31.0",
        "psutil==5.9.6",
        "schedule==1.2.0"
    ]
    
    print("📦 Installing requirements...")
    
    for package in requirements:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            return False
    
    return True

def setup_directories():
    """Create required directories"""
    directories = [
        '../CONFIG',
        '../CORE_SYSTEM',
        '../CONTROL_PANEL', 
        '../DATA/users',
        '../DATA/bots',
        '../DATA/analytics',
        '../DATA/backups',
        '../LOGS'
    ]
    
    print("📁 Creating directories...")
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}")
        except Exception as e:
            print(f"❌ Failed to create {directory}: {e}")
            return False
    
    return True

def create_config_files():
    """Create default configuration files for safe version"""
    print("⚙️ Creating safe config files...")
    
    try:
        # Copy the updated config files we created above
        configs = {
            '../CONFIG/global_settings.json': {
                "app_name": "UltimateSMM Bot - Safe Version",
                "version": "2.0.0",
                "operation_mode": "safe_slow",
                "safety_limits": {
                    "facebook": {"daily_per_bot": 20, "hourly_per_bot": 2},
                    "youtube": {"daily_per_bot": 15, "hourly_per_bot": 2},
                    "tiktok": {"daily_per_bot": 25, "hourly_per_bot": 3}
                }
            },
            '../CONFIG/auto_schedule.json': {
                "operation_mode": "safe_slow",
                "operational_hours": {
                    "start_time": "06:00",
                    "end_time": "22:00"
                }
            },
            '../CONFIG/safety_rules.json': {
                "operation_mode": "safe_slow",
                "platform_limits": {
                    "facebook": {"daily_per_bot": 20},
                    "youtube": {"daily_per_bot": 15},
                    "tiktok": {"daily_per_bot": 25}
                }
            }
        }
        
        for config_file, config_data in configs.items():
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
            print(f"✅ Created: {config_file}")
        
        return True
            
    except Exception as e:
        print(f"❌ Failed to create configs: {e}")
        return False

def set_permissions():
    """Set file permissions"""
    print("🔒 Setting file permissions...")
    
    try:
        # Make Python scripts executable
        scripts = [
            'run_bot.py',
            'safe_smm_bot.py',
            '../CONTROL_PANEL/main_dashboard.py',
            '../CORE_SYSTEM/scheduler.py'
        ]
        
        for script in scripts:
            if os.path.exists(script):
                os.chmod(script, 0o755)
                print(f"✅ Executable: {script}")
        
        return True
        
    except Exception as e:
        print(f"❌ Permission setting failed: {e}")
        return False

def main():
    """Main setup function"""
    print("""
╔═══════════════════════════════════════════╗
║      ULTIMATE SMM BOT - SAFE SETUP       ║
║         Account Protection Focus         ║
╚═══════════════════════════════════════════╝
    """)
    
    # Check Python
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not setup_directories():
        sys.exit(1)
    
    # Create config files
    if not create_config_files():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("⚠️ Some packages failed, but continuing...")
    
    # Set permissions
    set_permissions()
    
    print("\n🎉 SAFE SETUP COMPLETED SUCCESSFULLY!")
    print("\n📖 Safe Operation Guide:")
    print("   1. Run: python safe_smm_bot.py")
    print("   2. Bot Lifespan: 6-12 months target")
    print("   3. Daily Limits: 20 (FB), 15 (YT), 25 (TT) per bot")
    print("   4. Growth: Slow & steady - account protection first")
    print("\n🛡️  Safety Features:")
    print("   • Health monitoring for all bots")
    print("   • Automatic capacity management")
    print("   • Safe delays between actions")
    print("   • Bot rotation and recovery")

if __name__ == "__main__":
    main()