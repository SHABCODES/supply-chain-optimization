"""
Utility functions for supply chain optimization
"""

import pandas as pd
import numpy as np
import os

def create_data_folders():
    """Create necessary folders if they don't exist"""
    folders = ['data', 'results', 'logs']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created {folder}/ directory")

def validate_data(customers_df, warehouses_df, transport_df):
    """Validate data before optimization"""
    print("Validating data...")
    
    # Check for missing values
    if customers_df.isnull().any().any():
        print("Warning: Missing values in customers data")
    
    if warehouses_df.isnull().any().any():
        print("Warning: Missing values in warehouses data")
    
    if transport_df.isnull().any().any():
        print("Warning: Missing values in transport data")
    
    # Check data types
    required_columns = {
        'customers': ['customer_id', 'city', 'region', 'monthly_demand_kg'],
        'warehouses': ['warehouse_id', 'monthly_capacity', 'fixed_cost'],
        'transport': ['from_warehouse', 'to_customer_id', 'cost_per_kg']
    }
    
    # Validate columns exist
    for df_name, columns in required_columns.items():
        if df_name == 'customers':
            df = customers_df
        elif df_name == 'warehouses':
            df = warehouses_df
        else:
            df = transport_df
            
        missing_cols = [col for col in columns if col not in df.columns]
        if missing_cols:
            print(f"Missing columns in {df_name}: {missing_cols}")
    
    print("Data validation complete")

def calculate_business_metrics(customers_df, warehouses_df, transport_df, total_cost):
    """Calculate key business metrics"""
    total_demand = customers_df['monthly_demand_kg'].sum()
    cost_per_kg = total_cost / total_demand
    
    # Calculate baseline (all warehouses)
    baseline_cost = warehouses_df['fixed_cost'].sum() + transport_df['cost_per_kg'].mean() * total_demand
    savings = baseline_cost - total_cost
    savings_pct = (savings / baseline_cost) * 100
    
    metrics = {
        'total_demand_kg': total_demand,
        'total_cost': total_cost,
        'cost_per_kg': cost_per_kg,
        'baseline_cost': baseline_cost,
        'savings_amount': savings,
        'savings_percentage': savings_pct,
        'annual_savings': savings * 12
    }
    
    return metrics

def save_optimization_summary(results, filename='results/optimization_summary.txt'):
    """Save optimization results to a text file"""
    shipment_df, opened_warehouses, fixed_cost, transport_cost = results
    total_cost = fixed_cost + transport_cost
    
    summary = f"""
SUPPLY CHAIN OPTIMIZATION SUMMARY
=================================

OPTIMAL WAREHOUSE NETWORK
-------------------------
Selected Warehouses: {len(opened_warehouses)}
Warehouse List: {', '.join(opened_warehouses)}

COST BREAKDOWN
--------------
Fixed Costs: ${fixed_cost:,.2f}
Transportation Costs: ${transport_cost:,.2f}
Total Monthly Cost: ${total_cost:,.2f}

WAREHOUSE UTILIZATION
---------------------
"""
    
    # Add warehouse details
    for warehouse in opened_warehouses:
        shipped = shipment_df[shipment_df['from'] == warehouse]['kg'].sum()
        summary += f"- {warehouse}: {shipped:,.0f} kg shipped\n"
    
    with open(filename, 'w') as f:
        f.write(summary)
    
    print(f"Summary saved to {filename}")

def format_currency(amount):
    """Format numbers as currency"""
    return f"${amount:,.2f}"

def format_percentage(value):
    """Format numbers as percentage"""
    return f"{value:.1f}%"
