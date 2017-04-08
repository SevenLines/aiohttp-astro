<template>
  <div v-if="activePlanet">
    <h3>{{activePlanet.name}}</h3>
    <ul>
      <li>longitude: {{lon.deg}}&deg;{{lon.min}}&prime;{{lon.sec}}&Prime;</li>
      <li>latitutde: {{lat.deg}}&deg;{{lat.min}}&prime;{{lat.sec}}&Prime;</li>
      <li>azimuth: {{az.deg}}&deg;{{az.min}}&prime;{{az.sec}}&Prime;</li>
      <li>ra: {{ra.deg}}&deg;{{ra.min}}&prime;{{ra.sec}}&Prime;</li>
      <li>dec: {{dec.deg}}&deg;{{dec.min}}&prime;{{dec.sec}}&Prime;</li>
    </ul>
  </div>
</template>

<script>
  import helpers from '../helpers/helpers.js'

  export default {
    name: 'planet-info',
    props: ['active-planet'],
    computed: {
      lon () {
        return helpers.ConvertDDToDMS(this.activePlanet.lon)
      },
      lat () {
        return helpers.ConvertDDToDMS(this.activePlanet.lat)
      },
      az () {
        return helpers.ConvertDDToDMS(this.activePlanet.az)
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
