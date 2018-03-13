const { getGame } = require('./scripts/api')
const { parseGame } = require('./scripts/gameParser')
const fs = require('fs')

// 3777222389

getGame(3779051877)
  .then(game => parseGame(game))
  .then(parsedGame => {
    const data = JSON.stringify({[parsedGame.matchId]: parsedGame})
    fs.writeFileSync('./data/sampleGame.json', data)
  })
  .catch(err => console.log(err))
