var DockPoseSlider = document.getElementById("dock_pose_input");
var DockPoseOutput = document.getElementById("dock_pose_output");
DockPoseOutput.innerHTML = DockPoseSlider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
DockPoseSlider.oninput = function() {
  DockPoseOutput.innerHTML = this.value;
}

var RMSDSlider = document.getElementById("RMSD_input");
var RMSDOutput = document.getElementById("RMSD_output");
RMSDOutput.innerHTML = RMSDSlider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
RMSDSlider.oninput = function() {
  RMSDOutput.innerHTML = this.value;
}


// https://www.w3schools.com/howto/howto_js_rangeslider.asp
function call_load(){
  document.getElementById("load").classList.add("load_icon")
  document.getElementById("load").classList.remove("load_icon_hidden")
}


window.addEventListener("submit", call_load)
