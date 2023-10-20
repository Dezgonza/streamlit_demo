import os
import sys

sys.path.append('.\\utils')

import subprocess
import render_pdf
import streamlit as st
    

def filter_buyer(opt):

    buyer_id = buyers[buyers.razon_social == option_buyer]['id'].iloc[0]
    cotizaciones = conn.query(f"select * from cotizacion where id_receptor='{buyer_id}'", ttl=0)
    cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['id'].astype(str)
    
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

print(option_buyer)

if option_buyer is not None:

    print(option_buyer)

    cotizaciones = filter_buyer(option_buyer)

    print(cotizaciones)

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

    cotizaciones = conn.query(f"select * from cotizacion", ttl=0)
    cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['id'].astype(str)

    option_cotizacion = st.selectbox(
        "Selecciona una cotizacion para mostrar.",
        tuple(cotizaciones['numero_cot']),
        index=None,
        placeholder="Cotizacion...",
    )

    if option_cotizacion is not None:
        visualize(option_cotizacion)

        st.button("Mostrar en directorio", on_click=show_folder, args=[option_cotizacion])
