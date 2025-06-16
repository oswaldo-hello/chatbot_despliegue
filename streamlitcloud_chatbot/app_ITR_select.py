import streamlit as st

# Menús
platos = {
    "Arroz chaufa": 20,
    "Lomo saltado": 22,
    "Ensalada vegetal": 18,
    "Pollo a la brasa": 25,
    "Sopa criolla": 19
}

postres = {
    "Mazamorra morada": 8,
    "Arroz con leche": 7,
    "No, gracias": 0
}

bebidas = {
    "Chicha morada": 5,
    "Inca Kola": 6,
    "Agua": 4,
    "No, gracias": 0
}

# Inicializa sesión
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.pedido = {}

# Paso 1: Bienvenida y selección de plato
if st.session_state.step == 1:
    st.title("🍽️ Bienvenido al asistente del restaurante")
    st.markdown("Hola 👋 Soy tu asistente virtual. Aquí están nuestros platos del día:")

    for nombre, precio in platos.items():
        st.write(f"✅ **{nombre}** - S/ {precio}")

    plato = st.selectbox("¿Cuál deseas pedir?", list(platos.keys()))
    if st.button("Confirmar plato"):
        st.session_state.pedido["plato"] = plato
        st.session_state.pedido["precio_plato"] = platos[plato]
        st.session_state.step = 2
        st.rerun()

# Paso 2: Postre
elif st.session_state.step == 2:
    st.markdown(f"🥘 Excelente elección: **{st.session_state.pedido['plato']}**")
    postre = st.radio("¿Te gustaría acompañarlo con un postre?", list(postres.keys()))
    if st.button("Confirmar postre"):
        st.session_state.pedido["postre"] = postre
        st.session_state.pedido["precio_postre"] = postres[postre]
        st.session_state.step = 3
        st.rerun()

# Paso 3: Bebida
elif st.session_state.step == 3:
    bebida = st.radio("¿Deseas una bebida para acompañar?", list(bebidas.keys()))
    if st.button("Confirmar bebida"):
        st.session_state.pedido["bebida"] = bebida
        st.session_state.pedido["precio_bebida"] = bebidas[bebida]
        st.session_state.step = 4
        st.rerun()

# Paso 4: Pago
elif st.session_state.step == 4:
    total = st.session_state.pedido["precio_plato"] + st.session_state.pedido["precio_postre"] + st.session_state.pedido["precio_bebida"]
    st.markdown("🧾 Aquí está tu pedido:")
    st.write(f"🍽️ Plato: {st.session_state.pedido['plato']} - S/ {st.session_state.pedido['precio_plato']}")
    st.write(f"🍰 Postre: {st.session_state.pedido['postre']} - S/ {st.session_state.pedido['precio_postre']}")
    st.write(f"🥤 Bebida: {st.session_state.pedido['bebida']} - S/ {st.session_state.pedido['precio_bebida']}")
    st.markdown(f"**💰 Total a pagar: S/ {total}**")

    metodo = st.radio("¿Cómo deseas pagar?", ["Yape", "Tarjeta", "Efectivo"])

    if st.button("Confirmar pago"):
        st.session_state.pedido["metodo_pago"] = metodo
        st.session_state.step = 5
        st.rerun()

# Paso 5: Confirmación final
elif st.session_state.step == 5:
    metodo = st.session_state.pedido["metodo_pago"]
    st.success("✅ ¡Pedido registrado con éxito!")

    if metodo == "Yape":
        st.markdown("📲 Escanea este código QR para pagar con Yape:")
        st.image("https://i.ibb.co/QFZ0Wwv/yape-qr.png", width=200)
    elif metodo == "Tarjeta":
        st.markdown("💳 Un mozo se acercará con el POS para realizar el cobro.")
    else:
        st.markdown("💵 Un mozo se acercará para cobrarte en efectivo.")

    st.markdown("⏱️ **Tu pedido estará listo en aproximadamente 25 minutos.** ¡Gracias por tu visita! 🙌")

    if st.button("Hacer otro pedido"):
        st.session_state.step = 1
        st.session_state.pedido = {}
        st.rerun()
