import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Battery Analysis Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .battery-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Battery specifications database
BATTERY_SPECS = {
    "lfp": {
        "name": "Lithium Iron Phosphate (LiFePO4)",
        "nominal_voltage": 3.2,
        "min_voltage": 2.5,
        "max_voltage": 3.6,
        "energy_density": "90-120 Wh/kg",
        "cycle_life": "2000-3000 cycles",
        "operating_temp": "-20°C to 60°C",
        "safety": "Very High",
        "applications": ["Electric vehicles", "Energy storage", "Power tools"],
        "advantages": ["Long cycle life", "High safety", "Stable discharge"],
        "disadvantages": ["Lower energy density", "Higher cost per Wh"]
    },
    "nmc": {
        "name": "Nickel Manganese Cobalt (NMC)",
        "nominal_voltage": 3.7,
        "min_voltage": 3.0,
        "max_voltage": 4.2,
        "energy_density": "150-220 Wh/kg",
        "cycle_life": "500-1000 cycles",
        "operating_temp": "-10°C to 50°C",
        "safety": "Moderate",
        "applications": ["Electric vehicles", "Laptops", "Power banks"],
        "advantages": ["High energy density", "Good power capability"],
        "disadvantages": ["Shorter cycle life", "Thermal runaway risk"]
    },
    "lco": {
        "name": "Lithium Cobalt Oxide (LiCoO2)",
        "nominal_voltage": 3.7,
        "min_voltage": 3.0,
        "max_voltage": 4.2,
        "energy_density": "150-200 Wh/kg",
        "cycle_life": "300-500 cycles",
        "operating_temp": "0°C to 45°C",
        "safety": "Low",
        "applications": ["Smartphones", "Tablets", "Cameras"],
        "advantages": ["High energy density", "Low self-discharge"],
        "disadvantages": ["Poor thermal stability", "Limited cycle life"]
    }
}

