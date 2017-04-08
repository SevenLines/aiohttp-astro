/**
 * Created by m on 08.04.17.
 */

export default {
  ConvertDDToDMS (radians) {
    // let dir = D < 0 ? lng ? 'W' : 'S' : lng ? 'E' : 'N'
    let degrees = Math.degrees(radians)
    let deg = 0 | (degrees < 0 ? degrees = -degrees : degrees)
    let min = 0 | degrees % 1 * 60
    let sec = (0 | degrees * 60 % 1 * 6000) / 100
    return {
      deg,
      min,
      sec: sec.toFixed()
    }
  }
}
