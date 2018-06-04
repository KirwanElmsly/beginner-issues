
function strip_punct(str) {
    return str.replace(/[.,\/#!$%\^&\*;:{}=`~()]/g," ");
}

// When search button is clicked, redirect to page with results
document.getElementById("search").onclick = function() {
    if (document.getElementById("language").value == "") {
        alert("Enter a language")
    }
    else if (document.getElementById("labels").value == "") {
        alert("Enter some labels")
    }
    else {
        var language = strip_punct(document.getElementById("language").value);
        var labels = strip_punct(document.getElementById("labels").value).replace(/\s+/g, '+');
        var url = "http://localhost:5000/search/" + language + "/" + labels;
        window.location = url;
    }
};
