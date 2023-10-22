import os
import streamlit as st

os.remove('imgec.db')

# Create the SQL connection to pets_db as specified in your secrets file.
if not os.path.exists('imgec.db'):

    conn = st.experimental_connection('imgec_db', type='sql')

    with conn.session as s:

        s.execute("""CREATE TABLE IF NOT EXISTS buyers (
                  buyer_id integer primary key autoincrement,
                  company_name VARCHAR(50) NOT NULL,
                  rut VARCHAR(50),
                  mail VARCHAR(50));""")
        
        s.execute("""CREATE TABLE IF NOT EXISTS quotes (
                  quote_id integer primary key autoincrement,
                  buyer_id INT,
                  vehicle VARCHAR(50) NOT NULL,
                  vin VARCHAR(50) NOT NULL,
                  FOREIGN KEY (buyer_id) REFERENCES buyers(buyer_id));""")
        
        s.execute("""CREATE TABLE IF NOT EXISTS parts(
                  buyer_id INT,
                  quote_id INT,
                  amount INT NOT NULL,
                  description VARCHAR(50) NOT NULL,
                  price INT NOT NULL,
                  part_number VARCHAR(50) NOT NULL,
                  FOREIGN KEY (buyer_id) REFERENCES buyers(buyer_id),
                  FOREIGN KEY (quote_id) REFERENCES quotes(quote_id),
                  PRIMARY KEY (buyer_id, quote_id));""")
        
        s.execute("""INSERT INTO quotes (quote_id, buyer_id, vehicle, vin)
                VALUES (:quote_id, :buyer_id, :vehicle, :vin);""",
                params=dict(quote_id=721, buyer_id=-1, vehicle="", vin="")
                )
        
        s.commit()

# Query and display the data you inserted
# pet_owners = conn.query('select * from repuesto')
# st.dataframe(pet_owners)
