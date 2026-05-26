import streamlit as st

# Título de la aplicación
st.title("Asistente de Eco-Eficiencia para Cervecería Artesanal")
st.write("Optimiza agua y gas en tus ollas tradicionales a 2.600 msnm.")
st.divider()

# Pestañas del proceso
tab1, tab2, tab3 = st.tabs(["Maceración", "Ebullición", "Enfriamiento"])

with tab1:
    st.header("Optimización del Macerado")
    tipo_olla = st.selectbox("¿De qué material es tu olla?", ["Acero Inoxidable", "Aluminio", "Cava plástica"])
    if tipo_olla == "Cava plástica":
        st.success("Excelente aislamiento. No necesitas encender el fuego.")
    else:
        st.warning(f"La olla de {tipo_olla} pierde calor rápido. Aplica **pulsos térmicos**: fuego al mínimo solo 1 minuto cada 15 minutos.")

with tab2:
    st.header("Control de Evaporación y Gas")
    vol_inicial = st.number_input("¿Litros de mosto iniciales?", value=100)
    tiempo_hervor = st.number_input("¿Minutos de hervor?", value=60)
    
    # Cálculo termodinámico para Bogotá
    agua_evaporada_ideal = vol_inicial * 0.09 * (tiempo_hervor / 60)
    
    st.info("En Bogotá tu mosto hierve a **92.7°C**. ¡No busques los 100°C!")
    st.success(f"Meta de evaporación de tu receta: **{agua_evaporada_ideal:.1f} Litros**.")
    st.write("**Acción:** Al llegar a 92.7°C, baja la llama al 40% para mantener el hervor justo y ahorrar un 35% de gas Vanti.")

with tab3:
    st.header("Recuperación del Agua")
    agua_enfriamiento = vol_inicial * 3
    st.metric(label="Agua caliente limpia generada", value=f"{agua_enfriamiento} Litros")
    st.write(f"Recupera esos {agua_enfriamiento}L en un tanque para el lavado de mañana. ¡Bajarás tu consumo hídrico de 8:1 a 4:1!")
