from datetime import datetime
import json

class KeyLogger:
    def __init__(self):
        self.logged_keys = ""
        self.is_logging = False
        self.start_time = None
        self.key_count = 0
        self.special_keys = []
        
    def start_logging(self):
        """Start the keylogging session"""
        self.is_logging = True
        self.start_time = datetime.now()
        self.logged_keys = ""
        self.key_count = 0
        self.special_keys = []
        return True
        
    def stop_logging(self):
        """Stop the keylogging session"""
        self.is_logging = False
        return True
        
    def add_key(self, key):
        """Add a key to the logged keys"""
        if self.is_logging:
            self.logged_keys += key
            self.key_count += 1
            
    def add_special_key(self, key_name):
        """Add a special key (like Enter, Space, etc.)"""
        if self.is_logging:
            self.special_keys.append({
                'key': key_name,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            self.key_count += 1
            
    def get_logged_keys(self):
        """Get the current logged keys"""
        return self.logged_keys
        
    def get_log_stats(self):
        """Get statistics about the logged keys"""
        if not self.start_time:
            return {
                'duration': '0:00:00',
                'key_count': 0,
                'special_keys': []
            }
            
        current_time = datetime.now()
        duration = current_time - self.start_time
        
        return {
            'duration': str(duration).split('.')[0],
            'key_count': self.key_count,
            'special_keys': self.special_keys
        }
        
    def clear_logs(self):
        """Clear the logged keys"""
        self.logged_keys = ""
        self.key_count = 0
        self.special_keys = []
        
    def export_logs(self, filename='keylog.json'):
        """Export logs to a JSON file"""
        data = {
            'logged_keys': self.logged_keys,
            'stats': self.get_log_stats()
        }
        return json.dumps(data)

if __name__ == '__main__':
    # Example usage
    logger = KeyLogger()
    logger.start_logging()
    
    # Simulate some key presses
    logger.add_key("H")
    logger.add_key("e")
    logger.add_key("l")
    logger.add_key("l")
    logger.add_key("o")
    logger.add_special_key("Space")
    logger.add_key("W")
    logger.add_key("o")
    logger.add_key("r")
    logger.add_key("l")
    logger.add_key("d")
    logger.add_special_key("Enter")
    
    # Stop logging and print results
    logger.stop_logging()
    print("Logged keys:", logger.get_logged_keys())
    print("Statistics:", logger.get_log_stats())