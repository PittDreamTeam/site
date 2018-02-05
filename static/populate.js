
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
  httpRequest.onreadystatechange = function() { populateCategories(httpRequest) };
  httpRequest.open("GET", "/cats");
  httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  httpRequest.send();
}

function populateCategories(httpRequest){
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

function loadCategory(row){
  var table = document.getElementById("categories");
  var newRow  = table.insertRow();
  name = row['name'];
  newRow.id = name
  var newCell, newText;
  for (var key in row) {
    newCell  = newRow.insertCell();
    newCell.id = name + "-" + key;
    newText  = document.createTextNode(row[key]);
    newCell.appendChild(newText);
  }
  var cells = document.getElementById(name).cells;
  var remaining, budget;
  for(var i = 0; i < cells.length; i++) {
    if(cells[i].id===name+"-"+"remaining"){
      remaining = cells[i].innerHTML;
    }
  }

  newCell  = newRow.insertCell();
  newCell.id = name + "-" + "overbudget";
  if(remaining>=0){
    newText = document.createTextNode("No");
  } else {
    newText = document.createTextNode("Yes");
  }
  newCell.appendChild(newText);


  deletecell = newRow.insertCell();
  button = document.createElement('button');
  button.innerHTML = "Delete";
  button.addEventListener("click", function(){
    name = row['name'];
    deleteCategory(name);
  });
  deletecell.appendChild(button);
  var combobox = document.getElementById('purcat');
  var opt = document.createElement("option");
  opt.id = "opt"+name;
  opt.innerHTML = name;
  combobox.appendChild(opt);
}

function deleteCategory(name){
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
  }}

function getPurchases(){
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
