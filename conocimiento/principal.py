# aca ta el principal main.py
# MOTOR DE INFERENCIA - Sistema Experto: Precalificador de Crédito

from rule_engine import Rule
from base_conocimiento import reglas
from base_hechos import clientes_obj

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


# MAIN LOOP
def main():
    print("\n SISTEMA EXPERTO - PRECALIFICADOR DE CRÉDITO 🧩\n")
    for cliente in clientes_obj:
        resultados = evaluar_cliente(cliente)
        mostrar_resultados(cliente, resultados)

if __name__ == "__main__":
    main()
