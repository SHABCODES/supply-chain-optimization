"""
Data Transformation Pipeline
Convert raw shipment data into optimization-ready format
"""

import pandas as pd
import numpy as np
import sys
import os

# Add src to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import create_data_folders, validate_data

def load_and_clean_data(file_path='data/logistics_shipments_dataset.xlsx'):
    """Load the raw data and clean it"""
    print("Step 1: Loading and cleaning data...")
    
    try:
        df = pd.read_excel(file_path)
        print(f"✓ Loaded {len(df)} records from {file_path}")
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found")
        print("Please ensure the data file is in the data/ folder")
        return None
    
    # Clean data
    initial_count = len(df)
    df_clean = df.dropna(subset=['Delivery_Date', 'Cost'])
    removed_count = initial_count - len(df_clean)
    
    if removed_count > 0:
        print(f"✓ Removed {removed_count} records with missing values")
    
    print(f"✓ Cleaned dataset: {len(df_clean)} records")
    return df_clean

def create_customer_demand(shipments_df):
    """Calculate customer demand from shipment data"""
    print("Step 2: Calculating customer demand...")
    
    monthly_data = shipments_df.groupby(['Destination']).agg({
        'Weight_kg': 'sum',
        'Shipment_ID': 'count'
    }).reset_index()

    monthly_data['monthly_demand_kg'] = monthly_data['Weight_kg'] / 12
    monthly_data['customer_id'] = 'CUST_' + monthly_data['Destination'].str.replace(' ', '_').str.upper()
    
    def get_region(city):
        regions = {
            'San Francisco': 'West', 'Los Angeles': 'West', 'Seattle': 'West',
            'Chicago': 'Midwest', 'Detroit': 'Midwest', 'Minneapolis': 'Midwest',
            'New York': 'Northeast', 'Boston': 'Northeast', 'Philadelphia': 'Northeast',
            'Atlanta': 'Southeast', 'Miami': 'Southeast', 'Charlotte': 'Southeast',
            'Houston': 'South', 'Dallas': 'South', 'Phoenix': 'South'
        }
        return regions.get(city, 'Other')
    
    monthly_data['region'] = monthly_data['Destination'].apply(get_region)
    result_df = monthly_data[['customer_id', 'Destination', 'region', 'monthly_demand_kg']]
    result_df = result_df.rename(columns={'Destination': 'city'})
    
    print(f"✓ Created demand data for {len(result_df)} customers")
    return result_df

def create_warehouse_data(shipments_df):
    """Create warehouse capacity and cost data"""
    print("Step 3: Processing warehouse data...")
    
    warehouse_data = shipments_df.groupby('Origin_Warehouse').agg({
        'Weight_kg': 'sum',
        'Cost': 'mean',
        'Shipment_ID': 'count'
    }).reset_index()

    warehouse_data.columns = ['Origin_Warehouse', 'total_weight', 'avg_shipment_cost', 'shipment_count']
    warehouse_data['monthly_capacity'] = (warehouse_data['total_weight'] / 12 * 1.25).astype(int)
    
    base_cost = 30000
    warehouse_data['fixed_cost'] = (base_cost * 
                                  (warehouse_data['monthly_capacity'] / warehouse_data['monthly_capacity'].mean())).astype(int)

    final_df = warehouse_data[['Origin_Warehouse', 'monthly_capacity', 'fixed_cost']]
    final_df = final_df.rename(columns={'Origin_Warehouse': 'warehouse_id'})
    
    print(f"✓ Created data for {len(final_df)} warehouses")
    return final_df

def create_transportation_costs(shipments_df):
    """Create transportation cost matrix"""
    print("Step 4: Calculating transportation costs...")
    
    cost_data = shipments_df.groupby(['Origin_Warehouse', 'Destination']).agg({
        'Cost': 'mean',
        'Weight_kg': 'mean',
        'Distance_miles': 'mean'
    }).reset_index()

    cost_data['cost_per_kg'] = cost_data['Cost'] / cost_data['Weight_kg']
    
    all_combinations = [(w, c) for w in shipments_df['Origin_Warehouse'].unique() 
                       for c in shipments_df['Destination'].unique()]
    combinations_df = pd.DataFrame(all_combinations, columns=['Origin_Warehouse', 'Destination'])
    
    merged_data = combinations_df.merge(cost_data, on=['Origin_Warehouse', 'Destination'], how='left')
    
    # Fill missing costs with estimates
    avg_mile_cost = (merged_data['Cost'] / merged_data['Distance_miles']).mean()
    merged_data['estimated_cost'] = merged_data['Distance_miles'] * avg_mile_cost
    merged_data['estimated_cost_per_kg'] = merged_data['estimated_cost'] / merged_data['Weight_kg'].mean()
    merged_data['final_cost_per_kg'] = merged_data['cost_per_kg'].fillna(merged_data['estimated_cost_per_kg'])
    
    result_df = merged_data[['Origin_Warehouse', 'Destination', 'final_cost_per_kg', 'Distance_miles']]
    result_df = result_df.rename(columns={
        'Origin_Warehouse': 'from_warehouse',
        'Destination': 'to_customer',
        'final_cost_per_kg': 'cost_per_kg'
    })
    result_df['to_customer_id'] = 'CUST_' + result_df['to_customer'].str.replace(' ', '_').str.upper()
    
    final_df = result_df[['from_warehouse', 'to_customer_id', 'cost_per_kg', 'Distance_miles']]
    
    print(f"✓ Created {len(final_df)} transportation routes")
    return final_df

def save_processed_data(customers_df, warehouses_df, transport_df):
    """Save processed data to files"""
    print("Step 5: Saving processed data...")
    
    create_data_folders()
    
    customers_df.to_csv('data/optimization_customers.csv', index=False)
    warehouses_df.to_csv('data/optimization_warehouses.csv', index=False)
    transport_df.to_csv('data/optimization_transport_costs.csv', index=False)
    
    print("✓ Saved files to data/ folder:")
    print("  - optimization_customers.csv")
    print("  - optimization_warehouses.csv") 
    print("  - optimization_transport_costs.csv")

def main():
    """Main function to run data transformation"""
    print("=" * 60)
    print("DATA TRANSFORMATION PIPELINE")
    print("=" * 60)
    
    # Create folders
    create_data_folders()
    
    # Load and clean data
    df = load_and_clean_data()
    if df is None:
        return None
    
    # Transform data
    customers_df = create_customer_demand(df)
    warehouses_df = create_warehouse_data(df)
    transport_df = create_transportation_costs(df)
    
    # Validate data
    validate_data(customers_df, warehouses_df, transport_df)
    
    # Save data
    save_processed_data(customers_df, warehouses_df, transport_df)
    
    print("\n" + "=" * 60)
    print("DATA TRANSFORMATION COMPLETE!")
    print("=" * 60)
    print(f"✓ {len(customers_df)} customers")
    print(f"✓ {len(warehouses_df)} warehouses") 
    print(f"✓ {len(transport_df)} transportation routes")
    print("\nNext: Run 02_optimization_model.py")
    
    return customers_df, warehouses_df, transport_df

if __name__ == "__main__":
    customers_df, warehouses_df, transport_df = main()
