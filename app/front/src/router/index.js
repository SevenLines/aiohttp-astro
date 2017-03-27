import Vue from 'vue'
import Router from 'vue-router'
import Natal from '@/components/Natal'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Natal',
      component: Natal
    }
  ]
})
