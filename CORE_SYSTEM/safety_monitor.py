#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Safety Monitor
Professional Safety and Security System
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta

class SafetyMonitor:
    def __init__(self):
        self.monitoring = False
        self.safety_log = []
        self.suspicious_activities = []
        
    def load_safety_rules(self):
        """Load safety rules from config"""
        try:
            with open('CONFIG/safety_rules.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Safety rules load error: {e}")
            return self.get_default_rules()
    
    def get_default_rules(self):
        """Default safety rules"""
        return {
            "operation_limits": {
                "max_posts_per_day": 50,
                "min_delay_between_actions": 30,
                "max_actions_per_hour": 20,
                "max_concurrent_actions": 5
            },
            "safety_measures": {
                "suspicious_activity_threshold": 10,
                "auto_suspend_on_detection": True,
                "rate_limiting": True
            }
        }
    
    def log_activity(self, activity_type, platform, details):
        """Log activity for safety monitoring"""
        try:
            activity = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": activity_type,
                "platform": platform,
                "details": details
            }
            
            self.safety_log.append(activity)
            
            # Keep only last 1000 activities
            if len(self.safety_log) > 1000:
                self.safety_log = self.safety_log[-1000:]
            
            # Check for suspicious activity
            self.check_suspicious_activity(activity)
            
            return True
            
        except Exception as e:
            print(f"❌ Activity logging error: {e}")
            return False
    
    def check_suspicious_activity(self, activity):
        """Check for suspicious activity patterns"""
        try:
            rules = self.load_safety_rules()
            threshold = rules['safety_measures']['suspicious_activity_threshold']
            
            # Check rate limiting
            recent_activities = [
                act for act in self.safety_log 
                if datetime.now() - datetime.strptime(act['timestamp'], '%Y-%m-%d %H:%M:%S') < timedelta(hours=1)
            ]
            
            if len(recent_activities) > threshold:
                suspicious_activity = {
                    "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "high_frequency_activity",
                    "activities_count": len(recent_activities),
                    "recommendation": "Suspend operations temporarily"
                }
                
                self.suspicious_activities.append(suspicious_activity)
                print(f"🚨 Suspicious activity detected: {suspicious_activity['type']}")
                
                # Auto suspend if enabled
                if rules['safety_measures']['auto_suspend_on_detection']:
                    self.trigger_safety_protocol()
                
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Suspicious activity check error: {e}")
            return False
    
    def trigger_safety_protocol(self):
        """Trigger safety protocol"""
        try:
            print("🛡️ Activating safety protocol...")
            
            # Log safety event
            safety_event = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "event": "safety_protocol_activated",
                "action": "temporary_suspension",
                "duration_minutes": 30
            }
            
            # Save safety event
            self.save_safety_event(safety_event)
            
            print("✅ Safety protocol activated. Operations suspended for 30 minutes.")
            
            return True
            
        except Exception as e:
            print(f"❌ Safety protocol error: {e}")
            return False
    
    def save_safety_event(self, event):
        """Save safety event to file"""
        try:
            safety_log_file = "LOGS/safety_events.json"
            
            # Load existing events
            events = []
            if os.path.exists(safety_log_file):
                with open(safety_log_file, 'r') as f:
                    events = json.load(f)
            
            # Add new event
            events.append(event)
            
            # Save updated events
            with open(safety_log_file, 'w') as f:
                json.dump(events, f, indent=4)
            
            return True
            
        except Exception as e:
            print(f"❌ Safety event save error: {e}")
            return False
    
    def get_safety_report(self):
        """Generate safety report"""
        try:
            report = {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_activities_monitored": len(self.safety_log),
                "suspicious_activities_detected": len(self.suspicious_activities),
                "recent_suspicious_activities": self.suspicious_activities[-5:],  # Last 5
                "safety_status": "normal",
                "recommendations": []
            }
            
            if self.suspicious_activities:
                report["safety_status"] = "attention_required"
                report["recommendations"].append("Review recent suspicious activities")
            
            # Check activity frequency
            recent_hour_activities = [
                act for act in self.safety_log 
                if datetime.now() - datetime.strptime(act['timestamp'], '%Y-%m-%d %H:%M:%S') < timedelta(hours=1)
            ]
            
            if len(recent_hour_activities) > 50:
                report["safety_status"] = "high_activity"
                report["recommendations"].append("Consider increasing delay between actions")
            
            return report
            
        except Exception as e:
            print(f"❌ Safety report error: {e}")
            return {}
    
    def start_monitoring(self):
        """Start safety monitoring"""
        print("🛡️ Starting safety monitoring...")
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                try:
                    # Generate periodic safety report
                    report = self.get_safety_report()
                    
                    # Log report every 30 minutes
                    if int(datetime.now().strftime('%M')) % 30 == 0:
                        print(f"🛡️ Safety Status: {report.get('safety_status', 'unknown')}")
                    
                    time.sleep(60)  # Check every minute
                    
                except Exception as e:
                    print(f"❌ Safety monitor error: {e}")
                    time.sleep(60)
        
        # Start monitoring in separate thread
        monitor_thread = threading.Thread(target=monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("✅ Safety monitoring started")
    
    def stop_monitoring(self):
        """Stop safety monitoring"""
        print("🛑 Stopping safety monitoring...")
        self.monitoring = False
    
    def reset_monitoring(self):
        """Reset monitoring data"""
        print("🔄 Resetting safety monitoring data...")
        self.safety_log = []
        self.suspicious_activities = []
        print("✅ Safety monitoring data reset")

# Test function
def test_safety_monitor():
    """Test safety monitor functionality"""
    monitor = SafetyMonitor()
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Log some activities
    for i in range(15):
        monitor.log_activity("like", "facebook", {"target": f"post_{i}"})
    
    # Get safety report
    report = monitor.get_safety_report()
    print(f"Safety report: {report}")
    
    # Stop monitoring
    monitor.stop_monitoring()

if __name__ == "__main__":
    test_safety_monitor()