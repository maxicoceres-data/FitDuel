"""
Recipes page - Recipe database and management
"""

import streamlit as st

from utils import DESAYUNOS, ALMUERZOS, MERIENDAS

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Recetas Smart - FitDuel", layout="wide")

st.title("🍳 Recetas Smart")
st.markdown("Comé rico, bajá de peso")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# CHECK LOGIN
# ═════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    st.warning("👉 Por favor inicia sesión primero")
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# RECIPE TABS
# ═════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3 = st.tabs(["☀️ Desayunos", "🍽️ Almuerzos/Cenas", "☕ Meriendas"])

# ═════════════════────────────────────────────────────────────────────────────
# DESAYUNOS
# ═════────────────────────────────────────────────────────────────────────────

with tab1:
    st.markdown(f"### {len(DESAYUNOS)} opciones para arrancar el día con energía")

    for i, receta in enumerate(DESAYUNOS):
        with st.expander(f"{receta['emoji']} {receta['nombre']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"⏱ {receta['tiempo']}")
            with col2:
                st.caption(f"📊 {receta['dificultad']}")
            with col3:
                st.caption(f"🔥 {receta['calorias']}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🧺 Ingredientes**")
                for ingrediente in receta["ingredientes"]:
                    st.markdown(f"- {ingrediente}")

            with col2:
                st.markdown("**👨‍🍳 Pasos**")
                for j, paso in enumerate(receta["pasos"], 1):
                    st.markdown(f"{j}. {paso}")

            st.info(f"💡 **Tip:** {receta['tip']}")

# ═════────────────────────────────────────────────────────────────────────────
# ALMUERZOS
# ═════────────────────────────────────────────────────────────────────────────

with tab2:
    st.markdown(
        f"### {len(ALMUERZOS)} opciones para almuerzo o cena (2 por día, 6 días)"
    )

    for i, receta in enumerate(ALMUERZOS):
        with st.expander(f"{receta['emoji']} {receta['nombre']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"⏱ {receta['tiempo']}")
            with col2:
                st.caption(f"📊 {receta['dificultad']}")
            with col3:
                st.caption(f"🔥 {receta['calorias']}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🧺 Ingredientes**")
                for ingrediente in receta["ingredientes"]:
                    st.markdown(f"- {ingrediente}")

            with col2:
                st.markdown("**👨‍🍳 Pasos**")
                for j, paso in enumerate(receta["pasos"], 1):
                    st.markdown(f"{j}. {paso}")

            st.info(f"💡 **Tip:** {receta['tip']}")

# ═════────────────────────────────────────────────────────────────────────────
# MERIENDAS
# ═════────────────────────────────────────────────────────────────────────────

with tab3:
    st.markdown(f"### {len(MERIENDAS)} opciones para la tarde sin culpa")

    for i, receta in enumerate(MERIENDAS):
        with st.expander(f"{receta['emoji']} {receta['nombre']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.caption(f"⏱ {receta['tiempo']}")
            with col2:
                st.caption(f"📊 {receta['dificultad']}")
            with col3:
                st.caption(f"🔥 {receta['calorias']}")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🧺 Ingredientes**")
                for ingrediente in receta["ingredientes"]:
                    st.markdown(f"- {ingrediente}")

            with col2:
                st.markdown("**👨‍🍳 Pasos**")
                for j, paso in enumerate(receta["pasos"], 1):
                    st.markdown(f"{j}. {paso}")

            st.info(f"💡 **Tip:** {receta['tip']}")
