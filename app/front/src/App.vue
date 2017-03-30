<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  import 'bootstrap/dist/css/bootstrap.css'

  export default {
    name: 'app'
  }

  window.jQuery = window.$ = require('jquery')
  global.Tether = require('tether')
  require('bootstrap')

  Math.degrees = function (radians) {
    return radians * 180 / Math.PI
  }

  Math.radians = function (radians) {
    return radians * Math.PI / 180
  }

</script>

<style lang="scss">
  @import "assets/main.scss";
  /*@import "../node_modules/bootstrap/dist/css/bootstrap.css";*/

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height: 100%;
  }

  svg:not(:root) {
    overflow: visible !important;
  }

</style>
