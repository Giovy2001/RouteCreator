let holdContainer = document.getElementById("holdContainer")

holds.forEach(h => {
    let data = {
        id: h.id,
        x: h.x,
        y: h.y,
        scale: h.r,
        type: h.type,
        use: h.use
    };

    let hold = document.createElement("div");
    hold.classList.add("hold");
    hold.dataset.id = data.id;
    holdContainer.appendChild(hold);
    
    let use_text = (data.use === "hand") ? "M" : (data.use === "foot") ? "P" : "";

    if (use_text != "") {
        let use = document.createElement("label");
        use.textContent = use_text
        use.classList.add("use");
        hold.appendChild(use);
        use.style.left = `${24 * data.scale + 2}px`;
        use.style.top = `${12 * data.scale}px`;
    }

    updateHoldStyle(hold, data);
})

function updateHoldStyle(hold, data) {
    hold.style.left = `${data.x * 100}%`;
    hold.style.top = `${data.y * 100}%`;

    hold.style.width = `${24 * data.scale}px`;
    hold.style.height = `${24 * data.scale}px`;

    

    hold.classList.remove("start", "middle", "top");

    hold.classList.add(data.type);
}