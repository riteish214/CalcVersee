import tkinter as tk
from tkinter import ttk
import numpy as np
import sympy as sp
import math

class EquationSolverFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create equation type selector
        self.equation_type_frame = ttk.LabelFrame(self.main_container, text="Equation Type")
        self.equation_type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.equation_type = tk.StringVar(value="linear")
        ttk.Radiobutton(
            self.equation_type_frame, 
            text="Linear Equation (ax + b = 0)",
            variable=self.equation_type,
            value="linear",
            command=self.update_equation_form
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Radiobutton(
            self.equation_type_frame, 
            text="Quadratic Equation (ax² + bx + c = 0)",
            variable=self.equation_type,
            value="quadratic",
            command=self.update_equation_form
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Radiobutton(
            self.equation_type_frame, 
            text="System of Linear Equations (2x2)",
            variable=self.equation_type,
            value="system2x2",
            command=self.update_equation_form
        ).pack(anchor=tk.W, padx=5, pady=2)
        
        # Create input frame
        self.input_frame = ttk.LabelFrame(self.main_container, text="Enter Coefficients")
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Linear equation inputs (default)
        self.linear_frame = ttk.Frame(self.input_frame)
        self.linear_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(self.linear_frame, text="a:").grid(row=0, column=0, padx=5, pady=5)
        self.linear_a = ttk.Entry(self.linear_frame, width=10)
        self.linear_a.grid(row=0, column=1, padx=5, pady=5)
        self.linear_a.insert(0, "1")
        
        ttk.Label(self.linear_frame, text="b:").grid(row=0, column=2, padx=5, pady=5)
        self.linear_b = ttk.Entry(self.linear_frame, width=10)
        self.linear_b.grid(row=0, column=3, padx=5, pady=5)
        self.linear_b.insert(0, "0")
        
        # Create a preview of the equation
        ttk.Label(self.linear_frame, text="Equation:").grid(row=1, column=0, padx=5, pady=5)
        self.linear_equation_preview = ttk.Label(self.linear_frame, text="x + 0 = 0")
        self.linear_equation_preview.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        
        # Bind events to update the equation preview
        self.linear_a.bind("<KeyRelease>", lambda e: self.update_linear_preview())
        self.linear_b.bind("<KeyRelease>", lambda e: self.update_linear_preview())
        
        # Quadratic equation inputs (hidden initially)
        self.quadratic_frame = ttk.Frame(self.input_frame)
        
        ttk.Label(self.quadratic_frame, text="a:").grid(row=0, column=0, padx=5, pady=5)
        self.quadratic_a = ttk.Entry(self.quadratic_frame, width=10)
        self.quadratic_a.grid(row=0, column=1, padx=5, pady=5)
        self.quadratic_a.insert(0, "1")
        
        ttk.Label(self.quadratic_frame, text="b:").grid(row=0, column=2, padx=5, pady=5)
        self.quadratic_b = ttk.Entry(self.quadratic_frame, width=10)
        self.quadratic_b.grid(row=0, column=3, padx=5, pady=5)
        self.quadratic_b.insert(0, "0")
        
        ttk.Label(self.quadratic_frame, text="c:").grid(row=0, column=4, padx=5, pady=5)
        self.quadratic_c = ttk.Entry(self.quadratic_frame, width=10)
        self.quadratic_c.grid(row=0, column=5, padx=5, pady=5)
        self.quadratic_c.insert(0, "0")
        
        # Create a preview of the quadratic equation
        ttk.Label(self.quadratic_frame, text="Equation:").grid(row=1, column=0, padx=5, pady=5)
        self.quadratic_equation_preview = ttk.Label(self.quadratic_frame, text="x² + 0x + 0 = 0")
        self.quadratic_equation_preview.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="w")
        
        # Bind events to update the quadratic equation preview
        self.quadratic_a.bind("<KeyRelease>", lambda e: self.update_quadratic_preview())
        self.quadratic_b.bind("<KeyRelease>", lambda e: self.update_quadratic_preview())
        self.quadratic_c.bind("<KeyRelease>", lambda e: self.update_quadratic_preview())
        
        # System of linear equations inputs (hidden initially)
        self.system_frame = ttk.Frame(self.input_frame)
        
        # First equation: a1x + b1y = c1
        ttk.Label(self.system_frame, text="Equation 1:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.system_frame, text="a₁:").grid(row=1, column=0, padx=5, pady=5)
        self.system_a1 = ttk.Entry(self.system_frame, width=5)
        self.system_a1.grid(row=1, column=1, padx=5, pady=5)
        self.system_a1.insert(0, "1")
        
        ttk.Label(self.system_frame, text="x +").grid(row=1, column=2, padx=2, pady=5)
        
        ttk.Label(self.system_frame, text="b₁:").grid(row=1, column=3, padx=5, pady=5)
        self.system_b1 = ttk.Entry(self.system_frame, width=5)
        self.system_b1.grid(row=1, column=4, padx=5, pady=5)
        self.system_b1.insert(0, "1")
        
        ttk.Label(self.system_frame, text="y =").grid(row=1, column=5, padx=2, pady=5)
        
        ttk.Label(self.system_frame, text="c₁:").grid(row=1, column=6, padx=5, pady=5)
        self.system_c1 = ttk.Entry(self.system_frame, width=5)
        self.system_c1.grid(row=1, column=7, padx=5, pady=5)
        self.system_c1.insert(0, "0")
        
        # Second equation: a2x + b2y = c2
        ttk.Label(self.system_frame, text="Equation 2:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.system_frame, text="a₂:").grid(row=3, column=0, padx=5, pady=5)
        self.system_a2 = ttk.Entry(self.system_frame, width=5)
        self.system_a2.grid(row=3, column=1, padx=5, pady=5)
        self.system_a2.insert(0, "0")
        
        ttk.Label(self.system_frame, text="x +").grid(row=3, column=2, padx=2, pady=5)
        
        ttk.Label(self.system_frame, text="b₂:").grid(row=3, column=3, padx=5, pady=5)
        self.system_b2 = ttk.Entry(self.system_frame, width=5)
        self.system_b2.grid(row=3, column=4, padx=5, pady=5)
        self.system_b2.insert(0, "1")
        
        ttk.Label(self.system_frame, text="y =").grid(row=3, column=5, padx=2, pady=5)
        
        ttk.Label(self.system_frame, text="c₂:").grid(row=3, column=6, padx=5, pady=5)
        self.system_c2 = ttk.Entry(self.system_frame, width=5)
        self.system_c2.grid(row=3, column=7, padx=5, pady=5)
        self.system_c2.insert(0, "0")
        
        # Create action buttons
        self.button_frame = ttk.Frame(self.main_container)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.solve_button = ttk.Button(
            self.button_frame,
            text="Solve",
            command=self.solve_equation
        )
        self.solve_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_inputs
        )
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Create result display
        self.result_frame = ttk.LabelFrame(self.main_container, text="Results")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(
            self.result_frame,
            height=10,
            width=50,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Update the initial equation preview
        self.update_linear_preview()
    
    def update_equation_form(self):
        # Hide all frames
        self.linear_frame.pack_forget()
        self.quadratic_frame.pack_forget()
        self.system_frame.pack_forget()
        
        # Show the selected frame
        if self.equation_type.get() == "linear":
            self.linear_frame.pack(fill=tk.X, padx=5, pady=5)
            self.update_linear_preview()
        elif self.equation_type.get() == "quadratic":
            self.quadratic_frame.pack(fill=tk.X, padx=5, pady=5)
            self.update_quadratic_preview()
        elif self.equation_type.get() == "system2x2":
            self.system_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def update_linear_preview(self):
        try:
            a = float(self.linear_a.get() or "0")
            b = float(self.linear_b.get() or "0")
            
            a_str = "" if a == 1 else "-" if a == -1 else f"{a}"
            b_str = f"+ {b}" if b > 0 else f"- {abs(b)}" if b < 0 else ""
            
            equation = f"{a_str}x {b_str} = 0"
            self.linear_equation_preview.config(text=equation)
        except ValueError:
            self.linear_equation_preview.config(text="Invalid input")
    
    def update_quadratic_preview(self):
        try:
            a = float(self.quadratic_a.get() or "0")
            b = float(self.quadratic_b.get() or "0")
            c = float(self.quadratic_c.get() or "0")
            
            a_str = "" if a == 1 else "-" if a == -1 else f"{a}"
            b_str = f"+ {b}x" if b > 0 else f"- {abs(b)}x" if b < 0 else ""
            c_str = f"+ {c}" if c > 0 else f"- {abs(c)}" if c < 0 else ""
            
            equation = f"{a_str}x² {b_str} {c_str} = 0"
            self.quadratic_equation_preview.config(text=equation)
        except ValueError:
            self.quadratic_equation_preview.config(text="Invalid input")
    
    def solve_equation(self):
        eq_type = self.equation_type.get()
        
        try:
            if eq_type == "linear":
                self.solve_linear_equation()
            elif eq_type == "quadratic":
                self.solve_quadratic_equation()
            elif eq_type == "system2x2":
                self.solve_system_of_equations()
        except Exception as e:
            self.display_result(f"Error: {str(e)}")
    
    def solve_linear_equation(self):
        try:
            a = float(self.linear_a.get() or "0")
            b = float(self.linear_b.get() or "0")
            
            if a == 0:
                if b == 0:
                    result = "Infinite solutions (identity)"
                else:
                    result = "No solution (contradiction)"
            else:
                x = -b / a
                result = f"x = {x}"
                
                # For nicer display, check if it's close to an integer
                if abs(x - round(x)) < 1e-10:
                    result = f"x = {int(round(x))}"
            
            # Create the equation for history
            a_str = "" if a == 1 else "-" if a == -1 else f"{a}"
            b_str = f"+ {b}" if b > 0 else f"- {abs(b)}" if b < 0 else ""
            equation = f"{a_str}x {b_str} = 0"
            
            # Add to history
            self.history_manager.add_entry(
                "Equation Solver",
                equation,
                result
            )
            
            # Display the result with steps
            steps = [
                f"Equation: {equation}",
                f"Step 1: Solve for x by isolating the variable",
            ]
            
            if a != 0:
                steps.append(f"Step 2: x = -b/a = -({b})/{a} = {-b}/{a}")
                steps.append(f"Result: {result}")
            else:
                steps.append(f"Result: {result}")
            
            self.display_result("\n".join(steps))
            
        except ValueError:
            self.display_result("Error: Please enter valid numeric coefficients")
        except ZeroDivisionError:
            self.display_result("Error: Division by zero")
    
    def solve_quadratic_equation(self):
        try:
            a = float(self.quadratic_a.get() or "0")
            b = float(self.quadratic_b.get() or "0")
            c = float(self.quadratic_c.get() or "0")
            
            # Create the equation for history
            a_str = "" if a == 1 else "-" if a == -1 else f"{a}"
            b_str = f"+ {b}x" if b > 0 else f"- {abs(b)}x" if b < 0 else ""
            c_str = f"+ {c}" if c > 0 else f"- {abs(c)}" if c < 0 else ""
            equation = f"{a_str}x² {b_str} {c_str} = 0"
            
            if a == 0:
                # This is actually a linear equation
                if b == 0:
                    if c == 0:
                        result = "Infinite solutions (identity)"
                    else:
                        result = "No solution (contradiction)"
                else:
                    x = -c / b
                    result = f"x = {x}"
                
                steps = [
                    f"Equation: {equation}",
                    "Note: This is actually a linear equation (a = 0)",
                    f"Solving: {b}x + {c} = 0",
                    f"x = -{c}/{b} = {-c}/{b}",
                    f"Result: {result}"
                ]
            else:
                # Calculate the discriminant
                discriminant = b**2 - 4*a*c
                
                steps = [
                    f"Equation: {equation}",
                    f"Step 1: Calculate the discriminant (b² - 4ac)",
                    f"Discriminant = {b}² - 4({a})({c}) = {b**2} - {4*a*c} = {discriminant}"
                ]
                
                if discriminant > 0:
                    # Two real solutions
                    x1 = (-b + math.sqrt(discriminant)) / (2*a)
                    x2 = (-b - math.sqrt(discriminant)) / (2*a)
                    
                    # For nicer display, check if solutions are close to integers
                    if abs(x1 - round(x1)) < 1e-10:
                        x1 = int(round(x1))
                    if abs(x2 - round(x2)) < 1e-10:
                        x2 = int(round(x2))
                    
                    result = f"x₁ = {x1}, x₂ = {x2}"
                    
                    steps.append("Step 2: Discriminant > 0, so there are two real solutions")
                    steps.append(f"x₁ = (-b + √discriminant)/(2a) = ({-b} + √{discriminant})/{2*a} = {x1}")
                    steps.append(f"x₂ = (-b - √discriminant)/(2a) = ({-b} - √{discriminant})/{2*a} = {x2}")
                    
                elif discriminant == 0:
                    # One real solution (double root)
                    x = -b / (2*a)
                    
                    # For nicer display, check if solution is close to an integer
                    if abs(x - round(x)) < 1e-10:
                        x = int(round(x))
                    
                    result = f"x = {x} (double root)"
                    
                    steps.append("Step 2: Discriminant = 0, so there is one real solution (double root)")
                    steps.append(f"x = -b/(2a) = {-b}/{2*a} = {x}")
                    
                else:
                    # Complex solutions
                    real_part = -b / (2*a)
                    imag_part = math.sqrt(abs(discriminant)) / (2*a)
                    
                    # For nicer display, check if parts are close to integers
                    if abs(real_part - round(real_part)) < 1e-10:
                        real_part = int(round(real_part))
                    if abs(imag_part - round(imag_part)) < 1e-10:
                        imag_part = int(round(imag_part))
                    
                    result = f"x₁ = {real_part} + {imag_part}i, x₂ = {real_part} - {imag_part}i"
                    
                    steps.append("Step 2: Discriminant < 0, so there are two complex solutions")
                    steps.append(f"Real part = -b/(2a) = {-b}/{2*a} = {real_part}")
                    steps.append(f"Imaginary part = √|discriminant|/(2a) = √{abs(discriminant)}/{2*a} = {imag_part}")
                    steps.append(f"x₁ = {real_part} + {imag_part}i")
                    steps.append(f"x₂ = {real_part} - {imag_part}i")
            
            steps.append(f"Result: {result}")
            
            # Add to history
            self.history_manager.add_entry(
                "Equation Solver",
                equation,
                result
            )
            
            self.display_result("\n".join(steps))
            
        except ValueError:
            self.display_result("Error: Please enter valid numeric coefficients")
        except ZeroDivisionError:
            self.display_result("Error: Division by zero")
    
    def solve_system_of_equations(self):
        try:
            a1 = float(self.system_a1.get() or "0")
            b1 = float(self.system_b1.get() or "0")
            c1 = float(self.system_c1.get() or "0")
            a2 = float(self.system_a2.get() or "0")
            b2 = float(self.system_b2.get() or "0")
            c2 = float(self.system_c2.get() or "0")
            
            # Create the system equations for history
            equation1 = f"{a1}x + {b1}y = {c1}"
            equation2 = f"{a2}x + {b2}y = {c2}"
            system = f"{equation1}, {equation2}"
            
            # Calculate the determinant of the coefficient matrix
            det = a1 * b2 - a2 * b1
            
            steps = [
                f"System of equations:",
                f"Equation 1: {equation1}",
                f"Equation 2: {equation2}",
                f"Step 1: Calculate the determinant of the coefficient matrix",
                f"det = a₁b₂ - a₂b₁ = ({a1})({b2}) - ({a2})({b1}) = {a1*b2} - {a2*b1} = {det}"
            ]
            
            if det == 0:
                # Check if the system is consistent (has infinitely many solutions)
                if a1 * c2 == a2 * c1 and b1 * c2 == b2 * c1:
                    result = "Infinite solutions (dependent equations)"
                    steps.append("Step 2: Determinant = 0 and equations are consistent")
                    steps.append("Result: Infinite solutions (dependent equations)")
                else:
                    result = "No solution (inconsistent system)"
                    steps.append("Step 2: Determinant = 0 but equations are inconsistent")
                    steps.append("Result: No solution (inconsistent system)")
            else:
                # Solve using Cramer's rule
                det_x = c1 * b2 - c2 * b1
                det_y = a1 * c2 - a2 * c1
                
                x = det_x / det
                y = det_y / det
                
                # For nicer display, check if solutions are close to integers
                if abs(x - round(x)) < 1e-10:
                    x = int(round(x))
                if abs(y - round(y)) < 1e-10:
                    y = int(round(y))
                
                result = f"x = {x}, y = {y}"
                
                steps.append("Step 2: Determinant ≠ 0, so there is a unique solution")
                steps.append("Step 3: Using Cramer's rule to solve for x and y")
                steps.append(f"det_x = c₁b₂ - c₂b₁ = ({c1})({b2}) - ({c2})({b1}) = {c1*b2} - {c2*b1} = {det_x}")
                steps.append(f"det_y = a₁c₂ - a₂c₁ = ({a1})({c2}) - ({a2})({c1}) = {a1*c2} - {a2*c1} = {det_y}")
                steps.append(f"x = det_x/det = {det_x}/{det} = {x}")
                steps.append(f"y = det_y/det = {det_y}/{det} = {y}")
                steps.append(f"Result: {result}")
            
            # Add to history
            self.history_manager.add_entry(
                "Equation Solver",
                system,
                result
            )
            
            self.display_result("\n".join(steps))
            
        except ValueError:
            self.display_result("Error: Please enter valid numeric coefficients")
        except ZeroDivisionError:
            self.display_result("Error: Division by zero")
    
    def clear_inputs(self):
        if self.equation_type.get() == "linear":
            self.linear_a.delete(0, tk.END)
            self.linear_a.insert(0, "1")
            self.linear_b.delete(0, tk.END)
            self.linear_b.insert(0, "0")
            self.update_linear_preview()
        elif self.equation_type.get() == "quadratic":
            self.quadratic_a.delete(0, tk.END)
            self.quadratic_a.insert(0, "1")
            self.quadratic_b.delete(0, tk.END)
            self.quadratic_b.insert(0, "0")
            self.quadratic_c.delete(0, tk.END)
            self.quadratic_c.insert(0, "0")
            self.update_quadratic_preview()
        elif self.equation_type.get() == "system2x2":
            self.system_a1.delete(0, tk.END)
            self.system_a1.insert(0, "1")
            self.system_b1.delete(0, tk.END)
            self.system_b1.insert(0, "1")
            self.system_c1.delete(0, tk.END)
            self.system_c1.insert(0, "0")
            self.system_a2.delete(0, tk.END)
            self.system_a2.insert(0, "0")
            self.system_b2.delete(0, tk.END)
            self.system_b2.insert(0, "1")
            self.system_c2.delete(0, tk.END)
            self.system_c2.insert(0, "0")
        
        self.display_result("")
    
    def display_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)