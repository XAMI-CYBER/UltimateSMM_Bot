#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UltimateSMM Bot - Database Manager
Professional Data Management System
"""

import os
import json
import sqlite3
import pandas as pd
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.data_dir = "DATA"
        self.db_file = os.path.join(self.data_dir, "smm_bot.db")
        self.setup_database()
    
    def setup_database(self):
        """Setup SQLite database and tables"""
        try:
            # Ensure data directory exists
            os.makedirs(self.data_dir, exist_ok=True)
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    phone TEXT,
                    plan TEXT DEFAULT 'basic',
                    status TEXT DEFAULT 'active',
                    join_date TEXT NOT NULL,
                    last_login TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Bot accounts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    status TEXT DEFAULT 'active',
                    added_date TEXT NOT NULL,
                    last_used TEXT,
                    success_rate REAL DEFAULT 100.0,
                    total_actions INTEGER DEFAULT 0,
                    failed_actions INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(platform, username)
                )
            ''')
            
            # Activities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER,
                    bot_id INTEGER,
                    activity_type TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    target_url TEXT,
                    success BOOLEAN DEFAULT TRUE,
                    response_time REAL,
                    details TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (member_id) REFERENCES members (id),
                    FOREIGN KEY (bot_id) REFERENCES bot_accounts (id)
                )
            ''')
            
            # System logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_level TEXT NOT NULL,
                    module TEXT NOT NULL,
                    message TEXT NOT NULL,
                    details TEXT,
                    created_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("✅ Database setup completed")
            
        except Exception as e:
            print(f"❌ Database setup error: {e}")
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row  # Enable dictionary-like access
            return conn
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return None
    
    # Member management methods
    def add_member(self, username, email="", phone="", plan="basic"):
        """Add new member to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            current_time = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO members 
                (username, email, phone, plan, join_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, phone, plan, current_time, current_time, current_time))
            
            conn.commit()
            member_id = cursor.lastrowid
            conn.close()
            
            return True, f"Member '{username}' added successfully", member_id
            
        except sqlite3.IntegrityError:
            return False, "Member already exists", None
        except Exception as e:
            return False, f"Error adding member: {e}", None
    
    def get_member(self, username):
        """Get member by username"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM members WHERE username = ?', (username,))
            member = cursor.fetchone()
            conn.close()
            
            return dict(member) if member else None
            
        except Exception as e:
            print(f"❌ Get member error: {e}")
            return None
    
    def update_member_status(self, username, status):
        """Update member status"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            current_time = datetime.now().isoformat()
            
            cursor.execute('''
                UPDATE members 
                SET status = ?, updated_at = ?, last_login = ?
                WHERE username = ?
            ''', (status, current_time, current_time, username))
            
            conn.commit()
            conn.close()
            
            return True, f"Member '{username}' status updated to '{status}'"
            
        except Exception as e:
            return False, f"Error updating member status: {e}"
    
    # Bot account management methods
    def add_bot_account(self, platform, username, password_hash, email="", status="active"):
        """Add bot account to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            current_time = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO bot_accounts 
                (platform, username, password_hash, email, status, added_date, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (platform, username, password_hash, email, status, current_time, current_time, current_time))
            
            conn.commit()
            bot_id = cursor.lastrowid
            conn.close()
            
            return True, f"Bot account added for {platform}", bot_id
            
        except sqlite3.IntegrityError:
            return False, "Bot account already exists", None
        except Exception as e:
            return False, f"Error adding bot account: {e}", None
    
    def get_bot_accounts(self, platform=None, status=None):
        """Get bot accounts with optional filters"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM bot_accounts'
            params = []
            
            if platform or status:
                query += ' WHERE'
                conditions = []
                
                if platform:
                    conditions.append(' platform = ?')
                    params.append(platform)
                
                if status:
                    conditions.append(' status = ?')
                    params.append(status)
                
                query += ' AND'.join(conditions)
            
            cursor.execute(query, params)
            bots = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return bots
            
        except Exception as e:
            print(f"❌ Get bot accounts error: {e}")
            return []
    
    # Activity logging methods
    def log_activity(self, member_id, bot_id, activity_type, platform, target_url="", success=True, response_time=0, details=None):
        """Log activity to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            current_time = datetime.now().isoformat()
            details_json = json.dumps(details) if details else None
            
            cursor.execute('''
                INSERT INTO activities 
                (member_id, bot_id, activity_type, platform, target_url, success, response_time, details, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (member_id, bot_id, activity_type, platform, target_url, success, response_time, details_json, current_time))
            
            conn.commit()
            activity_id = cursor.lastrowid
            
            # Update bot account stats
            if bot_id:
                self.update_bot_stats(bot_id, success)
            
            conn.close()
            
            return True, "Activity logged successfully", activity_id
            
        except Exception as e:
            return False, f"Error logging activity: {e}", None
    
    def update_bot_stats(self, bot_id, success):
        """Update bot account statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get current stats
            cursor.execute('SELECT total_actions, failed_actions FROM bot_accounts WHERE id = ?', (bot_id,))
            bot = cursor.fetchone()
            
            if bot:
                total_actions = bot['total_actions'] + 1
                failed_actions = bot['failed_actions'] + (0 if success else 1)
                success_rate = ((total_actions - failed_actions) / total_actions) * 100
                
                cursor.execute('''
                    UPDATE bot_accounts 
                    SET total_actions = ?, failed_actions = ?, success_rate = ?, updated_at = ?
                    WHERE id = ?
                ''', (total_actions, failed_actions, success_rate, datetime.now().isoformat(), bot_id))
                
                conn.commit()
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Update bot stats error: {e}")
    
    # Analytics methods
    def get_daily_stats(self, date=None):
        """Get daily statistics"""
        try:
            if date is None:
                date = datetime.now().strftime('%Y-%m-%d')
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total activities for the day
            cursor.execute('''
                SELECT COUNT(*) as total_activities,
                       SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_activities,
                       AVG(response_time) as avg_response_time
                FROM activities 
                WHERE DATE(created_at) = ?
            ''', (date,))
            
            stats = dict(cursor.fetchone())
            
            # Activities by platform
            cursor.execute('''
                SELECT platform, COUNT(*) as count
                FROM activities 
                WHERE DATE(created_at) = ?
                GROUP BY platform
            ''', (date,))
            
            stats['platform_breakdown'] = {row['platform']: row['count'] for row in cursor.fetchall()}
            
            conn.close()
            
            return stats
            
        except Exception as e:
            print(f"❌ Get daily stats error: {e}")
            return {}
    
    def export_to_csv(self, table_name, output_file):
        """Export table data to CSV"""
        try:
            conn = self.get_connection()
            
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            df.to_csv(output_file, index=False)
            
            conn.close()
            
            return True, f"Data exported to {output_file}"
            
        except Exception as e:
            return False, f"Export error: {e}"
    
    def backup_database(self):
        """Create database backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.data_dir, "backups", f"smm_bot_backup_{timestamp}.db")
            
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            
            # Copy database file
            import shutil
            shutil.copy2(self.db_file, backup_file)
            
            return True, f"Database backed up to {backup_file}"
            
        except Exception as e:
            return False, f"Backup error: {e}"

# Test function
def test_database():
    """Test database functionality"""
    db = DatabaseManager()
    
    # Add test member
    success, message, member_id = db.add_member("test_user", "test@example.com", "123456789", "premium")
    print(f"Add member: {success} - {message}")
    
    # Add test bot account
    success, message, bot_id = db.add_bot_account("facebook", "bot_user", "hashed_password", "bot@example.com")
    print(f"Add bot: {success} - {message}")
    
    # Log activity
    if member_id and bot_id:
        success, message, activity_id = db.log_activity(
            member_id, bot_id, "like", "facebook", 
            "https://facebook.com/post/123", True, 2.5, {"custom": "data"}
        )
        print(f"Log activity: {success} - {message}")
    
    # Get daily stats
    stats = db.get_daily_stats()
    print(f"Daily stats: {stats}")
    
    # Get bot accounts
    bots = db.get_bot_accounts()
    print(f"Total bots: {len(bots)}")
    
    # Backup database
    success, message = db.backup_database()
    print(f"Backup: {success} - {message}")

if __name__ == "__main__":
    test_database()