#!/usr/bin/python3

print("Content-type: text/html\n")
print("<html><head><title>Complete Apples Fix</title></head><body>")
print("<h1>Complete Fix for Apples Workspace</h1>")

import sys
import MySQLdb
import datetime
import traceback
from etc.common import *

try:
    # Connect to the database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Find and delete the apples workspace completely
    print("<p>Looking for and removing 'apples' workspace...</p>")
    
    # First, get the workspace ID
    cursor.execute(f"SELECT wsid FROM {TABLE_PREFIX}workspaces0 WHERE wsname='apples'")
    row = cursor.fetchone()
    
    if not row:
        print("<p>No 'apples' workspace found! Creating fresh one...</p>")
        wsid = None
    else:
        wsid = row[0]
        print(f"<p>Found 'apples' workspace with ID {wsid}</p>")
        
        # Delete all notes for this workspace
        print("<p>Deleting all notes for this workspace...</p>")
        cursor.execute(f"DELETE FROM {TABLE_PREFIX}notes0 WHERE wsid=%s", [wsid])
        deleted_notes = cursor.rowcount
        print(f"<p>Deleted {deleted_notes} notes</p>")
        
        # Delete the workspace itself
        print("<p>Removing workspace record...</p>")
        cursor.execute(f"DELETE FROM {TABLE_PREFIX}workspaces0 WHERE wsid=%s", [wsid])
        
    # Also check for apples_new and delete it if exists
    cursor.execute(f"SELECT wsid FROM {TABLE_PREFIX}workspaces0 WHERE wsname='apples_new'")
    row = cursor.fetchone()
    if row:
        apples_new_id = row[0]
        print(f"<p>Found 'apples_new' workspace with ID {apples_new_id}, deleting it...</p>")
        cursor.execute(f"DELETE FROM {TABLE_PREFIX}notes0 WHERE wsid=%s", [apples_new_id])
        cursor.execute(f"DELETE FROM {TABLE_PREFIX}workspaces0 WHERE wsid=%s", [apples_new_id])
    
    # Create fresh timestamp
    new_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create a completely new apples workspace
    print("<p>Creating fresh 'apples' workspace...</p>")
    cursor.execute(f"INSERT INTO {TABLE_PREFIX}workspaces0 (wsname, nextNoteNum, time) VALUES (%s, %s, %s)",
                  ["apples", 3, new_timestamp])
    new_wsid = cursor.lastrowid
    
    # Add three sample notes with different positions and colors
    cursor.execute(f"INSERT INTO {TABLE_PREFIX}notes0 (noteid, text, bgcolor, xposition, yposition, "
                 f"height, width, zindex, wsid, time) VALUES "
                 f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 ("note0", "This is the first note in the fresh apples workspace", 
                  "#ffff30", 100, 100, 150, 250, 1, new_wsid, new_timestamp))
    
    cursor.execute(f"INSERT INTO {TABLE_PREFIX}notes0 (noteid, text, bgcolor, xposition, yposition, "
                 f"height, width, zindex, wsid, time) VALUES "
                 f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 ("note1", "This is a blue note", 
                  "#8facff", 300, 200, 150, 250, 2, new_wsid, new_timestamp))
    
    cursor.execute(f"INSERT INTO {TABLE_PREFIX}notes0 (noteid, text, bgcolor, xposition, yposition, "
                 f"height, width, zindex, wsid, time) VALUES "
                 f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 ("note2", "This is a green note with a longer text that has spaces in it. Let's see if this works correctly.",
                  "#7fff70", 500, 300, 200, 300, 3, new_wsid, new_timestamp))
    
    conn.commit()
    
    print("<p>Creation complete! Created fresh 'apples' workspace with ID " + str(new_wsid) + " and three test notes.</p>")
    print(f"<p>You can now access the new workspace at: <a href='load.py?name=apples'>apples</a></p>")
    
except Exception as e:
    print(f"<h2>Error</h2><p>{str(e)}</p>")
    print("<pre>")
    print(traceback.format_exc())
    print("</pre>")

print("</body></html>")
