/**
Clears the form when the page is loaded.
*/
window.onload = function() {
  document.getElementById("chat").reset();
};

/**
Toggles light and dark mode. Default mode is light.
*/
const setTheme = theme => {
  document.documentElement.className = theme;
  localStorage.setItem('theme', theme);
};

// check if theme is set in local storage
const savedTheme = localStorage.getItem('theme');

// if saved theme exists, set the theme to that
if (savedTheme) {
  setTheme(savedTheme);
}

/**
Displays the alerts for 2 seconds.
*/
$(document).ready(function() {
    // Hide flash messages after 2 seconds
    setTimeout(function() {
        $('.flashes').fadeOut('slow');
    }, 2000);
});


// toggle the note descriptions for the searches
$(document).ready(function() {
  $(".toggle-note").click(function() {
    var target = $($(this).data("target"));
    target.slideToggle();
    if ($(this).text() === "Show description") {
      $(this).text("Hide description");
    } else {
      $(this).text("Show description");
    }
  });
});



/**
Displays the chat button when the textarea is not empty.
*/
function ml_btn_visibility() {
    var textarea = document.querySelector('.ml_textarea');
    var button = document.getElementById('model-button');
    if (textarea.value.trim() !== '') {
        button.classList.add('show');
    } else {
        button.classList.remove('show');
    }
}

function chat_btn_visibility() {
    var textarea = document.querySelector('.chat_textarea');
    var button = document.getElementById('chat-button');
    if (textarea.value.trim() !== '') {
        button.classList.add('show');
    } else {
        button.classList.remove('show');
    }
}

/**
Displays the submit button when the title is not empty.
*/
function submit_btn_visibility() {
    var title = document.getElementById('title');
    var submit = document.getElementById('submit-btn');
    if (title.value.trim() !== '') {
        submit.disabled = false;
        submit.innerHTML = 'submit';
    } else {
        submit.disabled = true;
        submit.innerHTML = 'disabled';
    }
}

/**
deleting favorites
*/
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "favorites";
  });
}
