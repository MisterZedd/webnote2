#!/usr/bin/python3

"""An abstraction for the workspace."""

import sys, os, urllib.parse as urllib, datetime, MySQLdb
from xml.dom.minidom import *

from etc.common import *
from lib.logger import log
from lib import Db
import Note  # Keep just this one import

class Workspace:
  """An abstraction for the workspace."""
  def __init__(self):
    self.name = ''
    self.notes = []
    self.nextNoteNum = 0
    self.lasttime = '' # string
    self.newNoteText = ''
    
    # create a db connection
    self.dbh = Db.getDBH()
    self.db = self.dbh.cursor()
  
  def createUpdateWorkspace(self):
    """Create or update the workspaces table."""
    table_name = Db.getTableName(self.name, 'workspaces')
    
    # Debug log
    log("Creating/updating workspace: " + self.name + " in table " + table_name)
    
    self.db.execute("INSERT INTO " + table_name + "(wsname, nextNoteNum, time)"
                    " VALUES(%s, %s, %s)"
                    "ON DUPLICATE KEY UPDATE nextNoteNum=%s, time=%s",
                    (self.name, self.nextNoteNum, self.lasttime,
                     self.nextNoteNum, self.lasttime))
    
    self.wsid = self.dbh.insert_id()
    
    # Debug log
    log("Workspace ID: " + str(self.wsid))
  
  def commit(self):
    nowtime = datetime.datetime.now(TIMEZONE)
    # we save dates in the database localized to the current timezone
    self.lasttime = nowtime.strftime('%Y-%m-%d %H:%M:%S')
      
    self.createUpdateWorkspace()
        
    # save all the notes to wn_notes
    if len(self.notes) > 0:
      table_name = Db.getTableName(self.name, 'notes')
      sql = ('INSERT INTO %s(%s, time, wsid)'
             ' VALUES(%s, %%s, %%s)'
             % (table_name,
                ','.join(["%s" % k for k in Note.DBKEYS]),
                ','.join(['%s'] * len(Note.DBKEYS))))
      values = [n.getValues() + [self.lasttime, self.wsid] for n in self.notes]
      #log(sql)
      self.db.executemany(sql, values)

    self.dbh.commit()
    return self.lasttime
  
  def trimSaveHistory(self, num_entries):
    table_name = Db.getTableName(self.name, 'notes')
    '''Delete from wn_notes15 where wsid=29107 and time < (
       SELECT time FROM `wn_notes15` where wsid=29107 group by time ORDER BY `time` DESC limit 5, 1)'''
    self.db.execute("DELETE FROM " + table_name +
                    " WHERE wsid=%s and time <= ("
                    "   SELECT time FROM " + table_name +
                    "     WHERE wsid=%s"
                    "     GROUP BY time ORDER BY time DESC limit %s, 1)",
                    (self.wsid, self.wsid, num_entries))

  def createHTML(self):
    print("Content-type: text/html\n")
    # TODO: replace href in link rel=start
    if SHOWJSDEBUG:
      debugOn = 'true'
    else:
      debugOn = 'false'
    
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
  debugOn = """ + debugOn + """;
  workspace.setName(unescape('""" + self.name + """'));
  workspace.loadedTime = '""" + self.lasttime + """';
  adminEmail = '""" + HELPEMAIL + """';
  baseURI = '""" + BASEURL + """';
  numDates = """ + str(NUM_DATES) + """;
  init();
