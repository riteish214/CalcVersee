import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import datetime

class HistoryViewerFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        self.toolbar = ttk.Frame(self.main_container)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Filter by calculator type
        ttk.Label(self.toolbar, text="Filter:").pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combobox = ttk.Combobox(
            self.toolbar,
            textvariable=self.filter_var,
            values=["All", "Basic", "Scientific", "Equation Solver", "Matrix Operations", 
                    "Programmer", "Unit Converter", "Currency Converter", "Graph Plotter"],
            state="readonly",
            width=15
        )
        filter_combobox.pack(side=tk.LEFT, padx=5)
        filter_combobox.bind("<<ComboboxSelected>>", lambda e: self.refresh_history())
        
        # Export button
        export_button = ttk.Button(
            self.toolbar,
            text="Export History",
            command=self.export_history
        )
        export_button.pack(side=tk.RIGHT, padx=5)
        
        # Clear history button
        clear_button = ttk.Button(
            self.toolbar,
            text="Clear History",
            command=self.clear_history
        )
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Create history display
        self.history_frame = ttk.LabelFrame(self.main_container, text="Calculation History")
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for history
        self.history_tree = ttk.Treeview(
            self.history_frame,
            columns=("Time", "Type", "Input", "Result"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.history_tree.heading("Time", text="Time")
        self.history_tree.heading("Type", text="Calculator")
        self.history_tree.heading("Input", text="Input")
        self.history_tree.heading("Result", text="Result")
        
        self.history_tree.column("Time", width=150)
        self.history_tree.column("Type", width=120)
        self.history_tree.column("Input", width=250)
        self.history_tree.column("Result", width=250)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right-click menu
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy Input", command=lambda: self.copy_selected("input"))
        self.context_menu.add_command(label="Copy Result", command=lambda: self.copy_selected("result"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Delete", command=self.delete_selected)
        
        self.history_tree.bind("<Button-3>", self.show_context_menu)
        
        # Initial history display
        self.refresh_history()
    
    def refresh_history(self):
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get history from manager
        history = self.history_manager.get_history()
        
        # Apply filter
        filter_type = self.filter_var.get()
        if filter_type != "All":
            history = [entry for entry in history if entry["type"] == filter_type]
        
        # Add items to tree (newest first)
        for entry in reversed(history):
            self.history_tree.insert(
                "",
                "end",
                values=(
                    entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    entry["type"],
                    entry["input"],
                    entry["result"]
                ),
                tags=(entry["id"],)
            )
    
    def export_history(self):
        # Get filtered history
        history = self.history_manager.get_history()
        filter_type = self.filter_var.get()
        if filter_type != "All":
            history = [entry for entry in history if entry["type"] == filter_type]
        
        if not history:
            messagebox.showinfo("Export History", "No history to export.")
            return
        
        # Ask for export format
        export_format = tk.StringVar(value="csv")
        
        dialog = tk.Toplevel(self)
        dialog.title("Export Format")
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select export format:").pack(pady=10)
        
        ttk.Radiobutton(dialog, text="CSV", variable=export_format, value="csv").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Text", variable=export_format, value="txt").pack(anchor=tk.W, padx=20)
        
        def confirm_export():
            dialog.destroy()
            format_value = export_format.get()
            
            # Ask for file path
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"calculator_history_{current_time}.{format_value}"
            
            filepath = filedialog.asksaveasfilename(
                defaultextension=f".{format_value}",
                filetypes=[
                    ("CSV files", "*.csv") if format_value == "csv" else ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                initialfile=filename
            )
            
            if not filepath:
                return
            
            try:
                if format_value == "csv":
                    self.export_to_csv(filepath, history)
                else:
                    self.export_to_text(filepath, history)
                
                messagebox.showinfo("Export Complete", f"History exported to {filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export history: {str(e)}")
        
        ttk.Button(dialog, text="Export", command=confirm_export).pack(pady=10)
    
    def export_to_csv(self, filepath, history):
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Time", "Calculator", "Input", "Result"])
            # Write data
            for entry in history:
                writer.writerow([
                    entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
                    entry["type"],
                    entry["input"],
                    entry["result"]
                ])
    
    def export_to_text(self, filepath, history):
        with open(filepath, 'w') as file:
            file.write("CALCULATOR HISTORY\n")
            file.write("=================\n\n")
            
            for entry in history:
                file.write(f"Time: {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Calculator: {entry['type']}\n")
                file.write(f"Input: {entry['input']}\n")
                file.write(f"Result: {entry['result']}\n")
                file.write("-" * 40 + "\n\n")
    
    def clear_history(self):
        # Ask for confirmation
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all history?"):
            self.history_manager.clear_history()
            self.refresh_history()
    
    def show_context_menu(self, event):
        # Get the item under cursor
        item = self.history_tree.identify_row(event.y)
        if item:
            # Select the item
            self.history_tree.selection_set(item)
            # Show context menu
            self.context_menu.post(event.x_root, event.y_root)
    
    def copy_selected(self, field):
        # Get selected item
        selected = self.history_tree.selection()
        if not selected:
            return
            
        # Get values
        values = self.history_tree.item(selected[0], "values")
        
        # Copy to clipboard
        if field == "input":
            self.clipboard_clear()
            self.clipboard_append(values[2])
        elif field == "result":
            self.clipboard_clear()
            self.clipboard_append(values[3])
    
    def delete_selected(self):
        # Get selected item
        selected = self.history_tree.selection()
        if not selected:
            return
            
        # Get item ID
        item_id = self.history_tree.item(selected[0], "tags")[0]
        
        # Delete from history manager
        self.history_manager.delete_entry(item_id)
        
        # Refresh display
        self.refresh_history()