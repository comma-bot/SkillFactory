from pprint import pprint
from requests import post

import mysql.connector

from random import choice
from string import ascii_lowercase

def randomString(stringLength=10):
    return ''.join(choice(ascii_lowercase) for i in range(stringLength))

def get_data():

    r = post('http://84.201.129.203:4545/get_structure_course')
    data = r.json()

    blocks = data['blocks']
    _cortages = []
    def make_block_printer(blocks,delimiter,cortages):
        def block_printer(block_id,level=0,parent_id='NULL'):
            
            print('{}{}\t{}'.format(
                delimiter * level,
                blocks[block_id]['display_name'],
                blocks[block_id]['block_id']))
            
            cortages.append((
                parent_id,
                blocks[block_id]['block_id'],
                blocks[block_id]['display_name']))
            
            if 'children' in blocks[block_id].keys():
                for b_id in blocks[block_id]['children']:
                    block_printer(
                        b_id,
                        level+1,
                        blocks[block_id]['block_id'])

        return block_printer

    block_printer = make_block_printer(blocks,'-',_cortages)
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

    _tbl_name = randomString()

    create_table_command = "CREATE TABLE {} (parent_block_id CHAR(32), block_id CHAR(32) PRIMARY KEY ,name TEXT);"
    drop_table_command = "DROP TABLE IF EXISTS {};"

    mycursor.execute(create_table_command.format(_tbl_name))

    mycursor.executemany(
        "INSERT INTO {} (parent_block_id,block_id,name) VALUES (%s,%s,%s)".format(_tbl_name), 
        _cortages)

    mycursor.execute(drop_table_command.format(_tbl_name))
    mycursor.close()

if __name__ == '__main__':
    insert_data(_cortages)