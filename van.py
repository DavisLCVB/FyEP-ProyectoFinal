import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def calcular_van(inversion_inicial, flujos_caja, tasa_descuento, periodos):
    """
    Calcula el Valor Actual Neto (VAN)
    
    Args:
        inversion_inicial (float): Inversión inicial del proyecto
        flujos_caja (list): Lista de flujos de caja por período
        tasa_descuento (float): Tasa de descuento (como decimal)
        periodos (list): Lista de períodos
    
    Returns:
        tuple: (VAN, flujos_descontados, detalles_calculo)
    """
    flujos_descontados = []
    detalles_calculo = []
    
    for i, flujo in enumerate(flujos_caja):
        periodo = i + 1
        factor_descuento = (1 + tasa_descuento) ** periodo
        flujo_descontado = flujo / factor_descuento
        flujos_descontados.append(flujo_descontado)
        
        detalles_calculo.append({
            'Período': periodo,
            'Flujo de Caja': flujo,
            'Factor de Descuento': factor_descuento,
            'Flujo Descontado': flujo_descontado
        })
    
    van = -inversion_inicial + sum(flujos_descontados)
    
    return van, flujos_descontados, detalles_calculo

def calcular_tir(inversion_inicial, flujos_caja, max_iter=1000, precision=1e-6):
    """
    Calcula la Tasa Interna de Retorno (TIR) usando el método de Newton-Raphson
    """
    def van_funcion(tasa):
        van = -inversion_inicial
        for i, flujo in enumerate(flujos_caja):
            van += flujo / ((1 + tasa) ** (i + 1))
        return van
    
    def derivada_van(tasa):
        derivada = 0
        for i, flujo in enumerate(flujos_caja):
            derivada += -flujo * (i + 1) / ((1 + tasa) ** (i + 2))
        return derivada
    
    # Estimación inicial
    tasa = 0.1
    
    for _ in range(max_iter):
        van_actual = van_funcion(tasa)
        if abs(van_actual) < precision:
            return tasa
        
        derivada = derivada_van(tasa)
        if abs(derivada) < precision:
            return None  # No se puede calcular
        
        tasa_nueva = tasa - van_actual / derivada
        
        if abs(tasa_nueva - tasa) < precision:
            return tasa_nueva
        
        tasa = tasa_nueva
    
    return None  # No convergió

