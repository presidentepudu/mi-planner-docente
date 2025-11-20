import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi Planner Docente", layout="wide", page_icon="🎓")

# --- 2. INICIALIZAR MEMORIA (ESTO ES LO QUE ARREGLA EL ERROR) ---
# Aquí creamos las variables vacías si no existen, al principio de todo.

if 'estudiantes' not in st.session_state:
    # Datos iniciales de prueba
    st.session_state.estudiantes = pd.DataFrame({
        'Estudiante': ['Juan Pérez', 'María González', 'Pedro Soto'],
        'Nota 1': [4.5, 6.0, 5.5],
        'Nota 2': [5.0, 6.5, 4.0],
        'Décimas Acumuladas': [2, 5, 0]
    })

if 'recordatorios' not in st.session_state:
    st.session_state.recordatorios = []

if 'papers' not in st.session_state:
    st.session_state.papers = []

# --- DATOS PERSONALES ---
MI_EMAIL = "tu_correo@gmail.com"
NOMBRE_PROFE = "Cristobal"

# --- BARRA LATERAL (MENÚ) ---
st.sidebar.title(f"Hola, {NOMBRE_PROFE}")
opcion = st.sidebar.radio("Menú", ["Mis Estudiantes", "Google Calendar", "Tesis & Papers", "Configuración"])

# ==============================
# SECCIÓN 1: MIS ESTUDIANTES
# ==============================
if opcion == "Mis Estudiantes":
    st.title("📊 Control de Asignaturas")
    st.info("Edita las notas haciendo doble clic en la celda.")

    # Tabla editable conectada a la memoria
    df_editado = st.data_editor(
        st.session_state.estudiantes,
        num_rows="dynamic",
        key="editor_estudiantes", # Clave única para evitar conflictos
        column_config={
            "Nota 1": st.column_config.NumberColumn(min_value=1.0, max_value=7.0, step=0.1),
            "Nota 2": st.column_config.NumberColumn(min_value=1.0, max_value=7.0, step=0.1),
            "Décimas Acumuladas": st.column_config.NumberColumn(label="Décimas (+)", min_value=0, step=1)
        }
    )
    
    # Actualizar la memoria con los cambios
    st.session_state.estudiantes = df_editado

    # Botón de cálculo
    if st.button("Calcular Situación Final"):
        df_final = df_editado.copy()
        # Lógica: Promedio simple de notas + (décimas * 0.1)
        df_final['Promedio Notas'] = (df_final['Nota 1'] + df_final['Nota 2']) / 2
        df_final['Promedio Final'] = df_final['Promedio Notas'] + (df_final['Décimas Acumuladas'] * 0.1)
        
        st.write("### Resultados")
        # Resaltar promedios rojos (menor a 4.0)
        def color_rojo(val):
            color = '#ffcccc' if val < 4.0 else ''
            return f'background-color: {color}'
            
        st.dataframe(df_final.style.applymap(color_rojo, subset=['Promedio Final']))

# ==============================
# SECCIÓN 2: GOOGLE CALENDAR
# ==============================
elif opcion == "Google Calendar":
    st.title("📅 Mi Agenda")
    st.markdown("Aquí verás tu calendario sincronizado.")
    
    # URL de ejemplo (Feriados Chile). 
    # IMPORTANTE: Cámbiala por la tuya pública si quieres ver tus eventos reales.
    calendar_url = "https://calendar.google.com/calendar/embed?src=es.cl%23holiday%40group.v.calendar.google.com&ctz=America%2FSantiago"
    
    components.iframe(calendar_url, height=600, scrolling=True)

# ==============================
# SECCIÓN 3: TESIS & PAPERS
# ==============================
elif opcion == "Tesis & Papers":
    st.title("🎓 Gestión de Tesis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Recordatorios / Tareas")
        nueva_tarea = st.text_input("Nueva tarea pendiente:", placeholder="Ej: Revisar bibliografía...")
        if st.button("Agregar Tarea"):
            if nueva_tarea:
                st.session_state.recordatorios.append(nueva_tarea)
                st.rerun() # Recarga para mostrar el cambio inmediatamente
        
        st.write("---")
        if st.session_state.recordatorios:
            for i, tarea in enumerate(st.session_state.recordatorios):
                st.write(f"🔹 {tarea}")
                if st.button(f"Borrar", key=f"borrar_{i}"):
                    st.session_state.recordatorios.pop(i)
                    st.rerun()
        else:
            st.info("No hay tareas pendientes. ¡Bien hecho!")

    with col2:
        st.subheader("📚 Subir Paper")
        uploaded = st.file_uploader("Cargar PDF", type="pdf")
        if uploaded:
            st.success(f"Archivo '{uploaded.name}' listo para lectura.")
            # Aquí solo simulamos la subida, no se guarda en disco duro permanentemente en esta versión simple

# ==============================
# SECCIÓN 4: CONFIGURACIÓN
# ==============================
elif opcion == "Configuración":
    st.title("⚙️ Configuración")
    st.write("Aquí podrás ajustar parámetros futuros.")
    st.write(f"Usuario actual: {NOMBRE_PROFE}")