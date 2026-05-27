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
# Regresa el simulador del sensor que se había borrado
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


# --- PESTAÑAS DISTRIBUIDAS POR ETAPAS DEL PROCESO ---
tab1, tab2, tab3 = st.tabs(["1. Maceración", "2. Cocción (Hervor)", "3. Enfriamiento y Ahorro"])

with tab1:
    st.header("Etapa de Maceración")
    
    # Imagen de granos/malta usando un servidor de código abierto estable
    st.image("https://images.unsplash.com/photo-1566633806327-68e152aaf26d?w=500", 
             caption="Preparación de los granos de malta para el proceso", use_container_width=True)
    
    with st.container(border=True):
        st.subheader("Agua requerida para esta etapa:")
        st.metric(label="Mide exactamente e ingresa a la olla:", value=f"{agua_macerado_manual:.1f} Litros")
        st.write(f"Para esta cantidad de agua debes mezclar un total de **{grano_total_kg:.1f} kilos de grano**.")
    
    st.write("---")
    st.subheader("Instrucciones para el fuego:")
    st.write("- **Si usas olla de metal (Acero o Aluminio):** No dejes el fuego encendido todo el tiempo. Enciende la llama al mínimo solo 1 minuto cada 15 minutos para mantener el calor.")
    st.write("- **Si usas una cava plástica:** Tapa bien el recipiente. El plástico aísla el calor por sí solo y no necesitas prender fuego en ningún momento de esta hora.")

with tab2:
    st.header("Etapa de Cocción y Control de Fuego")
    
    # Imagen de la olla de cocción / ebullición
    st.image("https://images.unsplash.com/photo-1532635241-17e820aac095?w=500", 
             caption="Proceso de ebullición y control de energía en la olla", use_container_width=True)
    
    with st.container(border=True):
        st.subheader("Agua requerida para esta etapa:")
        st.metric(label="Agua que debes usar para la lavada del grano:", value=f"{agua_lavado_manual:.1f} Litros")
        st.write(f"Al juntar toda el agua filtrada en la olla antes de prender el quemador, debes tener exactamente **{vol_necesario_antes_hervir:.1f} Litros** de líquido.")

    st.write("---")
    st.subheader("Pauta del Sensor en Tiempo Real:")
    st.write(f"Por la altura de la ciudad, tu mosto nunca va a pasar de los {temp_ebullicion} grados. No gastes gas de más intentando buscar que suba a 100 grados.")
    
    # Evaluación en vivo del sensor dentro de la pestaña de cocción
    with st.container(border=True):
        st.write(f"**Temperatura detectada por el sensor:** {temperatura_sensor} °C")
        
        if temperatura_sensor < temp_ebullicion:
            st.info(" **Instrucción actual:** Sube el fuego al **Máximo (100% de potencia)**.")
            st.write(f"Faltan {temp_ebullicion - temperatura_sensor:.1f} °C para que empiece a hervir.")
        elif temperatura_sensor == temp_ebullicion:
            st.success(" **¡Llegaste al punto de hervor!** Baja de inmediato el fuego al **Nivel Medio-Bajo (40% de potencia)**.")
            st.write(f"Mantén este nivel bajito durante los {tiempo_hervor:.0f} minutos. Es calor suficiente para cocinar el mosto de forma eficiente.")
        else:
            st.error(" **¡Alerta de Desperdicio!** Te pasaste del punto de ebullición de Bogotá.")
            st.write(f"Estás a {temperatura_sensor} °C. El mosto no va a calentarse más, solo estás perdiendo gas y evaporando agua en exceso. ¡Baja el fuego ya!")

with tab3:
    st.header("Etapa de Enfriamiento y Dinero Ahorrado")
    
    # Imagen de flujo de agua limpia / enfriador
    st.image("https://images.unsplash.com/photo-1617155093730-a8bf47be792d?w=500", 
             caption="Recuperación del agua del intercambiador de calor", use_container_width=True)
    
    with st.container(border=True):
        st.subheader("Gasto de agua para enfriar:")
        st.write(f"Para enfriar este lote de mosto, pasarán por tu enfriador un total de **{agua_enfriamiento_total:.1f} Litros** de agua limpia.")
        st.info("Estrategia de reúso: Conecta la manguera de salida del enfriador a un tanque limpio. Toda esa agua saldrá caliente y limpia, perfecta para lavar tus ollas y pisos mañana sin gastar agua nueva de la llave.")

    st.write("---")
    st.subheader("Impacto y Beneficios de tu lote")
    
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
            st.write("**Impacto Ambiental:**")
            st.write(f"- Salvaste el equivalente a: **{botellas_ahorradas:,.0f} botellas de agua** de la tienda.")
            st.write(f"- Evitaste enviar a la atmósfera de Bogotá: **{co2_ahorrado_kg:.2f} kg de humo ($CO_2$)**.")
        
    with col_eco2:
        with st.container(border=True):
            st.write("**Dinero que dejas de pagar:**")
            st.write(f"- Por no botar el agua: $ {dinero_agua_ahorrado:,.0f} COP")
            st.write(f"- Por bajar el fuego a tiempo: $ {dinero_gas_ahorrado:,.0f} COP")
            st.divider()
            st.metric(label="AHORRO TOTAL DE ESTE LOTE", value=f"$ {total_dinero_ahorrado:,.0f} COP")

    st.divider()
    st.info("Mensaje para el jurado: Esta aplicación demuestra que la eco-eficiencia digital no requiere maquinaria costosa. Con solo organizar el uso del agua manualmente y controlar el fuego a tiempo paso a paso, se reducen las facturas de servicios públicos y el impacto ambiental.")
