# ⚡ Quick Start - Guía rápida

## Instalación ultrarrápida (3 minutos)

### Windows
1. Descarga o clona el proyecto
2. Doble clic en `run.bat`
3. ¡Listo! Se abre automáticamente en `http://localhost:8501`

### macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

### Terminal (cualquier SO)
```bash
pip install -r requirements.txt
streamlit run inicio.py
```

## Primeros pasos

### Paso 1: Crear tu sesión (30 segundos)
```
1. Haz clic en "➕ Nueva sesión"
2. Escribe el nombre (ej: "Maxi & Belu")
3. Presiona "Crear sesión"
```

### Paso 2: Agregar a las personas (2 minutos)
Para **Maxi**:
- Nombre: Maxi
- Altura: 1.76 m
- Peso inicial: 105 kg
- Meta: 90 kg

Para **Belu**:
- Nombre: Belu
- Altura: 1.78 m
- Peso inicial: 89.1 kg
- Meta: 79 kg

### Paso 3: Registrar el primer peso (1 minuto)
- Ingresa el peso actual en cada campo
- Haz clic en "+ Cargar"
- ¡Tu progreso se actualiza automáticamente!

## Ejemplo de sesiones

### Sesión 1: Tu grupo
```
Sesión: "Maxi & Belu"
├── Maxi (105 kg → 90 kg)
└── Belu (89.1 kg → 79 kg)
```

### Sesión 2: Hermano
```
Sesión: "Carlos & Maria"
├── Carlos (120 kg → 100 kg)
└── María (95 kg → 80 kg)
```

Cada sesión es **completamente independiente** ✨

## Datos útiles

| Concepto | Valor |
|----------|-------|
| Ritmo recomendado | 0.3-0.5 kg/semana |
| Frecuencia de pesada | 1 vez por semana |
| Mejor momento | Misma hora, mismo día |
| Meta realista | 8-16 semanas según meta |

## Atajos útiles

| Acción | Atajo |
|--------|-------|
| Recargar datos | F5 o Ctrl+R |
| Cambiar sesión | Dropdown arriba |
| Agregar usuario | Botón verde ➕ |
| Registrar peso | Botón "+ Cargar" |

## ❓ Problemas comunes

### "No se abre la app"
```bash
# En terminal/CMD, manualmente:
pip install -r requirements.txt
streamlit run app.py
```

### "Dice que ya existe la sesión"
- Los nombres de sesiones son únicos
- Usa un nombre diferente (ej: "Maxi & Belu v2")

### "No veo mis datos"
- Verifica que hayas seleccionado la sesión correcta en el dropdown
- Recarga la página (F5)

### "Quiero editar un peso"
- Por ahora no hay edición directa
- Puedes usar DB Browser para SQLite
- O contacta al developer 😄

## 🎯 Primer mes - Meta

### Semana 1
- ✅ Crea tu sesión
- ✅ Agrega a los usuarios
- ✅ Registra el peso inicial

### Semana 2-4
- 📊 Registra peso cada semana
- 📈 Mira tu gráfico crecer
- 💪 Mantén la consistencia

### Mes siguiente
- 🎉 Celebra el progreso
- 🔀 Rota recetas
- 📅 Consulta el plan

## 💡 Pro tips

1. **Básculas**: Usa la misma báscula siempre (pueden variar 1-2 kg)
2. **Hora**: Pésate en la mañana, después de ir al baño
3. **Ropa**: Sin ropa o con la misma ropa siempre
4. **Sesiones**: Crea una sesión por grupo de personas
5. **Datos**: Los datos se guardan automáticamente en SQLite

## 📊 Dashboard - Qué significa cada métrica

```
┌─────────────────────────────────────┐
│  Hoy: 103 kg                        │  ← Tu peso actual registrado
│  Meta: 90 kg                        │  ← Tu objetivo
│  Faltan: 13 kg                      │  ← Para alcanzar la meta
├─────────────────────────────────────┤
│  Progreso: 46.7%                    │  ← % del camino recorrido
├─────────────────────────────────────┤
│  IMC: 33.1 - Sobrepeso              │  ← Índice de masa corporal
│  Semanas restantes: ~26             │  ← Estimado a 0.5 kg/semana
│  Ya bajó: 2 kg                      │  ← Desde el inicio
└─────────────────────────────────────┘
```

## 🚀 Siguiente nivel

Cuando domines esto, puedes:

- Agregar más sesiones para otros grupos
- Usar la API de Streamlit para integrar datos
- Exportar datos a Excel
- Compartir sesiones con código de acceso
- Conectar a una base de datos en la nube

## 📱 Acceso desde múltiples dispositivos

Como Streamlit corre localmente en tu máquina, solo puedes acceder desde:
- Tu computadora (localhost:8501)

Si quieres compartir con otros, puedes:
1. Desplegar en Streamlit Cloud (gratis)
2. Compartir la laptop con acceso a la app
3. Usar un servicio como ngrok para exponer la app

## ✨ ¡Comenzar ahora!

```bash
# Windows
run.bat

# macOS/Linux
./run.sh
```

**¡Actualiza tu peso cada semana y mira cómo el gráfico muestra tu progreso! 💪**
