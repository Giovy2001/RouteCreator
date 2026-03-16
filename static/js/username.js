function saveUsername() {
  const username = document.getElementById("usernameInput").value;
  console.log(username)
  localStorage.setItem("boulderUsername", username);
}

function loadUsername() {
  const saved = localStorage.getItem("boulderUsername");
  console.log(saved)

  if (saved) {
    document.getElementById("usernameInput").value = saved;
  }
}

document.addEventListener("DOMContentLoaded", loadUsername);