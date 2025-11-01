# aca ta el principal main.py
# MOTOR DE INFERENCIA - Sistema Experto: Precalificador de Crédito

import pytest
from rule_engine import Rule
from knowledge.base_conocimiento import *
from engine.base_hechos import *

# FUNCIÓN PRINCIPAL DE EVALUACIÓN

def evaluar_cliente(cliente):
    """Evalúa todas las reglas sobre un cliente y devuelve el resultado."""
    resultados = []
    dict_cliente = cliente.to_dict()

    for r in reglas:
        regla = Rule(r["expresion"])
        cumple = regla.matches(dict_cliente)
        resultados.append({
            "codigo": r["codigo"],
            "descripcion": r["descripcion"],
            "cumple": cumple,
            "severidad": r["severidad"],
            "recomendacion": r["recomendacion"]
        })
    
    return resultados

# MOSTRAR RESULTADOS
def mostrar_resultados(cliente, resultados):
    """Muestra el resultado de evaluación con razones ordenadas por severidad."""

    # Diccionario para ordenar severidades
    niveles = {"alta": 3, "media": 2, "baja": 1}

    # Filtrar reglas no cumplidas
    rechazadas = [r for r in resultados if not r["cumple"]]
    rechazadas.sort(key=lambda r: niveles.get(r["severidad"].lower(), 0), reverse=True)

    # Determinar estado final según severidad más alta
    if not rechazadas:
        estado = "✅ APROBADO"
        print(f"{cliente.nombre} --> {estado}")
    else:
        severidad_max = rechazadas[0]["severidad"].lower()
        if severidad_max == "alta":
            estado = "❌ NO APROBADO"
        elif severidad_max == "media":
            estado = "🚫 NO APROBADO (riesgo moderado)"
        else:
            estado = "⚠️ PRE-APROBADO CON OBSERVACIONES"

        # Mostrar resultado principal
        print(f"{cliente.nombre} --> {estado} porque:")

        # Mostrar razones de rechazo ordenadas por severidad
        for r in rechazadas:
            print(f"   - {r['descripcion']} [{r['severidad'].upper()}]")

    print("=" * 60)


# TEST (pytest)
def test_inferencia_correcta():
    cliente = Cliente("Juan Pérez", 35, 2500, 500, 1, 5, "dependiente", True, 700, 3000, ahorros=500, empleo_estable=True, estado_civil="casado")
    resultados = evaluar_cliente(cliente)
    rechazadas = [r for r in resultados if not r["cumple"]]
    assert any("mora" in r["descripcion"].lower() for r in rechazadas), "Debería fallar por MORA activa."


def test_caso_borde():
    cliente = Cliente("María López", 21, 1200, 480, 0, 1, "independiente", True, 750, 4800, ahorros=600, empleo_estable=True, estado_civil="soltero")
    resultados = evaluar_cliente(cliente)
    rechazadas = [r for r in resultados if not r["cumple"]]
    assert len(rechazadas) == 0, "Debería ser APROBADO (sin fallas)."


def test_explicacion():
    cliente = Cliente("Pedro Ruiz", 40, 1000, 200, 0, 10, "independiente", False, 600, 500, ahorros=1000, empleo_estable=True, estado_civil="casado")
    resultados = evaluar_cliente(cliente)
    rechazadas = [r for r in resultados if not r["cumple"]]
    assert any("puntaje" in r["descripcion"].lower() for r in rechazadas), "Debe fallar por puntaje crediticio bajo."



# MAIN
def main():
    print("\n SISTEMA EXPERTO - PRECALIFICADOR DE CRÉDITO 🧩\n")
    for cliente in clientes_obj:
        resultados = evaluar_cliente(cliente)
        mostrar_resultados(cliente, resultados)

if __name__ == "__main__":
    main()
