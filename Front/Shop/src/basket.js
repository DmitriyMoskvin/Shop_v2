import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useBasketStore = defineStore('basketStore', () => {
  const quantityOfGoods = ref(0)
  const getQuantityOfGoods = () => {
    const basketItemsInLocalStorage = localStorage.getItem('basketProducts')
    if (basketItemsInLocalStorage) {
      const basketItems = JSON.parse(basketItemsInLocalStorage)
      return basketItems.reduce((total, item) => total + item.quantity, 0)
    }
    return 0
  }

  // Загрузка товаров если они уже есть в localStorage
  const loadBasketFromLocalStorage = (basketProducts) => {
    const basketItemsInLocalStorage = localStorage.getItem('basketProducts')
    if (basketItemsInLocalStorage) {
      basketProducts.value = JSON.parse(basketItemsInLocalStorage)
    }
  }

  return {
    quantityOfGoods,
    loadBasketFromLocalStorage,
    getQuantityOfGoods
  }
})
