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

    buyer_id = conn.query(f"""select id from receptor
                          where razon_social='{option}'""", ttl=0)['id'].iloc[0]
                          
    with conn.session as s:
        #s.execute('DELETE FROM receptor;')

        s.execute(
            """INSERT INTO cotizacion (id_receptor, vehiculo, vin)
            VALUES (:id_receptor, :vehiculo, :vin);""",
            params=dict(id_receptor=buyer_id, vehiculo=st.session_state.vehicule,
                        vin=st.session_state.vin)
        )

        for _, row in st.session_state.repuestos.iterrows():
            s.execute(
            """INSERT INTO repuesto (id_cotizacion, cantidad, descripcion, precio, numero_parte)
            VALUES (:id_cotizacion, :cantidad, :descripcion, :precio, :numero_parte);""",
            params=dict(id_cotizacion=st.session_state.next_id, cantidad=row['Cantidad'],
                        descripcion=row['Descripcion'], precio=row['Valor Unitario'],
                        numero_parte=row['Nº de Parte'])
            )
        s.commit()

    context = render_pdf.get_context(st.session_state.repuestos)
    NUM = st.session_state.num
    my_context = {'num': NUM, 'vehicule': st.session_state.vehicule,
                  'vin': st.session_state.vin}
    context.update(my_context)

    render_pdf.render(context, f"COTIZACION {NUM}.pdf")
    new_df()
    

st.set_page_config(
    page_title='Crear Cotizacion',
    page_icon='🧰'
)

conn = st.experimental_connection('imgec_db', type='sql')

LAST_ID = conn.query("""select * from cotizacion
                     where id=(select max(id) from cotizacion)""", ttl=0)['id'].iloc[0]
st.session_state.next_id = LAST_ID + 1

st.title(f"🧰 Cotizacion Nº {st.session_state.next_id}")

buyers = conn.query('select * from receptor', ttl=0)
# st.dataframe(buyers)

# refs = conn.query('select * from repuesto', ttl=0)
# st.dataframe(refs)

if "repuestos" not in st.session_state:
    new_df()

# st.write('Seleccionaste:', option)

# st.write(st.session_state.repuestos)

st.write("# Agrega informacion")

with st.form("info", clear_on_submit=False):
    option = st.selectbox(
        "Selecciona un comprador.",
        tuple(buyers['razon_social']),
        index=None,
        placeholder="Comprador...",
    )
    vehicule = st.text_input('Vehiculo', key="vehicule")
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
