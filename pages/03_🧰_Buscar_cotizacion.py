import os
import sys

sys.path.append('.\\utils')

import subprocess
import render_pdf
import streamlit as st
    

def filter_buyer(opt):

    buyer_id = buyers[buyers.company_name == option_buyer]['buyer_id'].iloc[0]
    cotizaciones = conn.query(f"SELECT * FROM quotes WHERE buyer_id='{buyer_id}'", ttl=0)
    cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['quote_id'].astype(str)
    
    return cotizaciones

def visualize(option_cotizacion):

    numero = option_cotizacion.split(' ')[-1]
    path = f'COTIZACION {numero}.pdf'
    pdf_display = render_pdf.show_pdf(path)
    st.markdown(pdf_display, unsafe_allow_html=True)

def show_folder(option_cotizacion):
    numero = option_cotizacion.split(' ')[-1]
    query_string = f'COTIZACION {numero}.pdf'
    local_path = r"C:\Users\Gonzalo\Documents\Git\sii" # r is raw for dealing with backslashes
    subprocess.Popen(f'explorer /select, {local_path}\{query_string}')


st.set_page_config(
    page_title='Buscar Cotizacion',
    page_icon='🧰'
)

st.title("🧰 Buscar Cotizacion")

conn = st.experimental_connection('imgec_db', type='sql')

buyers = conn.query('SELECT * FROM buyers', ttl=0)
# st.dataframe(buyers)

# refs = conn.query('select * from repuesto', ttl=0)
# st.dataframe(refs)

# cotizaciones = conn.query('select * from cotizacion', ttl=0)
# cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['numero'].astype(str)

option_buyer = st.selectbox(
    "Selecciona un comprador.",
    tuple(buyers['company_name']),
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

        st.button("Mostrar en directorio", on_click=show_folder, args=[option_cotizacion])

if option_buyer is None:

    cotizaciones = conn.query(f"SELECT * FROM quotes", ttl=0)
    cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['quote_id'].astype(str)

    option_cotizacion = st.selectbox(
        "Selecciona una cotizacion para mostrar.",
        tuple(cotizaciones['numero_cot']),
        index=None,
        placeholder="Cotizacion...",
    )

    if option_cotizacion is not None:
        visualize(option_cotizacion)

        st.button("Mostrar en directorio", on_click=show_folder, args=[option_cotizacion])
