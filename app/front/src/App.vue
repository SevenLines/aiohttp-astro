<template>
  <div id="app">
    <router-view></router-view>
    <!-- Yandex.Metrika counter --> <script type="text/javascript"> (function (d, w, c) { (w[c] = w[c] || []).push(function() { try { w.yaCounter43894959 = new Ya.Metrika({ id:43894959, clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true, trackHash:true }); } catch(e) { } }); var n = d.getElementsByTagName("script")[0], s = d.createElement("script"), f = function () { n.parentNode.insertBefore(s, n); }; s.type = "text/javascript"; s.async = true; s.src = "https://mc.yandex.ru/metrika/watch.js"; if (w.opera == "[object Opera]") { d.addEventListener("DOMContentLoaded", f, false); } else { f(); } })(document, window, "yandex_metrika_callbacks"); </script> <noscript><div><img src="https://mc.yandex.ru/watch/43894959" style="position:absolute; left:-9999px;" alt="" /></div></noscript> <!-- /Yandex.Metrika counter -->
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
