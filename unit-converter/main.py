import streamlit as st

length_units: dict = {
    "Kilometer (km)": 1000, "Meter (m)": 1, "Centimeter (cm)": 0.01,
    "Millimeter (mm)": 0.001, "Micrometer (µm)": 1e-6, "Nanometer (nm)": 1e-9,
    "Mile (mi)": 1609.34, "Yard (yd)": 0.9144, "Foot (ft)": 0.3048, "Inch (in)": 0.0254
}

weight_units: dict = {
    "Ton (t)": 1000, "Kilogram (kg)": 1, "Gram (g)": 0.001, "Milligram (mg)": 1e-6,
    "Microgram (µg)": 1e-9, "Pound (lb)": 0.453592, "Ounce (oz)": 0.0283495
}

volume_units: dict = {
    "Cubic Meter (m³)": 1000, "Liter (L)": 1, "Milliliter (mL)": 0.001,
    "Gallon (US)": 3.78541, "Gallon (UK)": 4.54609, "Pint (US)": 0.473176,
    "Pint (UK)": 0.568261, "Fluid Ounce (US)": 0.0295735, "Fluid Ounce (UK)": 0.0284131
}

time_units: dict = {
    "Hour (h)": 3600, "Minute (min)": 60, "Second (s)": 1,
    "Millisecond (ms)": 0.001, "Microsecond (µs)": 1e-6
}


st.title("Unit Converter")

conversion_type = st.selectbox("Select Conversion Type: ", ["Length", "Weight", "Volume", "Temperature", "Time"], index=None)


def converter(value, from_unit, to_unit):
    
    #Length
    if conversion_type == "Length":
        return value * (length_units[from_unit] / length_units[to_unit])
    
    #Weight
    elif conversion_type == "Weight":
        return value * (weight_units[from_unit] / weight_units[to_unit])
    
    # Volume
    elif conversion_type == "Volume":
        return value * (volume_units[from_unit] / volume_units[to_unit])
    
    # Time
    elif conversion_type == 'Time':
        return value * (time_units[from_unit] / time_units[to_unit])
    
    # Temperature
    elif conversion_type == 'Temperature':
        # Celsius to Farenheit
        if from_unit == "Celsius (°C)" and to_unit == "Fahrenheit (°F)":
            return (value * 9/5) + 32
        # Fahrenheit to Celsius
        elif from_unit == "Fahrenheit (°F)" and to_unit == "Celsius (°C)":
            return (value - 32) * 5/9
        # Celsius to Kelvin
        elif from_unit == "Celsius (°C)" and to_unit == "Kelvin (K)":
            return value + 273.15
        # kelvin to Celsius
        elif from_unit == "Kelvin (K)" and to_unit == "Celsius (°C)":
            return value - 273.15
        # Fahrenheit to Kelvin
        elif from_unit == "Fahrenheit (°F)" and to_unit == "Kelvin (K)":
            return (value - 32) * 5/9 + 273.15
        # Kelvin to Fahrenheit
        elif from_unit == "Kelvin (K)" and to_unit == "Fahrenheit (°F)":
            return (value - 273.15) * 9/5 + 32
        else:
            return value  # Same unit, no conversion needed


if conversion_type:
    if conversion_type == "Length":
        units = length_units.keys()
    elif conversion_type == "Weight":
        units = weight_units.keys()
    elif conversion_type == "Volume":
        units = volume_units.keys()
    elif conversion_type == "Temperature":
        units = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
    elif conversion_type == "Time":
        units = time_units.keys()

if conversion_type:
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    value = st.number_input("Enter Value", min_value=0, step=1)


    if st.button("Convert"):
        result = converter(value, from_unit, to_unit)
        st.success(f"✅ Result: {result} {to_unit}")