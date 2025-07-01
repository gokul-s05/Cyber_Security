import streamlit as st
import time
from datetime import datetime
import os
import json

class StreamlitKeyLogger:
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
        
    def clear_logs(self):
        """Clear the logged keys"""
        self.logged_keys = ""
        self.key_count = 0
        self.special_keys = []
        
    def save_to_file(self, filename):
        """Save logged keys to a file"""
        try:
            log_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_keys': self.key_count,
                'text_content': self.logged_keys,
                'special_keys': self.special_keys,
                'session_duration': self.get_session_duration()
            }
            
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving file: {e}")
            return False
            
    def get_session_info(self):
        """Get information about the current logging session"""
        if self.start_time:
            duration = self.get_session_duration()
            return {
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration': duration,
                'keys_captured': self.key_count,
                'special_keys_count': len(self.special_keys)
            }
        return None
        
    def get_session_duration(self):
        """Get the current session duration"""
        if self.start_time:
            duration = datetime.now() - self.start_time
            return str(duration).split('.')[0]
        return "00:00:00"

# Global keylogger instance
if 'keylogger' not in st.session_state:
    st.session_state.keylogger = StreamlitKeyLogger()

def keylogger_interface():
    if 'keylogger' not in st.session_state:
        st.session_state.keylogger = StreamlitKeyLogger()
    """Streamlit interface for the keylogger"""
    st.header("🔑 Key Logger")
    st.write("This tool simulates keylogging by capturing keystrokes from text inputs within this app.")
    
    # Status display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start Logging", type="primary", disabled=st.session_state.keylogger.is_logging):
            if st.session_state.keylogger.start_logging():
                st.success("Logging started!")
    
    with col2:
        if st.button("Stop Logging", type="secondary", disabled=not st.session_state.keylogger.is_logging):
            if st.session_state.keylogger.stop_logging():
                st.success("Logging stopped!")
    
    with col3:
        if st.button("Clear Logs", type="secondary"):
            st.session_state.keylogger.clear_logs()
            st.success("Logs cleared!")
    
    # Status indicator
    if st.session_state.keylogger.is_logging:
        st.warning("⚠️ **LOGGING ACTIVE** - Type in the text areas below to capture keystrokes!")
    else:
        st.info("📝 Logging is currently stopped")
    
    # Session info
    session_info = st.session_state.keylogger.get_session_info()
    if session_info:
        st.subheader("Session Information")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Start Time", session_info['start_time'])
        with col2:
            st.metric("Duration", session_info['duration'])
        with col3:
            st.metric("Keys Captured", session_info['keys_captured'])
        with col4:
            st.metric("Special Keys", session_info['special_keys_count'])
    
    # Test text areas for keylogging
    if st.session_state.keylogger.is_logging:
        st.subheader("🎯 Test Areas - Type here to capture keystrokes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Text Input 1:**")
            test_input1 = st.text_input("Type here to capture keystrokes:", key="test1")
            if test_input1 and st.session_state.keylogger.is_logging:
                # Simulate capturing the input
                st.session_state.keylogger.add_key(test_input1)
                
        with col2:
            st.write("**Text Input 2:**")
            test_input2 = st.text_input("Another test area:", key="test2")
            if test_input2 and st.session_state.keylogger.is_logging:
                # Simulate capturing the input
                st.session_state.keylogger.add_key(test_input2)
        
        # Special key simulation
        st.write("**Special Key Simulation:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Enter", key="enter_btn"):
                st.session_state.keylogger.add_special_key("Enter")
                st.success("Enter key captured!")
                
        with col2:
            if st.button("Space", key="space_btn"):
                st.session_state.keylogger.add_special_key("Space")
                st.success("Space key captured!")
                
        with col3:
            if st.button("Tab", key="tab_btn"):
                st.session_state.keylogger.add_special_key("Tab")
                st.success("Tab key captured!")
                
        with col4:
            if st.button("Backspace", key="backspace_btn"):
                st.session_state.keylogger.add_special_key("Backspace")
                st.success("Backspace key captured!")
    
    # Display logged keys
    st.subheader("📊 Captured Data")
    
    # Text content
    logged_text = st.session_state.keylogger.get_logged_keys()
    if logged_text:
        st.write("**Captured Text:**")
        st.text_area("Logged Keys:", value=logged_text, height=100, disabled=True)
    else:
        st.info("No text captured yet. Start logging and type in the test areas above.")
    
    # Special keys log
    if st.session_state.keylogger.special_keys:
        st.write("**Special Keys Log:**")
        special_keys_df = st.session_state.keylogger.special_keys
        for i, key_data in enumerate(special_keys_df):
            st.write(f"{i+1}. {key_data['key']} at {key_data['timestamp']}")
    
    # Download functionality
    if logged_text or st.session_state.keylogger.special_keys:
        st.subheader("💾 Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Download as TXT"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"keylog_{timestamp}.txt"
                if st.session_state.keylogger.save_to_file(filename):
                    with open(filename, 'r') as f:
                        st.download_button(
                            label="Click to download",
                            data=f.read(),
                            file_name=filename,
                            mime="text/plain"
                        )
                    # Clean up the temporary file
                    os.remove(filename)
        
        with col2:
            if st.button("Download as JSON"):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"keylog_{timestamp}.json"
                if st.session_state.keylogger.save_to_file(filename):
                    with open(filename, 'r') as f:
                        st.download_button(
                            label="Click to download JSON",
                            data=f.read(),
                            file_name=filename,
                            mime="application/json"
                        )
                    # Clean up the temporary file
                    os.remove(filename)
    
    # Instructions
    with st.expander("ℹ️ How to use"):
        st.write("""
        **This is a simulated keylogger for educational purposes:**
        
        1. **Start Logging**: Click 'Start Logging' to begin the session
        2. **Type in Test Areas**: Use the text inputs above to simulate keystroke capture
        3. **Special Keys**: Click the special key buttons to simulate capturing special keys
        4. **Monitor**: Watch the captured data update in real-time
        5. **Stop Logging**: Click 'Stop Logging' to end the session
        6. **Download**: Save the captured data as TXT or JSON files
        7. **Clear**: Reset all captured data
        
        **Important Notes:**
        - This is a simulation only - it cannot capture system-wide keystrokes
        - Real keyloggers require system-level permissions and are often considered malware
        - This tool is for educational and security testing purposes only
        - Browser security prevents web apps from accessing system-wide keystrokes
        
        **What it demonstrates:**
        - How keyloggers track keystrokes and timestamps
        - The types of data that can be captured
        - Why proper security measures are important
        """) 