import streamlit as st

st.title("Simulador Predictivo de Eco-Eficiencia")
st.subheader("Asistente Digital para Cervecería Artesanal")
st.write("Optimiza el gasto de agua y gas en tus ollas tradicionales teniendo en cuenta el clima de Bogotá.")
st.divider()

# --- PANEL IZQUIERDO: CONFIGURACIÓN Y SENSOR DE TEMPERATURA ---
st.sidebar.header("1. Metas de tu receta")
cerveza_deseada = st.sidebar.number_input("Litros de cerveza finales que quieres embotellar (L):", value=50.0, step=5.0)
tiempo_hervor = st.sidebar.number_input("Minutos totales que debe hervir el mosto (min):", value=60.0, step=5.0)

st.sidebar.header("2. Datos de tus ollas")
relacion_macerado = st.sidebar.number_input("¿Cuántos litros de agua usas por cada kilo de grano en la lavada inicial?:", value=3.0, step=0.5)
grano_por_litro = st.sidebar.number_input("¿Cuántos kilos de grano usas por cada litro de cerveza? (kg/L):", value=0.2, step=0.05)
relacion_enfriamiento = st.sidebar.number_input("¿Cuántos litros de agua gastas para enfriar un solo litro de mosto caliente?:", value=3.0, step=0.5)

st.sidebar.header("3. Monitor del Sensor (En Vivo)")
# Control deslizante para interactuar frente al jurado
temperatura_sensor = st.sidebar.slider("Temperatura actual en la olla física (°C):", min_value=15.0, max_value=100.0, value=40.0, step=0.5)


# --- VALORES DE REFERENCIA (Bogotá) ---
tasa_evaporacion_bogota = 0.09
temp_ebullicion = 92.7
costo_gas_m3 = 2700.0
costo_agua_litro = 6.5


# --- CÁLCULOS INTERNOS DE BALANCES ---
grano_total_kg = cerveza_deseada * grano_por_litro
absorcion_grano_l = grano_total_kg * 1.0

vol_necesario_antes_enfriar = cerveza_deseada * 1.02
vol_necesario_antes_hervir = vol_necesario_antes_enfriar / (1.0 - (tasa_evaporacion_bogota * (tiempo_hervor / 60.0)))

agua_macerado_manual = grano_total_kg * relacion_macerado
agua_lavado_manual = vol_necesario_antes_hervir - (agua_macerado_manual - absorcion_grano_l)
agua_total_proceso = agua_macerado_manual + agua_lavado_manual
agua_enfriamiento_total = vol_necesario_antes_enfriar * relacion_enfriamiento


# --- PESTAÑAS DISTRIBUIDAS POR ETAPAS CON BLOQUES DE COLOR ---
tab1, tab2, tab3 = st.tabs(["1. Maceración", "2. Cocción (Hervor)", "3. Enfriamiento y Ahorro"])

with tab1:
    st.header("Etapa de Maceración")
    
    st.subheader("Agua requerida para esta etapa:")
    st.info(f"💧 **Mide exactamente e ingresa a la olla:** {agua_macerado_manual:.1f} Litros")
    st.write(f"Para esta cantidad de agua debes mezclar un total de **{grano_total_kg:.1f} kilos de grano**.")
    
    st.write("---")
    st.subheader("Configuración del Equipo:")
    tipo_olla = st.selectbox("Selecciona el material de tu olla de maceración:", ["Acero Inoxidable", "Aluminio", "Cava plástica"])
    
    if tipo_olla == "Cava plástica":
        st.success("✅ **Instrucción:** Tapa bien el recipiente. Al ser plástico, aísla el calor por sí solo y **no necesitas encender el fuego** en ningún momento de esta hora.")
    else:
        st.warning("⚠️ **Instrucción para olla de metal:** El metal pierde calor rápido por el frío de Bogotá. No dejes el fuego encendido continuo; aplica pulsos térmicos prendiendo la llama al mínimo solo 1 minuto cada 15 minutos.")

