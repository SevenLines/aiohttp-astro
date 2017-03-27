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
              :lon="planet.lon"
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
              :icon="z.icon"
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
        width: 0,
        zodiacs: [
          {name: 'Aries', start: 0, end: 30, icon: '♈'},
          {name: 'Taurus', start: 30, end: 60, icon: '♉'},
          {name: 'Gemini', start: 60, end: 90, icon: '♊'},
          {name: 'Cancer', start: 90, end: 120, icon: '♋'},
          {name: 'Leo', start: 120, end: 150, icon: '♌'},
          {name: 'Virgo', start: 150, end: 180, icon: '♍'},
          {name: 'Libra', start: 180, end: 210, icon: '♎'},
          {name: 'Scorpio', start: 210, end: 240, icon: '♏'},
          {name: 'Sagittarius', start: 240, end: 270, icon: '♐'},
          {name: 'Capricorn', start: 270, end: 300, icon: '♑'},
          {name: 'Aquarius', start: 300, end: 330, icon: '♒'},
          {name: 'Pisces', start: 330, end: 360, icon: '♓'}
        ],
        circleWidth: 40
      }
    },
    components: {Zodiac, Planet},
    mounted () {
      let self = this

      window.addEventListener('resize', this.resize)
      this.resize()

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
    beforeDestroy () {
      window.removeEventListener('resize', this.resize)
    },
    computed: {
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
    },
    methods: {
      resize () {
        this.width = Math.min(window.innerHeight, window.innerWidth) - this.circleWidth * 2 - 20
        this.circleWidth = this.width / 20
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

    -webkit-transition: all 0.1s;
    -moz-transition: all 0.1s;
    -ms-transition: all 0.1s;
    -o-transition: all 0.1s;
    transition: all 0.1s;

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

    -webkit-transition: all 0.1s;
    -moz-transition: all 0.1s;
    -ms-transition: all 0.1s;
    -o-transition: all 0.1s;
    transition: all 0.1s;

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
