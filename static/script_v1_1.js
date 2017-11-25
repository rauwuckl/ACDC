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
  snapshot.upload({api_url: "/api/uploadImage"}).done(function(response) {
    console.log(response);
    let respObject = jQuery.parseJSON(response);
    console.log(respObject);
    if(respObject.status == "doctor_coming"){
      $("#doctor_coming_overlay").show();
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

});
