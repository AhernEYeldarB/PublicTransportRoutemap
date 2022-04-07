import psycopg2

connection = psycopg2.connect("dbname=ireland_osm user=postgres password=''")
cursor = connection.cursor()
query = 'SELECT id, ST_X(geom), ST_Y(geom) FROM nodes WHERE ST_Intersects(nodes.geom, ST_Buffer(ST_SetSRID(ST_MakePoint(-8.475218,51.897479), 4326), 0.06673844474));'
cursor.execute(query)
stops = cursor.fetchall()


with open('outfile.txt', 'w') as outfile:
    # print('id,latitude,longitude')
    outfile.write('id,longitude,latitude')
    for i in stops:
        outfile.write('%s,%s,%s\n'%(i[0], i[1], i[2]))
        # print('%s,%s,%s'%(i[0], i[1], i[2]))
