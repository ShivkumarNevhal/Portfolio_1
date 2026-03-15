// SMOOTH SCROLL
function scrollToSection(id){
  document.getElementById(id).scrollIntoView({behavior:"smooth"});
}

// TYPING ANIMATION
const text = ["Data Scientist", "Machine Learning Engineer", "AI Enthusiast"];
let count = 0, index = 0, currentText = "", letter = "";

function type(){
  if(count === text.length){ count = 0; }
  currentText = text[count];
  letter = currentText.slice(0, ++index);
  document.getElementById("typing").textContent = letter;
  if(letter.length === currentText.length){
    count++; index = 0;
    setTimeout(type,1500);
  } else { setTimeout(type,100); }
}
type();

// PARTICLES CONFIGURATION
particlesJS("particles-js", {
  "particles": {
    "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
    "color": { "value": "#38bdf8" },
    "shape": { "type": "circle", "stroke": { "width": 0, "color": "#000000" } },
    "opacity": { "value": 0.6, "random": true },
    "size": { "value": 3, "random": true },
    "line_linked": {
      "enable": true,
      "distance": 120,
      "color": "#8b5cf6",
      "opacity": 0.4,
      "width": 1
    },
    "move": { "enable": true, "speed": 2, "direction": "none", "random": true, "straight": false, "out_mode": "out" }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": { "enable": true, "mode": "grab" },
      "onclick": { "enable": true, "mode": "repulse" },
      "resize": true
    },
    "modes": {
      "grab": { "distance": 140, "line_linked": { "opacity": 1 } },
      "repulse": { "distance": 200, "duration": 0.4 }
    }
  },
  "retina_detect": true
});

// NAVBAR TOGGLE
function toggleMenu(){
  document.getElementById("nav-menu").classList.toggle("active");
}

// CONTACT FORM SUBMISSION
document.getElementById("contactForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    try {

        const response = await fetch("/contact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                message: message
            })
        });

        const data = await response.json();

        if(response.ok){
            alert(data.message);
        } else {
            alert("Server error: " + data.message);
        }

        document.getElementById("contactForm").reset();

    } catch(error) {
        console.error("Fetch error:", error);
        alert("Network error. Please try again.");
    }
});
