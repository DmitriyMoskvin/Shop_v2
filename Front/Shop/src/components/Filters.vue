<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRootStore } from '../root'

const rootStore = useRootStore()

const isFilterVisible = ref(false) // Состояние видимости фильтра
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

onMounted(rootStore.getFilters)
</script>

<template>
  <div class="flex flex-col grow-0">
    <!-- Бургер-меню -->
    <div class="md:hidden">
      <button
        @click="isFilterVisible = !isFilterVisible"
        class="p-2 bg-gray-500 text-white rounded-md"
      >
        <span v-if="!isFilterVisible">Открыть фильтры</span>
        <span v-else>Закрыть фильтры</span>
      </button>
    </div>

    <div
      v-show="isFilterVisible || windowWidth >= 768"
      class="border-2 border-slate-300 bg-slate-200 mt-2"
    >
      <form @submit.prevent="rootStore.getItemsByFilters" class="border-2 border-slate-300">
        <div class="flex flex-col bg-slate-200">
          <div class="w-full">
            <span class="h-9 bg-slate-100 block m-auto text-center">Цена</span>

            <div class="flex justify-between items-center">
              <label
                class="flex items-center w-8 md:w-10 lg:w-20 2xl:w-32 h-10 border border-black border-solid rounded 2xl:px-2.5"
              >
                <span class="hidden xl:block">от</span>
                <input
                  type="number"
                  :min="rootStore.selectedMinPrice"
                  :max="rootStore.selectedMaxPrice"
                  :placeholder="rootStore.selectedMinPrice"
                  v-model="rootStore.selectedMinPrice"
                  class="bg-inherit md:px-2.5 outline-0 grow"
                />
              </label>
              <div class="grow-0"><span>-</span></div>
              <label
                class="flex items-center w-14 md:w-20 lg:w-30 2xl:w-32 h-10 border border-black border-solid rounded 2xl:px-2.5"
              >
                <span class="hidden xl:block">до</span>
                <input
                  type="number"
                  :min="rootStore.selectedMinPrice"
                  :max="rootStore.selectedMaxPrice"
                  :placeholder="rootStore.selectedMaxPrice"
                  v-model="rootStore.selectedMaxPrice"
                  class="bg-inherit md:px-2.5 outline-0 grow"
                />
              </label>
            </div>
          </div>
          <span class="h-9 bg-slate-100 text-center">Категории</span>
          <ul>
            <li v-for="category in rootStore.filters.categories" :key="category.name">
              <div class="md:pl-4 flex hover:bg-slate-300">
                <input
                  type="checkbox"
                  :id="category.name"
                  :value="category.id"
                  v-model="rootStore.selectedCategories"
                />
                <label class="md:pl-4 grow cursor-pointer" :for="category.name"
                  >{{ category.name }}
                </label>
              </div>
            </li>
          </ul>

          <span class="h-9 bg-slate-100 text-center">Размеры</span>
          <ul>
            <li v-for="size in rootStore.filters.sizes" :key="size.name">
              <div class="md:pl-4 flex hover:bg-slate-300">
                <input
                  type="checkbox"
                  :id="size.name"
                  :value="size.id"
                  v-model="rootStore.selectedSizes"
                />
                <label class="pl-4 grow cursor-pointer" :for="size.name">{{ size.name }}</label>
              </div>
            </li>
          </ul>

          <span class="h-9 bg-slate-100 text-center">Цвета</span>
          <ul>
            <li v-for="color in rootStore.filters.colors" :key="color.name">
              <div class="md:pl-4 flex hover:bg-slate-300">
                <input
                  type="checkbox"
                  :id="color.name"
                  :value="color.id"
                  v-model="rootStore.selectedColors"
                />
                <label class="pl-4 grow cursor-pointer" :for="color.name">{{ color.name }}</label>
              </div>
            </li>
          </ul>
        </div>
        <button
          type="submit"
          class="h-9 bg-slate-300 block m-auto w-full hover:bg-violet-600 hover:text-white rounded-md"
        >
          Применить
        </button>
        <button
          @click="rootStore.resetFilters"
          class="h-18 lg:h-9 bg-slate-400 block m-auto w-full hover:bg-violet-600 hover:text-white rounded-md"
        >
          Сбросить фильтры
        </button>
      </form>
    </div>
  </div>
</template>
