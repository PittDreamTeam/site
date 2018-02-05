

function setup() {
  document.getElementById("addcat").addEventListener("click", newCategory, true);
  document.getElementById("addpurchase").addEventListener("click", newPurchase, true);
}

function newPurchase() {
  var httpRequest = new XMLHttpRequest();
  if (!httpRequest) {
    alert('Cannot create an XMLHTTP instance');
    return false;
  }
  var purname = document.getElementById('purname').value;
  var puramount = document.getElementById('puramount').value;
  var purcategory = document.getElementById('purcat').value;
  var purchase = { 'purname':purname, 'puramount':puramount, 'purcategory':purcategory };
  var json = JSON.stringify(purchase);

  httpRequest.onreadystatechange = function() { addPurchase(httpRequest) };
  httpRequest.open("POST", "/purchases");
  httpRequest.setRequestHeader('Content-Type', 'application/JSON');
  httpRequest.send(json);
  document.getElementById('purname').value = "";
  document.getElementById('puramount').value = "";
  document.getElementById('purcat').value = "";

}
function addPurchase(httpRequest){
  if (httpRequest.readyState === XMLHttpRequest.DONE) {
    if (httpRequest.status === 200) {
      console.log("[POST] Purchases: \n\n" + httpRequest.responseText);
      var json = JSON.parse(httpRequest.responseText);
      var category = json['category']
      updateCategory(category)
    } else {
      alert("There was a problem with the post request.");
    }
  }
}
function updateCategory(json){
  name = json['name'];
  remaining = document.getElementById(name+"-remaining");
  remaining.innerHTML=json['remaining'];
  budget = document.getElementById(name+"-budget");
  overbudget = document.getElementById(name+"-overbudget")
  if(remaining.innerHTML>=0){
    overbudget.innerHTML = "No";
  } else {
    overbudget.innerHTML = "Yes";
  }
}

function newCategory() {
	var httpRequest = new XMLHttpRequest();
	if (!httpRequest) {
		alert('Cannot create an XMLHTTP instance');
		return false;
	}
	var category = document.getElementById('catname').value;
	var budget = document.getElementById('catbudget').value;
	var cat = { 'catname':category, 'catbudget':budget };
	var json = JSON.stringify(cat);

	httpRequest.onreadystatechange = function() { addCategory(httpRequest) };
	httpRequest.open("POST", "/cats");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	httpRequest.send(json);
	document.getElementById('catname').value = "";
	document.getElementById('catbudget').value = "";

}

function addCategory(httpRequest){
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
      console.log("[POST] Categories: \n\n " + httpRequest.responseText);
			var jsonResponse = JSON.parse(httpRequest.responseText);
			loadCategory(jsonResponse);
		} else if(httpRequest.status === 409) {
      alert("Category already exists.")
    } else {
			alert("There was a problem with the post request.");
		}
	}
}

window.addEventListener("load", setup, true);
