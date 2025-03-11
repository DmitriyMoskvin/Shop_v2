import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

export const useRootStore = defineStore('rootStore', () => {
  // const URL = 'http://194.87.86.112/api/' //prod
  const URL = 'http://127.0.0.1:8000/api/' // dev

  const items = ref([]) // Товары
  const sections = ref([]) // Разделы/Секции
  const product = ref([]) // Определенный товар
  const filters = ref([]) // Фильтры

  const selectedCategories = ref([])
  const selectedSizes = ref([])
  const selectedColors = ref([])
  const selectedMinPrice = ref(0)
  const selectedMaxPrice = ref(100000)

  const route = useRoute()

  const getItems = async () => {
    items.value = []
    try {
      const { data } = await axios.get(`${URL}shop/products/`)
      items.value = data
    } catch (error) {
      console.log(error)
    }
  }

  const getSections = async () => {
    try {
      const { data } = await axios.get(`${URL}shop/sections/`)
      sections.value = data
    } catch (error) {
      console.log(error)
    }
  }

  const getItemsBySectionId = async (id) => {
    items.value = []
    try {
      const { data } = await axios.get(`${URL}shop/section/${id}/`)
      items.value = data
    } catch (error) {
      console.log(error)
    }
  }

  const getProductById = async (id) => {
    product.value = {}
    try {
      const { data } = await axios.get(`${URL}shop/product/${id}/`)
      product.value = data
    } catch (error) {
      console.log(error)
    }
  }

  const getFilters = async () => {
    try {
      const { data } = await axios.get(`${URL}shop/filters/`)
      filters.value = data
    } catch (error) {
      console.log(error)
    }
  }

  const getItemsByFilters = async () => {
    try {
      const params = {}

      if (selectedCategories.value.length > 0) {
        params.category = selectedCategories.value.join(',')
      }

      if (selectedSizes.value.length > 0) {
        params.size = selectedSizes.value.join(',')
      }

      if (selectedColors.value.length > 0) {
        params.colors = selectedColors.value.join(',')
      }

      if (selectedMinPrice.value) {
        params.price_per_unit_min = selectedMinPrice.value
      }

      if (selectedMaxPrice.value != 100000) {
        params.price_per_unit_max = selectedMaxPrice.value
      }

      const { data } = await axios.get(`${URL}shop/section/${route.params.id}/`, {
        params,
        paramsSerializer: {
          indexes: null
        }
      })

      items.value = data
    } catch (error) {
      console.log(error)
    }
  }

  const resetFilters = () => {
    selectedCategories.value = []
    selectedSizes.value = []
    selectedColors.value = []
    selectedMinPrice.value = 0
    selectedMaxPrice.value = 100000
  }

  return {
    URL,
    items,
    sections,
    product,
    filters,
    selectedCategories,
    selectedSizes,
    selectedColors,
    selectedMinPrice,
    selectedMaxPrice,

    getItems,
    getSections,
    getItemsBySectionId,
    getProductById,
    getFilters,
    getItemsByFilters,
    resetFilters
  }
})
