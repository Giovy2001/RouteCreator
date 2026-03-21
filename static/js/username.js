function saveUsername() {
  localStorage.removeItem("boulderUsername")
  const username = document.getElementById("usernameInput").value;
  localStorage.setItem("chalk_and_track_username", username);
}

function loadUsername() {
  const saved = localStorage.getItem("chalk_and_track_username");

  if (saved) {
    document.getElementById("usernameInput").value = saved;
  }
}

document.addEventListener("DOMContentLoaded", loadUsername);