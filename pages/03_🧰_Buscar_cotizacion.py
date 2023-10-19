import sys

sys.path.append('.\\utils')

import render_pdf
import streamlit as st
    

def filter_buyer(opt):

    buyer_id = buyers[buyers.razon_social == option_buyer]['id'].iloc[0]
    cotizaciones = conn.query(f"select * from cotizacion where id_receptor='{buyer_id}'", ttl=0)
    cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['numero'].astype(str)
    
    return cotizaciones

def visualize(option_cotizacion):

    numero = option_cotizacion.split(' ')[-1]
    path = f'COTIZACION {numero}.pdf'
    pdf_display = render_pdf.show_pdf(path)
    st.markdown(pdf_display, unsafe_allow_html=True)

st.set_page_config(
    page_title='Buscar Cotizacion',
    page_icon='🧰'
)

st.title("🧰 Buscar Cotizacion")

conn = st.experimental_connection('imgec_db', type='sql')

buyers = conn.query('select * from receptor', ttl=0)
# st.dataframe(buyers)

# refs = conn.query('select * from repuesto', ttl=0)
# st.dataframe(refs)

# cotizaciones = conn.query('select * from cotizacion', ttl=0)
# cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['numero'].astype(str)

option_buyer = st.selectbox(
    "Selecciona un comprador.",
    tuple(buyers['razon_social']),
    index=None,
    placeholder="Comprador...",
)

# st.button("Filtrar", on_click=filter_buyer)

if option_buyer is not None:
    cotizaciones = filter_buyer(option_buyer)

    option_cotizacion = st.selectbox(
        "Selecciona una cotizacion para mostrar.",
        tuple(cotizaciones['numero_cot']),
        index=None,
        placeholder="Cotizacion...",
    )

    if option_cotizacion is not None:
        visualize(option_cotizacion)
