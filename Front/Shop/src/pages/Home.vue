<script setup>
import { onMounted } from 'vue'
import { useRootStore } from '../root'
import CardList from '../components/CardList.vue'

const rootStore = useRootStore()

onMounted(rootStore.getItems)
</script>

<template>
  <div>
    <h2 class="text-3xl font-bold mb-8">Все товары</h2>
    <CardList :items="rootStore.items" />
  </div>
</template>
