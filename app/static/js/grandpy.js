let chatELT = document.getElementsByClassName("chat")[0]

function addResponseToChat(text, className) {
    let paraELT = document.createElement("p")
    paraELT.className= className
    paraELT.innerHTML = text
    chatELT.appendChild(paraELT)

}

let formELT = document.getElementsByTagName("form")[0];

formELT.addEventListener("submit", function(e) {
    let inputValue = formELT.elements[0].value
    e.preventDefault();
    addResponseToChat(inputValue.replace("\n", "<br>"), "user")
    ajaxPost("/test", inputValue , function (rep) {
        console.log(typeof rep.toString(2))
        let image_resp = document.createElement("img")
        image_resp.src = "data:image/png;base16" + rep
        chatELT.appendChild(image_resp)
        addResponseToChat(rep.replace("\n", "<br>"), "robot")
    })
    formELT.elements[0].value = ""
})


