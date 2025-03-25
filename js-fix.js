// Fix note positions after page load
window.addEventListener('load', function() {
  // Wait a moment for all notes to initialize
  setTimeout(function() {
    // Find all note elements
    var noteElements = document.querySelectorAll('div.note');
    
    // Get note data from database
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'get-note-positions.py?workspace=' + encodeURIComponent(workspace.name), true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var noteData = JSON.parse(xhr.responseText);
        
        // Apply positions from database
        for (var i = 0; i < noteData.length; i++) {
          var note = noteData[i];
          var noteObject = workspace.notes[note.noteid];
          
          if (noteObject && noteObject.div) {
            // Set positions
            noteObject.div.style.left = note.xposition + 'px';
            noteObject.div.style.top = note.yposition + 'px';
            noteObject.xposition = note.xposition;
            noteObject.yposition = note.yposition;
          }
        }
      }
    };
    xhr.send();
  }, 500);
});
