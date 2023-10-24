import streamlit as st

def new_buyer():
                          
    with conn.session as s:
        #s.execute('DELETE FROM receptor;')
        s.execute(
        'INSERT INTO buyers (company_name, rut, mail) VALUES (:company_name, :rut, :mail);',
        params=dict(company_name=st.session_state.name, rut=st.session_state.rut,
                    mail=st.session_state.mail)
        )
        s.commit()

def edit_buyer():
    
    with conn.session as s:
        #s.execute('DELETE FROM receptor;')
        s.execute(
        """UPDATE buyers SET company_name='{}', rut='{}', mail='{}'
        WHERE company_name='{}';""".format(st.session_state.new_name,
                                          st.session_state.new_rut,
                                          st.session_state.new_mail,
                                          option))
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
    submit_button = st.form_submit_button("Agregar")

if submit_button:
    if name == '':
        st.error("Debe ingresar el nombre del contacto")
    else:
        new_buyer()
        st.success(f"Se ha creado el contacto para {name}")

buyers = conn.query('SELECT * FROM buyers', ttl=0)

st.write("# Edita un comprador")

option = st.selectbox(
        "Selecciona un comprador.",
        tuple(buyers['company_name']),
        index=None,
        placeholder="Comprador...",
    )

if option is not None:

    buyer = buyers[buyers.company_name == option]

    with st.form("edit_buyer", clear_on_submit=True):
        new_name = st.text_input('Razon Social', key="new_name", value=option)
        new_rut = st.text_input('RUT', key="new_rut", value=buyer.rut.iloc[0])
        new_mail = st.text_input('E-mail', key="new_mail", value=buyer.mail.iloc[0])
        edit_button = st.form_submit_button("Actualizar")

    if edit_button:
        if new_name == '':
            st.error("Debe ingresar el nombre del contacto")
        else:
            edit_buyer()
            st.success(f"Se ha editado el contacto de {option}")
            st.rerun()

buyers = conn.query('SELECT * FROM buyers', ttl=0)
st.dataframe(buyers)
