# 🌿 Maxi & Belu - Streamlit Edition

Una aplicación web moderna para rastrear el viaje de pérdida de peso en grupo, con soporte para múltiples sesiones independientes. Hecha con **Streamlit y Python**, con arquitectura profesional y modular.

## ✨ Características principales

- **📋 Múltiples sesiones**: Cada pareja (tú + Belu, tu hermano + su esposa, etc.) tiene su propia sesión independiente
- **👥 Gestión de usuarios**: Agrega múltiples usuarios por sesión con sus propias metas
- **📊 Dashboard**: Seguimiento en tiempo real de peso, IMC y progreso
- **📈 Gráficos interactivos**: Visualiza tu progreso semanal con Plotly
- **🍳 Base de recetas**: 17+ recetas organizadas por tipo de comida
- **📅 Plan semanal**: Guía completa de actividades y alimentación
- **💾 Persistencia**: Los datos se guardan en una base de datos SQLite
- **🎨 Interfaz limpia**: Diseño moderno, responsive y profesional
- **🏗️ Arquitectura modular**: Código limpio, separado por responsabilidades

## 🚀 Instalación rápida

### Opción 1: Windows (más fácil)
```bash
# Doble clic en run.bat
# ¡Listo! Se abre automáticamente
```

### Opción 2: Terminal (cualquier SO)
```bash
pip install -r requirements.txt
streamlit run inicio.py
```

### Opción 3: macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

## 📁 Estructura del proyecto

```
maxi-y-belu-streamlit/
├── app.py                     # Punto de entrada principal
├── requirements.txt           # Dependencias (streamlit, pandas, plotly)
├── .streamlit/config.toml     # Configuración de tema
│
├── pages/                     # Páginas de la aplicación (multi-página)
│   ├── 1_📊_dashboard.py     # Dashboard - Tracking de peso
│   ├── 2_📈_grafico.py       # Gráficos - Evolución del peso
│   ├── 3_🍳_recetas.py       # Recetas - Base de datos de comidas
│   └── 4_📅_plan.py          # Plan - Guía semanal y tips
│
├── database/                  # Módulo de base de datos
│   ├── __init__.py
│   └── db.py                 # Todas las funciones SQL (CRUD)
│
├── utils/                     # Módulo de utilidades
│   ├── __init__.py
│   ├── calculations.py       # Cálculos (IMC, progreso, etc)
│   └── constants.py          # Constantes (recetas, plan, tips)
│
├── config/                    # Módulo de configuración
│   └── __init__.py
│
├── data/                      # Datos (creado automáticamente)
│   └── maxi_belu.db          # Base de datos SQLite
│
├── .gitignore
├── run.bat                    # Script para Windows
├── run.sh                     # Script para macOS/Linux
├── README.md                  # Este archivo
└── QUICKSTART.md              # Guía rápida
```

## 📖 Cómo usar

### 1️⃣ Crear una sesión
- En la página de inicio, haz clic en "**➕ Nueva sesión**"
- Ingresa un nombre (ej: "Maxi & Belu", "Carlos & Maria")
- ¡Sesión creada!

### 2️⃣ Agregar usuarios
- Selecciona tu sesión del dropdown
- Ve a la pestaña **📊 Dashboard**
- Haz clic en "**➕ Agregar usuario**"
- Completa nombre, altura, peso inicial y meta

### 3️⃣ Registrar pesos
- En el Dashboard, ingresa el nuevo peso
- Haz clic en "+ Cargar"
- ¡Se actualiza automáticamente!

### 4️⃣ Explorar secciones
- **📊 Dashboard**: Seguimiento de peso y progreso
- **📈 Gráficos**: Evolución en el tiempo
- **🍳 Recetas**: 17+ recetas saludables
- **📅 Plan**: Guía semanal y tips

## 🗄️ Base de datos

Los datos se almacenan en **SQLite** (`data/maxi_belu.db`) con 3 tablas:

