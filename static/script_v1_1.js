navigator.mediaDevices.getUserMedia({video: true})
  .then(gotMedia)
  .catch(error => console.error('getUserMedia() error:', error));

function gotMedia(mediaStream) {
  const mediaStreamTrack = mediaStream.getVideoTracks()[0];
  const imageCapture = new ImageCapture(mediaStreamTrack);
  // console.log(imageCapture);

  console.log("before");
  console.log(imageCapture.getPhotoSettings());
  console.log("done");
  // var bla = {imageWidth: 200};
  // console.log(bla.imageWidth);
  const img = document.querySelector('img');

  imageCapture.takePhoto()
    .then(blob => {
      var myurl = URL.createObjectURL(blob);
      console.log(myurl);
      img.src = myurl;
      img.onload = () => { URL.revokeObjectURL(this.src);
      uploadFile(blob);
      }
    })
    .catch(error => console.error('takePhoto() error:', error));
}


// Upload the image
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
