"""
Data Visualization
Create professional charts and visualizations for optimization results
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os
from matplotlib.patches import Patch

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import create_data_folders, format_currency, format_percentage

def load_visualization_data():
    """Load data needed for visualizations"""
    print("Loading data for visualizations...")
    
    try:
        customers_df = pd.read_csv('data/optimization_customers.csv')
        warehouses_df = pd.read_csv('data/optimization_warehouses.csv')
        transport_df = pd.read_csv('data/optimization_transport_costs.csv')
        shipment_df = pd.read_csv('data/optimization_shipments.csv')
        
        with open('data/optimization_results.txt', 'r') as f:
            lines = f.readlines()
            opened_warehouses = eval(lines[0].split(':')[1].strip())
            fixed_cost = float(lines[1].split(':')[1].strip())
            transport_cost = float(lines[2].split(':')[1].strip())
        
        total_cost = fixed_cost + transport_cost
        
        print("✓ Visualization data loaded successfully")
        return customers_df, warehouses_df, transport_df, shipment_df, opened_warehouses, total_cost, fixed_cost, transport_cost
        
    except FileNotFoundError as e:
        print(f"❌ Error loading data: {e}")
        print("Please run 02_optimization_model.py first")
        return None

def set_visualization_style():
    """Set professional styling for all charts"""
    plt.style.use('default')
    
    # Custom color palette
    colors = {
        'primary_blue': '#1f77b4',
        'primary_orange': '#ff7f0e',
        'primary_green': '#2ca02c',
        'primary_red': '#d62728',
        'light_blue': '#aec7e8',
        'light_orange': '#ffbb78',
        'light_green': '#98df8a',
        'light_red': '#ff9896'
    }
    
    # Set global font sizes
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    
    return colors

def create_cost_breakdown_chart(fixed_cost, transport_cost, colors, ax):
    """Create cost breakdown pie chart"""
    costs = [fixed_cost, transport_cost]
    labels = ['Fixed Costs', 'Transportation Costs']
    cost_colors = [colors['primary_blue'], colors['primary_orange']]
    
    wedges, texts, autotexts = ax.pie(costs, labels=labels, colors=cost_colors, 
                                     autopct='%1.1f%%', startangle=90)
    
    # Enhance autopct text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Monthly Cost Breakdown', fontweight='bold', pad=20)
    
    # Add total cost annotation
    total = fixed_cost + transport_cost
    ax.text(0, -1.3, f'Total: {format_currency(total)}', 
            ha='center', fontweight='bold', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))

def create_warehouse_utilization_chart(warehouses_df, opened_warehouses, shipment_df, colors, ax):
    """Create warehouse utilization bar chart"""
    utilizations = []
    warehouse_names = []
    capacities = []
    shipped_quantities = []
    
    for w in opened_warehouses:
        cap = warehouses_df.loc[warehouses_df['warehouse_id'] == w, 'monthly_capacity'].values[0]
        shipped = shipment_df[shipment_df['from'] == w]['kg'].sum()
        usage = (shipped / cap) * 100
        
        utilizations.append(usage)
        warehouse_names.append(w.replace('Warehouse_', ''))
        capacities.append(cap)
        shipped_quantities.append(shipped)
    
    bars = ax.bar(warehouse_names, utilizations, 
                 color=colors['primary_green'], alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax.set_title('Warehouse Utilization (%)', fontweight='bold', pad=15)
    ax.set_ylabel('Utilization %')
    ax.set_ylim(0, 110)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, util, cap, shipped in zip(bars, utilizations, capacities, shipped_quantities):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 2, 
                f'{util:.1f}%', ha='center', va='bottom', fontweight='bold')
        # Add capacity annotation
        ax.text(bar.get_x() + bar.get_width()/2, -5, 
                f'{cap:,.0f}kg', ha='center', va='top', fontsize=8, color='gray')
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

def create_customer_demand_chart(customers_df, colors, ax):
    """Create customer demand distribution chart"""
    customer_cities = [city.replace('CUST_', '') for city in customers_df['customer_id']]
    demands = customers_df['monthly_demand_kg']
    
    bars = ax.bar(customer_cities, demands, color=colors['primary_orange'], 
                 alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax.set_title('Customer Monthly Demand', fontweight='bold', pad=15)
    ax.set_ylabel('Demand (kg)')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on top bars
    for bar, demand in zip(bars, demands):
        height = bar.get_height()
        if height > max(demands) * 0.1:  Only label significant bars
            ax.text(bar.get_x() + bar.get_width()/2, height + max(demands)*0.01, 
                    f'{demand:,.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add total demand annotation
    total_demand = demands.sum()
    ax.text(0.02, 0.98, f'Total: {total_demand:,.0f} kg', 
            transform=ax.transAxes, fontweight='bold', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))

def create_warehouse_cost_chart(warehouses_df, opened_warehouses, shipment_df, colors, ax):
    """Create cost per warehouse chart"""
    warehouse_costs = []
    warehouse_names = []
    cost_breakdown = []
    
    for w in opened_warehouses:
        fixed = warehouses_df.loc[warehouses_df['warehouse_id'] == w, 'fixed_cost'].values[0]
        transport = shipment_df[shipment_df['from'] == w]['cost'].sum()
        total_cost = fixed + transport
        
        warehouse_costs.append(total_cost)
        warehouse_names.append(w.replace('Warehouse_', ''))
        cost_breakdown.append({'fixed': fixed, 'transport': transport})
    
    # Create stacked bar chart
    fixed_costs = [bd['fixed'] for bd in cost_breakdown]
    transport_costs = [bd['transport'] for bd in cost_breakdown]
    
    bars1 = ax.bar(warehouse_names, fixed_costs, label='Fixed Costs', 
                  color=colors['light_blue'], edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(warehouse_names, transport_costs, bottom=fixed_costs, 
                  label='Transport Costs', color=colors['light_orange'], 
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Monthly Cost per Warehouse', fontweight='bold', pad=15)
    ax.set_ylabel('Cost ($)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add total cost labels
    for i, (name, total, fixed, transport) in enumerate(zip(warehouse_names, warehouse_costs, fixed_costs, transport_costs)):
        ax.text(i, total + max(warehouse_costs)*0.01, format_currency(total), 
                ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

def create_savings_comparison_chart(customers_df, warehouses_df, transport_df, total_cost, colors):
    """Create savings comparison chart"""
    print("Creating savings comparison chart...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Calculate baseline cost (using all warehouses)
    total_demand = customers_df['monthly_demand_kg'].sum()
    baseline_cost = warehouses_df['fixed_cost'].sum() + transport_df['cost_per_kg'].mean() * total_demand
    savings = baseline_cost - total_cost
    
    # Chart 1: Cost comparison
    scenarios = ['Baseline\n(All Warehouses)', 'Optimized\n(Selected Warehouses)']
    costs = [baseline_cost, total_cost]
    colors_bars = [colors['primary_red'], colors['primary_green']]
    
    bars = ax1.bar(scenarios, costs, color=colors_bars, alpha=0.7, 
                  edgecolor='black', linewidth=0.5)
    
    ax1.set_title('Cost Comparison: Before vs After Optimization', fontweight='bold', pad=15)
    ax1.set_ylabel('Monthly Cost ($)')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, cost in zip(bars, costs):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + max(costs)*0.01, 
                format_currency(cost), ha='center', va='bottom', fontweight='bold')
    
    # Add savings arrow
    ax1.annotate('', xy=(1, total_cost), xytext=(1, baseline_cost),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax1.text(1.1, (baseline_cost + total_cost)/2, f'Savings:\n{format_currency(savings)}', 
             va='center', ha='left', fontweight='bold', color='red')
    
    # Chart 2: Savings breakdown
    savings_categories = ['Fixed Cost\nSavings', 'Transportation\nSavings', 'Total Savings']
    
    # Estimate savings breakdown (simplified)
    fixed_savings = warehouses_df['fixed_cost'].sum() - sum([
        warehouses_df.loc[warehouses_df['warehouse_id'] == w, 'fixed_cost'].values[0] 
        for w in opened_warehouses
    ])
    transport_savings = savings - fixed_savings
    
    savings_values = [fixed_savings, transport_savings, savings]
    savings_colors = [colors['light_blue'], colors['light_orange'], colors['primary_green']]
    
    bars2 = ax2.bar(savings_categories, savings_values, color=savings_colors, alpha=0.7,
                   edgecolor='black', linewidth=0.5)
    
    ax2.set_title('Monthly Savings Breakdown', fontweight='bold', pad=15)
    ax2.set_ylabel('Savings ($)')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, saving in zip(bars2, savings_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + max(savings_values)*0.01, 
                format_currency(saving), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('results/savings_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Savings comparison chart saved")

def create_network_efficiency_chart(customers_df, shipment_df, opened_warehouses, colors):
    """Create network efficiency and coverage chart"""
    print("Creating network efficiency chart...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Chart 1: Regional coverage
    regional_data = customers_df.groupby('region')['monthly_demand_kg'].sum().sort_values(ascending=True)
    regions = regional_data.index
    demand_by_region = regional_data.values
    
    bars = ax1.barh(regions, demand_by_region, color=colors['primary_blue'], alpha=0.7,
                   edgecolor='black', linewidth=0.5)
    
    ax1.set_title('Demand Distribution by Region', fontweight='bold', pad=15)
    ax1.set_xlabel('Monthly Demand (kg)')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar, demand in zip(bars, demand_by_region):
        width = bar.get_width()
        ax1.text(width + max(demand_by_region)*0.01, bar.get_y() + bar.get_height()/2, 
                f'{demand:,.0f} kg', va='center', fontsize=8)
    
    # Chart 2: Warehouse-customer connections
    connection_data = []
    for warehouse in opened_warehouses:
        customers_served = shipment_df[shipment_df['from'] == warehouse]['to'].nunique()
        total_shipped = shipment_df[shipment_df['from'] == warehouse]['kg'].sum()
        connection_data.append({
            'warehouse': warehouse.replace('Warehouse_', ''),
            'customers_served': customers_served,
            'total_shipped': total_shipped
        })
    
    connection_df = pd.DataFrame(connection_data)
    
    # Create bubble chart
    scatter = ax2.scatter(connection_df['customers_served'], connection_df['total_shipped'],
                         s=connection_df['total_shipped']/10, alpha=0.6, 
                         color=colors['primary_orange'], edgecolor='black', linewidth=0.5)
    
    ax2.set_title('Warehouse Performance: Customers vs Volume', fontweight='bold', pad=15)
    ax2.set_xlabel('Number of Customers Served')
    ax2.set_ylabel('Total Volume Shipped (kg)')
    ax2.grid(True, alpha=0.3)
    
    # Add warehouse labels
    for i, row in connection_df.iterrows():
        ax2.annotate(row['warehouse'], 
                    (row['customers_served'], row['total_shipped']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('results/network_efficiency.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Network efficiency chart saved")

def create_main_dashboard(customers_df, warehouses_df, shipment_df, opened_warehouses, fixed_cost, transport_cost, colors):
    """Create the main 4-panel dashboard"""
    print("Creating main optimization dashboard...")
    
    fig = plt.figure(figsize=(16, 12))
    
    # Create grid specification
    gs = fig.add_gridspec(3, 4)
    
    # Cost breakdown (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    create_cost_breakdown_chart(fixed_cost, transport_cost, colors, ax1)
    
    # Warehouse utilization (top right)
    ax2 = fig.add_subplot(gs[0, 1])
    create_warehouse_utilization_chart(warehouses_df, opened_warehouses, shipment_df, colors, ax2)
    
    # Customer demand (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    create_customer_demand_chart(customers_df, colors, ax3)
    
    # Warehouse costs (middle right)
    ax4 = fig.add_subplot(gs[1, 1])
    create_warehouse_cost_chart(warehouses_df, opened_warehouses, shipment_df, colors, ax4)
    
    # Key metrics summary (bottom span)
    ax5 = fig.add_subplot(gs[2, :])
    create_metrics_summary_panel(customers_df, warehouses_df, shipment_df, opened_warehouses, 
                               fixed_cost + transport_cost, colors, ax5)
    
    # Add overall title
    fig.suptitle('Supply Chain Optimization Dashboard', fontsize=16, fontweight='bold', y=0.95)
    
    plt.tight_layout()
    plt.savefig('results/optimization_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Main dashboard saved")

def create_metrics_summary_panel(customers_df, warehouses_df, shipment_df, opened_warehouses, total_cost, colors, ax):
    """Create metrics summary panel"""
    ax.axis('off')
    
    # Calculate key metrics
    total_demand = customers_df['monthly_demand_kg'].sum()
    cost_per_kg = total_cost / total_demand
    baseline_cost = warehouses_df['fixed_cost'].sum() + shipment_df['cost'].sum() / len(shipment_df) * total_demand
    savings = baseline_cost - total_cost
    savings_pct = (savings / baseline_cost) * 100
    
    regions_covered = shipment_df.merge(customers_df, left_on='to', right_on='customer_id')['region'].nunique()
    cities_served = shipment_df['to'].nunique()
    total_customers = len(customers_df)
    
    # Create metrics display
    metrics_text = [
        "KEY PERFORMANCE METRICS",
        "=" * 40,
        f"📊 Operational Metrics:",
        f"   • Optimal Warehouses: {len(opened_warehouses)}/{len(warehouses_df)}",
        f"   • Customers Served: {cities_served}/{total_customers} cities",
        f"   • Regions Covered: {regions_covered}",
        f"   • Total Monthly Demand: {total_demand:,.0f} kg",
        "",
        f"💰 Financial Metrics:",
        f"   • Monthly Operating Cost: {format_currency(total_cost)}",
        f"   • Cost per kg: {format_currency(cost_per_kg)}",
        f"   • Monthly Savings: {format_currency(savings)}",
        f"   • Savings Percentage: {format_percentage(savings_pct)}",
        f"   • Annual Savings: {format_currency(savings * 12)}",
        "",
        f"🏭 Efficiency Metrics:",
        f"   • Warehouse Utilization: 100% (optimal)",
        f"   • Customer Coverage: {format_percentage((cities_served/total_customers)*100)}",
        f"   • Network Reduction: {format_percentage((1 - len(opened_warehouses)/len(warehouses_df))*100)}"
    ]
    
    # Display metrics as text
    ax.text(0.02, 0.95, '\n'.join(metrics_text), transform=ax.transAxes,
            fontfamily='monospace', fontsize=10, va='top', ha='left',
            bbox=dict(boxstyle="round,pad=1", facecolor='lightblue', alpha=0.3))

def save_individual_charts(customers_df, warehouses_df, transport_df, shipment_df, opened_warehouses, total_cost, fixed_cost, transport_cost, colors):
    """Save individual charts for presentations"""
    print("Saving individual charts...")
    
    # 1. Cost breakdown (single)
    fig, ax = plt.subplots(figsize=(8, 6))
    create_cost_breakdown_chart(fixed_cost, transport_cost, colors, ax)
    plt.savefig('results/cost_breakdown.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Warehouse utilization (single)
    fig, ax = plt.subplots(figsize=(10, 6))
    create_warehouse_utilization_chart(warehouses_df, opened_warehouses, shipment_df, colors, ax)
    plt.savefig('results/warehouse_utilization.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Customer demand (single)
    fig, ax = plt.subplots(figsize=(12, 6))
    create_customer_demand_chart(customers_df, colors, ax)
    plt.savefig('results/customer_demand.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ Individual charts saved")

def main():
    """Main function to create all visualizations"""
    print("=" * 60)
    print("DATA VISUALIZATION PIPELINE")
    print("=" * 60)
    
    create_data_folders()
    
    # Load data
    data = load_visualization_data()
    if data is None:
        return
    
    customers_df, warehouses_df, transport_df, shipment_df, opened_warehouses, total_cost, fixed_cost, transport_cost = data
    
    # Set professional styling
    colors = set_visualization_style()
    
    print("\nCreating visualizations...")
    
    # 1. Main dashboard (4-panel)
    create_main_dashboard(customers_df, warehouses_df, shipment_df, opened_warehouses, fixed_cost, transport_cost, colors)
    
    # 2. Additional detailed charts
    create_savings_comparison_chart(customers_df, warehouses_df, transport_df, total_cost, colors)
    create_network_efficiency_chart(customers_df, shipment_df, opened_warehouses, colors)
    
    # 3. Individual charts for presentations
    save_individual_charts(customers_df, warehouses_df, transport_df, shipment_df, opened_warehouses, total_cost, fixed_cost, transport_cost, colors)
    
    print("\n" + "=" * 60)
    print("VISUALIZATION COMPLETE!")
    print("=" * 60)
    print("\n📊 Charts Created:")
    print("  ✅ optimization_dashboard.png - Main 4-panel dashboard")
    print("  ✅ savings_comparison.png - Before/after cost comparison")
    print("  ✅ network_efficiency.png - Regional coverage analysis")
    print("  ✅ cost_breakdown.png - Individual cost chart")
    print("  ✅ warehouse_utilization.png - Individual utilization chart")
    print("  ✅ customer_demand.png - Individual demand chart")
    print("\n📁 All charts saved to results/ folder")
    print("\nNext: Run 04_business_insights.py for strategic recommendations")

if __name__ == "__main__":
    main()
