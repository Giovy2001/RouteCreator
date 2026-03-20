const currentUser = localStorage.getItem('boulderUsername');
const authorButtons = document.getElementById("authorButtons");

if (currentUser == routeAuthour) {
    authorButtons.style.display = "block";
}