<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  sections: Array
})
</script>

<template>
  <div class="bg-black">
    <ul class="w-4/5 m-auto flex text-white text-sm text-slate-300">
      <li class="grow hover:bg-slate-700" v-for="section in sections" :key="section.id">
        <RouterLink :to="`/section/${section.id}`">
          <p class="block py-2 w-auto text-center">{{ section.name }}</p>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>
