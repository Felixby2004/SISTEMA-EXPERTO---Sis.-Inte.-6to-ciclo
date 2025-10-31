# aca ta el principal main.py
# MOTOR DE INFERENCIA - Sistema Experto: Precalificador de Crédito

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
    # CLIENTE ESPERADO: NO APROBADO (La regla de MORA se dispara)
    print("\n--- Ejecutando Test: Inferencia Correcta (NO APROBADO por Mora) ---")
    cliente = Cliente("Juan Pérez", 35, 2500, 500, True, 5, "dependiente", True, 700, 3000, ahorros=500, empleo_estable=True, estado_civil="casado")
    resultados = evaluar_cliente(cliente)
    mostrar_resultados(cliente, resultados)


def test_caso_borde():
    # CLIENTE ESPERADO: APROBADO (Datos balanceados que pasan por poco o justo)
    print("\n--- Ejecutando Test: Caso Borde (APROBADO) ---")
    cliente = Cliente("María López", 28, 1500, 200, False, 2, "independiente", True, 750, 2000, ahorros=600, empleo_estable=True, estado_civil="soltero")
    resultados = evaluar_cliente(cliente)
    mostrar_resultados(cliente, resultados)


def test_explicacion():
    # CLIENTE ESPERADO: NO APROBADO (La regla de PUNTAJE BAJO se dispara, forzando explicación)
    print("\n--- Ejecutando Test: Explicación (Fallo por Puntaje) ---")
    cliente = Cliente("Pedro Ruiz", 40, 1000, 200, False, 10, "independiente", False, 600, 500, ahorros=1000, empleo_estable=True, estado_civil="casado")
    resultados = evaluar_cliente(cliente)
    mostrar_resultados(cliente, resultados)



# MAIN
def main():
    print("\n SISTEMA EXPERTO - PRECALIFICADOR DE CRÉDITO 🧩\n")
    print("--- 1. Ejecución del Sistema Experto ---")
    for cliente in clientes_obj:
        resultados = evaluar_cliente(cliente)
        mostrar_resultados(cliente, resultados)

    # 2. Ejecución de los Tests
    print("--- 2. Ejecución de las Pruebas Unitarias ---")
    test_inferencia_correcta()
    test_caso_borde()
    test_explicacion()

if __name__ == "__main__":
    main()
