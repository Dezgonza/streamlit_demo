import sys

sys.path.append('.\\utils')

import sii_sign
import streamlit as st    


def sign():
    numero = option.split(' ')[-1]
    cotizacion = conn.query(f"select * from cotizacion where id='{numero}'", ttl=0)
    id, id_receptor = cotizacion['id'].loc[0], cotizacion['id_receptor'].loc[0]
    repuestos = conn.query(f"select * from repuesto where id_cotizacion='{id}'", ttl=0)
    articulos = [list(repuestos.loc[i]) for i in range(len(repuestos))]
    receptor = conn.query(f"select * from receptor where id='{id_receptor}'", ttl=0)
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

cotizaciones = conn.query('select * from cotizacion', ttl=0)
cotizaciones['numero_cot'] = 'Cotizacion Nº ' + cotizaciones['id'].astype(str)

option = st.selectbox(
        "Selecciona una cotizacion para firmar.",
        tuple(cotizaciones['numero_cot']),
        index=None,
        placeholder="Cotizacion...",
    )

st.write('Seleccionaste:', option)

st.button("Firmar", on_click=sign)
