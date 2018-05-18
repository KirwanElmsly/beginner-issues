
var myWorker = new Worker('/static/worker.js');
var globalresult;

var resultTemplate = '<div class="results">\
    <div class="container">\
        <div class="row row-eq-height" id="result-row">\
        </div>\
    </div>\
</div>'

var issueTemplate =

document.getElementById("search").onclick = function() {
    console.log("Working");
    var language = document.getElementById("language").value;
    var labels = document.getElementById("labels").value.replace(/\s/g, '+');
    var url = "http://localhost:5000/search/" + language + "/" + labels;
    myWorker.postMessage(url);
    console.log("Posted " + url + " to worker");
};

myWorker.onmessage = function(e) {
    result = JSON.parse(e.data);
    document.getElementById('content')
        .insertAdjacentHTML('afterend', resultTemplate);
    globalresult = result

    for (var i = 0; i < result["items"].length; i++) {
        document.getElementById('result-row').insertAdjacentHTML('beforeend', '\
            <div class="issue-box col-12 col-sm-6 col-md-4 col-lg-3">\
                <div class="issue">\
                    <div class="issue-info">\
                        <div class="issue-title">\
                            <a href="' + result["items"][i]["html_url"] + '">' + result["items"][i]["title"] + '</a>\
                        </div>\
                        <div class="subtitle">\
                            <a href="' + result["items"][i]["repository_url"] +  '" target="_blank">\
                            ' + result["items"][i]["name"] + '</a> - \
                            ' + result["items"][i]['time_alive'] + ' old\
                        </div>\
                    </div>\
                        <div id="labels-issue' + i + '" class="labels">\
                        </div>\
                </div>\
            </div>'
        );

        for (var j = 0; j < result["items"][i]['labels'].length; j++) {
            document.getElementById('labels-issue' + i).insertAdjacentHTML('beforeend', '\
                <div class="label badge badge-pill badge-secondary">\
                    ' + result["items"][i]["labels"][j]["name"] + '\
                </div>'
            );
        }
    }
};
