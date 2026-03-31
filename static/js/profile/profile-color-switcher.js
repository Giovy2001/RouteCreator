const palette = [
  get_palette_color(1), get_palette_color(2), get_palette_color(3),
  get_palette_color(4), get_palette_color(5), get_palette_color(6),
  get_palette_color(7), get_palette_color(8)
]

function get_palette_color(user_color_id) {
  return getComputedStyle(document.documentElement).getPropertyValue(`--user-color-${user_color_id}`);
}

function rgb_to_hex(rgb) {
  const match = rgb.match(/\d+/g);
  if (!match) return null;
  return "#" + match
    .slice(0, 3)
    .map(num => {
      const hex = parseInt(num, 10).toString(16);
      return hex.padStart(2, "0");
    })
    .join("")
    .toUpperCase();
}

function switch_profile_color() {
  let profile_color_active = document.getElementById("profile-color-active");
  let profile_image = document.getElementById("profile-image");

  let current_color = rgb_to_hex(window.getComputedStyle(profile_color_active).getPropertyValue("background-color"));

  let new_value = palette.indexOf(current_color) + 1;
  if (palette.length == new_value) {
    new_value = 0
  }

  profile_color_active.style.backgroundColor = palette[new_value];
  profile_image.src = `/static/icons/profile/Icon_${new_value}.png`

  update_website_icon(new_value)

  // Chiamata all'endpoint per aggiornare il database
  const username = localStorage.getItem("chalk_and_track_username");
  if (username) {
    fetch("/backend_update_color", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({username: username, color_id: new_value})
    })
    .then(response => response.json())
    .then(data => {
      if (!data.success) console.error("Errore aggiornamento colore:", data.message);
    })
    .catch(err => console.error("Fetch error:", err));
  }

  localStorage.setItem("chalk_and_track_color", new_value);
}

function loadColor() {
  const saved = localStorage.getItem("chalk_and_track_color");
  let profile_color_active = document.getElementById("profile-color-active");
  let profile_image = document.getElementById("profile-image");

  if (saved) {
    profile_color_active.style.backgroundColor = palette[saved];
    profile_image.src = `/static/icons/profile/Icon_${saved}.png`
    update_website_icon(saved)
  } else {
    profile_image.src = `/static/icons/profile/Icon_${0}.png`
    update_website_icon(0)
  }
}

document.addEventListener("DOMContentLoaded", loadColor);