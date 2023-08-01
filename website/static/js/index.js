function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/chat";
    });
  }

function startNewConversation() {
    fetch("/delete-all-notes", {
        method: "POST",
        body: JSON.stringify({}),
    }).then((_res) => {
        window.location.href = "/chat";
    });
  }