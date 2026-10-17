
import asyncio
import uuid

import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from business_agent.agent import root_agent


APP_NAME = "bizmind_ai"


@st.cache_resource
def inicializar_agente():
    sesiones = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=sesiones,
    )
    return runner, sesiones


async def crear_sesion(sesiones, user_id, session_id):
    await sesiones.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )


async def consultar_agente(runner, user_id, session_id, pregunta):
    mensaje = types.Content(
        role="user",
        parts=[types.Part(text=pregunta)],
    )

    respuesta = []

    async for evento in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=mensaje,
    ):
        if evento.is_final_response() and evento.content:
            for parte in evento.content.parts:
                if parte.text:
                    respuesta.append(parte.text)

    return "\n".join(respuesta) or "No se recibió una respuesta."


st.set_page_config(
    page_title="BizMind AI",
    page_icon="📊",
    layout="centered",
)

st.title("📊 BizMind AI")
st.caption("Inteligencia para los negocios")
st.write(
    "Tu asistente para analizar ventas, consultar "
    "estrategias comerciales y evaluar promociones."
)

with st.sidebar:
    st.subheader("Acerca del proyecto")
    st.write(
        "Demo de IA aplicada a los negocios con Google ADK, "
        "Gemini, análisis de datos y RAG."
    )

    if st.button("Nueva conversación"):
        st.session_state.user_id = str(uuid.uuid4())
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.session_created = False
        st.rerun()


runner, sesiones = inicializar_agente()

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_created" not in st.session_state:
    st.session_state.session_created = False

if not st.session_state.session_created:
    asyncio.run(
        crear_sesion(
            sesiones,
            st.session_state.user_id,
            st.session_state.session_id,
        )
    )
    st.session_state.session_created = True

for mensaje in st.session_state.messages:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

pregunta = st.chat_input(
    "Pregunta sobre ventas, productos o promociones..."
)

if pregunta:
    st.session_state.messages.append(
        {"role": "user", "content": pregunta}
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            try:
                respuesta = asyncio.run(
                    consultar_agente(
                        runner,
                        st.session_state.user_id,
                        st.session_state.session_id,
                        pregunta,
                    )
                )
                st.markdown(respuesta)

            except Exception as error:
                respuesta = (
                    "No pude procesar la consulta. "
                    "Revisa el error en la terminal de VS Code."
                )
                st.error(respuesta)
                print(f"Error de BizMind AI: {error}")

    st.session_state.messages.append(
        {"role": "assistant", "content": respuesta}
    )
