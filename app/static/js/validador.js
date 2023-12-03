const validateRegion = (region) => {
    if (!region) return false;
    
    return true;
};

const validateComuna = (comuna) => {
    if (!comuna) return false;
    return true;
};

const validateTipoArtesania = (tipoArtesania) => {

    if (!tipoArtesania) return false;
    select = document.getElementById('tipo_artesania');
    if (select.options.length > 3) return false;
    return true;
};

const validateDescArtesania = (descArtesania) => {
    return true;
};

const validateFotoArtesania = (fotoArtesania) => {
    if (!fotoArtesania) return false;

    let largo = fotoArtesania.length;
    let largotrue = (1 >= largo <= 3);

    // file type validation
    let typeValid = true;

    for (const file of fotoArtesania) {
        // file.type should be "image/<foo>" or "application/pdf"
        let fileFamily = file.type.split("/")[0];
        typeValid &&= fileFamily == "image";
    }

    return typeValid && largotrue;

};

const validateNombre = (nombre) => {
    if (!nombre) return false;
    return  (nombre.length >= 3) && (nombre.length <= 80);
};

const validateEmail = (email) => {
    if (!email) return false;
    let emailLength = email.length <= 30;
    let re = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
    let formatValid = re.test(email);
    return formatValid && emailLength;
};

const validateTelefono = (telefono) => {
    // Si no hay nada, retorno true, porque es opcional
    if (!telefono) return true;
    let telefonoLength = telefono.length <= 15;
    let re = /^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$/;
    let formatValid = re.test(telefono);
    return formatValid && telefonoLength;
};


// const validateForm = (nameForm, id1, id2,id3, id4, id5, id6, id7, id8) => {
//     // get elements from DOM by using form's name.
//     let form =  document.getElementById(nameForm);
//     let sel1 = document.getElementById(id1).value;
//     let sel2 = document.getElementById(id2).value;
//     let sel3 = document.getElementById(id3).value;
//     let sel4 = document.getElementById(id4).value;
//     let sel5 = document.getElementById(id5).value;
//     let sel6 = document.getElementById(id6).value;
//     let sel7 = document.getElementById(id7).value;
//     let sel8 = document.getElementById(id8).value;

//     // validation auxiliary variables anfunction.
//     let isValid = true;
//     let invalidInputs = [];
//     const setInvalidInput = (inputName) => {
//         invalidInputs.push(inputName);
//         isValid &&= false;
//     }; 

//     //Validation 
//     if (form === 'form_hincha') {
//         if (!validateSports(sel1)) setInvalidInput(id1);
//         if (!validateRegion(sel2)) setInvalidInput(id2);
//         if (!validateComuna(sel3)) setInvalidInput(id3);
//         if (!validateTransporte(sel4)) setInvalidInput(id4);
//         if (!validateNombre(sel5)) setInvalidInput(id5);
//         if (!validateEmail(sel6)) setInvalidInput(id6);
//         if (!validateTelefono(sel7)) setInvalidInput(id7);
//         if (!validateComentarios(sel8)) setInvalidInput(id8);
//     } 
//     else if (form === 'form_artesano')
//     {
//         if (!validateRegion(sel1)) setInvalidInput(id1);
//         if (!validateComuna(sel2)) setInvalidInput(id2);
//         if (!validateTipoArtesania(sel3)) setInvalidInput(id3);
//         //if (!validateDescArtesania(sel4)) setInvalidInput(id4);
//         //if (!validateFotoArtesania(form['foto_artesania'].files)) setInvalidInput(id5);
//         //if (!validateNombre(sel6)) setInvalidInput(id6);
//         //if (!validateEmail(sel7)) setInvalidInput(id7);
//         //if (!validateTelefono(sel8)) setInvalidInput(id8);
//     }

//     // finally display validation
//     let validationBox = document.getElementById("val-box");
//     let validationMessageElem = document.getElementById("val-msg");
//     let validationListElem = document.getElementById("val-list");

//     if (!isValid) {
//         validationListElem.textContent = "";
//         // add invalid elements to val-list element.
//         for (input of invalidInputs) {
//           let listElement = document.createElement("li");
//           listElement.innerText = input;
//           validationListElem.append(listElement);
//         }
//         // set val-msg
//         validationMessageElem.innerText = "Los siguiente campos son invalidos:";
    
//         // make validtion prompt visible
//         validationBox.hidden = false;
//     } else {
//         form.submit();   
//     }
// };


// //let submitArtesano = document.getElementById("submit-btn-artesano");
// //submitArtesano.addEventListener("click", () => {validateForm('form_artesano',  'region_artesano', 'comuna_artesano', 'tipo_artesania', 'desc_artesania', 'foto_artesania', 'nombre_artesano', 'email_artesano', 'celular_artesano')});


let submitArtesano = document.getElementById("submit-btn-artesano");
let form_art =  document.getElementById('form_artesano');
if (form_art){
    submitArtesano.addEventListener("click", () => {form_art.submit()});
}

let submitHincha = document.getElementById("submit-btn-hincha");
let form_hin =  document.getElementById('form_hincha');
if (form_hin){
    submitHincha.addEventListener("click", () => {form_hin.submit()});
}

