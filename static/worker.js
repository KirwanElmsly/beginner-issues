
onmessage = function(e) {
    url = e.data;
    console.log("Received " + url);
    var request = new XMLHttpRequest();
    request.open('GET', url, false);

    request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      // Success!
      var data = request.responseText
      console.log(request);
      postMessage(data);
    } else {
      // We reached our target server, but it returned an error - deal with it?

    }
    };

    request.onerror = function() {
    // There was a connection error of some sort - deal with it somehow?
    };

    request.send();
};
