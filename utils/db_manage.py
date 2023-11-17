def create_db(session, start_by=None):

    session.execute("""CREATE TABLE IF NOT EXISTS buyers (
                    buyer_id integer primary key autoincrement,
                    company_name VARCHAR(50) NOT NULL,
                    rut VARCHAR(50),
                    mail VARCHAR(50));""")
    
    session.execute("""CREATE TABLE IF NOT EXISTS quotes (
                    quote_id integer primary key autoincrement,
                    buyer_id INT  NOT NULL,
                    vehicle VARCHAR(50) NOT NULL,
                    vin VARCHAR(50) NOT NULL,
                    signed BOOLEAN NOT NULL DEFAULT FALSE,
                    FOREIGN KEY (buyer_id) REFERENCES buyers(buyer_id));""")
        
    session.execute("""CREATE TABLE IF NOT EXISTS parts (
                    buyer_id INT,
                    quote_id INT,
                    amount INT NOT NULL,
                    description VARCHAR(50) NOT NULL,
                    price INT NOT NULL,
                    part_number VARCHAR(50) NOT NULL,
                    FOREIGN KEY (buyer_id) REFERENCES buyers(buyer_id),
                    FOREIGN KEY (quote_id) REFERENCES quotes(quote_id),
                    PRIMARY KEY (buyer_id, quote_id));""")
        
    if start_by:
        
        session.execute("""INSERT INTO quotes (quote_id, buyer_id, vehicle, vin)
                        VALUES (:quote_id, :buyer_id, :vehicle, :vin);""",
                        params=dict(quote_id=start_by, buyer_id=-1, vehicle="", vin="")
                        )
        
        session.commit()
