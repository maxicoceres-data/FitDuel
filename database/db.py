"""
Database management for FitDuel
Now using Supabase (PostgreSQL cloud)
"""

import pandas as pd
import bcrypt
import streamlit as st
from supabase import create_client, Client


# ═════════════════════════════════════════════════════════════════════════════
# SUPABASE CLIENT
# ═════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_supabase() -> Client:
    """Get or create Supabase client"""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def init_db():
    """No-op for Supabase - tables are created via SQL"""
    pass


# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═════════════════════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def register_user(username: str, password: str, email: str = "") -> tuple[bool, str]:
    """Register a new user. Returns (success, message)"""
    if not username or len(username) < 3:
        return False, "El usuario debe tener al menos 3 caracteres"
    if not password or len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"

    supabase = get_supabase()
    try:
        password_hash = hash_password(password)
        result = supabase.table("auth_users").insert({
            "username": username,
            "password_hash": password_hash,
            "email": email,
        }).execute()
        return True, "✅ Usuario registrado exitosamente"
    except Exception as e:
        error_msg = str(e)
        if "duplicate" in error_msg.lower() or "unique" in error_msg.lower():
            return False, "❌ El usuario ya existe"
        return False, f"❌ Error: {error_msg}"


def login_user(username: str, password: str) -> tuple[bool, int | None, str]:
    """Login a user. Returns (success, user_id, message)"""
    supabase = get_supabase()
    try:
        result = supabase.table("auth_users").select("id, password_hash").eq("username", username).execute()
        if not result.data:
            return False, None, "❌ Usuario no encontrado"

        user_data = result.data[0]
        user_id = user_data["id"]
        password_hash = user_data["password_hash"]

        if verify_password(password, password_hash):
            return True, user_id, "✅ Inicio de sesión exitoso"
        return False, None, "❌ Contraseña incorrecta"
    except Exception as e:
        return False, None, f"❌ Error: {str(e)}"


# ═════════════════════════════════════════════════════════════════════════════
# SESIONES
# ═════════════════════════════════════════════════════════════════════════════

def get_sesiones() -> pd.DataFrame:
    """Get all sessions"""
    supabase = get_supabase()
    result = supabase.table("sesiones").select("*").execute()
    return pd.DataFrame(result.data) if result.data else pd.DataFrame()


def create_sesion(nombre: str) -> int | None:
    """Create a new session (legacy)"""
    supabase = get_supabase()
    try:
        result = supabase.table("sesiones").insert({"nombre": nombre}).execute()
        return result.data[0]["id"] if result.data else None
    except Exception:
        return None


