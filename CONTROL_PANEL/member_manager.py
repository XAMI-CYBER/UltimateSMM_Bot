#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Member Manager
Professional Member Management System
"""

import os
import json
import csv
from datetime import datetime

class MemberManager:
    def __init__(self):
        self.members_dir = "DATA/users"
        
    def ensure_directory(self):
        """Ensure members directory exists"""
        os.makedirs(self.members_dir, exist_ok=True)
    
    def create_member(self, username, email="", phone="", plan="basic"):
        """Create new member"""
        try:
            self.ensure_directory()
            
            member_dir = os.path.join(self.members_dir, username)
            
            if os.path.exists(member_dir):
                return False, "Member already exists"
            
            os.makedirs(member_dir)
            
            # Member configuration
            member_config = {
                "username": username,
                "email": email,
                "phone": phone,
                "plan": plan,
                "status": "active",
                "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": None,
                "permissions": ["view_dashboard", "basic_operations"]
            }
            
            # Save member config
            with open(os.path.join(member_dir, "config.json"), 'w') as f:
                json.dump(member_config, f, indent=4)
            
            # Create targets file
            with open(os.path.join(member_dir, "targets.txt"), 'w') as f:
                f.write("# Member targets file\n")
            
            # Create activity log
            with open(os.path.join(member_dir, "activity_log.csv"), 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "activity", "details"])
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "account_created", "Member account created"])
            
            return True, f"Member '{username}' created successfully"
            
        except Exception as e:
            return False, f"Error creating member: {str(e)}"
    
    def delete_member(self, username):
        """Delete member"""
        try:
            member_dir = os.path.join(self.members_dir, username)
            
            if not os.path.exists(member_dir):
                return False, "Member not found"
            
            import shutil
            shutil.rmtree(member_dir)
            
            return True, f"Member '{username}' deleted successfully"
            
        except Exception as e:
            return False, f"Error deleting member: {str(e)}"
    
    def get_member_info(self, username):
        """Get member information"""
        try:
            config_file = os.path.join(self.members_dir, username, "config.json")
            
            if not os.path.exists(config_file):
                return None
            
            with open(config_file, 'r') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"Error reading member info: {e}")
            return None
    
    def list_members(self):
        """List all members with details"""
        try:
            self.ensure_directory()
            
            members = []
            for username in os.listdir(self.members_dir):
                member_dir = os.path.join(self.members_dir, username)
                if os.path.isdir(member_dir):
                    member_info = self.get_member_info(username)
                    if member_info:
                        members.append(member_info)
            
            return members
            
        except Exception as e:
            print(f"Error listing members: {e}")
            return []
    
    def update_member_status(self, username, status):
        """Update member status"""
        try:
            config_file = os.path.join(self.members_dir, username, "config.json")
            
            if not os.path.exists(config_file):
                return False, "Member not found"
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            config['status'] = status
            config['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            return True, f"Member '{username}' status updated to '{status}'"
            
        except Exception as e:
            return False, f"Error updating member status: {str(e)}"
    
    def log_activity(self, username, activity, details=""):
        """Log member activity"""
        try:
            log_file = os.path.join(self.members_dir, username, "activity_log.csv")
            
            if not os.path.exists(log_file):
                return False
            
            with open(log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    activity,
                    details
                ])
            
            return True
            
        except Exception as e:
            print(f"Error logging activity: {e}")
            return False
    
    def get_member_stats(self):
        """Get member statistics"""
        members = self.list_members()
        
        stats = {
            "total_members": len(members),
            "active_members": len([m for m in members if m.get('status') == 'active']),
            "inactive_members": len([m for m in members if m.get('status') == 'inactive']),
            "plans": {},
            "recent_join": None
        }
        
        # Count by plan
        for member in members:
            plan = member.get('plan', 'basic')
            stats['plans'][plan] = stats['plans'].get(plan, 0) + 1
        
        # Get most recent join
        if members:
            recent_member = max(members, key=lambda x: x.get('join_date', ''))
            stats['recent_join'] = recent_member.get('join_date')
        
        return stats

# Test function
def test_member_manager():
    """Test member manager functionality"""
    manager = MemberManager()
    
    # Create test member
    success, message = manager.create_member("test_user", "test@example.com", "123456789", "premium")
    print(f"Create member: {success} - {message}")
    
    # List members
    members = manager.list_members()
    print(f"Total members: {len(members)}")
    
    # Get stats
    stats = manager.get_member_stats()
    print(f"Member stats: {stats}")
    
    # Log activity
    manager.log_activity("test_user", "test_activity", "Testing activity logging")
    
    # Update status
    success, message = manager.update_member_status("test_user", "inactive")
    print(f"Update status: {success} - {message}")
    
    # Delete test member
    success, message = manager.delete_member("test_user")
    print(f"Delete member: {success} - {message}")

if __name__ == "__main__":
    test_member_manager()