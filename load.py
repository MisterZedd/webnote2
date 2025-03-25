#!/usr/bin/python3

from etc.common import *
import sys
import urllib.parse
import MySQLdb
import cgi
import datetime

try:
    # Get the form data
    form = cgi.FieldStorage()
    wsname = form.getfirst('name', '').replace("'", '')
    
    if not wsname:
        # No workspace name provided, redirect to index
        print('Location: .\n\n')
        sys.exit(0)
    
    # Connect to the database
    conn = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)
    cursor = conn.cursor()
    
    # Look up the workspace
    table_name = f"{TABLE_PREFIX}workspaces0"
    cursor.execute(f"SELECT wsid, nextNoteNum, DATE_FORMAT(time, '%%Y-%%m-%%d %%H:%%i:%%s') FROM {table_name} WHERE wsname=%s", [wsname])
    row = cursor.fetchone()
    
    if not row:
        # Workspace doesn't exist, create a blank one
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f"INSERT INTO {table_name} (wsname, nextNoteNum, time) VALUES (%s, %s, %s)", 
                      [wsname, 0, timestamp])
        wsid = cursor.lastrowid
        nextNoteNum = 0
        lasttime = timestamp
        conn.commit()
        notes = []
    else:
        # Workspace exists, get notes
        wsid, nextNoteNum, lasttime = row
        
        # Get notes
        notes_table = f"{TABLE_PREFIX}notes0"
        cursor.execute(f"SELECT noteid, text, bgcolor, xposition, yposition, height, width, zindex FROM {notes_table} WHERE wsid=%s AND time=%s", 
                     [wsid, lasttime])
        notes = cursor.fetchall()
    
    # Generate HTML
    print("Content-type: text/html\n")
    print("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <meta http-equiv="X-UA-Compatible" content="IE=EmulateIE8" />
    <link rel="start"  type="text/html" href="http://www.aypwip.org/webnote/" 
         title="Webnote - an online tool for taking notes" />
    <link rel="SHORTCUT ICON" href="webnote_favicon.ico" type="image/x-icon" />
    <script type="text/javascript" src="objects.js"></script>
    <script type="text/javascript" src="strings.js"></script>
    <script type="text/javascript" src="webnote.js"></script>
    <script type="text/javascript">

<!--
function loadinit()
{
  debugOn = false;
  workspace.setName(unescape('""" + wsname + """'));
  workspace.loadedTime = '""" + lasttime + """';
  adminEmail = '""" + HELPEMAIL + """';
  baseURI = '""" + BASEURL + """';
  numDates = """ + str(NUM_DATES) + """;
  init();
""")
    
    # Add notes to the JavaScript
    for note in notes:
        noteid, text, bgcolor, xposition, yposition, height, width, zindex = note
        # Properly escape single quotes in text - this is the fix for the syntax error
        escaped_text = text.replace("'", "\\'")
        # Create the note using string concatenation, not f-strings with escapes
        print("  workspace.createNote({")
        print("    'noteid': '" + noteid + "',")
        print("    'text': '" + escaped_text + "',")
        print("    'bgcolor': '" + bgcolor + "',")
        print("    'xposition': " + str(xposition) + ",")
        print("    'yposition': " + str(yposition) + ",")
        print("    'height': " + str(height) + ",")
        print("    'width': " + str(width) + ",")
        print("    'zindex': " + str(zindex))
        print("  });")
    
    # Finish the JavaScript setup
    print("  workspace.nextNoteNum = " + str(nextNoteNum) + ";")
    print("  workspace.changed = false;")
    print("}")
    print("// -->")
    print("""    </script>
    <link rel="stylesheet" href="style.css" type="text/css" />
    <title>""" + wsname + """</title>
</head>
<body onload='loadinit();' style='background-color: #f0f0f0;'>
  <div id='content'>
    <div id='toolbar'>
        <div class='controls'>
          <img id="newImg" src='images/new.gif' class='controls' onclick="workspace.createNote()" alt='new note icon' />
          <img id="saveImg" src='images/save.gif' class='controlsDisabled' onclick="workspace.save()" alt='disk icon (save)' />
          <img id="reloadImg" src='images/reload.gif' class='controls' onclick="workspace.loadlist()" alt='reload icon' />
          <img id="undoImg" src='images/undo.gif' class='controlsDisabled' onclick="workspace.history.undo()" alt='undo icon' />
          <img id="redoImg" src='images/redo.gif' class='controlsDisabled' onclick="workspace.history.redo()" alt='redo icon' />
        </div>
        <div id='filters'>
            <input style='width: 135px; padding: 1px 2px 1px 2px;' id='textfilter' onchange='workspace.filter(this.value)' onkeydown='if(13==event.keyCode){workspace.filter(this.value);}; event.cancelBubble=true;'/>
            <!-- this button is strictly for looks -->
            <input style='width: 50px;' type='button' value='filter' />
        </div>
        <div id='mini'>
        </div>
        <div id='links'>
          <a id='rsslink' href='""" + wsname + """.xml'><img style='margin: 6px 2px;border:0;width:19px;height:9px;' src='images/minixml.gif' /></a>
        </div>
        <div id='wsname'>
        </div>
    </div>
    <div id='db'></div>
  </div>
</body>
</html>""")

except Exception as e:
    import traceback
    print("Content-type: text/html\n")
    print("""<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Internal Server Error</h1>
    <p>""" + str(e) + """</p>
    <pre>""" + traceback.format_exc() + """</pre>
</body>
</html>""")
