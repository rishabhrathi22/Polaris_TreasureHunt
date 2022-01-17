// Get the modal
var modal = document.getElementById("rulesModal");
// Get the button that opens the modal
var btn = document.getElementById("myBtn");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[1];
// When the user clicks the button, open the modal
btn.onclick = function () {
  modal.style.display = "block";
};
// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
};

var modal2 = document.getElementById("leaderboardModal");
var btn2 = document.getElementById("myBtn2");
var span2 = document.getElementsByClassName("close")[0];
btn2.onclick = function () {
  // get data from backend
  var table = document.getElementById("leaderboardTable");

  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    const data = JSON.parse(this.responseText);

    for (const user in data) {
      table.innerHTML +=
        "<tr><td>" +
        data[user]["user"] +
        "</td><td>" +
        data[user]["ques_solved"] +
        "</td><td>" +
        data[user]["score"] +
        "</td><td>" +
        data[user]["hints_taken"] +
        "</td></tr>";
    }
  };

  xhttp.open("GET", "leaderboard?t=" + Math.random());
  xhttp.send();

  // open modal
  modal2.style.display = "block";
};
span2.onclick = function () {
  modal2.style.display = "none";
  document.getElementById("leaderboardTable").innerHTML = "";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (e) {
  if (e.target == modal) {
    modal.style.display = "none";
  } else if (e.target == modal2) {
    modal2.style.display = "none";
    document.getElementById("leaderboardTable").innerHTML = "";
  }
};
