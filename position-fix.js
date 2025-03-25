// Get all notes from database
var notesData = {
  "apples": [
    // Hardcoded positioning data for the "apples" workspace
    {noteid: "note0", xposition: 170, yposition: 40},
    {noteid: "note1", xposition: 344, yposition: 663},
    {noteid: "note2", xposition: 1372, yposition: 180}
  ]
};

// Function to apply positions
function fixNotePositions() {
  // Get current workspace name
  var workspaceName = workspace.name;
  
  // Check if we have position data for this workspace
  if (notesData[workspaceName]) {
    var positions = notesData[workspaceName];
    
    // Apply positions to each note
    for (var i = 0; i < positions.length; i++) {
      var pos = positions[i];
      var note = workspace.notes[pos.noteid];
      
      if (note && note.div) {
        // Apply position
        note.div.style.left = pos.xposition + 'px';
        note.div.style.top = pos.yposition + 'px';
        note.xposition = pos.xposition;
        note.yposition = pos.yposition;
      }
    }
  }
}

// Run after page load
if (window.addEventListener) {
  window.addEventListener('load', function() {
    // Wait a short time to ensure all notes are created
    setTimeout(fixNotePositions, 500);
  });
}
