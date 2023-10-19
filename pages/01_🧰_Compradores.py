import streamlit as st

def new_buyer():
                          
    with conn.session as s:
        #s.execute('DELETE FROM receptor;')
        s.execute(
        'INSERT INTO receptor (razon_social, rut, mail) VALUES (:razon_social, :rut, :mail);',
        params=dict(razon_social=st.session_state.name, rut=st.session_state.rut,
                    mail=st.session_state.mail)
        )
        s.commit()

st.set_page_config(
    page_title='Compradores',
    page_icon='🧰'
)

st.title("🧰 Compradores")

conn = st.experimental_connection('imgec_db', type='sql')

st.write("# Agrega un nuevo comprador")
with st.form("new_buyer", clear_on_submit=True):
    name = st.text_input('Razon Social', key="name")
    rut = st.text_input('RUT', key="rut")
    mail = st.text_input('E-mail', key="mail")
    st.form_submit_button("Agregar", on_click=new_buyer)

buyers = conn.query('select * from receptor', ttl=0)
st.dataframe(buyers)
