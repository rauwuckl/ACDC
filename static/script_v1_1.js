// import {Spinner} from 'static/spin.js';
// var spinnWheelOpts = {
//     lines: 11 // The number of lines to draw
//   , length: 28 // The length of each line
//   , width: 12 // The line thickness
//   , radius: 56 // The radius of the inner circle
//   , scale: 0.5 // Scales overall size of the spinner
//   , corners: 1 // Corner roundness (0..1)
//   , color: '#000' // #rgb or #rrggbb or array of colors
//   , opacity: 0 // Opacity of the lines
//   , rotate: 0 // The rotation offset
//   , direction: 1 // 1: clockwise, -1: counterclockwise
//   , speed: 0.7 // Rounds per second
//   , trail: 100 // Afterglow percentage
//   , fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
//   , zIndex: 2e9 // The z-index (defaults to 2000000000)
//   , className: 'spinner' // The CSS class to assign to the spinner
//   , top: '50%' // Top position relative to parent
//   , left: '50%' // Left position relative to parent
//   , shadow: false // Whether to render a shadow
//   , hwaccel: false // Whether to use hardware acceleration
//   , position: 'relative' // Element positioning
// };
// var globalActorList = [];
// var spinner = new Spinner(spinnWheelOpts);


$(document).ready(function(){


// navigator.mediaDevices.getUserMedia({video: true})
//   .then(gotMedia)
//   .catch(error => console.error('getUserMedia() error:', error));
//
// function gotMedia(mediaStream) {
//   const mediaStreamTrack = mediaStream.getVideoTracks()[0];
//   const imageCapture = new ImageCapture(mediaStreamTrack);
//   // console.log(imageCapture);
//
//   console.log("before");
//   console.log(imageCapture.getPhotoSettings());
//   console.log("done");
//   // var bla = {imageWidth: 200};
//   // console.log(bla.imageWidth);
//   const img = document.querySelector('img');
//
//   imageCapture.takePhoto()
//     .then(blob => {
//       var myurl = URL.createObjectURL(blob);
//       console.log(myurl);
//       img.src = myurl;
//       img.onload = () => { URL.revokeObjectURL(this.src);
//       uploadFile(blob);
//       }
//     })
//     .catch(error => console.error('takePhoto() error:', error));
// }
// const cam = document.getElementById("camera");
// console.log(cam);
var camera = new JpegCamera("#camera");

// var snapshot = camera.capture();

console.log("before showing")
// snapshot.show(); // Display the snapshot

// snapshot.upload({api_url: "/upload_image"}).done(function(response) {
//   response_container.innerHTML = response;
//   this.discard(); // discard snapshot and show video stream again
// }).fail(function(status_code, error_message, response) {
//   alert("Upload failed with status " + status_code);
// });
$("#call_doctor").click(call_doctor);

console.log("init done");
// Upload the image

function call_doctor(){
  var snapshot = camera.capture();
  snapshot.show();
  $("#loader").show();

  snapshot.upload({api_url: "/api/uploadImage"}).done(function(response) {
    let respObject = jQuery.parseJSON(response);
    $("#loader").hide();
    console.log(respObject);
    if(respObject.status == "doctor_coming"){
      $("#camera").css("opacity", .5);
      $("#doctor_coming_overlay").show();
      $("#call_doctor").hide();
      console.log("showed doctor_coming");
    }
    //this.discard(); // discard snapshot and show video stream again
  }).fail(function(status_code, error_message, response) {
    alert("Upload failed with status " + status_code);
  });
  console.log(snapshot);

}

function uploadFile(blob){

    var formdata = new FormData();
    formdata.append("file", blob)
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            let respObject = jQuery.parseJSON(this.responseText);
            console.log(respObject);
        }
        else if(this.readyState == 4 && this.status == 400){
            var serverMessage = jQuery.parseJSON(this.responseText).message;
            alert("The server could not classify your image: " + serverMessage);
            location.reload();
        }
        else if(this.readyState == 4){
            alert("Unknown server error");
            location.reload();
  }

    };

    xhttp.open("POST", "api/uploadImage", true);
    xhttp.send(formdata);
    return false;
}
 function close_accordion_section() {
        $('.accordion .accordion-section-title').removeClass('active');
        $('.accordion .accordion-section-content').slideUp(300).removeClass('open');
    }

    $('.accordion-section-title').click(function(e) {
        // Grab current anchor value
        var currentAttrValue = $(this).attr('href');

        if($(e.target).is('.active')) {
            close_accordion_section();
        }else {
            close_accordion_section();

            // Add active class to section title
            $(this).addClass('active');
            // Open up the hidden content panel
            $('.accordion ' + currentAttrValue).slideDown(300).addClass('open');
        }

        e.preventDefault();
    });
});
