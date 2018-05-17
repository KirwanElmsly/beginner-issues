
document.getElementById("search").onclick = function() {
    language = document.getElementById("language").value;
    labels = document.getElementById("labels").value.replace(/\s/g, '+');
    url = "http://localhost:5000/search/" + language + "/" + labels;
    console.log(url);
    location.replace(url);
};
