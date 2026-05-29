"""
Calculation utilities for Maxi & Belu
"""


def calcular_imc(peso: float, altura: float) -> float:
    """Calculate BMI"""
    return round(peso / (altura ** 2), 1)


def clasificar_imc(imc: float) -> tuple[str, str]:
    """Classify BMI and return category and color"""
    if imc < 18.5:
        return "Bajo peso", "#60a5fa"
    elif imc < 25:
        return "Normal", "#34d399"
    elif imc < 30:
        return "Sobrepeso", "#fbbf24"
    else:
        return "Obesidad I", "#f87171"


def calcular_progreso(peso_actual: float, peso_inicial: float, meta_peso: float) -> float:
    """Calculate progress percentage"""
    if peso_inicial == meta_peso:
        return 0.0
    return max(0.0, min(100.0, ((peso_inicial - peso_actual) / (peso_inicial - meta_peso)) * 100))


def calcular_semanas_restantes(peso_actual: float, meta_peso: float) -> int:
    """Calculate estimated weeks remaining at 0.5 kg/week pace"""
    kg_restantes = max(0, peso_actual - meta_peso)
    return max(0, int(kg_restantes / 0.5))


def calcular_bajada(peso_inicial: float, peso_actual: float) -> float:
    """Calculate total weight loss"""
    return round(peso_inicial - peso_actual, 1)


def calcular_falta(peso_actual: float, meta_peso: float) -> float:
    """Calculate remaining weight to lose"""
    return round(max(0, peso_actual - meta_peso), 1)
