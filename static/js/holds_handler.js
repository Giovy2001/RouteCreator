function createHold(data) {
    let holdContainer = document.getElementById("holdContainer")

    let hold = document.createElement("div");
    hold.classList.add("hold");
    hold.dataset.id = data.id;
    holdContainer.appendChild(hold);

    let use = document.createElement("label");
    use.classList.add("use");
    hold.appendChild(use);
    
    updateHoldStyle(hold, data);
    updateUseStyle(hold, data);

    return hold
}

function updateHoldStyle(hold, data) {
    hold.style.left = `${data.x * 100}%`;
    hold.style.top = `${data.y * 100}%`;

    hold.style.width = `${24 * data.scale}px`;
    hold.style.height = `${24 * data.scale}px`;

    hold.classList.remove("start", "middle", "top");

    hold.classList.add(data.type);
}

function updateUseStyle(hold, data) {
    let use = hold.querySelector(".use");
    let use_text = (data.use === "hand") ? "M" : (data.use === "foot") ? "P" : "";
    use.textContent = use_text;
    use.style.left = `${24 * data.scale + 2}px`;
    use.style.top = `${12 * data.scale}px`;
}