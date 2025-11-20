import streamlit as st
import pandas as pd
import json

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Planner Docente V4", layout="wide", page_icon="🎓")

# Función para aplicar estilos
def aplicar_estilos():
    tema = st.session_state.get('tema', 'Hacker (Matrix)') # Por defecto Hacker
    
    if tema == 'Hacker (Matrix)':
        st.markdown("""
        <style>
        .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
        div[data-testid="stMarkdownContainer"] p { color: #00ff41 !important; }
        h1, h2, h3 { color: #00ff41 !important; }
        .stButton>button { background-color: #0d0208; color: #00ff41; border: 1px solid #00ff41; }
        input, textarea, select { background-color: #111 !important; color: #00ff41 !important; }
        div[data-testid="stExpander"] { background-color: #0a0a0a; border: 1px solid #00ff41; }
        </style>
        """, unsafe_allow_html=True)
    elif tema == 'Claro':
        # Estilos por defecto de Streamlit
        pass

# ==========================================
# 2. INICIALIZACIÓN DE DATOS
# ==========================================
if 'datos_cursos' not in st.session_state:
    # Estructura inicial con TUS cursos reales
    st.session_state.datos_cursos = {
        "7mo Básico": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "8vo Básico": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "Computación": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "Electivo Programación": pd.DataFrame(columns=["Nombre", "Nota 1"])
    }

# Estructura separada para Décimas (Nombre Estudiante -> Cantidad)
if 'decimas' not in st.session_state:
    st.session_state.decimas = {} 

if 'planificacion' not in st.session_state:
    st.session_state.planificacion = []

if 'tesis_papers' not in st.session_state:
    st.session_state.tesis_papers = []

if 'tema' not in st.session_state:
    st.session_state.tema = 'Hacker (Matrix)'

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

aplicar_estilos()

# ==========================================
# 3. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.title("💻 Sistema Docente")
    st.caption(f"Modo: {st.session_state.tema}")
    
    seleccion = st.radio(
        "Menú:", 
        ["Inicio", "Mis Cursos", "Gestor de Décimas", "Planificación", "Tesis", "Configuración"],
        index=["Inicio", "Mis Cursos", "Gestor de Décimas", "Planificación", "Tesis", "Configuración"].index(st.session_state.pagina_actual)
    )
    
    if seleccion != st.session_state.pagina_actual:
        st.session_state.pagina_actual = seleccion
        st.rerun()

# ==========================================
# 4. LÓGICA PRINCIPAL
# ==========================================

# --- INICIO ---
if st.session_state.pagina_actual == "Inicio":
    st.title("Bienvenido, Profesor Cristobal")
    st.success("Sistema cargado correctamente.")
    st.info("💡 Novedad: Ahora puedes subir archivos CSV y agregar columnas de notas dinámicamente.")

