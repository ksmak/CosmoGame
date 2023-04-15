export const getToken = async (auth) => {
  return fetch('http://0.0.0.0:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(auth)
  })
}

export const getGameObjects = async (token) => {
  return fetch('http://0.0.0.0:8000/api/objects', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  })
}