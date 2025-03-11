<script setup>
import ItemDoesNotExist from '../components/ItemDoesNotExist.vue'
import { ref, watch, onMounted } from 'vue'
import { useRootStore } from '../root'
import { useBasketStore } from '../basket'
import axios from 'axios'

const rootStore = useRootStore()
const basketStore = useBasketStore()

const basketProducts = ref([])

const quantity = ref(1)
// const selectedColor = ref(null)
// const selectedSize = ref(null)

const selectedColor = ref({
  id: null,
  name: ''
})
const selectedSize = ref({
  id: null,
  name: ''
})

let isOpacityNone = ref(false)

let itemDoesNotExist = ref(false)

const props = defineProps({
  id: String
})

const onChangeQuantity = (event) => {
  quantity.value = Number(event.target.value)
}

const minusQuantity = () => {
  quantity.value = quantity.value - 1
}

const addQuantity = () => {
  quantity.value = quantity.value + 1
}

const addToBasket = () => {
  // Сбор данных, которые выбрал клиент
  const newBasketProduct = {
    id: rootStore.product.id,
    name: rootStore.product.name,
    price: rootStore.product.price_per_unit,
    photo: rootStore.product.photo,
    color: selectedColor.value,
    size: selectedSize.value,
    quantity: quantity.value
  }

  // Проверка на наличие товара в корзине
  const existingItem = basketProducts.value.find(
    (item) =>
      item.id === newBasketProduct.id &&
      item.color.id === newBasketProduct.color.id &&
      item.size.id === newBasketProduct.size.id
  )

  if (existingItem) {
    existingItem.quantity += newBasketProduct.quantity
    quantity.value = 1
  } else {
    basketProducts.value.push(newBasketProduct)
    quantity.value = 1
  }
}

onMounted(() => {
  rootStore.getProductById(props.id).then(() => {
    if (rootStore.product.colors.length > 0) {
      //начальное значение для радиокнопки цвета
      selectedColor.value.id = rootStore.product.colors[rootStore.product.colors.length - 1].id
      selectedColor.value.name = rootStore.product.colors[rootStore.product.colors.length - 1].name
    }
    if (rootStore.product.size.length > 0) {
      //начальное значение для радиокнопки размера
      selectedSize.value.id = rootStore.product.size[rootStore.product.size.length - 1].id
      selectedSize.value.name = rootStore.product.size[rootStore.product.size.length - 1].name
    }
    checkSelectedFilters()
  })
})

onMounted(() => {
  basketStore.loadBasketFromLocalStorage(basketProducts)
})

watch(quantity, () => {
  if (quantity.value < 1) {
    quantity.value = 1
  }
  if (quantity.value > 99) {
    quantity.value = 99
  }
})

watch(
  basketProducts,
  (newItems) => {
    localStorage.setItem('basketProducts', JSON.stringify(newItems))
    basketStore.quantityOfGoods = basketStore.getQuantityOfGoods() // Обновление количества товаров в корзине
  },
  { deep: true }
)

// Блок код проверки наличия такого товара в зависимости от фильтров и активация диактивация кнопки
const checkSelectedFilters = async () => {
  try {
    await axios.get(`${rootStore.URL}shop/item/${props.id}/`, {
      params: { color: selectedColor.value.id, size: selectedSize.value.id },
      paramsSerializer: {
        indexes: null
      }
    })
    // Если запрос успешен (код 200), делаем кнопку активной
    enableButton()
    itemDoesNotExist.value = false
  } catch (error) {
    if (error.response && error.response.status === 404) {
      // Если пришла ошибка 404, делаем кнопку неактивной
      disableButton()
      itemDoesNotExist.value = true // Показать шаблон отсутсвия товара на складе
    } else {
      console.log(error)
    }
  }
}

// Функция для деактивации кнопки
const disableButton = () => {
  const button = document.getElementById('submitButton')
  if (button) {
    button.disabled = true
    button.classList.remove('bg-black')
    button.classList.remove('hover:bg-violet-600')
    button.classList.remove('active:bg-black')
    button.classList.add('bg-slate-300') // Добавляем класс для визуального эффекта
  }
}

// Функция для активации кнопки
const enableButton = () => {
  const button = document.getElementById('submitButton')
  if (button) {
    button.disabled = false
    button.classList.remove('bg-slate-300')
    button.classList.add('bg-black')
    button.classList.add('hover:bg-violet-600')
    button.classList.add('active:bg-black')
  }
}

//конец верхнего блока

