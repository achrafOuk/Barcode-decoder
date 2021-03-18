import sqlite3
def create_connect(database):
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        pass
    return conn
def recherche_produit(conn,barcode_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM produit WHERE barcode_id=?", (barcode_id,))
    rows = cur.fetchone()
    liste=[]
    for index,j in enumerate(rows):
        liste.append(j)
    return liste


conn=create_connect("barcode_ti_product.db")
rows=recherche_produit(conn,"5901234123457")

#FetchedData=[list(map(str,i)) for i in rows]
print(rows[1])