# --- MIS CURSOS ---
elif st.session_state.pagina_actual == "Mis Cursos":
    st.title("📂 Gestión de Cursos")
    
    # --- SELECTOR Y GESTIÓN DE CURSOS ---
    col_sel, col_act = st.columns([2, 1])
    
    with col_sel:
        lista_cursos = list(st.session_state.datos_cursos.keys())
        if not lista_cursos:
            st.warning("No tienes cursos. Crea uno nuevo.")
            curso_actual = None
        else:
            curso_actual = st.selectbox("Selecciona Curso:", lista_cursos)

    with col_act:
        # Botón para borrar curso actual
        if curso_actual and st.button("🗑️ Eliminar Curso Actual"):
            del st.session_state.datos_cursos[curso_actual]
            st.rerun()
    
    # --- CREAR NUEVO CURSO ---
    with st.expander("➕ Crear Nuevo Curso"):
        nombre_nuevo = st.text_input("Nombre del curso:")
        if st.button("Crear") and nombre_nuevo:
            st.session_state.datos_cursos[nombre_nuevo] = pd.DataFrame(columns=["Nombre", "Nota 1"])
            st.rerun()

    if curso_actual:
        st.markdown(f"### 📝 Planilla: {curso_actual}")
        df_curso = st.session_state.datos_cursos[curso_actual]

        # --- CARGA MASIVA (CSV) ---
        uploaded_file = st.file_uploader(f"📂 Cargar lista de estudiantes (CSV) para {curso_actual}", type=["csv"])
        if uploaded_file:
            try:
                # Cargar CSV
                df_nuevo = pd.read_csv(uploaded_file)
                # Asegurar que tenga columna Nombre
                if "Nombre" not in df_nuevo.columns and "Estudiante" in df_nuevo.columns:
                    df_nuevo.rename(columns={"Estudiante": "Nombre"}, inplace=True)
                
                st.session_state.datos_cursos[curso_actual] = df_nuevo
                st.success("¡Lista cargada exitosamente!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al leer CSV: {e}")

        # --- AGREGAR COLUMNAS DE NOTAS ---
        col_add, col_dummy = st.columns([1, 3])
        with col_add:
            if st.button("➕ Agregar Nueva Evaluación"):
                nuevo_num = len([c for c in df_curso.columns if "Nota" in c]) + 1
                df_curso[f"Nota {nuevo_num}"] = 0.0
                st.rerun()

        # --- CONFIGURAR EDITOR ---
        # Configuramos dinámicamente las columnas para que sean numéricas
        column_cfg = {"Nombre": st.column_config.TextColumn(disabled=False)}
        
        for col in df_curso.columns:
            if "Nota" in col:
                column_cfg[col] = st.column_config.NumberColumn(
                    label=col,
                    min_value=1.0, max_value=7.0, step=0.1, format="%.1f"
                )

        # --- EDITOR PRINCIPAL ---
        df_editado = st.data_editor(
            df_curso,
            column_config=column_cfg,
            use_container_width=True,
            num_rows="dynamic",
            key=f"editor_{curso_actual}"
        )
        
        # Guardar cambios
        st.session_state.datos_cursos[curso_actual] = df_editado

        # --- CÁLCULO PROMEDIOS ---
        st.write("---")
        if not df_editado.empty:
            cols_notas = [c for c in df_editado.columns if "Nota" in c]
            if cols_notas:
                df_prom = df_editado.copy()
                # Convertir a números por seguridad
                for c in cols_notas:
                    df_prom[c] = pd.to_numeric(df_prom[c], errors='coerce')
                
                # Calcular promedio ignorando ceros
                df_prom['Promedio'] = df_prom[cols_notas].replace(0, pd.NA).mean(axis=1).round(1)
                
                # Mostrar
                def color_rojo(val):
                     # Lógica segura para colorear
                     try:
                         if float(val) < 4.0: return 'color: #ff4b4b'
                     except: pass
                     return 'color: #00ff41' if st.session_state.tema == 'Hacker (Matrix)' else 'color: black'

                st.dataframe(df_prom[['Nombre', 'Promedio']].style.applymap(color_rojo, subset=['Promedio']), use_container_width=True)

