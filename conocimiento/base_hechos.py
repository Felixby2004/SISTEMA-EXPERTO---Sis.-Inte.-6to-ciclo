# base_hechos.py
# ======================================
# BASE DE HECHOS - Clase Cliente e instancias simuladas
# ======================================

from typing import Dict

class Cliente:
    """
    Representa a un cliente con los atributos usados por las reglas.
    Proporciona to_dict() para evaluación por rule-engine (que usa dicts).
    """
    def __init__(self,
                 nombre: str,
                 edad: int,
                 ingresos: float,
                 deudas: float,
                 mora: int,
                 antiguedad_laboral: float,
                 tipo_empleo: str,
                 tiene_aval: bool,
                 puntaje_crediticio: int,
                 monto_solicitado: float,
                 ahorros: float = 0.0,
                 empleo_estable: bool = True,
                 estado_civil: str = "soltero"):
        # datos básicos
        self.nombre = nombre
        self.edad = int(edad)
        self.ingresos = float(ingresos)
        self.deudas = float(deudas)
        self.mora = int(mora)  # 0 o 1
        self.antiguedad_laboral = float(antiguedad_laboral)  # años
        self.tipo_empleo = tipo_empleo  # 'dependiente'|'independiente'
        self.tiene_aval = bool(tiene_aval)
        self.puntaje_crediticio = int(puntaje_crediticio)  # escala 0-1000
        self.monto_solicitado = float(monto_solicitado)
        self.ahorros = float(ahorros)
        self.empleo_estable = bool(empleo_estable)
        self.estado_civil = estado_civil

        self._validar()

    def _validar(self):
        """Validaciones simples para evitar valores incoherentes."""
        if self.edad < 0:
            raise ValueError("edad no puede ser negativa")
        if self.ingresos < 0 or self.deudas < 0 or self.monto_solicitado < 0 or self.ahorros < 0:
            raise ValueError("valores monetarios no pueden ser negativos")
        if self.mora not in (0, 1):
            raise ValueError("mora debe ser 0 (no) o 1 (sí)")
        if self.tipo_empleo not in ("dependiente", "independiente"):
            # permitimos flexibilidad pero normalizamos
            self.tipo_empleo = "independiente"

    def to_dict(self) -> Dict:
        """
        Devuelve un diccionario plano con los atributos.
        Útil para pasar a rule-engine: Rule.matches(vars(cliente)) o Rule.matches(cliente.to_dict()).
        """
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "ingresos": self.ingresos,
            "deudas": self.deudas,
            "mora": self.mora,
            "antiguedad_laboral": self.antiguedad_laboral,
            "tipo_empleo": self.tipo_empleo,
            "tiene_aval": self.tiene_aval,
            "puntaje_crediticio": self.puntaje_crediticio,
            "monto_solicitado": self.monto_solicitado,
            "ahorros": self.ahorros,
            "empleo_estable": self.empleo_estable,
            "estado_civil": self.estado_civil
        }

    def __repr__(self):
        return f"<Cliente {self.nombre} | ingresos={self.ingresos} deudas={self.deudas} puntaje={self.puntaje_crediticio}>"

# ======================================================
# Instancias simuladas (10 clientes) - lista 'clientes_obj'
# ======================================================
clientes_obj = [
    Cliente("Ana Torres", 28, 1500, 200, 0, 2, "independiente", True, 750, 2000, ahorros=600, empleo_estable=True, estado_civil="soltero"),
    Cliente("Imanol Ramos", 35, 900, 400, 1, 1, "dependiente", False, 500, 1500, ahorros=100, empleo_estable=True, estado_civil="casado"),
    Cliente("Felix Chavez", 42, 2200, 300, 0, 5, "dependiente", True, 820, 5000, ahorros=2000, empleo_estable=True, estado_civil="conviviente"),
    Cliente("Jorge Pérez", 22, 1100, 100, 0, 0.5, "independiente", False, 650, 1000, ahorros=50, empleo_estable=False, estado_civil="soltero"),
    Cliente("Kiara López", 30, 1800, 800, 0, 3, "dependiente", True, 780, 4000, ahorros=1200, empleo_estable=True, estado_civil="casado"),
    Cliente("Kevin Vargas", 26, 700, 200, 0, 0.8, "independiente", False, 580, 800, ahorros=100, empleo_estable=False, estado_civil="soltero"),
    Cliente("Geraldine Rojas", 31, 1600, 300, 0, 2, "dependiente", True, 710, 2500, ahorros=800, empleo_estable=True, estado_civil="soltero"),
    Cliente("Diego Cuba", 45, 3000, 1000, 0, 10, "dependiente", True, 900, 6000, ahorros=10000, empleo_estable=True, estado_civil="casado"),
    Cliente("Gaby Ramos", 24, 950, 150, 0, 1, "independiente", False, 670, 1200, ahorros=300, empleo_estable=False, estado_civil="soltero"),
    Cliente("Pedro Castillo", 50, 4000, 700, 0, 15, "dependiente", True, 880, 7000, ahorros=5000, empleo_estable=True, estado_civil="casado")
]
