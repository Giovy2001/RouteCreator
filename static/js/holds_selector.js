// --- Gestione prese ---

// save holds
const holds_label = document.getElementById('jsonHoldsHidden');
const saveButton = document.getElementById('save_route');
saveButton.addEventListener('click', (e) => {
    holds_label.value = JSON.stringify(holds)
});


const holdContainer = document.getElementById("holdContainer");
const holdTypeSelect = document.getElementById("hold_type_select");
const holdUseSelect = document.getElementById("hold_use_select");
const holdSize = document.getElementById("hold_size");
const deleteBtn = document.getElementById("delete_hold");

let holds = [];
let selectedHold = null;
let holdId = 0;


holdContainer.addEventListener("pointerdown", (e)=>{

    // se clicco su una presa gestisce lei l'evento
    if(e.target.classList.contains("hold")) return;

    // se esiste una presa selezionata → deseleziona
    if(selectedHold){
        deselectHold();
        return;
    }

    // altrimenti crea una nuova presa
    const rect = holdContainer.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;

    const data = {
        hold_id: holdId++,
        x: x, y: y,
        size: parseFloat(holdSize.value),
        progression_id: holdTypeSelect.value,
        constraint_id: holdUseSelect.value
    };

    let hold = createHold(data)
    holds.push({element:hold,data:data});
    addHoldEvents(hold);
});

function addHoldEvents(hold){
    hold.addEventListener("pointerdown",(e)=>{
        e.stopPropagation();
        selectHold(hold);
        startDrag(e,hold);
    });
}

function selectHold(hold){
    document.querySelectorAll(".hold").forEach(h=>h.classList.remove("selected"));

    hold.classList.add("selected");
    selectedHold=hold;

    const obj=holds.find(h=>h.element===hold);

    deleteBtn.style.display = "block";  

    holdTypeSelect.value=obj.data.progression_id;
    holdUseSelect.value=obj.data.constraint_id;
    holdSize.value=obj.data.size;
}

function deselectHold(){
    document.querySelectorAll(".hold").forEach(h=>h.classList.remove("selected"));
    selectedHold=null;
    deleteBtn.style.display = "none";
}

function startDrag(e,hold){
    const rect=holdContainer.getBoundingClientRect();
    hold.setPointerCapture(e.pointerId);
    function move(ev){
        let x=(ev.clientX-rect.left)/rect.width;
        let y=(ev.clientY-rect.top)/rect.height;

        x=Math.min(Math.max(x,0),1);
        y=Math.min(Math.max(y,0),1);

        hold.style.left=`${x*100}%`;
        hold.style.top=`${y*100}%`;

        const obj=holds.find(h=>h.element===hold);

        obj.data.x=x;
        obj.data.y=y;
    }

    function up(){
        hold.removeEventListener("pointermove",move);
        hold.removeEventListener("pointerup",up);
    }

    hold.addEventListener("pointermove",move);
    hold.addEventListener("pointerup",up);
}

// CAMBIO TIPO
holdTypeSelect.addEventListener("change",()=>{
    if(!selectedHold) return;

    const obj=holds.find(h=>h.element===selectedHold);
    obj.data.progression_id=holdTypeSelect.value;
    updateHoldStyle(selectedHold, obj.data);
});

// CAMBIO USO
holdUseSelect.addEventListener("change",()=>{
    if(!selectedHold) return;

    const obj=holds.find(h=>h.element===selectedHold);
    obj.data.constraint_id=holdUseSelect.value;
    updateConstraintStyle(selectedHold, obj.data)
});

// RIDIMENSIONA
holdSize.addEventListener("input",()=>{
    if(!selectedHold) return;

    const obj=holds.find(h=>h.element===selectedHold);
    obj.data.size=holdSize.value;
    updateHoldStyle(selectedHold, obj.data);
    updateConstraintStyle(selectedHold, obj.data)
});

// ELIMINA
deleteBtn.addEventListener("click",()=>{
    if(!selectedHold) return;

    const index=holds.findIndex(h=>h.element===selectedHold);
    selectedHold.remove();
    holds.splice(index,1);
    deleteBtn.style.display = "none";
    selectedHold=null;
});

// clic fuori → deseleziona
holdContainer.addEventListener("click",(e)=>{
    if(e.target===holdContainer){
        deselectHold();
    }
});

// Carica le prese esistenti se il blocco esiste già
if ("holds_array" in previous_data) {
    previous_data["holds_array"].forEach(h => {
        let data = {
            hold_id: h.id,
            x: h.x,
            y: h.y,
            size: h.size,
            progression_id: h.progression_id,
            constraint_id: h.constraint_id
        };

        let hold = createHold(data)
        holds.push({element:hold,data:data});
        addHoldEvents(hold);
    })
}