```
sesiones
├── id
├── nombre (único)
└── creada_en

usuarios
├── id
├── sesion_id
├── nombre
├── altura
├── meta_peso
└── peso_inicial

pesos
├── id
├── usuario_id
├── peso
├── fecha
└── registrado_en
```

## 💡 Ejemplos de sesiones

**Sesión 1: Tu grupo**
```
Nombre: "Maxi & Belu"
├── Maxi (105 kg → 90 kg)
└── Belu (89.1 kg → 79 kg)
```

**Sesión 2: Hermano**
```
Nombre: "Carlos & Maria"
├── Carlos (120 kg → 100 kg)
└── María (95 kg → 80 kg)
```

Cada sesión es **completamente independiente** ✨

## 📊 Métricas disponibles

Para cada usuario:
- **Peso actual** - Último registrado
- **Peso meta** - Objetivo a alcanzar
- **Faltan** - kg restantes
- **IMC** - Índice de masa corporal + clasificación
- **Progreso** - Porcentaje del camino recorrido
- **Semanas restantes** - Estimado a 0.5 kg/semana
- **Bajada total** - Desde el inicio

## 🎨 Colores y diseño

- **Primario**: Azul (#818cf8)
- **Secundario**: Rosa (#f472b6)
- **Éxito**: Verde (#34d399)
- **Advertencia**: Amarillo (#fbbf24)
- **Fondo**: Gradiente oscuro profesional

## 🔧 Configuración

Puedes personalizar:
- **Colores**: En `.streamlit/config.toml`
- **Recetas**: En `utils/constants.py`
- **Plan y tips**: En `utils/constants.py`
- **Cálculos**: En `utils/calculations.py`

## 📱 Compatibilidad

- ✅ Windows (run.bat)
- ✅ macOS (run.sh)
- ✅ Linux (run.sh)
- ✅ Dispositivos móviles (navegador)

## 🚀 Despliegue en línea (Streamlit Cloud)

1. Sube el proyecto a GitHub (privado o público)
2. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecta tu repositorio
4. ¡Listo! Tu app estará disponible en línea y compartible

## 📚 Tecnologías utilizadas

- **Streamlit**: Framework web para Python
- **Pandas**: Análisis y manipulación de datos
- **Plotly**: Gráficos interactivos
- **SQLite**: Base de datos local

## 🎯 Filosofía del plan

> Sin prohibiciones. Sin contar calorías. Comer bien, moverse, disfrutar.
>
> El déficit viene solo cuando la base es buena. Ustedes van a cocinar rico —
> solo hay que hacer pequeños ajustes inteligentes.

## 💪 Tips importantes

- Actualiza tu peso **semanalmente**
- Ritmo saludable: **0.3-0.5 kg por semana**
- Usa la **misma báscula** siempre
- Pésate en la **mañana**, después de ir al baño
- **Sin ropa** o con la misma siempre
- Se consistente con **actividad física**

## ❓ Preguntas frecuentes

**P: ¿Mis datos son privados?**
R: Sí, se guardan en tu máquina. Nada se envía a servidores externos (a menos que despliegues en la nube).

**P: ¿Cuántas sesiones puedo crear?**
R: Ilimitadas. Cada una es completamente independiente.

**P: ¿Puedo editar pesos registrados?**
R: Directamente en la app no, pero puedes editar la base de datos SQLite manualmente.

**P: ¿Puedo compartir con otros?**
R: Sí, desplegando en Streamlit Cloud obtienes un link compartible.

## 🛠️ Próximas mejoras

- [ ] Exportar datos a Excel/CSV
- [ ] Compartir sesiones con PIN
- [ ] Sistema de autenticación
- [ ] Notificaciones de milestones
- [ ] Historial de cambios
- [ ] Más recetas (40+)

## 📝 Licencia

Proyecto personal. Libre para adaptar a tus necesidades.

---

**¡Actualiza tu peso cada semana · 0.3–0.5 kg por semana es perfecto · ¡van a llegar! 💪**

¿Preguntas? Revisa [QUICKSTART.md](QUICKSTART.md) para una guía rápida de 3 minutos.
