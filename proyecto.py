import streamlit as st
from groq import Groq

#Nombre de la pestaña e icono
st.set_page_config(page_title="Mi chatGPT", page_icon= "icono.jpg", layout="centered")

#titulo

st.title("Mi primera app en Python con Streamlit")

#entrada texto

nom = st.text_input("¿cual es tu nombre?")

#btn saludo

if st.button("saludar"):
    st.write(f'hola {nom}, bienvenido a mi chatgpt')

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def config():
    #titulo 
    st.title("Mi chat de inteligencia artificial")
    st.sidebar.title("Configuracion de la IA")
    elegirModelo = st.sidebar.selectbox("Elegi un modelo", options = modelos, index=0)
    return elegirModelo

#Clase 7

def crear_usuario_groq():
    claveSecreta = st.secrets["clave_api"]
    return Groq(api_key=claveSecreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model= modelo,
        messages = [{"role": "user", "content": mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes=[]
        

#clase 8

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
                st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()

#clase 9

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


def main():
    modelo = config()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Por favor, escribí un mensaje")

    if mensaje:
        actualizar_historial("user", mensaje,"🧑🏻") # Función de esta clase
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa,"🤖")
        st.rerun()


if __name__ == "__main__":
    main()



