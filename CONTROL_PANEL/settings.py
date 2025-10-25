#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Settings Manager
Professional Settings Management System
"""

import os
import json
import shutil
from datetime import datetime

class SettingsManager:
    def __init__(self):
        self.config_dir = "CONFIG"
        self.backup_dir = "DATA/backups"
    
    def ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def load_settings(self, settings_file):
        """Load settings from file"""
        try:
            filepath = os.path.join(self.config_dir, settings_file)
            
            if not os.path.exists(filepath):
                return None
            
            with open(filepath, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error loading settings from {settings_file}: {e}")
            return None
    
    def save_settings(self, settings_file, settings_data):
        """Save settings to file"""
        try:
            self.ensure_directories()
            
            filepath = os.path.join(self.config_dir, settings_file)
            
            # Create backup before saving
            self.backup_config(settings_file)
            
            with open(filepath, 'w') as f:
                json.dump(settings_data, f, indent=4)
            
            return True, "Settings saved successfully"
            
        except Exception as e:
            return False, f"Error saving settings: {str(e)}"
    
    def backup_config(self, config_file):
        """Create backup of configuration file"""
        try:
            source = os.path.join(self.config_dir, config_file)
            if not os.path.exists(source):
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{config_file}.backup_{timestamp}"
            destination = os.path.join(self.backup_dir, backup_file)
            
            shutil.copy2(source, destination)
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_config(self, config_file, backup_file):
        """Restore configuration from backup"""
        try:
            source = os.path.join(self.backup_dir, backup_file)
            destination = os.path.join(self.config_dir, config_file)
            
            if not os.path.exists(source):
                return False, "Backup file not found"
            
            # Create backup of current config
            self.backup_config(config_file)
            
            shutil.copy2(source, destination)
            return True, "Configuration restored successfully"
            
        except Exception as e:
            return False, f"Error restoring configuration: {str(e)}"
    
    def list_backups(self, config_file):
        """List available backups for a configuration file"""
        try:
            if not os.path.exists(self.backup_dir):
                return []
            
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith(f"{config_file}.backup_"):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    backups.append({
                        "filename": filename,
                        "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                        "size": stat.st_size
                    })
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x["created"], reverse=True)
            return backups
            
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []
    
    def get_system_info(self):
        """Get system information"""
        try:
            import platform
            import psutil
            
            system_info = {
                "python_version": platform.python_version(),
                "system": platform.system(),
                "processor": platform.processor(),
                "hostname": platform.node(),
                "cpu_cores": psutil.cpu_count(),
                "total_memory": round(psutil.virtual_memory().total / (1024**3), 2),  # GB
                "available_memory": round(psutil.virtual_memory().available / (1024**3), 2),
                "disk_usage": {
                    "total": round(psutil.disk_usage('.').total / (1024**3), 2),
                    "used": round(psutil.disk_usage('.').used / (1024**3), 2),
                    "free": round(psutil.disk_usage('.').free / (1024**3), 2)
                }
            }
            
            return system_info
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            return {
                "python_version": platform.python_version(),
                "system": platform.system(),
                "error": "Detailed system info unavailable"
            }
    
    def update_auto_schedule(self, new_schedule):
        """Update auto-schedule settings"""
        try:
            schedule_file = os.path.join(self.config_dir, "auto_schedule.json")
            
            if os.path.exists(schedule_file):
                with open(schedule_file, 'r') as f:
                    current_schedule = json.load(f)
            else:
                current_schedule = {}
            
            # Update schedule settings
            current_schedule.update(new_schedule)
            current_schedule['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(schedule_file, 'w') as f:
                json.dump(current_schedule, f, indent=4)
            
            return True, "Auto-schedule updated successfully"
            
        except Exception as e:
            return False, f"Error updating auto-schedule: {str(e)}"
    
    def update_safety_rules(self, new_rules):
        """Update safety rules"""
        try:
            rules_file = os.path.join(self.config_dir, "safety_rules.json")
            
            if os.path.exists(rules_file):
                with open(rules_file, 'r') as f:
                    current_rules = json.load(f)
            else:
                current_rules = {}
            
            # Update safety rules
            current_rules.update(new_rules)
            current_rules['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(rules_file, 'w') as f:
                json.dump(current_rules, f, indent=4)
            
            return True, "Safety rules updated successfully"
            
        except Exception as e:
            return False, f"Error updating safety rules: {str(e)}"
    
    def cleanup_old_backups(self, days_to_keep=7):
        """Clean up old backup files"""
        try:
            if not os.path.exists(self.backup_dir):
                return True, "No backups to clean"
            
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            deleted_count = 0
            
            for filename in os.listdir(self.backup_dir):
                filepath = os.path.join(self.backup_dir, filename)
                if os.path.isfile(filepath) and os.stat(filepath).st_mtime < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
            
            return True, f"Cleaned up {deleted_count} old backups"
            
        except Exception as e:
            return False, f"Error cleaning up backups: {str(e)}"

# Test function
def test_settings_manager():
    """Test settings manager functionality"""
    manager = SettingsManager()
    
    # Get system info
    system_info = manager.get_system_info()
    print(f"System info: {system_info}")
    
    # List backups
    backups = manager.list_backups("global_settings.json")
    print(f"Available backups: {len(backups)}")
    
    # Update auto-schedule
    new_schedule = {
        "operational_hours": {
            "start_time": "07:00",
            "end_time": "22:00"
        }
    }
    success, message = manager.update_auto_schedule(new_schedule)
    print(f"Update schedule: {success} - {message}")
    
    # Cleanup old backups
    success, message = manager.cleanup_old_backups()
    print(f"Cleanup backups: {success} - {message}")

if __name__ == "__main__":
    test_settings_manager()