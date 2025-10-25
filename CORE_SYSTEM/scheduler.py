#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Smart Scheduler
Safe and Automated Task Management
"""

import time
import json
import threading
from datetime import datetime, timedelta

class AutomationScheduler:
    def __init__(self):
        self.is_running = False
        self.tasks = []
        self.break_mode = False
        self.last_break_time = None
        
    def load_config(self):
        """Load scheduler configuration"""
        try:
            with open('CONFIG/auto_schedule.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Scheduler config error: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Default scheduler configuration"""
        return {
            "operational_hours": {
                "start_time": "06:00",
                "end_time": "23:00",
                "enabled": True
            },
            "break_schedule": [
                {"after_minutes": 60, "break_minutes": 15, "enabled": True}
            ]
        }
    
    def is_within_operational_hours(self):
        """Check if current time is within operational hours"""
        try:
            config = self.load_config()
            if not config['operational_hours']['enabled']:
                return True
            
            current_time = datetime.now().strftime("%H:%M")
            start_time = config['operational_hours']['start_time']
            end_time = config['operational_hours']['end_time']
            
            return start_time <= current_time <= end_time
            
        except Exception as e:
            print(f"⚠️ Operational hours check error: {e}")
            return True
    
    def should_take_break(self, start_time):
        """Check if break is needed"""
        try:
            if self.break_mode:
                return False
                
            config = self.load_config()
            break_schedules = config.get('break_schedule', [])
            
            current_time = datetime.now()
            running_minutes = (current_time - start_time).total_seconds() / 60
            
            for schedule in break_schedules:
                if (schedule['enabled'] and 
                    running_minutes >= schedule['after_minutes'] and
                    (not self.last_break_time or 
                     (current_time - self.last_break_time).total_seconds() / 60 >= schedule['after_minutes'])):
                    return schedule
            
            return None
            
        except Exception as e:
            print(f"⚠️ Break check error: {e}")
            return None
    
    def take_break(self, break_schedule):
        """Execute break period"""
        try:
            self.break_mode = True
            break_minutes = break_schedule['break_minutes']
            
            print(f"💤 Taking scheduled break for {break_minutes} minutes...")
            
            # Break countdown
            for remaining in range(break_minutes, 0, -1):
                if not self.is_running:
                    break
                print(f"   ⏳ Resuming in {remaining} minutes...", end='\r')
                time.sleep(60)
            
            if self.is_running:
                print("\n🔄 Break completed! Resuming operations...")
                self.break_mode = False
                self.last_break_time = datetime.now()
                
        except Exception as e:
            print(f"⚠️ Break execution error: {e}")
            self.break_mode = False
    
    def add_task(self, task_name, task_function, interval_minutes=60):
        """Add a scheduled task"""
        task = {
            'name': task_name,
            'function': task_function,
            'interval': interval_minutes,
            'last_run': None
        }
        self.tasks.append(task)
        print(f"✅ Task added: {task_name} (every {interval_minutes} minutes)")
    
    def run_tasks(self):
        """Execute pending tasks"""
        if self.break_mode or not self.is_within_operational_hours():
            return
        
        current_time = datetime.now()
        
        for task in self.tasks:
            try:
                if (task['last_run'] is None or 
                    (current_time - task['last_run']).total_seconds() >= task['interval'] * 60):
                    
                    print(f"🔄 Running task: {task['name']}")
                    task['function']()
                    task['last_run'] = current_time
                    
            except Exception as e:
                print(f"❌ Task {task['name']} failed: {e}")
    
    def start(self):
        """Start the scheduler"""
        print("⏰ Starting Smart Scheduler...")
        self.is_running = True
        start_time = datetime.now()
        
        while self.is_running:
            try:
                # Check operational hours
                if not self.is_within_operational_hours():
                    print("💤 Outside operational hours. Waiting...")
                    time.sleep(300)  # Wait 5 minutes
                    continue
                
                # Check for breaks
                break_schedule = self.should_take_break(start_time)
                if break_schedule:
                    self.take_break(break_schedule)
                    start_time = datetime.now()  # Reset start time after break
                    continue
                
                # Run tasks
                self.run_tasks()
                
                # Wait before next check
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                time.sleep(60)
    
    def stop(self):
        """Stop the scheduler"""
        print("🛑 Stopping scheduler...")
        self.is_running = False

# Example task functions
def health_check_task():
    """Example health check task"""
    print("❤️ Performing health check...")

def backup_task():
    """Example backup task"""
    print("💾 Creating system backup...")

def cleanup_task():
    """Example cleanup task"""
    print("🧹 Cleaning temporary files...")

if __name__ == "__main__":
    # Test the scheduler
    scheduler = AutomationScheduler()
    scheduler.add_task("Health Check", health_check_task, 30)
    scheduler.add_task("Backup", backup_task, 120)
    scheduler.add_task("Cleanup", cleanup_task, 240)
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.stop()