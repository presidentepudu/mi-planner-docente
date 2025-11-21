import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
import os # Necesario para verificar si existe la imagen

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS (TEMAS CORREGIDOS)
# ==========================================
st.set_page_config(page_title="Planner Docente V10", layout="wide", page_icon="🦌")

def aplicar_estilos():
    tema = st.session_state.get('tema', 'Hacker (Matrix)')
    
    if tema == 'Hacker (Matrix)':
        st.markdown("""
        <style>
        /* === TEMA HACKER (Se mantiene igual) === */
        .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
        div[data-testid="stMarkdownContainer"] p, h1, h2, h3, h4, span, label { color: #00ff41 !important; }
        .stButton>button { background-color: #0d0208; color: #00ff41; border: 1px solid #00ff41; }
        section[data-testid="stSidebar"] { background-color: #0a0a0a !important; border-right: 1px solid #00ff41; }
        input, textarea, select, div[data-baseweb="select"] > div { background-color: #111 !important; color: #00ff41 !important; border-color: #00ff41 !important; }
        div[data-testid="stExpander"] { background-color: #0a0a0a; border: 1px solid #00ff41; }
        </style>
        """, unsafe_allow_html=True)
        
    elif tema == 'Pastel':
        st.markdown("""
        <style>
        /* === TEMA PASTEL (Corregido) === */
        .stApp { background-color: #fffaf0; color: #5c5c5c; }
        h1, h2, h3, h4, p, label, span { color: #5c5c5c !important; }
        
        /* Menú lateral lavanda */
        section[data-testid="stSidebar"] > div { background-color: #e6e6fa !important; }
        section[data-testid="stSidebar"] { background-color: #e6e6fa !important; }
        /* Asegurar que el texto del menú lateral sea oscuro */
        section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span { color: #5c5c5c !important; }

        /* Botones y Expanders */
        .stButton>button { background-color: #ffd1dc; color: black; border-radius: 15px; border: none; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);}
        div[data-testid="stExpander"] { background-color: #fff5f8; border-radius: 10px; border: 1px solid #f0dae0; }

        /* --- CORRECCIÓN DE ELEMENTOS OSCUROS --- */
        div[data-baseweb="select"] > div, input, textarea {
            background-color: #fff0f5 !important;
            color: #5c5c5c !important;
            border-color: #dcd0ff !important;
        }
        div[data-baseweb="select"] span { color: #5c5c5c !important; }

        div[data-testid="stFileUploader"] section {
            background-color: #f3eaff !important;
            border: 1px dashed #dcd0ff;
        }
        div[data-testid="stFileUploader"] button {
             background-color: #dcd0ff !important;
             color: #5c5c5c !important;
             border: none;
        }
        div[data-testid="stFileUploader"] svg { color: #9370db !important; }
        </style>
        """, unsafe_allow_html=True)
        
    elif tema == 'Claro (Oficina)':
        st.markdown("""
        <style>
        /* === TEMA CLARO OFICINA (Corregido) === */
        .stApp { background-color: #ffffff; color: #31333F; }
        h1, h2, h3, h4, p, label, span { color: #31333F !important; }
        
        /* Menú lateral gris claro */
        section[data-testid="stSidebar"] > div { background-color: #f8f9fa !important; }
        section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6;}
        
        /* Forzamos texto oscuro en el sidebar */
        section[data-testid="stSidebar"] label, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p { 
            color: #31333F !important; 
        }
        
        div[data-baseweb="select"] > div, input, textarea {
            background-color: #ffffff !important;
            color: #31333F !important;
            border-color: #cccccc !important;
        }
        </style>
        """, unsafe_allow_html=True)

# FUNCIÓN DEL NUEVO PUDÚ (IMAGEN PNG)
def mostrar_pudu():
    # Nombre del archivo que guardaste
    nombre_imagen = "scout.png"
    
    # Verificamos si la imagen existe en la carpeta antes de mostrarla
    if os.path.exists(nombre_imagen):
        # Mostramos la imagen centrada en la barra lateral
        st.sidebar.image(nombre_imagen, use_container_width=True)
    else:
        # Si no la encuentra (útil para debugging), muestra un aviso
        st.sidebar.warning(f"⚠️ No encuentro '{nombre_imagen}'. Asegúrate de subirla a GitHub en la misma carpeta que app.py")
        st.sidebar.markdown("---") # Separador

