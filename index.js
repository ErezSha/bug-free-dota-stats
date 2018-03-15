/* eslint camelcase: 0 */
const { getGame, getProMatches } = require('./scripts/api')
const { parseGame } = require('./scripts/gameParser')
const fs = require('fs')
const moment = require('moment')

// 3777222389

/*
getGame(3779051877)
  .then(game => parseGame(game))
  .then(parsedGame => {
    const data = JSON.stringify({[parsedGame.matchId]: parsedGame})
    fs.writeFileSync('./data/sampleGame.json', data)
  })
  .catch(err => console.log(err))
*/

async function getMatchesToParse () {
  const games = {}
  let lowestGameId
  while (Object.keys(games).length < 5000) {
    const proMatches = await getProMatches(lowestGameId)
    proMatches.forEach((pm) => {
      const { match_id, start_time, radiant_win } = pm
      games[match_id] = { startTime: moment.unix(start_time).format('DD-MM-YY'), radiantWin: radiant_win, didFetch: false }
    })
    lowestGameId = proMatches[proMatches.length - 1].match_id
  }
  fs.writeFileSync('./data/games.json', JSON.stringify(games))
}

async function parseGames () {
  const gameData = fs.readFileSync('./data/games.json')
  const games = JSON.parse(gameData)
  const gameIds = Object.keys(games).reverse()
  const parsedGames = {}

  try {
    for (let gameIndex = 0; gameIndex < gameIds.length; gameIndex++) {
      const gameId = gameIds[gameIndex]
      // should not fetch game if already parsed
      if (games[gameId].didFetch) {
        console.log(`already fetched game ${gameId}`)
        continue
      }

      const fetchedGame = await getGame(gameId)
      let parsedGame
      try {
        parsedGame = parseGame(fetchedGame)
      } catch (err) {
        console.log(`skipping game ${gameId}`)
      }

      if (parsedGame) {
        parsedGames[gameId] = parsedGame
        games[gameId].didFetch = true
        console.log(`done with game ${gameId}`)
      } else {
        console.log(`skipping game ${gameId}`)
      }
    }
  } finally {
    console.log(`Done parsing ${Object.keys(parsedGames).length} games`)

    // write which games already fetched
    fs.writeFileSync('./data/games.json', JSON.stringify(games))

    // write parsed games to file
    const existingGames = JSON.parse(fs.readFileSync('./data/parsedGames.json'))
    const allGames = Object.assign(existingGames, parsedGames)
    const parsedGameDataToWrite = JSON.stringify(allGames)
    fs.writeFileSync('./data/parsedGames.json', parsedGameDataToWrite)
  }
}

// getMatchesToParse()
parseGames()
