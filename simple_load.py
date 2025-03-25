#!/usr/bin/python3

print("Content-type: text/html\n")
print("<html><body>")

try:
    import cgi
    import MySQLdb
    from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_PREFIX
    
    # Get the workspace name
    form = cgi.FieldStorage()
    name = form.getfirst('name', '').replace("'", '')
    
    if not name:
        print("<p>No workspace name provided.</p>")
    else:
        print(f"<p>Looking for workspace: {name}</p>")
        
        # Connect to database
        conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
        cursor = conn.cursor()
        
        # Get the workspace data - using simplest possible query
        table_name = f"{TABLE_PREFIX}workspaces0"
        cursor.execute(f"SELECT wsid, nextNoteNum, time FROM {table_name} WHERE wsname=%s", [name])
        row = cursor.fetchone()
        
        if row:
            wsid, nextNoteNum, lasttime = row
            print(f"<p>Found workspace: ID={wsid}, NextNoteNum={nextNoteNum}, Time={lasttime}</p>")
            
            # Get notes
            table_name = f"{TABLE_PREFIX}notes0"
            cursor.execute(f"SELECT * FROM {table_name} WHERE wsid=%s", [wsid])
            notes = cursor.fetchall()
            
            print(f"<p>Found {len(notes)} notes</p>")
        else:
            print("<p>Workspace not found.</p>")
            
except Exception as e:
    import traceback
    print(f"<h2>Error:</h2><p>{str(e)}</p>")
    print("<pre>")
    traceback.print_exc()
    print("</pre>")

print("</body></html>")
