<script setup>
import { useRoute } from 'vue-router'
import Card from './Card.vue'

const route = useRoute()

defineProps({
  items: Array
})
</script>

<template>
  <div>
    <div
      v-if="route.path.includes('section')"
      class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-2 md:gap-5"
      v-auto-animate
    >
      <Card
        v-for="item in items"
        :key="item.id"
        :id="item.id"
        :name="item.name"
        :photo="item.photo"
        :price_per_unit="item.price_per_unit"
      />
    </div>
    <div v-else class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-5 gap-5" v-auto-animate>
      <Card
        v-for="item in items"
        :key="item.id"
        :id="item.id"
        :name="item.name"
        :photo="item.photo"
        :price_per_unit="item.price_per_unit"
      />
    </div>
  </div>
</template>
