# 🔐 Sistema de Login - Maxi & Belu

## ¿Qué es nuevo?

Ahora la app tiene un **sistema de autenticación seguro** para que cada pareja pueda tener sus propias sesiones completamente separadas y privadas.

## 🔑 Cómo funciona

### Estructura de usuarios

```
Usuario 1 (Maxi)
├── Sesión "Maxi & Belu"
│   ├── Usuario: Maxi (105 kg → 90 kg)
│   └── Usuario: Belu (89.1 kg → 79 kg)
└── (otras sesiones opcionales)

Usuario 2 (Carlos)
├── Sesión "Carlos & Maria"
│   ├── Usuario: Carlos (120 kg → 100 kg)
│   └── Usuario: Maria (95 kg → 80 kg)
└── (otras sesiones opcionales)
```

Cada usuario ve **solo sus propias sesiones** ✨

## 📋 Primeros pasos

### Paso 1: Registrarse (primera vez)
1. Abre la app
2. Ve a la pestaña **🔐 Login**
3. Selecciona **📝 Registrarse**
4. Completa:
   - **Usuario**: Tu nombre o apodo (mín 3 caracteres)
   - **Email**: Opcional
   - **Contraseña**: Mín 6 caracteres
   - **Confirmar contraseña**: Debe coincidir
5. Haz clic en **📝 Registrarse**

### Paso 2: Iniciar sesión
1. Vuelve a la pestaña **🔓 Iniciar sesión**
2. Ingresa tu usuario y contraseña
3. Haz clic en **🔓 Iniciar sesión**
4. ¡Listo! Ya estás dentro

### Paso 3: Crear sesiones
1. Selecciona "➕ Nueva sesión"
2. Ingresa el nombre (ej: "Maxi & Belu")
3. Haz clic en "Crear sesión"
4. ¡Ahora puedes agregar usuarios a esta sesión!

## 🔒 Seguridad

### ¿Cómo se guardan las contraseñas?

Las contraseñas se **hashean con bcrypt**, un algoritmo criptográfico seguro:

```
Tu contraseña: "miContraseña123"
        ↓ (bcrypt)
Hash guardado: "$2b$12$abcdefghijklmnopqrstuvwxyz..."
```

- ✅ Las contraseñas NO se guardan en texto plano
- ✅ Imposible recuperar la contraseña original
- ✅ Cada contraseña tiene un hash único

### ¿Quién puede ver mis sesiones?

Solo **tú** con tu usuario y contraseña.

Tu hermano con su usuario verá solo sus sesiones, nunca las tuyas.

## 👥 Ejemplo de uso con múltiples parejas

### Tú y Belu
```
Usuario: maxi
Contraseña: tuContraseña123
  └── Sesión "Maxi & Belu"
      ├── Maxi
      └── Belu
```

### Tu hermano y su esposa
```
Usuario: carlos
Contraseña: suContraseña456
  └── Sesión "Carlos & Maria"
      ├── Carlos
      └── Maria
```

Completamente separado. Ninguno ve las sesiones del otro.

## 🔄 Flujo de la app

```
1. Abre la app
   ↓
2. ¿Tienes cuenta?
   ├─ SÍ → Inicia sesión
   └─ NO → Regístrate
   ↓
3. Selecciona una sesión tuya
   ↓
4. Maneja tus usuarios y pesos
```

## ⚙️ Gestión de cuenta

### Cambiar contraseña (próxima versión)
- Aún no está implementado
- Por ahora, contacta al admin

### Eliminar cuenta (próxima versión)
- Aún no está implementado
- Se eliminarían todas tus sesiones y datos

### Cerrar sesión
- Haz clic en **🚪 Logout** en la esquina superior derecha
- Tendrás que iniciar sesión de nuevo

## ❓ Preguntas frecuentes

**P: ¿Puedo cambiar mi usuario/contraseña?**
R: No por ahora. Se agregará en la próxima versión.

**P: ¿Qué pasa si olvido mi contraseña?**
R: Aún no hay recuperación. Contacta al admin. (Se agregará recovery por email)

**P: ¿Puedo tener múltiples cuentas?**
R: Sí, registra otro usuario diferente.

**P: ¿Se pueden compartir cuentas?**
R: Técnicamente sí, pero no es recomendable. Mejor que cada uno tenga su propia cuenta.

**P: ¿Dónde se guardan las contraseñas?**
R: En la base de datos SQLite local (`data/maxi_belu.db`), hasheadas con bcrypt.

**P: ¿Mi contraseña se envía a un servidor?**
R: No. Todo se procesa localmente. Nada se envía a internet.

## 🛡️ Mejores prácticas

1. **Usa una contraseña fuerte**
   - ❌ "123456" o "password"
   - ✅ "MiContraseña#2024Segura"

2. **No compartas tu contraseña**
   - Cada uno debe tener su propia cuenta

3. **Cierra sesión en computadoras públicas**
   - Haz clic en **🚪 Logout** cuando termines

4. **Mantén la BD segura**
   - El archivo `data/maxi_belu.db` contiene tus datos
   - Haz backup regularmente

## 🔐 Próximas mejoras de seguridad

- [ ] Cambio de contraseña
- [ ] Recuperación por email
- [ ] Autenticación de dos factores (2FA)
- [ ] Historial de intentos de login
- [ ] Expiración de sesiones

---

**¡Tu privacidad es importante! Cada uno con su cuenta, cada uno con sus sesiones.** 🔒
