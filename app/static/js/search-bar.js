let inputSearch = document.getElementById("search-input");
let iconSearch = document.getElementById("search-icon");
let matchSearch = document.getElementById("search-list");

let populateMatchList = (matchList) => {
    // delete previous childs
    while (matchSearch.firstChild) {
      matchSearch.removeChild(matchSearch.firstChild);
    }
  
    for (confTitle of matchList) {
      let option = document.createElement("a");
      option.href = `${window.origin}/comentarios/${confTitle["nombre"]}`;
      option.innerText = confTitle["nombre"] + "   |   " + confTitle["email"] + "   |   " + confTitle["comuna"] + "   |   " ;
      matchSearch.append(option);
    }
    matchSearch.hidden = false;
  };


let fetchAJAX = (url) => {
    fetch(url, {
        mode: "cors",
        credentials: "include",
    }) // 1 acceder al url
        .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json(); // 2 parseamos el response a un json
        })
        .then((ajaxResponse) => {
        populateMatchList(ajaxResponse["data"]); // 3 le pasamos el data a populate...()
        console.log(ajaxResponse);
        })
        .catch((error) => {
        console.error(
            "There has been a problem with your fetch operation:",
            error
        );
        });
};

let handleAJAX = (event) => {
    if (event.target.value.length < 3) {
        matchSearch.hidden = true;
        return;
    }
    let url = `${window.origin}/get-people/${event.target.value}`;
    fetchAJAX(url);
};

inputSearch.addEventListener("input", handleAJAX);
