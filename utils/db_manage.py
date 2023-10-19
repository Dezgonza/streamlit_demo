def create_db(session):

    session.execute("""CREATE TABLE IF NOT EXISTS cotizacion(id integer primary key autoincrement,
                                                             numero integer, id_receptor integer,
                                                             vehiculo varchar(50), vin varchar(50))""")
    session.execute("""CREATE TABLE IF NOT EXISTS repuesto(id_cotizacion integer, cantidad integer,
                                                           descripcion varchar(50), precio integer,
                                                           numero_parte varchar(50))""")
    session.execute("""CREATE TABLE IF NOT EXISTS receptor(id integer primary key autoincrement,
                                                           razon_social varchar(50), rut varchar(50))""")
