"""
Graphics page - Weight evolution charts
"""

import streamlit as st
import plotly.graph_objects as go

from database import get_usuarios, get_pesos_usuario, get_sesion_by_id
from utils import calcular_bajada
from datetime import datetime
import pandas as pd

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Ranking & Stats - FitDuel", layout="wide")

# Card styling now handled by theme.py (light/dark mode aware)
st.markdown("""
<style>
div[class*="st-key-graph_card"],
div[class*="st-key-stats_card"] {
    padding: 20px !important;
    margin-bottom: 16px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 Ranking & Stats")
st.markdown("Compite, supérate, gana")
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
sesion_info = get_sesion_by_id(sesion_id)

# ═════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═════════════════════════════════════════════════════════════════════════════

usuarios_df = get_usuarios(sesion_id)

if usuarios_df.empty:
    st.info("👉 Agrega usuarios al desafío para ver gráficos")
else:
    # ═════════════════════════════════════════════════════════════════════════════
    # COMPETITIVE MODE - LEADERBOARD AND STATS
    # ═════════════════════════════════════════════════════════════════════════════

    if sesion_info and sesion_info.get("competitivo") in [True, 1]:
        # Calculate progress for each user
        leaderboard_data = []
        for idx, usuario in usuarios_df.iterrows():
            usuario_id = usuario["id"]
            nombre = usuario["nombre"]
            peso_inicial = usuario["peso_inicial"]

            pesos_df = get_pesos_usuario(usuario_id)
            peso_actual = pesos_df["peso"].iloc[-1] if not pesos_df.empty else peso_inicial

            bajada = calcular_bajada(peso_inicial, peso_actual)
            leaderboard_data.append({
                "Posición": 0,
                "Nombre": nombre,
                "Inicial": f"{peso_inicial:.1f} kg",
                "Actual": f"{peso_actual:.1f} kg",
                "Bajada": f"{bajada:.1f} kg",
                "usuario_id": usuario_id,
            })

        leaderboard_data = sorted(leaderboard_data, key=lambda x: float(x["Bajada"].split()[0]), reverse=True)

        for i, item in enumerate(leaderboard_data, 1):
            item["Posición"] = f"🥇 {i}" if i == 1 else f"🥈 {i}" if i == 2 else f"🥉 {i}" if i == 3 else f"#{i}"

        # Leaderboard card
        with st.container(key="stats_card_leaderboard"):
            st.markdown("### 🏆 Leaderboard de Competencia")
            leaderboard_df = pd.DataFrame([
                {
                    "Posición": item["Posición"],
                    "Nombre": item["Nombre"],
                    "Peso Inicial": item["Inicial"],
                    "Peso Actual": item["Actual"],
                    "Bajada": item["Bajada"],
                }
                for item in leaderboard_data
            ])
            st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)

        # Progress card
        with st.container(key="stats_card_progress"):
            st.markdown("### ⏱️ Progreso del Desafío")
            col1, col2, col3 = st.columns(3)

            if sesion_info.get("fecha_inicio") and sesion_info.get("fecha_fin"):
                fecha_inicio = datetime.strptime(sesion_info["fecha_inicio"], "%Y-%m-%d")
                fecha_fin = datetime.strptime(sesion_info["fecha_fin"], "%Y-%m-%d")
                ahora = datetime.now()

                total_dias = (fecha_fin - fecha_inicio).days
                dias_transcurridos = (ahora - fecha_inicio).days
                porcentaje = min(100, max(0, (dias_transcurridos / total_dias * 100))) if total_dias > 0 else 0

                with col1:
                    st.metric("Progreso", f"{porcentaje:.1f}%")
                with col2:
                    st.metric("Días Transcurridos", f"{dias_transcurridos} / {total_dias}")
                with col3:
                    dias_restantes = max(0, (fecha_fin - ahora).days)
                    st.metric("Días Restantes", dias_restantes)
            else:
                with col1:
                    st.metric("Progreso", "Sin fecha fin")
                with col2:
                    st.metric("Estado", "Indefinido")

        # Stats card
        with st.container(key="stats_card_stats"):
            st.markdown("### 📊 Estadísticas del Desafío")
            col1, col2, col3, col4 = st.columns(4)

            total_bajada = sum(float(item["Bajada"].split()[0]) for item in leaderboard_data)
            with col1:
                st.metric("Total Bajado", f"{total_bajada:.1f} kg")

            bajada_promedio = total_bajada / len(leaderboard_data) if leaderboard_data else 0
            with col2:
                st.metric("Bajada Promedio", f"{bajada_promedio:.1f} kg")

            if leaderboard_data:
                ganador = leaderboard_data[0]
                with col3:
                    st.metric("Ganador Actual", ganador["Nombre"])

            with col4:
                st.metric("Participantes", len(leaderboard_data))
    # Render chart for each user
    for idx, usuario in usuarios_df.iterrows():
        usuario_id = usuario["id"]
        nombre = usuario["nombre"]
        meta = usuario["meta_peso"]

        pesos_df = get_pesos_usuario(usuario_id)

        with st.container(key=f"graph_card_{usuario_id}"):
            if pesos_df.empty:
                st.markdown(f"### 📈 Evolución de {nombre}")
                st.info(f"👉 Registra pesos para {nombre} para ver la gráfica")
            else:
                st.markdown(f"### 📈 Evolución de {nombre}")

                # Create figure
                fig = go.Figure()

                # Add weight line
                fig.add_trace(
                    go.Scatter(
                        x=pesos_df["fecha"],
                        y=pesos_df["peso"],
                        mode="lines+markers",
                        name="Peso",
                        line=dict(color="#10B981", width=3),
                        marker=dict(size=8, color="#F59E0B"),
                        hovertemplate="<b>%{x}</b><br>Peso: %{y:.1f} kg<extra></extra>",
                    )
                )

                # Add goal line
                fig.add_hline(
                    y=meta,
                    line_dash="dash",
                    line_color="#F59E0B",
                    annotation=dict(
                        text="🎯 Meta",
                        font=dict(color="#F59E0B", size=12),
                        xanchor="right",
                        yanchor="bottom",
                    ),
                    annotation_position="top right",
                )

                # Update layout - transparent background to blend with card
                fig.update_layout(
                    title="",
                    xaxis_title="Fecha",
                    yaxis_title="Peso (kg)",
                    hovermode="x unified",
                    template="plotly_white",
                    height=400,
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=20, b=40, l=40, r=40),
                )

                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"{len(pesos_df)} medición(es) registrada(s)")
