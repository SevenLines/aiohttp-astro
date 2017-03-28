<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
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

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    height: 100%;
  }
</style>
