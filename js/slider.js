var slider = document.getElementById("dock_pose_input");
var output = document.getElementById("dock_pose_output");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}


var slider = document.getElementById("RMSD_input");
var output = document.getElementById("RMSD_output");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
}


// https://www.w3schools.com/howto/howto_js_rangeslider.asp