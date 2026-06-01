"""
Logros / Achievements system for FitDuel
"""

from database.db import get_supabase

# Definition of all available achievements
LOGROS = {
    "primer_paso": {
        "icono": "🥉",
        "nombre": "Primer Paso",
        "descripcion": "Registraste tu primer peso",
    },
    "constante": {
        "icono": "📅",
        "nombre": "Constante",
        "descripcion": "3 registros realizados",
    },
    "imparable": {
        "icono": "🔥",
        "nombre": "Imparable",
        "descripcion": "7 días seguidos registrando",
    },
    "primer_kg": {
        "icono": "💪",
        "nombre": "Primer Kg",
        "descripcion": "Bajaste tu primer kg",
    },
    "cinco_kg": {
        "icono": "🎯",
        "nombre": "5kg Menos",
        "descripcion": "Bajaste 5kg en total",
    },
    "diez_kg": {
        "icono": "🏆",
        "nombre": "10kg Menos",
        "descripcion": "Bajaste 10kg en total",
    },
    "mitad_camino": {
        "icono": "⭐",
        "nombre": "Mitad del Camino",
        "descripcion": "50% del progreso a la meta",
    },
    "campeon": {
        "icono": "👑",
        "nombre": "Campeón",
        "descripcion": "Llegaste a la meta",
    },
    "lider": {
        "icono": "🥇",
        "nombre": "Líder",
        "descripcion": "Estás 1ro en el ranking",
    },
    "en_equipo": {
        "icono": "🤝",
        "nombre": "En Equipo",
        "descripcion": "Te uniste a un desafío",
    },
}


def get_logros_usuario(usuario_id: int) -> list[str]:
    """Get all unlocked achievement IDs for a user"""
    supabase = get_supabase()
    try:
        result = supabase.table("logros_desbloqueados").select("logro_id").eq("usuario_id", usuario_id).execute()
        return [r["logro_id"] for r in result.data] if result.data else []
    except Exception:
        return []


def desbloquear_logro(usuario_id: int, logro_id: str) -> bool:
    """Unlock an achievement for a user. Returns True if it was newly unlocked."""
    if logro_id not in LOGROS:
        return False

    supabase = get_supabase()
    try:
        # Check if already unlocked
        existing = supabase.table("logros_desbloqueados").select("id").eq("usuario_id", usuario_id).eq("logro_id", logro_id).execute()
        if existing.data:
            return False

        # Unlock it
        supabase.table("logros_desbloqueados").insert({
            "usuario_id": usuario_id,
            "logro_id": logro_id,
        }).execute()
        return True
    except Exception:
        return False


def evaluar_logros(usuario_id: int, peso_inicial: float, peso_actual: float,
                   meta_peso: float, pesos_count: int, is_leader: bool = False,
                   in_team: bool = False) -> list[str]:
    """
    Evaluate which achievements a user has earned.
    Returns list of newly unlocked achievement IDs.
    """
    newly_unlocked = []
    current_logros = set(get_logros_usuario(usuario_id))

    bajada = peso_inicial - peso_actual
    progreso = (bajada / (peso_inicial - meta_peso) * 100) if peso_inicial > meta_peso else 0

    # primer_paso: First weight registered
    if pesos_count >= 1 and "primer_paso" not in current_logros:
        if desbloquear_logro(usuario_id, "primer_paso"):
            newly_unlocked.append("primer_paso")

    # constante: 3 records
    if pesos_count >= 3 and "constante" not in current_logros:
        if desbloquear_logro(usuario_id, "constante"):
            newly_unlocked.append("constante")

    # imparable: 7 records
    if pesos_count >= 7 and "imparable" not in current_logros:
        if desbloquear_logro(usuario_id, "imparable"):
            newly_unlocked.append("imparable")

    # primer_kg: lost first kg
    if bajada >= 1 and "primer_kg" not in current_logros:
        if desbloquear_logro(usuario_id, "primer_kg"):
            newly_unlocked.append("primer_kg")

    # cinco_kg: lost 5kg
    if bajada >= 5 and "cinco_kg" not in current_logros:
        if desbloquear_logro(usuario_id, "cinco_kg"):
            newly_unlocked.append("cinco_kg")

    # diez_kg: lost 10kg
    if bajada >= 10 and "diez_kg" not in current_logros:
        if desbloquear_logro(usuario_id, "diez_kg"):
            newly_unlocked.append("diez_kg")

    # mitad_camino: 50% progress
    if progreso >= 50 and "mitad_camino" not in current_logros:
        if desbloquear_logro(usuario_id, "mitad_camino"):
            newly_unlocked.append("mitad_camino")

    # campeon: reached goal
    if peso_actual <= meta_peso and "campeon" not in current_logros:
        if desbloquear_logro(usuario_id, "campeon"):
            newly_unlocked.append("campeon")

    # lider: first in ranking
    if is_leader and "lider" not in current_logros:
        if desbloquear_logro(usuario_id, "lider"):
            newly_unlocked.append("lider")

    # en_equipo: joined a team
    if in_team and "en_equipo" not in current_logros:
        if desbloquear_logro(usuario_id, "en_equipo"):
            newly_unlocked.append("en_equipo")

    return newly_unlocked
