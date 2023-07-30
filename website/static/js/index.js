function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  function deleteAllNotes() {
    fetch("/delete-all-notes", {
      method: "POST",
      body: JSON.stringify({}), // Since we are not specifying a specific noteId for all notes, we can just send an empty object as the body
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  