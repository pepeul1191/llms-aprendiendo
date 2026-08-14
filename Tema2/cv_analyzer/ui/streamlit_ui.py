import streamlit as st
from models.cv_model import AnalisisCV
from services.pdf_processor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato

def main():
    """Función principal que define la interfaz de usuario de Streamlit"""
    
    st.set_page_config(
        page_title="Sistema de Evaluación de CVs",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📄 Sistema de Evaluación de CVs con IA")
    st.markdown("""
    **Analiza currículums y evalúa candidatos de manera objetiva usando IA**
    
    Este sistema utiliza inteligencia artificial para:
    - Extraer información clave de currículums en PDF
    - Analizar la experiencia y habilidades del candidato
    - Evaluar el ajuste al puesto específico
    - Proporcionar recomendaciones objetivas de contratación
    """)
    
    st.divider()
    
    col_entrada, col_resultado = st.columns([1, 1], gap="large")
    
    with col_entrada:
        procesar_entrada()
    
    with col_resultado:
        mostrar_area_resultados()

def procesar_entrada():
    """Maneja la entrada de datos del usuario"""
    
    st.header("📋 Datos de Entrada")
    
    archivo_cv = st.file_uploader(
        "**1. Sube el CV del candidato (PDF)**",
        type=['pdf'],
        help="Selecciona un archivo PDF que contenga el currículum a evaluar. Asegúrate de que el texto sea legible y no esté en formato de imagen."
    )
    
    if archivo_cv is not None:
        st.success(f"✅ Archivo cargado: {archivo_cv.name}")
        st.info(f"📊 Tamaño: {archivo_cv.size:,} bytes")
    
    st.markdown("---")
    
    st.markdown("**2. Descripción del puesto de trabajo**")
    descripcion_puesto = st.text_area(
        "Detalla los requisitos, responsabilidades y habilidades necesarias:",
        height=250,
        placeholder="""Ejemplo detallado:

**Puesto:** Desarrollador Frontend Senior

**Requisitos obligatorios:**
- 3+ años de experiencia en desarrollo frontend
- Dominio de React.js y JavaScript/TypeScript
- Experiencia con HTML5, CSS3 y frameworks CSS (Bootstrap, Tailwind)
- Conocimiento de herramientas de build (Webpack, Vite)

**Requisitos deseables:**
- Experiencia con Next.js o similares
- Conocimientos de testing (Jest, Cypress)
- Familiaridad con metodologías ágiles
- Inglés intermedio-avanzado

**Responsabilidades:**
- Desarrollo de interfaces de usuario responsivas
- Colaboración con equipos de diseño y backend
- Optimización de rendimiento de aplicaciones web
- Mantenimiento de código legacy""",
        help="Sé específico sobre requisitos técnicos, experiencia requerida y responsabilidades del puesto."
    )
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    
    with col_btn1:
        analizar = st.button(
            "🔍 Analizar Candidato", 
            type="primary",
            use_container_width=True
        )
    
    with col_btn2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.rerun()
    
    st.session_state['archivo_cv'] = archivo_cv
    st.session_state['descripcion_puesto'] = descripcion_puesto
    st.session_state['analizar'] = analizar

def mostrar_area_resultados():
    """Muestra el área de resultados del análisis"""
    
    st.header("📊 Resultado del Análisis")
    
    if st.session_state.get('analizar', False):
        archivo_cv = st.session_state.get('archivo_cv')
        descripcion_puesto = st.session_state.get('descripcion_puesto', '').strip()
        
        if archivo_cv is None:
            st.error("⚠️ Por favor sube un archivo PDF con el currículum")
            return
            
        if not descripcion_puesto:
            st.error("⚠️ Por favor proporciona una descripción detallada del puesto")
            return
        
        procesar_analisis(archivo_cv, descripcion_puesto)
    else:
        st.info("""
        👆 **Instrucciones:**
        
        1. Sube un CV en formato PDF en la columna izquierda
        2. Describe detalladamente el puesto de trabajo
        3. Haz clic en "Analizar Candidato"
        4. Aquí aparecerá el análisis completo del candidato
        
        **Consejos para mejores resultados:**
        - Usa CVs con texto seleccionable (no imágenes escaneadas)
        - Sé específico en la descripción del puesto
        - Incluye tanto requisitos obligatorios como deseables
        """)

def procesar_analisis(archivo_cv, descripcion_puesto):
    """Procesa el análisis completo del CV"""
    
    with st.spinner("🔄 Procesando currículum..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("📄 Extrayendo texto del PDF...")
        progress_bar.progress(25)
        
        texto_cv = extraer_texto_pdf(archivo_cv)
        
        if texto_cv.startswith("Error"):
            st.error(f"❌ {texto_cv}")
            return
        
        status_text.text("🤖 Preparando análisis con IA...")
        progress_bar.progress(50)
        
        status_text.text("📊 Analizando candidato...")
        progress_bar.progress(75)
        
        resultado = evaluar_candidato(texto_cv, descripcion_puesto)
        
        status_text.text("✅ Análisis completado")
        progress_bar.progress(100)
        
        progress_bar.empty()
        status_text.empty()
        
        mostrar_resultados(resultado)

def mostrar_resultados(resultado: AnalisisCV):
    """Muestra los resultados del análisis de manera estructurada y profesional"""
    
    st.subheader("🎯 Evaluación Principal")
    
    if resultado.porcentaje_ajuste >= 80:
        color = "🟢"
        nivel = "EXCELENTE"
        mensaje = "Candidato altamente recomendado"
    elif resultado.porcentaje_ajuste >= 60:
        color = "🟡"
        nivel = "BUENO"
        mensaje = "Candidato recomendado con reservas"
    elif resultado.porcentaje_ajuste >= 40:
        color = "🟠"
        nivel = "REGULAR"
        mensaje = "Candidato requiere evaluación adicional"
    else:
        color = "🔴"
        nivel = "BAJO"
        mensaje = "Candidato no recomendado"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric(
            label="Porcentaje de Ajuste al Puesto",
            value=f"{resultado.porcentaje_ajuste}%",
            delta=f"{color} {nivel}"
        )
        st.markdown(f"**{mensaje}**")
    
    st.divider()
    
    st.subheader("👤 Perfil del Candidato")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**👨‍💼 Nombre:** {resultado.nombre_candidato}")
        st.info(f"**⏱️ Experiencia:** {resultado.experiencia_años} años")
    
    with col2:
        st.info(f"**🎓 Educación:** {resultado.education}")
    
    st.subheader("💼 Experiencia Relevante")
    st.info(f"📋 **Resumen de experiencia:**\n\n{resultado.experiencia_relevante}")
    
    st.divider()
    
    st.subheader("🛠️ Habilidades Técnicas Clave")
    if resultado.habilidades_clave:
        cols = st.columns(min(len(resultado.habilidades_clave), 4))
        for i, habilidad in enumerate(resultado.habilidades_clave):
            with cols[i % 4]:
                st.success(f"✅ {habilidad}")
    else:
        st.warning("No se identificaron habilidades técnicas específicas")
    
    st.divider()
    
    col_fortalezas, col_mejoras = st.columns(2)
    
    with col_fortalezas:
        st.subheader("💪 Fortalezas Principales")
        if resultado.fortalezas:
            for i, fortaleza in enumerate(resultado.fortalezas, 1):
                st.markdown(f"**{i}.** {fortaleza}")
        else:
            st.info("No se identificaron fortalezas específicas")
    
    with col_mejoras:
        st.subheader("📈 Áreas de Desarrollo")
        if resultado.areas_mejora:
            for i, area in enumerate(resultado.areas_mejora, 1):
                st.markdown(f"**{i}.** {area}")
        else:
            st.info("No se identificaron áreas de mejora específicas")
    
    st.divider()
    
    st.subheader("📋 Recomendación Final")
    
    if resultado.porcentaje_ajuste >= 70:
        st.success("""
        ✅ **CANDIDATO RECOMENDADO**
        
        El perfil del candidato está bien alineado con los requisitos del puesto. 
        Se recomienda proceder con las siguientes etapas del proceso de selección.
        """)
    elif resultado.porcentaje_ajuste >= 50:
        st.warning("""
        ⚠️ **CANDIDATO CON POTENCIAL**
        
        El candidato muestra potencial pero requiere evaluación adicional. 
        Se recomienda una entrevista técnica para validar competencias específicas.
        """)
    else:
        st.error("""
        ❌ **CANDIDATO NO RECOMENDADO**
        
        El perfil no se alinea suficientemente con los requisitos del puesto. 
        Se recomienda continuar la búsqueda de candidatos más adecuados.
        """)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Guardar Análisis", use_container_width=True):
            st.info("Funcionalidad de guardado - En desarrollo")