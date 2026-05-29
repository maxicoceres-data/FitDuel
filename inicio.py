"""
🌿 Maxi & Belu - Weight Tracking App
Main entry point for Streamlit application
"""

import streamlit as st
import random
from datetime import datetime

from database import (
    init_db,
    get_sesiones_por_usuario,
    create_sesion_for_user,
    register_user,
    login_user,
    get_sesion_by_id,
    update_sesion,
    delete_sesion,
)
from utils import TIPS

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="⚔️ FitDuel",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════════
# STYLES
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #10B981;
            --health: #059669;
            --action: #F59E0B;
            --warning: #FF6B6B;
            --text: #1F2937;
            --bg: #F4F7F6;
        }

        /* Apply Inter only to body - inherited by text elements */
        body, .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        /* Specific text elements only */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp p, .stApp label, .stApp button {
            font-family: 'Inter', sans-serif !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        .metric-card {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 12px;
        }
        .section-title {
            font-size: 18px;
            color: #1F2937;
            margin-bottom: 16px;
            margin-top: 20px;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
        }
        .logo-title {
            font-size: 32px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
            font-family: 'Inter', sans-serif !important;
        }
    </style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═════════════════════════════════════════════════════════════════════════════

import json
import os

init_db()

# ─────────────────────────────────────────────────────────────────────────
# RESTORE SESSION FROM FILE
# ─────────────────────────────────────────────────────────────────────────

SESSION_FILE = "data/.session"

def save_session():
    """Save current session to file"""
    if st.session_state.get("logged_in"):
        session_data = {
            "logged_in": True,
            "user_id": st.session_state.user_id,
            "username": st.session_state.username,
        }
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
        with open(SESSION_FILE, "w") as f:
            json.dump(session_data, f)

def restore_session():
    """Restore session from file if exists"""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                session_data = json.load(f)
                if session_data.get("logged_in"):
                    st.session_state.logged_in = True
                    st.session_state.user_id = session_data.get("user_id")
                    st.session_state.username = session_data.get("username")
                    st.session_state.current_page = "inicio"
        except:
            pass

def clear_session():
    """Clear session file"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# Restore session on page load
if "logged_in" not in st.session_state:
    restore_session()

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR - LOGO SIEMPRE VISIBLE
# ═════════════════════════════════════════════════════════════════════════════

st.sidebar.markdown('<div class="logo-title">⚔️</div>', unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center'>FitDuel</h3>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# MAIN APP LOGIC
# ═════════════════════════════════════════════════════════════════════════════

if st.session_state.get("logged_in"):
    # ─────────────────────────────────────────────────────────────────────────
    # LOGGED IN - SHOW NAVIGATION AND CONTENT
    # ─────────────────────────────────────────────────────────────────────────

    st.sidebar.markdown("---")
    st.sidebar.caption(f"👤 {st.session_state.username}")
    st.sidebar.markdown("---")

    # Navigation buttons
    if st.sidebar.button("🏠 Inicio", use_container_width=True, key="nav_inicio"):
        st.session_state.current_page = "inicio"
    if st.sidebar.button("📊 Dashboard", use_container_width=True, key="nav_dashboard"):
        st.session_state.current_page = "dashboard"
    if st.sidebar.button("📈 Gráficos", use_container_width=True, key="nav_graficos"):
        st.session_state.current_page = "graficos"
    if st.sidebar.button("🍳 Recetas", use_container_width=True, key="nav_recetas"):
        st.session_state.current_page = "recetas"
    if st.sidebar.button("📅 Plan", use_container_width=True, key="nav_plan"):
        st.session_state.current_page = "plan"

    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Cerrar sesión", use_container_width=True, key="sidebar_logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.sesion_id = None
        st.session_state.current_page = "inicio"
        clear_session()
        st.success("✅ Sesión cerrada")
        st.rerun()

    # Initialize current_page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "inicio"

    # Display content based on current page
    if st.session_state.current_page == "inicio":
        # ─────────────────────────────────────────────────────────────────────
        # INICIO PAGE
        # ─────────────────────────────────────────────────────────────────────

        col1, col2 = st.columns([2, 1])

        with col1:
            st.title(f"👋 Hola, {st.session_state.username}")
            st.caption("Su viaje juntos · sin sufrimiento · listos para otra semana de progreso 💪")

        with col2:
            st.info(f"💡 {random.choice(TIPS)}")

        st.markdown("---")

        usuario_id = st.session_state.user_id

        st.markdown("### 📋 Tus sesiones")

        sesiones_df = get_sesiones_por_usuario(usuario_id)
        sesiones_list = sesiones_df["nombre"].tolist() if not sesiones_df.empty else []

        col1, col2 = st.columns([3, 1])

        with col1:
            if sesiones_list:
                sesion_select = st.selectbox(
                    "Selecciona una sesión:",
                    sesiones_list,
                    key="sesion_select",
                )
                sesion_id = int(sesiones_df[sesiones_df["nombre"] == sesion_select]["id"].values[0])
                st.session_state.sesion_id = sesion_id
                st.session_state.sesion_nombre = sesion_select
            else:
                sesion_select = None
                sesion_id = None
                st.session_state.sesion_id = None

        with col2:
            if st.button("➕ Nueva sesión", use_container_width=True):
                st.session_state.show_new_sesion = True

        if st.session_state.get("show_new_sesion", False):
            with st.expander("Crear nuevo desafío", expanded=True):
                nueva_sesion = st.text_input(
                    "Nombre del desafío (ej: Enero Challenge)",
                    key="new_sesion_input",
                )

                col1, col2 = st.columns(2)
                with col1:
                    fecha_inicio = st.date_input(
                        "Fecha de inicio",
                        key="new_sesion_inicio",
                    )
                with col2:
                    fecha_fin = st.date_input(
                        "Fecha de fin (opcional)",
                        value=None,
                        key="new_sesion_fin",
                    )

                objetivo = st.text_input(
                    "Objetivo del desafío (ej: Bajar 5kg)",
                    key="new_sesion_objetivo",
                    placeholder="Opcional"
                )

                competitivo = st.checkbox(
                    "🏆 Modo competitivo (mostrar ranking)",
                    value=True,
                    key="new_sesion_competitivo"
                )

                if st.button("Crear desafío"):
                    if nueva_sesion and fecha_inicio:
                        sesion_id_new = create_sesion_for_user(
                            usuario_id,
                            nueva_sesion,
                            fecha_inicio=fecha_inicio.isoformat(),
                            fecha_fin=fecha_fin.isoformat() if fecha_fin else None,
                            competitivo=competitivo,
                            objetivo=objetivo if objetivo else None
                        )
                        if sesion_id_new:
                            st.success(f"✅ Desafío '{nueva_sesion}' creado!")
                            st.session_state.show_new_sesion = False
                            st.rerun()
                        else:
                            st.error("❌ Ya tienes un desafío con ese nombre")
                    else:
                        st.error("Por favor completa nombre y fecha de inicio")

        st.markdown("---")

        if sesion_id:
            st.success(f"✅ Desafío activo: **{sesion_select}**")

            sesion_info = get_sesion_by_id(sesion_id)

            # Inicializar variables de estado
            if "edit_open" not in st.session_state:
                st.session_state.edit_open = False
            if "delete_open" not in st.session_state:
                st.session_state.delete_open = False

            def toggle_edit():
                st.session_state.edit_open = not st.session_state.edit_open
                st.session_state.delete_open = False

            def toggle_delete():
                st.session_state.delete_open = not st.session_state.delete_open
                st.session_state.edit_open = False

            # Botones de acción principales
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.button("✏️ Editar desafío", key="btn_edit", use_container_width=True, on_click=toggle_edit)
            with col_btn2:
                st.button("🗑️ Eliminar desafío", key="btn_delete", use_container_width=True, on_click=toggle_delete)

            # SECCIÓN: EDITAR (Usando st.form)
            if st.session_state.edit_open and sesion_info:
                st.markdown("### Editar Desafío")

                with st.form(key="edit_session_form"):
                    edit_nombre = st.text_input("Nombre", sesion_info.get("nombre"), key="e_name")

                    col1, col2 = st.columns(2)
                    with col1:
                        fecha_ini_str = sesion_info.get("fecha_inicio")
                        fecha_ini = datetime.strptime(fecha_ini_str, "%Y-%m-%d").date() if fecha_ini_str else datetime.now().date()
                        edit_inicio = st.date_input("Inicio", fecha_ini, key="e_start")
                    with col2:
                        fecha_fin_str = sesion_info.get("fecha_fin")
                        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date() if fecha_fin_str else None
                        edit_fin = st.date_input("Fin", fecha_fin, key="e_end")

                    edit_comp = st.checkbox("Competitivo", bool(sesion_info.get("competitivo")), key="e_comp")
                    edit_obj = st.text_input("Objetivo", sesion_info.get("objetivo") or "", key="e_obj")

                    submitted = st.form_submit_button("Guardar Cambios", type="primary")

                    if submitted:
                        result = update_sesion(
                            sesion_id,
                            nombre=edit_nombre,
                            fecha_inicio=edit_inicio.isoformat() if edit_inicio else None,
                            fecha_fin=edit_fin.isoformat() if edit_fin else None,
                            competitivo=edit_comp,
                            objetivo=edit_obj
                        )
                        if result:
                            st.success("✅ Guardado correctamente")
                            st.session_state.edit_open = False
                            st.rerun()
                        else:
                            st.error("❌ Error al guardar en la base de datos")

            # SECCIÓN: ELIMINAR
            if st.session_state.delete_open:
                st.warning(f"⚠️ ¿Seguro que deseas eliminar '{sesion_select}' y todos sus datos?")

                col_del1, col_del2 = st.columns(2)
                with col_del1:
                    if st.button("Sí, eliminar", key="delete_confirm", use_container_width=True):
                        delete_sesion(sesion_id)
                        st.session_state.sesion_id = None
                        st.session_state.delete_open = False
                        st.success("✅ Eliminado con éxito")
                        st.rerun()
                with col_del2:
                    if st.button("Cancelar", key="delete_cancel", use_container_width=True):
                        st.session_state.delete_open = False
                        st.rerun()

            st.caption("Usa el menú lateral para navegar entre las secciones")
        else:
            if sesiones_list:
                st.warning("👆 Selecciona un desafío del menú de arriba")
            else:
                st.info("👆 Crea un nuevo desafío para comenzar")

        st.markdown("\n")
        st.caption("Actualicen su peso cada semana · 0.3–0.5 kg por semana es perfecto · ¡van a llegar! 💪")

    elif st.session_state.current_page == "dashboard":
        # Load Dashboard page
        exec(open("app_pages/1_📊_Dashboard.py", encoding="utf-8").read())

    elif st.session_state.current_page == "graficos":
        # Load Gráficos page
        exec(open("app_pages/2_📈_Gráficos.py", encoding="utf-8").read())

    elif st.session_state.current_page == "recetas":
        # Load Recetas page
        exec(open("app_pages/3_🍳_Recetas.py", encoding="utf-8").read())

    elif st.session_state.current_page == "plan":
        # Load Plan page
        exec(open("app_pages/4_📅_Plan.py", encoding="utf-8").read())

else:
    # ─────────────────────────────────────────────────────────────────────────
    # NOT LOGGED IN - SHOW LOGIN PAGE
    # ─────────────────────────────────────────────────────────────────────────

    st.title("⚔️ FitDuel")
    st.markdown("**Su transformación, su desafío**")
    st.markdown("---")

    # LOGIN / REGISTER TABS
    tab1, tab2 = st.tabs(["🔓 Iniciar sesión", "📝 Registrarse"])

    # ─────────────────────────────────────────────────────────────────────────
    # LOGIN TAB
    # ─────────────────────────────────────────────────────────────────────────

    with tab1:
        st.caption("¿No tienes cuenta? Regístrate ☝️")
        st.markdown("### Inicia sesión con tu cuenta")

        username = st.text_input(
            "Usuario",
            placeholder="tu_usuario",
            key="login_username",
        )

        password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="••••••",
            key="login_password",
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔓 Iniciar sesión", use_container_width=True, key="login_btn"):
                if not username or not password:
                    st.error("Por favor completa todos los campos")
                else:
                    success, user_id, message = login_user(username, password)

                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.current_page = "inicio"
                        save_session()
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(message)

        st.markdown("---")
        

    # ─────────────────────────────────────────────────────────────────────────
    # REGISTER TAB
    # ─────────────────────────────────────────────────────────────────────────

    with tab2:
        st.markdown("### Crea una cuenta nueva")

        reg_username = st.text_input(
            "Usuario",
            placeholder="tu_usuario (mín 3 caracteres)",
            key="reg_username",
        )

        reg_email = st.text_input(
            "Email (opcional)",
            placeholder="tu@email.com",
            key="reg_email",
        )

        reg_password = st.text_input(
            "Contraseña",
            type="password",
            placeholder="••••• (mín 6 caracteres)",
            key="reg_password",
        )

        reg_password_confirm = st.text_input(
            "Confirmar contraseña",
            type="password",
            placeholder="•••••",
            key="reg_password_confirm",
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📝 Registrarse", use_container_width=True, key="register_btn"):
                # Validaciones
                if not reg_username or not reg_password:
                    st.error("Usuario y contraseña son obligatorios")
                elif len(reg_username) < 3:
                    st.error("El usuario debe tener al menos 3 caracteres")
                elif len(reg_password) < 6:
                    st.error("La contraseña debe tener al menos 6 caracteres")
                elif reg_password != reg_password_confirm:
                    st.error("Las contraseñas no coinciden")
                else:
                    success, message = register_user(reg_username, reg_password, reg_email)
                    if success:
                        st.success(message)
                        st.info("👉 Ahora puedes iniciar sesión arriba")
                    else:
                        st.error(message)

        st.markdown("---")
        st.caption("¿Ya tienes cuenta? Inicia sesión arriba 👆")

    # ─────────────────────────────────────────────────────────────────────────
    # INFO SECTION
    # ─────────────────────────────────────────────────────────────────────────

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 ¿Qué es FitDuel?")
        st.markdown("""
        La app que convierte tu transformación en un desafío compartido.

        - 📊 Mirá tu progreso en tiempo real
        - 🏆 Compite con tu pareja o amigos
        - 📈 Estadísticas y rankings
        - 🍳 Recetas que te acercan a la meta
        - 📅 Tu plan semanal personalizado
        """)

    with col2:
        st.markdown("### 💡 Características")
        st.markdown("""
        - 🔐 Cuenta personal segura
        - 📋 Múltiples sesiones por usuario
        - ⚖️ Cálculo automático de IMC
        - 📱 Accesible desde cualquier dispositivo
        - 💾 Datos almacenados localmente
        - 🎨 Interfaz moderna y limpia
        """)

    st.markdown("---")
    st.caption("Actualicen su peso cada semana · 0.3–0.5 kg por semana es perfecto · ¡van a llegar! 💪")
