document.addEventListener('DOMContentLoaded', () => {
  const usernameField = document.querySelector('.login-container #username')
  const passwordField = document.querySelector('.login-container #password')

  if (!usernameField || !passwordField) {
    return
  }

  if (!window.localStorage) {
    return
  }

  const store = window.localStorage.getItem('authentication')
  if (!store) {
    return
  }

  let data

  try {
    data = JSON.parse(store)
  } catch(e) {
    return
  }

  setTimeout(() => {
    if (usernameField.value || passwordField.value) {
      return
    }

    usernameField.value = data.username
    passwordField.value = data.password

    localStorage.removeItem('authentication')
  }, 750)
})
