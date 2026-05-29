"""
Plan page - Weekly plan and nutrition tips
"""

import streamlit as st
import pandas as pd

from utils import PLAN, PLAN_TIPS

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Tu Plan Semanal - FitDuel", layout="wide")

st.title("📅 Tu Plan Semanal")
st.markdown("Cada día cuenta")
st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# CHECK LOGIN
# ═════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    st.warning("👉 Por favor inicia sesión primero")
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# PHILOSOPHY
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 🎯 La filosofía del plan")
st.markdown("""
**Sin prohibiciones. Sin contar calorías. Comer bien, moverse, disfrutar.**

El déficit viene solo cuando la base es buena. Ustedes van a cocinar rico —
solo hay que hacer pequeños ajustes inteligentes.
""")

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# WEEKLY PLAN
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 📋 Plan semanal")
st.markdown("Actividades y comidas sugeridas para cada día")

plan_df = pd.DataFrame(PLAN)
st.dataframe(plan_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# NUTRITION TIPS
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 🍽️ Tips de alimentación sin drama")

col1, col2 = st.columns(2)
for i, tip in enumerate(PLAN_TIPS):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"✔ {tip}")

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# ADDITIONAL TIPS
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 💡 Tips importantes")

col1, col2 = st.columns(2)

with col1:
    st.success("**✅ Haz esto:**")
    st.markdown("""
    - Come despacio (20 min)
    - Cocina en casa
    - Camina después de comer
    - Bebe agua constantemente
    - Duerme 7-8 horas
    - Sé consistente
    """)

with col2:
    st.warning("**⚠️ Evita esto:**")
    st.markdown("""
    - Restricciones severas
    - Saltear comidas
    - Bebidas azucaradas
    - Estrés y dormir mal
    - Compararte con otros
    - Abandones a los 2 meses
    """)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# MOTIVATION
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("### 💪 Mantente motivado")
st.info(
    "📊 Actualiza tu peso cada semana · 0.3–0.5 kg por semana es perfecto · ¡van a llegar! 💪"
)
