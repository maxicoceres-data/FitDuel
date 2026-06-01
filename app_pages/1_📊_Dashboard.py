"""
Dashboard page - Weight tracking and progress display
"""

import streamlit as st
from datetime import datetime

from database import (
    get_usuarios, add_peso, get_pesos_usuario, update_usuario, delete_usuario,
    get_comentarios, add_comentario, delete_comentario, get_comentarios_count,
    notificar_a_miembros_sesion,
)
from logros import LOGROS, get_logros_usuario, evaluar_logros
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

# Card styling now handled by theme.py (light/dark mode aware)
# Logros CSS
st.html("""
<style>
.logros-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 16px 0;
    padding: 12px;
    border-radius: 12px;
    background: rgba(16, 185, 129, 0.04);
    border: 1px solid rgba(16, 185, 129, 0.1);
}
.logro {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px 12px;
    border-radius: 10px;
    min-width: 80px;
    text-align: center;
    transition: all 0.3s ease;
}
.logro-desbloqueado {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(245, 158, 11, 0.15));
    border: 1px solid rgba(16, 185, 129, 0.3);
    animation: glow 2s ease-in-out infinite;
}
.logro-bloqueado {
    opacity: 0.3;
    filter: grayscale(80%);
}
.logro-icon {
    font-size: 28px;
    margin-bottom: 4px;
}
.logro-name {
    font-size: 11px;
    font-weight: 600;
    line-height: 1.2;
}
@keyframes glow {
    0%, 100% { box-shadow: 0 0 8px rgba(16, 185, 129, 0.3); }
    50% { box-shadow: 0 0 16px rgba(16, 185, 129, 0.5); }
}

/* Comments styling */
.comentario {
    padding: 10px 14px;
    margin: 8px 0;
    border-radius: 12px;
    background: rgba(16, 185, 129, 0.05);
    border-left: 3px solid #10B981;
}
.comentario-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 12px;
}
.comentario-author {
    font-weight: 700;
    color: #10B981;
}
.comentario-fecha {
    color: #94a3b8;
    font-size: 11px;
}
.comentario-mensaje {
    font-size: 14px;
    line-height: 1.4;
}
</style>
""")