""")
    # create notes here
    for n in self.notes:
      n.printJavascript()
    
    # Force explicit positions for notes
    for n in self.notes:
        print("  // Force position for note " + n.noteid)
        print("  if (workspace.notes['" + n.noteid + "'] && workspace.notes['" + n.noteid + "'].div) {")
        print("    workspace.notes['" + n.noteid + "'].div.style.left = '" + str(n.xposition) + "px';")
        print("    workspace.notes['" + n.noteid + "'].div.style.top = '" + str(n.yposition) + "px';")
        print("    workspace.notes['" + n.noteid + "'].xposition = " + str(n.xposition) + ";")
        print("    workspace.notes['" + n.noteid + "'].yposition = " + str(n.yposition) + ";")
        print("  }")
    # Force correct positions for notes
    for n in self.notes:
      print("  // Override position for note " + n.noteid)
      print("  var note = workspace.notes['" + n.noteid + "'];")
      print("  if (note && note.div) {")
      print("    note.div.style.left = '" + str(n.xposition) + "px';")
      print("    note.div.style.top = '" + str(n.yposition) + "px';")
      print("    note.xposition = " + str(n.xposition) + ";")
      print("    note.yposition = " + str(n.yposition) + ";")
      print("  }")

    # set workspace information
    # this happens after the notes are made to prevent the
    # nextNoteNum from incrementing unnecessarily
    print("  workspace.nextNoteNum = " + str(self.nextNoteNum) + ";")
    # set the status to unchanged
    print("  workspace.changed = false;")

    # create a new note (for bookmarklet hack)
    if self.newNoteText:
      print("workspace.createNote({'text': '%s'});" % self.newNoteText.replace("'", "\\'"))

    print("""
}
// -->
    </script>
    <link rel="stylesheet" href="style.css" type="text/css" />""")
    print('    <link rel="alternate" type="application/rss+xml" '
           'title="%s - webnote" href="%s.xml" />'
           % (urllib.unquote(self.name).replace('&', '&amp;')
                                       .replace("'", '&apos;')
                                       .replace('"', '&quot;'),
              urllib.quote(urllib.quote(self.name))))
    print(CUSTOMHEADER)
    print("""
    <title>""" + urllib.unquote(self.name) + """</title>
<script type="text/javascript" src="position-fix.js"></script>
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
          <a id='rsslink' href="%s.xml"><img style='margin: 6px 2px;border:0;width:19px;height:9px;' src='images/minixml.gif' /></a>
        </div>
        <div id='wsname'>
        </div>
    </div>
    <div id='db'></div>
  </div>
</body>
</html>""" % (urllib.quote(urllib.quote(self.name))))

  def __del__(self):
    if hasattr(self, 'db') and self.db:
      self.db.close()

# global methods for creating Workspaces
def CreateSave():
    ret = Workspace()
    size = os.environ.get('CONTENT_LENGTH', 0)
    data = sys.stdin.read(int(size)).replace('\0', '')
    
    # Debug log
    log("Received save data: " + data[:100])
    
    # there should be something here for catching an incomplete send
    dom = parseString(data)
    wsRoot = dom.getElementsByTagName('workspace').item(0)
    
    # Explicitly log the extracted name
    wsname = wsRoot.getAttribute('name')
    log("Extracted workspace name: " + wsname)
    ret.name = wsname
    
    ret.nextNoteNum = wsRoot.getAttribute('nextNoteNum')
    
    nlNotes = wsRoot.getElementsByTagName('note')

    for i in range(nlNotes.length):
        ret.notes.append(Note.FromXML(nlNotes.item(i)))
    
    return ret

def CreateLoad():
  import cgi
  ret = Workspace()
  form = cgi.FieldStorage()
  
  # get the name, strip invalid quote characters
  ret.name = form.getfirst('name', '').replace("'", '')
  
  # make sure it's a valid request
  if not ret.name:
    return None

  # get the workspace data
  ret.db.execute("SELECT wsid, nextNoteNum,"
                 " DATE_FORMAT(time, '%%Y-%%m-%%d %%H:%%i:%%s')"
                 " FROM " + Db.getTableName(ret.name, 'workspaces') +
                 " WHERE wsname=%s", [ret.name])
  row = ret.db.fetchone()
  if row:
    ret.wsid, ret.nextNoteNum, ret.lasttime = row
    if 'time' in form:
      ret.lasttime = form['time'].value
    
    # load the notes
    table_name = Db.getTableName(ret.name, 'notes')
    sql = ("SELECT %s FROM %s"
           " WHERE wsid=%%s AND %s.time=%%s"
           % (','.join(Note.DBKEYS), table_name, table_name))
    ret.db.execute(sql, [ret.wsid, ret.lasttime])
    for row in ret.db.fetchall():
      ret.notes.append(Note.FromTuple(*row))

  
  # this is a hack for now
  # TODO: add this to the notes array
  ret.newNoteText = (form.getfirst('nn', '')
                     .replace("\n", "\\n")
                     .replace("\r", "")
                     .replace("\l", ""))
  if ret.newNoteText:
    via = form.getfirst('via', '')
    ret.newNoteText += "<br />via <a href='%s'>%s</a>" % (via, via)
  
  return ret
