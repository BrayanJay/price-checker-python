#!/usr/bin/env python3
"""
Demo version of the Pricing Engine GUI that works without API server
This version includes mock data and simulated API responses for demonstration
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from typing import Dict, Any
import threading
import time

class PricingEngineDemoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pricing Engine - FastAPI Integration (DEMO)")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Mock data storage
        self.mock_customers = [
            {"customer_id": 1, "name": "John Doe", "tier": "GOLD", "groups": ["REGULAR", "VIP"], "loyalty_products_count": 2},
            {"customer_id": 2, "name": "Jane Smith", "tier": "PLATINUM", "groups": ["BULK"], "loyalty_products_count": 1},
            {"customer_id": 3, "name": "Bob Johnson", "tier": "SILVER", "groups": ["REGULAR"], "loyalty_products_count": 0}
        ]
        
        self.mock_products = [
            {"product_id": 101, "name": "Premium Widget", "base_price": 99.99, "tier_prices_count": 3, "group_prices_count": 2},
            {"product_id": 102, "name": "Standard Widget", "base_price": 49.99, "tier_prices_count": 2, "group_prices_count": 1},
            {"product_id": 103, "name": "Basic Widget", "base_price": 19.99, "tier_prices_count": 1, "group_prices_count": 3}
        ]
        
        # Create main interface
        self.setup_ui()
        
        # Simulate API connection
        self.simulate_api_connection()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🚀 Pricing Engine - FastAPI Integration (DEMO MODE)", 
                              font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Status Frame
        status_frame = tk.Frame(self.root, bg="#f0f0f0")
        status_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="🔄 Simulating API connection...", 
                                    font=("Arial", 10), bg="#f0f0f0")
        self.status_label.pack(side=tk.LEFT)
        
        # Demo notice
        demo_notice = tk.Label(status_frame, text="⚠️ DEMO MODE - Using mock data", 
                              font=("Arial", 10, "italic"), fg="orange", bg="#f0f0f0")
        demo_notice.pack(side=tk.RIGHT)
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_overview_tab()
        self.create_customer_tab()
        self.create_product_tab()
        self.create_demo_calculator_tab()
    
    def create_overview_tab(self):
        """Create overview/demo tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Overview")
        
        # Welcome Section
        welcome_section = ttk.LabelFrame(overview_frame, text="Welcome to Pricing Engine GUI", padding=20)
        welcome_section.pack(fill=tk.X, padx=10, pady=10)
        
        welcome_text = """
🎯 This GUI demonstrates FastAPI integration with a desktop application.

Key Features Demonstrated:
✅ Customer Management with tiers and groups
✅ Product Management with dynamic pricing
✅ Real-time Price Calculations
✅ RESTful API Integration patterns
✅ Error handling and user feedback
✅ Multi-tab interface design

🚀 In production mode, this GUI connects to a live FastAPI server running on http://localhost:8000
📝 Demo mode uses mock data to showcase all features without requiring a server
        """
        
        tk.Label(welcome_section, text=welcome_text, font=("Arial", 11), justify=tk.LEFT).pack()
        
        # Quick Demo Section
        demo_section = ttk.LabelFrame(overview_frame, text="Quick Demo Actions", padding=15)
        demo_section.pack(fill=tk.X, padx=10, pady=10)
        
        demo_buttons_frame = tk.Frame(demo_section)
        demo_buttons_frame.pack()
        
        ttk.Button(demo_buttons_frame, text="🔄 Refresh Data", 
                  command=self.refresh_demo_data).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(demo_buttons_frame, text="📊 Show System Status", 
                  command=self.show_system_status).pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(demo_buttons_frame, text="💰 Demo Price Calculation", 
                  command=self.demo_price_calculation).pack(side=tk.LEFT, padx=10, pady=5)
        
        # API Integration Info
        api_section = ttk.LabelFrame(overview_frame, text="API Integration Details", padding=15)
        api_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        api_info = """
Real API Endpoints Integration:
▶ GET /customers - List all customers
▶ POST /customers - Create new customers  
▶ GET /products - List all products
▶ POST /products - Create new products
▶ POST /calculate-price - Calculate order prices
▶ POST /load-sample-data - Load test data
▶ GET /health - Health check monitoring

Technical Stack:
🐍 Python with Tkinter for GUI
🚀 FastAPI for REST API backend
📡 HTTP requests for API communication
🧵 Threading for non-blocking operations
📊 JSON for data serialization
        """
        
        tk.Label(api_section, text=api_info, font=("Courier", 10), justify=tk.LEFT).pack()
    
    def create_customer_tab(self):
        """Create customer management tab with demo data"""
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="👥 Customers")
        
        # Customer Form Section
        form_section = ttk.LabelFrame(customer_frame, text="Create Customer (Demo)", padding=10)
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
        
        # Buttons
        button_frame = tk.Frame(form_section)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Create Customer (Demo)", 
                  command=self.demo_create_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Demo Data", 
                  command=self.load_demo_customers).pack(side=tk.LEFT, padx=5)
        
        # Customer List Section
        list_section = ttk.LabelFrame(customer_frame, text="Customer List (Demo Data)", padding=10)
        list_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for customers
        columns = ("ID", "Name", "Tier", "Groups", "Loyalty Rules")
        self.customer_tree = ttk.Treeview(list_section, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=120)
        
        scrollbar_customers = ttk.Scrollbar(list_section, orient=tk.VERTICAL, command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=scrollbar_customers.set)
        
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_customers.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load demo data initially
        self.load_demo_customers()
    
    def create_product_tab(self):
        """Create product management tab with demo data"""
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="📦 Products")
        
        # Product Form Section
        form_section = ttk.LabelFrame(product_frame, text="Create Product (Demo)", padding=10)
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
        
        ttk.Button(button_frame, text="Create Product (Demo)", 
                  command=self.demo_create_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Demo Data", 
                  command=self.load_demo_products).pack(side=tk.LEFT, padx=5)
        
        # Product List Section
        list_section = ttk.LabelFrame(product_frame, text="Product List (Demo Data)", padding=10)
        list_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for products
        columns = ("ID", "Name", "Base Price", "Tier Rules", "Group Rules")
        self.product_tree = ttk.Treeview(list_section, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, width=120)
        
        scrollbar_products = ttk.Scrollbar(list_section, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar_products.set)
        
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_products.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load demo data initially
        self.load_demo_products()
    
    def create_demo_calculator_tab(self):
        """Create demo price calculator tab"""
        calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(calc_frame, text="💰 Calculator")
        
        # Calculator Section
        calc_section = ttk.LabelFrame(calc_frame, text="Demo Price Calculator", padding=15)
        calc_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Pre-filled demo values
        tk.Label(calc_section, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.demo_customer_var = tk.StringVar(value="1")
        customer_combo = ttk.Combobox(calc_section, textvariable=self.demo_customer_var, 
                                     values=["1 (John Doe - GOLD)", "2 (Jane Smith - PLATINUM)", "3 (Bob Johnson - SILVER)"], 
                                     width=25)
        customer_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(calc_section, text="Product ID:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.demo_product_var = tk.StringVar(value="101")
        product_combo = ttk.Combobox(calc_section, textvariable=self.demo_product_var, 
                                    values=["101 (Premium Widget - LKR 99.99)", "102 (Standard Widget - LKR 49.99)", "103 (Basic Widget - LKR 19.99)"], 
                                    width=30)
        product_combo.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(calc_section, text="Quantity:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.demo_qty_var = tk.StringVar(value="5")
        qty_spinbox = tk.Spinbox(calc_section, from_=1, to=100, textvariable=self.demo_qty_var, width=10)
        qty_spinbox.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(calc_section, text="🧮 Calculate Demo Price", 
                  command=self.calculate_demo_price).grid(row=1, column=2, columnspan=2, padx=10, pady=10)
        
        # Results Section
        results_section = ttk.LabelFrame(calc_frame, text="Calculation Results", padding=10)
        results_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.demo_results_text = scrolledtext.ScrolledText(results_section, height=20, width=80, font=("Courier", 10))
        self.demo_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial welcome message
        welcome_msg = """
🎯 Welcome to the Demo Price Calculator!

This calculator simulates the pricing engine logic with realistic data:

🏆 Customer Tiers:
   • SILVER: 5% discount (minimum 10 items)
   • GOLD: 10% discount (minimum 5 items)  
   • PLATINUM: 15% discount (minimum 3 items)

👥 Customer Groups:
   • REGULAR: Standard pricing
   • BULK: Additional 5% discount (minimum 20 items)
   • VIP: Additional 8% discount (minimum 2 items)

💎 Loyalty Pricing:
   • Personalized discounts for specific customer-product combinations
   • Overrides tier and group pricing when applicable

📊 Try different combinations to see how pricing works!
        """
        
        self.demo_results_text.insert(tk.END, welcome_msg)
    
    # Demo Methods
    def simulate_api_connection(self):
        """Simulate API connection check"""
        def simulate():
            time.sleep(2)
            self.status_label.config(text="✅ Demo Mode Connected - Using Mock Data", fg="green")
        
        threading.Thread(target=simulate, daemon=True).start()
    
    def refresh_demo_data(self):
        """Refresh demo data"""
        self.load_demo_customers()
        self.load_demo_products()
        messagebox.showinfo("Demo", "Demo data refreshed successfully!")
    
    def show_system_status(self):
        """Show mock system status"""
        status_info = {
            "status": "healthy",
            "mode": "demo",
            "customers": len(self.mock_customers),
            "products": len(self.mock_products),
            "api_endpoints": 18,
            "version": "1.0.0"
        }
        
        messagebox.showinfo("System Status", 
                           f"System Status: {status_info['status'].upper()}\n"
                           f"Mode: {status_info['mode'].upper()}\n"
                           f"Customers: {status_info['customers']}\n"
                           f"Products: {status_info['products']}\n"
                           f"API Endpoints: {status_info['api_endpoints']}\n"
                           f"Version: {status_info['version']}")
    
    def demo_price_calculation(self):
        """Run a quick demo price calculation"""
        self.demo_customer_var.set("1")
        self.demo_product_var.set("101")
        self.demo_qty_var.set("10")
        self.calculate_demo_price()
        self.notebook.select(3)  # Switch to calculator tab
    
    def demo_create_customer(self):
        """Demo customer creation"""
        if not self.customer_id_var.get() or not self.customer_name_var.get():
            messagebox.showwarning("Demo", "Please fill in Customer ID and Name for demo")
            return
        
        new_customer = {
            "customer_id": int(self.customer_id_var.get()),
            "name": self.customer_name_var.get(),
            "tier": self.customer_tier_var.get(),
            "groups": ["REGULAR"],  # Default for demo
            "loyalty_products_count": 0
        }
        
        self.mock_customers.append(new_customer)
        self.load_demo_customers()
        messagebox.showinfo("Demo", f"Customer '{new_customer['name']}' created successfully in demo!")
        
        # Clear form
        self.customer_id_var.set("")
        self.customer_name_var.set("")
    
    def demo_create_product(self):
        """Demo product creation"""
        if not self.product_id_var.get() or not self.product_name_var.get() or not self.product_price_var.get():
            messagebox.showwarning("Demo", "Please fill in all product fields for demo")
            return
        
        new_product = {
            "product_id": int(self.product_id_var.get()),
            "name": self.product_name_var.get(),
            "base_price": float(self.product_price_var.get()),
            "tier_prices_count": 0,
            "group_prices_count": 0
        }
        
        self.mock_products.append(new_product)
        self.load_demo_products()
        messagebox.showinfo("Demo", f"Product '{new_product['name']}' created successfully in demo!")
        
        # Clear form
        self.product_id_var.set("")
        self.product_name_var.set("")
        self.product_price_var.set("")
    
    def load_demo_customers(self):
        """Load demo customers into tree view"""
        # Clear existing items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # Add customers to tree
        for customer in self.mock_customers:
            self.customer_tree.insert("", tk.END, values=(
                customer["customer_id"],
                customer["name"],
                customer["tier"],
                ", ".join(customer["groups"]),
                customer["loyalty_products_count"]
            ))
    
    def load_demo_products(self):
        """Load demo products into tree view"""
        # Clear existing items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Add products to tree
        for product in self.mock_products:
            self.product_tree.insert("", tk.END, values=(
                product["product_id"],
                product["name"],
                f"LKR {product['base_price']:,.2f}",
                product["tier_prices_count"],
                product["group_prices_count"]
            ))
    
    def calculate_demo_price(self):
        """Calculate demo price with realistic logic"""
        try:
            # Extract customer ID from combo selection
            customer_id = int(self.demo_customer_var.get().split()[0])
            product_id = int(self.demo_product_var.get().split()[0])
            quantity = int(self.demo_qty_var.get())
            
            # Find customer and product
            customer = next((c for c in self.mock_customers if c["customer_id"] == customer_id), None)
            product = next((p for p in self.mock_products if p["product_id"] == product_id), None)
            
            if not customer or not product:
                messagebox.showerror("Demo Error", "Customer or Product not found")
                return
            
            # Calculate price with demo logic
            base_price = product["base_price"]
            total_base = base_price * quantity
            
            # Apply tier discount
            tier_discount = 0
            if customer["tier"] == "SILVER" and quantity >= 10:
                tier_discount = 0.05
            elif customer["tier"] == "GOLD" and quantity >= 5:
                tier_discount = 0.10
            elif customer["tier"] == "PLATINUM" and quantity >= 3:
                tier_discount = 0.15
            
            # Apply group discount
            group_discount = 0
            if "VIP" in customer["groups"] and quantity >= 2:
                group_discount = 0.08
            elif "BULK" in customer["groups"] and quantity >= 20:
                group_discount = 0.05
            
            # Calculate final price
            tier_savings = total_base * tier_discount
            group_savings = total_base * group_discount
            final_price = total_base - tier_savings - group_savings
            
            # Display results
            result_text = f"""
{'='*60}
💰 DEMO PRICE CALCULATION RESULT
{'='*60}

📋 Order Details:
   Customer: {customer['name']} (ID: {customer_id})
   Tier: {customer['tier']}
   Groups: {', '.join(customer['groups'])}
   
   Product: {product['name']} (ID: {product_id})
   Base Price: LKR {base_price:,.2f}
   Quantity: {quantity}

💵 Price Breakdown:
   Subtotal: LKR {total_base:,.2f}
   
   🏆 Tier Discount ({customer['tier']}): -{tier_discount*100:.1f}% = -LKR {tier_savings:,.2f}
   👥 Group Discount: -{group_discount*100:.1f}% = -LKR {group_savings:,.2f}
   
   💎 FINAL PRICE: LKR {final_price:,.2f}
   
   💡 Total Savings: LKR {tier_savings + group_savings:,.2f} ({((tier_savings + group_savings)/total_base)*100:.1f}%)

{'='*60}
📊 Pricing Rules Applied:
   • {customer['tier']} tier pricing: {'✅ Applied' if tier_discount > 0 else '❌ Not applicable (quantity too low)'}
   • Group pricing: {'✅ Applied' if group_discount > 0 else '❌ Not applicable'}
   • Loyalty pricing: ❌ Not configured in demo

🎯 This demonstrates the multi-level pricing engine logic!
{'='*60}

"""
            
            self.demo_results_text.insert(tk.END, result_text)
            self.demo_results_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Demo Error", f"Calculation error: {str(e)}")

def main():
    root = tk.Tk()
    app = PricingEngineDemoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()