# --- GESTOR DE DÉCIMAS ---
elif st.session_state.pagina_actual == "Gestor de Décimas":
    st.title("🌟 Banco de Décimas")
    st.info("Desacoplado de las notas. Agrega o quita décimas rápidamente.")

    # Seleccionar curso
    curso_sel = st.selectbox("Curso:", list(st.session_state.datos_cursos.keys()))
    
    if curso_sel:
        # Obtener lista de estudiantes de ese curso
        estudiantes = st.session_state.datos_cursos[curso_sel]['Nombre'].tolist()
        
        # Preparar DataFrame de décimas
        datos_decimas = []
        for est in estudiantes:
            # Buscar si ya tiene décimas, si no, 0
            val = st.session_state.decimas.get(f"{curso_sel}_{est}", 0)
            datos_decimas.append({"Estudiante": est, "Décimas": val})
        
        df_dec = pd.DataFrame(datos_decimas)
        
        # Editor especial para décimas
        df_dec_editado = st.data_editor(
            df_dec,
            column_config={
                "Estudiante": st.column_config.TextColumn(disabled=True),
                "Décimas": st.column_config.NumberColumn(
                    step=1, min_value=-10, max_value=50, format="%d 🌟"
                )
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Guardar cambios en el diccionario global
        for index, row in df_dec_editado.iterrows():
            clave = f"{curso_sel}_{row['Estudiante']}"
            st.session_state.decimas[clave] = row['Décimas']

# --- PLANIFICACIÓN ---
elif st.session_state.pagina_actual == "Planificación":
    st.title("📅 Planificador")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Agendar")
        dia = st.selectbox("Día", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
        act = st.text_input("Actividad")
        tag = st.selectbox("Etiqueta", ["Clase", "Reunión", "Tesis", "Personal"])
        if st.button("Guardar Evento") and act:
            st.session_state.planificacion.append({"dia": dia, "titulo": act, "tipo": tag})
            st.success("Guardado")
            st.rerun()
            
        if st.button("Limpiar Todo"):
            st.session_state.planificacion = []
            st.rerun()
            
    with c2:
        st.subheader("Semana")
        for d in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
            with st.expander(d, expanded=True):
                eventos = [e for e in st.session_state.planificacion if e['dia'] == d]
                for i, e in enumerate(eventos):
                    col_a, col_b = st.columns([4, 1])
                    col_a.markdown(f"**[{e['tipo']}]** {e['titulo']}")
                    if col_b.button("X", key=f"del_{d}_{i}"):
                        st.session_state.planificacion.remove(e)
                        st.rerun()

# --- TESIS ---
elif st.session_state.pagina_actual == "Tesis":
    st.title("🎓 Tesis & Papers")
    
    st.markdown("### 📝 Nuevo Registro")
    tit = st.text_input("Título Paper / Tarea")
    res = st.text_area("Resumen")
    if st.button("Guardar Paper"):
        st.session_state.tesis_papers.append({"titulo": tit, "resumen": res, "leido": False})
        st.rerun()
        
    st.write("---")
    for i, p in enumerate(st.session_state.tesis_papers):
        icon = "✅" if p['leido'] else "⏳"
        with st.expander(f"{icon} {p['titulo']}"):
            st.write(p['resumen'])
            if st.checkbox("Marcar Leído", value=p['leido'], key=f"p_{i}"):
                st.session_state.tesis_papers[i]['leido'] = True
                st.rerun()
            if st.button("Borrar", key=f"del_p_{i}"):
                st.session_state.tesis_papers.pop(i)
                st.rerun()

# --- CONFIGURACIÓN (RESPALDO ARREGLADO) ---
elif st.session_state.pagina_actual == "Configuración":
    st.title("⚙️ Configuración")
    
    # Selector de tema
    tema_nuevo = st.selectbox("Tema Visual", ["Hacker (Matrix)", "Claro"], 
                             index=0 if st.session_state.tema == 'Hacker (Matrix)' else 1)
    if tema_nuevo != st.session_state.tema:
        st.session_state.tema = tema_nuevo
        st.rerun()

    st.write("---")
    st.subheader("💾 Sistema de Respaldo (JSON)")
    
    # DESCARGAR
    datos_exportar = {
        "cursos": {k: v.to_json() for k, v in st.session_state.datos_cursos.items()},
        "decimas": st.session_state.decimas,
        "planificacion": st.session_state.planificacion,
        "tesis": st.session_state.tesis_papers,
        "tema": st.session_state.tema
    }
    st.download_button("⬇️ Descargar Respaldo", data=json.dumps(datos_exportar), file_name="respaldo_cristobal.json", mime="application/json")
    
    # SUBIR (CON CORRECCIÓN DE ERRORES)
    archivo = st.file_uploader("⬆️ Cargar Respaldo", type="json")
    if archivo:
        try:
            data = json.load(archivo)
            
            # Restaurar Cursos CONVERTIENDO NÚMEROS
            if "cursos" in data:
                nuevos_cursos = {}
                for nombre_curso, json_data in data["cursos"].items():
                    df = pd.read_json(json_data)
                    # Forzar que las columnas 'Nota X' sean números (float)
                    cols_notas = [c for c in df.columns if "Nota" in c]
                    for c in cols_notas:
                        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)
                    nuevos_cursos[nombre_curso] = df
                st.session_state.datos_cursos = nuevos_cursos
            
            # Restaurar resto de datos
            if "decimas" in data: st.session_state.decimas = data["decimas"]
            if "planificacion" in data: st.session_state.planificacion = data["planificacion"]
            if "tesis" in data: st.session_state.tesis_papers = data["tesis"]
            if "tema" in data: st.session_state.tema = data["tema"]
            
            st.success("¡Respaldo cargado sin errores!")
            st.rerun()
        except Exception as e:
            st.error(f"Error al cargar: {e}")
