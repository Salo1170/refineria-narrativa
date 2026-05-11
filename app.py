import streamlit as st
import google.generativeai as genai

# Configuración de marca LNP™
st.set_page_config(page_title="Destilador de Ficción | LNP System™", page_icon="🏗️")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1 { color: #1a1a1a; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #1a1a1a; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Destilador de Ficción")
st.subheader("Fase D1: Extracción de Material de Obra")
st.write("Bienvenido a la Refinería Narrativa™. Este sistema extraerá el material base de tu historia.")

# --- CONFIGURACIÓN DE GEMINI ---
# Asegúrate de que en Secrets el nombre sea exactamente: GOOGLE_API_KEY
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Definimos la instrucción de sistema ANTES de iniciar el modelo
system_prompt = """
Actúas como el Destilador de Ficción del LNP System™, diseñado por Salomón Rivera. 
Tu función es Consultor de Arquitectura del Conocimiento. 

REGLAS CRÍTICAS:
1. Nunca sugieres ideas. Solo extraes lo que el autor ya tiene.
2. Si algo no existe, marcas [PENDIENTE DE DISEÑO EN TALLER].
3. Haz UNA SOLA PREGUNTA a la vez.
4. Usa un tono sobrio, profesional y directo.

FLUJO DE EXTRACCIÓN:
- Paso 1: Pedir la 'Idea Cruda' de la historia.
- Paso 2: Extraer Protagonista (Deseo vs Necesidad).
- Paso 3: Identificar el 'Precio' (lo que se pierde).
- Paso 4: Construir la Sentencia Central (Protagonista + Acción + Objetivo + Precio + Obstáculo).
- Paso 5: Hitos (Incidente Incitador, Midpoint, Clímax).
- Paso 6: Escenas Ancla (pedir 5 imágenes o momentos claros).

Al finalizar, genera el 'REPORTE DE EXTRACCIÓN PARA EL TALLER LNP' con todos los puntos anteriores.
"""

# Inicializamos el modelo con la instrucción de sistema correcta
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])
    st.session_state.messages = [
        {"role": "assistant", "content": "Para comenzar la arquitectura de tu novela: ¿Cuál es la historia? Cuéntamela como si se la contaras a un amigo en un café, sin adornos."}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interacción
if prompt := st.chat_input("Escribe tu respuesta aquí..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hubo un error con la conexión: {e}")