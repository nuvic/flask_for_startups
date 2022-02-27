const register_form = document.getElementById('register_form');

function register(e) {
    e.preventDefault();
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    fetch("/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin",
      body: JSON.stringify({ username: username, email: email, password: password }),
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      register_form.reset();
    })
    .catch((err) => {
      console.log(err);
    });
};

register_form.addEventListener('submit', register);