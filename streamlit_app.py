import streamlit as st

st.title("Simulador Predictivo de Eco-Eficiencia")
st.subheader("Asistente Digital para Cervecería Artesanal")
st.write("Optimiza tus recursos paso a paso en cada etapa del proceso.")
st.divider()

# --- VALORES FIJOS DE REFERENCIA (Bogotá) ---
tasa_evaporacion_bogota = 0.09
temp_ebullicion = 92.7
costo_gas_m3 = 2689.44
costo_agua_litro = 11.70

# --- PESTAÑAS DISTRIBUIDAS POR ETAPAS ---
tab1, tab2, tab3 = st.tabs(["1. Maceración", "2. Cocción (Hervor)", "3. Enfriamiento y Ahorro"])

with tab1:
    st.header("Etapa de Maceración")
    st.write("Configura los datos de tu receta para calcular el agua inicial.")
    
    # 1. PARÁMETROS DE ENTRADA PROPIOS DE ESTA ETAPA
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        cerveza_deseada = st.number_input("Litros de cerveza finales que quieres embotellar (L):", value=50.0, step=5.0, key="mace_l")
        grano_por_litro = st.number_input("Kilos de grano que usas por cada litro de cerveza (kg/L):", value=0.2, step=0.05, key="mace_grano")
    with col_in2:
        relacion_macerado = st.number_input("Litros de agua que usas por cada kilo de grano en esta etapa:", value=3.0, step=0.5, key="mace_rel")
        tipo_olla = st.selectbox("Selecciona el material de tu olla de maceración:", ["Acero Inoxidable", "Aluminio", "Cava plástica"])

    # CÁLCULOS ESPECÍFICOS DE MACERACIÓN
    grano_total_kg = cerveza_deseada * grano_por_litro
    agua_macerado_manual = grano_total_kg * relacion_macerado

    st.write("---")
    
    # 2. BALANCE DE AGUA DE LA ETAPA
    st.subheader("💧 Balance de Agua: Maceración")
    st.info(f"**Agua requerida para iniciar:** Mide exactamente **{agua_macerado_manual:.1f} Litros** de agua e ingrésalos a la olla.")
    st.write(f"Para mantener la receta balanceada, debes mezclar esa agua con un total de **{grano_total_kg:.1f} kilos de grano**.")

    # 3. ANÁLISIS ENERGÉTICO DE LA ETAPA
    st.subheader("🔥 Análisis Energético: Maceración")
    if tipo_olla == "Cava plástica":
        st.success("✅ **Hervor pasivo:** Al usar una cava plástica, el recipiente aísla el calor por sí solo. Mantén la tapa bien cerrada y **no necesitas encender el fuego** en ningún momento de esta hora. Ahorro de gas: 100%.")
    else:
        st.warning("⚠️ **Pérdida térmica:** Las ollas de metal pierden calor rápidamente por el clima frío de Bogotá. No dejes la llama encendida todo el tiempo; aplica pulsos de calor prendiendo el fuego al mínimo solo 1 minuto cada 15 minutos.")

with tab2:
    st.header("Etapa de Cocción y Control de Fuego")
    st.write("Monitorea el punto de ebullición para evitar el desperdicio de gas.")
    
    # 1. PARÁMETROS DE ENTRADA PROPIOS DE ESTA ETAPA
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        tiempo_hervor = st.number_input("Minutos totales que debe hervir el mosto (min):", value=60.0, step=5.0, key="coc_tiempo")
    with col_c2:
        temperatura_sensor = st.slider("Temperatura actual en la olla física (°C):", min_value=15.0, max_value=100.0, value=40.0, step=0.5, key="coc_sensor")

    # CÁLCULOS ESPECÍFICOS DE COCCIÓN
    vol_necesario_antes_enfriar = cerveza_deseada * 1.02
    vol_necesario_antes_hervir = vol_necesario_antes_enfriar / (1.0 - (tasa_evaporacion_bogota * (tiempo_hervor / 60.0)))
    absorcion_grano_l = grano_total_kg * 1.0
    agua_lavado_manual = vol_necesario_antes_hervir - (agua_macerado_manual - absorcion_grano_l)

    st.write("---")
    
    # 2. BALANCE DE AGUA DE LA ETAPA
    st.subheader("💧 Balance de Agua: Cocción")
    st.info(f"**Agua para la lavada del grano:** Necesitas pasar **{agua_lavado_manual:.1f} Litros** de agua caliente sobre el grano.")
    st.write(f"**Control de llenado:** Al juntar todo el líquido filtrado en la olla antes de encender el quemador principal, debes tener exactamente **{vol_necesario_antes_hervir:.1f} Litros**.")

    # 3. ANÁLISIS ENERGÉTICO DE LA ETAPA
    st.subheader("🔥 Análisis Energético y Sensor en Vivo: Cocción")
    st.write("Por la altura de Bogotá, tu mosto nunca va a pasar de los {temp_ebullicion} °C. Monit
