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
    updateHoldStyle(hold, data);
    hold.dataset.id = data.id;
    holdContainer.appendChild(hold);
})

function updateHoldStyle(hold, data) {
    hold.style.left = `${data.x * 100}%`;
    hold.style.top = `${data.y * 100}%`;
    hold.style.transform = `translate(-50%,-50%) scale(${data.scale})`;

    hold.classList.remove("start", "middle", "top");

    hold.classList.add(data.type);
}