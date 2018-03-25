/* eslint camelcase: 0 */
function sortByGold (player1, player2) {
  return player2.total_gold - player1.total_gold
}

function sortByExp (player1, player2) {
  return player2.total_xp - player1.total_xp
}

function getFirstAndSecondPositionPlayers (playersArray) {
  const byGold = playersArray.sort(sortByGold)
  const byExp = playersArray.sort(sortByExp)
  return {
    first: byGold[0].hero_id,
    second: byGold[1].hero_id
  }
}

function getSeq (data, heroId) {
  const {radiant: {radiantHeroPick1, radiantHeroPick2, radiantHeroPick3, radiantHeroPick4, radiantHeroPick5},
    dire: {direHeroPick1, direHeroPick2, direHeroPick3, direHeroPick4, direHeroPick5}} = data
  if (heroId === radiantHeroPick1 || heroId === direHeroPick1) return 1
  if (heroId === radiantHeroPick2 || heroId === direHeroPick2) return 2
  if (heroId === radiantHeroPick3 || heroId === direHeroPick3) return 3
  if (heroId === radiantHeroPick4 || heroId === direHeroPick4) return 4
  if (heroId === radiantHeroPick5 || heroId === direHeroPick5) return 5
}

function getTotalTimeTaken (draftTimings, hero_id) {
  if (!draftTimings) return -1
  return draftTimings.filter(dt => dt.hero_id === hero_id)[0].total_time_taken
}

function getPlayer (players, hero_id, isPick) {
  if (!isPick) return { playerSlot: -1, account_id: -1 }
  const player = players.filter(player => player.hero_id === hero_id)[0]
  return {
    playerSlot: player.player_slot,
    accountId: player.account_id
  }
}

function parseGame (game) {
  const { match_id, draft_timings, leagueid, picks_bans, dire_team = {team_id: -1},
    radiant_team = {team_id: -1}, players, radiant_win } = game

  if (!picks_bans || !players || radiant_win === undefined || radiant_win === null) return undefined

  const radiantWin = radiant_win ? 1 : 0
  const radiantBans = []
  const radiantPicks = []
  const direBans = []
  const direPicks = []

  picks_bans.forEach((pb) => {
    const pickBan = pb
    const { is_pick, hero_id, team } = pickBan
    let pickObj = {heroId: hero_id, ttt: getTotalTimeTaken(draft_timings, hero_id)}
    pickObj = Object.assign(pickObj, getPlayer(players, hero_id, is_pick))

    if (is_pick && team === 0) radiantPicks.push(pickObj)
    if (!is_pick && team === 0) radiantBans.push(pickObj)
    if (is_pick && team === 1) direPicks.push(pickObj)
    if (!is_pick && team === 1) direBans.push(pickObj)
  })

  const radiantPlayers = []
  const direPlayers = []
  players.forEach((player) => {
    if (player.isRadiant) radiantPlayers.push(player)
    else direPlayers.push(player)
  })

  // for heroes: account_id, total_gold, total_xp, benchmarks, isRadiant, hero_id
  // team 2 is radiant

  const data = {
    radiantWin,
    matchId: match_id,
    leagueId: leagueid,
    radiantTeamId: radiant_team.team_id,
    direTeamId: dire_team.team_id,
    radiant: {
      radiantBan1: radiantBans[0].heroId,
      radiantBan2: radiantBans[1].heroId,
      radiantBan3: radiantBans[2].heroId,
      radiantBan4: radiantBans[3].heroId,
      radiantBan5: radiantBans[4].heroId,
      radiantBan1TotalTime: radiantBans[0].ttt,
      radiantBan2TotalTime: radiantBans[1].ttt,
      radiantBan3TotalTime: radiantBans[2].ttt,
      radiantBan4TotalTime: radiantBans[3].ttt,
      radiantBan5TotalTime: radiantBans[4].ttt,
      radiantHeroPick1: radiantPicks[0].heroId,
      radiantHeroPick2: radiantPicks[1].heroId,
      radiantHeroPick3: radiantPicks[2].heroId,
      radiantHeroPick4: radiantPicks[3].heroId,
      radiantHeroPick5: radiantPicks[4].heroId,
      radiantHeroPick1TotalTime: radiantPicks[0].ttt,
      radiantHeroPick2TotalTime: radiantPicks[1].ttt,
      radiantHeroPick3TotalTime: radiantPicks[2].ttt,
      radiantHeroPick4TotalTime: radiantPicks[3].ttt,
      radiantHeroPick5TotalTime: radiantPicks[4].ttt,
      radiantHeroPick1Player: radiantPicks[0].accountId,
      radiantHeroPick2Player: radiantPicks[1].accountId,
      radiantHeroPick3Player: radiantPicks[2].accountId,
      radiantHeroPick4Player: radiantPicks[3].accountId,
      radiantHeroPick5Player: radiantPicks[4].accountId
    },
    dire: {
      direBan1: direBans[0].heroId,
      direBan2: direBans[1].heroId,
      direBan3: direBans[2].heroId,
      direBan4: direBans[3].heroId,
      direBan5: direBans[4].heroId,
      direBan1TotalTime: direBans[0].ttt,
      direBan2TotalTime: direBans[1].ttt,
      direBan3TotalTime: direBans[2].ttt,
      direBan4TotalTime: direBans[3].ttt,
      direBan5TotalTime: direBans[4].ttt,
      direHeroPick1: direPicks[0].heroId,
      direHeroPick2: direPicks[1].heroId,
      direHeroPick3: direPicks[2].heroId,
      direHeroPick4: direPicks[3].heroId,
      direHeroPick5: direPicks[4].heroId,
      direHeroPick1TotalTime: direPicks[0].ttt,
      direHeroPick2TotalTime: direPicks[1].ttt,
      direHeroPick3TotalTime: direPicks[2].ttt,
      direHeroPick4TotalTime: direPicks[3].ttt,
      direHeroPick5TotalTime: direPicks[4].ttt,
      direHeroPick1Player: direPicks[0].accountId,
      direHeroPick2Player: direPicks[1].accountId,
      direHeroPick3Player: direPicks[2].accountId,
      direHeroPick4Player: direPicks[3].accountId,
      direHeroPick5Player: direPicks[4].accountId
    }
  }

  if (radiantBans[5]) {
    data.radiant.radiantBan6 = radiantBans[5].heroId
    data.radiant.radiantBan6TotalTime = radiantBans[5].ttt
  }
  if (direBans[5]) {
    data.dire.direBan6 = direBans[5].heroId
    data.dire.direBan6TotalTime = direBans[5].ttt
  }

  const radiantFirstSecondPositionPlayers = getFirstAndSecondPositionPlayers(radiantPlayers)
  data.radiantFirstPositionPickSeq = getSeq(data, radiantFirstSecondPositionPlayers.first)
  data.radiantSecondPositionPickSeq = getSeq(data, radiantFirstSecondPositionPlayers.second)
  const direFirstSecondPositionPlayers = getFirstAndSecondPositionPlayers(direPlayers)
  data.direFirstPositionPickSeq = getSeq(data, direFirstSecondPositionPlayers.first)
  data.direSecondPositionPickSeq = getSeq(data, direFirstSecondPositionPlayers.second)
  return data
}

module.exports = {
  parseGame
}
