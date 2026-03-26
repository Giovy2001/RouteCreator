function saveUsername() {
  const username = document.getElementById("usernameInput").value;
  localStorage.setItem("chalk_and_track_username", username);

  /* remove old local storage entry */
  localStorage.removeItem("boulderUsername")
}

function loadUsername() {
  const saved = localStorage.getItem("chalk_and_track_username");

  if (saved) {
    document.getElementById("usernameInput").value = saved;
  }
}

document.addEventListener("DOMContentLoaded", loadUsername);