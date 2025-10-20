"""
Optimization Model
Mixed-Integer Linear Programming for supply chain optimization
"""

import pandas as pd
import pulp
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import create_data_folders, save_optimization_summary

def load_processed_data():
    """Load data from previous step"""
    print("Loading processed data...")
    
    try:
        customers_df = pd.read_csv('data/optimization_customers.csv')
        warehouses_df = pd.read_csv('data/optimization_warehouses.csv')
        transport_df = pd.read_csv('data/optimization_transport_costs.csv')
        
        print("✓ Data loaded successfully")
        return customers_df, warehouses_df, transport_df
        
    except FileNotFoundError as e:
        print(f"❌ Error loading data: {e}")
        print("Please run 01_data_transformation.py first")
        return None, None, None

def calculate_capacity_constraints(customers_df, warehouses_df):
    """Calculate realistic warehouse constraints"""
    print("\nAnalyzing capacity requirements...")
    
    total_demand = customers_df['monthly_demand_kg'].sum()
    total_capacity = warehouses_df['monthly_capacity'].sum()
    
    print(f"Total monthly demand: {total_demand:,.0f} kg")
    print(f"Total warehouse capacity: {total_capacity:,.0f} kg")
    print(f"Capacity utilization: {(total_demand/total_capacity)*100:.1f}%")
    
    # Find minimum warehouses needed
    warehouses_sorted = warehouses_df.sort_values('monthly_capacity', ascending=False)
    current_capacity = 0
    min_warehouses = 0
    
    print("\nFinding minimum warehouses needed:")
    for i, (_, warehouse) in enumerate(warehouses_sorted.iterrows(), 1):
        current_capacity += warehouse['monthly_capacity']
        print(f"  {i} warehouses: {current_capacity:,.0f} kg capacity")
        if current_capacity >= total_demand:
            min_warehouses = i
            break
    
    MIN_WAREHOUSES = min_warehouses
    MAX_WAREHOUSES = len(warehouses_df)
    
    print(f"\n✓ Warehouse constraints: {MIN_WAREHOUSES} to {MAX_WAREHOUSES} warehouses")
    return MIN_WAREHOUSES, MAX_WAREHOUSES

def build_optimization_model(customers_df, warehouses_df, transport_df, MIN_WAREHOUSES, MAX_WAREHOUSES):
    """Build the MILP optimization model"""
    print("\nBuilding optimization model...")
    
    # Initialize problem
    model = pulp.LpProblem("Supply_Chain_Network_Optimization", pulp.LpMinimize)

    # Decision variables
    open_warehouses = pulp.LpVariable.dicts("Open", warehouses_df['warehouse_id'], cat='Binary')
    shipment_vars = pulp.LpVariable.dicts("Ship", 
                                        [(w, c) for w in warehouses_df['warehouse_id'] 
                                         for c in customers_df['customer_id']],
                                        lowBound=0, cat='Continuous')

    # Objective function: Minimize Total Cost
    fixed_cost_total = pulp.lpSum([
        warehouses_df.loc[warehouses_df['warehouse_id'] == w, 'fixed_cost'].values[0] * open_warehouses[w]
        for w in warehouses_df['warehouse_id']
    ])

    transport_cost_total = pulp.lpSum([
        transport_df.loc[
            (transport_df['from_warehouse'] == w) & 
            (transport_df['to_customer_id'] == c), 
            'cost_per_kg'
        ].values[0] * shipment_vars[(w, c)]
        for w in warehouses_df['warehouse_id']
        for c in customers_df['customer_id']
    ])

    model += fixed_cost_total + transport_cost_total

    # Constraints
    print("Adding constraints...")
    
    # 1. Demand satisfaction
    for customer in customers_df['customer_id']:
        demand = customers_df.loc[customers_df['customer_id'] == customer, 'monthly_demand_kg'].values[0]
        model += pulp.lpSum([shipment_vars[(w, customer)] for w in warehouses_df['warehouse_id']]) == demand

    # 2. Capacity constraints
    for warehouse in warehouses_df['warehouse_id']:
        capacity = warehouses_df.loc[warehouses_df['warehouse_id'] == warehouse, 'monthly_capacity'].values[0]
        model += pulp.lpSum([shipment_vars[(warehouse, c)] for c in customers_df['customer_id']]) <= capacity * open_warehouses[warehouse]

    # 3. Strategic constraints
    model += pulp.lpSum([open_warehouses[w] for w in warehouses_df['warehouse_id']]) >= MIN_WAREHOUSES
    model += pulp.lpSum([open_warehouses[w] for w in warehouses_df['warehouse_id']]) <= MAX_WAREHOUSES

    # 4. Shipping logic
    for w in warehouses_df['warehouse_id']:
        for c in customers_df['customer_id']:
            capacity = warehouses_df.loc[warehouses_df['warehouse_id'] == w, 'monthly_capacity'].values[0]
            model += shipment_vars[(w, c)] <= open_warehouses[w] * capacity

    print("✓ Model built successfully")
    print(f"✓ Decision variables: {len(model.variables())}")
    print(f"✓ Constraints: {len(model.constraints)}")
    
    return model, open_warehouses, shipment_vars

