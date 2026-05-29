"""
Dashboard page - Weight tracking and progress display
"""

import streamlit as st
from datetime import datetime

from database import get_usuarios, add_peso, get_pesos_usuario, update_usuario, delete_usuario
from utils import (
    calcular_imc,
    clasificar_imc,
    calcular_progreso,
    calcular_semanas_restantes,
    calcular_bajada,
    calcular_falta,
)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Mi Progreso - FitDuel", layout="wide")

# Card styling using key-based CSS
st.markdown("""
<style>
.st-key-user_card_ {
    background: #FFFFFF !important;
    box-shadow: 0 4px 24px rgba(16, 185, 129, 0.08), 0 2px 8px rgba(31, 41, 55, 0.06) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(16, 185, 129, 0.1) !important;
}

/* Target containers with user_card keys */
div[class*="st-key-user_card"] {
    background: #FFFFFF !important;
    box-shadow: 0 4px 24px rgba(16, 185, 129, 0.08), 0 2px 8px rgba(31, 41, 55, 0.06) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(16, 185, 129, 0.1) !important;
}

/* Inputs inside user cards - gray background */
div[class*="st-key-user_card"] input,
div[class*="st-key-user_card"] textarea,
div[class*="st-key-user_card"] [data-baseweb="input"],
div[class*="st-key-user_card"] [data-baseweb="textarea"],
div[class*="st-key-user_card"] [data-baseweb="select"] {
    background-color: #F4F7F6 !important;
    border-color: #E5E7EB !important;
}

/* Number input wrapper */
div[class*="st-key-user_card"] .stNumberInput > div > div {
    background-color: #F4F7F6 !important;
}

/* Expander background (Editar usuario expander) */
div[class*="st-key-user_card"] [data-testid="stExpander"] {
    background-color: #F9FAFB !important;
    border-radius: 12px !important;
    border: 1px solid #E5E7EB !important;
}

/* Expander content */
div[class*="st-key-user_card"] [data-testid="stExpander"] details {
    background-color: #F9FAFB !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Mi Progreso")
st.markdown("Todo tu progreso en un vistazo")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# CHECK LOGIN AND SESSION
# ═════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    st.warning("👉 Por favor inicia sesión primero")
    st.stop()

if not st.session_state.get("sesion_id"):
    st.warning("👈 Por favor selecciona un desafío primero")
    st.stop()

sesion_id = st.session_state.sesion_id

# ═════════════════════════════════════════════════════════════════════════════
# ADD USER SECTION
# ═════════════════════════════════════════════════════════════════════════════

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("➕ Agregar usuario", use_container_width=True):
        st.session_state.show_add_user = True

if st.session_state.get("show_add_user", False):
    with st.expander("Agregar nuevo usuario", expanded=True):
        from database import create_usuario

        col1, col2 = st.columns(2)
        with col1:
            nombre_user = st.text_input("Nombre")
            altura = st.number_input(
                "Altura (m)",
                min_value=1.0,
                max_value=2.5,
                step=0.01,
                value=1.75,
                format="%.2f",
            )

        with col2:
            peso_inicial = st.number_input(
                "Peso inicial (kg)",
                min_value=40.0,
                max_value=200.0,
                step=0.1,
                value=100.0,
                format="%.1f",
            )
            meta_peso = st.number_input(
                "Meta de peso (kg)",
                min_value=40.0,
                max_value=200.0,
                step=0.1,
                value=90.0,
                format="%.1f",
            )

        if st.button("Crear usuario"):
            if nombre_user and altura and peso_inicial and meta_peso:
                create_usuario(sesion_id, nombre_user, altura, meta_peso, peso_inicial)
                st.success(f"✅ Usuario '{nombre_user}' creado!")
                st.session_state.show_add_user = False
                st.rerun()
            else:
                st.error("Por favor completa todos los campos")

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# USERS DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════

usuarios_df = get_usuarios(sesion_id)

if usuarios_df.empty:
    st.info("👉 Agrega usuarios para comenzar a trackear pesos")
else:
    for idx, usuario in usuarios_df.iterrows():
        usuario_id = usuario["id"]
        nombre = usuario["nombre"]
        altura = usuario["altura"]
        meta = usuario["meta_peso"]
        peso_inicial = usuario["peso_inicial"]

        # Get weight history
        pesos_df = get_pesos_usuario(usuario_id)
        peso_actual = pesos_df["peso"].iloc[-1] if not pesos_df.empty else peso_inicial

        # Calculations
        imc_actual = calcular_imc(peso_actual, altura)
        imc_cat, imc_color = clasificar_imc(imc_actual)
        progreso = calcular_progreso(peso_actual, peso_inicial, meta)
        faltan = calcular_falta(peso_actual, meta)
        semanas = calcular_semanas_restantes(peso_actual, meta)
        bajo = calcular_bajada(peso_inicial, peso_actual)

        # Create user card container
        with st.container(border=True, key=f"user_card_{usuario_id}"):
            # User card with action buttons
            col_title, col_edit, col_delete = st.columns([2, 1, 1])
            with col_title:
                st.markdown(f"### 👤 {nombre}")
            with col_edit:
                if st.button("✏️ Editar", key=f"edit_{usuario_id}", use_container_width=True):
                    st.session_state[f"edit_user_{usuario_id}"] = True
            with col_delete:
                if st.button("🗑️ Eliminar", key=f"delete_{usuario_id}", use_container_width=True):
                    st.session_state[f"confirm_delete_{usuario_id}"] = True

            # Edit modal
            if st.session_state.get(f"edit_user_{usuario_id}", False):
                with st.expander("Editar usuario", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_nombre = st.text_input("Nombre", value=nombre, key=f"edit_nombre_{usuario_id}")
                        new_altura = st.number_input(
                            "Altura (m)",
                            min_value=1.0,
                            max_value=2.5,
                            step=0.01,
                            value=float(altura),
                            key=f"edit_altura_{usuario_id}",
                            format="%.2f",
                        )
                    with col2:
                        new_meta = st.number_input(
                            "Meta de peso (kg)",
                            min_value=40.0,
                            max_value=200.0,
                            step=0.1,
                            value=float(meta),
                            key=f"edit_meta_{usuario_id}",
                            format="%.1f",
                        )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Guardar cambios", key=f"save_{usuario_id}", use_container_width=True):
                            if update_usuario(usuario_id, nombre=new_nombre, altura=new_altura, meta_peso=new_meta):
                                st.success(f"✅ Usuario '{new_nombre}' actualizado!")
                                st.session_state[f"edit_user_{usuario_id}"] = False
                                st.rerun()
                            else:
                                st.error("Error al actualizar el usuario")
                    with col2:
                        if st.button("❌ Cancelar", key=f"cancel_{usuario_id}", use_container_width=True):
                            st.session_state[f"edit_user_{usuario_id}"] = False
                            st.rerun()

            # Delete confirmation
            if st.session_state.get(f"confirm_delete_{usuario_id}", False):
                st.warning(f"⚠️ ¿Estás seguro de que quieres eliminar a '{nombre}'? Se borrarán todos sus registros de peso.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Sí, eliminar", key=f"confirm_yes_{usuario_id}", use_container_width=True):
                        if delete_usuario(usuario_id):
                            st.success(f"✅ Usuario '{nombre}' eliminado")
                            st.session_state[f"confirm_delete_{usuario_id}"] = False
                            st.rerun()
                        else:
                            st.error("Error al eliminar el usuario")
                with col2:
                    if st.button("❌ Cancelar", key=f"confirm_no_{usuario_id}", use_container_width=True):
                        st.session_state[f"confirm_delete_{usuario_id}"] = False
                        st.rerun()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Hoy", f"{peso_actual:.1f} kg", f"IMC {imc_actual}")
            with col2:
                st.metric("Meta", f"{meta:.1f} kg", "")
            with col3:
                st.metric("Faltan", f"{faltan:.1f} kg", "")

            # Progress bar
            st.progress(
                min(100, max(0, progreso / 100)),
                text=f"{progreso:.1f}% del camino",
            )
            st.caption(
                f"⏱ A ritmo sano (~0.5kg/sem): ~{semanas} semanas | Ya bajó {bajo:.1f} kg"
            )

            # Weight input
            col1, col2 = st.columns([3, 1])
            with col1:
                nuevo_peso = st.number_input(
                    f"Nuevo peso para {nombre} (kg)",
                    min_value=40.0,
                    max_value=200.0,
                    step=0.1,
                    value=float(peso_actual),
                    key=f"peso_{usuario_id}",
                    format="%.1f",
                )
            with col2:
                if st.button("+ Cargar", key=f"btn_{usuario_id}", use_container_width=True):
                    fecha = datetime.now().strftime("%d %b")
                    if add_peso(usuario_id, nuevo_peso, fecha):
                        st.success(f"✅ Peso registrado para {nombre}")
                        st.rerun()
                    else:
                        st.error("Error al registrar el peso")
        st.markdown("---")

    # Summary card
    st.markdown("### ⚖️ Resumen del equipo")
    col1, col2, col3 = st.columns(3)

    total_bajada = 0
    for idx, usuario in usuarios_df.iterrows():
        usuario_id = usuario["id"]
        peso_inicial = usuario["peso_inicial"]
        pesos_df = get_pesos_usuario(usuario_id)
        peso_actual = pesos_df["peso"].iloc[-1] if not pesos_df.empty else peso_inicial
        total_bajada += calcular_bajada(peso_inicial, peso_actual)

    with col1:
        st.metric("Total bajado (todos)", f"{total_bajada:.1f} kg", "")
    with col2:
        st.metric("Usuarios activos", len(usuarios_df), "")
    with col3:
        st.metric("Promedio de progreso", f"{usuarios_df.shape[0]} personas", "")
