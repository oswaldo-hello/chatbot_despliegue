import streamlit as st
import difflib

# Menús y precios
platos = {
    "arroz chaufa": 20,
    "lomo saltado": 22,
    "ensalada vegetal": 18,
    "pollo a la brasa": 25,
    "sopa criolla": 19
}

postres = {
    "mazamorra morada": 8,
    "arroz con leche": 7
}

bebidas = {
    "chicha morada": 5,
    "inca kola": 6,
    "agua": 4
}

pagos = ["yape", "tarjeta", "efectivo"]
negaciones = ["no", "nada", "ninguno", "ninguna", "no gracias", "no, gracias"]

# Función para similitud
def buscar_coincidencia(user_input, opciones):
    user_input = user_input.lower()
    coincidencias = difflib.get_close_matches(user_input, opciones, n=1, cutoff=0.5)
    return coincidencias[0] if coincidencias else None

# Inicializa sesión
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.pedido = {}

st.title("🍽️ Chatbot ITR - Restaurante Virtual")

# Paso 1: Plato
if st.session_state.step == 1:
    st.markdown("👋 ¡Bienvenido! Estos son nuestros platos del día:")
    for nombre, precio in platos.items():
        st.write(f"- **{nombre.title()}** - S/ {precio}")
    entrada = st.text_input("✍️ Escribe el plato que deseas pedir:", key="plato_input")
    if entrada:
        plato = buscar_coincidencia(entrada, platos.keys())
        if plato:
            st.session_state.pedido["plato"] = plato
            st.session_state.pedido["precio_plato"] = platos[plato]
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("❌ No reconocí ese plato. Intenta escribir uno del menú.")

# Paso 2: Postre
elif st.session_state.step == 2:
    st.markdown(f"🍽️ Elegiste: **{st.session_state.pedido['plato'].title()}**")
    st.markdown("🍰 ¿Deseas un postre?")
    for nombre, precio in postres.items():
        st.write(f"- {nombre.title()} - S/ {precio}")
    entrada = st.text_input("✍️ Escribe tu postre:", key="postre_input")
    if entrada:
        entrada_lower = entrada.lower()
        if any(neg in entrada_lower for neg in negaciones):
            st.session_state.pedido["postre"] = "ninguno"
            st.session_state.pedido["precio_postre"] = 0
            st.session_state.step = 3
            st.rerun()
        else:
            postre = buscar_coincidencia(entrada, postres.keys())
            if postre:
                st.session_state.pedido["postre"] = postre
                st.session_state.pedido["precio_postre"] = postres[postre]
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("❌ No reconocí ese postre.")

# Paso 3: Bebida
elif st.session_state.step == 3:
    st.markdown("🥤 ¿Deseas una bebida?")
    for nombre, precio in bebidas.items():
        st.write(f"- {nombre.title()} - S/ {precio}")
    entrada = st.text_input("✍️ Escribe tu bebida:", key="bebida_input")
    if entrada:
        entrada_lower = entrada.lower()
        if any(neg in entrada_lower for neg in negaciones):
            st.session_state.pedido["bebida"] = "ninguna"
            st.session_state.pedido["precio_bebida"] = 0
            st.session_state.step = 4
            st.rerun()
        else:
            bebida = buscar_coincidencia(entrada, bebidas.keys())
            if bebida:
                st.session_state.pedido["bebida"] = bebida
                st.session_state.pedido["precio_bebida"] = bebidas[bebida]
                st.session_state.step = 4
                st.rerun()
            else:
                st.error("❌ No reconocí esa bebida.")

# Paso 4: Método de pago
elif st.session_state.step == 4:
    total = sum([
        st.session_state.pedido.get("precio_plato", 0),
        st.session_state.pedido.get("precio_postre", 0),
        st.session_state.pedido.get("precio_bebida", 0)
    ])
    st.markdown("🧾 **Resumen de tu pedido:**")
    st.write(f"🍽️ Plato: {st.session_state.pedido['plato'].title()} - S/ {st.session_state.pedido['precio_plato']}")
    st.write(f"🍰 Postre: {st.session_state.pedido['postre'].title()} - S/ {st.session_state.pedido['precio_postre']}")
    st.write(f"🥤 Bebida: {st.session_state.pedido['bebida'].title()} - S/ {st.session_state.pedido['precio_bebida']}")
    st.markdown(f"💰 **Total a pagar: S/ {total}**")

    st.markdown("💳 ¿Cómo deseas pagar? (Yape, Tarjeta, Efectivo)")
    entrada = st.text_input("✍️ Escribe tu método de pago:", key="pago_input")
    if entrada:
        metodo = buscar_coincidencia(entrada, pagos)
        if metodo:
            st.session_state.pedido["metodo_pago"] = metodo
            st.session_state.step = 5
            st.rerun()
        else:
            st.error("❌ Medio de pago no reconocido. Escribe: Yape, Tarjeta o Efectivo.")

# Paso 5: Confirmación
elif st.session_state.step == 5:
    metodo = st.session_state.pedido["metodo_pago"]
    st.success("✅ ¡Pedido registrado con éxito!")

    if metodo == "yape":
        st.markdown("📲 Escanea este QR para pagar con Yape:")
        st.image("https://i.ibb.co/QFZ0Wwv/yape-qr.png", width=200)
        # para poner tu imagen QR: https://imgbb.com/ o https://postimages.org/
    elif metodo == "tarjeta":
        st.markdown("💳 Un mozo se acercará con el POS para cobrarte.")
    else:
        st.markdown("💵 Un mozo se acercará para recibir el efectivo.")

    st.markdown("⏱️ Tu pedido estará listo en **25 minutos**. ¡Gracias por visitarnos! 🙌")

    if st.button("🆕 Hacer otro pedido"):
        st.session_state.step = 1
        st.session_state.pedido = {}
        st.rerun()
