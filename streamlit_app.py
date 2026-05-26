import streamlit as st

st.title("Eco-Brew Bogota")
st.subheader("Asistente de Eco-Eficiencia para Cerveceria Manual")
st.write("Optimiza agua y gas en tus ollas tradicionales a 2.600 msnm.")
st.divider()

# Pestañas del proceso (Sin emojis)
tab1, tab2, tab3 = st.tabs(["Maceracion", "Ebullicion", "Enfriamiento"])

with tab1:
    st.header("Optimizacion del Macerado")
    tipo_olla = st.selectbox("Material de tu olla:", ["Acero Inoxidable", "Aluminio", "Cava plastica"])
    
    if tipo_olla == "Cava plastica":
        st.success("Excelente aislamiento. No necesitas encender el fuego durante los 60 minutos.")
    else:
        st.warning("La olla pierde calor rapidamente por el clima de Bogota. Aplica pulsos termicos: enciende la candela al nivel minimo solo 1 minuto cada 15 minutos. No dejes el fuego encendido continuo.")

with tab2:
    st.header("Control de Evaporacion, Candela y Gas")
    
    # Inputs operativos
    vol_inicial = st.number_input("Litros de mosto antes de hervir (L):", value=100.0, step=10.0)
    tiempo_hervor = st.number_input("Minutos totales de hervor de la receta:", value=60.0, step=5.0)
    vol_final_real = st.number_input("Litros reales que quedaron al apagar el fuego (L):", value=85.0, step=5.0)
    
    # PARAMETROS DE INGENIERIA (Bogota)
    temp_ebullicion = 92.7
    tasa_evaporacion_ideal = 0.09 # 9% por hora
    costo_gas_por_m3 = 2700.0 # Valor promedio comercial en COP
    
    # CALCULOS DEL BALANCE DE MASA (AGUA)
    evaporacion_ideal_L = vol_inicial * tasa_evaporacion_ideal * (tiempo_hervor / 60.0)
    vol_final_teorico = vol_inicial - evaporacion_ideal_L
    
    st.info(f"Parametro Local: En Bogota tu mosto hierve a {temp_ebullicion} grados Celsius. No busques llegar a 100 grados Celsius.")
    
    st.write("---")
    st.subheader("Instrucciones de Tiempo y Nivel de Candela")
    
    st.write(f"1. **Etapa de Calentamiento:** Enciende la candela al **Nivel Maximo (100% de potencia)** hasta que el termometro marque {temp_ebullicion} grados Celsius.")
    st.write(f"2. **Etapa de Hervor Sostenido:** Apenas empiece la ebullicion, reduce de inmediato la candela al **Nivel Medio-Bajo (40% de potencia)** y mantenlo asi de forma fija durante los {tiempo_hervor:.0f} minutos del proceso. Esto es suficiente para mantener el hervor burbujeante sin sobre-evaporar.")
    
    st.write("---")
    st.subheader("Resultados del Balance Hidrico en Ebullicion")
    
    # Evaluacion del agua evaporada
    evaporacion_real = vol_inicial - vol_final_real
    
    if vol_final_real < vol_final_teorico:
        agua_desperdiciada = vol_final_teorico - vol_final_real
        st.error(f"Alerta de Desperdicio: Evaporaste {evaporacion_real:.1f} L. Lo ideal para la receta eran solo {evaporacion_ideal_L:.1f} L.")
        st.metric(label="Agua perdida en exceso (Vaporizado de mas)", value=f"{agua_desperdiciada:.1f} Litros")
    else:
        st.success("Control de evaporacion eficiente. Mantuviste los balances de agua dentro del rango ideal.")
        agua_desperdiciada = 0.0
        st.metric(label="Agua perdida en exceso", value="0.0 Litros")
        
    st.write("---")
    st.subheader("Estimacion de Ahorro Economico (Gas Natural)")
    
    # SIMULACION DE AHORRO DE ENERGIA (GAS VANTI)
    # Traducimos el exceso de agua evaporada a energia (Calor latente de vaporizacion = 2257 kJ/kg)
    # Asumiendo eficiencia del quemador artesanal del 40%, calculamos el ahorro de m3 de gas
    energia_exceso_kj = agua_desperdiciada * 2257.0
    m3_gas_desperdiciado = (energia_exceso_kj / 37000.0) / 0.40 # 37000 kJ es el poder calorifico del m3 de gas
    
    # Ahorro por reduccion de potencia de candela base fija (Ahorro estimado de 0.4 m3 por hora en modo eficiente)
    ahorro_base_m3 = 0.4 * (tiempo_hervor / 60.0)
    
    if agua_desperdiciada > 0:
        total_m3_ahorrado = ahorro_base_m3 + m3_gas_desperdiciado
    else:
        total_m3_ahorrado = ahorro_base_m3
        
    ahorro_cop = total_m3_ahorrado * costo_gas_por_m3
    
    col_eco1, col_eco2 = st.columns(2)
    with col_eco1:
        st.metric(label="Gas Natural Ahorrado", value=f"{total_m3_ahorrado:.2f} m3")
    with col_eco2:
        st.metric(label="Ahorro Economico Estimado", value=f"$ {ahorro_cop:,.0f} COP", delta="Reduccion de costos")
        
    st.caption("Nota: El ahorro economico aumenta proporcionalmente segun el tamano de tu lote y los excesos de llama alta controlados.")

with tab3:
    st.header("Recuperacion del Agua y Sostenibilidad Global")
    
    # Relacion estandar de enfriamiento manual
    agua_enfriamiento = vol_final_real * 3.0
    
    st.subheader("Balance de Enfriamiento")
    st.metric(label="Agua caliente limpia recuperable", value=f"{agua_enfriamiento:.1f} Litros")
    
    st.write("---")
    st.subheader("Indicador Ambiental del Negocio (Agua : Cerveza)")
    
    indicador_tradicional = (vol_inicial + agua_enfriamiento) / vol_final_real
    indicador_eco_brew = vol_inicial / vol_final_real
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Indicador Tradicional (Botando agua)", value=f"{indicador_tradicional:.1f} : 1", delta="Alto consumo", delta_color="inverse")
    with col2:
        st.metric(label="Indicador Eco-Brew (Reusando agua)", value=f"{indicador_eco_brew:.1f} : 1", delta="Eficiencia Optima")
        
    st.info("Argumento de sustentacion: Al recuperar los litros del agua de enfriamiento para las tareas de aseo del dia siguiente, el indicador global disminuye a la mitad, reduciendo drasticamente la huella hidrica de la planta.")
