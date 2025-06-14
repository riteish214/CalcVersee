import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Import calculator modes
from ui.basic_calculator import BasicCalculatorFrame
from ui.scientific_calculator import ScientificCalculatorFrame
from ui.equation_solver import EquationSolverFrame
from ui.matrix_operations import MatrixOperationsFrame
from ui.programmer_calculator import ProgrammerCalculatorFrame
from ui.unit_converter import UnitConverterFrame
from ui.currency_converter import CurrencyConverterFrame
from ui.graph_plotter import GraphPlotterFrame
from ui.history_viewer import HistoryViewerFrame
from utils.theme_manager import ThemeManager
from utils.history_manager import HistoryManager

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Set icon if available
        try:
            self.root.iconbitmap("assets/calculator_icon.ico")
        except:
            pass  # Icon not found, continue without it
        
        # Initialize theme and history managers
        self.theme_manager = ThemeManager(self.root)
        self.history_manager = HistoryManager()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for each calculator mode
        self.basic_frame = BasicCalculatorFrame(self.notebook, self.history_manager)
        self.scientific_frame = ScientificCalculatorFrame(self.notebook, self.history_manager)
        self.equation_frame = EquationSolverFrame(self.notebook, self.history_manager)
        self.matrix_frame = MatrixOperationsFrame(self.notebook, self.history_manager)
        self.programmer_frame = ProgrammerCalculatorFrame(self.notebook, self.history_manager)
        self.unit_frame = UnitConverterFrame(self.notebook, self.history_manager)
        self.currency_frame = CurrencyConverterFrame(self.notebook, self.history_manager)
        self.graph_frame = GraphPlotterFrame(self.notebook, self.history_manager)
        self.history_frame = HistoryViewerFrame(self.notebook, self.history_manager)
        
        # Add frames to notebook
        self.notebook.add(self.basic_frame, text="Basic")
        self.notebook.add(self.scientific_frame, text="Scientific")
        self.notebook.add(self.equation_frame, text="Equation Solver")
        self.notebook.add(self.matrix_frame, text="Matrix")
        self.notebook.add(self.programmer_frame, text="Programmer")
        self.notebook.add(self.unit_frame, text="Unit Converter")
        self.notebook.add(self.currency_frame, text="Currency")
        self.notebook.add(self.graph_frame, text="Graph")
        self.notebook.add(self.history_frame, text="History")
        
        # Create bottom control bar
        self.control_bar = ttk.Frame(self.main_container)
        self.control_bar.pack(fill=tk.X, pady=(8, 0))
        
        # Theme toggle button
        self.theme_btn = ttk.Button(
            self.control_bar, 
            text="Toggle Theme", 
            command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=8)
        
        # Apply initial theme
        self.theme_manager.apply_theme("light")
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()
        
    def toggle_theme(self):
        current_theme = self.theme_manager.current_theme
        new_theme = "dark" if current_theme == "light" else "light"
        self.theme_manager.apply_theme(new_theme)
    
    def setup_shortcuts(self):
        # Keyboard shortcuts
        self.root.bind("<Control-1>", lambda e: self.notebook.select(0))  # Ctrl+1 for Basic
        self.root.bind("<Control-2>", lambda e: self.notebook.select(1))  # Ctrl+2 for Scientific
        self.root.bind("<Control-3>", lambda e: self.notebook.select(2))  # Ctrl+3 for Equation
        self.root.bind("<Control-4>", lambda e: self.notebook.select(3))  # Ctrl+4 for Matrix
        self.root.bind("<Control-5>", lambda e: self.notebook.select(4))  # Ctrl+5 for Programmer
        self.root.bind("<Control-6>", lambda e: self.notebook.select(5))  # Ctrl+6 for Unit
        self.root.bind("<Control-7>", lambda e: self.notebook.select(6))  # Ctrl+7 for Currency
        self.root.bind("<Control-8>", lambda e: self.notebook.select(7))  # Ctrl+8 for Graph
        self.root.bind("<Control-h>", lambda e: self.notebook.select(8))  # Ctrl+H for History
        self.root.bind("<Control-t>", lambda e: self.toggle_theme())      # Ctrl+T for Theme