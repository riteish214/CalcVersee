import tkinter as tk
from tkinter import ttk
import json
import threading
import time
from datetime import datetime
import requests

class CurrencyConverterFrame(ttk.Frame):
    def __init__(self, parent, history_manager):
        super().__init__(parent, padding="10")
        self.history_manager = history_manager
        
        # API endpoint for exchange rates
        self.api_url = "https://open.er-api.com/v6/latest/USD"
        
        # Currency data
        self.exchange_rates = {}
        self.last_updated = None
        self.loading = True
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_container)
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Loading exchange rates...",
            foreground="blue"
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.update_button = ttk.Button(
            self.status_frame,
            text="Update Rates",
            command=self.fetch_exchange_rates,
            state="disabled"
        )
        self.update_button.pack(side=tk.RIGHT, padx=5)
        
        # Create conversion frame
        self.conversion_frame = ttk.LabelFrame(self.main_container, text="Currency Conversion")
        self.conversion_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # From currency
        from_frame = ttk.Frame(self.conversion_frame)
        from_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(from_frame, text="From:").pack(side=tk.LEFT, padx=5)
        
        self.from_currency_var = tk.StringVar(value="USD")
        self.from_currency_combobox = ttk.Combobox(
            from_frame,
            textvariable=self.from_currency_var,
            state="readonly",
            width=10
        )
        self.from_currency_combobox.pack(side=tk.LEFT, padx=5)
        self.from_currency_combobox.bind("<<ComboboxSelected>>", self.convert)
        
        self.from_amount_var = tk.StringVar(value="1")
        from_amount_entry = ttk.Entry(
            from_frame,
            textvariable=self.from_amount_var,
            width=15
        )
        from_amount_entry.pack(side=tk.LEFT, padx=5)
        from_amount_entry.bind("<KeyRelease>", self.convert)
        
        # To currency
        to_frame = ttk.Frame(self.conversion_frame)
        to_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(to_frame, text="To:").pack(side=tk.LEFT, padx=5)
        
        self.to_currency_var = tk.StringVar(value="EUR")
        self.to_currency_combobox = ttk.Combobox(
            to_frame,
            textvariable=self.to_currency_var,
            state="readonly",
            width=10
        )
        self.to_currency_combobox.pack(side=tk.LEFT, padx=5)
        self.to_currency_combobox.bind("<<ComboboxSelected>>", self.convert)
        
        self.to_amount_var = tk.StringVar()
        self.to_amount_entry = ttk.Entry(
            to_frame,
            textvariable=self.to_amount_var,
            width=15,
            state="readonly"
        )
        self.to_amount_entry.pack(side=tk.LEFT, padx=5)
        
        # Exchange rate display
        rate_frame = ttk.Frame(self.conversion_frame)
        rate_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(rate_frame, text="Exchange Rate:").pack(side=tk.LEFT, padx=5)
        
        self.rate_var = tk.StringVar()
        rate_label = ttk.Label(
            rate_frame,
            textvariable=self.rate_var,
            font=("Arial", 10, "bold")
        )
        rate_label.pack(side=tk.LEFT, padx=5)
        
        # Swap button
        swap_button = ttk.Button(
            self.conversion_frame,
            text="⇄ Swap Currencies",
            command=self.swap_currencies
        )
        swap_button.pack(padx=10, pady=5)
        
        # Popular currencies list
        self.popular_frame = ttk.LabelFrame(self.main_container, text="Popular Currencies (vs USD)")
        self.popular_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a canvas with scrollbar for popular currencies
        canvas = tk.Canvas(self.popular_frame)
        scrollbar = ttk.Scrollbar(self.popular_frame, orient="vertical", command=canvas.yview)
        self.popular_scrollable_frame = ttk.Frame(canvas)
        
        self.popular_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.popular_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Fetch exchange rates in a separate thread
        threading.Thread(target=self.fetch_exchange_rates, daemon=True).start()
    
    def fetch_exchange_rates(self):
        # Update status
        self.status_label.config(text="Loading exchange rates...", foreground="blue")
        self.update_button.config(state="disabled")
        self.loading = True
        
        try:
            # Fetch exchange rates from API
            response = requests.get(self.api_url)
            data = response.json()
            
            if data.get("result") == "success":
                # Extract exchange rates
                self.exchange_rates = data.get("rates", {})
                
                # Extract timestamp and convert to datetime
                timestamp = data.get("time_last_update_unix", 0)
                self.last_updated = datetime.fromtimestamp(timestamp)
                
                # Update currency comboboxes
                currencies = sorted(self.exchange_rates.keys())
                self.from_currency_combobox.config(values=currencies)
                self.to_currency_combobox.config(values=currencies)
                
                # Set default values if not already set
                if not self.from_currency_var.get() in currencies:
                    self.from_currency_var.set("USD")
                if not self.to_currency_var.get() in currencies:
                    self.to_currency_var.set("EUR" if "EUR" in currencies else currencies[0])
                
                # Update status
                last_updated_str = self.last_updated.strftime("%Y-%m-%d %H:%M:%S")
                self.status_label.config(
                    text=f"Rates updated: {last_updated_str}",
                    foreground="green"
                )
                
                # Update popular currencies
                self.update_popular_currencies()
                
                # Perform conversion
                self.convert()
            else:
                # API error
                error_msg = data.get("error-type", "Unknown error")
                self.status_label.config(
                    text=f"Error loading rates: {error_msg}",
                    foreground="red"
                )
        except Exception as e:
            # Network or parsing error
            self.status_label.config(
                text=f"Error: {str(e)}",
                foreground="red"
            )
        
        # Enable update button
        self.update_button.config(state="normal")
        self.loading = False
    
    def convert(self, event=None):
        if self.loading or not self.exchange_rates:
            return
            
        try:
            # Get selected currencies
            from_currency = self.from_currency_var.get()
            to_currency = self.to_currency_var.get()
            
            # Get amount
            try:
                amount = float(self.from_amount_var.get())
            except ValueError:
                self.to_amount_var.set("Invalid input")
                self.rate_var.set("")
                return
            
            # Get exchange rates
            from_rate = self.exchange_rates.get(from_currency, 0)
            to_rate = self.exchange_rates.get(to_currency, 0)
            
            if from_rate and to_rate:
                # Calculate direct conversion rate
                rate = to_rate / from_rate
                
                # Calculate converted amount
                converted_amount = amount * rate
                
                # Update the result
                self.to_amount_var.set(f"{converted_amount:.4f}")
                self.rate_var.set(f"1 {from_currency} = {rate:.6f} {to_currency}")
                
                # Add to history
                self.history_manager.add_entry(
                    "Currency Converter",
                    f"{amount} {from_currency} to {to_currency}",
                    f"{converted_amount:.4f} {to_currency}"
                )
            else:
                self.to_amount_var.set("Rate not available")
                self.rate_var.set("")
                
        except Exception as e:
            self.to_amount_var.set(f"Error: {str(e)}")
            self.rate_var.set("")
    
    def swap_currencies(self):
        # Swap currencies
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()
        
        self.from_currency_var.set(to_currency)
        self.to_currency_var.set(from_currency)
        
        # Update conversion
        self.convert()
    
    def update_popular_currencies(self):
        # Clear existing widgets
        for widget in self.popular_scrollable_frame.winfo_children():
            widget.destroy()
        
        # List of popular currencies
        popular_currencies = [
            "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", 
            "HKD", "NZD", "SEK", "KRW", "SGD", "NOK", "MXN", 
            "INR", "RUB", "ZAR", "BRL", "TRY"
        ]
        
        # Create header
        header_frame = ttk.Frame(self.popular_scrollable_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(header_frame, text="Currency", width=10, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Code", width=8, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Label(header_frame, text="Rate (vs USD)", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Add separator
        ttk.Separator(self.popular_scrollable_frame, orient="horizontal").pack(fill=tk.X, padx=5, pady=2)
        
        # Add each currency
        for currency in popular_currencies:
            if currency in self.exchange_rates:
                rate = self.exchange_rates[currency]
                
                row = ttk.Frame(self.popular_scrollable_frame)
                row.pack(fill=tk.X, padx=5, pady=2)
                
                # Currency name (using code as fallback)
                currency_name = self.get_currency_name(currency)
                ttk.Label(row, text=currency_name, width=20).pack(side=tk.LEFT, padx=5)
                
                # Currency code
                ttk.Label(row, text=currency, width=8).pack(side=tk.LEFT, padx=5)
                
                # Exchange rate vs USD
                ttk.Label(row, text=f"{rate:.4f}").pack(side=tk.LEFT, padx=5)
                
                # Use in conversion button
                ttk.Button(
                    row,
                    text="Use",
                    width=5,
                    command=lambda curr=currency: self.use_currency(curr)
                ).pack(side=tk.RIGHT, padx=5)
    
    def use_currency(self, currency):
        # Set as the "to" currency
        self.to_currency_var.set(currency)
        
        # Update conversion
        self.convert()
    
    def get_currency_name(self, code):
        # Dictionary of currency codes to names
        currency_names = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "HKD": "Hong Kong Dollar",
            "NZD": "New Zealand Dollar",
            "SEK": "Swedish Krona",
            "KRW": "South Korean Won",
            "SGD": "Singapore Dollar",
            "NOK": "Norwegian Krone",
            "MXN": "Mexican Peso",
            "INR": "Indian Rupee",
            "RUB": "Russian Ruble",
            "ZAR": "South African Rand",
            "BRL": "Brazilian Real",
            "TRY": "Turkish Lira"
        }
        
        return currency_names.get(code, code)