def render_logros(usuario_id):
    """Render achievements section for a user (single line HTML for st.html)"""
    logros_desbloqueados = set(get_logros_usuario(usuario_id))

    items = []
    for logro_id, logro_info in LOGROS.items():
        is_unlocked = logro_id in logros_desbloqueados
        css_class = "logro-desbloqueado" if is_unlocked else "logro-bloqueado"
        items.append(
            f'<div class="logro {css_class}" title="{logro_info["descripcion"]}">'
            f'<div class="logro-icon">{logro_info["icono"]}</div>'
            f'<div class="logro-name">{logro_info["nombre"]}</div>'
            f'</div>'
        )

    return '<div class="logros-container">' + "".join(items) + '</div>'

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

        # Evaluate achievements
        pesos_count = len(pesos_df) if not pesos_df.empty else 0
        in_team = len(usuarios_df) > 1
        newly_unlocked = evaluar_logros(
            usuario_id=int(usuario_id),
            peso_inicial=peso_inicial,
            peso_actual=peso_actual,
            meta_peso=meta,
            pesos_count=pesos_count,
            is_leader=False,  # TODO: calculate based on ranking
            in_team=in_team,
        )
        # Show notification for newly unlocked achievements
        if newly_unlocked:
            for logro_id in newly_unlocked:
                logro_info = LOGROS.get(logro_id, {})
                st.toast(f"🎉 ¡Logro desbloqueado! {logro_info.get('icono', '')} {logro_info.get('nombre', '')}", icon="🏆")

        # Create user card container
        with st.container(border=True, key=f"user_card_{usuario_id}"):
            # User card with action buttons
            comm_count = get_comentarios_count(int(usuario_id))
            comm_label = f"💬 ({comm_count})" if comm_count > 0 else "💬"

            col_title, col_chat, col_edit, col_delete = st.columns([2, 1, 1, 1])
            with col_title:
                st.markdown(f"### 👤 {nombre}")
            with col_chat:
                if st.button(comm_label, key=f"chat_{usuario_id}", use_container_width=True, help="Comentarios"):
                    st.session_state[f"chat_open_{usuario_id}"] = not st.session_state.get(f"chat_open_{usuario_id}", False)
            with col_edit:
                if st.button("✏️ Editar", key=f"edit_{usuario_id}", use_container_width=True):
                    st.session_state[f"edit_user_{usuario_id}"] = True
            with col_delete:
                if st.button("🗑️", key=f"delete_{usuario_id}", use_container_width=True, help="Eliminar"):
                    st.session_state[f"confirm_delete_{usuario_id}"] = True

            # Comments section
            if st.session_state.get(f"chat_open_{usuario_id}", False):
                with st.expander(f"💬 Comentarios para {nombre}", expanded=True):
                    # Display existing comments
                    comentarios_df = get_comentarios(int(usuario_id))

                    if comentarios_df.empty:
                        st.caption("Aún no hay comentarios. ¡Sé el primero en motivar! 💪")
                    else:
                        for _, com in comentarios_df.iterrows():
                            from datetime import datetime as dt
                            try:
                                fecha = dt.fromisoformat(com["creado_en"].replace("Z", "+00:00")).strftime("%d %b %H:%M")
                            except Exception:
                                fecha = com["creado_en"][:16]

                            col_com, col_del = st.columns([10, 1])
                            with col_com:
                                st.html(f"""
                                <div class="comentario">
                                    <div class="comentario-header">
                                        <span class="comentario-author">👤 {com['auth_username']}</span>
                                        <span class="comentario-fecha">{fecha}</span>
                                    </div>
                                    <div class="comentario-mensaje">{com['mensaje']}</div>
                                </div>
                                """)
                            with col_del:
                                # Only the author can delete their comment
                                if com["auth_user_id"] == st.session_state.user_id:
                                    if st.button("🗑️", key=f"del_com_{com['id']}", help="Eliminar comentario"):
                                        if delete_comentario(int(com["id"]), st.session_state.user_id):
                                            st.rerun()

                    # New comment form
                    st.markdown("---")
                    with st.form(key=f"add_comment_form_{usuario_id}", clear_on_submit=True):
                        new_msg = st.text_area(
                            f"Escribir comentario para {nombre}",
                            placeholder="Ej: 💪 ¡Vamos campeón!",
                            key=f"new_comment_{usuario_id}",
                            height=80,
                        )
                        submitted = st.form_submit_button("Enviar mensaje 📤", type="primary")
                        if submitted and new_msg.strip():
                            ok, err = add_comentario(
                                int(usuario_id),
                                st.session_state.user_id,
                                st.session_state.username,
                                new_msg.strip()
                            )
                            if ok:
                                # Notify other members
                                notificar_a_miembros_sesion(
                                    sesion_id=int(sesion_id),
                                    exclude_auth_user_id=st.session_state.user_id,
                                    tipo="comentario",
                                    titulo=f"💬 Nuevo comentario en {nombre}",
                                    mensaje=f"{st.session_state.username}: {new_msg.strip()[:80]}",
                                )
                                st.toast("✅ Comentario enviado", icon="💬")
                                st.rerun()
                            else:
                                st.error(f"❌ Error al guardar: {err}")

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

            # Achievements section
            st.html(render_logros(int(usuario_id)))

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
                        # Notify other members
                        diff = nuevo_peso - peso_actual
                        emoji = "📉" if diff < 0 else ("📈" if diff > 0 else "➡️")
                        notificar_a_miembros_sesion(
                            sesion_id=int(sesion_id),
                            exclude_auth_user_id=st.session_state.user_id,
                            tipo="peso",
                            titulo=f"{emoji} Nuevo peso registrado",
                            mensaje=f"{nombre} registró {nuevo_peso:.1f} kg ({diff:+.1f} kg)",
                        )
                        # If reached goal
                        if nuevo_peso <= meta and peso_actual > meta:
                            notificar_a_miembros_sesion(
                                sesion_id=int(sesion_id),
                                exclude_auth_user_id=st.session_state.user_id,
                                tipo="meta",
                                titulo=f"🎯 ¡{nombre} llegó a la meta!",
                                mensaje=f"{nombre} alcanzó su meta de {meta:.1f} kg 🏆",
                            )
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
