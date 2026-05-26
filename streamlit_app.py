import streamlit as st
import time

st.title("Propuesta de Gemelo Digital - Planta Cervecera")
st.subheader("Réplica Virtual para la Eco-Eficiencia Operativa")
st.write("Este módulo actúa como el gemelo digital de tu olla física en Bogotá, simulando el proceso térmico.")
st.divider()

# ENTRADAS MANUALES EN EL PANEL IZQUIERDO
st.sidebar.header("1. Parámetros de la Planta Física")
cerveza_deseada = st.sidebar.number_input("Litros de cerveza finales a producir (L):", value=50.0, step=5.0)
tiempo_hervor = st.sidebar.number_input("Minutos de cocción programados (min):", value=60.0, step=5.0)

st.sidebar.header("2. Telemetría / Entrada de Sensores")
# Simulamos un sensor de temperatura físico mediante un control deslizante
temperatura_sensor = st.sidebar.slider("Temperatura actual de la olla física (°C):", min_value=15.0, max_value=100.0, value=20.0, step=0.5)

# VARIABLES DE REFERENCIA (Bogotá)
tasa_evaporacion_bogota = 0.09
temp_ebullicion = 92.7
costo_gas_m3 = 2700.0
costo_agua_litro = 6.5

# CÁLCULOS DEL GEMELO DIGITAL
grano_total_kg = cerveza_deseada * 0.2
vol_necesario_antes_enfriar = cerveza_deseada * 1.02
vol_necesario_antes_hervir = vol_necesario_antes_enfriar / (1.0 - (tasa_evaporacion_bogota * (tiempo_hervor / 60.0)))
agua_enfriamiento_total = vol_necesario_antes_enfriar * 3.0

# PESTAÑAS DEL GEMELO DIGITAL
tab1, tab2 = st.tabs(["Panel de Control del Gemelo Digital", "Reporte de Sostenibilidad"])

with tab1:
    st.header("Monitoreo de la Réplica Virtual")
    
    # Creamos un indicador visual que cambie según el "sensor"
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.metric(label="Temperatura en la Olla Física", value=f"{temperatura_sensor} °C")
    with col_v2:
        if temperatura_sensor < temp_ebullicion:
            st.warning("Estado: Fase de Calentamiento Inicial")
        else:
            st.success("Estado: ¡Punto de Ebullición Alcanzado!")

    st.write("---")
    st.subheader("Instrucciones Automáticas del Asistente Virtual")
    
    if temperatura_sensor < temp_ebullicion:
        st.write("👉 **Acción en Planta:** Mantén la candela al **Nivel Máximo (100% de potencia)**.")
        st.write(f"El gemelo digital estima que aún faltan {temp_ebullicion - temperatura_sensor:.1f} °C para iniciar el hervor en Bogotá.")
    else:
        st.write("🚨 **¡ALERTA DE ECO-EFICIENCIA!**")
        st.write(f"El sensor detecta que ya estás a {temperatura_sensor} °C. Por la altura de Bogotá, el mosto no calentará más.")
        st.write("👉 **Acción en Planta de inmediato:** Baja la candela al **Nivel Medio-Bajo (40% de potencia)** para evitar evaporar agua en exceso y ahorrar gas.")

with tab2:
    st.header("Balances de Masa y Energía del Lote")
    st.write("Volúmenes iniciales calculados por el gemelo digital para iniciar el proceso:")
    st.write(f"- Agua total para el proceso: **{vol_necesario_antes_hervir + (grano_total_kg * 3.0):.1f} Litros**.")
    
    st.write("---")
    st.subheader("Retorno de Inversión Ambiental")
    botellas_ahorradas = agua_enfriamiento_total / 0.5
    st.write(f"Al recuperar el agua de enfriamiento basándote en las alertas del gemelo, evitas botar **{agua_enfriamiento_total:.1f} Litros**.")
    st.metric(label="Equivalente en botellas de agua (500 mL)", value=f"{botellas_ahorradas:,.0f} Botellas")
    
    # Cálculos económicos
    dinero_agua_ahorrado = agua_enfriamiento_total * costo_agua_litro
    ahorro_gas_m3 = 0.4 * (tiempo_hervor / 60.0)
    dinero_gas_ahorrado = ahorro_gas_m3 * costo_gas_m3
    
    st.metric(label="TOTAL DE DINERO AHORRADO EN ESTE LOTE", value=f"$ {dinero_agua_ahorrado + dinero_gas_rodo:,.0f} COP" if 'dinero_gas_rodo' in locals() else f"$ {dinero_agua_ahorrado + dinero_gas_ahorrado:,.0f} COP")
