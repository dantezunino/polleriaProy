import sqlite3

def agregarUsuario(name, passw, cert, actprivi):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    privi = 0
    #"Administrador", "Usuario con privilegios", "Usuario comun"
    if cert == "Administrador":
        privi=1
    if cert == "Usuario con privilegios":
        privi=2
    if cert == "Usuario comun":
        privi=3
    info = [name, passw, privi]
    print(info[0], info[1], info[2], actprivi)
    if actprivi != 0:
        print("No tienes los permisos")
        conn.close()
    else:
        c.execute("INSERT INTO usuarios VALUES (NULL, ?, ?, ?)", info)
        conn.commit()
        conn.close()

def loggearUsuario(name, passw, cond, privi):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM usuarios ORDER BY id'):
        if row[1] == name:
            if row[2] == passw:
                cond[0] = True
                privi[0] = row[3]
        else:
            pass
    conn.commit()
    conn.close()

def leerMateriaPrima(dat1, dat2, dat3, dat4, dat5):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM materiaprima ORDER BY id'):
        dat1.append(row[0])
        dat2.append(row[1])
        dat3.append(row[2])
        dat4.append(row[3])
        dat5.append(row[4])
    conn.commit()
    conn.close()

def leerProductos(dat1, dat2, dat3, dat4):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM productos ORDER BY id'):
        dat1.append(row[0])
        dat2.append(row[1])
        dat3.append(row[2])
        dat4.append(row[3])
    conn.commit()
    conn.close()