with tab2:
    st.header("Etapa de Cocción y Control de Fuego")
    
    st.subheader("Agua requerida para esta etapa:")
    st.info(f"💧 **Agua que debes usar para la lavada del grano:** {agua_lavado_manual:.1f} Litros")
    st.write(f"Al juntar toda el agua filtrada en la olla antes de prender el quemador, debes tener exactamente **{vol_necesario_antes_hervir:.1f} Litros** de líquido.")

    st.write("---")
    st.subheader("Pauta del Sensor en Tiempo Real:")
    st.write(f"Por la altura de la ciudad, tu mosto nunca va a pasar de los {temp_ebullicion} grados. Sigue la alerta de color según lo que marque tu termómetro:")
    
    st.write(f"**Temperatura actual detectada:** {temperatura_sensor} °C")
    
    if temperatura_sensor < 92.0:
        st.info(f"🔵 **Fase: CALENTAMIENTO INICIAL** \n**Acción:** Sube el fuego al **Máximo (100% de potencia)**. El asistente digital estima que aún faltan {temp_ebullicion - temperatura_sensor:.1f} °C para que empiece a hervir.")
    elif 92.0 <= temperatura_sensor <= 93.5:
        st.success(f"🟢 **Fase: ¡HERVOR EFICIENTE ALCANZADO!** \n**Acción de Eco-Eficiencia:** ¡Baja de inmediato el fuego al **Nivel Medio-Bajo (40% de potencia)**! Este nivel bajito es calor suficiente para cocinar el mosto de forma óptima durante los {tiempo_hervor:.0f} minutos.")
    else:
        grados_exceso = temperatura_sensor - temp_ebullicion
        st.error(f"🔴 **Fase: ¡ALERTA DE DESPERDICIO CRÍTICO!** \n**Acción:** Te pasaste por {grados_exceso:.1f} °C del punto de ebullición de Bogotá. El mosto no se va a calentar más; estás gastando gas innecesario y evaporando el agua de tu receta. **¡Baja el fuego de inmediato!**")

    st.write(f"**Meta al apagar el quemador:** Deben quedarte exactamente **{vol_necesario_antes_enfriar:.1f} Litros** dentro de la olla.")

with tab3:
    st.header("Etapa de Enfriamiento y Dinero Ahorrado")
    
    st.subheader("Gasto de agua para enfriar:")
    st.warning(f"💧 **Agua total que pasará por el enfriador:** {agua_enfriamiento_total:.1f} Litros de agua limpia.")
    st.success("💡 **Estrategia de reúso:** Conecta la manguera de salida del enfriador a un tanque limpio. Toda esa agua saldrá caliente y limpia, perfecta para lavar tus ollas y pisos mañana sin gastar agua nueva de la llave.")

    st.write("---")
    st.subheader("Impacto y Beneficios Totales de tu Lote")
    
    # Cálculos económicos y ambientales
    botellas_ahorradas = agua_enfriamiento_total / 0.5
    dinero_agua_ahorrado = agua_enfriamiento_total * costo_agua_litro
    ahorro_gas_m3 = 0.4 * (tiempo_hervor / 60.0)
    dinero_gas_ahorrado = ahorro_gas_m3 * costo_gas_m3
    total_dinero_ahorrado = dinero_agua_ahorrado + dinero_gas_ahorrado
    co2_ahorrado_kg = ahorro_gas_m3 * 1.95

    col_eco1, col_eco2 = st.columns(2)
    
    with col_eco1:
        with st.container(border=True):
            st.subheader("Sostenibilidad Ambiental")
            st.metric(label="Agua Limpia Salvada", value=f"{agua_enfriamiento_total:.1f} L")
            st.write(f"Equivale a **{botellas_ahorradas:,.0f} botellas de agua** de la tienda.")
            st.metric(label="Reducción de Humo (CO2)", value=f"{co2_ahorrado_kg:.2f} kg")
            st.write("Evitado en la atmósfera de Bogotá.")
        
    with col_eco2:
        with st.container(border=True):
            st.subheader("Viabilidad Económica")
            st.write(f"- Por no botar el agua: $ {dinero_agua_ahorrado:,.0f} COP")
            st.write(f"- Por bajar el fuego a tiempo: $ {dinero_gas_ahorrado:,.0f} COP")
            st.divider()
            st.metric(label="AHORRO TOTAL DE ESTE LOTE", value=f"$ {total_dinero_ahorrado:,.0f} COP")

    st.divider()
    st.info("Mensaje para el jurado: Esta aplicación demuestra que la eco-eficiencia digital no requiere maquinaria costosa. Con solo organizar el uso del agua manualmente y controlar el fuego a tiempo paso a paso, se reducen las facturas de servicios públicos y el impacto ambiental.")