def solve_and_analyze(model, open_vars, ship_vars, customers_df, warehouses_df, transport_df):
    """Solve the model and analyze results"""
    print("\nSolving optimization model...")
    
    # Solve the model
    model.solve()
    
    print(f"Solution status: {pulp.LpStatus[model.status]}")
    print(f"Total optimal cost: ${pulp.value(model.objective):,.2f}")

    if model.status != 1:
        print("❌ Model did not solve optimally")
        return None

    print("\n" + "=" * 50)
    print("OPTIMAL SOLUTION FOUND")
    print("=" * 50)

    # Analyze opened warehouses
    selected_warehouses = []
    total_fixed = 0

    print("\nSELECTED WAREHOUSES:")
    for warehouse in open_vars:
        if open_vars[warehouse].varValue > 0.5:
            fixed = warehouses_df.loc[warehouses_df['warehouse_id'] == warehouse, 'fixed_cost'].values[0]
            capacity = warehouses_df.loc[warehouses_df['warehouse_id'] == warehouse, 'monthly_capacity'].values[0]
            selected_warehouses.append(warehouse)
            total_fixed += fixed

            shipped = sum([ship_vars[(warehouse, c)].varValue for c in customers_df['customer_id']])
            usage = (shipped / capacity) * 100
            print(f"✅ {warehouse}: ${fixed:,.0f}/month, {capacity:,.0f} kg, {usage:.1f}% used")

    # Analyze transportation
    total_transport = 0
    shipments = []

    for (w, c), var in ship_vars.items():
        if var.varValue > 0.1 and w in selected_warehouses:
            cost_kg = transport_df.loc[
                (transport_df['from_warehouse'] == w) & 
                (transport_df['to_customer_id'] == c), 
                'cost_per_kg'
            ].values[0]
            transport = var.varValue * cost_kg
            total_transport += transport

            shipments.append({
                'from': w,
                'to': c,
                'kg': round(var.varValue, 2),
                'cost': round(transport, 2)
            })

    shipment_df = pd.DataFrame(shipments)

    # Print cost breakdown
    print(f"\nCOST BREAKDOWN:")
    print(f"Fixed costs: ${total_fixed:,.2f}")
    print(f"Transport costs: ${total_transport:,.2f}")
    print(f"Total monthly cost: ${pulp.value(model.objective):,.2f}")

    return shipment_df, selected_warehouses, total_fixed, total_transport

def main():
    """Main function to run optimization"""
    print("=" * 60)
    print("SUPPLY CHAIN OPTIMIZATION MODEL")
    print("=" * 60)
    
    create_data_folders()
    
    # Load data
    customers_df, warehouses_df, transport_df = load_processed_data()
    if customers_df is None:
        return None
    
    # Calculate constraints
    MIN_WAREHOUSES, MAX_WAREHOUSES = calculate_capacity_constraints(customers_df, warehouses_df)
    
    # Build model
    model, open_vars, ship_vars = build_optimization_model(
        customers_df, warehouses_df, transport_df, MIN_WAREHOUSES, MAX_WAREHOUSES
    )
    
    # Solve and analyze
    results = solve_and_analyze(model, open_vars, ship_vars, customers_df, warehouses_df, transport_df)
    
    if results:
        shipment_df, opened_warehouses, fixed_cost, transport_cost = results
        total_cost = fixed_cost + transport_cost
        
        # Save results for next steps
        shipment_df.to_csv('data/optimization_shipments.csv', index=False)
        
        with open('data/optimization_results.txt', 'w') as f:
            f.write(f"opened_warehouses: {opened_warehouses}\n")
            f.write(f"fixed_cost: {fixed_cost}\n")
            f.write(f"transport_cost: {transport_cost}\n")
        
        save_optimization_summary(results)
        
        print("\n" + "=" * 60)
        print("OPTIMIZATION COMPLETE!")
        print("=" * 60)
        print(f"✓ Selected {len(opened_warehouses)} warehouses")
        print(f"✓ Total cost: ${total_cost:,.2f}/month")
        print("\nNext: Run 03_visualization.py")
        
        return results
    else:
        print("❌ Optimization failed")
        return None

if __name__ == "__main__":
    results = main()
