// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

window.jQuery = window.$ = require('jquery')

Vue.config.productionTip = false

Vue.directive('window-resize', {
  bind: function (el, binding, vnode) {
    console.log(this)
    this.event = function (event) {
      vnode.context[binding.expression](event)
    }
  },
  unbind: function (el) {
    window.removeEventListener('resize', this.event)
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App}
})