function zoom(e) {
  const zoomer = e.currentTarget
  let offsetX, offsetY, x, y

  if (e.offsetX) {
    offsetX = e.offsetX
  } else {
    offsetX = e.touches[0].pageX
  }

  if (e.offsetY) {
    offsetY = e.offsetY
  } else {
    offsetY = e.touches[0].pageY
  }

  x = (offsetX / zoomer.offsetWidth) * 100
  y = (offsetY / zoomer.offsetHeight) * 100

  zoomer.style.backgroundPosition = `${x}% ${y}%`

  if (x > 98 || y > 98 || x < 2 || y < 2) {
    isOpacityNone.value = false
  }
}
function toggleOpacity() {
  isOpacityNone.value = !isOpacityNone.value
}
</script>

<template>
  <div>
    <div v-if="rootStore.product">
      <div class="bg-white">
        <div class="p-4 flex flex-col md:flex-row">
          <div class="flex-[0_0_80%] grid md:grid-cols-4 gap-5">
            <div class="md:col-span-2">
              <div
                class="zoom"
                @mousemove="zoom"
                :style="{ backgroundImage: `url(${rootStore.product.photo})` }"
              >
                <img
                  :src="rootStore.product.photo"
                  @click="toggleOpacity"
                  :class="{ 'opacity-none': isOpacityNone }"
                />
              </div>
            </div>
            <div v-for="image in rootStore.product.images" :key="image.id" class="col-span-2">
              <div
                class="zoom"
                @mousemove="zoom"
                :style="{ backgroundImage: `url(${image.image})` }"
              >
                <img
                  :src="image.image"
                  @click="toggleOpacity"
                  :class="{ 'opacity-none': isOpacityNone }"
                />
              </div>
            </div>
          </div>
          <div class="flex-[0_0_20%] p-4">
            <div>
              <span class="text-xl font-medium">{{ rootStore.product.name }}</span>
            </div>
            <div>
              <span class="text-slate-400">{{ rootStore.product.category?.name }}</span>
            </div>
            <div class="pt-4 text-lg font-normal">
              <span>{{ rootStore.product.price_per_unit }} т</span>
            </div>

            <div class="flex gap-4 text-lg">
              <div>
                <span>Цвет:</span>
              </div>
              <div class="flex justify-around items-center gap-4">
                <div class="flex" v-for="color in rootStore.product.colors" :key="color.name">
                  <div>
                    <input
                      type="radio"
                      :id="color.name"
                      :value="color.id"
                      @change="checkSelectedFilters"
                      name="color"
                      class="form_radio px-1 appearance-none"
                      v-model="selectedColor.id"
                    />
                    <label class="px-1 grow cursor-pointer" :for="color.name"
                      >{{ color.name }}
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <div class="flex gap-4 text-lg">
              <div>
                <span>Размеры:</span>
              </div>
              <div class="flex justify-around items-center gap-4">
                <div v-for="size in rootStore.product.size" :key="size.name">
                  <div>
                    <input
                      type="radio"
                      :id="size.name"
                      :value="size.id"
                      @change="checkSelectedFilters"
                      name="size"
                      class="form_radio px-1 appearance-none"
                      v-model="selectedSize.id"
                    />
                    <label class="px-1 grow cursor-pointer" :for="size.name"
                      >{{ size.name }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <div class="flex flex-col text-lg text-2xl font-bold">
                <div class="mt-2">
                  <span>Количество:</span>
                  <div class="flex items-center justify-center">
                    <input
                      type="button"
                      value="-"
                      @click="minusQuantity"
                      class="p-2 px-2 mx-4 hover:bg-violet-600 active:bg-violet-900 w-10 text-center rounded-lg bg-violet-300"
                    />

                    <input
                      @change="onChangeQuantity"
                      type="number"
                      inputmode="numeric"
                      :value="quantity"
                      min="1"
                      pattern="[0-9]"
                      class="w-10 text-4xl text-center"
                    />

                    <input
                      type="button"
                      value="+"
                      @click="addQuantity"
                      class="p-2 px-2 mx-4 hover:bg-violet-600 active:bg-violet-900 w-10 text-center rounded-lg bg-violet-300"
                    />
                  </div>
                </div>

                <button
                  id="submitButton"
                  class="h-12 mt-2 text-white bg-black text-base w-full rounded-md hover:bg-violet-600 active:bg-black"
                  @click="addToBasket"
                >
                  В корзину
                </button>
                <div v-if="itemDoesNotExist">
                  <ItemDoesNotExist />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="p-4">
          <span class="text-xl font-medium">О товаре:</span>
          <div>
            <span>Описание: {{ rootStore.product.description }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<style>
.form_radio:checked + label {
  border-radius: 1rem;
  background-color: rgb(226 232 240);
  color: black;
}

.form_radio:hover + label {
  border-radius: 1rem;
  background-color: rgb(71 85 105);
  color: white;
}

.form_radio:active + label {
  border-radius: 1rem;
  background-color: rgb(226 232 240);
  color: black;
}

.zoom {
  display: inline-block;
  background-size: 300%; /* Масштаб увеличения */
}
.zoom img {
  display: block;
  width: 600px;
}
.opacity-none {
  opacity: 0;
}
</style>
