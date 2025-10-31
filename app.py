import streamlit as st
from knowledge.base_conocimiento import reglas
from engine.base_hechos import Cliente, clientes_obj
from rule_engine import Rule

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
    .motivo-card {
        border: 2px solid #001C66;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #FFFFFF;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
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


st.markdown("<hr style='border-bottom: 1px solid #F47A31;'>", unsafe_allow_html=True)

modo = st.radio("Seleccionar vista:", ["👥 Lista de Clientes", "🧪 Tests"], horizontal=True)


def evaluar_cliente(cliente):
        resultados = []
        datos = cliente.to_dict()
        for r in reglas:
            regla = Rule(r["expresion"])
            cumple = regla.matches(datos)
            resultados.append({
                "codigo": r["codigo"],
                "descripcion": r["descripcion"],
                "cumple": cumple,
                "severidad": r["severidad"],
                "recomendacion": r["recomendacion"]
            })
        return resultados

if modo == "👥 Lista de Clientes":

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


    # --- EVALUACIÓN DENTRO DEL CLIENTE BOX ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Evaluación del cliente")

    if st.button("Evaluar cliente", use_container_width=True, type="primary"):
        resultados = evaluar_cliente(cliente_obj)
        estado, rechazadas = obtener_conclusion(resultados)

        if "✅ APROBADO" in estado:
            st.success(f"{estado} - El cliente cumple con todas las políticas crediticias del BCP.")
        elif "❌ NO APROBADO" in estado:
            st.error(f"{estado} - El cliente no cumple las condiciones necesarias.")
        else:
            st.warning(f"{estado}")

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


elif modo == "🧪 Tests":
    st.subheader("🧪 Pruebas automáticas")
    
    # --- Función común para evaluar ---
    def evaluar_y_mostrar(cliente, titulo_test):
        resultados = evaluar_cliente(cliente)
        rechazadas = [r for r in resultados if not r["cumple"]]

        st.markdown(f"<h4 style='color:#F47A31; margin-bottom:10px;'>{titulo_test}</h4>", unsafe_allow_html=True)
        st.markdown(f"**Cliente:** {cliente.nombre} — **Edad:** {cliente.edad} años — **Ingresos:** S/ {cliente.ingresos:,.2f}", unsafe_allow_html=True)

        if not rechazadas:
            st.success("✅ APROBADO - El cliente cumple con todas las políticas crediticias del BCP.")
        else:
            st.error("❌ NO APROBADO - El cliente no cumple las condiciones necesarias.")
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
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TEST 1 ---
    if st.button("Test 1: Inferencia correcta (NO APROBADO por Mora)", use_container_width=True):
        cliente = Cliente("Juan Pérez", 35, 2500, 500, True, 5, "dependiente", True, 700, 3000, ahorros=500, empleo_estable=True, estado_civil="casado")
        evaluar_y_mostrar(cliente, "Test 1: Inferencia Correcta (Mora detectada)")

    # --- TEST 2 ---
    if st.button("Test 2: Caso Borde (APROBADO justo)", use_container_width=True):
        cliente = Cliente("María López", 28, 1500, 200, False, 2, "independiente", True, 750, 2000, ahorros=600, empleo_estable=True, estado_civil="soltero")
        evaluar_y_mostrar(cliente, "Test 2: Caso Borde (Aprobación ajustada)")

    # --- TEST 3 ---
    if st.button("Test 3: Explicación (Puntaje bajo)", use_container_width=True):
        cliente = Cliente("Pedro Ruiz", 40, 1000, 200, False, 10, "independiente", False, 600, 500, ahorros=1000, empleo_estable=True, estado_civil="casado")
        evaluar_y_mostrar(cliente, "Test 3: Explicación del sistema (Puntaje bajo)")



# --- FOOTER ---
st.markdown("<div class='footer'>Este sistema experto utiliza Bases de conocimiento del Banco de Crédito del Perú (BCP).</div>", unsafe_allow_html=True)
