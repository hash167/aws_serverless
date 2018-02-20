var form = document.getElementById("textform");
var thankyou = document.getElementById('thankyou');
var calls = document.getElementById('calls');
var errorblock = document.getElementById('error');

form.onsubmit = function (e) {
  // stop the regular form submission
  e.preventDefault();

  // collect the form data while iterating over the inputs
  var data = {};
  for (var i = 0, ii = form.length; i < ii; ++i) {
    var input = form[i];
    if (input.name) {
      data[input.name] = input.value;
    }
  }



  if (data['text'] == "" || data['email'] == "") {
    alert("Please enter all the fields");
  } else {
    // construct an HTTP request
    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.setRequestHeader('Authorization', data['g-recaptcha-response'])

    // send the collected data as JSON
    console.log(data)
    xhr.send(JSON.stringify(data));

    xhr.onerror = function () {
      console.log(this);
      form.style.display = "none";
      errorblock.style.display = "block";
    };

    xhr.onload = function () {
      form.style.display = "none";
      thankyou.style.display = "block";
      var html = ""
      var hash = JSON.parse(this.responseText);
      console.log(hash);
      //document.getElementById("calls").innerHTML = JSON.stringify(this.responseText);
      // EXTRACT VALUE FOR HTML HEADER.
      // ('Book ID', 'Book Name', 'Category' and 'Price')
      var row = [];
      Object.keys(hash).forEach(function (key) {
        row.push(hash[key]);
      })

//      // CREATE DYNAMIC TABLE.
      var table = document.createElement("table");
//      // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.
//
      var tr = table.insertRow(-1);                   // TABLE ROW.
//

      var th = document.createElement("th");      // TABLE HEADER.
      th.innerHTML = "";
      tr.appendChild(th);
      Object.keys(row[0]).forEach(function (key) {
        var th = document.createElement("th");      // TABLE HEADER.
          if(key != 'id'){
            th.innerHTML = key;
            tr.appendChild(th);
          }

      })

      for (var i = 0; i < row.length; i++) {

            tr = table.insertRow(-1);

            Object.keys(row[i]).forEach(function (key) {
                var tabCell = tr.insertCell(-1);
                if(key != 'id'){
                    tabCell.innerHTML = row[i][key];
                   }

    // iteration code
            })


       }

       var divContainer = document.getElementById("calls");
       divContainer.innerHTML = "";
       divContainer.appendChild(table);


    };
  }
};

function enableBtn(){
  var btnSendText = document.getElementById("btnSendText");

  btnSendText.disabled = false;
  btnSendText.style.color="white";
  btnSendText.style.background="#1e7f58";
}