import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import re
import math

# Configure matplotlib to use TkAgg backend
matplotlib.use("TkAgg")

class GraphPlotterFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Default functions
        self.function_entries = []
        self.function_colors = [
            "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
            "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
        ]
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create left panel for inputs
        self.left_panel = ttk.Frame(self.main_container)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # Function input frame
        self.function_frame = ttk.LabelFrame(self.left_panel, text="Functions")
        self.function_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create initial function input
        self.add_function_input()
        
        # Add function button
        add_btn = ttk.Button(
            self.function_frame,
            text="+ Add Function",
            command=self.add_function_input
        )
        add_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Range inputs
        self.range_frame = ttk.LabelFrame(self.left_panel, text="X Range")
        self.range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        range_input_frame = ttk.Frame(self.range_frame)
        range_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(range_input_frame, text="Min:").grid(row=0, column=0, padx=5, pady=2)
        self.x_min_var = tk.StringVar(value="-10")
        ttk.Entry(range_input_frame, textvariable=self.x_min_var, width=8).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(range_input_frame, text="Max:").grid(row=0, column=2, padx=5, pady=2)
        self.x_max_var = tk.StringVar(value="10")
        ttk.Entry(range_input_frame, textvariable=self.x_max_var, width=8).grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(range_input_frame, text="Step:").grid(row=1, column=0, padx=5, pady=2)
        self.x_step_var = tk.StringVar(value="0.1")
        ttk.Entry(range_input_frame, textvariable=self.x_step_var, width=8).grid(row=1, column=1, padx=5, pady=2)
        
        # Y axis range (optional)
        self.y_range_frame = ttk.LabelFrame(self.left_panel, text="Y Range (Auto if empty)")
        self.y_range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        y_range_input_frame = ttk.Frame(self.y_range_frame)
        y_range_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(y_range_input_frame, text="Min:").grid(row=0, column=0, padx=5, pady=2)
        self.y_min_var = tk.StringVar(value="")
        ttk.Entry(y_range_input_frame, textvariable=self.y_min_var, width=8).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(y_range_input_frame, text="Max:").grid(row=0, column=2, padx=5, pady=2)
        self.y_max_var = tk.StringVar(value="")
        ttk.Entry(y_range_input_frame, textvariable=self.y_max_var, width=8).grid(row=0, column=3, padx=5, pady=2)
        
        # Graph options
        self.options_frame = ttk.LabelFrame(self.left_panel, text="Graph Options")
        self.options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Grid option
        self.show_grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame, 
            text="Show Grid",
            variable=self.show_grid_var
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Legend option
        self.show_legend_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            self.options_frame, 
            text="Show Legend",
            variable=self.show_legend_var
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Plot button
        plot_btn = ttk.Button(
            self.left_panel,
            text="Plot Graph",
            command=self.plot_graph
        )
        plot_btn.pack(fill=tk.X, padx=5, pady=10)
        
        # Clear button
        clear_btn = ttk.Button(
            self.left_panel,
            text="Clear All",
            command=self.clear_all
        )
        clear_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Create right panel for graph
        self.right_panel = ttk.Frame(self.main_container)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create initial matplotlib figure
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Create canvas for matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize with default graph
        self.plot_graph()
    
    def add_function_input(self):
        # Limit to 5 functions
        if len(self.function_entries) >= 5:
            return
            
        # Create a frame for this function
        func_entry_frame = ttk.Frame(self.function_frame)
        func_entry_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Function label
        func_label = ttk.Label(func_entry_frame, text=f"f{len(self.function_entries) + 1}(x) =")
        func_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Function entry
        func_entry = ttk.Entry(func_entry_frame, width=30)
        func_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Default function based on entry number
        if len(self.function_entries) == 0:
            func_entry.insert(0, "sin(x)")
        elif len(self.function_entries) == 1:
            func_entry.insert(0, "cos(x)")
        elif len(self.function_entries) == 2:
            func_entry.insert(0, "x^2")
        elif len(self.function_entries) == 3:
            func_entry.insert(0, "sqrt(abs(x))")
        elif len(self.function_entries) == 4:
            func_entry.insert(0, "exp(-x^2/10)*sin(x)")
        
        # Remove button
        remove_btn = ttk.Button(
            func_entry_frame,
            text="×",
            width=3,
            command=lambda: self.remove_function_input(func_entry_frame)
        )
        remove_btn.pack(side=tk.RIGHT, padx=5)
        
        # Store the entry widget
        self.function_entries.append((func_entry_frame, func_entry))
    
    def remove_function_input(self, frame):
        # Find the entry in the list
        for i, (entry_frame, _) in enumerate(self.function_entries):
            if entry_frame == frame:
                # Remove from list
                self.function_entries.pop(i)
                # Destroy the frame
                frame.destroy()
                break
    
    def clear_all(self):
        # Clear all function inputs
        for frame, _ in self.function_entries:
            frame.destroy()
        self.function_entries = []
        
        # Add one empty function input
        self.add_function_input()
        
        # Reset ranges
        self.x_min_var.set("-10")
        self.x_max_var.set("10")
        self.x_step_var.set("0.1")
        self.y_min_var.set("")
        self.y_max_var.set("")
        
        # Clear the plot
        self.ax.clear()
        self.fig.tight_layout()
        self.canvas.draw()
    
    def parse_function(self, func_str):
        # Replace common mathematical expressions with their numpy equivalents
        replacements = {
            r'sin\(': 'np.sin(',
            r'cos\(': 'np.cos(',
            r'tan\(': 'np.tan(',
            r'asin\(': 'np.arcsin(',
            r'acos\(': 'np.arccos(',
            r'atan\(': 'np.arctan(',
            r'ln\(': 'np.log(',
            r'log\(': 'np.log10(',
            r'sqrt\(': 'np.sqrt(',
            r'abs\(': 'np.abs(',
            r'exp\(': 'np.exp(',
            r'pi': 'np.pi',
            r'e': 'np.e',
            r'([0-9]+|x|\))[ ]*\^[ ]*([0-9]+|x|\(.*?\))': r'\1**\2'  # Handle power operations
        }
        
        result = func_str
        for pattern, replacement in replacements.items():
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def evaluate_function(self, func_str, x_values):
        try:
            # Parse the function string
            parsed_func = self.parse_function(func_str)
            
            # Create function to evaluate
            def f(x):
                return eval(parsed_func)
            
            # Evaluate function for all x values
            y_values = f(x_values)
            
            return y_values
        except Exception as e:
            print(f"Error evaluating function '{func_str}': {str(e)}")
            return None
    
    def plot_graph(self):
        try:
            # Clear previous plot
            self.ax.clear()
            
            # Get x range
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())
            x_step = float(self.x_step_var.get())
            
            # Create x values
            x_values = np.arange(x_min, x_max + x_step, x_step)
            
            # Process each function
            legend_entries = []
            history_entries = []
            
            for i, (_, entry) in enumerate(self.function_entries):
                func_str = entry.get().strip()
                if func_str:
                    # Get color for this function
                    color = self.function_colors[i % len(self.function_colors)]
                    
                    # Evaluate the function
                    y_values = self.evaluate_function(func_str, x_values)
                    
                    if y_values is not None:
                        # Plot the function
                        line, = self.ax.plot(x_values, y_values, color=color, label=f"f{i+1}(x) = {func_str}")
                        legend_entries.append(line)
                        history_entries.append(func_str)
                    else:
                        # Error in function
                        entry.config(foreground="red")
            
            # Configure the plot
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.set_title('Function Plot')
            
            # Set y range if specified
            if self.y_min_var.get() and self.y_max_var.get():
                try:
                    y_min = float(self.y_min_var.get())
                    y_max = float(self.y_max_var.get())
                    self.ax.set_ylim(y_min, y_max)
                except ValueError:
                    pass
            
            # Show grid if enabled
            if self.show_grid_var.get():
                self.ax.grid(True, linestyle='--', alpha=0.7)
            
            # Show legend if enabled and there are functions
            if self.show_legend_var.get() and legend_entries:
                self.ax.legend()
            
            # Add x and y axes
            self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            
            # Update the canvas
            self.fig.tight_layout()
            self.canvas.draw()
            
            # Add to history
            if history_entries:
                functions_str = ", ".join(history_entries)
                self.history_manager.add_entry(
                    "Graph Plotter",
                    functions_str,
                    f"Plot created with x in [{x_min}, {x_max}]"
                )
            
        except Exception as e:
            # Display error in the plot
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error: {str(e)}", 
                         horizontalalignment='center',
                         verticalalignment='center',
                         transform=self.ax.transAxes,
                         color='red')
            self.fig.tight_layout()
            self.canvas.draw()