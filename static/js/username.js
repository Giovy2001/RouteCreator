function saveUsername() {
  const username = document.getElementById("usernameInput").value;
  localStorage.setItem("boulderUsername", username);
}

function loadUsername() {
  const saved = localStorage.getItem("boulderUsername");

  if (saved) {
    document.getElementById("usernameInput").value = saved;
  }
}

document.addEventListener("DOMContentLoaded", loadUsername);