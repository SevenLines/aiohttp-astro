<template>
  <div v-if="activePlanet">
    <div class="name">{{activePlanet.name}}</div>
    <div class="reverse" v-if="activePlanet.reverse">r</div>
    <div class="clearfix"></div>
    <ul class="parameters">
      <li v-if="day">day <span class="value">{{day.number}}</span> from <span class="value">{{day.start}}</span> to <span class="value">{{day.end}}</span></li>
      <li><span class="key">longitude:</span> <span class="value">{{lon.deg}}&deg;{{lon.min}}&prime;{{lon.sec}}&Prime;</span></li>
      <li><span class="key">latitutde:</span> <span class="value">{{lat.deg}}&deg;{{lat.min}}&prime;{{lat.sec}}&Prime;</span></li>
      <li><span class="key">azimuth:</span> <span class="value">{{az.deg}}&deg;{{az.min}}&prime;{{az.sec}}&Prime;</span></li>
      <li><span class="key">altitude:</span> <span class="value">{{alt.deg}}&deg;{{alt.min}}&prime;{{alt.sec}}&Prime;</span></li>
      <li><span class="key">ra:</span> <span class="value">{{ra.deg}}&deg;{{ra.min}}&prime;{{ra.sec}}&Prime;</span></li>
      <li><span class="key">dec:</span> <span class="value">{{dec.deg}}&deg;{{dec.min}}&prime;{{dec.sec}}&Prime;</span></li>
    </ul>
  </div>
</template>

<script>
  import helpers from '../helpers/helpers.js'
  import moment from 'moment-timezone'

  export default {
    name: 'planet-info',
    props: ['active-planet'],
    computed: {
      day () {
        if (this.activePlanet.day) {
          return {
            number: this.activePlanet.day.number,
            start: moment(this.activePlanet.day.start).format('hh:mm:ss DD-MM'),
            end: moment(this.activePlanet.day.end).format('hh:mm:ss DD-MM')
          }
        } else {
          return null
        }
      },
      lon () {
        return helpers.ConvertDDToDMS(this.activePlanet.lon)
      },
      lat () {
        return helpers.ConvertDDToDMS(this.activePlanet.lat)
      },
      az () {
        return helpers.ConvertDDToDMS(this.activePlanet.az)
      },
      alt () {
        return helpers.ConvertDDToDMS(this.activePlanet.alt)
      },
      ra () {
        return helpers.ConvertDDToDMS(this.activePlanet.ra)
      },
      dec () {
        return helpers.ConvertDDToDMS(this.activePlanet.dec)
      }
    }
  }
</script>

<style lang="scss" >
  .name {
    float: left;
    font-size: 2em;
  }
  .reverse {
    background-color: #ff0053;
    display: block;
    width: 20px;
    height: 20px;
    font-size: 12px;
    clear: none;
    float: left;
    text-align: center;
    border-radius: 50%;
  }
  .parameters {
    list-style: none;
    padding-left: 0;
    .key {
    }
    .value {
      font-weight: bold;
    }
  }
</style>
