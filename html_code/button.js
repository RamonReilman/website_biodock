var slider = document.getElementById("slider_input");
var output = document.getElementById("slider_output");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}


// https://www.w3schools.com/howto/howto_js_rangeslider.asp