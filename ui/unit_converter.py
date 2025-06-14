import tkinter as tk
from tkinter import ttk

class UnitConverterFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Define unit categories and conversions
        self.unit_categories = {
            "Length": {
                "Meter": 1.0,
                "Kilometer": 1000.0,
                "Centimeter": 0.01,
                "Millimeter": 0.001,
                "Inch": 0.0254,
                "Foot": 0.3048,
                "Yard": 0.9144,
                "Mile": 1609.344
            },
            "Weight/Mass": {
                "Kilogram": 1.0,
                "Gram": 0.001,
                "Milligram": 0.000001,
                "Pound": 0.45359237,
                "Ounce": 0.028349523125,
                "Ton": 1000.0
            },
            "Temperature": {
                "Celsius": "C",
                "Fahrenheit": "F",
                "Kelvin": "K"
            },
            "Area": {
                "Square Meter": 1.0,
                "Square Kilometer": 1000000.0,
                "Square Centimeter": 0.0001,
                "Square Millimeter": 0.000001,
                "Square Inch": 0.00064516,
                "Square Foot": 0.09290304,
                "Square Yard": 0.83612736,
                "Acre": 4046.8564224,
                "Hectare": 10000.0
            },
            "Volume": {
                "Cubic Meter": 1.0,
                "Cubic Centimeter": 0.000001,
                "Liter": 0.001,
                "Milliliter": 0.000001,
                "Gallon (US)": 0.00378541,
                "Quart (US)": 0.000946353,
                "Pint (US)": 0.000473176,
                "Cup (US)": 0.000236588,
                "Fluid Ounce (US)": 0.0000295735,
                "Cubic Inch": 0.0000163871,
                "Cubic Foot": 0.0283168
            },
            "Time": {
                "Second": 1.0,
                "Minute": 60.0,
                "Hour": 3600.0,
                "Day": 86400.0,
                "Week": 604800.0,
                "Month (30 days)": 2592000.0,
                "Year (365 days)": 31536000.0
            },
            "Speed": {
                "Meter per Second": 1.0,
                "Kilometer per Hour": 0.277778,
                "Mile per Hour": 0.44704,
                "Knot": 0.514444,
                "Foot per Second": 0.3048
            },
            "Pressure": {
                "Pascal": 1.0,
                "Kilopascal": 1000.0,
                "Bar": 100000.0,
                "Atmosphere": 101325.0,
                "mmHg": 133.322,
                "PSI": 6894.76
            }
        }
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create category selector
        self.category_frame = ttk.LabelFrame(self.main_container, text="Unit Category")
        self.category_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.category_var = tk.StringVar()
        category_combobox = ttk.Combobox(
            self.category_frame,
            textvariable=self.category_var,
            values=list(self.unit_categories.keys()),
            state="readonly",
            width=20
        )
        category_combobox.pack(padx=10, pady=5)
        category_combobox.bind("<<ComboboxSelected>>", self.update_unit_options)
        
        # Set default category
        self.category_var.set("Length")
        
        # Create unit conversion frame
        self.conversion_frame = ttk.LabelFrame(self.main_container, text="Unit Conversion")
        self.conversion_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # From unit
        from_frame = ttk.Frame(self.conversion_frame)
        from_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(from_frame, text="From:").pack(side=tk.LEFT, padx=5)
        
        self.from_unit_var = tk.StringVar()
        self.from_unit_combobox = ttk.Combobox(
            from_frame,
            textvariable=self.from_unit_var,
            state="readonly",
            width=15
        )
        self.from_unit_combobox.pack(side=tk.LEFT, padx=5)
        self.from_unit_combobox.bind("<<ComboboxSelected>>", self.convert)
        
        self.from_value_var = tk.StringVar(value="1")
        from_value_entry = ttk.Entry(
            from_frame,
            textvariable=self.from_value_var,
            width=15
        )
        from_value_entry.pack(side=tk.LEFT, padx=5)
        from_value_entry.bind("<KeyRelease>", self.convert)
        
        # To unit
        to_frame = ttk.Frame(self.conversion_frame)
        to_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(to_frame, text="To:").pack(side=tk.LEFT, padx=5)
        
        self.to_unit_var = tk.StringVar()
        self.to_unit_combobox = ttk.Combobox(
            to_frame,
            textvariable=self.to_unit_var,
            state="readonly",
            width=15
        )
        self.to_unit_combobox.pack(side=tk.LEFT, padx=5)
        self.to_unit_combobox.bind("<<ComboboxSelected>>", self.convert)
        
        self.to_value_var = tk.StringVar()
        self.to_value_entry = ttk.Entry(
            to_frame,
            textvariable=self.to_value_var,
            width=15,
            state="readonly"
        )
        self.to_value_entry.pack(side=tk.LEFT, padx=5)
        
        # Formula display
        formula_frame = ttk.Frame(self.conversion_frame)
        formula_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(formula_frame, text="Formula:").pack(side=tk.LEFT, padx=5)
        
        self.formula_var = tk.StringVar()
        formula_label = ttk.Label(
            formula_frame,
            textvariable=self.formula_var,
            font=("Arial", 10)
        )
        formula_label.pack(side=tk.LEFT, padx=5)
        
        # Common values display
        self.common_values_frame = ttk.LabelFrame(self.main_container, text="Common Values")
        self.common_values_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize unit options
        self.update_unit_options()
    
    def update_unit_options(self, event=None):
        category = self.category_var.get()
        units = list(self.unit_categories[category].keys())
        
        # Update from unit combobox
        self.from_unit_combobox.config(values=units)
        if not self.from_unit_var.get() in units:
            self.from_unit_var.set(units[0])
        
        # Update to unit combobox
        self.to_unit_combobox.config(values=units)
        if not self.to_unit_var.get() in units:
            self.to_unit_var.set(units[1] if len(units) > 1 else units[0])
        
        # Update conversion
        self.convert()
        
        # Update common values
        self.update_common_values()
    
    def convert(self, event=None):
        try:
            # Get selected category, units and value
            category = self.category_var.get()
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            
            # If units not set yet, return
            if not from_unit or not to_unit:
                return
            
            # Get the input value
            try:
                from_value = float(self.from_value_var.get())
            except ValueError:
                self.to_value_var.set("Invalid input")
                self.formula_var.set("")
                return
            
            # Handle temperature conversion specially
            if category == "Temperature":
                converted_value, formula = self.convert_temperature(from_unit, to_unit, from_value)
            else:
                # Get conversion factors
                from_factor = self.unit_categories[category][from_unit]
                to_factor = self.unit_categories[category][to_unit]
                
                # Convert to base unit then to target unit
                base_value = from_value * from_factor
                converted_value = base_value / to_factor
                
                # Create formula string
                if from_factor == to_factor:
                    formula = f"{from_value} {from_unit} = {converted_value} {to_unit}"
                else:
                    formula = f"{from_value} {from_unit} × {from_factor} ÷ {to_factor} = {converted_value} {to_unit}"
            
            # Format the result
            if abs(converted_value) < 0.000001 and converted_value != 0:
                formatted_value = f"{converted_value:.10e}"
            elif abs(converted_value) > 1000000:
                formatted_value = f"{converted_value:.10e}"
            else:
                formatted_value = f"{converted_value:.10g}"
            
            # Update the result
            self.to_value_var.set(formatted_value)
            self.formula_var.set(formula)
            
            # Add to history
            self.history_manager.add_entry(
                "Unit Converter",
                f"{from_value} {from_unit} to {to_unit}",
                f"{formatted_value} {to_unit}"
            )
            
        except Exception as e:
            self.to_value_var.set(f"Error: {str(e)}")
            self.formula_var.set("")
    
    def convert_temperature(self, from_unit, to_unit, value):
        # Convert to Celsius first (as base unit)
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5/9
            formula_part_1 = f"({value}°F - 32) × 5/9 = {celsius}°C"
        elif from_unit == "Kelvin":
            celsius = value - 273.15
            formula_part_1 = f"{value}K - 273.15 = {celsius}°C"
        
        # Convert from Celsius to target unit
        if to_unit == "Celsius":
            result = celsius
            if from_unit == "Celsius":
                formula = f"{value}°C = {result}°C"
            else:
                formula = formula_part_1
        elif to_unit == "Fahrenheit":
            result = celsius * 9/5 + 32
            if from_unit == "Celsius":
                formula = f"{value}°C × 9/5 + 32 = {result}°F"
            else:
                formula = f"{formula_part_1}, then {celsius}°C × 9/5 + 32 = {result}°F"
        elif to_unit == "Kelvin":
            result = celsius + 273.15
            if from_unit == "Celsius":
                formula = f"{value}°C + 273.15 = {result}K"
            else:
                formula = f"{formula_part_1}, then {celsius}°C + 273.15 = {result}K"
        
        return result, formula
    
    def update_common_values(self):
        # Clear existing widgets
        for widget in self.common_values_frame.winfo_children():
            widget.destroy()
        
        # Get current category and units
        category = self.category_var.get()
        from_unit = self.from_unit_var.get()
        
        # Create a scrollable frame for common values
        canvas = tk.Canvas(self.common_values_frame)
        scrollbar = ttk.Scrollbar(self.common_values_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add common values based on category
        if category == "Length":
            common_values = [1, 10, 100, 1000]
            for value in common_values:
                self.add_common_value_row(scrollable_frame, value, from_unit)
        elif category == "Weight/Mass":
            common_values = [1, 10, 100, 1000]
            for value in common_values:
                self.add_common_value_row(scrollable_frame, value, from_unit)
        elif category == "Temperature":
            if from_unit == "Celsius":
                common_values = [0, 20, 37, 100]
            elif from_unit == "Fahrenheit":
                common_values = [32, 68, 98.6, 212]
            elif from_unit == "Kelvin":
                common_values = [273.15, 293.15, 310.15, 373.15]
            for value in common_values:
                self.add_common_value_row(scrollable_frame, value, from_unit)
        else:
            common_values = [1, 10, 100, 1000]
            for value in common_values:
                self.add_common_value_row(scrollable_frame, value, from_unit)
    
    def add_common_value_row(self, parent, value, unit):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, padx=5, pady=2)
        
        # Display the common value
        ttk.Label(row, text=f"{value} {unit}:", width=15, anchor="e").pack(side=tk.LEFT, padx=5)
        
        # Calculate conversions to all other units
        category = self.category_var.get()
        units = self.unit_categories[category]
        
        # Create a subframe for the conversions
        conversions_frame = ttk.Frame(row)
        conversions_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add each conversion
        for target_unit in units:
            if target_unit != unit:
                # Calculate the conversion
                if category == "Temperature":
                    try:
                        converted_value, _ = self.convert_temperature(unit, target_unit, value)
                    except:
                        continue
                else:
                    from_factor = units[unit]
                    to_factor = units[target_unit]
                    base_value = value * from_factor
                    converted_value = base_value / to_factor
                
                # Format the result
                if abs(converted_value) < 0.000001 and converted_value != 0:
                    formatted_value = f"{converted_value:.6e}"
                elif abs(converted_value) > 1000000:
                    formatted_value = f"{converted_value:.6e}"
                else:
                    formatted_value = f"{converted_value:.6g}"
                
                # Add the conversion to the frame
                conversion_text = f"{formatted_value} {target_unit}"
                ttk.Label(conversions_frame, text=conversion_text).pack(anchor="w", padx=5, pady=1)