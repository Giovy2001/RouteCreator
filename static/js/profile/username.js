function changeUsername(username_changed, username_icon) {
  if (!username_changed) {return;}
  
  window.location.href = `/profile?username=${username_changed}`;
  localStorage.setItem("chalk_and_track_username", username_changed);
  localStorage.setItem("chalk_and_track_color", parseInt(username_icon));

  update_bottom_nav()
}

function loadUsername() {
  const username = localStorage.getItem("chalk_and_track_username");

  if (username) {
    document.getElementById("usernameInput").value = username;

    /* Setta gli args dell'url per passare l'username al server */
    const params = new URLSearchParams(window.location.search);
    const currentUsername = params.get("username");
    if (currentUsername !== username) {
      window.location.href = `/profile?username=${username}`;
    }
  } else {
    /* Se non esiste il profilo redirect alla pagina di creazione */
    window.location.href = `/create_user`;
  }
}

function createUsername(username_created) {
  /* This runs only after creating the database entry */
  if (!username_created) {return;}

  /* remove old local storage entry */
  localStorage.removeItem("boulderUsername");

  localStorage.setItem("chalk_and_track_username", username_created);
  localStorage.setItem("chalk_and_track_color", 0);

  update_bottom_nav()
}


document.addEventListener("DOMContentLoaded", loadUsername);