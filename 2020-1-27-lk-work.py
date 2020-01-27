from requests import post

import mysql.connector
from datetime import datetime, date, time

def get_data():

    r = post('http://84.201.129.203:4545/get_structure_course')
    data = r.json()

    blocks = data['blocks']
    _cortages = []
    def make_block_printer(blocks,delimiter,cortages):
        def block_printer(block_id,level=0,parent_id='NULL'):
            
            cortages.append((
                parent_id,
                blocks[block_id]['block_id'],
                blocks[block_id]['display_name'],
                datetime.now()))
            
            if 'children' in blocks[block_id].keys():
                for b_id in blocks[block_id]['children']:
                    block_printer(
                        b_id,
                        level+2,
                        blocks[block_id]['block_id'])

        return block_printer

    block_printer = make_block_printer(blocks,' ',_cortages)
    block_printer(data['root'])

    return _cortages

def insert_data(_cortages):
 
     mydb = mysql.connector.connect(
         host="84.201.129.203",
         port="32769",
         user="user1",
         passwd="qkfurf65ff~",
         auth_plugin='mysql_native_password',
         database='test'
     )
 
     mycursor = mydb.cursor()
 
     create_table_command = "CREATE TABLE SKILL (parent_block_id CHAR(32), block_id CHAR(32) PRIMARY KEY ,name TEXT, update DATE);"
     drop_table_command = "DROP TABLE IF EXISTS SKILL;"
 
     mycursor.execute(drop_table_command)
     mycursor.execute(create_table_command)
 
     mycursor.executemany(
         "INSERT INTO SKILL (parent_block_id,block_id,name,update) VALUES (%s,%s,%s,%s)", _cortages)

     mycursor.close()
 
if __name__ == '__main__':
     insert_data(get_data())
