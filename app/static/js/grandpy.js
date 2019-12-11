let chatELT = document.getElementsByClassName("chat")[0];

let platform = new H.service.Platform({
    'apikey': 's-GCuUP2fbtkdhIHysMqbFTtnZ4EGa3a09Bj7OWDhc8'
  });

let defaultLayers = platform.createDefaultLayers();

function addResponseToChat(text, className) {
    let paraELT = document.createElement("p")
    paraELT.className= className
    paraELT.innerHTML = text
    chatELT.appendChild(paraELT)
    paraELT.scrollIntoView({behavior : "smooth"})

}
function addImageApiToChat(latitude, longitude) {
    let divElt = document.createElement("div")
    divElt.className = "robotImage"
    chatELT.appendChild(divElt)
    let map = new H.Map(
        divElt,
        defaultLayers.vector.normal.map,
        {
          zoom: 16,
          center: { lat: longitude, lng: latitude}
        });
    window.addEventListener('resize', () => map.getViewPort().resize());
    let Marker = new H.map.Marker({lat:longitude, lng:latitude});
    map.addObject(Marker);
    divElt.scrollIntoView({behavior : "smooth"})
}

let formELT = document.getElementsByTagName("form")[0];

formELT.addEventListener("submit", function(e) {
    let inputValue = formELT.elements[0].value
    e.preventDefault();
    addResponseToChat(inputValue.replace("\n", "<br>"), "user")
    ajaxPost("/answer", inputValue , function (rep) {
        console.log(rep)
        console.log(typeof rep.api_infos)
        if (rep.parsed === true) {
            if (rep.api_infos.status === true) {
                addResponseToChat("Ah ! je connais ce lieu. D'ailleurs, j'ai retrouvé une carte de ses environs !", "robot")
                addImageApiToChat(rep.api_infos.latitude, rep.api_infos.longitude)
                addResponseToChat("Ce lieu me rappelle des souvenirs, j'ai une anecdote"
                                  + ` sur cet endroit et ses alentours : ${rep.api_infos.wiki.title}`, "robot")
                addResponseToChat(rep.api_infos.wiki.intro.replace("\n", "<br>"), "robot")
            }
            else {
                addResponseToChat("Oh oh, il semblerait que je n'ai pas d'histoire à te raconter à ce sujet.", "robot")
            }

        }
        else {
            addResponseToChat("Je n'ai pas compris ta question. Pourrais-tu donner des informations"+
                              " plus précises sur le lieu que tu cherches s'il te plaît ? Attention, l'orthographe compte.", "robot")
        }
        /*
        addResponseToChat(rep.sentence.replace("\n", "<br>"), "robot")
        addImageApiToChat()
        */
    })
    formELT.elements[0].value = ""
})



