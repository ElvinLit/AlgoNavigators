function startNewConversation() {
    fetch("/delete-conversation", {
        method: "POST",
        body: JSON.stringify({}),
    }).then((_res) => {
        window.location.href = "/chat";
    });
  }