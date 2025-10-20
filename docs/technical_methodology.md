markdown
# Technical Methodology

## Mathematical Approach

### Optimization Model Type
**Mixed-Integer Linear Programming (MILP)**
- Binary variables for warehouse opening decisions
- Continuous variables for shipment quantities
- Linear objective function and constraints

### Objective Function
Minimize: Total Cost = Fixed Costs + Transportation Costs

text

### Decision Variables
- `open_w` = 1 if warehouse w is open, 0 otherwise (binary)
- `ship_wc` = quantity shipped from warehouse w to customer c (continuous)

### Constraints
1. **Demand Satisfaction**: ∑_w ship_wc = demand_c for all customers c
2. **Capacity Limits**: ∑_c ship_wc ≤ capacity_w * open_w for all warehouses w  
3. **Warehouse Count**: MIN ≤ ∑_w open_w ≤ MAX
4. **Shipping Logic**: ship_wc ≤ open_w * M (big M constraint)

## Data Processing Pipeline

### Step 1: Data Transformation
- Load and clean raw shipment data
- Calculate monthly demand averages
- Estimate warehouse capacities from historical data
- Compute transportation cost matrix

### Step 2: Feature Engineering
- Customer demand aggregation
- Warehouse capacity estimation
- Transportation cost calculation
- Regional assignment

### Step 3: Model Building
- Define decision variables
- Formulate objective function
- Add constraints
- Set strategic parameters

### Step 4: Solution & Analysis
- Solve optimization model
- Extract optimal solution
- Analyze cost breakdown
- Generate business insights

## Technical Stack

### Programming Languages
- **Python 3.8+**: Main programming language

### Key Libraries
- **Pandas**: Data manipulation and analysis
- **PuLP**: Mathematical optimization modeling
- **NumPy**: Numerical computations
- **Matplotlib**: Data visualization

### Optimization Solver
- **CBC (Coin-or branch and cut)**: Default solver in PuLP
- Open-source mixed integer programming solver

## Model Validation

### Feasibility Checks
- Demand-capacity balance verification
- Constraint satisfaction testing
- Solution integrity validation

### Sensitivity Analysis
- Capacity constraint impact
- Demand variation effects
- Cost parameter changes

### Performance Metrics
- Solution optimality gap
- Computation time
- Memory usage
- Scalability assessment

## File Structure
supply-chain-optimization/
├── data/ # Input and processed data
├── src/ # Source code
│ ├── 01_data_transformation.py
│ ├── 02_optimization_model.py
│ ├── 03_visualization.py
│ └── 04_business_insights.py
├── docs/ # Documentation
├── results/ # Output files
└── requirements.txt # Dependencies

text

## Assumptions & Limitations

### Key Assumptions
- Historical demand patterns predict future demand
- Warehouse capacities scale with historical usage
- Transportation costs follow distance-based patterns
- Fixed costs correlate with warehouse size

### Limitations
- Static demand (no seasonality)
- Linear cost relationships
- Deterministic parameters
- Single-period optimization

## Future Enhancements
- Multi-period optimization
- Stochastic demand modeling
- Nonlinear cost functions
- Real-time data integration
