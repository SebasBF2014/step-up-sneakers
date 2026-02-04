import streamlit as st
import pandas as pd
from datetime import datetime

# Configurar página
st.set_page_config(
    page_title="Step Up Sneakers",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown("""
    <style>
        .product-card {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .price-tag {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
        }
        .discount-badge {
            background-color: #ff6b6b;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Base de datos de productos
PRODUCTOS = {
    "Zapatillas": [
        {"id": 1, "nombre": "Air Running Pro", "precio": 129.99, "imagen": "👟", "talla": "M", "color": "Negro"},
        {"id": 2, "nombre": "Classic Canvas", "precio": 79.99, "imagen": "👟", "talla": "M/L", "color": "Blanco"},
        {"id": 3, "nombre": "Street Style Kicks", "precio": 99.99, "imagen": "👟", "talla": "M", "color": "Azul"},
        {"id": 4, "nombre": "Premium Basketball", "precio": 149.99, "imagen": "🏀", "talla": "M", "color": "Rojo/Blanco"},
        {"id": 5, "nombre": "Casual Comfort Walk", "precio": 89.99, "imagen": "👟", "talla": "L", "color": "Gris"},
    ],
    "Camisetas": [
        {"id": 6, "nombre": "Athletic Fit Black", "precio": 29.99, "imagen": "👕", "talla": "S/M/L/XL", "color": "Negro"},
        {"id": 7, "nombre": "Sports Dri-Fit", "precio": 39.99, "imagen": "👕", "talla": "M/L", "color": "Azul"},
        {"id": 8, "nombre": "Streetwear Oversized", "precio": 34.99, "imagen": "👕", "talla": "M/L/XL", "color": "Blanco"},
    ],
    "Pantalones": [
        {"id": 9, "nombre": "Sport Joggers", "precio": 59.99, "imagen": "👖", "talla": "S/M/L", "color": "Negro"},
        {"id": 10, "nombre": "Classic Denim", "precio": 79.99, "imagen": "👖", "talla": "M/L/XL", "color": "Azul"},
        {"id": 11, "nombre": "Casual Chinos", "precio": 49.99, "imagen": "👖", "talla": "M/L", "color": "Beige"},
    ],
    "Accesorios": [
        {"id": 12, "nombre": "Sports Socks Pack", "precio": 19.99, "imagen": "🧦", "talla": "Único", "color": "Multicolor"},
        {"id": 13, "nombre": "Running Cap", "precio": 24.99, "imagen": "🧢", "talla": "Único", "color": "Negro"},
        {"id": 14, "nombre": "Gym Backpack", "precio": 44.99, "imagen": "🎒", "talla": "Único", "color": "Negro/Gris"},
    ]
}

# Códigos de descuento disponibles
DESCUENTOS = {
    "WELCOME20": {"porcentaje": 20, "descripcion": "Bienvenida - 20% descuento"},
    "SUMMER30": {"porcentaje": 30, "descripcion": "Verano - 30% descuento"},
    "SALE15": {"porcentaje": 15, "descripcion": "Venta general - 15% descuento"},
    "NEWUSER10": {"porcentaje": 10, "descripcion": "Nuevo usuario - 10% descuento"},
    "VIP50": {"porcentaje": 50, "descripcion": "VIP - 50% descuento exclusivo"},
    "FRIDAY15": {"porcentaje": 15, "descripcion": "Black Friday - 15% adicional"},
}

# Inicializar sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = []
if "codigo_aplicado" not in st.session_state:
    st.session_state.codigo_aplicado = None

# Header
st.markdown("# 👟 Step Up Sneakers")
st.markdown("### Tu tienda de ropa y zapatos premium")

# Menú
col1, col2, col3 = st.columns(3)
with col1:
    ver_tienda = st.button("🛍️ Ver Tienda", use_container_width=True)
with col2:
    ver_carrito = st.button("🛒 Carrito", use_container_width=True)
with col3:
    ver_codigos = st.button("🏷️ Códigos", use_container_width=True)

# Sección: Ver Tienda
if ver_tienda or (ver_carrito == False and ver_codigos == False):
    st.markdown("---")
    st.markdown("## Catálogo de Productos")
    
    # Filtro por categoría
    categoria = st.selectbox(
        "Selecciona una categoría:",
        list(PRODUCTOS.keys()),
        index=0
    )
    
    # Mostrar productos
    st.markdown(f"### {categoria}")
    
    cols = st.columns(2)
    for idx, producto in enumerate(PRODUCTOS[categoria]):
        col = cols[idx % 2]
        
        with col:
            st.markdown(f"""
            <div class="product-card">
                <h3>{producto['imagen']} {producto['nombre']}</h3>
                <p><strong>Precio:</strong> <span class="price-tag">${producto['precio']}</span></p>
                <p><strong>Color:</strong> {producto['color']}</p>
                <p><strong>Talla:</strong> {producto['talla']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            cantidad = st.number_input(
                f"Cantidad - {producto['nombre']}",
                min_value=0,
                max_value=10,
                value=0,
                key=f"qty_{producto['id']}"
            )
            
            if st.button(
                "➕ Agregar al carrito",
                key=f"btn_{producto['id']}",
                use_container_width=True
            ):
                if cantidad > 0:
                    # Verificar si el producto ya está en el carrito
                    producto_existe = False
                    for item in st.session_state.carrito:
                        if item["id"] == producto["id"]:
                            item["cantidad"] += cantidad
                            producto_existe = True
                            break
                    
                    if not producto_existe:
                        st.session_state.carrito.append({
                            **producto,
                            "cantidad": cantidad
                        })
                    
                    st.success(f"✅ {cantidad}x {producto['nombre']} agregado al carrito!")
                else:
                    st.warning("Selecciona una cantidad mayor a 0")

# Sección: Ver Carrito
if ver_carrito:
    st.markdown("---")
    st.markdown("## 🛒 Tu Carrito de Compras")
    
    if st.session_state.carrito:
        # Mostrar items del carrito
        df_carrito = pd.DataFrame(st.session_state.carrito)
        df_carrito["Subtotal"] = df_carrito["precio"] * df_carrito["cantidad"]
        
        st.dataframe(
            df_carrito[["nombre", "precio", "cantidad", "Subtotal", "color"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Calcular totales
        subtotal = df_carrito["Subtotal"].sum()
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Código de Descuento")
            codigo_ingresado = st.text_input(
                "Ingresa tu código de descuento:",
                placeholder="ej: WELCOME20"
            ).upper()
            
            if st.button("✓ Aplicar Código", use_container_width=True):
                if codigo_ingresado in DESCUENTOS:
                    st.session_state.codigo_aplicado = codigo_ingresado
                    st.success(f"✅ Código '{codigo_ingresado}' aplicado! {DESCUENTOS[codigo_ingresado]['descripcion']}")
                else:
                    st.error("❌ Código de descuento inválido")
            
            if st.session_state.codigo_aplicado:
                st.info(f"Código aplicado: {st.session_state.codigo_aplicado}")
                if st.button("Remover código", use_container_width=True):
                    st.session_state.codigo_aplicado = None
                    st.rerun()
        
        with col2:
            st.markdown("### Resumen de Pago")
            
            descuento_porcentaje = 0
            if st.session_state.codigo_aplicado:
                descuento_porcentaje = DESCUENTOS[st.session_state.codigo_aplicado]["porcentaje"]
            
            descuento_monto = subtotal * (descuento_porcentaje / 100)
            total = subtotal - descuento_monto
            impuesto = total * 0.08  # 8% de impuesto
            total_final = total + impuesto
            
            st.metric("Subtotal", f"${subtotal:.2f}")
            if descuento_porcentaje > 0:
                st.metric(
                    f"Descuento ({descuento_porcentaje}%)",
                    f"-${descuento_monto:.2f}",
                    delta=f"{descuento_porcentaje}% OFF"
                )
            st.metric("Impuesto (8%)", f"${impuesto:.2f}")
            st.markdown("---")
            st.metric("TOTAL A PAGAR", f"${total_final:.2f}")
            
            if st.button("💳 Proceder al Pago", use_container_width=True, type="primary"):
                st.success(f"✅ ¡Compra realizada! Total: ${total_final:.2f}")
                st.info("Tu pedido ha sido confirmado. Recibirás un email con los detalles.")
                st.session_state.carrito = []
                st.session_state.codigo_aplicado = None
        
        # Botón para limpiar carrito
        st.markdown("---")
        if st.button("🗑️ Limpiar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.session_state.codigo_aplicado = None
            st.rerun()
    
    else:
        st.info("Tu carrito está vacío. ¡Ve a la tienda para agregar productos!")

# Sección: Ver Códigos de Descuento
if ver_codigos:
    st.markdown("---")
    st.markdown("## 🏷️ Códigos de Descuento Disponibles")
    
    st.info("Usa estos códigos en tu carrito para obtener descuentos especiales:")
    
    for codigo, info in DESCUENTOS.items():
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"### `{codigo}`")
        with col2:
            st.markdown(f"**{info['descripcion']}**")
        with col3:
            st.markdown(f"<span class='discount-badge'>{info['porcentaje']}% OFF</span>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <center>
        <p style='color: gray; font-size: 12px;'>
            © 2024 Step Up Sneakers | Tienda Online Premium de Ropa y Zapatos
        </p>
    </center>
""", unsafe_allow_html=True)
