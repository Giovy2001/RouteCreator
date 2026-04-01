function changeUsername(username_changed) {
  /* Avviato quando viene cambiato da un profilo a un altro */
  if (!username_changed) {return;}
  
  localStorage.setItem("chalk_and_track_username", username_changed);

  update_bottom_nav()
  request_profile_data(username_changed)
}

function loadUsername() {
  /* Avviato quando viene caricato il profilo all'apertura della pagina */
  const username = localStorage.getItem("chalk_and_track_username");

  if (!username) {window.location.href = `/create_user`; return;}
  
  document.getElementById("usernameInput").value = username;

  update_bottom_nav()
  request_profile_data(username)
}

function createUsername(username_created) {
  /* Avviato quando viene creato il profilo, dopo aver creato il database entry */
  if (!username_created) {return;}

  /* remove old local storage entry */
  localStorage.removeItem("boulderUsername");

  localStorage.setItem("chalk_and_track_username", username_created);
  localStorage.setItem("chalk_and_track_color", 0);

  update_bottom_nav()
  request_profile_data(username_created)
}


document.addEventListener("DOMContentLoaded", loadUsername);