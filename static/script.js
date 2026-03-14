const canvas = document.getElementById("canvas")
const ctx = canvas.getContext("2d")

let holds = []
let img = new Image()

document.getElementById("imageInput").onchange = function(e){

    const file = e.target.files[0]
    const url = URL.createObjectURL(file)

    img.src = url

    img.onload = function(){
        canvas.width = img.width
        canvas.height = img.height
        ctx.drawImage(img,0,0)
    }

}

canvas.addEventListener("click", function(e){

    const rect = canvas.getBoundingClientRect()

    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    holds.push({x:x, y:y, r:20})

    draw()

})

function draw(){

    ctx.clearRect(0,0,canvas.width,canvas.height)
    ctx.drawImage(img,0,0)

    ctx.strokeStyle = "red"
    ctx.lineWidth = 3

    holds.forEach(h => {

        ctx.beginPath()
        ctx.arc(h.x,h.y,h.r,0,Math.PI*2)
        ctx.stroke()

    })

    document.getElementById("holdsInput").value =
        JSON.stringify(holds)

}