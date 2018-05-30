
var resultsWorker = new Worker('/static/getEndpointWorker.js'); // Worker to search & return results
var result;

var resultTemplate = '<div class="results">\
    <div class="container">\
        <div class="row row-eq-height" id="result-row">\
        </div>\
    </div>\
</div>'


// Sorts list of results based on arbitrary key
function sorting(js_object, key_to_sort_by) {
  function sortByKey(a, b) {
    var x = a[key_to_sort_by];
    var y = b[key_to_sort_by];
    return ((x < y) ? -1 : ((x > y) ? 1 : 0));
  };
  return js_object.sort(sortByKey);
};


// Returns either a black or white text colour based on background colour
// Takes hexadecimal colour value as input
function ideal_text_color(hex) {
    if (hex.indexOf('#') === 0) {
        hex = hex.slice(1);
    }
    //convert 3 digit hex to 6 digit
    if (hex.length === 3) {
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }

    r = parseInt(hex.slice(0, 2), 16);
    g = parseInt(hex.slice(2, 4), 16);
    b = parseInt(hex.slice(4, 6), 16);

    // Basic way to determine intensity of color
    if ((r*0.299 + g*0.587 + b*0.114) > 186) {
        return "#000000";
    } else {
        return "#FFFFFF";
    }
};


// When search button is clicked, send endpoint location to worker (off main thread)
window.onload = function() {
    var this_url = window.location.href
    var endpoint_url = this_url.replace("/search/", "/api/search/");
    resultsWorker.postMessage(endpoint_url);
};


//When worker sends message back, display results accordingly
resultsWorker.onmessage = function(e) {
    document.getElementById('content')
        .insertAdjacentHTML('afterend', resultTemplate);

    result = JSON.parse(e.data);
    sorted_result = sorting(result["items"], "time_alive_seconds");

    //This is sooooooo messy.
    //Is there a better way to insert large amounts of HTML with variables inline?
    for (var i = 0; i < sorted_result.length; i++) { //displaying issue box, heading & subtitle
        var issue_url = sorted_result[i]["html_url"];
        var issue_title = sorted_result[i]["title"];
        var repo_url = sorted_result[i]["repository_url"];
        var repo_name = sorted_result[i]["name"];
        var repo_time_alive = sorted_result[i]["time_alive_readable"];


        document.getElementById('result-row').insertAdjacentHTML('beforeend', '\
            <div class="issue-box col-12 col-sm-6 col-md-4 col-lg-3">\
                <div class="issue">\
                    <div class="issue-info">\
                        <div class="issue-title">\
                            <a href="' + issue_url + '">' + issue_title + '</a>\
                        </div>\
                        <div class="subtitle">\
                            <a href="' + repo_url +  '" target="_blank">\
                            ' + repo_name + '</a> - \
                            ' + repo_time_alive + ' old\
                        </div>\
                    </div>\
                        <div id="labels-issue' + i + '" class="labels">\
                        </div>\
                </div>\
            </div>'
        );

        for (var j = 0; j < sorted_result[i]['labels'].length; j++) { //displaying list of labels
            var label_color = "#" + sorted_result[i]["labels"][j]["color"];
            var label_name = sorted_result[i]["labels"][j]["name"];
            var label_text_color = ideal_text_color(label_color);

            document.getElementById('labels-issue' + i).insertAdjacentHTML('beforeend', '\
                <div class="label badge badge-pill badge-primary" \
                     style="background-color:' + label_color + '; color:' + label_text_color + ';">\
                    ' + label_name + '\
                </div>'
            );
        }
    }
};
