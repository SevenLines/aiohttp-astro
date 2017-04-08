<template>
  <div class="row" style="height: 100%">
    <div class="col">
      <div class="natal" id="natal">
        <svg width="100%" height="100%">
          <svg x="50%" y="50%" width="1" height="1" overflow="visible">
            <zodiac v-for="(z, index) in zodiacs"
                    :start="z.start"
                    :end="z.end"
                    :name="z.name"
                    :icon="z.icon"
                    :width="width"
                    :circle-width="circleWidth"
                    :key="z.name"
            ></zodiac>
            <aspect v-for="(a, index) in aspects"
                    :planet1="a.planet1"
                    :planet2="a.planet2"
                    :type="a.type"
                    :width="width"
                    :circleWidth="circleWidth"
                    :key="a.id"
                    @aspectHover="onAspectHover(index)"
            ></aspect>
          </svg>
        </svg>

        <div class="planets">
          <planet v-for="planet in planets"
                  :name="planet.name"
                  :alt="planet.alt"
                  :az="planet.az"
                  :ra="planet.ra"
                  :dec="planet.dec"
                  :lon="planet.lon"
                  :reverse="planet.reverse"
                  :width="width"
                  :day="planet.day"
                  :circle-width="circleWidth"
                  :is-active="planet.name === activePlanetName"
                  @click="onPlanetClick(planet, $event)"
                  v-bind:key="planet.name"
          ></planet>
        </div>

      </div>
    </div>
    <div class="col">
      <div class="location-editor">
        <h2><small>Время: </small>{{ realTime.format('LTS') }}</h2>
        <hr>
        <planet-info :active-planet="activePlanet"/>
        <!--<div class="buttons">-->
          <!--<button class="btn btn-primary">RESET</button>-->
        <!--</div>-->
        <div class="map-wrapper">
          <div id="map"></div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  import Planet from '@/components/Planet'
  import Zodiac from '@/components/Zodiac'
  import Aspect from '@/components/Aspect'
  import PlanetInfo from '@/components/PlanetInfo'
  import moment from 'moment-timezone'
  import _ from 'lodash'
  moment.locale(navigator.language)

  export default {
    name: 'natal',
    data () {
      return {
        draw: null,
        map: null,
        location: require('js-cookie').get('location'),
        locationMarker: null,
        activeAspectId: null,
        activeAspect: null,
        socket: null,
        planets: {},
        activePlanetName: 'moon',
        aspects: [],
        serverTime: moment(new Date()),
        serverTimeOffset: 0,
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
    components: {Zodiac, Planet, Aspect, PlanetInfo},
    watch: {
      location: function () {
        this.updateMapLocation()
      }
    },
    computed: {
      realTime () {
        this.serverTimeOffset // для синхронизации
        return this.serverTime
      },
      activePlanet () {
        let self = this
        return _.find(this.planets, (planet) => {
          return planet.name === self.activePlanetName
        })
      }
    },
    mounted () {
      let self = this

      window.addEventListener('resize', this.resize)
      this.resize()

      function setConnection () {
        let server = process.env.HOST
        let url = server + '/ws/positions/'

        self.socket = new WebSocket('ws://' + url)
        self.socket.onopen = function () {
          if (!(self.location && self.location.longitude)) {
            navigator.geolocation.getCurrentPosition(function (position) {
              self.location = position.coords
              self.updateMapLocation()
              self.sendSetLocationSocket(position.coords.latitude, position.coords.longitude)
            })
          } else {
            self.updateMapLocation()
            self.sendSetLocationSocket(self.location.latitude, self.location.longitude)
          }
        }

        self.socket.onmessage = function (event) {
          let data = JSON.parse(event.data)
          self.planets = data.planets
          self.serverTime = moment(data.server_time)
          self.serverTimeOffset = 0
          self.planets.forEach(item => {
            if (item.day !== null) {
              item.day.start = moment(item.day.start)
              item.day.end = moment(item.day.end)
            }
            return item
          })
          self.generateAspects()
        }

        self.socket.onclose = function () {
          setTimeout(setConnection, 1000)
        }
      }

      // launch timer
      self.doTheTime()

//      self.initMap()
      setConnection()
    },
    beforeDestroy () {
      window.removeEventListener('resize', this.resize)
    },
    methods: {
      onPlanetClick (planet, $event) {
        this.activePlanetName = planet.name
      },
      doTheTime () {
        this.serverTimeOffset += 1
        this.serverTime.add(1, 'seconds')
        setTimeout(() => {
          this.doTheTime()
        }, 1000, this)
      },
      generateAspects () {
        let self = this
        this.aspects.length = 0

        for (let i = 0; i < this.planets.length; ++i) {
          for (let j = i; j < this.planets.length; ++j) {
            let planet1 = this.planets[i]
            let planet2 = this.planets[j]
            let aspect = null
            let angle1 = Math.degrees(planet1.lon)
            let angle2 = Math.degrees(planet2.lon)
            let angle = Math.abs(angle1 - angle2)
            if (angle > 180) {
              angle = 360 - angle
            }

            if (Math.abs(angle - 180) < 5) {
              aspect = {
                type: 'opposition'
              }
            } else if (Math.abs(angle - 60) < 5) {
              aspect = {
                type: 'sextile'
              }
            } else if (Math.abs(angle - 90) < 5) {
              aspect = {
                type: 'square'
              }
            } else if (Math.abs(angle - 120) < 5) {
              aspect = {
                type: 'trine'
              }
            } else if (Math.abs(angle) < 5) {
              aspect = {
                type: 'conjunction'
              }
            }

            if (aspect) {
              aspect.planet1 = planet1
              aspect.planet2 = planet2
              aspect.id = `${planet1.name}-${planet2.name}`
              this.aspects.push(aspect)
            }
          }
        }

        this.aspects.sort((a) => {
          if (a.id === self.activeAspectId) {
            return 1
          }
          return 0
        })
      },
      initMap () {
        let GoogleMapsLoader = require('google-maps') // only for common js environments
        let self = this
        GoogleMapsLoader.KEY = 'AIzaSyBel-jfT8hor4c7vzA6ItUFRNIQI-SS1kU'

        GoogleMapsLoader.load(function (google) {
          global.google = google
          self.map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: -34.397, lng: 150.644},
            zoom: 8
          })

          self.locationMarker = new google.maps.Marker({
            title: ''
          })

          self.map.addListener('click', function (e) {
            self.locationMarker.setPosition(e.latLng)
            self.map.panTo(e.latLng)
            self.sendSetLocationSocket(e.latLng.latitude, e.latLng.longitude)
          })

          self.updateMapLocation()
        })
      },
      updateMapLocation () {
        if (this.map && this.location) {
          let coord = new global.google.maps.LatLng(
            this.location.latitude,
            this.location.longitude
          )

          this.map.setCenter(coord)
          this.locationMarker.setPosition(coord)
          this.locationMarker.setMap(this.map)
        }
      },
      sendSetLocationSocket (latitude, longitude) {
        require('js-cookie').set('location', {
          latitude: latitude,
          longitude: longitude
        })
        if (this.socket) {
          this.socket.send(JSON.stringify({
            'type': 'set_location',
            'data': {
              'lat': latitude,
              'lon': longitude
            }
          }))
        }
      },
      onAspectHover (index) {
        this.activeAspectId = this.aspects[index].id
        this.activeAspect = this.aspects[index]
        this.aspects.push(this.aspects.splice(index, 1)[0])
      },
      resize () {
        let natal = document.querySelector('.natal')
        this.width = Math.min(natal.offsetWidth, natal.offsetHeight) - this.circleWidth * 2 - 40
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

  .natal {
    left: 50%;
    top: 50%;
    height: 90%;
    width: 100%;
    /*height: 100%;*/
  }

  .row {
    margin-left: 0;
    margin-right: 0;
  }

  #map {
    height: 500px;
    width: 100%;
  }

  .location-editor {
    padding: 1em;
    height: 100%;
    .map-wrapper {
    }
    .buttons {
      margin-bottom: 1em;
    }
  }


</style>
