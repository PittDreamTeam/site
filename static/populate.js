
function setup() {
    populatePage();
    getPurchases();
}

function populatePage() {
    var httpRequest = new XMLHttpRequest();
    if (!httpRequest) {
        alert('Cannot create an XMLHTTP instance');
        return false;
    }
    httpRequest.onreadystatechange = function() { populate(httpRequest) };
    httpRequest.open("GET", "/cats");
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    httpRequest.send();
}

function populate(httpRequest) {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
        if (httpRequest.status === 200) {
            console.log("[GET] /cats: \n\n" + httpRequest.responseText);
            var json = JSON.parse(httpRequest.responseText);
            for (var key in json) {
                loadCategory(json[key]);
            }
        } else {
            alert("There was a problem with the get request.");
        }
    }
}

function loadCategory(row) {
    var newText = document.createTextNode("HEY THERE, POSTER");
}

function deleteCategory(name) {
    var httpRequest = new XMLHttpRequest();
    if (!httpRequest) {
        alert('Cannot create an XMLHTTP instance');
        return false;
    }
    var json = JSON.stringify(name);
    httpRequest.onreadystatechange = function() { removeCategory(httpRequest, name) };
    httpRequest.open("DELETE", "/cats");
    httpRequest.setRequestHeader('Content-Type', 'application/JSON');
    httpRequest.send(json);
}

function removeCategory(httpRequest, name) {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
        if (httpRequest.status === 200) {
            console.log("[DELETE] /cats: \n\n" + httpRequest.responseText);
            document.getElementById('categories').removeChild(document.getElementById(name));
            document.getElementById('purcat').removeChild(document.getElementById("opt"+name))
        } else {
            alert("There was a problem with the delete request.");
        }
    }
}

function getPurchases() {
    var httpRequest = new XMLHttpRequest();
    if (!httpRequest) {
        alert('Cannot create an XMLHTTP instance');
        return false;
    }
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                console.log("[GET] /purchases: \n\n" + httpRequest.responseText);
            }
        }
    };
    httpRequest.open("GET", "/purchases");
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    httpRequest.send();
}

window.addEventListener("load", setup, true);
