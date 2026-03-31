function update_website_icon(image_id) {
    let link = document.getElementById("apple-icon");
    link.href = `/static/icons/profile/Icon_${image_id}.png?v=${image_id}`; 
}