import datetime
import uuid
import json
import os

class HistoryManager:
    def __init__(self):
        self.history = []
        self.max_entries = 1000  # Limit history size
        
        # Load history from file if exists
        self.history_file = "calculator_history.json"
        self.load_history()
    
    def add_entry(self, type, input_text, result):
        """Add a new entry to the history."""
        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.datetime.now(),
            "type": type,
            "input": input_text,
            "result": result
        }
        
        # Add to history
        self.history.append(entry)
        
        # Limit history size
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]
        
        # Save to file
        self.save_history()
        
        return entry
    
    def get_history(self):
        """Get the full history."""
        return self.history
    
    def get_filtered_history(self, calculator_type=None):
        """Get history filtered by calculator type."""
        if calculator_type:
            return [entry for entry in self.history if entry["type"] == calculator_type]
        return self.history
    
    def delete_entry(self, entry_id):
        """Delete an entry by ID."""
        self.history = [entry for entry in self.history if entry["id"] != entry_id]
        self.save_history()
    
    def clear_history(self):
        """Clear all history."""
        self.history = []
        self.save_history()
    
    def save_history(self):
        """Save history to file."""
        try:
            # Convert history to serializable format
            serializable_history = []
            for entry in self.history:
                serializable_entry = entry.copy()
                serializable_entry["timestamp"] = serializable_entry["timestamp"].isoformat()
                serializable_history.append(serializable_entry)
            
            with open(self.history_file, 'w') as f:
                json.dump(serializable_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {str(e)}")
    
    def load_history(self):
        """Load history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    serialized_history = json.load(f)
                
                # Convert serialized history back to objects
                self.history = []
                for entry in serialized_history:
                    entry["timestamp"] = datetime.datetime.fromisoformat(entry["timestamp"])
                    self.history.append(entry)
        except Exception as e:
            print(f"Error loading history: {str(e)}")
            self.history = []