def main():
    st.set_page_config(
        page_title="Calculadora VAN - Valor Actual Neto",
        page_icon="💰",
        layout="wide"
    )
    
    st.title("💰 Calculadora de Valor Actual Neto (VAN)")
    st.markdown("---")
    
    # Sidebar para parámetros principales
    st.sidebar.header("⚙️ Parámetros del Proyecto")
    
    # Inversión inicial
    inversion_inicial = st.sidebar.number_input(
        "💵 Inversión Inicial ($)",
        min_value=0.0,
        value=100000.0,
        step=1000.0,
        help="Monto de la inversión inicial del proyecto"
    )
    
    # Tasa de descuento
    tasa_descuento_pct = st.sidebar.number_input(
        "📈 Tasa de Descuento (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
        help="Tasa de descuento anual para el proyecto"
    )
    tasa_descuento = tasa_descuento_pct / 100
    
    # Tipo de período
    tipo_periodo = st.sidebar.selectbox(
        "📅 Tipo de Período",
        ["Anual", "Mensual"],
        help="Selecciona si los flujos de caja son anuales o mensuales"
    )
    
    # Ajustar tasa para períodos mensuales
    if tipo_periodo == "Mensual":
        tasa_periodo = (1 + tasa_descuento) ** (1/12) - 1
        st.sidebar.info(f"Tasa mensual equivalente: {tasa_periodo*100:.3f}%")
    else:
        tasa_periodo = tasa_descuento
    
    # Número de períodos
    num_periodos = st.sidebar.number_input(
        f"🔢 Número de {tipo_periodo.lower()}s",
        min_value=1,
        max_value=50,
        value=5,
        step=1
    )
    
    st.sidebar.markdown("---")
    
    # Sección principal para flujos de caja
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💸 Flujos de Caja por Período")
        
        # Inicializar flujos de caja en session_state
        if 'flujos_caja' not in st.session_state:
            st.session_state.flujos_caja = [0.0] * num_periodos
        
        # Ajustar el tamaño de la lista si cambia el número de períodos
        if len(st.session_state.flujos_caja) != num_periodos:
            if len(st.session_state.flujos_caja) < num_periodos:
                # Agregar períodos
                st.session_state.flujos_caja.extend([0.0] * (num_periodos - len(st.session_state.flujos_caja)))
            else:
                # Reducir períodos
                st.session_state.flujos_caja = st.session_state.flujos_caja[:num_periodos]
        
        # Crear inputs para cada período
        flujos_caja = []
        
        # Organizar en columnas para mejor visualización
        cols_per_row = 3
        for i in range(0, num_periodos, cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < num_periodos:
                    periodo_num = i + j + 1
                    with cols[j]:
                        flujo = st.number_input(
                            f"Período {periodo_num}",
                            value=st.session_state.flujos_caja[i + j],
                            step=1000.0,
                            key=f"flujo_{periodo_num}"
                        )
                        flujos_caja.append(flujo)
                        st.session_state.flujos_caja[i + j] = flujo
        
        # Botones de ayuda
        st.markdown("### 🔧 Herramientas Rápidas")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("📈 Flujos Crecientes"):
                flujo_base = st.sidebar.number_input("Flujo base", value=20000.0)
                crecimiento = st.sidebar.number_input("Crecimiento %", value=5.0) / 100
                for i in range(num_periodos):
                    st.session_state.flujos_caja[i] = flujo_base * ((1 + crecimiento) ** i)
                st.rerun()
        
        with col_btn2:
            if st.button("📊 Flujos Uniformes"):
                flujo_uniforme = st.sidebar.number_input("Flujo uniforme", value=25000.0)
                for i in range(num_periodos):
                    st.session_state.flujos_caja[i] = flujo_uniforme
                st.rerun()
        
        with col_btn3:
            if st.button("🗑️ Limpiar Todo"):
                for i in range(num_periodos):
                    st.session_state.flujos_caja[i] = 0.0
                st.rerun()
    
    with col2:
        st.header("📊 Resultados")
        
        # Calcular VAN
        van, flujos_descontados, detalles_calculo = calcular_van(
            inversion_inicial, flujos_caja, tasa_periodo, list(range(1, num_periodos + 1))
        )
        
        # Mostrar resultados principales
        st.metric("💰 VAN", f"${van:,.2f}", delta=None)
        
        if van > 0:
            st.success("✅ Proyecto RENTABLE")
        elif van < 0:
            st.error("❌ Proyecto NO RENTABLE")
        else:
            st.warning("⚠️ Proyecto en punto de equilibrio")
        
        # Calcular TIR
        tir = calcular_tir(inversion_inicial, flujos_caja)
        if tir is not None:
            st.metric("📈 TIR", f"{tir*100:.2f}%")
            if tir > tasa_descuento:
                st.success("✅ TIR > Tasa de descuento")
            else:
                st.error("❌ TIR < Tasa de descuento")
        else:
            st.warning("⚠️ No se pudo calcular la TIR")
        
        # Período de recuperación simple
        flujos_acumulados = np.cumsum([-inversion_inicial] + flujos_caja)
        periodo_recuperacion = None
        for i, flujo_acum in enumerate(flujos_acumulados):
            if flujo_acum > 0:
                periodo_recuperacion = i
                break
        
        if periodo_recuperacion is not None:
            st.metric("⏱️ Período de Recuperación", f"{periodo_recuperacion} {tipo_periodo.lower()}s")
        else:
            st.metric("⏱️ Período de Recuperación", "No se recupera")
    
    # Tabla de detalles
    st.markdown("---")
    st.header("📋 Detalle de Cálculos")
    
    df_detalles = pd.DataFrame(detalles_calculo)
    df_detalles['Flujo de Caja'] = df_detalles['Flujo de Caja'].apply(lambda x: f"${x:,.2f}")
    df_detalles['Factor de Descuento'] = df_detalles['Factor de Descuento'].apply(lambda x: f"{x:.4f}")
    df_detalles['Flujo Descontado'] = df_detalles['Flujo Descontado'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(df_detalles, use_container_width=True)
    
    # Gráficos
    st.markdown("---")
    st.header("📈 Visualizaciones")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        # Gráfico de flujos de caja
        fig1 = go.Figure()
        
        periodos = list(range(0, num_periodos + 1))
        flujos_totales = [-inversion_inicial] + flujos_caja
        
        fig1.add_trace(go.Bar(
            x=periodos,
            y=flujos_totales,
            name="Flujos de Caja",
            marker_color=['red' if x < 0 else 'green' for x in flujos_totales]
        ))
        
        fig1.update_layout(
            title="Flujos de Caja por Período",
            xaxis_title="Período",
            yaxis_title="Flujo de Caja ($)",
            showlegend=False
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_graf2:
        # Gráfico de flujos acumulados
        flujos_acumulados = np.cumsum(flujos_totales)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=periodos,
            y=flujos_acumulados,
            mode='lines+markers',
            name="Flujos Acumulados",
            line=dict(color='blue', width=3)
        ))
        
        fig2.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Punto de Equilibrio")
        
        fig2.update_layout(
            title="Flujos de Caja Acumulados",
            xaxis_title="Período",
            yaxis_title="Flujo Acumulado ($)",
            showlegend=False
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Análisis de sensibilidad
    st.markdown("---")
    st.header("🔍 Análisis de Sensibilidad")
    
    with st.expander("Ver Análisis de Sensibilidad de la Tasa de Descuento"):
        tasas_test = np.arange(0.01, 0.30, 0.01)
        vans_sensibilidad = []
        
        for tasa_test in tasas_test:
            tasa_test_periodo = (1 + tasa_test) ** (1/12) - 1 if tipo_periodo == "Mensual" else tasa_test
            van_test, _, _ = calcular_van(inversion_inicial, flujos_caja, tasa_test_periodo, list(range(1, num_periodos + 1)))
            vans_sensibilidad.append(van_test)
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=tasas_test * 100,
            y=vans_sensibilidad,
            mode='lines',
            name="VAN vs Tasa de Descuento",
            line=dict(color='purple', width=2)
        ))
        
        fig3.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="VAN = 0")
        fig3.add_vline(x=tasa_descuento_pct, line_dash="dash", line_color="blue", annotation_text="Tasa Actual")
        
        fig3.update_layout(
            title="Sensibilidad del VAN a la Tasa de Descuento",
            xaxis_title="Tasa de Descuento (%)",
            yaxis_title="VAN ($)"
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    # Información adicional
    st.markdown("---")
    st.info("""
    **📚 Información sobre el VAN:**
    
    - **VAN > 0**: El proyecto genera valor y es rentable
    - **VAN < 0**: El proyecto destruye valor y no es rentable  
    - **VAN = 0**: El proyecto está en el punto de equilibrio
    
    **🔍 Otros indicadores:**
    - **TIR**: Tasa que hace el VAN igual a cero
    - **Período de Recuperación**: Tiempo necesario para recuperar la inversión inicial
    """)

if __name__ == "__main__":
    main()