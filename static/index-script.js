
// When search button is clicked, redirect to page with results
document.getElementById("search").onclick = function() {
    var language = document.getElementById("language").value;
    var labels = document.getElementById("labels").value.replace(/\s/g, '+');
    var url = "http://localhost:5000/search/" + language + "/" + labels;
    window.location = url;
};