def get_sesion_by_id(sesion_id: int) -> dict | None:
    """Get session details by ID"""
    supabase = get_supabase()
    try:
        result = supabase.table("sesiones").select("*").eq("id", sesion_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


def get_sesiones_por_usuario(usuario_id: int) -> pd.DataFrame:
    """Get all sessions where user is owner OR member"""
    supabase = get_supabase()
    try:
        # Sesiones donde es owner
        own_result = supabase.table("sesiones").select("id, nombre").eq("usuario_id", usuario_id).execute()

        # Sesiones donde es miembro
        member_result = supabase.table("sesion_miembros").select("sesion_id").eq("auth_user_id", usuario_id).execute()

        all_sessions = []
        if own_result.data:
            all_sessions.extend(own_result.data)

        if member_result.data:
            member_sesion_ids = [m["sesion_id"] for m in member_result.data]
            if member_sesion_ids:
                member_sesiones = supabase.table("sesiones").select("id, nombre").in_("id", member_sesion_ids).execute()
                if member_sesiones.data:
                    # Evitar duplicados
                    existing_ids = {s["id"] for s in all_sessions}
                    for s in member_sesiones.data:
                        if s["id"] not in existing_ids:
                            all_sessions.append(s)

        return pd.DataFrame(all_sessions) if all_sessions else pd.DataFrame(columns=["id", "nombre"])
    except Exception:
        return pd.DataFrame(columns=["id", "nombre"])


def create_sesion_for_user(usuario_id: int, nombre: str, fecha_inicio: str = None,
                           fecha_fin: str = None, competitivo: bool = True,
                           objetivo: str = None) -> int | None:
    """Create a new session for a user"""
    supabase = get_supabase()
    try:
        data = {
            "usuario_id": usuario_id,
            "nombre": nombre,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "competitivo": competitivo,
            "objetivo": objetivo,
        }
        result = supabase.table("sesiones").insert(data).execute()
        return result.data[0]["id"] if result.data else None
    except Exception:
        return None


def update_sesion(sesion_id: int, nombre: str = None, fecha_inicio=None,
                  fecha_fin=None, competitivo: bool = None, objetivo: str = None) -> bool:
    """Update session information"""
    supabase = get_supabase()
    try:
        updates = {}
        if nombre is not None:
            updates["nombre"] = nombre
        if fecha_inicio is not None:
            updates["fecha_inicio"] = fecha_inicio
        if fecha_fin is not None:
            updates["fecha_fin"] = fecha_fin
        if competitivo is not None:
            updates["competitivo"] = competitivo
        if objetivo is not None:
            updates["objetivo"] = objetivo

        if not updates:
            return False

        supabase.table("sesiones").update(updates).eq("id", sesion_id).execute()
        return True
    except Exception:
        return False


def delete_sesion(sesion_id: int) -> bool:
    """Delete a session and cascade everything"""
    supabase = get_supabase()
    try:
        # CASCADE in Supabase elimina automáticamente usuarios y pesos
        supabase.table("sesiones").delete().eq("id", sesion_id).execute()
        return True
    except Exception:
        return False


# ═════════════════════════════════════════════════════════════════════════════
# USUARIOS (participantes en sesiones)
# ═════════════════════════════════════════════════════════════════════════════

def get_usuarios(sesion_id: int) -> pd.DataFrame:
    """Get users for a specific session"""
    supabase = get_supabase()
    try:
        result = supabase.table("usuarios").select("*").eq("sesion_id", sesion_id).order("id").execute()
        return pd.DataFrame(result.data) if result.data else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def create_usuario(sesion_id: int, nombre: str, altura: float,
                   meta_peso: float, peso_inicial: float) -> int | None:
    """Create a new participant in a session"""
    supabase = get_supabase()
    try:
        result = supabase.table("usuarios").insert({
            "sesion_id": sesion_id,
            "nombre": nombre,
            "altura": altura,
            "meta_peso": meta_peso,
            "peso_inicial": peso_inicial,
        }).execute()
        return result.data[0]["id"] if result.data else None
    except Exception:
        return None


def get_usuario_by_id(usuario_id: int) -> dict | None:
    """Get a specific user by ID"""
    supabase = get_supabase()
    try:
        result = supabase.table("usuarios").select("*").eq("id", usuario_id).execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


def update_usuario(usuario_id: int, nombre: str = None, altura: float = None,
                   meta_peso: float = None) -> bool:
    """Update user information"""
    supabase = get_supabase()
    try:
        updates = {}
        if nombre is not None:
            updates["nombre"] = nombre
        if altura is not None:
            updates["altura"] = altura
        if meta_peso is not None:
            updates["meta_peso"] = meta_peso

        if not updates:
            return False

        supabase.table("usuarios").update(updates).eq("id", usuario_id).execute()
        return True
    except Exception:
        return False


def delete_usuario(usuario_id: int) -> bool:
    """Delete a user and all their weight records (CASCADE)"""
    supabase = get_supabase()
    try:
        supabase.table("usuarios").delete().eq("id", usuario_id).execute()
        return True
    except Exception:
        return False


# ═════════════════════════════════════════════════════════════════════════════
# PESOS
# ═════════════════════════════════════════════════════════════════════════════

def get_pesos_usuario(usuario_id: int) -> pd.DataFrame:
    """Get weight history for a user"""
    supabase = get_supabase()
    try:
        result = supabase.table("pesos").select("*").eq("usuario_id", usuario_id).order("fecha").execute()
        return pd.DataFrame(result.data) if result.data else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def add_peso(usuario_id: int, peso: float, fecha: str) -> bool:
    """Add a weight record"""
    supabase = get_supabase()
    try:
        supabase.table("pesos").insert({
            "usuario_id": usuario_id,
            "peso": peso,
            "fecha": fecha,
        }).execute()
        return True
    except Exception:
        return False


# ═════════════════════════════════════════════════════════════════════════════
# MIEMBROS DE SESIONES (sesiones compartidas)
# ═════════════════════════════════════════════════════════════════════════════

def add_miembro_sesion(sesion_id: int, username: str) -> tuple[bool, str]:
    """Add a user as member of a session by username"""
    supabase = get_supabase()
    try:
        # Buscar el usuario por username
        user_result = supabase.table("auth_users").select("id").eq("username", username).execute()
        if not user_result.data:
            return False, "❌ Usuario no encontrado"

        auth_user_id = user_result.data[0]["id"]

        # Verificar que no sea ya miembro
        existing = supabase.table("sesion_miembros").select("id").eq("sesion_id", sesion_id).eq("auth_user_id", auth_user_id).execute()
        if existing.data:
            return False, "❌ Este usuario ya es miembro del desafío"

        # Agregar como miembro
        supabase.table("sesion_miembros").insert({
            "sesion_id": sesion_id,
            "auth_user_id": auth_user_id,
        }).execute()
        return True, f"✅ Usuario '{username}' agregado al desafío"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_miembros_sesion(sesion_id: int) -> pd.DataFrame:
    """Get all members of a session (owner + invited)"""
    supabase = get_supabase()
    try:
        # Obtener owner
        sesion_result = supabase.table("sesiones").select("usuario_id").eq("id", sesion_id).execute()

        members = []
        if sesion_result.data:
            owner_id = sesion_result.data[0]["usuario_id"]
            owner_info = supabase.table("auth_users").select("id, username").eq("id", owner_id).execute()
            if owner_info.data:
                members.append({
                    "auth_user_id": owner_info.data[0]["id"],
                    "username": owner_info.data[0]["username"],
                    "rol": "👑 Owner"
                })

        # Obtener miembros invitados
        miembros_result = supabase.table("sesion_miembros").select("auth_user_id").eq("sesion_id", sesion_id).execute()
        if miembros_result.data:
            member_ids = [m["auth_user_id"] for m in miembros_result.data]
            if member_ids:
                users_info = supabase.table("auth_users").select("id, username").in_("id", member_ids).execute()
                if users_info.data:
                    for user in users_info.data:
                        members.append({
                            "auth_user_id": user["id"],
                            "username": user["username"],
                            "rol": "👤 Miembro"
                        })

        return pd.DataFrame(members) if members else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def remove_miembro_sesion(sesion_id: int, auth_user_id: int) -> bool:
    """Remove a member from a session"""
    supabase = get_supabase()
    try:
        supabase.table("sesion_miembros").delete().eq("sesion_id", sesion_id).eq("auth_user_id", auth_user_id).execute()
        return True
    except Exception:
        return False
