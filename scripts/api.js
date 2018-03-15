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

async function getGame (gameId) {
  const url = `https://api.opendota.com/api/matches/${gameId}`
  return callApi(url).then((game) => {
    return game
  }).catch((err) => console.log(err))
}

function getPlayer (playerId) {
  const url = `https://api.opendota.com/api/players/${playerId}`
  return callApi(url).then((player) => {
    return player
  })
}

function getPlayerHeroStats (accountId, options) {
  let url = `https://api.opendota.com/api/players/${playerId}/heroes?`
  if (options) {
    if (options.heroId) url += `hero_id=${options.heroId}`
  }
  return callApi(url).then((playerHeroStats) => {
    return playerHeroStats
  })
}

async function getProMatches (lessThanGameId) {
  let url = `https://api.opendota.com/api/proMatches?`
  if (lessThanGameId) url += `less_than_match_id=${lessThanGameId}`
  return callApi(url).then((gameArray) => {
    return gameArray
  })
}

module.exports = {
  getGame, getPlayer, getPlayerHeroStats, getProMatches
}
