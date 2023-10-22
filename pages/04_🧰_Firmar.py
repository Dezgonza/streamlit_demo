import sys

sys.path.append('.\\utils')

import sii_sign
import streamlit as st    


def sign():
    numero = option.split(' ')[-1]
    cotizacion = conn.query(f"SELECT * FROM quotes WHERE quote_id='{numero}'", ttl=0)
    id, id_receptor = cotizacion['quote_id'].loc[0], cotizacion['buyer_id'].loc[0]
    repuestos = conn.query(f"SELECT * FROM parts WHERE quote_id='{id}'", ttl=0)
    articulos = [list(repuestos.loc[i]) for i in range(len(repuestos))]
    receptor = conn.query(f"SELECT * FROM buyers WHERE buyer_id='{id_receptor}'", ttl=0)
    rut, mail = receptor['rut'].loc[0], receptor['mail'].loc[0]
    # print(rut, mail)
    # print(articulos)
    sii_sign.main(rut, articulos)


st.set_page_config(
    page_title='Firma Electronica',
    page_icon='🧰'
)

st.title("🧰 Firma Electronica")

conn = st.experimental_connection('imgec_db', type='sql')

cotizaciones = conn.query('SELECT * FROM quotes', ttl=0)
cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['quote_id'].astype(str)

option = st.selectbox(
        "Selecciona una cotizacion para firmar.",
        tuple(cotizaciones['numero_cot']),
        index=None,
        placeholder="Cotizacion...",
    )

st.write('Seleccionaste:', option)

st.button("Firmar", on_click=sign)
