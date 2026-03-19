holds.forEach(h => {
    let data = {
        id: h.id,
        x: h.x,
        y: h.y,
        scale: h.r,
        type: h.type,
        use: h.use
    };

    createHold(data);
})