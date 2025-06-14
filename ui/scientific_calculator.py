import tkinter as tk
from tkinter import ttk
import math

class ScientificCalculatorFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Calculator state
        self.current_input = ""
        self.current_operation = None
        self.first_number = None
        self.result = None
        self.operation_just_pressed = False
        self.in_degree_mode = True  # Toggle between degrees and radians
        
        # Create display
        self.display_frame = ttk.Frame(self)
        self.display_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Entry(
            self.display_frame, 
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            state="readonly"
        )
        self.display.pack(fill=tk.X)
        
        # Secondary display for showing the operation
        self.operation_var = tk.StringVar(value="")
        self.operation_display = ttk.Label(
            self.display_frame,
            textvariable=self.operation_var,
            font=("Arial", 12),
            anchor="e"
        )
        self.operation_display.pack(fill=tk.X)
        
        # Mode indicator (DEG/RAD)
        self.mode_var = tk.StringVar(value="DEG")
        self.mode_label = ttk.Label(
            self.display_frame,
            textvariable=self.mode_var,
            font=("Arial", 10),
            anchor="w"
        )
        self.mode_label.pack(fill=tk.X)
        
        # Create main frame to hold buttons
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create button frames
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scientific_buttons_frame = ttk.Frame(self.main_frame)
        self.scientific_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Configure button frame grids
        for i in range(5):
            self.buttons_frame.columnconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.rowconfigure(i, weight=1)
            
        for i in range(3):
            self.scientific_buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.scientific_buttons_frame.rowconfigure(i, weight=1)
        
        # Define buttons
        self.create_basic_buttons()
        self.create_scientific_buttons()
        
        # Set up keyboard bindings
        self.setup_keyboard_bindings()
    
    def create_basic_buttons(self):
        # Button layout
        button_layout = [
            ("C", self.clear, 0, 0),
            ("±", self.negate, 0, 1),
            ("%", lambda: self.handle_operator("%"), 0, 2),
            ("÷", lambda: self.handle_operator("/"), 0, 3),
            
            ("7", lambda: self.append_number("7"), 1, 0),
            ("8", lambda: self.append_number("8"), 1, 1),
            ("9", lambda: self.append_number("9"), 1, 2),
            ("×", lambda: self.handle_operator("*"), 1, 3),
            
            ("4", lambda: self.append_number("4"), 2, 0),
            ("5", lambda: self.append_number("5"), 2, 1),
            ("6", lambda: self.append_number("6"), 2, 2),
            ("-", lambda: self.handle_operator("-"), 2, 3),
            
            ("1", lambda: self.append_number("1"), 3, 0),
            ("2", lambda: self.append_number("2"), 3, 1),
            ("3", lambda: self.append_number("3"), 3, 2),
            ("+", lambda: self.handle_operator("+"), 3, 3),
            
            ("0", lambda: self.append_number("0"), 4, 0, 2),  # Spans 2 columns
            (".", lambda: self.append_decimal(), 4, 2),
            ("=", self.calculate, 4, 3),
        ]
        
        # Create buttons
        for button in button_layout:
            if len(button) == 5:  # Special case for buttons that span multiple columns
                text, command, row, col, colspan = button
                btn = ttk.Button(self.buttons_frame, text=text, command=command)
                btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
            else:
                text, command, row, col = button
                btn = ttk.Button(self.buttons_frame, text=text, command=command)
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
    def create_scientific_buttons(self):
        # Button layout for scientific functions
        scientific_buttons = [
            ("sin", lambda: self.apply_scientific_function("sin"), 0, 0),
            ("cos", lambda: self.apply_scientific_function("cos"), 0, 1),
            ("tan", lambda: self.apply_scientific_function("tan"), 0, 2),
            
            ("ln", lambda: self.apply_scientific_function("ln"), 1, 0),
            ("log", lambda: self.apply_scientific_function("log"), 1, 1),
            ("√", lambda: self.apply_scientific_function("sqrt"), 1, 2),
            
            ("x²", lambda: self.apply_scientific_function("square"), 2, 0),
            ("x³", lambda: self.apply_scientific_function("cube"), 2, 1),
            ("xʸ", lambda: self.handle_operator("^"), 2, 2),
            
            ("1/x", lambda: self.apply_scientific_function("reciprocal"), 3, 0),
            ("e^x", lambda: self.apply_scientific_function("exp"), 3, 1),
            ("π", lambda: self.append_number(str(math.pi)), 3, 2),
            
            ("DEG/RAD", self.toggle_degree_mode, 4, 0, 3),  # Spans 3 columns
        ]
        
        # Create buttons
        for button in scientific_buttons:
            if len(button) == 5:  # Special case for buttons that span multiple columns
                text, command, row, col, colspan = button
                btn = ttk.Button(self.scientific_buttons_frame, text=text, command=command)
                btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
            else:
                text, command, row, col = button
                btn = ttk.Button(self.scientific_buttons_frame, text=text, command=command)
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
    def setup_keyboard_bindings(self):
        # Number keys
        for i in range(10):
            self.master.bind(str(i), lambda e, digit=i: self.append_number(str(digit)))
        
        # Operation keys
        self.master.bind("+", lambda e: self.handle_operator("+"))
        self.master.bind("-", lambda e: self.handle_operator("-"))
        self.master.bind("*", lambda e: self.handle_operator("*"))
        self.master.bind("/", lambda e: self.handle_operator("/"))
        self.master.bind("%", lambda e: self.handle_operator("%"))
        self.master.bind("^", lambda e: self.handle_operator("^"))
        
        # Equals and Enter
        self.master.bind("=", lambda e: self.calculate())
        self.master.bind("<Return>", lambda e: self.calculate())
        
        # Decimal point
        self.master.bind(".", lambda e: self.append_decimal())
        
        # Clear
        self.master.bind("<Escape>", lambda e: self.clear())
        self.master.bind("c", lambda e: self.clear())
        
        # Backspace
        self.master.bind("<BackSpace>", lambda e: self.backspace())
    
    def toggle_degree_mode(self):
        self.in_degree_mode = not self.in_degree_mode
        self.mode_var.set("DEG" if self.in_degree_mode else "RAD")
    
    def append_number(self, number):
        if self.operation_just_pressed:
            self.current_input = ""
            self.operation_just_pressed = False
            
        if self.current_input == "0" and number != ".":
            self.current_input = number
        else:
            self.current_input += number
        
        self.update_display()
    
    def append_decimal(self):
        if self.operation_just_pressed:
            self.current_input = "0"
            self.operation_just_pressed = False
            
        if "." not in self.current_input:
            if not self.current_input:
                self.current_input = "0"
            self.current_input += "."
        
        self.update_display()
    
    def handle_operator(self, operator):
        if self.current_input:
            if self.first_number is not None:
                self.calculate()
            
            self.first_number = float(self.current_input)
            self.current_operation = operator
            self.operation_just_pressed = True
            
            # Update operation display
            display_operator = operator
            if operator == "*":
                display_operator = "×"
            elif operator == "/":
                display_operator = "÷"
            elif operator == "^":
                display_operator = "^"
            
            self.operation_var.set(f"{self.first_number} {display_operator}")
    
    def apply_scientific_function(self, function):
        if not self.current_input:
            return
            
        value = float(self.current_input)
        expression = f"{function}({value})"
        
        try:
            if function == "sin":
                if self.in_degree_mode:
                    value = math.radians(value)
                self.result = math.sin(value)
            elif function == "cos":
                if self.in_degree_mode:
                    value = math.radians(value)
                self.result = math.cos(value)
            elif function == "tan":
                if self.in_degree_mode:
                    value = math.radians(value)
                self.result = math.tan(value)
            elif function == "ln":
                self.result = math.log(value)  # Natural log
            elif function == "log":
                self.result = math.log10(value)  # Base 10 log
            elif function == "sqrt":
                self.result = math.sqrt(value)
            elif function == "square":
                self.result = value ** 2
                expression = f"({value})²"
            elif function == "cube":
                self.result = value ** 3
                expression = f"({value})³"
            elif function == "reciprocal":
                self.result = 1 / value
                expression = f"1/({value})"
            elif function == "exp":
                self.result = math.exp(value)
                expression = f"e^({value})"
            
            # Format result for display
            if abs(self.result) < 1e-10:
                self.result = 0
            
            # Add to history
            self.history_manager.add_entry(
                "Scientific",
                expression,
                str(self.result)
            )
            
            # Update display
            self.current_input = str(self.result)
            self.update_display()
            
        except Exception as e:
            self.display_var.set(f"Error: {str(e)}")
            self.reset_after_error()
    
    def calculate(self):
        if self.current_operation and self.first_number is not None and self.current_input:
            second_number = float(self.current_input)
            
            # Prepare expression for history
            display_operator = self.current_operation
            if self.current_operation == "*":
                display_operator = "×"
            elif self.current_operation == "/":
                display_operator = "÷"
            
            expression = f"{self.first_number} {display_operator} {second_number}"
            
            try:
                if self.current_operation == "+":
                    self.result = self.first_number + second_number
                elif self.current_operation == "-":
                    self.result = self.first_number - second_number
                elif self.current_operation == "*":
                    self.result = self.first_number * second_number
                elif self.current_operation == "/":
                    if second_number == 0:
                        raise ZeroDivisionError("Division by zero")
                    self.result = self.first_number / second_number
                elif self.current_operation == "%":
                    self.result = self.first_number % second_number
                elif self.current_operation == "^":
                    self.result = self.first_number ** second_number
                    expression = f"{self.first_number}^{second_number}"
                
                # Format the result
                if self.result.is_integer():
                    self.result = int(self.result)
                
                # Add to history
                self.history_manager.add_entry(
                    "Scientific",
                    expression,
                    str(self.result)
                )
                
                # Update display
                self.current_input = str(self.result)
                self.first_number = None
                self.current_operation = None
                self.operation_var.set("")
                self.update_display()
                
            except ZeroDivisionError:
                self.display_var.set("Error: Division by zero")
                self.reset_after_error()
            except Exception as e:
                self.display_var.set(f"Error: {str(e)}")
                self.reset_after_error()
    
    def clear(self):
        self.current_input = ""
        self.current_operation = None
        self.first_number = None
        self.result = None
        self.operation_var.set("")
        self.display_var.set("0")
    
    def negate(self):
        if self.current_input:
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.update_display()
    
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input or self.current_input == "-":
                self.current_input = ""
            self.update_display()
    
    def update_display(self):
        if not self.current_input:
            self.display_var.set("0")
        else:
            self.display_var.set(self.current_input)
    
    def reset_after_error(self):
        self.current_input = ""
        self.current_operation = None
        self.first_number = None
        self.result = None
        self.operation_var.set("")