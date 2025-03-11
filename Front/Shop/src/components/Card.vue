<script setup>
defineProps({
  id: Number,
  name: String,
  photo: String,
  price_per_unit: String
})
</script>

<template>
  <RouterLink :to="`/product/${id}`">
    <div
      class="h-full p-2 bg-white border border-slate-100 rounded-2xl cursor-pointer hover:shadow-xl hover:-translate-y-2 transition"
    >
      <div class="relative overflow-hidden h-0 pb-80 max-w-full">
        <img :src="photo" alt="test1" class="absolute h-full w-full rounded-2xl" />
      </div>
      <div>
        <p class="mt-2">{{ name }}</p>
      </div>
      <div class="flex justify-between">
        <div class="flex flex-col h-full justify-between lg:pt-5">
          <span class="text-slate-400">Цена:</span>
          <b>{{ price_per_unit }} тг</b>
        </div>
        <!-- <img src="/plus.svg" alt="Plus" /> -->
      </div>
    </div>
  </RouterLink>
</template>
