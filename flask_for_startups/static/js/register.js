const register_form = document.getElementById('register_form');

function register(e) {
    e.preventDefault();
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let csrf = document.getElementsByName("csrf-token")[0].content;
    fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "same-origin",
      body: JSON.stringify({ username: username, email: email }),
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.log(err);
    });
};

register_form.addEventListener('submit', register);