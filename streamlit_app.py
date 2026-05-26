import streamlit as st

st.title("Simulador Predictivo de Eco-Eficiencia")
st.subheader("Asistente Digital para Cervecería Artesanal")
st.write("Optimiza el gasto de agua y gas en tus ollas tradicionales teniendo en cuenta el clima de Bogotá.")
st.divider()

# ENTRADAS MANUALES - EL CERVECERO ESCRIBE TODO EN SU LENGUAJE
st.sidebar.header("1. Metas de tu receta")
cerveza_deseada = st.sidebar.number_input("Litros de cerveza finales que quieres embotellar (L):", value=50.0, step=5.0)
tiempo_hervor = st.sidebar.number_input("Minutos totales que debe hervir el mosto (min):", value=60.0, step=5.0)

st.sidebar.header("2. Datos de tus ollas y equipos")
relacion_macerado = st.sidebar.number_input("¿Cuántos litros de agua usas por cada kilo de grano en la lavada inicial?:", value=3.0, step=0.5)
grano_por_litro = st.sidebar.number_input("¿Cuántos kilos de grano usas por cada litro de cerveza que produces? (kg/L):", value=0.2, step=0.05)
relacion_enfriamiento = st.sidebar.number_input("¿Cuántos litros de agua gastas para enfriar un solo litro de mosto caliente?:", value=3.0, step=0.5)

# VALORES DE REFERENCIA EN BOGOTÁ (Precios y clima)
tasa_evaporacion_bogota = 0.09 # El agua se evapora un 9% por hora por la altura de la ciudad
temp_ebullicion = 92.7 # Temperatura exacta a la que hierve el agua en Bogotá
costo_gas_m3 = 2700.0 # Precio promedio del gas comercial
costo_agua_litro = 6.5 # Precio promedio del litro de agua comercial

# CÁLCULOS INTERNOS DE AGUA (Hacia atrás desde el producto final)
grano_total_kg = cerveza_deseada * grano_por_litro
absorcion_grano_l = grano_total_kg * 1.0 # El grano absorbe siempre 1 litro por cada kilo

vol_necesario_antes_enfriar = cerveza_deseada * 1.02 # Se cuenta un 2% que se pierde en el fondo de la olla
vol_necesario_antes_hervir = vol_necesario_antes_enfriar / (1.0 - (tasa_evaporacion_bogota * (tiempo_hervor / 60.0)))

agua_macerado_manual = grano_total_kg * relacion_macerado
agua_lavado_manual = vol_necesario_antes_hervir - (agua_macerado_manual - absorcion_grano_l)
agua_total_proceso = agua_macerado_manual + agua_lavado_manual
agua_enfriamiento_total = vol_necesario_antes_enfriar * relacion_enfriamiento

# PESTAÑAS DE LA APLICACIÓN
tab1, tab2, tab3 = st.tabs(["Agua que debes medir", "Control del fuego", "Dinero y agua ahorrada"])

with tab1:
    st.header("Cantidad de agua exacta para iniciar")
    st.write(f"Para que al final te salgan exactamente {cerveza_deseada:.1f} Litros de cerveza, debes medir estas cantidades desde el principio:")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.metric(label="Agua para iniciar la Maceración", value=f"{agua_macerado_manual:.1f} Litros")
    with col_a2:
        st.metric(label="Agua para la Lavada del grano", value=f"{agua_lavado_manual:.1f} Litros")
        
    st.subheader("Total de agua para tus ollas")
    st.metric(label="Suma total de agua que debes usar en el día", value=f"{agua_total_proceso:.1f} Litros")

with tab2:
    st.header("Cómo controlar el fuego para ahorrar gas")
    st.write(f"Por la altura de Bogotá, tu mosto no va a subir de {temp_ebullicion} grados. No gastes gas intentando buscar los 100 grados. Sigue estos pasos:")
    st.write("---")
    st.write("1. **Para calentar el mosto:** Pon el fuego al **Máximo (100% de potencia)**.")
    st.write(f"2. **Al empezar a hervir:** Apenas veas las primeras burbujas y el termómetro marque {temp_ebullicion} grados, baja de inmediato el fuego al **Nivel Medio-Bajo (40% de potencia)**.")
    st.write(f"3. **Durante la cocción:** Mantén el fuego bajito de forma fija durante los {tiempo_hervor:.0f} minutos de tu receta. Ese calor es suficiente para mantener el hervor.")
    st.write(f"4. **Meta al apagar:** Al apagar el quemador, debes tener exactamente {vol_necesario_antes_enfriar:.1f} Litros dentro de la olla.")

with tab3:
    st.header("Ahorro real al reusar el agua de enfriamiento")
    st.write(f"Si guardas en un tanque limpio toda el agua caliente que sale de tu enfriador para usarla mañana en el aseo y lavado de equipos, logras este beneficio:")
    st.write("---")
    
    # Conversión a botellas de agua familiares
    botellas_ahorradas = agua_enfriamiento_total / 0.5
    st.subheader("Impacto en el medio ambiente")
    st.write(f"Evitas botar por el tubo del desagüe **{agua_enfriamiento_total:.1f} Litros** de agua limpia.")
    st.metric(label="Equivalente en botellas de agua de la tienda (500 mL)", value=f"{botellas_ahorradas:,.0f} Botellas")
    
    st.write("---")
    st.subheader("Ahorro económico para tu negocio")
    
    # Cuenta del dinero que se deja de pagar
    dinero_agua_ahorrado = agua_enfriamiento_total * costo_agua_litro
    ahorro_gas_m3 = 0.4 * (tiempo_hervor / 60.0)
    dinero_gas_ahorrado = ahorro_gas_m3 * costo_gas_m3
    total_dinero_ahorrado = dinero_agua_ahorrado + dinero_gas_ahorrado
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.write("**Dinero que te ahorras por separado:**")
        st.write(f"- Por reusar el agua del enfriador: $ {dinero_agua_ahorrado:,.0f} COP")
        st.write(f"- Por bajar el fuego a la mitad: $ {dinero_gas_ahorrado:,.0f} COP")
    with col_d2:
        st.metric(label="TOTAL DE DINERO QUE DEJAS DE PAGAR", value=f"$ {total_dinero_ahorrado:,.0f} COP")
        
    st.info("Mensaje para el jurado: Esta aplicación demuestra que la eco-eficiencia digital no requiere maquinaria costosa. Con solo organizar el uso del agua manualmente y controlar el fuego a tiempo, se reducen las facturas de servicios públicos.")
