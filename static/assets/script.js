var menuIcon = document.querySelector(".menu-icon")
var sidebar = document.querySelector(".side-bar")
var container = document.querySelector(".container")
var viewbook = document.querySelector(".viewbook")

menuIcon.onclick = function(){
    sidebar.classList.toggle("small-sidebar");
    container.classList.toggle("large-container");
}

viewbook.onclick = function(){
    viewbook.classList.toggle("small-sidebar");
    container.classList.toggle("large-container");
}


document.addEventListener('contextmenu', event => event.preventDefault());


document.addEventListener('contextmenu', event => event.preventDefault());
document.addEventListener('keydown', event => {
    if (event.ctrlKey && (event.key === 'p' || event.key === 's' || event.key === 'u' || event.key === 'Shift' || event.key === 'j')) {
        event.preventDefault();
    }
});

window.onbeforeprint = function() {
    return false;
};

document.addEventListener('DOMContentLoaded', function() {
    const introText = document.querySelector('#home p');
    introText.style.display = 'none'; // Hide the intro text initially

    const welcomeMessage = document.querySelector('#home h1');
    welcomeMessage.addEventListener('animationend', function() {
        introText.style.display = 'inline-block'; // Show the intro text after welcome message animation
        introText.style.animation = 'typing 3.5s steps(40, end)';
        introText.addEventListener('animationend', function() {
            document.querySelector('.cta').style.display = 'inline-block'; // Show the CTA after the paragraph animation
        });
    });
});





    document.getElementById("signup-form").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        // Fetch form input values
        var fullName = document.getElementById("full-name").value;
        var email = document.getElementById("email").value;
        var password = document.getElementById("password").value;
        var confirmPassword = document.getElementById("confirm-password").value;
        var school = document.getElementById("school").value;
        var gradeLevel = document.getElementById("grade-level").value;

        // Validate password matching
        if (password !== confirmPassword) {
            showMessage("Passwords do not match", "error");
            return;
        }

        
        if (!isValidEmail(email)) {
            showMessage("Invalid email format", "error");
            return;
        }

        // Assume registration is successful for demonstration
        showMessage("Thanks for joining Study Arena! Enjoy your time here.", "success");

    });

    function isValidEmail(email) {
        // Basic email format validation
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showMessage(message, type) {
        var messageDiv = document.getElementById("message");
        messageDiv.textContent = message;
        messageDiv.className = type; // This assumes you have CSS classes for styling (e.g., .success and .error)
    }



// Display hidding content
    
document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");
    const showMoreButton = document.createElement("button");
    showMoreButton.textContent = "More";
    showMoreButton.classList.add("show-more");

    const bookContainer = document.querySelector(".book-container");
    if (bookContainer) {
        console.log("Book container found");
    } else {
        console.error("Book container not found");
    }
    
    const bookItems = Array.from(bookContainer.querySelectorAll(".book-item"));
    console.log("Book items:", bookItems);

    // Show only the first 4 books initially
    const initialBooksToShow = 4;
    for (let i = initialBooksToShow; i < bookItems.length; i++) {
        bookItems[i].classList.add("hidden");
    }

    bookContainer.after(showMoreButton);

    showMoreButton.addEventListener("click", function() {
        for (let i = initialBooksToShow; i < bookItems.length; i++) {
            bookItems[i].classList.remove("hidden");
        }
        showMoreButton.style.display = "none";
    });
});