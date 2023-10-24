import sys

sys.path.append('.\\utils')

import render_pdf
import pandas as pd
import streamlit as st


def new_df():
    df = pd.DataFrame(columns=['Cantidad', 'Nº de Parte',
                               'Descripcion', 'Valor Unitario'])
    st.session_state.repuestos = df

def new_repuestos():
    n = len(st.session_state.repuestos)
    st.session_state.repuestos.loc[n] = [
        st.session_state.cnt, st.session_state.parte,
        st.session_state.desc, st.session_state.price
    ]

def save():

    buyer_id = conn.query(f"""SELECT * FROM buyers
                          WHERE company_name='{option}'""", ttl=0)['buyer_id'].iloc[0]
                          
    with conn.session as s:
        #s.execute('DELETE FROM receptor;')

        s.execute(
            """INSERT INTO quotes (buyer_id, vehicle, vin)
            VALUES (:buyer_id, :vehicle, :vin);""",
            params=dict(buyer_id=int(buyer_id), vehicle=st.session_state.vehicle,
                        vin=st.session_state.vin)
        )

        for _, row in st.session_state.repuestos.iterrows():
            s.execute(
            """INSERT INTO parts (quote_id, amount, description, price, part_number)
            VALUES (:quote_id, :amount, :description, :price, :part_number);""",
            params=dict(quote_id=st.session_state.next_id, amount=row['Cantidad'],
                        description=row['Descripcion'], price=row['Valor Unitario'],
                        part_number=row['Nº de Parte'])
            )

        context = render_pdf.get_context(st.session_state.repuestos)
        NUM = st.session_state.next_id
        my_context = {'num': NUM, 'vehicle': st.session_state.vehicle,
                      'vin': st.session_state.vin, 'name': option}
        context.update(my_context)

        render_pdf.render(context, f'{st.secrets.render_path.output_render}/COTIZACION {NUM}.pdf')

        s.commit()

    new_df()
    

st.set_page_config(
    page_title='Crear Cotizacion',
    page_icon='🧰'
)

conn = st.experimental_connection('imgec_db', type='sql')

LAST_ID = conn.query("""SELECT * FROM quotes
                     WHERE quote_id=(
                     SELECT max(quote_id) FROM quotes)""", ttl=0)['quote_id'].iloc[0]

st.session_state.next_id = int(LAST_ID) + 1

st.title(f"🧰 Cotizacion Nº {st.session_state.next_id}")

buyers = conn.query('SELECT * FROM buyers', ttl=0)

if "repuestos" not in st.session_state:
    new_df()

st.write("# Agrega informacion")

with st.form("info", clear_on_submit=False):
    option = st.selectbox(
        "Selecciona un comprador.",
        tuple(buyers['company_name']),
        index=None,
        placeholder="Comprador...",
    )
    vehicle = st.text_input('Vehiculo', key="vehicle")
    vin = st.text_input('VIN', key="vin")
    st.form_submit_button("Actualizar info")

st.write("# Tabla Repuestos")

st.write(st.session_state.repuestos)

st.write("# Agrega un nuevo repuesto")
with st.form("new_repuesto", clear_on_submit=True):
    desc = st.text_input('Descripcion', key="desc")
    parte = st.text_input('Nº de Parte', key="parte")
    price = st.text_input('Valor Unitario', key="price")
    cnt = st.text_input('Cantidad', key="cnt")
    st.form_submit_button("Agregar", on_click=new_repuestos)

col1, col2 = st.columns([0.8, 0.2], gap="large")

with col1:
    st.button("Vaciar", on_click=new_df)

with col2:
    st.button("Guardar", on_click=save)
