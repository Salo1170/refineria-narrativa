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
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Usamos el modelo base sin sufijos, que es el más compatible
model = genai.GenerativeModel('gemini-1.5-flash')

# Prompt de Sistema
system_prompt = """
Actuas como el Destilador de Ficcion del LNP System, diseñado por Salomon Rivera. 
Tu funcion es Consultor de Arquitectura del Conocimiento. 
REGLAS: No sugieras ideas. Haz UNA pregunta a la vez. Tono sobrio.
FLUJO: 1. Idea Cruda, 2. Protagonista, 3. Precio, 4. Sentencia Central, 5. Hitos, 6. Escenas Ancla.
"""

# Inicializar historial si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Para comenzar la arquitectura de tu novela: ¿Cuál es la historia? Cuéntamela como si se la contaras a un amigo en un café, sin adornos."}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interaccion
if prompt := st.chat_input("Escribe tu respuesta aqui..."):
    # 1. Mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generar respuesta con todo el historial para que no pierda el contexto
    with st.chat_message("assistant"):
        try:
            # Construimos el contexto completo para la IA
            full_context = f"{system_prompt}\n\nHistorial de conversacion:\n"
            for m in st.session_state.messages:
                full_context += f"{m['role']}: {m['content']}\n"
            
            # Llamada directa (más estable que el modo chat)
            response = model.generate_content(full_context)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error("El servicio de Google esta saturado o no disponible en tu region. Detalles técnicos: " + str(e))