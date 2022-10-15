$(function() {

	// Get the form.
	var form = $('#ajax-contact');

	// Get the messages div.
	var formMessages = $('#form-messages');

	// Set up an event listener for the contact form.
	$(form).submit(function(e) {
		// Stop the browser from submitting the form.
		e.preventDefault();

		// Serialize the form data.
		var formData = $(form).serialize();

		// Submit the form using AJAX.
		$.ajax({
			type: 'POST',
			url: $(form).attr('action'),
			data: formData
		})
		.done(function(response) {
			// Make sure that the formMessages div has the 'success' class.
			$(formMessages).removeClass('bg-danger');
			$(formMessages).addClass('bg-success');

			// Set the message text.
			$(formMessages).text('Your message successfully sent');

			// Clear the form.
			$('#name, #email, #message').val('');			
		})
		.fail(function(data) {
			// Make sure that the formMessages div has the 'error' class.
			$(formMessages).removeClass('bg-success');
			$(formMessages).addClass('bg-danger');

			// Set the message text.
			if (data.responseText !== '') {
				$(formMessages).text(data.responseText);
			} else {
				$(formMessages).text('Oops! An error occured and your message could not be sent.');
			}
		});

	});

});



//selecting all required elements
const dropArea = document.querySelector(".drag-area");
let dragText = dropArea.querySelector("header");
let button = document.querySelector("#browse-btn");
let input = document.querySelector("#fil-input");
const cl_btn = document.querySelector("#clear-btn");
const label_btn = document.querySelector("#label-btn");
let label_result = document.querySelector(".label-result");

let file; //this is a global variable and we'll use it inside multiple functions
// button.onclick = ()=>{
//   input.click(); //if user click on the button then the input also clicked
// }

button.addEventListener("click", ()=>{input.click();})

input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});

//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});

function showFile(){
  let fileType = file.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"]; //adding some valid image extensions in array
  if(validExtensions.includes(fileType)){ //if user selected file is an image file
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = ()=>{
      let fileURL = fileReader.result; //passing user file source in fileURL variable
        
      let imgTag = `<img src="${fileURL}" alt="image">`; //creating an img tag and passing user selected file source inside src attribute
      dropArea.innerHTML = imgTag; //adding that created img tag inside dropArea container
    }
    fileReader.readAsDataURL(file);
	label_btn.style.visibility = "visible";
	cl_btn.style.visibility = "visible";
  }
  else{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}



cl_btn.addEventListener("click", ()=>{
	dropArea.innerHTML = `<div class="icon"><i class="fas fa-cloud-upload-alt"></i></div>
	<header>Drag & Drop to Upload File</header>
	<span>OR</span>
	<button id="browse-btn">Browse File</button>
	<input type="file" id="fil-input" hidden>`;

	file = null;
	delete fileReader;
	document.getElementById("label-btn").style.visibility = "hidden";
	cl_btn.style.visibility = "hidden";
	dropArea.classList.remove("active");
	label_result.style.visibility = "hidden";
	label_result.textContent = "";

	button = document.querySelector("#browse-btn"),
	input = document.querySelector("#fil-input");
	button.addEventListener("click", ()=>{input.click();})
	input.addEventListener("change", function(){
	//getting user select file and [0] this means if user select multiple files then we'll select only the first one
	file = this.files[0];
	dropArea.classList.add("active");
	showFile(); //calling function
	});
})


label_btn.addEventListener("click", ()=>{
	let = formData = new FormData();
	formData.append("file", file);

	fetch(`${window.origin}/label`, {
		headers: {
			"Content-Type": file.contentType,
		},
		mode: "no-cors",
		method: "POST",
		files: file,
		body: formData
	}).then(res => {
		if (res.ok)
		{
			document.querySelector('#app-audio').play()
			return res.json();
		}
	}).then(data => {
		text_label = data["text_label"]
		console.log(text_label)
		label_result.style.visibility = "visible";
		label_result.textContent = text_label;
	})
})
