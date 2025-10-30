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
    """se imprimen los resultados de cada cliente evaluado."""
    print("=" * 60)
    print(f"Evaluación de crédito: {cliente.nombre}")
    print("-" * 60)

    aprobadas = [r for r in resultados if r["cumple"]]
    rechazadas = [r for r in resultados if not r["cumple"]]

    if len(rechazadas) == 0:
        print("Cliente PRE-APROBADO.")
    else:
        print("Cliente NO PRE-APROBADO.")
        print("\nMotivos de rechazo:")
        for r in rechazadas:
            print(f" - [{r['codigo']}] {r['descripcion']} ({r['severidad']})")
            print(f"Recomendación: {r['recomendacion']}")

    print("\nResumen:")
    print(f"Cumple {len(aprobadas)}/{len(resultados)} reglas")
    print("=" * 60 + "\n")

# MAIN LOOP
def main():
    print("\n SISTEMA EXPERTO - PRECALIFICADOR DE CRÉDITO 🧩\n")
    for cliente in clientes_obj:
        resultados = evaluar_cliente(cliente)
        mostrar_resultados(cliente, resultados)

if __name__ == "__main__":
    main()
