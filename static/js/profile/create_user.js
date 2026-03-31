function loadUsername() {
    const username_input = document.getElementById("usernameInput");
    const local_user_name = localStorage.getItem("chalk_and_track_username");


    if (username_edited) {
        username_input.value = username_edited;
    } else if (local_user_name) {
        username_input.value = local_user_name;
    }
}

document.addEventListener("DOMContentLoaded", loadUsername);