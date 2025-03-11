<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import { useRootStore } from '../root'
import { useRoute } from 'vue-router'

import CardList from '../components/CardList.vue'
import Filters from '../components/Filters.vue'

const rootStore = useRootStore()
const route = useRoute()

const props = defineProps({
  id: String
})

const windowWidth = ref(window.innerWidth)

const handleResize = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

const sectionName = computed(() => {
  const targetObject = rootStore.sections.find((item) => item.id == route.params.id)
  return targetObject ? targetObject.name : null
})

watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      rootStore.getItemsBySectionId(newId)
    }
  }
)

watch(() => route.params, rootStore.resetFilters) // Reset filters when changing the URL

onMounted(() => {
  if (route.params.id) {
    rootStore.getItemsBySectionId(props.id)
  }
})
</script>

<template>
  <div>
    <h2 class="text-3xl font-bold mb-8">
      {{ sectionName }}
    </h2>
    <div v-if="windowWidth <= 768" class="mb-5">
      <Filters />
    </div>
    <div class="grid grid-cols-4 md:grid-cols-5 gap-2 md:gap-5">
      <Filters v-if="windowWidth > 768" class="col-span-1" />
      <CardList class="col-span-4" :items="rootStore.items" />
    </div>
  </div>
</template>
