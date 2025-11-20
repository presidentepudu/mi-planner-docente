import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS (TEMAS)
# ==========================================
st.set_page_config(page_title="Planner Docente Pro", layout="wide", page_icon="🎓")

# Inicializar estado de navegación si no existe
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

# --- GESTIÓN DE TEMAS (CSS) ---
def aplicar_estilos():
    tema = st.session_state.get('tema', 'Claro')
    
    css = ""
    if tema == 'Oscuro':
        css = """
        <style>
        .stApp { background-color: #0E1117; color: white; }
        div[data-testid="stMarkdownContainer"] { color: white; }
        </style>
        """
    elif tema == 'Pastel':
        css = """
        <style>
        .stApp { background-color: #fdf6e3; color: #586e75; }
        .stButton>button { background-color: #ffd1dc; color: black; border-radius: 20px; border: none;}
        div[data-testid="stExpander"] { background-color: #e6e6fa; border-radius: 10px; }
        </style>
        """
    elif tema == 'Hacker (Matrix)':
        css = """
        <style>
        .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
        div[data-testid="stMarkdownContainer"] p { color: #00ff41 !important; }
        h1, h2, h3 { color: #00ff41 !important; }
        .stButton>button { background-color: #0d0208; color: #00ff41; border: 1px solid #00ff41; }
        input, textarea { background-color: #111; color: #00ff41; }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 2. INICIALIZACIÓN DE DATOS (MEMORIA)
# ==========================================
if 'datos_cursos' not in st.session_state:
    # Estructura inicial vacía para cursos
    st.session_state.datos_cursos = {
        "1° Medio A": pd.DataFrame(columns=["Nombre", "Nota 1", "Nota 2", "Nota 3"]),
        "2° Medio B": pd.DataFrame(columns=["Nombre", "Nota 1", "Nota 2", "Nota 3"]),
        "3° Medio Electivo": pd.DataFrame(columns=["Nombre", "Nota 1", "Nota 2", "Nota 3"])
    }

if 'planificacion' not in st.session_state:
    # Lista de eventos: {'dia': 'Lunes', 'titulo': '...', 'tipo': 'Clase'}
    st.session_state.planificacion = []

if 'tesis_papers' not in st.session_state:
    # Lista de papers: {'titulo': '...', 'resumen': '...', 'leido': False}
    st.session_state.tesis_papers = []

if 'tema' not in st.session_state:
    st.session_state.tema = 'Claro'

# Aplicar el tema seleccionado
aplicar_estilos()

# ==========================================
# 3. BARRA LATERAL (NAVEGACIÓN)
# ==========================================
with st.sidebar:
    st.title("Panel de Control")
    
    # Menú de navegación manual
    seleccion = st.radio(
        "Ir a:", 
        ["Inicio", "Mis Cursos", "Planificación", "Tesis", "Configuración"],
        index=["Inicio", "Mis Cursos", "Planificación", "Tesis", "Configuración"].index(st.session_state.pagina_actual)
    )
    
    # Actualizar la página si se cambia en el sidebar
    if seleccion != st.session_state.pagina_actual:
        st.session_state.pagina_actual = seleccion
        st.rerun()

# ==========================================
# 4. LÓGICA DE LAS PÁGINAS
# ==========================================

# --- PÁGINA: INICIO ---
if st.session_state.pagina_actual == "Inicio":
    st.title(f"👋 Bienvenido, Profesor")
    st.markdown("### Tu centro de comando personal para la docencia y la investigación.")
    st.write("Este programa está diseñado para funcionar rápido, sin internet y adaptarse a tu flujo de trabajo.")
    
    st.write("---")
    
    # Botones de acceso rápido con colores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🎓 **Docencia**")
        st.write("Gestiona listas de cursos y notas.")
        if st.button("Ir a Mis Cursos", use_container_width=True):
            st.session_state.pagina_actual = "Mis Cursos"
            st.rerun()
            
    with col2:
        st.warning("📅 **Organización**")
        st.write("Tu semana laboral lunes a viernes.")
        if st.button("Ir a Planificación", use_container_width=True):
            st.session_state.pagina_actual = "Planificación"
            st.rerun()
            
    with col3:
        st.success("📚 **Investigación**")
        st.write("Resúmenes de papers y tareas.")
        if st.button("Ir a Tesis", use_container_width=True):
            st.session_state.pagina_actual = "Tesis"
            st.rerun()

# --- PÁGINA: MIS CURSOS ---
elif st.session_state.pagina_actual == "Mis Cursos":
    st.title("🎓 Mis Cursos y Notas")
    
    # Selector de Curso
    curso_actual = st.selectbox("Selecciona el curso:", list(st.session_state.datos_cursos.keys()))
    
    # Botón para agregar nuevo curso (opcional)
    with st.expander("➕ Agregar nuevo curso"):
        nuevo_curso = st.text_input("Nombre del nuevo curso")
        if st.button("Crear Curso") and nuevo_curso:
            if nuevo_curso not in st.session_state.datos_cursos:
                st.session_state.datos_cursos[nuevo_curso] = pd.DataFrame(columns=["Nombre", "Nota 1", "Nota 2", "Nota 3"])
                st.success(f"Curso {nuevo_curso} creado!")
                st.rerun()

    st.markdown(f"### Planilla de: {curso_actual}")
    st.caption("Las notas bajo 4.0 se marcarán en rojo. El promedio se calcula solo (si quieres).")
    
    # Obtener dataframe del curso seleccionado
    df_curso = st.session_state.datos_cursos[curso_actual]
    
    # Asegurar tipos de datos
    column_config = {
        "Nombre": st.column_config.TextColumn("Estudiante", width="medium", required=True),
        "Nota 1": st.column_config.NumberColumn("N1", min_value=1.0, max_value=7.0, step=0.1, format="%.1f"),
        "Nota 2": st.column_config.NumberColumn("N2", min_value=1.0, max_value=7.0, step=0.1, format="%.1f"),
        "Nota 3": st.column_config.NumberColumn("N3", min_value=1.0, max_value=7.0, step=0.1, format="%.1f"),
    }

    # Editor de Datos
    df_editado = st.data_editor(
        df_curso,
        num_rows="dynamic",
        column_config=column_config,
        use_container_width=True,
        key=f"editor_{curso_actual}"
    )
    
    # Guardar cambios en memoria
    st.session_state.datos_cursos[curso_actual] = df_editado
    
    # Mostrar promedios (Visualización simple)
    if not df_editado.empty:
        st.write("---")
        st.subheader("Vista Previa de Promedios")
        
        # Calculo simple para visualización
        cols_notas = [c for c in df_editado.columns if "Nota" in c]
        df_promedios = df_editado.copy()
        df_promedios[cols_notas] = df_promedios[cols_notas].apply(pd.to_numeric, errors='coerce')
        df_promedios['Promedio'] = df_promedios[cols_notas].mean(axis=1).round(1)
        
        # Estilizar: Rojo si es menor a 4.0
        def estilo_notas(val):
            if isinstance(val, float) or isinstance(val, int):
                color = '#ff4b4b' if val < 4.0 else '#90ee90' # Rojo o Verde suave
                return f'color: {color}; font-weight: bold'
            return ''

        st.dataframe(df_promedios.style.applymap(estilo_notas, subset=cols_notas + ['Promedio']), use_container_width=True)

# --- PÁGINA: PLANIFICACIÓN ---
elif st.session_state.pagina_actual == "Planificación":
    st.title("📅 Planificador Semanal")
    st.caption("Sin sábados ni domingos. Solo lo importante.")
    
    col_form, col_cal = st.columns([1, 2])
    
    with col_form:
        st.markdown("#### 📌 Nueva Actividad")
        dia_evento = st.selectbox("Día:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        titulo_evento = st.text_input("Actividad:")
        tipo_evento = st.selectbox("Etiqueta:", ["Clase", "Reunión", "Tesis", "Personal", "Urgente"])
        
        if st.button("Agendar"):
            if titulo_evento:
                st.session_state.planificacion.append({
                    "dia": dia_evento, 
                    "titulo": titulo_evento, 
                    "tipo": tipo_evento
                })
                st.success("Agendado")
                st.rerun()
                
        st.write("---")
        if st.button("🗑️ Borrar Todo el calendario"):
            st.session_state.planificacion = []
            st.rerun()

    with col_cal:
        st.markdown("#### 🗓️ Tu Semana")
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        
        # Colores por etiqueta
        colores = {
            "Clase": "blue", "Reunión": "orange", "Tesis": "purple", 
            "Personal": "green", "Urgente": "red"
        }
        
        cols = st.columns(5)
        for idx, dia in enumerate(dias_semana):
            with cols[idx]:
                st.markdown(f"**{dia}**")
                eventos_dia = [e for e in st.session_state.planificacion if e['dia'] == dia]
                
                if not eventos_dia:
                    st.markdown("*-Libre-*")
                
                for i, evento in enumerate(eventos_dia):
                    color = colores.get(evento['tipo'], "grey")
                    # Tarjeta de evento simulada
                    st.markdown(f"""
                    <div style="background-color: {color}; padding: 5px; border-radius: 5px; color: white; margin-bottom: 5px; font-size: 0.8em;">
                        {evento['titulo']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Opción pequeña para borrar individualmente
                    if st.button("x", key=f"del_{dia}_{i}", help=f"Borrar {evento['titulo']}"):
                        st.session_state.planificacion.remove(evento)
                        st.rerun()

# --- PÁGINA: TESIS ---
elif st.session_state.pagina_actual == "Tesis":
    st.title("📚 Bitácora de Investigación")
    
    tab1, tab2 = st.tabs(["📝 Nuevo Paper / Nota", "🗃️ Mis Resúmenes"])
    
    with tab1:
        st.write("Ingresa la información clave del paper. No subimos archivos, solo tus ideas.")
        t_titulo = st.text_input("Título del Paper / Tarea:")
        t_resumen = st.text_area("Resumen / Notas importantes:", height=150)
        
        if st.button("Guardar en Bitácora"):
            if t_titulo:
                st.session_state.tesis_papers.append({
                    "titulo": t_titulo,
                    "resumen": t_resumen,
                    "leido": False,
                    "fecha": datetime.now().strftime("%Y-%m-%d")
                })
                st.success("Guardado correctamente")
    
    with tab2:
        st.write(f"Tienes {len(st.session_state.tesis_papers)} registros.")
        
        for i, paper in enumerate(st.session_state.tesis_papers):
            # Contenedor visual para cada paper
            check_leido = "✅" if paper['leido'] else "⏳"
            with st.expander(f"{check_leido} {paper['titulo']} ({paper['fecha']})"):
                st.write(paper['resumen'])
                
                c1, c2 = st.columns([1, 4])
                # Checkbox para marcar como leído
                leido_status = c1.checkbox("Marcar Leído", value=paper['leido'], key=f"leido_{i}")
                if leido_status != paper['leido']:
                    st.session_state.tesis_papers[i]['leido'] = leido_status
                    st.rerun()
                
                if c2.button("Eliminar", key=f"elim_paper_{i}"):
                    st.session_state.tesis_papers.pop(i)
                    st.rerun()

# --- PÁGINA: CONFIGURACIÓN ---
elif st.session_state.pagina_actual == "Configuración":
    st.title("⚙️ Configuración & Datos")
    
    st.subheader("🎨 Temas Visuales")
    tema_seleccionado = st.selectbox(
        "Elige el aspecto de la aplicación:",
        ["Claro", "Oscuro", "Pastel", "Hacker (Matrix)"],
        index=["Claro", "Oscuro", "Pastel", "Hacker (Matrix)"].index(st.session_state.tema)
    )
    
    if tema_seleccionado != st.session_state.tema:
        st.session_state.tema = tema_seleccionado
        st.rerun()

    st.write("---")
    st.subheader("💾 Respaldo de Usuario")
    st.info("Para mantener tus datos seguros al cambiar de computador, usa estos botones. Funciona como tu 'Cuenta de Usuario'.")
    
    col_dl, col_ul = st.columns(2)
    
    with col_dl:
        # Lógica para empaquetar TODO en un solo archivo JSON
        datos_totales = {
            "cursos": {k: v.to_json() for k, v in st.session_state.datos_cursos.items()},
            "planificacion": st.session_state.planificacion,
            "tesis": st.session_state.tesis_papers,
            "tema": st.session_state.tema
        }
        json_str = json.dumps(datos_totales)
        
        st.download_button(
            label="⬇️ Descargar Respaldo (Mi Usuario)",
            data=json_str,
            file_name="respaldo_profe.json",
            mime="application/json",
            help="Guarda este archivo en tu correo o pendrive."
        )

    with col_ul:
        uploaded_file = st.file_uploader("⬆️ Cargar Respaldo Anterior", type="json")
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                
                # Restaurar Cursos
                if "cursos" in data:
                    st.session_state.datos_cursos = {k: pd.read_json(v) for k, v in data["cursos"].items()}
                
                # Restaurar Planificación
                if "planificacion" in data:
                    st.session_state.planificacion = data["planificacion"]
                    
                # Restaurar Tesis
                if "tesis" in data:
                    st.session_state.tesis_papers = data["tesis"]
                    
                # Restaurar Tema
                if "tema" in data:
                    st.session_state.tema = data["tema"]
                
                st.success("¡Sesión restaurada con éxito!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al cargar el archivo: {e}")
