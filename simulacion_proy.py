import streamlit as st
import pandas as pd
import random
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

class ProyectoHidraulico:
    def __init__(self, nombre, cliente, duracion, monto):
        self.nombre = nombre
        self.cliente = cliente
        self.duracion = duracion  # en días
        self.monto = monto
        self.ganancia = self.calcular_ganancia()
        self.margen = round((self.ganancia / self.monto) * 100, 1) if self.monto > 0 else 0
    
    def calcular_ganancia(self):
        # Margen de ganancia entre 20-35%
        margen_porcentaje = random.uniform(20, 35)
        return round(self.monto * margen_porcentaje / 100)

class SimuladorProyectos:
    def __init__(self):
        self.proyectos = []
        self.dias_mes = 30
        self.margen_dias = 7  # ±7 días de margen
        
        # Datos reales de la tabla original (enero-marzo 2025)
        self.datos_reales = {
            'proyectos': [
                {'nombre': 'Reparación de unidad hidráulica de freno de molino SAG', 'cliente': 'Minera Colquiria S.A.', 'monto': 12800, 'estado': 'Finalizado'},
                {'nombre': 'Fabricación de manifold hidráulico para sistema de izaje', 'cliente': 'Constructora San José S.A.', 'monto': 9450, 'estado': 'Finalizado'},
                {'nombre': 'Proyecto de Reparación de Camión Lubricador', 'cliente': 'Transporte Pesado Cruz del Sur', 'monto': 5000, 'estado': 'Finalizado'},
                {'nombre': 'Proyecto de Mantenimiento Neumático Industrial', 'cliente': 'Cementos Pacasmayo S.A.A.', 'monto': 4500, 'estado': 'Finalizado'},
                {'nombre': 'Mantenimiento de central hidráulica móvil (chasis y válvulas)', 'cliente': 'Cosapi Minería S.A.C', 'monto': 7300, 'estado': 'Finalizado'},
                {'nombre': 'Reparación de gato hidráulico de 30T – Sucursal Zárate', 'cliente': 'Maestro Perú S.A. (SJL)', 'monto': 2700, 'estado': 'Entregado'},
                {'nombre': 'Suministro de unidad hidráulica para sistema de refrigeración de prensa', 'cliente': 'Minera Aurífera Retamas S.A.', 'monto': 14200, 'estado': 'En ejecución'},
                {'nombre': 'Diagnóstico y prueba de banco de válvulas direccionales', 'cliente': 'Haug S.A.', 'monto': 3500, 'estado': 'Entregado'},
                {'nombre': 'Mantenimiento de prensa hidráulica industrial – 100T', 'cliente': 'Metalurgia & Servicios EIRL', 'monto': 6800, 'estado': 'Finalizado'}
            ],
            'total_proyectos': 9,
            'total_ingresos': 65250,
            'periodo': '3 meses (enero-marzo 2025)',
            'promedio_mensual': 21750,  # 65250 / 3 meses
            'proyectos_por_mes': 3,  # 9 proyectos / 3 meses
            'monto_promedio_proyecto': 7250  # 65250 / 9 proyectos
        }
        
        # Datos base para generar proyectos realistas
        self.tipos_proyecto = [
            "Reparación de unidad hidráulica de freno",
            "Mantenimiento de sistema hidráulico de molino",
            "Fabricación de manifold hidráulico para izaje",
            "Reparación de gato hidráulico de 30T",
            "Mantenimiento de prensa hidráulica industrial",
            "Diagnóstico y prueba de banco de válvulas",
            "Reparación de bomba hidráulica de refrigeración",
            "Mantenimiento de central hidráulica móvil",
            "Suministro de unidad hidráulica para sistema",
            "Proyecto de reparación de camión lubricador"
        ]
        
        self.tipos_cliente = [
            "Minera", "Constructora", "Transporte", "Cementos", "Maestro Perú",
            "Metalurgia", "Cosapi", "Haug", "Aurífera", "Pesado Cruz"
        ]
        
        self.empresas = [
            "Colquiria S.A.", "San José S.A.", "Cruz del Sur", "Pacasmayo S.A.A.",
            "Minería S.A.C", "Perú S.A.", "Retamas S.A.", "S.A.", "& Servicios EIRL",
            "Sucursal Zárate", "SAG", "Industrial"
        ]
    
    def calcular_duracion_automatica(self, cantidad_proyectos):
        """Calcula la duración promedio automáticamente basada en la cantidad"""
        dias_objetivo = random.randint(self.dias_mes - self.margen_dias, 
                                     self.dias_mes + self.margen_dias)
        duracion_promedio = dias_objetivo / cantidad_proyectos
        return max(1, round(duracion_promedio))
    
    def generar_monto(self, duracion):
        """Genera monto basado en la duración del proyecto"""
        # Tarifa base por día: 400-800 soles
        tarifa_base = random.randint(400, 800)
        # Costo fijo adicional
        costo_fijo = random.randint(500, 2000)
        monto = duracion * tarifa_base + costo_fijo
        # Redondear a centenas
        return round(monto / 100) * 100
    
    def generar_proyectos(self, cantidad_proyectos, duracion_promedio=None):
        """Genera lista de proyectos"""
        self.proyectos = []
        
        # Si no se especifica duración, calcularla automáticamente
        if duracion_promedio is None:
            duracion_promedio = self.calcular_duracion_automatica(cantidad_proyectos)
        
        # Calcular días totales objetivo
        dias_objetivo = random.randint(self.dias_mes - self.margen_dias, 
                                     self.dias_mes + self.margen_dias)
        dias_restantes = dias_objetivo
        
        for i in range(cantidad_proyectos):
            # Generar duración con variación
            if i == cantidad_proyectos - 1:
                # Último proyecto: usar días restantes
                duracion = max(1, dias_restantes)
            else:
                # Variación del 40% sobre la duración promedio
                variacion = max(1, int(duracion_promedio * 0.4))
                duracion_min = max(1, duracion_promedio - variacion)
                duracion_max = duracion_promedio + variacion
                
                # No exceder días restantes
                dias_max_posible = max(1, dias_restantes // (cantidad_proyectos - i))
                duracion = min(random.randint(duracion_min, duracion_max), dias_max_posible)
                duracion = max(1, duracion)
            
            dias_restantes -= duracion
            
            # Generar datos del proyecto
            nombre = random.choice(self.tipos_proyecto)
            tipo_cliente = random.choice(self.tipos_cliente)
            empresa = random.choice(self.empresas)
            cliente = f"{tipo_cliente} {empresa}"
            monto = self.generar_monto(duracion)
            
            proyecto = ProyectoHidraulico(nombre, cliente, duracion, monto)
            self.proyectos.append(proyecto)
        
        return self.proyectos
    
    def obtener_resumen(self):
        """Obtiene resumen de los proyectos generados"""
        if not self.proyectos:
            return {}
        
        total_dias = sum(p.duracion for p in self.proyectos)
        total_ingresos = sum(p.monto for p in self.proyectos)
        total_ganancias = sum(p.ganancia for p in self.proyectos)
        margen_promedio = round((total_ganancias / total_ingresos) * 100, 1) if total_ingresos > 0 else 0
        duracion_promedio = round(total_dias / len(self.proyectos), 1)
        
        return {
            'total_proyectos': len(self.proyectos),
            'total_dias': total_dias,
            'total_ingresos': total_ingresos,
            'total_ganancias': total_ganancias,
            'margen_promedio': margen_promedio,
            'duracion_promedio': duracion_promedio,
            'ingreso_promedio': round(total_ingresos / len(self.proyectos)),
            'ganancia_promedio': round(total_ganancias / len(self.proyectos))
        }
    
    def obtener_comparacion_real(self):
        """Compara los proyectos simulados con los datos reales"""
        resumen_simulado = self.obtener_resumen()
        
        if not resumen_simulado:
            return {}
        
        real = self.datos_reales
        
        # Calcular diferencias
        diff_ingresos = resumen_simulado['total_ingresos'] - real['promedio_mensual']
        diff_proyectos = resumen_simulado['total_proyectos'] - real['proyectos_por_mes']
        diff_monto_promedio = resumen_simulado['ingreso_promedio'] - real['monto_promedio_proyecto']
        
        # Calcular porcentajes de variación
        var_ingresos = round((diff_ingresos / real['promedio_mensual']) * 100, 1) if real['promedio_mensual'] > 0 else 0
        var_proyectos = round((diff_proyectos / real['proyectos_por_mes']) * 100, 1) if real['proyectos_por_mes'] > 0 else 0
        var_monto_promedio = round((diff_monto_promedio / real['monto_promedio_proyecto']) * 100, 1) if real['monto_promedio_proyecto'] > 0 else 0
        
        return {
            'simulado': resumen_simulado,
            'real': real,
            'diferencias': {
                'ingresos': diff_ingresos,
                'proyectos': diff_proyectos,
                'monto_promedio': diff_monto_promedio
            },
            'variaciones': {
                'ingresos': var_ingresos,
                'proyectos': var_proyectos,
                'monto_promedio': var_monto_promedio
            }
        }
    
    def obtener_dataframe_real(self):
        """Convierte datos reales a DataFrame"""
        data = []
        for i, p in enumerate(self.datos_reales['proyectos'], 1):
            # Estimar duración basada en monto (para comparación visual)
            duracion_estimada = max(1, round(p['monto'] / 800))  # Usando tarifa promedio de 800/día
            
            data.append({
                'N°': i,
                'Proyecto': p['nombre'][:50] + '...' if len(p['nombre']) > 50 else p['nombre'],
                'Cliente': p['cliente'],
                'Duración Estimada (días)': duracion_estimada,
                'Monto (S/.)': f"S/. {p['monto']:,}",
                'Estado': p['estado']
            })
        
        return pd.DataFrame(data)
    
    def obtener_dataframe(self):
        """Convierte proyectos a DataFrame para mostrar en tabla"""
        if not self.proyectos:
            return pd.DataFrame()
        
        data = []
        for i, p in enumerate(self.proyectos, 1):
            data.append({
                'N°': i,
                'Proyecto': p.nombre,
                'Cliente': p.cliente,
                'Duración (días)': p.duracion,
                'Monto (S/.)': f"S/. {p.monto:,}",
                'Ganancia (S/.)': f"S/. {p.ganancia:,}",
                'Margen (%)': f"{p.margen}%"
            })
        
        return pd.DataFrame(data)

def main():
    st.set_page_config(
        page_title="Simulador de Proyectos Hidráulicos",
        page_icon="🔧",
        layout="wide"
    )
    
    # CSS personalizado
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #2C3E50, #3498DB);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stDataFrame {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔧 Simulador de Proyectos Hidráulicos</h1>
        <p style="color: white; text-align: center; margin: 0;">
            Optimiza tu planificación mensual de proyectos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar simulador
    if 'simulador' not in st.session_state:
        st.session_state.simulador = SimuladorProyectos()
        st.session_state.cantidad_anterior = 3
    
    # Controles en columnas
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.subheader("📊 Configuración")
        cantidad_proyectos = st.slider(
            "Cantidad de Proyectos por Mes:",
            min_value=1,
            max_value=8,
            value=3,
            key="cantidad_slider"
        )
        
        # Detectar cambio en cantidad para ajustar duración automáticamente
        if cantidad_proyectos != st.session_state.cantidad_anterior:
            nueva_duracion = st.session_state.simulador.calcular_duracion_automatica(cantidad_proyectos)
            st.session_state.duracion_promedio = nueva_duracion
            st.session_state.cantidad_anterior = cantidad_proyectos
        
        # Inicializar duración si no existe
        if 'duracion_promedio' not in st.session_state:
            st.session_state.duracion_promedio = st.session_state.simulador.calcular_duracion_automatica(cantidad_proyectos)
    
    with col2:
        st.subheader("⏱️ Duración Automática")
        duracion_promedio = st.slider(
            "Duración Promedio por Proyecto (días):",
            min_value=1,
            max_value=20,
            value=st.session_state.duracion_promedio,
            key="duracion_slider"
        )
        
        st.info(f"💡 Duración ajustada automáticamente a {st.session_state.duracion_promedio} días para {cantidad_proyectos} proyectos")
    
    with col3:
        st.subheader("🚀 Generar")
        if st.button("Generar Nuevos Proyectos", type="primary"):
            with st.spinner("Generando proyectos..."):
                st.session_state.simulador.generar_proyectos(cantidad_proyectos, duracion_promedio)
                st.success("¡Proyectos generados exitosamente!")
    
    # Generar proyectos iniciales
    if not st.session_state.simulador.proyectos:
        st.session_state.simulador.generar_proyectos(cantidad_proyectos, duracion_promedio)
    
    # Mostrar resumen
    resumen = st.session_state.simulador.obtener_resumen()
    
    if resumen:
        st.subheader("📈 Resumen del Mes")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🗓️ Total de Días",
                value=f"{resumen['total_dias']} días",
                delta=f"{resumen['total_dias'] - 30} vs mes ideal"
            )
        
        with col2:
            st.metric(
                label="💰 Ingresos Totales",
                value=f"S/. {resumen['total_ingresos']:,}",
                delta=f"S/. {resumen['ingreso_promedio']:,} promedio"
            )
        
        with col3:
            st.metric(
                label="📊 Ganancias Totales",
                value=f"S/. {resumen['total_ganancias']:,}",
                delta=f"{resumen['margen_promedio']}% margen"
            )
        
        with col4:
            st.metric(
                label="⏰ Duración Promedio",
                value=f"{resumen['duracion_promedio']} días",
                delta=f"{resumen['total_proyectos']} proyectos"
            )
    
    # Comparación con datos reales
    st.subheader("🔍 Comparación con Datos Reales")
    comparacion = st.session_state.simulador.obtener_comparacion_real()
    
    if comparacion:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Simulación vs Realidad")
            
            # Crear DataFrame para comparación
            datos_comparacion = pd.DataFrame({
                'Métrica': ['Ingresos Mensuales', 'Proyectos por Mes', 'Monto Promedio por Proyecto'],
                'Datos Reales': [
                    f"S/. {comparacion['real']['promedio_mensual']:,}",
                    f"{comparacion['real']['proyectos_por_mes']} proyectos",
                    f"S/. {comparacion['real']['monto_promedio_proyecto']:,}"
                ],
                'Simulación': [
                    f"S/. {comparacion['simulado']['total_ingresos']:,}",
                    f"{comparacion['simulado']['total_proyectos']} proyectos",
                    f"S/. {comparacion['simulado']['ingreso_promedio']:,}"
                ],
                'Variación (%)': [
                    f"{comparacion['variaciones']['ingresos']:+.1f}%",
                    f"{comparacion['variaciones']['proyectos']:+.1f}%",
                    f"{comparacion['variaciones']['monto_promedio']:+.1f}%"
                ]
            })
            
            st.dataframe(datos_comparacion, hide_index=True, use_container_width=True)
            
            # Indicadores de performance
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                color_ingresos = "normal" if abs(comparacion['variaciones']['ingresos']) <= 20 else "inverse"
                st.metric(
                    "💰 Variación Ingresos",
                    f"{comparacion['variaciones']['ingresos']:+.1f}%",
                    delta=f"S/. {comparacion['diferencias']['ingresos']:+,}"
                )
            
            with col_b:
                color_proyectos = "normal" if abs(comparacion['variaciones']['proyectos']) <= 30 else "inverse"
                st.metric(
                    "📈 Variación Proyectos",
                    f"{comparacion['variaciones']['proyectos']:+.1f}%",
                    delta=f"{comparacion['diferencias']['proyectos']:+.0f} proyectos"
                )
            
            with col_c:
                color_monto = "normal" if abs(comparacion['variaciones']['monto_promedio']) <= 25 else "inverse"
                st.metric(
                    "💎 Variación Monto Prom.",
                    f"{comparacion['variaciones']['monto_promedio']:+.1f}%",
                    delta=f"S/. {comparacion['diferencias']['monto_promedio']:+,}"
                )
        
        with col2:
            st.markdown("### 📋 Información de Datos Reales")
            st.info(f"""
            **Período de Referencia:** {comparacion['real']['periodo']}
            
            **Resumen Real:**
            - 🏢 Total de proyectos: {comparacion['real']['total_proyectos']}
            - 💰 Ingresos totales: S/. {comparacion['real']['total_ingresos']:,}
            - 📊 Promedio mensual: S/. {comparacion['real']['promedio_mensual']:,}
            - 🎯 Proyectos por mes: {comparacion['real']['proyectos_por_mes']}
            - 💎 Monto promedio: S/. {comparacion['real']['monto_promedio_proyecto']:,}
            """)
            
            # Semáforo de precisión
            precision_score = 100 - (abs(comparacion['variaciones']['ingresos']) + 
                                   abs(comparacion['variaciones']['proyectos']) + 
                                   abs(comparacion['variaciones']['monto_promedio'])) / 3
            
            if precision_score >= 80:
                st.success(f"🎯 **Excelente precisión:** {precision_score:.1f}% - Tu simulación está muy cerca de la realidad")
            elif precision_score >= 60:
                st.warning(f"⚠️ **Buena precisión:** {precision_score:.1f}% - Simulación aceptable con algunas diferencias")
            else:
                st.error(f"🔄 **Ajuste necesario:** {precision_score:.1f}% - Considera ajustar los parámetros")
    
    # Mostrar datos reales en tabla
    with st.expander("📊 Ver Tabla de Proyectos Reales (Enero-Marzo 2025)"):
        df_real = st.session_state.simulador.obtener_dataframe_real()
        st.dataframe(df_real, hide_index=True, use_container_width=True)
        
        st.markdown("**Fuente:** Datos reales de proyectos hidráulicos de enero-marzo 2025")
        
        # Gráfico comparativo
        if comparacion:
            st.subheader("📈 Gráfico Comparativo: Simulación vs Realidad")
            
            # Preparar datos para el gráfico
            metricas = ['Ingresos Mensuales', 'Proyectos por Mes', 'Monto Promedio']
            valores_reales = [
                comparacion['real']['promedio_mensual'],
                comparacion['real']['proyectos_por_mes'] * 1000,  # Escalar para visualización
                comparacion['real']['monto_promedio_proyecto']
            ]
            valores_simulados = [
                comparacion['simulado']['total_ingresos'],
                comparacion['simulado']['total_proyectos'] * 1000,  # Escalar para visualización
                comparacion['simulado']['ingreso_promedio']
            ]
            
            fig_comparativo = go.Figure(data=[
                go.Bar(name='Datos Reales', x=metricas, y=valores_reales, marker_color='#e74c3c'),
                go.Bar(name='Simulación', x=metricas, y=valores_simulados, marker_color='#3498db')
            ])
            
            fig_comparativo.update_layout(
                barmode='group',
                title="Comparación Datos Reales vs Simulación",
                yaxis_title="Valores (S/. para montos, x1000 para proyectos)",
                showlegend=True
            )
            
            st.plotly_chart(fig_comparativo, use_container_width=True)
            
            st.caption("📝 Los proyectos por mes están multiplicados por 1000 para mejor visualización en el gráfico")
    
    # Tabla de proyectos
    st.subheader("📋 Detalle de Proyectos")
    df = st.session_state.simulador.obtener_dataframe()
    
    if not df.empty:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribución por Duración")
            duraciones = [p.duracion for p in st.session_state.simulador.proyectos]
            fig_duracion = px.histogram(
                x=duraciones,
                nbins=10,
                title="Días por Proyecto",
                labels={'x': 'Duración (días)', 'y': 'Cantidad de Proyectos'}
            )
            fig_duracion.update_layout(showlegend=False)
            st.plotly_chart(fig_duracion, use_container_width=True)
        
        with col2:
            st.subheader("💰 Distribución por Monto")
            montos = [p.monto for p in st.session_state.simulador.proyectos]
            fig_monto = px.histogram(
                x=montos,
                nbins=8,
                title="Montos por Proyecto",
                labels={'x': 'Monto (S/.)', 'y': 'Cantidad de Proyectos'}
            )
            fig_monto.update_layout(showlegend=False)
            st.plotly_chart(fig_monto, use_container_width=True)
        
        # Gráfico de barras comparativo
        st.subheader("🔄 Comparación Monto vs Ganancia por Proyecto")
        proyectos_nombres = [f"P{i+1}" for i in range(len(st.session_state.simulador.proyectos))]
        montos = [p.monto for p in st.session_state.simulador.proyectos]
        ganancias = [p.ganancia for p in st.session_state.simulador.proyectos]
        
        fig_comparacion = go.Figure(data=[
            go.Bar(name='Monto', x=proyectos_nombres, y=montos),
            go.Bar(name='Ganancia', x=proyectos_nombres, y=ganancias)
        ])
        fig_comparacion.update_layout(
            barmode='group',
            title="Comparación Monto vs Ganancia",
            xaxis_title="Proyectos",
            yaxis_title="Soles (S/.)"
        )
        st.plotly_chart(fig_comparacion, use_container_width=True)
    
    # Información adicional
    with st.expander("ℹ️ Información del Modelo"):
        st.markdown("""
        ### 🔧 Características del Simulador:
        
        **Ajuste Automático:**
        - Al cambiar la cantidad de proyectos, la duración se ajusta automáticamente
        - Mantiene el objetivo de ~30 días de trabajo mensual (±7 días de margen)
        
        **Cálculo de Montos:**
        - Tarifa base: 400-800 soles por día
        - Costo fijo adicional: 500-2,000 soles por proyecto
        - Montos redondeados a centenas
        
        **Sistema de Ganancias:**
        - Margen de ganancia: 20-35% sobre el monto total
        - Ganancias proporcionales al tiempo y complejidad
        
        **Datos Realistas:**
        - Basado en proyectos hidráulicos reales del sector minero e industrial
        - Nombres de clientes y proyectos similares a la tabla original
        
        ### 📊 Comparación con Datos Reales:
        
        **Período de Referencia:** Enero-Marzo 2025 (9 proyectos, S/. 65,250 total)
        
        **Métricas de Referencia:**
        - 📈 Promedio mensual: S/. 21,750
        - 🎯 Proyectos por mes: 3
        - 💰 Monto promedio por proyecto: S/. 7,250
        
        **Indicadores de Precisión:**
        - 🟢 Verde (80-100%): Excelente precisión
        - 🟡 Amarillo (60-79%): Buena precisión
        - 🔴 Rojo (<60%): Necesita ajustes
        
        **Cómo Interpretar:**
        - Variaciones ±20% en ingresos son normales
        - Variaciones ±30% en cantidad de proyectos son aceptables
        - Variaciones ±25% en monto promedio indican buena calibración
        """)
        
        # Añadir tabla de proyectos reales resumida
        st.markdown("### 📋 Resumen de Proyectos Reales:")
        proyectos_resumen = pd.DataFrame({
            'Estado': ['Finalizado', 'Entregado', 'En ejecución'],
            'Cantidad': [6, 2, 1],
            'Monto Total': ['S/. 44,850', 'S/. 6,200', 'S/. 14,200'],
            'Porcentaje': ['68.7%', '9.5%', '21.8%']
        })
        st.dataframe(proyectos_resumen, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    main()