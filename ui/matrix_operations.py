import tkinter as tk
from tkinter import ttk
import numpy as np

class MatrixOperationsFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Matrix dimensions
        self.dimensions_frame = ttk.LabelFrame(self.main_container, text="Matrix Dimensions")
        self.dimensions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Matrix A dimensions
        ttk.Label(self.dimensions_frame, text="Matrix A:").grid(row=0, column=0, padx=5, pady=5)
        
        self.matrix_a_rows = tk.IntVar(value=2)
        ttk.Label(self.dimensions_frame, text="Rows:").grid(row=0, column=1, padx=5, pady=5)
        rows_spinbox_a = ttk.Spinbox(
            self.dimensions_frame, 
            from_=1, 
            to=5, 
            width=5,
            textvariable=self.matrix_a_rows,
            command=self.update_matrix_inputs
        )
        rows_spinbox_a.grid(row=0, column=2, padx=5, pady=5)
        
        self.matrix_a_cols = tk.IntVar(value=2)
        ttk.Label(self.dimensions_frame, text="Columns:").grid(row=0, column=3, padx=5, pady=5)
        cols_spinbox_a = ttk.Spinbox(
            self.dimensions_frame, 
            from_=1, 
            to=5, 
            width=5,
            textvariable=self.matrix_a_cols,
            command=self.update_matrix_inputs
        )
        cols_spinbox_a.grid(row=0, column=4, padx=5, pady=5)
        
        # Matrix B dimensions
        ttk.Label(self.dimensions_frame, text="Matrix B:").grid(row=1, column=0, padx=5, pady=5)
        
        self.matrix_b_rows = tk.IntVar(value=2)
        ttk.Label(self.dimensions_frame, text="Rows:").grid(row=1, column=1, padx=5, pady=5)
        rows_spinbox_b = ttk.Spinbox(
            self.dimensions_frame, 
            from_=1, 
            to=5, 
            width=5,
            textvariable=self.matrix_b_rows,
            command=self.update_matrix_inputs
        )
        rows_spinbox_b.grid(row=1, column=2, padx=5, pady=5)
        
        self.matrix_b_cols = tk.IntVar(value=2)
        ttk.Label(self.dimensions_frame, text="Columns:").grid(row=1, column=3, padx=5, pady=5)
        cols_spinbox_b = ttk.Spinbox(
            self.dimensions_frame, 
            from_=1, 
            to=5, 
            width=5,
            textvariable=self.matrix_b_cols,
            command=self.update_matrix_inputs
        )
        cols_spinbox_b.grid(row=1, column=4, padx=5, pady=5)
        
        # Matrix operation selection
        self.operation_frame = ttk.LabelFrame(self.main_container, text="Operation")
        self.operation_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.operation = tk.StringVar(value="add")
        ttk.Radiobutton(
            self.operation_frame, 
            text="Addition (A + B)",
            variable=self.operation,
            value="add"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(
            self.operation_frame, 
            text="Subtraction (A - B)",
            variable=self.operation,
            value="subtract"
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(
            self.operation_frame, 
            text="Multiplication (A × B)",
            variable=self.operation,
            value="multiply"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(
            self.operation_frame, 
            text="Transpose (A^T)",
            variable=self.operation,
            value="transpose_a"
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(
            self.operation_frame, 
            text="Determinant (|A|)",
            variable=self.operation,
            value="determinant_a"
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(
            self.operation_frame, 
            text="Inverse (A^-1)",
            variable=self.operation,
            value="inverse_a"
        ).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        # Create a paned window for matrices
        self.matrices_pane = ttk.PanedWindow(self.main_container, orient=tk.HORIZONTAL)
        self.matrices_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Matrix A input frame
        self.matrix_a_frame = ttk.LabelFrame(self.matrices_pane, text="Matrix A")
        self.matrices_pane.add(self.matrix_a_frame, weight=1)
        
        # Matrix B input frame
        self.matrix_b_frame = ttk.LabelFrame(self.matrices_pane, text="Matrix B")
        self.matrices_pane.add(self.matrix_b_frame, weight=1)
        
        # Result display frame
        self.result_frame = ttk.LabelFrame(self.main_container, text="Result")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize matrix entries
        self.matrix_a_entries = []
        self.matrix_b_entries = []
        self.update_matrix_inputs()
        
        # Create action buttons
        self.button_frame = ttk.Frame(self.main_container)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.calculate_button = ttk.Button(
            self.button_frame,
            text="Calculate",
            command=self.perform_operation
        )
        self.calculate_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_matrices
        )
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def update_matrix_inputs(self):
        # Clear existing entries
        for widget in self.matrix_a_frame.winfo_children():
            widget.destroy()
        
        for widget in self.matrix_b_frame.winfo_children():
            widget.destroy()
        
        # Clear existing entry references
        self.matrix_a_entries = []
        self.matrix_b_entries = []
        
        # Create Matrix A entries
        a_rows = self.matrix_a_rows.get()
        a_cols = self.matrix_a_cols.get()
        
        for i in range(a_rows):
            row_entries = []
            for j in range(a_cols):
                entry = ttk.Entry(self.matrix_a_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.matrix_a_entries.append(row_entries)
        
        # Create Matrix B entries
        b_rows = self.matrix_b_rows.get()
        b_cols = self.matrix_b_cols.get()
        
        for i in range(b_rows):
            row_entries = []
            for j in range(b_cols):
                entry = ttk.Entry(self.matrix_b_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                row_entries.append(entry)
            self.matrix_b_entries.append(row_entries)
        
        # Clear result
        for widget in self.result_frame.winfo_children():
            widget.destroy()
    
    def get_matrix_values(self, entries):
        rows = len(entries)
        cols = len(entries[0])
        
        matrix = np.zeros((rows, cols))
        
        for i in range(rows):
            for j in range(cols):
                try:
                    value = float(entries[i][j].get())
                    # Convert to int if it's a whole number
                    if value.is_integer():
                        value = int(value)
                    matrix[i, j] = value
                except ValueError:
                    matrix[i, j] = 0
        
        return matrix
    
    def perform_operation(self):
        # Clear previous result
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get matrices
            matrix_a = self.get_matrix_values(self.matrix_a_entries)
            matrix_b = self.get_matrix_values(self.matrix_b_entries)
            
            operation = self.operation.get()
            result = None
            operation_str = ""
            
            if operation == "add":
                # Check dimensions
                if matrix_a.shape != matrix_b.shape:
                    self.show_error("Matrix dimensions must match for addition")
                    return
                    
                result = matrix_a + matrix_b
                operation_str = "A + B"
                
            elif operation == "subtract":
                # Check dimensions
                if matrix_a.shape != matrix_b.shape:
                    self.show_error("Matrix dimensions must match for subtraction")
                    return
                    
                result = matrix_a - matrix_b
                operation_str = "A - B"
                
            elif operation == "multiply":
                # Check dimensions
                if matrix_a.shape[1] != matrix_b.shape[0]:
                    self.show_error("Number of columns in A must equal number of rows in B for multiplication")
                    return
                    
                result = np.matmul(matrix_a, matrix_b)
                operation_str = "A × B"
                
            elif operation == "transpose_a":
                result = np.transpose(matrix_a)
                operation_str = "A^T"
                
            elif operation == "determinant_a":
                # Check if matrix is square
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    self.show_error("Matrix must be square to calculate determinant")
                    return
                    
                det = np.linalg.det(matrix_a)
                
                # Display determinant result
                result_label = ttk.Label(
                    self.result_frame,
                    text=f"Determinant = {det:.4f}",
                    font=("Arial", 12)
                )
                result_label.pack(padx=5, pady=5)
                
                # Add to history
                self.history_manager.add_entry(
                    "Matrix Operations",
                    f"Determinant of {matrix_a.shape[0]}x{matrix_a.shape[1]} matrix",
                    f"Determinant = {det:.4f}"
                )
                
                return
                
            elif operation == "inverse_a":
                # Check if matrix is square
                if matrix_a.shape[0] != matrix_a.shape[1]:
                    self.show_error("Matrix must be square to calculate inverse")
                    return
                
                # Check if matrix is invertible
                det = np.linalg.det(matrix_a)
                if abs(det) < 1e-10:
                    self.show_error("Matrix is singular (not invertible)")
                    return
                    
                result = np.linalg.inv(matrix_a)
                operation_str = "A^-1"
            
            # Display result matrix
            self.display_matrix(result)
            
            # Add to history
            if result is not None:
                shape_str = f"{result.shape[0]}x{result.shape[1]}"
                self.history_manager.add_entry(
                    "Matrix Operations",
                    f"{operation_str} ({shape_str})",
                    f"Matrix calculation completed"
                )
            
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def display_matrix(self, matrix):
        rows, cols = matrix.shape
        
        for i in range(rows):
            for j in range(cols):
                value = matrix[i, j]
                
                # Format the value for display
                if value.is_integer():
                    display_value = str(int(value))
                elif abs(value) < 1e-10:
                    display_value = "0"
                else:
                    display_value = f"{value:.4f}"
                
                entry = ttk.Entry(self.result_frame, width=8)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, display_value)
                entry.configure(state="readonly")
    
    def show_error(self, message):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        error_label = ttk.Label(
            self.result_frame,
            text=message,
            foreground="red"
        )
        error_label.pack(padx=5, pady=5)
    
    def clear_matrices(self):
        # Reset all matrix entries to 0
        for row in self.matrix_a_entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
                
        for row in self.matrix_b_entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        
        # Clear result
        for widget in self.result_frame.winfo_children():
            widget.destroy()