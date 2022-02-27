function getUserProfile() {
  let currentEmailEl = document.getElementById('current_email');
  let currentUsernameEl = document.getElementById('current_username');
  fetch("/api/user", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "same-origin"
  })
  .then((res) => res.json())
  .then((data) => {
    console.log(data);
    currentEmailEl.innerText = data.data.email;
    currentUsernameEl.innerText = data.data.username;
  })
  .catch((err) => {
    console.log(err);
  });
}

document.addEventListener("DOMContentLoaded", () => { getUserProfile() }); 


function updateEmail(e) {
  e.preventDefault();
  let email = document.getElementById('new_email').value;
  let csrf = document.getElementsByName("csrf-token")[0].content;
  fetch("/api/email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrf,
    },
    credentials: "same-origin",
    body: JSON.stringify({ email: email }),
  })
  .then((res) => res.json())
  .then((data) => {
    console.log(data);
    if (data.errors) {
      alert(data.errors.display_error);
    }
  })
  .catch((err) => {
    console.log(err);
  });
};

const settings_form = document.getElementById('settings_form');
settings_form.addEventListener('submit', updateEmail);
