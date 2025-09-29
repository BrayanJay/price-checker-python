"""
GUI Application for Pricing Engine FastAPI Integration
A Tkinter-based interface to interact with the pricing engine REST API
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from typing import Dict, Any
import threading

class PricingEngineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pricing Engine - FastAPI Integration")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # API Configuration
        self.api_base_url = "http://localhost:8000"
        
        # Create main interface
        self.setup_ui()
        
        # Check API connection on startup
        self.check_api_connection()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🚀 Pricing Engine - FastAPI Integration", 
                              font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#f0f0f0")
        status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="🔄 Checking API connection...", 
                                    font=("Arial", 10), bg="#f0f0f0")
        self.status_label.pack(side=tk.LEFT)
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_system_tab()
        self.create_customer_tab()
        self.create_product_tab()
        self.create_pricing_tab()
        self.create_calculation_tab()
        self.create_api_explorer_tab()
    
    def create_system_tab(self):
        """Create system management tab"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="System")
        
        # API Status Section
        status_section = ttk.LabelFrame(system_frame, text="API Status", padding=10)
        status_section.pack(fill=tk.X, padx=10, pady=5)
        
        status_buttons_frame = tk.Frame(status_section)
        status_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(status_buttons_frame, text="Check Health", 
                  command=self.check_health).pack(side=tk.LEFT, padx=5)
        ttk.Button(status_buttons_frame, text="Get Status", 
                  command=self.get_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(status_buttons_frame, text="Refresh Connection", 
                  command=self.check_api_connection).pack(side=tk.LEFT, padx=5)
        
        # Data Management Section
        data_section = ttk.LabelFrame(system_frame, text="Data Management", padding=10)
        data_section.pack(fill=tk.X, padx=10, pady=5)
        
        data_buttons_frame = tk.Frame(data_section)
        data_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(data_buttons_frame, text="Load Sample Data", 
                  command=self.load_sample_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(data_buttons_frame, text="Clear All Data", 
                  command=self.clear_data).pack(side=tk.LEFT, padx=5)
        
        # System Information Display
        info_section = ttk.LabelFrame(system_frame, text="System Information", padding=10)
        info_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.system_info_text = scrolledtext.ScrolledText(info_section, height=15, width=70)
        self.system_info_text.pack(fill=tk.BOTH, expand=True)
    
    def create_customer_tab(self):
        """Create customer management tab"""
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="Customers")
        
        # Customer Form Section
        form_section = ttk.LabelFrame(customer_frame, text="Create Customer", padding=10)
        form_section.pack(fill=tk.X, padx=10, pady=5)
        
        # Customer ID
        tk.Label(form_section, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_id_var = tk.StringVar()
        tk.Entry(form_section, textvariable=self.customer_id_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        # Customer Name
        tk.Label(form_section, text="Name:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.customer_name_var = tk.StringVar()
        tk.Entry(form_section, textvariable=self.customer_name_var, width=30).grid(row=0, column=3, padx=5, pady=2)
        
        # Tier
        tk.Label(form_section, text="Tier:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.customer_tier_var = tk.StringVar(value="GOLD")
        tier_combo = ttk.Combobox(form_section, textvariable=self.customer_tier_var, 
                                 values=["SILVER", "GOLD", "PLATINUM"], state="readonly", width=17)
        tier_combo.grid(row=1, column=1, padx=5, pady=2)
        
        # Groups
        tk.Label(form_section, text="Groups:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        groups_frame = tk.Frame(form_section)
        groups_frame.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        
        self.group_regular_var = tk.BooleanVar()
        self.group_bulk_var = tk.BooleanVar()
        self.group_vip_var = tk.BooleanVar()
        
        tk.Checkbutton(groups_frame, text="REGULAR", variable=self.group_regular_var).pack(side=tk.LEFT)
        tk.Checkbutton(groups_frame, text="BULK", variable=self.group_bulk_var).pack(side=tk.LEFT)
        tk.Checkbutton(groups_frame, text="VIP", variable=self.group_vip_var).pack(side=tk.LEFT)
        
        # Buttons
        button_frame = tk.Frame(form_section)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Create Customer", 
                  command=self.create_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Customers", 
                  command=self.load_customers).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", 
                  command=self.clear_customer_form).pack(side=tk.LEFT, padx=5)
        
        # Customer List Section
        list_section = ttk.LabelFrame(customer_frame, text="Customer List", padding=10)
        list_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for customers
        columns = ("ID", "Name", "Tier", "Groups", "Loyalty Rules")
        self.customer_tree = ttk.Treeview(list_section, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=120)
        
        scrollbar_customers = ttk.Scrollbar(list_section, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar_customers.set)
        
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_customers.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_product_tab(self):
        """Create product management tab"""
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="Products")
        
        # Product Form Section
        form_section = ttk.LabelFrame(product_frame, text="Create Product", padding=10)
        form_section.pack(fill=tk.X, padx=10, pady=5)
        
        # Product fields
        tk.Label(form_section, text="Product ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.product_id_var = tk.StringVar()
        tk.Entry(form_section, textvariable=self.product_id_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(form_section, text="Product Name:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.product_name_var = tk.StringVar()
        tk.Entry(form_section, textvariable=self.product_name_var, width=30).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(form_section, text="Base Price:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.product_price_var = tk.StringVar()
        tk.Entry(form_section, textvariable=self.product_price_var, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        # Buttons
        button_frame = tk.Frame(form_section)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Create Product", 
                  command=self.create_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Products", 
                  command=self.load_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", 
                  command=self.clear_product_form).pack(side=tk.LEFT, padx=5)
        
        # Product List Section
        list_section = ttk.LabelFrame(product_frame, text="Product List", padding=10)
        list_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for products
        columns = ("ID", "Name", "Base Price", "Tier Rules", "Group Rules")
        self.product_tree = ttk.Treeview(list_section, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=120)
        
        scrollbar_products = ttk.Scrollbar(list_section, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar_products.set)
        
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_products.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_pricing_tab(self):
        """Create pricing rules management tab"""
        pricing_frame = ttk.Frame(self.notebook)
        self.notebook.add(pricing_frame, text="Pricing Rules")
        
        # Tier Pricing Section
        tier_section = ttk.LabelFrame(pricing_frame, text="Add Tier Pricing Rule", padding=10)
        tier_section.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(tier_section, text="Product ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.tier_product_id_var = tk.StringVar()
        tk.Entry(tier_section, textvariable=self.tier_product_id_var, width=15).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(tier_section, text="Tier:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.tier_type_var = tk.StringVar(value="GOLD")
        ttk.Combobox(tier_section, textvariable=self.tier_type_var, 
                    values=["SILVER", "GOLD", "PLATINUM"], state="readonly", width=12).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(tier_section, text="Discount Rate:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.tier_discount_var = tk.StringVar()
        tk.Entry(tier_section, textvariable=self.tier_discount_var, width=15).grid(row=0, column=5, padx=5, pady=2)
        
        tk.Label(tier_section, text="Min Qty:").grid(row=0, column=6, sticky=tk.W, padx=5, pady=2)
        self.tier_min_qty_var = tk.StringVar()
        tk.Entry(tier_section, textvariable=self.tier_min_qty_var, width=10).grid(row=0, column=7, padx=5, pady=2)
        
        ttk.Button(tier_section, text="Add Tier Rule", 
                  command=self.add_tier_pricing).grid(row=1, column=0, columnspan=8, pady=10)
        
        # Group Pricing Section
        group_section = ttk.LabelFrame(pricing_frame, text="Add Group Pricing Rule", padding=10)
        group_section.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(group_section, text="Product ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.group_product_id_var = tk.StringVar()
        tk.Entry(group_section, textvariable=self.group_product_id_var, width=15).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(group_section, text="Group:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.group_type_var = tk.StringVar(value="VIP")
        ttk.Combobox(group_section, textvariable=self.group_type_var, 
                    values=["REGULAR", "BULK", "VIP"], state="readonly", width=12).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(group_section, text="Discount Rate:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.group_discount_var = tk.StringVar()
        tk.Entry(group_section, textvariable=self.group_discount_var, width=15).grid(row=0, column=5, padx=5, pady=2)
        
        tk.Label(group_section, text="Min Qty:").grid(row=0, column=6, sticky=tk.W, padx=5, pady=2)
        self.group_min_qty_var = tk.StringVar()
        tk.Entry(group_section, textvariable=self.group_min_qty_var, width=10).grid(row=0, column=7, padx=5, pady=2)
        
        ttk.Button(group_section, text="Add Group Rule", 
                  command=self.add_group_pricing).grid(row=1, column=0, columnspan=8, pady=10)
        
        # Loyalty Pricing Section
        loyalty_section = ttk.LabelFrame(pricing_frame, text="Add Loyalty Pricing Rule", padding=10)
        loyalty_section.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(loyalty_section, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.loyalty_customer_id_var = tk.StringVar()
        tk.Entry(loyalty_section, textvariable=self.loyalty_customer_id_var, width=15).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(loyalty_section, text="Product ID:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.loyalty_product_id_var = tk.StringVar()
        tk.Entry(loyalty_section, textvariable=self.loyalty_product_id_var, width=15).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(loyalty_section, text="Discount Rate:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.loyalty_discount_var = tk.StringVar()
        tk.Entry(loyalty_section, textvariable=self.loyalty_discount_var, width=15).grid(row=0, column=5, padx=5, pady=2)
        
        tk.Label(loyalty_section, text="Min Qty:").grid(row=0, column=6, sticky=tk.W, padx=5, pady=2)
        self.loyalty_min_qty_var = tk.StringVar()
        tk.Entry(loyalty_section, textvariable=self.loyalty_min_qty_var, width=10).grid(row=0, column=7, padx=5, pady=2)
        
        ttk.Button(loyalty_section, text="Add Loyalty Rule", 
                  command=self.add_loyalty_pricing).grid(row=1, column=0, columnspan=8, pady=10)
    
    def create_calculation_tab(self):
        """Create price calculation tab"""
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="Price Calculator")
        
        # Single Order Section
        single_section = ttk.LabelFrame(calc_frame, text="Single Price Calculation", padding=10)
        single_section.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(single_section, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.calc_customer_id_var = tk.StringVar()
        tk.Entry(single_section, textvariable=self.calc_customer_id_var, width=15).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(single_section, text="Product ID:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.calc_product_id_var = tk.StringVar()
        tk.Entry(single_section, textvariable=self.calc_product_id_var, width=15).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(single_section, text="Quantity:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.calc_quantity_var = tk.StringVar()
        tk.Entry(single_section, textvariable=self.calc_quantity_var, width=15).grid(row=0, column=5, padx=5, pady=2)
        
        ttk.Button(single_section, text="Calculate Price", 
                  command=self.calculate_single_price).grid(row=1, column=0, columnspan=6, pady=10)
        
        # Results Section
        results_section = ttk.LabelFrame(calc_frame, text="Calculation Results", padding=10)
        results_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_section, height=20, width=80)
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def create_api_explorer_tab(self):
        """Create API explorer tab"""
        explorer_frame = ttk.Frame(self.notebook)
        self.notebook.add(explorer_frame, text="API Explorer")
        
        # Request Section
        request_section = ttk.LabelFrame(explorer_frame, text="API Request", padding=10)
        request_section.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(request_section, text="Method:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.api_method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(request_section, textvariable=self.api_method_var, 
                                   values=["GET", "POST", "DELETE"], state="readonly", width=10)
        method_combo.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(request_section, text="Endpoint:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.api_endpoint_var = tk.StringVar(value="/status")
        endpoint_combo = ttk.Combobox(request_section, textvariable=self.api_endpoint_var, 
                                     values=["/", "/health", "/status", "/customers", "/products", 
                                            "/load-sample-data", "/clear-data"], width=30)
        endpoint_combo.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Button(request_section, text="Send Request", 
                  command=self.send_api_request).grid(row=0, column=4, padx=10)
        
        # JSON Payload Section
        payload_section = ttk.LabelFrame(explorer_frame, text="JSON Payload (for POST requests)", padding=10)
        payload_section.pack(fill=tk.X, padx=10, pady=5)
        
        self.payload_text = scrolledtext.ScrolledText(payload_section, height=8, width=80)
        self.payload_text.pack(fill=tk.BOTH, expand=True)
        self.payload_text.insert(tk.END, '{\n  "example": "payload"\n}')
        
        # Response Section
        response_section = ttk.LabelFrame(explorer_frame, text="API Response", padding=10)
        response_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.response_text = scrolledtext.ScrolledText(response_section, height=15, width=80)
        self.response_text.pack(fill=tk.BOTH, expand=True)
    
    # API Connection Methods
    def check_api_connection(self):
        """Check if API is accessible"""
        def check():
            try:
                response = requests.get(f"{self.api_base_url}/health", timeout=5)
                if response.status_code == 200:
                    self.status_label.config(text="✅ API Connected - Ready", fg="green")
                else:
                    self.status_label.config(text="⚠️ API Error - Check server", fg="orange")
            except Exception as e:
                self.status_label.config(text="❌ API Disconnected - Start server", fg="red")
        
        threading.Thread(target=check, daemon=True).start()
    
    def check_health(self):
        """Check API health"""
        try:
            response = requests.get(f"{self.api_base_url}/health")
            result = f"Health Check Result:\nStatus: {response.status_code}\nResponse: {json.dumps(response.json(), indent=2)}\n\n"
            self.system_info_text.insert(tk.END, result)
            self.system_info_text.see(tk.END)
        except Exception as e:
            messagebox.showerror("API Error", str(e))
    
    def get_status(self):
        """Get system status"""
        try:
            response = requests.get(f"{self.api_base_url}/status")
            result = f"System Status:\nStatus: {response.status_code}\nResponse: {json.dumps(response.json(), indent=2)}\n\n"
            self.system_info_text.insert(tk.END, result)
            self.system_info_text.see(tk.END)
        except Exception as e:
            messagebox.showerror("API Error", str(e))
    
    def load_sample_data(self):
        """Load sample data via API"""
        try:
            response = requests.post(f"{self.api_base_url}/load-sample-data")
            if response.status_code == 200:
                messagebox.showinfo("Success", "Sample data loaded successfully!")
                self.load_customers()
                self.load_products()
            else:
                messagebox.showerror("Error", f"Failed to load sample data: {response.text}")
        except Exception as e:
            messagebox.showerror("API Error", str(e))
    
    def clear_data(self):
        """Clear all data via API"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            try:
                response = requests.delete(f"{self.api_base_url}/clear-data")
                if response.status_code == 200:
                    messagebox.showinfo("Success", "All data cleared successfully!")
                    self.load_customers()
                    self.load_products()
                else:
                    messagebox.showerror("Error", f"Failed to clear data: {response.text}")
            except Exception as e:
                messagebox.showerror("API Error", str(e))
    
    # Customer Management Methods
    def create_customer(self):
        """Create new customer via API"""
        try:
            groups = []
            if self.group_regular_var.get(): groups.append("REGULAR")
            if self.group_bulk_var.get(): groups.append("BULK")
            if self.group_vip_var.get(): groups.append("VIP")
            
            customer_data = {
                "customer_id": int(self.customer_id_var.get()),
                "name": self.customer_name_var.get(),
                "tier": self.customer_tier_var.get(),
                "groups": groups
            }
            
            response = requests.post(f"{self.api_base_url}/customers", json=customer_data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Customer created successfully!")
                self.clear_customer_form()
                self.load_customers()
            else:
                messagebox.showerror("Error", f"Failed to create customer: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_customers(self):
        """Load customers from API"""
        try:
            response = requests.get(f"{self.api_base_url}/customers")
            if response.status_code == 200:
                customers = response.json()
                
                # Clear existing items
                for item in self.customer_tree.get_children():
                    self.customer_tree.delete(item)
                
                # Add customers to tree
                for customer in customers:
                    self.customer_tree.insert("", tk.END, values=(
                        customer["customer_id"],
                        customer["name"],
                        customer["tier"],
                        ", ".join(customer["groups"]),
                        customer["loyalty_products_count"]
                    ))
        except Exception as e:
            messagebox.showerror("API Error", str(e))
    
    def clear_customer_form(self):
        """Clear customer form"""
        self.customer_id_var.set("")
        self.customer_name_var.set("")
        self.customer_tier_var.set("GOLD")
        self.group_regular_var.set(False)
        self.group_bulk_var.set(False)
        self.group_vip_var.set(False)
    
    # Product Management Methods
    def create_product(self):
        """Create new product via API"""
        try:
            product_data = {
                "product_id": int(self.product_id_var.get()),
                "name": self.product_name_var.get(),
                "base_price": float(self.product_price_var.get())
            }
            
            response = requests.post(f"{self.api_base_url}/products", json=product_data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Product created successfully!")
                self.clear_product_form()
                self.load_products()
            else:
                messagebox.showerror("Error", f"Failed to create product: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_products(self):
        """Load products from API"""
        try:
            response = requests.get(f"{self.api_base_url}/products")
            if response.status_code == 200:
                products = response.json()
                
                # Clear existing items
                for item in self.product_tree.get_children():
                    self.product_tree.delete(item)
                
                # Add products to tree
                for product in products:
                    self.product_tree.insert("", tk.END, values=(
                        product["product_id"],
                        product["name"],
                        f"LKR {product['base_price']:,.2f}",
                        product["tier_prices_count"],
                        product["group_prices_count"]
                    ))
        except Exception as e:
            messagebox.showerror("API Error", str(e))
    
    def clear_product_form(self):
        """Clear product form"""
        self.product_id_var.set("")
        self.product_name_var.set("")
        self.product_price_var.set("")
    
    # Pricing Rules Methods
    def add_tier_pricing(self):
        """Add tier pricing rule via API"""
        try:
            rule_data = {
                "product_id": int(self.tier_product_id_var.get()),
                "tier": self.tier_type_var.get(),
                "discount_rate": float(self.tier_discount_var.get()),
                "min_qty": int(self.tier_min_qty_var.get())
            }
            
            product_id = rule_data["product_id"]
            response = requests.post(f"{self.api_base_url}/products/{product_id}/tier-prices", json=rule_data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Tier pricing rule added successfully!")
                # Clear form
                self.tier_product_id_var.set("")
                self.tier_discount_var.set("")
                self.tier_min_qty_var.set("")
            else:
                messagebox.showerror("Error", f"Failed to add tier pricing: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_group_pricing(self):
        """Add group pricing rule via API"""
        try:
            rule_data = {
                "product_id": int(self.group_product_id_var.get()),
                "group": self.group_type_var.get(),
                "discount_rate": float(self.group_discount_var.get()),
                "min_qty": int(self.group_min_qty_var.get())
            }
            
            product_id = rule_data["product_id"]
            response = requests.post(f"{self.api_base_url}/products/{product_id}/group-prices", json=rule_data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Group pricing rule added successfully!")
                # Clear form
                self.group_product_id_var.set("")
                self.group_discount_var.set("")
                self.group_min_qty_var.set("")
            else:
                messagebox.showerror("Error", f"Failed to add group pricing: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def add_loyalty_pricing(self):
        """Add loyalty pricing rule via API"""
        try:
            rule_data = {
                "customer_id": int(self.loyalty_customer_id_var.get()),
                "product_id": int(self.loyalty_product_id_var.get()),
                "discount_rate": float(self.loyalty_discount_var.get()),
                "min_qty": int(self.loyalty_min_qty_var.get())
            }
            
            customer_id = rule_data["customer_id"]
            response = requests.post(f"{self.api_base_url}/customers/{customer_id}/loyalty-prices", json=rule_data)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Loyalty pricing rule added successfully!")
                # Clear form
                self.loyalty_customer_id_var.set("")
                self.loyalty_product_id_var.set("")
                self.loyalty_discount_var.set("")
                self.loyalty_min_qty_var.set("")
            else:
                messagebox.showerror("Error", f"Failed to add loyalty pricing: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Price Calculation Methods
    def calculate_single_price(self):
        """Calculate single order price via API"""
        try:
            order_data = {
                "customer_id": int(self.calc_customer_id_var.get()),
                "product_id": int(self.calc_product_id_var.get()),
                "quantity": int(self.calc_quantity_var.get())
            }
            
            response = requests.post(f"{self.api_base_url}/calculate-price", json=order_data)
            if response.status_code == 200:
                result = response.json()
                result_text = f"""
Price Calculation Result:
========================
Customer ID: {order_data['customer_id']}
Product ID: {order_data['product_id']}
Quantity: {order_data['quantity']}

Result:
- Product: {result['product_id']}
- Final Price: LKR {result['price']:,.2f}
- Price Type: {result['price_type']}

{'-'*50}
"""
                self.results_text.insert(tk.END, result_text)
                self.results_text.see(tk.END)
            else:
                messagebox.showerror("Error", f"Failed to calculate price: {response.json()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # API Explorer Methods
    def send_api_request(self):
        """Send custom API request"""
        try:
            method = self.api_method_var.get()
            endpoint = self.api_endpoint_var.get()
            url = f"{self.api_base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                payload = self.payload_text.get(1.0, tk.END).strip()
                if payload:
                    json_data = json.loads(payload)
                    response = requests.post(url, json=json_data)
                else:
                    response = requests.post(url)
            elif method == "DELETE":
                response = requests.delete(url)
            
            # Display response
            response_text = f"""
Request: {method} {url}
Status Code: {response.status_code}
Response:
{json.dumps(response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text, indent=2)}

{'-'*80}
"""
            self.response_text.insert(tk.END, response_text)
            self.response_text.see(tk.END)
            
        except Exception as e:
            error_text = f"Error: {str(e)}\n{'-'*80}\n"
            self.response_text.insert(tk.END, error_text)
            self.response_text.see(tk.END)

def main():
    root = tk.Tk()
    app = PricingEngineGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()