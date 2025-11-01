# PROGRAMA EN STREAMLIT

import pytest
import streamlit as st
import time
from knowledge.base_conocimiento import reglas
from engine.base_hechos import clientes_obj
from rule_engine import Rule
from principal import test_inferencia_correcta, test_caso_borde, test_explicacion, evaluar_cliente

st.set_page_config(page_title="Precalificador de Créditos BCP", page_icon="💳", layout="wide")

# estilos
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #F5F5F5;
    }
    [data-testid="stHeader"] {
        background: none;
    }
            
    .titulo-bcp {
        color: #001C66;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
        letter-spacing: 0.5px;
    }
    .subtitulo {
        color: #F47A31;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    .cliente-box {
        background-color: #FFFFFF;
        border: 3px solid #F47A31;
        border-radius: 12px;
        padding: 1.8rem;
        color: #001C66;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .dato-label {
        color: #001C66;
        font-weight: 600;
    }
    .dato-valor {
        color: #F47A31;
        font-weight: 700;
    }
    .footer {
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
        border-top: 1px solid #F47A31;
        margin-top: 20px;
        padding-top: 5px;
    }
    .motivo-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .motivo-descripcion {
        color: #001C66;
        font-weight: 600;
        font-size: 1rem;
    }
    .motivo-severidad {
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
    }
    .sev-alta {
        background-color: #ffe5e5;
        color: #d32f2f;
        border: 1px solid #d32f2f;
    }
    .sev-media {
        background-color: #fff0e0;
        color: #f57c00;
        border: 1px solid #f57c00;
    }
    .sev-baja {
        background-color: #e8f5e9;
        color: #388e3c;
        border: 1px solid #388e3c;
    }
    .motivo-recomendacion {
        color: #001C66;
        margin-top: 5px;
        font-size: 0.95rem;
    }
    .motivo-recomendacion span {
        color: #F47A31;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)



# titulo
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("logo.jpg", width=200)
with col_titulo:
    st.markdown("<div class='titulo-bcp'>Precalificador de Créditos</div>"
                "<div class='subtitulo'>Sistema experto basado en reglas del Banco de Crédito del Perú</div>"
                ,unsafe_allow_html=True)

with st.expander("Más Información"):
        st.markdown(
            """
            El <strong>Precalificador de Créditos</strong> es un sistema experto diseñado para evaluar de forma preliminar la elegibilidad de un cliente antes de iniciar el proceso formal de solicitud de crédito. 
            Su propósito es analizar la información financiera y personal del solicitante para emitir una recomendación automatizada sobre la viabilidad de aprobación, de acuerdo con las políticas crediticias del <strong>Banco de Crédito del Perú (BCP)</strong>.
            <br><br>

            <h4 style='color: #F47A31;'>Objetivo del Sistema</h4>
            <ul>
                <li>
                    <strong>Evaluación inicial:</strong> Permitir al banco determinar si un cliente cumple los requisitos mínimos para acceder a un crédito.
                </li>
                <li>
                    <strong>Reducción de riesgo:</strong> Prevenir la aprobación de solicitudes de alto riesgo crediticio mediante la aplicación de reglas claras de acuerdo a información oficial del BCP.
                </li>
                <li>
                    <strong>Optimización del proceso:</strong> Agilizar la etapa de revisión y priorizar a los clientes con mayor probabilidad de aprobación.
                </li>
            </ul>
            <br>

            <h4 style='color: #F47A31;'>Funcionamiento</h4>
            El sistema experto emplea una <strong>base de conocimiento</strong> que contiene las reglas crediticias del BCP, las cuales se aplican a los datos ingresados por el cliente (hechos) para obtener una conclusión.
            <ul>
                <li>
                    <strong>Reglas (conocimiento):</strong> Representan las políticas crediticias, como ingresos mínimos, límite de endeudamiento, score crediticio, presencia de aval o moras activas.
                </li>
                <li>
                    <strong>Hechos (datos del cliente):</strong> Contienen la información específica de cada solicitante: edad, ingresos, deudas, puntaje crediticio, antigüedad laboral, entre otros.
                </li>
                <li>
                    <strong>Motor de inferencia:</strong> Compara las reglas con los datos del cliente y determina si el crédito es <strong>aprobado</strong> o <strong>no aprobado</strong>.
                </li>
            </ul>
            <br>

            <h4 style='color: #F47A31;'>Conclusión y Explicación</h4>
            Una vez ejecutada la evaluación, el sistema muestra:
            <ul>
                <li><strong>Conclusión:</strong> Indica si el cliente es <strong>APROBADO</strong> o <strong>NO APROBADO</strong>.</li>
                <li><strong>Motivos y recomendaciones:</strong> Explica las reglas activadas y las observaciones que justifican la decisión final. Solo se dá en casos NO APROBADOS.</li>
            </ul>
            """
            , unsafe_allow_html=True
        )

st.markdown("##### ⚠️ AVISO: No uso directo en producción. Este sistema da resultados pero quien tiene la decisión final es un experto en finanzas.")

st.markdown("<hr style='border-bottom: 1px solid #F47A31;'>", unsafe_allow_html=True)

modo = st.radio("Seleccionar vista:", ["👥 Lista de Clientes", "🧪 Tests"], horizontal=True)


def obtener_conclusion(resultados):
    niveles = {"alta": 3, "media": 2, "baja": 1}
    rechazadas = [r for r in resultados if not r["cumple"]]
    rechazadas.sort(key=lambda r: niveles.get(r["severidad"].lower(), 0), reverse=True)

    if not rechazadas:
        return "✅ APROBADO", []
    severidad_max = rechazadas[0]["severidad"].lower()
    if severidad_max == "alta":
        estado = "❌ NO APROBADO"
    elif severidad_max == "media":
        estado = "🚫 NO APROBADO (riesgo moderado)"
    else:
        estado = "⚠️ PRE-APROBADO CON OBSERVACIONES"
    return estado, rechazadas


if modo == "👥 Lista de Clientes":
    # lista de clientes
    st.subheader("👥 Lista de clientes")
    nombres = [c.nombre for c in clientes_obj]
    cliente_seleccionado = st.selectbox("Seleccione un cliente:", nombres)
    cliente_obj = next(c for c in clientes_obj if c.nombre == cliente_seleccionado)

    # datos del cliente seleccionado
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<span class='dato-label'>Edad:</span> <span class='dato-valor'>{cliente_obj.edad} años</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Ingresos:</span> <span class='dato-valor'>S/ {cliente_obj.ingresos:,.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Deudas:</span> <span class='dato-valor'>S/ {cliente_obj.deudas:,.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Ahorros:</span> <span class='dato-valor'>S/ {cliente_obj.ahorros:,.2f}</span>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<span class='dato-label'>Puntaje crediticio:</span> <span class='dato-valor'>{cliente_obj.puntaje_crediticio}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Antigüedad laboral:</span> <span class='dato-valor'>{cliente_obj.antiguedad_laboral} años</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Tipo de empleo:</span> <span class='dato-valor'>{cliente_obj.tipo_empleo}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Empleo estable:</span> <span class='dato-valor'>{'Sí' if cliente_obj.empleo_estable else 'No'}</span>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<span class='dato-label'>Mora:</span> <span class='dato-valor'>{'Sí' if cliente_obj.mora else 'No'}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Tiene aval:</span> <span class='dato-valor'>{'Sí' if cliente_obj.tiene_aval else 'No'}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Monto solicitado:</span> <span class='dato-valor'>S/ {cliente_obj.monto_solicitado:,.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"<span class='dato-label'>Estado civil:</span> <span class='dato-valor'>{cliente_obj.estado_civil.capitalize()}</span>", unsafe_allow_html=True)


    # evaluar al cliente
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Evaluación del cliente")

    if st.button("Evaluar cliente", use_container_width=True, type="primary"):
        resultados = evaluar_cliente(cliente_obj)
        estado, rechazadas = obtener_conclusion(resultados)

        if "✅ APROBADO" in estado:
            st.success(f"{estado} - El cliente cumple con todas las políticas crediticias del BCP.")
        elif "❌ NO APROBADO" in estado:
            st.error(f"{estado} - El cliente no cumple las políticas crediticias del BCP.")
        elif "🚫 NO APROBADO (riesgo moderado)" in estado:
            st.info(f"{estado} - El cliente no cumple las políticas crediticias del BCP con un riesgo moderado.")
        else:
            st.warning(f"{estado} - El cliente esta pre-aprobado con algunas observaciones.")


        if rechazadas:
            # tarjetas
            for r in rechazadas:
                sev = r["severidad"].lower()
                clase = "sev-alta" if sev == "alta" else "sev-media" if sev == "media" else "sev-baja"

                motivo_html = f"""
                <div class="cliente-box">
                    <div class="motivo-header">
                        <div class="motivo-descripcion">{r['descripcion']}</div>
                        <div class="motivo-severidad {clase}"> Severidad: {r['severidad'].capitalize()}</div>
                    </div>
                    <div class="motivo-recomendacion">
                        <span><b>Recomendación:</b></span> {r['recomendacion']}
                    </div>
                </div>
                """
                st.markdown(motivo_html, unsafe_allow_html=True)


else:
    st.subheader("🧪 Tests (Pruebas automáticas)")

    # los 3 tests
    def ejecutar_tests_pytest():
        inicio = time.time()
        tests = [
        ("test_inferencia_correcta", test_inferencia_correcta),
        ("test_caso_borde", test_caso_borde),
        ("test_explicacion", test_explicacion)
        ]

        passed = 0
        
        simulacion = """
            <div class="cliente-box" style="background-color: #1e1e1e; color: #d4d4d4; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 14px;">
            <pre style="margin: 0; white-space: pre-wrap; word-break: break-all; color: #d4d4d4;">
        """
        
        simulacion += "collected 3 items<br><br>"
        time.sleep(0.6)

        for nombre, funcion in tests:
            try:
                # Ejecutamos la función. Si hay un 'assert' fallido, salta al except.
                funcion()
                estado_texto = f'PASSED'
                estado_html = f'<span style="color:#6aa84f; font-weight:700;">{estado_texto}</span><br>'
                passed += 1
            except AssertionError as e:
                estado_texto = f'FAILED'
                estado_html = f'<span style="color:#ffc107; font-weight:700;">{estado_texto}</span><br>'
            except NameError:
                estado_html = f'<span style="color:#ffc107; font-weight:700;">ERROR (No definido)</span><br>'


            linea_test = f"principal.py::{nombre}"
            
            espacios_necesarios = 50 - len(linea_test) 
            
            simulacion += f"{linea_test}{' ' * espacios_necesarios}{estado_html}\n"
            
            time.sleep(0.4)

        # 4. Resumen final
        duracion = time.time() - inicio
        
        # Línea de separación verde de consola
        linea_separadora = f'<span style="color:#6aa84f;">{"="*55}</span>'
        simulacion += f"<br>{linea_separadora}\n"
        
        # Texto del resumen final
        resumen_final = f'{passed} passed in {duracion:.2f}s'
        simulacion += f'<span style="color:#6aa84f; font-weight:700;">{resumen_final}</span>\n'
        simulacion += f'{linea_separadora}\n'

        simulacion += "</pre></div>"

        st.markdown(simulacion, unsafe_allow_html=True)


    if st.button("▶️ Ejecutar pruebas (pytest simulado)", use_container_width=True):
        with st.spinner("Ejecutando tests..."):
            time.sleep(0.8)
            ejecutar_tests_pytest()


# footer
st.markdown("<div class='footer'>Este sistema experto utiliza Bases de conocimiento del Banco de Crédito del Perú (BCP).</div>", unsafe_allow_html=True)
