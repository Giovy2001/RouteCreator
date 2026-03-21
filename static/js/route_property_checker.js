const currentUser = localStorage.getItem('chalk_and_track_username');
const authorButtons = document.getElementById("authorButtons");

if (currentUser == routeAuthour) {
    authorButtons.style.display = "block";
}