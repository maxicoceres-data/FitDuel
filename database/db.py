"""
Database management for Maxi & Belu
Handles all SQLite operations
"""

import sqlite3
import pandas as pd
import bcrypt
from pathlib import Path

DB_PATH = Path("data/maxi_belu.db")


def init_db():
    """Initialize the database with required tables"""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Usuarios (auth) table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sesiones table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            fecha_inicio DATE,
            fecha_fin DATE,
            competitivo BOOLEAN DEFAULT 1,
            objetivo TEXT,
            creada_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES auth_users(id),
            UNIQUE(usuario_id, nombre)
        )
    """)

    # Usuarios table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            altura REAL NOT NULL,
            meta_peso REAL NOT NULL,
            peso_inicial REAL NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sesion_id) REFERENCES sesiones(id)
        )
    """)

    # Pesos table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pesos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            peso REAL NOT NULL,
            fecha TEXT NOT NULL,
            registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conn.commit()
    conn.close()


def get_sesiones() -> pd.DataFrame:
    """Get all sessions"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sesiones", conn)
    conn.close()
    return df


def create_sesion(nombre: str) -> int | None:
    """Create a new session"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO sesiones (nombre) VALUES (?)", (nombre,))
        conn.commit()
        sesion_id = cursor.lastrowid
        conn.close()
        return sesion_id
    except sqlite3.IntegrityError:
        conn.close()
        return None


def get_usuarios(sesion_id: int) -> pd.DataFrame:
    """Get users for a specific session"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM usuarios WHERE sesion_id = ? ORDER BY id",
        conn,
        params=(sesion_id,),
    )
    conn.close()
    return df


def create_usuario(
    sesion_id: int, nombre: str, altura: float, meta_peso: float, peso_inicial: float
) -> int:
    """Create a new user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (sesion_id, nombre, altura, meta_peso, peso_inicial) VALUES (?, ?, ?, ?, ?)",
        (sesion_id, nombre, altura, meta_peso, peso_inicial),
    )
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    return usuario_id


def get_pesos_usuario(usuario_id: int) -> pd.DataFrame:
    """Get weight history for a user"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM pesos WHERE usuario_id = ? ORDER BY fecha",
        conn,
        params=(usuario_id,),
    )
    conn.close()
    return df


def add_peso(usuario_id: int, peso: float, fecha: str) -> bool:
    """Add a weight record"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pesos (usuario_id, peso, fecha) VALUES (?, ?, ?)",
            (usuario_id, peso, fecha),
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def get_usuario_by_id(usuario_id: int) -> dict | None:
    """Get a specific user by ID"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM usuarios WHERE id = ?",
        conn,
        params=(usuario_id,),
    )
    conn.close()
    if df.empty:
        return None
    return df.iloc[0].to_dict()


# ═════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION FUNCTIONS
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
    # Validate inputs
    if not username or len(username) < 3:
        return False, "El usuario debe tener al menos 3 caracteres"
    if not password or len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO auth_users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        conn.commit()
        conn.close()
        return True, "✅ Usuario registrado exitosamente"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "❌ El usuario ya existe"
    except Exception as e:
        conn.close()
        return False, f"❌ Error: {str(e)}"


def login_user(username: str, password: str) -> tuple[bool, int | None, str]:
    """Login a user. Returns (success, user_id, message)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, password_hash FROM auth_users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return False, None, "❌ Usuario no encontrado"

    user_id, password_hash = result
    if verify_password(password, password_hash):
        return True, user_id, "✅ Inicio de sesión exitoso"
    else:
        return False, None, "❌ Contraseña incorrecta"


def get_sesion_by_id(sesion_id: int) -> dict | None:
    """Get session details by ID"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM sesiones WHERE id = ?",
        conn,
        params=(sesion_id,),
    )
    conn.close()
    if df.empty:
        return None
    return df.iloc[0].to_dict()


def get_sesiones_por_usuario(usuario_id: int) -> pd.DataFrame:
    """Get all sessions for a specific user"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT id, nombre FROM sesiones WHERE usuario_id = ? ORDER BY creada_en DESC",
        conn,
        params=(usuario_id,),
    )
    conn.close()
    return df


def create_sesion_for_user(usuario_id: int, nombre: str, fecha_inicio: str = None, fecha_fin: str = None, competitivo: bool = True, objetivo: str = None) -> int | None:
    """Create a new session for a user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sesiones (usuario_id, nombre, fecha_inicio, fecha_fin, competitivo, objetivo) VALUES (?, ?, ?, ?, ?, ?)",
            (usuario_id, nombre, fecha_inicio, fecha_fin, competitivo, objetivo),
        )
        conn.commit()
        sesion_id = cursor.lastrowid
        conn.close()
        return sesion_id
    except sqlite3.IntegrityError:
        conn.close()
        return None
    except Exception:
        conn.close()
        return None


def update_usuario(usuario_id: int, nombre: str = None, altura: float = None, meta_peso: float = None) -> bool:
    """Update user information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        updates = []
        params = []

        if nombre is not None:
            updates.append("nombre = ?")
            params.append(nombre)
        if altura is not None:
            updates.append("altura = ?")
            params.append(altura)
        if meta_peso is not None:
            updates.append("meta_peso = ?")
            params.append(meta_peso)

        if not updates:
            conn.close()
            return False

        params.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def delete_usuario(usuario_id: int) -> bool:
    """Delete a user and all their weight records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Delete weight records first
        cursor.execute("DELETE FROM pesos WHERE usuario_id = ?", (usuario_id,))
        # Delete user
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def update_sesion(sesion_id: int, nombre: str = None, fecha_inicio = None, fecha_fin = None, competitivo: bool = None, objetivo: str = None) -> bool:
    """Update session information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        updates = []
        params = []

        if nombre is not None:
            updates.append("nombre = ?")
            params.append(nombre)
        if fecha_inicio is not None:
            updates.append("fecha_inicio = ?")
            params.append(fecha_inicio)
        if fecha_fin is not None:
            updates.append("fecha_fin = ?")
            params.append(fecha_fin)
        if competitivo is not None:
            updates.append("competitivo = ?")
            params.append(competitivo)
        if objetivo is not None:
            updates.append("objetivo = ?")
            params.append(objetivo)

        if not updates:
            conn.close()
            return False

        params.append(sesion_id)
        query = f"UPDATE sesiones SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def delete_sesion(sesion_id: int) -> bool:
    """Delete a session and all related users and weight records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Get all usuarios in this sesion
        cursor.execute("SELECT id FROM usuarios WHERE sesion_id = ?", (sesion_id,))
        usuarios = cursor.fetchall()

        # Delete weight records for each user
        for usuario in usuarios:
            cursor.execute("DELETE FROM pesos WHERE usuario_id = ?", (usuario[0],))

        # Delete usuarios
        cursor.execute("DELETE FROM usuarios WHERE sesion_id = ?", (sesion_id,))

        # Delete sesion
        cursor.execute("DELETE FROM sesiones WHERE id = ?", (sesion_id,))

        conn.commit()
        conn.close()
        return True
    except Exception:
        conn.close()
        return False
