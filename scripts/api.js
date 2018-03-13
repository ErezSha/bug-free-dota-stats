const fetch = require('node-fetch')

function callApi (url, options = {}) {
  return fetch(url, options).then(response => {
    return response.json()
  }).then((jsonData) => {
    return jsonData
  }).catch(
    error => console.log(error)
  )
}

function getGame (gameId) {
  const url = `https://api.opendota.com/api/matches/${gameId}`
  return callApi(url).then((game) => {
    return game
  })
}

module.exports = {
  getGame
}
