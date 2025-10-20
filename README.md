# Supply Chain Network Optimization

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Optimization](https://img.shields.io/badge/Optimization-MILP-green)](https://www.python.org)
[![Supply Chain](https://img.shields.io/badge/Supply%20Chain-Logistics-orange)](https://www.python.org)

##  Project Overview
Optimized a national distribution network using **Mixed-Integer Linear Programming (MILP)** to minimize costs while meeting customer demand across 15 major US cities. This project demonstrates end-to-end data analysis from raw data to business recommendations.

##  Key Achievements
- **22.6% monthly cost reduction** ($76,922 savings)
- **$923,072 annual savings** identified  
- **5,438% ROI** over 3 years
- **Optimal 8-warehouse network** serving 15 cities

##  Demo
![supply_chain_optimization_results](results/supply_chain_optimization_results.png)
*Cost breakdown, warehouse utilization, and demand distribution*

##  Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation & Run
```bash
# Clone repository
git clone https://github.com/yourusername/supply-chain-optimization.git
cd supply-chain-optimization

# Install dependencies
pip install -r requirements.txt

# Run complete analysis
python run_all.py
Run Individual Steps
bash
# Step-by-step execution
python src/01_data_transformation.py    # Data preparation
python src/02_optimization_model.py     # Optimization
python src/03_visualization.py          # Charts & graphs
python src/04_business_insights.py      # Business analysis
Project Structure
text
supply-chain-optimization/
├── data/                 # Input/processed data
├── src/                  # Source code
│   ├── 01_data_transformation.py
│   ├── 02_optimization_model.py
│   ├── 03_visualization.py
│   └── 04_business_insights.py
├── docs/                 # Documentation
├── results/              # Output visualizations
└── run_all.py           # One-click runner
Technical Implementation
Methodology
Mathematical Optimization: Mixed-Integer Linear Programming (MILP)

Data Source: 2,000+ real shipment records

Objective: Minimize Total Cost = Fixed Costs + Transportation Costs

Constraints: Demand satisfaction, capacity limits, strategic warehouse count

Key Features
Data Pipeline: Raw data → Transformation → Optimization → Insights

Problem Solving: Diagnosed and fixed model infeasibility through capacity analysis

Business Intelligence: Executive dashboards with ROI analysis

Professional Visualization: Four-panel charts for comprehensive insights

Technologies Used
Python (Pandas, PuLP, Matplotlib, NumPy)

Mathematical Optimization (Mixed-Integer Linear Programming)

Data Analysis & Business Intelligence

Supply Chain Management principles

Business Impact
Before Optimization
Inefficient warehouse utilization

High transportation costs

Suboptimal network design

After Optimization
22.6% cost reduction ($76,922 monthly savings)

Strategic 8-warehouse network (from 10 potential locations)

100% capacity utilization across selected facilities

6 regions covered, 15/15 cities served

ROI Analysis
Implementation Cost: $50,000 (one-time)

Annual Savings: $923,072

Payback Period: 0.1 years

3-Year ROI: 5,438%

Skills Demonstrated
Technical Skills
Mathematical Modeling: MILP formulation and solving

Data Engineering: Data cleaning, transformation, feature engineering

Optimization: Constraint handling, capacity-demand balancing

Data Visualization: Professional charts and business dashboards

Business Skills
Supply Chain Management: Network design, logistics optimization

Financial Analysis: ROI calculation, cost-benefit analysis

Strategic Planning: Implementation roadmap, growth planning

Problem Solving: Constraint diagnosis and resolution

Soft Skills
Analytical Thinking: Breaking down complex business problems

Communication: Translating technical results to business insights

Project Management: End-to-end project execution

Use Cases
For Businesses
Supply chain network design

Distribution center optimization

Logistics cost reduction

Capacity planning and expansion

For Job Seekers
Data science portfolio project

Operations research demonstration

Supply chain analytics example

Business consulting case study

Documentation
Project Overview - Business context and objectives

Technical Methodology - Detailed technical approach

Dependencies
txt
pandas>=1.5.0
numpy>=1.21.0  
pulp>=2.6.0
matplotlib>=3.5.0
openpyxl>=3.0.0
Contributing
Contributions welcome! Please feel free to submit a Pull Request.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

 License
Distributed under the MIT License. See LICENSE for more information.

Author
Your Name

GitHub: @SHABCODES

LinkedIn: https://www.linkedin.com/in/shabda-pyari-mantripragada/

Acknowledgments
Data sourced from real logistics operations

Optimization concepts from operations research

Visualization techniques from data science best practices

Why This Project Stands Out
This project demonstrates real business impact through:

Quantifiable Results: 22.6% cost reduction with $923K annual savings

End-to-End Execution: From raw data to executive recommendations

Technical Depth: Mathematical optimization with constraint handling

Professional Presentation: Business-ready visualizations and insights

Perfect for demonstrating capabilities to employers in consulting, analytics, and supply chain roles!

 If you found this project useful, please give it a star!

text

## KEY ADDITIONS THAT MAKE IT STAND OUT:

### 1. Visual Elements
- Badges for technologies
- Demo image section
- Clean formatting

### 2. Business Impact Focus
- Clear "before/after" comparison
- ROI analysis
- Real savings numbers

### 3. Skills Highlight
- Technical, business, AND soft skills
- Specific technologies used
- Problem-solving examples

### 4. Use Cases
- Shows applicability to real business problems
- Demonstrates value to employers

### 5. Professional Tone
- Confident but not arrogant
- Focus on results and impact
- Clear value proposition

### 6. **Call to Action**
- Star the repo
- Contact information
- Clear next steps
