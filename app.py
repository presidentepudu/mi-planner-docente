import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Planner Docente V11", layout="wide", page_icon="🦌")

def aplicar_estilos():
    tema = st.session_state.get('tema', 'Hacker (Matrix)')
    
    if tema == 'Hacker (Matrix)':
        st.markdown("""
        <style>
        .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
        div[data-testid="stMarkdownContainer"] p, h1, h2, h3, h4, span, label { color: #00ff41 !important; }
        .stButton>button { background-color: #0d0208; color: #00ff41; border: 1px solid #00ff41; }
        section[data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #00ff41; }
        input, textarea, select, div[data-baseweb="select"] > div { background-color: #111 !important; color: #00ff41 !important; border-color: #00ff41 !important; }
        div[data-testid="stExpander"] { background-color: #0a0a0a; border: 1px solid #00ff41; }
        div[data-testid="stTabs"] button { color: #00ff41 !important; } 
        </style>
        """, unsafe_allow_html=True)
        
    elif tema == 'Pastel':
        st.markdown("""
        <style>
        .stApp { background-color: #fffaf0; color: #5c5c5c; }
        h1, h2, h3, h4, p, label, span { color: #5c5c5c !important; }
        section[data-testid="stSidebar"] > div { background-color: #e6e6fa !important; }
        section[data-testid="stSidebar"] { background-color: #e6e6fa !important; }
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span { color: #5c5c5c !important; }
        .stButton>button { background-color: #ffd1dc; color: black; border-radius: 15px; border: none; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);}
        div[data-testid="stExpander"] { background-color: #fff5f8; border-radius: 10px; border: 1px solid #f0dae0; }
        div[data-baseweb="select"] > div, input, textarea { background-color: #fff0f5 !important; color: #5c5c5c !important; border-color: #dcd0ff !important; }
        div[data-baseweb="select"] span { color: #5c5c5c !important; }
        div[data-testid="stFileUploader"] section { background-color: #f3eaff !important; border: 1px dashed #dcd0ff; }
        div[data-testid="stFileUploader"] button { background-color: #dcd0ff !important; color: #5c5c5c !important; border: none; }
        div[data-testid="stFileUploader"] svg { color: #9370db !important; }
        </style>
        """, unsafe_allow_html=True)
        
    elif tema == 'Claro (Oficina)':
        st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: #31333F; }
        h1, h2, h3, h4, p, label, span { color: #31333F !important; }
        section[data-testid="stSidebar"] > div { background-color: #f8f9fa !important; }
        section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6;}
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] p { color: #31333F !important; }
        div[data-baseweb="select"] > div, input, textarea { background-color: #ffffff !important; color: #31333F !important; border-color: #cccccc !important; }
        </style>
        """, unsafe_allow_html=True)

def mostrar_pudu():
    nombre_imagen = "scout.png"
    if os.path.exists(nombre_imagen):
        st.sidebar.image(nombre_imagen, use_container_width=True)
    else:
        st.sidebar.warning(f"⚠️ No encuentro '{nombre_imagen}' en GitHub/Carpeta.")
        st.sidebar.markdown("---")

# ==========================================
# 2. INICIALIZACIÓN DE DATOS
# ==========================================
if 'datos_cursos' not in st.session_state:
    st.session_state.datos_cursos = {
        "7mo Básico": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "8vo Básico": pd.DataFrame(columns=["Nombre", "Nota 1"]),
    }

if 'datos_decimas' not in st.session_state:
    st.session_state.datos_decimas = {}

if 'planificacion' not in st.session_state:
    st.session_state.planificacion = []

# --- NUEVAS LISTAS PARA LA TESIS ---
if 'tesis_papers' not in st.session_state:
    st.session_state.tesis_papers = [] # Aquí van los papers

if 'tesis_tareas' not in st.session_state:
    st.session_state.tesis_tareas = [] # Aquí van las notas/tareas

if 'tema' not in st.session_state:
    st.session_state.tema = 'Hacker (Matrix)'

if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

aplicar_estilos()

# ==========================================
# 3. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.title("Sistema Docente")
    mostrar_pudu()
    
    seleccion = st.radio(
        "Navegación:", 
        ["Inicio", "Mis Cursos", "Planificación", "Tesis", "Configuración"],
        index=["Inicio", "Mis Cursos", "Planificación", "Tesis", "Configuración"].index(st.session_state.pagina_actual)
    )
    
    if seleccion != st.session_state.pagina_actual:
        st.session_state.pagina_actual = seleccion
        st.rerun()

# ==========================================
# 4. LÓGICA DE PÁGINAS
# ==========================================

# --- INICIO ---
if st.session_state.pagina_actual == "Inicio":
    st.title(f"👋 Bienvenido, Profesor")
    st.markdown("### Tu centro de comando personal.")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎓 **Mis Cursos**")
        if st.button("Ir a Cursos", use_container_width=True):
            st.session_state.pagina_actual = "Mis Cursos"
            st.rerun()
    with col2:
        st.warning("📅 **Agenda**")
        if st.button("Ir a Planificación", use_container_width=True):
            st.session_state.pagina_actual = "Planificación"
            st.rerun()
    with col3:
        st.success("📚 **Tesis**")
        if st.button("Ir a Tesis", use_container_width=True):
            st.session_state.pagina_actual = "Tesis"
            st.rerun()

# --- MIS CURSOS (SIMPLIFICADO Y ROBUSTO) ---
elif st.session_state.pagina_actual == "Mis Cursos":
    st.title("📂 Gestión de Cursos")
    
    lista_cursos = list(st.session_state.datos_cursos.keys())
    if not lista_cursos:
        st.warning("Crea un curso primero.")
        curso_actual = None
    else:
        col_sel, col_del = st.columns([3, 1])
        with col_sel:
            curso_actual = st.selectbox("Selecciona Curso:", lista_cursos)
        with col_del:
            st.write("")
            if st.button("🗑️ Borrar Curso"):
                del st.session_state.datos_cursos[curso_actual]
                if curso_actual in st.session_state.datos_decimas:
                    del st.session_state.datos_decimas[curso_actual]
                st.rerun()

    with st.expander("➕ Crear Nuevo Curso"):
        nombre_nuevo = st.text_input("Nombre:")
        if st.button("Crear") and nombre_nuevo:
            st.session_state.datos_cursos[nombre_nuevo] = pd.DataFrame(columns=["Nombre", "Nota 1"])
            st.rerun()

    if curso_actual:
        st.write("---")
        df_curso = st.session_state.datos_cursos[curso_actual]
        
        # SINCRONIZACIÓN DÉCIMAS
        if curso_actual not in st.session_state.datos_decimas:
             st.session_state.datos_decimas[curso_actual] = pd.DataFrame(index=df_curso.index, columns=["Décimas"]).fillna(0)
        
        df_decimas = st.session_state.datos_decimas[curso_actual]
        
        if len(df_curso) > len(df_decimas):
            filas_faltantes = len(df_curso) - len(df_decimas)
            nuevas_filas = pd.DataFrame({"Décimas": [0]*filas_faltantes})
            df_decimas = pd.concat([df_decimas, nuevas_filas], ignore_index=True)
        elif len(df_curso) < len(df_decimas):
             df_decimas = df_decimas.iloc[:len(df_curso)]
        
        # --- INTERFAZ ---
        col_notas, col_decimas = st.columns([3, 1])
        
        with col_notas:
            st.subheader(f"Planilla: {curso_actual}")
            c_up, c_add = st.columns([2,1])
            with c_up:
                uploaded_file = st.file_uploader("Cargar CSV", type=["csv"], label_visibility="collapsed")
            with c_add:
                if st.button("➕ Columna Nota"):
                    nuevo_num = len([c for c in df_curso.columns if "Nota" in c]) + 1
                    df_curso[f"Nota {nuevo_num}"] = 0.0
                    st.rerun()

            if uploaded_file:
                try:
                    df_nuevo = pd.read_csv(uploaded_file)
                    # Normalización de nombres
                    if "Nombre" not in df_nuevo.columns and "Estudiante" in df_nuevo.columns:
                        df_nuevo.rename(columns={"Estudiante": "Nombre"}, inplace=True)
                    
                    # Limpieza de comas decimales
                    for col in df_nuevo.columns:
                        if "Nota" in col and df_nuevo[col].dtype == object:
                            df_nuevo[col] = df_nuevo[col].astype(str).str.replace(',', '.')

                    st.session_state.datos_cursos[curso_actual] = df_nuevo
                    st.success("Importado correctamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error CSV: {e}")

            # Configuración Flexible
            column_cfg = {"Nombre": st.column_config.TextColumn(disabled=False, width="medium")}
            for col in df_curso.columns:
                if "Nota" in col:
                    column_cfg[col] = st.column_config.NumberColumn(min_value=1.0, max_value=7.0, step=0.1, format="%.1f")

            df_editado = st.data_editor(
                df_curso,
                column_config=column_cfg,
                num_rows="dynamic",
                use_container_width=True,
                key=f"editor_main_{curso_actual}"
            )
            st.session_state.datos_cursos[curso_actual] = df_editado

        with col_decimas:
            st.subheader("Décimas")
            st.write("") 
            st.write("") 
            st.write("") 
            
            df_dec_editado = st.data_editor(
                df_decimas,
                column_config={
                    "Décimas": st.column_config.NumberColumn(label="Ganadas", step=1, min_value=0, max_value=50, format="%d 🌟")
                },
                use_container_width=True,
                num_rows="fixed",
                key=f"editor_dec_{curso_actual}"
            )
            st.session_state.datos_decimas[curso_actual] = df_dec_editado

# --- PLANIFICACIÓN ---
elif st.session_state.pagina_actual == "Planificación":
    st.title("📅 Agenda Docente")
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Agendar Nuevo")
        fecha_obj = st.date_input("Selecciona Fecha", value=date.today())
        act = st.text_input("Actividad")
        tag = st.selectbox("Etiqueta", ["Clase", "Reunión", "Tesis", "Personal", "Urgente"])
        
        if st.button("Guardar Evento") and act:
            st.session_state.planificacion.append({
                "fecha": str(fecha_obj), 
                "titulo": act, 
                "tipo": tag
            })
            st.success("Evento agendado")
            st.rerun()
            
        if st.button("Limpiar Todo"):
            st.session_state.planificacion = []
            st.rerun()
            
    with c2:
        st.subheader("Próximos Eventos")
        if not st.session_state.planificacion:
            st.info("No tienes eventos pendientes.")
        else:
            df_plan = pd.DataFrame(st.session_state.planificacion)
            if "fecha" not in df_plan.columns:
                df_plan["fecha"] = str(date.today())
            
            df_plan = df_plan.sort_values("fecha")
            
            for index, row in df_plan.iterrows():
                emoji = "📌"
                if row['tipo'] == "Tesis": emoji = "🎓"
                if row['tipo'] == "Urgente": emoji = "🔥"
                
                with st.expander(f"{row['fecha']} | {emoji} {row['titulo']}"):
                    col_a, col_b = st.columns([4, 1])
                    col_a.markdown(f"**Tipo:** {row['tipo']}")
                    if col_b.button("Borrar", key=f"del_plan_{index}"):
                        item = {"fecha": row['fecha'], "titulo": row['titulo'], "tipo": row['tipo']}
                        if item in st.session_state.planificacion:
                            st.session_state.planificacion.remove(item)
                            st.rerun()

# --- TESIS (AHORA CON DOS PESTAÑAS) ---
elif st.session_state.pagina_actual == "Tesis":
    st.title("🎓 Tesis & Avances")
    
    # CREAMOS LAS DOS PESTAÑAS
    tab_tareas, tab_papers = st.tabs(["📝 Bitácora y Tareas", "📚 Bibliografía (Papers)"])

    # --- PESTAÑA 1: TAREAS Y NOTAS ---
    with tab_tareas:
        st.subheader("Lista de Pendientes")
        c_t1, c_t2 = st.columns([3, 1])
        with c_t1:
            nueva_tarea = st.text_input("Nueva tarea o nota rápida:", placeholder="Ej: Corregir introducción, enviar correo...")
        with c_t2:
            st.write("")
            st.write("")
            if st.button("Agregar Tarea") and nueva_tarea:
                st.session_state.tesis_tareas.append({"tarea": nueva_tarea, "hecho": False})
                st.rerun()
        
        st.write("---")
        if not st.session_state.tesis_tareas:
            st.info("No hay tareas pendientes. ¡A avanzar!")
        else:
            for i, t in enumerate(st.session_state.tesis_tareas):
                col_check, col_txt, col_del = st.columns([0.5, 4, 1])
                
                # Checkbox para marcar como hecho
                is_done = col_check.checkbox("", value=t['hecho'], key=f"chk_tarea_{i}")
                if is_done != t['hecho']:
                    st.session_state.tesis_tareas[i]['hecho'] = is_done
                    st.rerun()
                
                # Texto tachado si está listo
                if t['hecho']:
                    col_txt.markdown(f"~~{t['tarea']}~~")
                else:
                    col_txt.markdown(t['tarea'])
                
                if col_del.button("🗑️", key=f"del_tarea_{i}"):
                    st.session_state.tesis_tareas.pop(i)
                    st.rerun()

    # --- PESTAÑA 2: PAPERS ---
    with tab_papers:
        st.subheader("Registro de Lecturas")
        with st.expander("➕ Agregar Nuevo Paper", expanded=False):
            tit = st.text_input("Título del Paper")
            res = st.text_area("Tus notas / Resumen personal")
            if st.button("Guardar Paper"):
                st.session_state.tesis_papers.append({"titulo": tit, "resumen": res, "leido": False})
                st.rerun()
            
        st.write("---")
        if not st.session_state.tesis_papers:
            st.info("Aún no has agregado papers.")
        
        for i, p in enumerate(st.session_state.tesis_papers):
            # Icono dinámico
            estado = "✅ LEÍDO" if p['leido'] else "⏳ POR LEER"
            color_estado = "green" if p['leido'] else "orange"
            
            with st.expander(f"📄 {p['titulo']}  [{estado}]"):
                st.markdown(f"**Resumen:**")
                st.write(p['resumen'])
                
                c_p1, c_p2 = st.columns([1, 1])
                with c_p1:
                    # Checkbox para marcar leído
                    leido = st.checkbox("Marcar como Leído", value=p['leido'], key=f"paper_check_{i}")
                    if leido != p['leido']:
                        st.session_state.tesis_papers[i]['leido'] = leido
                        st.rerun()
                with c_p2:
                    if st.button("Borrar Paper", key=f"del_paper_{i}"):
                        st.session_state.tesis_papers.pop(i)
                        st.rerun()

# --- CONFIGURACIÓN ---
elif st.session_state.pagina_actual == "Configuración":
    st.title("⚙️ Configuración")
    
    st.subheader("🎨 Tema Visual")
    tema_nuevo = st.selectbox("Elige tema:", ["Hacker (Matrix)", "Pastel", "Claro (Oficina)"], 
                              index=["Hacker (Matrix)", "Pastel", "Claro (Oficina)"].index(st.session_state.tema))
    
    if tema_nuevo != st.session_state.tema:
        st.session_state.tema = tema_nuevo
        st.rerun()

    st.write("---")
    st.subheader("💾 Respaldo")
    
    datos_exportar = {
        "cursos": {k: v.to_json() for k, v in st.session_state.datos_cursos.items()},
        "decimas_data": {k: v.to_json() for k, v in st.session_state.datos_decimas.items()},
        "planificacion": st.session_state.planificacion,
        "tesis_papers": st.session_state.tesis_papers, # Lista de papers
        "tesis_tareas": st.session_state.tesis_tareas, # Nueva lista de tareas
        "tema": st.session_state.tema
    }
    st.download_button("⬇️ Descargar Respaldo JSON", data=json.dumps(datos_exportar), file_name="respaldo_v11_tesis.json", mime="application/json")
    
    archivo = st.file_uploader("⬆️ Cargar Respaldo", type="json")
    if archivo:
        try:
            data = json.load(archivo)
            if "cursos" in data:
                nuevos_cursos = {}
                for k, v in data["cursos"].items():
                    df = pd.read_json(v)
                    for col in df.columns:
                        if "Nota" in col: 
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
                    nuevos_cursos[k] = df
                st.session_state.datos_cursos = nuevos_cursos

            if "decimas_data" in data:
                nuevas_decimas = {}
                for k, v in data["decimas_data"].items():
                    nuevas_decimas[k] = pd.read_json(v)
                st.session_state.datos_decimas = nuevas_decimas
            
            if "planificacion" in data: st.session_state.planificacion = data["planificacion"]
            
            # Carga inteligente de tesis (por si el respaldo es antiguo)
            if "tesis_papers" in data: 
                st.session_state.tesis_papers = data["tesis_papers"]
            elif "tesis" in data: # Compatibilidad con versiones viejas
                 st.session_state.tesis_papers = data["tesis"]

            if "tesis_tareas" in data: st.session_state.tesis_tareas = data["tesis_tareas"]
            if "tema" in data: st.session_state.tema = data["tema"]
            
            st.success("¡Sistema restaurado y actualizado!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
