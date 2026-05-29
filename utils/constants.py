"""
Constants for Maxi & Belu
Recipes, plan, and tips data
"""

TIPS = [
    "🥗 Coman despacio — el cerebro tarda 20 min en sentirse lleno",
    "🍳 Cocinar en casa ya es el 80% del éxito",
    "🚶 Caminar después de comer baja el pico de azúcar",
    "💧 A veces el hambre es sed — prueben un vaso de agua primero",
    "🍽️ Plato más chico = misma satisfacción, menos calorías",
    "🌙 Cenar temprano mejora el descanso y el metabolismo",
    "🫀 El músculo quema calorías en reposo — caminar lo activa",
    "🎉 Un día fuera del plan no arruina el proceso, ¡relax!",
]

PLAN = [
    {"dia": "Lunes", "act": "🚶 Caminata 30–40 min", "com": "Proteína + verduras salteadas"},
    {"dia": "Martes", "act": "😴 Descanso activo (stretching)", "com": "Pasta integral + ensalada"},
    {"dia": "Miércoles", "act": "🚶 Caminata 40–50 min", "com": "Pollo / pescado + legumbres"},
    {"dia": "Jueves", "act": "🚶 Caminata 30 min", "com": "Libre (sin excesos)"},
    {"dia": "Viernes", "act": "😴 Descanso", "com": "Lo que tengan ganas"},
    {"dia": "Sábado", "act": "🚶 Caminata larga 60 min", "com": "Disfruten — cocinen algo rico"},
    {"dia": "Domingo", "act": "🚶 Paseo tranquilo", "com": "Liviano, preparar la semana"},
]

PLAN_TIPS = [
    "Más proteína en cada plato → más saciedad",
    "Verduras: la mitad del plato, siempre",
    "Pan, pasta, arroz: sí, pero en moderación",
    "Alcohol: 1-2 veces por semana máximo",
    "Snacks: frutas, nueces, yogur natural",
    "Hidratación: 2L de agua por día c/u",
]

DESAYUNOS = [
    {
        "nombre": "Avena cremosa con banana y miel",
        "emoji": "🥣",
        "tiempo": "10 min",
        "dificultad": "Fácil",
        "calorias": "~320 kcal",
        "ingredientes": ["Avena arrollada", "Leche (o leche vegetal)", "Banana", "Miel", "Canela", "Nueces"],
        "pasos": [
            "Cocinar la avena en leche a fuego medio revolviendo.",
            "Agregar canela y una cucharadita de miel.",
            "Servir con banana en rodajas y nueces por arriba.",
        ],
        "tip": "Podés dejarlo preparado la noche anterior en la heladera (overnight oats) y en la mañana solo agregás la fruta.",
    },
    {
        "nombre": "Tostadas integrales con ricota y mermelada",
        "emoji": "🍞",
        "tiempo": "5 min",
        "dificultad": "Fácil",
        "calorias": "~270 kcal",
        "ingredientes": ["Pan integral", "Ricota descremada", "Mermelada sin azúcar", "Semillas de chía", "Café o té"],
        "pasos": ["Tostar el pan.", "Untar generosamente con ricota.", "Sumar una cucharadita de mermelada y espolvorear chía."],
        "tip": "La ricota tiene proteína que te mantiene satisfecho hasta el almuerzo, mucho mejor que solo mermelada.",
    },
    {
        "nombre": "Yogur con granola y frutos rojos",
        "emoji": "🫐",
        "tiempo": "5 min",
        "dificultad": "Fácil",
        "calorias": "~290 kcal",
        "ingredientes": ["Yogur natural o griego", "Granola sin azúcar", "Frutos rojos (frescos o congelados)", "Miel", "Semillas"],
        "pasos": ["Poner el yogur en un bowl.", "Agregar granola, frutos rojos y un hilo de miel.", "Mezclar o comer en capas."],
        "tip": "El yogur griego tiene el doble de proteína que el común — más saciedad con menos cantidad.",
    },
]

ALMUERZOS = [
    {
        "nombre": "Pollo al limón con papas al horno",
        "emoji": "🍋",
        "tiempo": "45 min",
        "dificultad": "Fácil",
        "calorias": "~420 kcal",
        "ingredientes": ["Pechuga de pollo", "Papas", "Limón", "Ajo", "Romero", "Aceite de oliva"],
        "pasos": [
            "Cortar papas en cubos y condimentar con aceite, ajo y romero.",
            "Adobar el pollo con jugo de limón, sal y pimienta.",
            "Hornear todo junto a 200°C por 35-40 min.",
        ],
        "tip": "Las papas quedan más crocantes si las ponés en la bandeja sin amontonar.",
    },
    {
        "nombre": "Wok de verduras con arroz integral",
        "emoji": "🥦",
        "tiempo": "25 min",
        "dificultad": "Fácil",
        "calorias": "~320 kcal",
        "ingredientes": ["Arroz integral", "Brócoli", "Zanahoria", "Morrón", "Salsa de soja", "Jengibre"],
        "pasos": [
            "Cocinar el arroz integral según el paquete.",
            "Saltear las verduras a fuego fuerte con un chorrito de aceite.",
            "Agregar salsa de soja y jengibre rallado al final.",
        ],
        "tip": "El secreto es fuego bien fuerte para que las verduras queden crocantes.",
    },
]

MERIENDAS = [
    {
        "nombre": "Manzana con mantequilla de maní",
        "emoji": "🍎",
        "tiempo": "3 min",
        "dificultad": "Fácil",
        "calorias": "~200 kcal",
        "ingredientes": ["1 manzana", "2 cdas. mantequilla de maní natural", "Canela opcional"],
        "pasos": ["Cortar la manzana en gajos.", "Untarlos con mantequilla de maní.", "Espolvorear canela si querés."],
        "tip": "La mezcla dulce + grasa + fibra es una de las más saciantes para la tarde.",
    },
    {
        "nombre": "Tostadas con palta y semillas",
        "emoji": "🥑",
        "tiempo": "5 min",
        "dificultad": "Fácil",
        "calorias": "~230 kcal",
        "ingredientes": ["Pan integral", "1/2 palta", "Jugo de limón", "Sal marina", "Semillas de girasol o zapallo"],
        "pasos": ["Tostar el pan.", "Pisar la palta con limón y sal.", "Untar y espolvorear semillas."],
        "tip": "Rápida, saciante y llena de grasas buenas. Ideal si la tarde se hace larga.",
    },
]
