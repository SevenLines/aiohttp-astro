<template>
  <div class="natal">
    <div class="inner-circle" :style="innerStyle"></div>
    <div class="outer-circle" :style="outerStyle"></div>
    <div class="planets">
      <planet v-for="planet in planets"
              :name="planet.name"
              :alt="planet.alt"
              :az="planet.az"
              :ra="planet.ra"
              :dec="planet.dec"
              :width="width"
              :circle-width="circleWidth"
              v-bind:key="planet.name"
      ></planet>
    </div>

    <div class="zodiacs">
      <zodiac v-for="z in zodiacs"
              :start="z.start"
              :end="z.end"
              :name="z.name"
              :width="width"
              :circle-width="circleWidth"
              :key="z.name"
      ></zodiac>
    </div>
  </div>
</template>


<script>
  import Planet from '@/components/Planet'
  import Zodiac from '@/components/Zodiac'

  export default {
    name: 'natal',
    data () {
      return {
        planets: {},
        zodiacs: [
          {name: 'Aries', start: 0, end: 30},
          {name: 'Taurus', start: 30, end: 60},
          {name: 'Gemini', start: 60, end: 90},
          {name: 'Cancer', start: 90, end: 120},
          {name: 'Leo', start: 120, end: 150},
          {name: 'Virgo', start: 150, end: 180},
          {name: 'Libra', start: 180, end: 210},
          {name: 'Scorpio', start: 210, end: 240},
          {name: 'Sagittarius', start: 240, end: 270},
          {name: 'Capricorn', start: 270, end: 300},
          {name: 'Aquarius', start: 300, end: 330},
          {name: 'Pisces', start: 330, end: 360}
        ],
        circleWidth: 40
      }
    },
    components: {Zodiac, Planet},
    mounted () {
      let self = this

      function setConnection () {
        let server = '127.0.0.1:8081'
        let url = server + '/ws/positions/'

        let sock
        sock = new WebSocket('ws://' + url)
        sock.onopen = function () {
          navigator.geolocation.getCurrentPosition(function (position) {
            sock.send(JSON.stringify({
              'type': 'set_location',
              'data': {
                'lat': position.coords.latitude,
                'lon': position.coords.longitude
              }
            }))
          })
        }

        sock.onmessage = function (event) {
          let data = JSON.parse(event.data)
          self.planets = data.planets
        }

        sock.onclose = function () {
          setTimeout(setConnection, 1000)
        }
      }

      setConnection()
    },
    computed: {
      width () {
        return Math.min(window.innerHeight, window.innerWidth) - this.circleWidth * 2 - 20
      },
      outerStyle () {
        let width = this.width - this.circleWidth * 2
        return {
          width: `${width}px`,
          height: `${width}px`,
          borderRadius: `${width}px`
        }
      },
      innerStyle () {
        let width = this.width + this.circleWidth * 2
        return {
          width: `${width}px`,
          height: `${width}px`,
          borderRadius: `${width}px`
        }
      }
    }
  }
</script>


<style lang="scss">
  @mixin size($width) {
    height: $width;
    width: $width;
    border-radius: $width;
  }

  .inner-circle {
    position: absolute;
    left: 50%;
    top: 50%;
    border: 2px solid black;

    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  .outer-circle {
    position: absolute;
    left: 50%;
    top: 50%;
    border: 2px solid black;

    -webkit-transform: translate(-50%, -50%);
    -moz-transform: translate(-50%, -50%);
    -ms-transform: translate(-50%, -50%);
    -o-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  .natal {
    left: 50%;
    top: 50%;
    height: 100%;
    width: 100%;
  }


</style>
