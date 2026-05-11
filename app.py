# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai

# Configuración de marca LNP
st.set_page_config(page_title="Destilador de Ficcion | LNP System", page_icon="🏗️")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    h1 { color: #1a1a1a; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #1a1a1a; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Destilador de Ficcion")
st.subheader("Fase D1: Extraccion de Material de Obra")
st.write("Bienvenido a la Refineria Narrativa. Este sistema extraera el material base de tu historia.")

# --- CONFIGURACIÓN DE GEMINI ---
# Asegurate de tener GOOGLE_API_KEY en los Secrets de Streamlit
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

MODEL_NAME = "gemini-1.5-flash-latest"

# Prompt de Sistema (Sin caracteres especiales que rompan el codigo)
system_prompt = """
Actuas como el Destilador de Ficcion del LNP System, diseñado por Salomon Rivera. 
Tu funcion es Consultor de Arquitectura del Conocimiento. 

REGLAS CRITICAS:
1. Nunca sugieres ideas. Solo extraes lo que el autor ya tiene.
2. Si algo no existe, marcas [PENDIENTE DE DISEÑO EN TALLER].
3. Haz UNA SOLA PREGUNTA a la vez.
4. Usa un tono sobrio, profesional y directo.

FLUJO DE EXTRACCION:
- Paso 1: Pedir la 'Idea Cruda' de la historia.
- Paso 2: Extraer Protagonista (Deseo vs Necesidad).
- Paso 3: Identificar el 'Precio' (lo que se pierde).
- Paso 4: Construir la Sentencia Central (Protagonista + Accion + Objetivo + Precio + Obstaculo).
- Paso 5: Hitos (Incidente Incitador, Midpoint, Climax).
- Paso 6: Escenas Ancla (pedir 5 imagenes o momentos claros).

Al finalizar, genera el REPORTE DE EXTRACCION PARA EL TALLER LNP.
"""

if "messages" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(MODEL_NAME)
    st.session_state.chat = st.session_state.model.start_chat(history=[])
    # Enviamos la instruccion de sistema primero
    st.session_state.chat.send_message(system_prompt)
    
    st.session_state.messages = [
        {"role": "assistant", "content": "Para comenzar la arquitectura de tu novela: ¿Cuál es la historia? Cuéntamela como si se la contaras a un amigo en un café, sin adornos."}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interaccion
if prompt := st.chat_input("Escribe tu respuesta aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error de conexion. Por favor intenta de nuevo. {e}")