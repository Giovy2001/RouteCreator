function getHighestGrade(routes) {
    const grades_map = ["8C+", "8C", "8B+", "8B", "8A+", "8A", "7C+", "7C", "7B+", "7B", "7A+", "7A", "6C+", "6C", "6B+", "6B", "6A+", "6A", "5C+", "5C", "5B+", "5B", "5A+", "5A", "4C+", "4C", "4B+", "4B", "4A+", "4A"]
    let bestGrade = null;
    let bestIndex = Infinity;

    for (const route of routes) {
        const grade = route.route_grade;
        const index = grades_map.indexOf(grade);

        if (index !== -1 && index < bestIndex) {
            bestIndex = index;
            bestGrade = grade;
        }
    }

    return bestGrade;
}

function set_profile_data(user) {
    const profile_tag = document.getElementById("profile-tag");
    const profile_score = document.getElementById("profile-score");
    
    /* Colore */
    setColor(parseInt(user["user_color"]))
    
    /* Punti */
    profile_score.innerHTML = user["points"]
    
    /* Tag */
    for (const [key, value] of Object.entries({
        "PRO" : 5000,
        "EXP" : 2500,
        "ADV" : 1000,
        "INT" : 500,
        "BEG" : 200,
        "NEW" : 0
    })) {
        if (user["points"] >= value) {
            profile_tag.innerHTML = key
            break
        }
    }
}

function set_routes_data(routes) {
    const stat_created_n = document.getElementById("stat-created-n");
    const stat_created_hardest = document.getElementById("stat-created-hardest");

    
    let total_stats = 2
    let hidden_stats = 0


    /* Stat */
    if (routes.length == 0) {
        let cellGrid = stat_created_n.closest(".cell-grid");
        cellGrid.style.display = "none";
        hidden_stats += 1;
    } else {
        stat_created_n.innerHTML = routes.length
    }

    let grade = getHighestGrade(routes)
    if (!grade) {
        let cellGrid = stat_created_hardest.closest(".cell-grid");
        cellGrid.style.display = "none";
        hidden_stats += 1;
    } else {
        stat_created_hardest.innerHTML = grade;
    }


    /* Stat container */
    if (hidden_stats == total_stats) {
        let stat_grid = stat_created_n.closest(".stat-grid");
        stat_grid.style.display = "none";
    }
}


function request_profile_data(username) {
    fetch("/backend_get_profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
    })      
            .then(response => response.json())
            .then(data => {
                console.log(data);
                set_profile_data(data["user"])
                set_routes_data(data["routes"])
            })
            .catch(err => console.error(err));
}