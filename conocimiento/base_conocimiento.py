# base_conocimiento.py
# ======================================
# BASE DE CONOCIMIENTO - Políticas Crediticias (BCP-style)
# ======================================

from rule_engine import Rule

"""
Políticas basadas en criterios de precalificación utilizados en banca retail peruana.
Las expresiones deben ser compatibles con rule-engine (usa sintaxis tipo Python/JSON).
"""

reglas = [
    {
        "codigo": "R1",
        "expresion": "edad >= 21 and edad <= 70",
        "descripcion": "El cliente debe tener entre 21 y 70 años para acceder a créditos personales.",
        "severidad": "alta",
        "recomendacion": "No otorgar crédito fuera de rango etario permitido."
    },
    {
        "codigo": "R2",
        "expresion": "ingresos >= 1200",
        "descripcion": "Ingreso mínimo mensual de S/ 1200 (límite típico BCP para clientes dependientes).",
        "severidad": "alta",
        "recomendacion": "Solicitar comprobantes de ingresos o derivar a crédito pyme."
    },
    {
        "codigo": "R3",
        "expresion": "deudas <= ingresos * 0.4",
        "descripcion": "Las deudas totales no deben superar el 40% de los ingresos mensuales.",
        "severidad": "alta",
        "recomendacion": "Reducir deudas o refinanciar antes de solicitar nuevo crédito."
    },
    {
        "codigo": "R4",
        "expresion": "mora == 0",
        "descripcion": "El cliente no debe tener moras activas reportadas en centrales de riesgo.",
        "severidad": "alta",
        "recomendacion": "Regularizar moras y esperar 3 meses para re-evaluación."
    },
    {
        "codigo": "R5",
        "expresion": "antiguedad_laboral >= 1",
        "descripcion": "El cliente debe tener al menos 1 año de antigüedad laboral o negocio formal.",
        "severidad": "media",
        "recomendacion": "Esperar a cumplir 12 meses o presentar garantía adicional."
    },
    {
        "codigo": "R6",
        "expresion": "puntaje_crediticio >= 650",
        "descripcion": "Puntaje crediticio mínimo según score Equifax o Sentinel: 650.",
        "severidad": "alta",
        "recomendacion": "Mejorar historial de pago antes de aplicar nuevamente."
    },
    {
        "codigo": "R7",
        "expresion": "tiene_aval or puntaje_crediticio >= 700",
        "descripcion": "Si no cuenta con aval, su score crediticio debe ser de al menos 700.",
        "severidad": "media",
        "recomendacion": "Solicitar aval o demostrar excelente comportamiento crediticio."
    },
    {
        "codigo": "R8",
        "expresion": "monto_solicitado <= ingresos * 4",
        "descripcion": "El monto solicitado no debe exceder 4 veces los ingresos mensuales declarados.",
        "severidad": "baja",
        "recomendacion": "Reducir el monto o ampliar plazo del préstamo."
    },
    {
        "codigo": "R9",
        "expresion": "deudas + (0.1 * monto_solicitado) <= ingresos * 0.9",
        "descripcion": "La carga total (deudas + 10% del nuevo crédito) no debe superar el 90% del ingreso neto.",
        "severidad": "alta",
        "recomendacion": "Recalcular monto o cancelar obligaciones actuales."
    },
    {
        "codigo": "R10",
        "expresion": "empleo_estable",
        "descripcion": "Debe contar con empleo o fuente de ingresos estable y verificable.",
        "severidad": "media",
        "recomendacion": "Solicitar boletas, contratos o estados financieros según tipo de empleo."
    }
]
