// datatime.js

function displayDateTime() {
    const element = document.getElementById("datetime");
    const dataTime = new Date().toLocaleString();
    element.innerText = dataTime.replace(", ", " - ");
}

displayDateTime();
setInterval(displayDateTime, 1000);