# ==========================================
# 2. INICIALIZACIÓN DE DATOS
# ==========================================
if 'datos_cursos' not in st.session_state:
    st.session_state.datos_cursos = {
        "7mo Básico": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "8vo Básico": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "Computación": pd.DataFrame(columns=["Nombre", "Nota 1"]),
        "Electivo Programación": pd.DataFrame(columns=["Nombre", "Nota 1"])
    }

if 'datos_decimas' not in st.session_state:
    st.session_state.datos_decimas = {}

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
    st.title("Sistema Docente")
    # AQUI SE MUESTRA LA IMAGEN DEL PUDÚ TRIBAL
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
    st.write("Selecciona una opción rápida para comenzar:")
    
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🎓 **Mis Cursos**")
        st.write("Notas y Décimas en una sola vista.")
        if st.button("Ir a Cursos", use_container_width=True):
            st.session_state.pagina_actual = "Mis Cursos"
            st.rerun()
            
    with col2:
        st.warning("📅 **Agenda**")
        st.write("Planificador semanal sin fines de semana.")
        if st.button("Ir a Planificación", use_container_width=True):
            st.session_state.pagina_actual = "Planificación"
            st.rerun()
            
    with col3:
        st.success("📚 **Tesis**")
        st.write("Bitácora y resúmenes de papers.")
        if st.button("Ir a Tesis", use_container_width=True):
            st.session_state.pagina_actual = "Tesis"
            st.rerun()

# --- MIS CURSOS ---
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
                    if "Nombre" not in df_nuevo.columns and "Estudiante" in df_nuevo.columns:
                        df_nuevo.rename(columns={"Estudiante": "Nombre"}, inplace=True)
                    st.session_state.datos_cursos[curso_actual] = df_nuevo
                    st.rerun()
                except: pass

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
                    "Décimas": st.column_config.NumberColumn(
                        label="Ganadas",
                        step=1,
                        min_value=0,
                        max_value=50,
                        format="%d 🌟"
                    )
                },
                use_container_width=True,
                num_rows="fixed",
                key=f"editor_dec_{curso_actual}"
            )
            st.session_state.datos_decimas[curso_actual] = df_dec_editado

        # --- CÁLCULO FINAL ---
        st.write("---")
        if not df_editado.empty:
            df_final = df_editado.copy()
            cols_notas = [c for c in df_final.columns if "Nota" in c]
            
            for c in cols_notas:
                df_final[c] = pd.to_numeric(df_final[c], errors='coerce')
            
            df_final['Prom. Notas'] = df_final[cols_notas].replace(0, pd.NA).mean(axis=1).round(1)
            
            decimas_lista = df_dec_editado['Décimas'].tolist()
            if len(decimas_lista) < len(df_final):
                decimas_lista += [0] * (len(df_final) - len(decimas_lista))
            
            df_final['Décimas'] = decimas_lista
            df_final['Prom. Final'] = df_final['Prom. Notas'] + (df_final['Décimas'] * 0.1)
            
            def style_red(val):
                try: return 'color: #ff4b4b' if val < 4.0 else ''
                except: return ''
                
            st.dataframe(df_final[['Nombre', 'Prom. Notas', 'Décimas', 'Prom. Final']].style.applymap(style_red, subset=['Prom. Final']), use_container_width=True)

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
        "tesis": st.session_state.tesis_papers,
        "tema": st.session_state.tema
    }
    st.download_button("⬇️ Descargar Respaldo JSON", data=json.dumps(datos_exportar), file_name="respaldo_v10_final.json", mime="application/json")
    
    archivo = st.file_uploader("⬆️ Cargar Respaldo", type="json")
    if archivo:
        try:
            data = json.load(archivo)
            if "cursos" in data:
                nuevos_cursos = {}
                for k, v in data["cursos"].items():
                    df = pd.read_json(v)
                    for col in df.columns:
                        if "Nota" in col: df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
                    nuevos_cursos[k] = df
                st.session_state.datos_cursos = nuevos_cursos

            if "decimas_data" in data:
                nuevas_decimas = {}
                for k, v in data["decimas_data"].items():
                    nuevas_decimas[k] = pd.read_json(v)
                st.session_state.datos_decimas = nuevas_decimas
            
            if "planificacion" in data: st.session_state.planificacion = data["planificacion"]
            if "tesis" in data: st.session_state.tesis_papers = data["tesis"]
            if "tema" in data: st.session_state.tema = data["tema"]
            
            st.success("¡Sistema restaurado!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

