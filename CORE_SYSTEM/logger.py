#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Logger System
Professional Logging Management
"""

import os
import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

class UltimateLogger:
    def __init__(self):
        self.logs_dir = "LOGS"
        self.setup_logging()
    
    def setup_logging(self):
        """Setup professional logging system"""
        try:
            # Create logs directory
            os.makedirs(self.logs_dir, exist_ok=True)
            
            # Configure root logger
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            
            # Clear existing handlers
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            
            # System log handler
            system_handler = RotatingFileHandler(
                os.path.join(self.logs_dir, 'system.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            system_handler.setLevel(logging.INFO)
            
            # Error log handler
            error_handler = RotatingFileHandler(
                os.path.join(self.logs_dir, 'errors.log'),
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3
            )
            error_handler.setLevel(logging.ERROR)
            
            # Activity log handler
            activity_handler = RotatingFileHandler(
                os.path.join(self.logs_dir, 'activity.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            activity_handler.setLevel(logging.INFO)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            system_handler.setFormatter(formatter)
            error_handler.setFormatter(formatter)
            activity_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers
            logger.addHandler(system_handler)
            logger.addHandler(error_handler)
            logger.addHandler(activity_handler)
            logger.addHandler(console_handler)
            
            print("✅ Logging system initialized")
            
        except Exception as e:
            print(f"❌ Logging setup error: {e}")
    
    def log_system_event(self, event_type, message, details=None):
        """Log system events"""
        try:
            logger = logging.getLogger('system')
            
            log_data = {
                "event": event_type,
                "message": message,
                "details": details or {},
                "timestamp": datetime.now().isoformat()
            }
            
            if event_type == "error":
                logger.error(json.dumps(log_data))
            elif event_type == "warning":
                logger.warning(json.dumps(log_data))
            else:
                logger.info(json.dumps(log_data))
            
            return True
            
        except Exception as e:
            print(f"❌ System event logging error: {e}")
            return False
    
    def log_activity(self, activity_type, platform, user, details=None):
        """Log user activities"""
        try:
            logger = logging.getLogger('activity')
            
            activity_data = {
                "activity": activity_type,
                "platform": platform,
                "user": user,
                "details": details or {},
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(json.dumps(activity_data))
            
            return True
            
        except Exception as e:
            print(f"❌ Activity logging error: {e}")
            return False
    
    def log_performance(self, operation, duration, success=True, details=None):
        """Log performance metrics"""
        try:
            logger = logging.getLogger('performance')
            
            performance_data = {
                "operation": operation,
                "duration_seconds": duration,
                "success": success,
                "details": details or {},
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(json.dumps(performance_data))
            
            return True
            
        except Exception as e:
            print(f"❌ Performance logging error: {e}")
            return False
    
    def get_log_stats(self, log_type="system", hours=24):
        """Get log statistics"""
        try:
            log_file = os.path.join(self.logs_dir, f'{log_type}.log')
            
            if not os.path.exists(log_file):
                return {"error": "Log file not found"}
            
            stats = {
                "total_entries": 0,
                "errors": 0,
                "warnings": 0,
                "info": 0,
                "last_activity": None
            }
            
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        stats["total_entries"] += 1
                        
                        # Count by level
                        if "ERROR" in line:
                            stats["errors"] += 1
                        elif "WARNING" in line:
                            stats["warnings"] += 1
                        else:
                            stats["info"] += 1
                            
                        # Get last activity
                        if not stats["last_activity"]:
                            stats["last_activity"] = log_entry.get("timestamp")
                            
                    except json.JSONDecodeError:
                        continue
            
            return stats
            
        except Exception as e:
            return {"error": f"Log stats error: {e}"}
    
    def cleanup_old_logs(self, days_to_keep=7):
        """Clean up old log files"""
        try:
            import glob
            
            current_time = datetime.now().timestamp()
            cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
            deleted_count = 0
            
            # Find all log files
            log_files = glob.glob(os.path.join(self.logs_dir, "*.log.*"))  # Rotated files
            
            for log_file in log_files:
                if os.path.isfile(log_file) and os.path.getmtime(log_file) < cutoff_time:
                    os.remove(log_file)
                    deleted_count += 1
            
            return True, f"Cleaned up {deleted_count} old log files"
            
        except Exception as e:
            return False, f"Log cleanup error: {e}"
    
    def export_logs(self, log_type="system", output_format="json"):
        """Export logs for analysis"""
        try:
            log_file = os.path.join(self.logs_dir, f'{log_type}.log')
            
            if not os.path.exists(log_file):
                return False, "Log file not found"
            
            export_data = []
            
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        export_data.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
            
            # Save exported data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = os.path.join(self.logs_dir, f'export_{log_type}_{timestamp}.{output_format}')
            
            with open(export_file, 'w') as f:
                if output_format == "json":
                    json.dump(export_data, f, indent=2)
                else:
                    # Simple text format
                    for entry in export_data:
                        f.write(f"{entry.get('timestamp')} - {entry.get('message', '')}\n")
            
            return True, f"Logs exported to {export_file}"
            
        except Exception as e:
            return False, f"Log export error: {e}"

# Global logger instance
logger = UltimateLogger()

# Test function
def test_logger():
    """Test logger functionality"""
    # Log different types of events
    logger.log_system_event("info", "System started successfully")
    logger.log_system_event("warning", "High memory usage detected", {"memory_usage": "85%"})
    logger.log_system_event("error", "Database connection failed", {"error_code": "DB_001"})
    
    # Log activities
    logger.log_activity("like", "facebook", "user123", {"target": "post_456"})
    logger.log_activity("share", "instagram", "user456", {"target": "story_789"})
    
    # Log performance
    logger.log_performance("api_call", 2.5, True, {"endpoint": "/posts"})
    
    # Get stats
    stats = logger.get_log_stats("system")
    print(f"System log stats: {stats}")
    
    # Export logs
    success, message = logger.export_logs("system", "json")
    print(f"Log export: {success} - {message}")

if __name__ == "__main__":
    test_logger()