import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import App from './App.vue'

import Home from './pages/Home.vue'
import Basket from './pages/Basket.vue'
import Product from './pages/Product.vue'
import Section from './pages/Section.vue'
import OrderAccepted from './pages/OrderAccepted.vue'

const app = createApp(App)
const pinia = createPinia()
const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/basket', name: 'Basket', component: Basket },
  { path: '/section/:id', name: 'Section', component: Section, props: true },
  { path: '/product/:id', name: 'Product', component: Product, props: true },
  { path: '/orderaccepted', name: 'OrderAccepted', component: OrderAccepted }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

app.use(router)
app.use(pinia)
app.use(autoAnimatePlugin)

app.mount('#app')
