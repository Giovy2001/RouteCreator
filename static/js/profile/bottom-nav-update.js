function update_bottom_nav() {
  const saved = localStorage.getItem("chalk_and_track_username");
  const nav_item = document.getElementById("create-button-hidden");

  if (saved) {
    nav_item.style.display = "flex";
  } else {
    nav_item.style.display = "none";
  }
}

document.addEventListener("DOMContentLoaded", update_bottom_nav);