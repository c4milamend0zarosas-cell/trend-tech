import streamlit as st

st.title("Planificador Predictivo de Eco-Eficiencia")
st.write("Calcula los volumenes de agua exactos para tu lote basandote en tu meta de produccion.")
st.divider()

# ENTRADA PRINCIPAL GLOBAL
st.sidebar.header("Meta de Produccion")
cerveza_deseada = st.sidebar.number_input("Litros de cerveza terminada que deseas obtener (L):", value=50.0, step=5.0)

# Pestañas del proceso (Sin emojis)
tab1, tab2, tab3 = st.tabs(["Planificacion Global", "Maceracion", "Ebullicion y Enfriamiento"])

# VARIABLES FIJAS DE INGENIERIA (Configuradas para Bogota)
# Rendimiento promedio: 1 kg de grano por cada 5 litros de cerveza de densidad estándar
grano_estimado_kg = cerveza_deseada / 5.0 
absorcion_grano_l_per_kg = 1.0 # El grano retiene 1L de agua por cada kg
tasa_evaporacion_bogota = 0.09 # 9% por hora debido a la altitud
tiempo_hervor_estandar = 60.0 # minutos
perdida_enfriamiento_trub = 1.02 # 2% de contraccion y retencion de lodos

# CALCULOS DE BALANCES INVERSOS
vol_necesario_antes_enfriar = cerveza_deseada * perdida_enfriamiento_trub
vol_necesario_antes_hervir = vol_necesario_antes_enfriar / (1.0 - (tasa_evaporacion_bogota * (tiempo_hervor_estandar / 60.0)))
agua_macerado_teorica = grano_estimado_kg * 3.0 # Relacion comun 3L agua / 1kg malta
agua_lavado_teorica = vol_necesario_antes_hervir - (agua_macerado_teorica - (grano_estimado_kg * absorcion_grano_l_per_kg))
agua_total_proceso = agua_macerado_teorica + agua_lavado_teorica

with tab1:
    st.header("Resumen del Balance de Agua Requerido")
    st.write(f"Para obtener **{cerveza_deseada:.1f} Litros** de cerveza final en Bogota, la planta debe ingresar un total de:")
    
    st.metric(label="AGUA TOTAL DE PROCESO REQUERIDA", value=f"{agua_total_proceso:.1f} Litros")
    
    st.write("---")
    st.subheader("Distribucion de Agua por Etapas")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.metric(label="1. Agua para Maceracion", value=f"{agua_macerado_teorica:.1f} L")
    with col_l2:
        st.metric(label="2. Agua para Lavado de Grano", value=f"{agua_lavado_teorica:.1f} L")
        
    st.caption("Nota: Este calculo previene de forma exacta que te quedes corto de volumen al final de la jornada o que hiervas agua de mas consumiendo gas innecesario.")

with tab2:
    st.header("Instrucciones para la Maceracion")
    st.write(f"1. Mide exactamente **{agua_macerado_teorica:.1f} Litros** de agua e ingresalos a tu olla de macerado.")
    st.write(f"2. Agrega los **{grano_estimado_kg:.1f} kg** de malta molida cuando el agua este a la temperatura objetivo.")
    
    tipo_olla = st.selectbox("Material de tu olla de macerado:", ["Acero Inoxidable", "Aluminio", "Cava plastica"])
    if tipo_olla == "Cava plastica":
        st.success("Excelente aislamiento. Tapa la olla y no enciendas el fuego durante los 60 minutos.")
    else:
        st.warning("Control manual de temperatura: No dejes la llama encendida. Aplica pulsos termicos de candela al nivel minimo durante solo 1 minuto cada 15 minutos.")

with tab3:
    st.header("Instrucciones de Ebullicion y Enfriamiento")
    
    st.subheader("Etapa de Ebullicion")
    st.write(f"1. Al finalizar el filtrado, debes tener en tu olla exactamente **{vol_necesario_antes_hervir:.1f} Litros** de mosto antes de encender el quemador.")
    st.write("2. **Nivel de Candela - Calentamiento:** Enciende el fogon al **Nivel Maximo (100% de potencia)** hasta alcanzar los 92.7 grados Celsius (Punto de ebullicion en Bogota).")
    st.write(f"3. **Nivel de Candela - Hervor Sostenido:** Apenas empiece a hervir, disminuye de inmediato la potencia de la candela al **Nivel Medio-Bajo (40% de potencia)** y sostenlo estrictamente durante **{tiempo_hervor_estandar:.0f} minutos**.")
    st.write(f"4. Al apagar el fuego, tu volumen final en la olla debe ser de **{vol_necesario_antes_enfriar:.1f} Litros** (se habran evaporado {vol_necesario_antes_hervir - vol_necesario_antes_enfriar:.1f} L de agua de forma controlada).")
    
    st.write("---")
    st.subheader("Etapa de Enfriamiento y Sostenibilidad")
    agua_enfriamiento_necesaria = vol_necesario_antes_enfriar * 3.0
    st.write(f"Para enfriar este lote, circularan **{agua_enfriamiento_necesaria:.1f} Litros** de agua limpia por tu intercambiador.")
    
    st.info("Estrategia Eco-Brew: Almacena esa agua caliente en un tanque de reserva. No requiere tratamiento y servira para el lavado de tu planta el dia de manana. Esto reduce el indicador global de consumo de la fabrica de 8:1 a un eficiente 4:1.")
    
    # Modelo de Ahorro Financiero por candela optimizada
    ahorro_gas_m3 = 0.4 * (tiempo_hervor_est
