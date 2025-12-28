const text = "Initializing Protocol...";

function changeText() {
    const button = document.getElementById("submitBtn");
    button.innerText = text;
    button.classList.add("disabled");
    }

function scroll(){
    const card = document.getElementById("main-card")
    if(card){
        card.scrollIntoView({behavior : 'smooth'})
    }
}

window.onload = scroll;