def main():
    st.markdown('<h1 class="main-header">🔋 Battery Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar for user inputs
    st.sidebar.header("Battery Configuration")
    
    # User inputs
    bench_name = st.sidebar.text_input("Enter your bench name:", value="Bench-001")
    group_num = st.sidebar.number_input("Enter your group number:", min_value=1, max_value=100, value=1)
    
    # Battery type selection
    battery_type = st.sidebar.selectbox(
        "Select battery cell type:",
        options=["lfp", "nmc", "lco"],
        format_func=lambda x: f"{x.upper()} - {BATTERY_SPECS[x]['name']}"
    )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📊 Battery Analysis")
        
        # Display current configuration
        st.info(f"**Bench:** {bench_name} | **Group:** {group_num} | **Cell Type:** {battery_type.upper()}")
        
        # Get battery specifications
        specs = BATTERY_SPECS[battery_type]
        
        # Display key metrics
        st.subheader("Key Battery Metrics")
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.metric("Nominal Voltage", f"{specs['nominal_voltage']} V")
        with metric_cols[1]:
            st.metric("Min Voltage", f"{specs['min_voltage']} V")
        with metric_cols[2]:
            st.metric("Max Voltage", f"{specs['max_voltage']} V")
        with metric_cols[3]:
            st.metric("Energy Density", specs['energy_density'])
        
        # Voltage analysis chart
        st.subheader("Voltage Analysis")
        
        # Generate sample voltage data for demonstration
        time_points = np.linspace(0, 100, 100)
        voltage_data = generate_voltage_curve(specs, time_points)
        
        fig_voltage = go.Figure()
        fig_voltage.add_trace(go.Scatter(
            x=time_points,
            y=voltage_data,
            mode='lines',
            name='Battery Voltage',
            line=dict(color='#1f77b4', width=2)
        ))
        
        # Add voltage limits
        fig_voltage.add_hline(y=specs['nominal_voltage'], line_dash="dash", 
                             line_color="green", annotation_text="Nominal Voltage")
        fig_voltage.add_hline(y=specs['min_voltage'], line_dash="dash", 
                             line_color="red", annotation_text="Min Voltage")
        fig_voltage.add_hline(y=specs['max_voltage'], line_dash="dash", 
                             line_color="orange", annotation_text="Max Voltage")
        
        fig_voltage.update_layout(
            title="Battery Voltage vs State of Charge",
            xaxis_title="State of Charge (%)",
            yaxis_title="Voltage (V)",
            height=400
        )
        
        st.plotly_chart(fig_voltage, use_container_width=True)
        
        # Cycle life analysis
        st.subheader("Cycle Life Analysis")
        
        cycle_data = generate_cycle_data(specs)
        
        fig_cycle = px.line(cycle_data, x='Cycle', y='Capacity_Retention', 
                           title='Battery Capacity Retention vs Cycle Number',
                           labels={'Capacity_Retention': 'Capacity Retention (%)'})
        fig_cycle.update_traces(line_color='#ff7f0e')
        fig_cycle.update_layout(height=400)
        
        st.plotly_chart(fig_cycle, use_container_width=True)
    
    with col2:
        st.header("🔋 Battery Information")
        
        # Battery specifications card
        with st.container():
            st.markdown(f"""
            <div class="battery-card">
                <h3>{specs['name']}</h3>
                <p><strong>Nominal Voltage:</strong> {specs['nominal_voltage']} V</p>
                <p><strong>Voltage Range:</strong> {specs['min_voltage']} - {specs['max_voltage']} V</p>
                <p><strong>Energy Density:</strong> {specs['energy_density']}</p>
                <p><strong>Cycle Life:</strong> {specs['cycle_life']}</p>
                <p><strong>Operating Temp:</strong> {specs['operating_temp']}</p>
                <p><strong>Safety Level:</strong> {specs['safety']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Applications
        st.subheader("Applications")
        for app in specs['applications']:
            st.write(f"• {app}")
        
        # Advantages
        st.subheader("✅ Advantages")
        for adv in specs['advantages']:
            st.write(f"• {adv}")
        
        # Disadvantages
        st.subheader("❌ Disadvantages")
        for dis in specs['disadvantages']:
            st.write(f"• {dis}")
        
        # Safety recommendations
        st.subheader("⚠️ Safety Recommendations")
        safety_tips = [
            "Monitor temperature during operation",
            "Avoid overcharging and deep discharge",
            "Use appropriate charging protocols",
            "Regular capacity testing",
            "Proper ventilation in battery rooms"
        ]
        
        for tip in safety_tips:
            st.write(f"• {tip}")
    
    # Additional analysis section
    st.header("📈 Advanced Analysis")
    
    analysis_tabs = st.tabs(["Temperature Effects", "Power Analysis", "Degradation Model"])
    
    with analysis_tabs[0]:
        st.subheader("Temperature Impact on Performance")
        temp_data = generate_temperature_data(specs)
        
        fig_temp = px.line(temp_data, x='Temperature', y=['Capacity', 'Power'], 
                          title='Battery Performance vs Temperature',
                          labels={'value': 'Relative Performance (%)', 'Temperature': 'Temperature (°C)'})
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with analysis_tabs[1]:
        st.subheader("Power Analysis")
        power_data = generate_power_data(specs)
        
        fig_power = px.scatter(power_data, x='Current', y='Power', color='SOC',
                              title='Power Output vs Current Draw',
                              labels={'Current': 'Current (A)', 'Power': 'Power (W)', 'SOC': 'State of Charge (%)'})
        st.plotly_chart(fig_power, use_container_width=True)
    
    with analysis_tabs[2]:
        st.subheader("Battery Degradation Model")
        
        col1, col2 = st.columns(2)
        with col1:
            cycles_input = st.slider("Number of Cycles", 0, 3000, 1000)
        with col2:
            temp_input = st.slider("Average Temperature (°C)", -20, 60, 25)
        
        degradation_data = calculate_degradation(specs, cycles_input, temp_input)
        
        fig_deg = go.Figure()
        fig_deg.add_trace(go.Scatter(
            x=list(range(cycles_input + 1)),
            y=degradation_data,
            mode='lines',
            name='Capacity Retention',
            line=dict(color='red', width=2)
        ))
        
        fig_deg.update_layout(
            title=f"Predicted Capacity Degradation at {temp_input}°C",
            xaxis_title="Cycle Number",
            yaxis_title="Capacity Retention (%)",
            height=400
        )
        
        st.plotly_chart(fig_deg, use_container_width=True)
        
        current_retention = degradation_data[-1] if degradation_data else 100
        st.metric("Predicted Capacity Retention", f"{current_retention:.1f}%")

def generate_voltage_curve(specs, soc_points):
    """Generate realistic voltage curve based on battery type"""
    nominal = specs['nominal_voltage']
    min_v = specs['min_voltage']
    max_v = specs['max_voltage']
    
    # Create a typical discharge curve
    voltage_curve = []
    for soc in soc_points:
        if soc > 90:
            # High SOC - voltage drops quickly initially
            voltage = max_v - (max_v - nominal) * (100 - soc) / 10 * 0.3
        elif soc > 20:
            # Mid SOC - relatively flat
            voltage = nominal + (max_v - nominal) * (soc - 20) / 70 * 0.3
        else:
            # Low SOC - voltage drops rapidly
            voltage = min_v + (nominal - min_v) * soc / 20
        
        voltage_curve.append(max(voltage, min_v))
    
    return voltage_curve

def generate_cycle_data(specs):
    """Generate cycle life data"""
    if "lfp" in specs['cycle_life'].lower():
        max_cycles = 2500
        retention_rate = 0.9998
    elif "nmc" in specs['cycle_life'].lower():
        max_cycles = 800
        retention_rate = 0.9992
    else:
        max_cycles = 400
        retention_rate = 0.9985
    
    cycles = list(range(0, max_cycles, 50))
    retention = [100 * (retention_rate ** cycle) for cycle in cycles]
    
    return pd.DataFrame({'Cycle': cycles, 'Capacity_Retention': retention})

def generate_temperature_data(specs):
    """Generate temperature performance data"""
    temps = list(range(-20, 61, 5))
    capacity = []
    power = []
    
    for temp in temps:
        if temp < 0:
            cap_factor = 0.6 + 0.4 * (temp + 20) / 20
            pow_factor = 0.3 + 0.7 * (temp + 20) / 20
        elif temp <= 25:
            cap_factor = 0.9 + 0.1 * temp / 25
            pow_factor = 0.8 + 0.2 * temp / 25
        else:
            cap_factor = 1.0 - 0.2 * (temp - 25) / 35
            pow_factor = 1.0 - 0.3 * (temp - 25) / 35
        
        capacity.append(max(cap_factor * 100, 20))
        power.append(max(pow_factor * 100, 10))
    
    return pd.DataFrame({'Temperature': temps, 'Capacity': capacity, 'Power': power})

def generate_power_data(specs):
    """Generate power analysis data"""
    currents = np.linspace(0.1, 10, 50)
    socs = [20, 50, 80, 100]
    
    data = []
    for soc in socs:
        for current in currents:
            voltage = specs['nominal_voltage'] * (0.8 + 0.2 * soc / 100) * (1 - current * 0.05)
            power = voltage * current
            data.append({'Current': current, 'Power': power, 'SOC': soc})
    
    return pd.DataFrame(data)

def calculate_degradation(specs, cycles, temperature):
    """Calculate battery degradation over cycles"""
    if cycles == 0:
        return [100]
    
    # Base degradation rate (capacity loss per cycle)
    if "lfp" in specs['cycle_life'].lower():
        base_rate = 0.00008  # LFP degrades slowly
    elif "nmc" in specs['cycle_life'].lower():
        base_rate = 0.0002   # NMC moderate degradation
    else:
        base_rate = 0.0005   # LCO degrades faster
    
    # Temperature factor (higher temp = faster degradation)
    temp_factor = 1 + max(0, (temperature - 25) * 0.02)
    
    degradation_rate = base_rate * temp_factor
    
    retention = []
    current_capacity = 100
    
    for cycle in range(cycles + 1):
        retention.append(current_capacity)
        current_capacity = max(current_capacity - degradation_rate * 100, 60)
    
    return retention

if __name__ == "__main__":
    main()