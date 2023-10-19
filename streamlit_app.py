import streamlit as st

# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.experimental_connection('imgec_db', type='sql')

start_id = 721

with conn.session as s:

    s.execute("""CREATE TABLE IF NOT EXISTS cotizacion(id integer primary key autoincrement,
                                                       id_receptor integer, vehiculo varchar(50), 
                                                       vin varchar(50))""")
    s.execute("""CREATE TABLE IF NOT EXISTS repuesto(id_cotizacion integer, cantidad integer,
                                                     descripcion varchar(50), precio integer,
                                                     numero_parte varchar(50))""")
    s.execute("""CREATE TABLE IF NOT EXISTS receptor(id integer primary key autoincrement,
                                                     razon_social varchar(50), rut varchar(50),
                                                     mail varchar(50))""")
    
    s.execute("""INSERT INTO cotizacion (id, id_receptor, vehiculo, vin)
              VALUES (:id, :id_receptor, :vehiculo, :vin);""",
              params=dict(id=start_id, id_receptor=-1, vehiculo="", vin="")
              )
    s.commit()

# Query and display the data you inserted
pet_owners = conn.query('select * from repuesto')
st.dataframe(pet_owners)
