#!/usr/bin/python3

import cgi
from etc.common import *
from lib import Db
import sys

def main():
    print("Content-type: text/plain\n")
    
    form = cgi.FieldStorage()
    wsname = form.getfirst('name', '')
    
    # make sure it's a valid request
    if not wsname:
        print('')
        return
    
    # Connect to database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Get latest timestamp for workspace
    table_name = f"{TABLE_PREFIX}workspaces0"
    cursor.execute(f"SELECT DATE_FORMAT(time, '%%Y-%%m-%%d %%H:%%i:%%s') FROM {table_name} WHERE wsname=%s", [wsname])
    row = cursor.fetchone()
    
    if row and row[0]:
        print(row[0])
    else:
        print('')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        with open('/tmp/webnote_getrecent_error.log', 'a') as f:
            f.write(f"\n--- Error in getrecent.py ---\n")
            f.write(traceback.format_exc())
        print('')
