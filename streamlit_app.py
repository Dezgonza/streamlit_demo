import os
import streamlit as st
from utils import db_manage

#os.remove('imgec.db')

# Create the SQL connection to pets_db as specified in your secrets file.
if not os.path.exists('imgec.db'):

    conn = st.experimental_connection('imgec_db', type='sql')

    with conn.session as s:

        db_manage.create_db(s, start_by=721)

# Query and display the data you inserted
# pet_owners = conn.query('select * from repuesto')
# st.dataframe(pet_owners)
