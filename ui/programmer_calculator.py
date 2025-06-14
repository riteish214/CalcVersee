import tkinter as tk
from tkinter import ttk

class ProgrammerCalculatorFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Current number and display mode
        self.current_value = 0
        self.display_base = "dec"  # One of: bin, oct, dec, hex
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Number display
        self.display_frame = ttk.LabelFrame(self.main_container, text="Number Display")
        self.display_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Display for different bases
        self.displays = {}
        
        # Hexadecimal display
        hex_frame = ttk.Frame(self.display_frame)
        hex_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(hex_frame, text="HEX:", width=6).pack(side=tk.LEFT)
        self.displays["hex"] = ttk.Entry(hex_frame, justify="right", state="readonly")
        self.displays["hex"].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Decimal display
        dec_frame = ttk.Frame(self.display_frame)
        dec_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(dec_frame, text="DEC:", width=6).pack(side=tk.LEFT)
        self.displays["dec"] = ttk.Entry(dec_frame, justify="right", state="readonly")
        self.displays["dec"].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Octal display
        oct_frame = ttk.Frame(self.display_frame)
        oct_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(oct_frame, text="OCT:", width=6).pack(side=tk.LEFT)
        self.displays["oct"] = ttk.Entry(oct_frame, justify="right", state="readonly")
        self.displays["oct"].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Binary display
        bin_frame = ttk.Frame(self.display_frame)
        bin_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(bin_frame, text="BIN:", width=6).pack(side=tk.LEFT)
        self.displays["bin"] = ttk.Entry(bin_frame, justify="right", state="readonly")
        self.displays["bin"].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Number of bits selector
        bits_frame = ttk.Frame(self.display_frame)
        bits_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(bits_frame, text="Word Size:").pack(side=tk.LEFT)
        
        self.word_size = tk.StringVar(value="32")
        word_sizes = ["8", "16", "32", "64"]
        size_combobox = ttk.Combobox(
            bits_frame, 
            textvariable=self.word_size,
            values=word_sizes,
            width=5,
            state="readonly"
        )
        size_combobox.pack(side=tk.LEFT, padx=5)
        size_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_displays())
        
        # Base selector
        self.base_frame = ttk.LabelFrame(self.main_container, text="Base")
        self.base_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.base_var = tk.StringVar(value="dec")
        
        bases = [
            ("Hexadecimal", "hex"),
            ("Decimal", "dec"),
            ("Octal", "oct"),
            ("Binary", "bin")
        ]
        
        for text, value in bases:
            radio = ttk.Radiobutton(
                self.base_frame,
                text=text,
                variable=self.base_var,
                value=value,
                command=self.change_base
            )
            radio.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Operations frame
        self.operations_frame = ttk.LabelFrame(self.main_container, text="Operations")
        self.operations_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Bitwise operations
        bitwise_ops = [
            ("AND", self.bitwise_and),
            ("OR", self.bitwise_or),
            ("XOR", self.bitwise_xor),
            ("NOT", self.bitwise_not),
            ("<<", self.shift_left),
            (">>", self.shift_right)
        ]
        
        # Create operation buttons
        op_frame = ttk.Frame(self.operations_frame)
        op_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for text, command in bitwise_ops:
            btn = ttk.Button(op_frame, text=text, command=command, width=6)
            btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Create keypad
        self.keypad_frame = ttk.Frame(self.main_container)
        self.keypad_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid
        for i in range(4):
            self.keypad_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.keypad_frame.rowconfigure(i, weight=1)
        
        # Hex keys (initially disabled)
        hex_keys = [
            ('A', 0, 0), ('B', 0, 1), ('C', 0, 2), ('D', 0, 3),
            ('E', 1, 0), ('F', 1, 1), ('CLR', 1, 2), ('DEL', 1, 3)
        ]
        
        self.hex_buttons = {}
        for key, row, col in hex_keys:
            if key in ['CLR', 'DEL']:
                btn = ttk.Button(
                    self.keypad_frame, 
                    text=key,
                    command=self.clear if key == 'CLR' else self.backspace
                )
            else:
                btn = ttk.Button(
                    self.keypad_frame, 
                    text=key,
                    command=lambda k=key: self.append_digit(k)
                )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            if key not in ['CLR', 'DEL']:
                self.hex_buttons[key] = btn
                btn.state(['disabled'])  # Initially disabled (decimal mode)
        
        # Number keys
        num_keys = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3)
        ]
        
        self.num_buttons = {}
        for key, row, col in num_keys:
            if key in ['+', '-', '*', '/', '=', '.']:
                btn = ttk.Button(
                    self.keypad_frame, 
                    text=key,
                    command=lambda k=key: self.handle_operation(k)
                )
                if key == '.':
                    btn.state(['disabled'])  # Disabled for integer operations
            else:
                btn = ttk.Button(
                    self.keypad_frame, 
                    text=key,
                    command=lambda k=key: self.append_digit(k)
                )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self.num_buttons[key] = btn
            
            # In binary mode, only 0 and 1 are enabled
            if key in ['2', '3', '4', '5', '6', '7', '8', '9']:
                if self.display_base == "bin":
                    btn.state(['disabled'])
                    
            # In octal mode, 8 and 9 are disabled
            if key in ['8', '9']:
                if self.display_base == "oct":
                    btn.state(['disabled'])
        
        # Set up keyboard bindings
        self.setup_keyboard_bindings()
        
        # Initialize displays
        self.update_displays()
    
    def setup_keyboard_bindings(self):
        # Number keys
        for i in range(10):
            self.master.bind(str(i), lambda e, digit=i: self.append_digit(str(digit)))
        
        # Hex keys
        for c in 'abcdef':
            self.master.bind(c, lambda e, digit=c.upper(): self.append_digit(digit))
            self.master.bind(c.upper(), lambda e, digit=c.upper(): self.append_digit(digit))
        
        # Operation keys
        self.master.bind("+", lambda e: self.handle_operation("+"))
        self.master.bind("-", lambda e: self.handle_operation("-"))
        self.master.bind("*", lambda e: self.handle_operation("*"))
        self.master.bind("/", lambda e: self.handle_operation("/"))
        
        # Equals and Enter
        self.master.bind("=", lambda e: self.handle_operation("="))
        self.master.bind("<Return>", lambda e: self.handle_operation("="))
        
        # Clear
        self.master.bind("<Escape>", lambda e: self.clear())
        
        # Backspace
        self.master.bind("<BackSpace>", lambda e: self.backspace())
    
    def change_base(self):
        self.display_base = self.base_var.get()
        
        # Update button states based on selected base
        self.update_button_states()
        
        # Update displays
        self.update_displays()
    
    def update_button_states(self):
        # Reset all number buttons
        for key in '0123456789':
            if key in self.num_buttons:
                self.num_buttons[key].state(['!disabled'])
        
        # Reset all hex buttons
        for key in 'ABCDEF':
            if key in self.hex_buttons:
                self.hex_buttons[key].state(['disabled'])
        
        # Update based on current base
        if self.display_base == "bin":
            # Binary: only 0 and 1 allowed
            for key in '23456789':
                if key in self.num_buttons:
                    self.num_buttons[key].state(['disabled'])
        elif self.display_base == "oct":
            # Octal: 0-7 allowed
            for key in '89':
                if key in self.num_buttons:
                    self.num_buttons[key].state(['disabled'])
        elif self.display_base == "hex":
            # Hexadecimal: 0-9 and A-F allowed
            for key in 'ABCDEF':
                if key in self.hex_buttons:
                    self.hex_buttons[key].state(['!disabled'])
    
    def update_displays(self):
        # Get current value
        value = self.current_value
        
        # Get word size in bits
        word_size = int(self.word_size.get())
        max_value = (1 << word_size) - 1
        
        # Apply word size mask
        value = value & max_value
        
        # Update displays
        self.displays["bin"].config(state="normal")
        self.displays["bin"].delete(0, tk.END)
        # Format binary with word size and add spaces every 4 bits
        bin_str = format(value, f'0{word_size}b')
        formatted_bin = ' '.join(bin_str[i:i+4] for i in range(0, len(bin_str), 4))
        self.displays["bin"].insert(0, formatted_bin)
        self.displays["bin"].config(state="readonly")
        
        self.displays["oct"].config(state="normal")
        self.displays["oct"].delete(0, tk.END)
        self.displays["oct"].insert(0, format(value, 'o'))
        self.displays["oct"].config(state="readonly")
        
        self.displays["dec"].config(state="normal")
        self.displays["dec"].delete(0, tk.END)
        self.displays["dec"].insert(0, str(value))
        self.displays["dec"].config(state="readonly")
        
        self.displays["hex"].config(state="normal")
        self.displays["hex"].delete(0, tk.END)
        self.displays["hex"].insert(0, format(value, 'X'))
        self.displays["hex"].config(state="readonly")
    
    def append_digit(self, digit):
        base = self.get_base_value()
        
        # Convert current value to string in current base
        if self.display_base == "bin":
            current = format(self.current_value, 'b')
        elif self.display_base == "oct":
            current = format(self.current_value, 'o')
        elif self.display_base == "dec":
            current = str(self.current_value)
        elif self.display_base == "hex":
            current = format(self.current_value, 'X')
        
        # Append the new digit
        current += digit
        
        # Convert back to integer
        self.current_value = int(current, base)
        
        # Update displays
        self.update_displays()
    
    def get_base_value(self):
        if self.display_base == "bin":
            return 2
        elif self.display_base == "oct":
            return 8
        elif self.display_base == "dec":
            return 10
        elif self.display_base == "hex":
            return 16
        return 10  # Default to decimal
    
    def handle_operation(self, op):
        # For now, just add to history
        if op == "=":
            # Add current value to history
            base_str = self.display_base.upper()
            value_str = self.displays[self.display_base].get()
            
            self.history_manager.add_entry(
                "Programmer",
                f"{value_str} ({base_str})",
                f"Value in different bases"
            )
    
    def bitwise_and(self):
        # Prompt for second operand
        self.prompt_for_second_operand("AND")
    
    def bitwise_or(self):
        # Prompt for second operand
        self.prompt_for_second_operand("OR")
    
    def bitwise_xor(self):
        # Prompt for second operand
        self.prompt_for_second_operand("XOR")
    
    def bitwise_not(self):
        # Perform NOT operation
        word_size = int(self.word_size.get())
        mask = (1 << word_size) - 1
        
        # Record original value
        original = self.current_value
        
        # Perform NOT with masking to maintain word size
        self.current_value = (~self.current_value) & mask
        
        # Update displays
        self.update_displays()
        
        # Add to history
        self.history_manager.add_entry(
            "Programmer",
            f"NOT {original}",
            f"= {self.current_value}"
        )
    
    def shift_left(self):
        # Prompt for shift amount
        self.prompt_for_shift("<<")
    
    def shift_right(self):
        # Prompt for shift amount
        self.prompt_for_shift(">>")
    
    def prompt_for_second_operand(self, operation):
        # Create a dialog to get the second operand
        dialog = tk.Toplevel(self)
        dialog.title(f"{operation} Operation")
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter second operand:").pack(pady=10)
        
        entry = ttk.Entry(dialog)
        entry.pack(fill=tk.X, padx=20, pady=5)
        entry.focus_set()
        
        def perform_operation():
            try:
                # Get the second operand
                second_value = int(entry.get(), self.get_base_value())
                
                # Record original value
                original = self.current_value
                
                # Perform the operation
                if operation == "AND":
                    self.current_value &= second_value
                elif operation == "OR":
                    self.current_value |= second_value
                elif operation == "XOR":
                    self.current_value ^= second_value
                
                # Update displays
                self.update_displays()
                
                # Add to history
                self.history_manager.add_entry(
                    "Programmer",
                    f"{original} {operation} {second_value}",
                    f"= {self.current_value}"
                )
                
                dialog.destroy()
            except ValueError:
                ttk.Label(dialog, text="Invalid input", foreground="red").pack(pady=5)
        
        ttk.Button(dialog, text="Apply", command=perform_operation).pack(pady=10)
        
        # Handle Enter key
        entry.bind("<Return>", lambda e: perform_operation())
    
    def prompt_for_shift(self, operation):
        # Create a dialog to get the shift amount
        dialog = tk.Toplevel(self)
        dialog.title(f"{operation} Shift")
        dialog.geometry("300x150")
        dialog.transient(self)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter shift amount:").pack(pady=10)
        
        entry = ttk.Entry(dialog)
        entry.pack(fill=tk.X, padx=20, pady=5)
        entry.focus_set()
        
        def perform_shift():
            try:
                # Get the shift amount
                shift_amount = int(entry.get())
                
                # Record original value
                original = self.current_value
                
                # Get word size
                word_size = int(self.word_size.get())
                mask = (1 << word_size) - 1
                
                # Perform the shift
                if operation == "<<":
                    self.current_value = (self.current_value << shift_amount) & mask
                elif operation == ">>":
                    self.current_value = (self.current_value >> shift_amount)
                
                # Update displays
                self.update_displays()
                
                # Add to history
                self.history_manager.add_entry(
                    "Programmer",
                    f"{original} {operation} {shift_amount}",
                    f"= {self.current_value}"
                )
                
                dialog.destroy()
            except ValueError:
                ttk.Label(dialog, text="Invalid input", foreground="red").pack(pady=5)
        
        ttk.Button(dialog, text="Apply", command=perform_shift).pack(pady=10)
        
        # Handle Enter key
        entry.bind("<Return>", lambda e: perform_shift())
    
    def clear(self):
        self.current_value = 0
        self.update_displays()
    
    def backspace(self):
        base = self.get_base_value()
        
        # Convert current value to string in current base
        if self.display_base == "bin":
            current = format(self.current_value, 'b')
        elif self.display_base == "oct":
            current = format(self.current_value, 'o')
        elif self.display_base == "dec":
            current = str(self.current_value)
        elif self.display_base == "hex":
            current = format(self.current_value, 'X')
        
        # Remove the last digit
        if len(current) > 0:
            current = current[:-1]
            
            # Convert back to integer
            self.current_value = int(current, base) if current else 0
        
        # Update displays
        self.update_displays()