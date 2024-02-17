const x = document.getElementById("geoError");

function locateFunction() {
    var pos = {};

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            $.ajax({
                type: "POST",
                url: "/geopost",
                contentType: "application/json",
                data: JSON.stringify({location: pos}),
                dataType: "json",
                success: function(response) {
                    console.log(response)
                    // formData.set('address', response)
                    ;
                },
                error: function(err) {
                    console.log(err);
                }
            });

        }, showError)
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      x.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "An unknown error occurred."
      break;
  }
}
