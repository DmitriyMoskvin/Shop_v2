<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useBasketStore } from '../basket'
import { useRootStore } from '../root'

import Menu from './Menu.vue'

const rootStore = useRootStore()
const basketStore = useBasketStore()

onMounted(rootStore.getSections)
onMounted(() => (basketStore.quantityOfGoods = basketStore.getQuantityOfGoods()))
</script>

<template>
  <header>
    <div class="fixed z-50 w-full bg-white h-40 md:h-32">
      <div class="w-4/5 m-auto flex flex-col md:flex-row justify-between items-center">
        <div class="flex gap-1">
          <img src="/Phone.jpg" alt="Phone" class="size-6" />
          <a href="tel:87770000000">8 (777) 000 0000</a>
        </div>
        <div>
          <RouterLink to="/"> <img src="/Logo.JPG?url" alt="Logo" /> </RouterLink>
        </div>
        <div class="flex">
          <div
            class="w-5 h-5 text-center text-white bg-green-500 rounded-full flex items-center justify-center"
          >
            <p>{{ basketStore.quantityOfGoods }}</p>
          </div>
          <RouterLink to="/basket">
            <img src="/basket.jpg" alt="basket" class="w-12" />
          </RouterLink>
        </div>
      </div>
      <Menu :sections="rootStore.sections" />
    </div>
  </header>
</template>
