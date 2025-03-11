<script setup>
import { onMounted, ref, watch, computed } from 'vue'
import { useBasketStore } from '../basket'
import { useRootStore } from '../root'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Inputmask from 'inputmask'

const basketStore = useBasketStore()
const RootStore = useRootStore()
const basketProducts = ref([])

const router = useRouter()

const name = ref('')
const phone = ref('')
const address = ref('')
const comment = ref('')

const nameError = ref('')
const phoneError = ref('')

const totalPrice = computed(() => {
  let totalPrice = 0
  for (let product of basketProducts.value) {
    totalPrice += product.quantity * product.price
  }
  return totalPrice
})

const onChangeQuantity = (event, index) => {
  if (Number(event.target.value) < 1) {
    basketProducts.value.splice(index, 1)
  } else if (Number(event.target.value) > 99) {
    basketProducts.value[index].quantity = 99
  } else {
    basketProducts.value[index].quantity = Number(event.target.value)
  }
}

const minusQuantity = (index) => {
  let quantity = basketProducts.value[index].quantity

  if (quantity - 1 < 1) {
    basketProducts.value.splice(index, 1)
  } else {
    basketProducts.value[index].quantity -= 1
  }
}

const addQuantity = (index) => {
  let quantity = basketProducts.value[index].quantity

  if (quantity + 1 > 99) {
    basketProducts.value[index].quantity = 99
  } else {
    basketProducts.value[index].quantity += 1
  }
}

const removeProduct = (index) => {
  basketProducts.value.splice(index, 1)
}

function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}
const csrfToken = getCookie('csrftoken')

const placeAnOrder = async () => {
  try {
    if (!validateName(name.value).isValid) {
      throw 'nameIsNotValid'
    }
    if (!validatePhone(phone.value).isValid) {
      throw 'phoneIsNotValid'
    }

    await axios
      .post(
        `${RootStore.URL}basket/Orders/`,
        {
          Items: basketProducts.value,
          Customer: {
            Name: name.value,
            Phone: phone.value,
            Address: address.value,
            Comment: comment.value
          },
          TotalPrice: totalPrice.value
        },
        {
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          }
        }
      )
      .then(() => {
        router.push('OrderAccepted')
        basketProducts.value = []
      })
  } catch (error) {
    console.log(error)
    if (error == 'nameIsNotValid') {
      nameError.value = validateName(name.value).message
    }
    if (error == 'phoneIsNotValid') {
      phoneError.value = validatePhone(name.value).message
    }
  }
}

watch(
  basketProducts,
  (newItems) => {
    localStorage.setItem('basketProducts', JSON.stringify(newItems))
    basketStore.quantityOfGoods = basketStore.getQuantityOfGoods() // Обновление количества товаров в корзине
  },
  { deep: true }
)

// Маска телефона и валидация
const validateName = (name) => {
  const namePattern = /^[a-zA-Zа-яА-ЯёЁ\s-]+$/
  if (!name || name.length < 2 || name.length > 50) {
    return { isValid: false, message: 'Имя должно содержать от 2 до 50 символов.' }
  }
  if (!namePattern.test(name)) {
    return { isValid: false, message: 'Имя должно содержать только буквы, пробелы и дефисы.' }
  }
  return { isValid: true, message: '' }
}

const validatePhone = (phone) => {
  const phonePattern = /^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$/
  if (!phonePattern.test(phone)) {
    return { isValid: false, message: 'Телефон должен быть в формате +7 (XXX) XXX-XX-XX.' }
  }
  return { isValid: true, message: '' }
}

// Слежение за изменением имени и телефона
watch(name, (newValue) => {
  const validation = validateName(newValue)
  nameError.value = validation.isValid ? '' : validation.message
})

watch(phone, (newValue) => {
  const validation = validatePhone(newValue)
  phoneError.value = validation.isValid ? '' : validation.message
})

// Инициализация маски телефона при монтировании компонента
onMounted(() => {
  const phoneInput = document.getElementById('phone')
  const im = new Inputmask('+7 (999) 999-99-99')
  im.mask(phoneInput)

  // Загрузка корзины из локального хранилища при монтировании
  basketStore.loadBasketFromLocalStorage(basketProducts)
})
</script>

<template>
  <div>
    <h2 class="text-3xl font-bold mb-8">Корзина</h2>

    <div class="flex flex-col md:flex-row justify-between items-center bg-white py-7 px-12 mb-8">
      <div class="flex items-center gap-4">
        <img src="/success.JPG?url" alt="success" class="size-14 rounded-full" />
        <span class="text-lg">Оформление заказа</span>
      </div>
      <span class="text-2xl text-[#56593D]"
        >{{ totalPrice.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') }} тг</span
      >
    </div>

    <div>
      <h5>Товаров в корзине: {{ basketStore.quantityOfGoods }}</h5>
    </div>

    <div class="bg-white mb-8">
      <div
        v-for="(product, index) in basketProducts"
        :key="product.id"
        class="grid grid-cols-1 md:grid-cols-7 gap-5 items-center"
      >
        <RouterLink
          :to="`/product/${product.id}`"
          class="cursor-pointer hover:shadow-xl hover:-translate-y-2 transition rounded-2xl"
          ><div class="m-4"><img :src="product.photo" class="rounded-2xl" alt="" /></div
        ></RouterLink>
        <div class="w-auto md:w-10 text-2xl text-center">{{ product.name }}</div>
        <div class="w-auto md:w-10 text-2xl text-center">{{ product.price }} тг</div>
        <div class="w-auto md:w-10 text-2xl text-center">{{ product.color.name }}</div>
        <div class="w-auto md:w-10 text-2xl text-center">{{ product.size.name }}</div>
        <div class="flex items-center justify-center">
          <input
            type="button"
            value="-"
            @click="minusQuantity(index)"
            class="p-2 px-2 mx-4 hover:bg-violet-600 active:bg-violet-900 w-10 text-center rounded-lg bg-violet-300"
          />

          <input
            @change="(event) => onChangeQuantity(event, index)"
            type="number"
            inputmode="numeric"
            :value="product.quantity"
            min="1"
            pattern="[0-9]"
            class="w-10 text-4xl text-center"
          />

          <input
            type="button"
            value="+"
            @click="addQuantity(index)"
            class="p-2 px-2 mx-4 hover:bg-violet-600 active:bg-violet-900 w-10 text-center rounded-lg bg-violet-300"
          />
        </div>
        <div class="flex items-center justify-center">
          <button
            @click="removeProduct(index)"
            class="w-auto md:w-24 h-10 border-solid border-2 rounded-lg hover:bg-violet-600 active:bg-violet-900 text-center bg-violet-300"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>

    <div class="mb-8">
      <form action="">
        <h5 class="py-7 px-12 bg-white text-2xl bg-[#f2f5f7]">Оформление заказа</h5>
        <div class="py-7 px-12 bg-white text-lg text-[#56593D] flex flex-col">
          <label for="name">Имя</label>
          <input
            v-model="name"
            type="text"
            name="name"
            id="name"
            required
            class="border border-solid h-12 text-black"
          />
          <span v-if="nameError" class="text-red-600">{{ nameError }}</span>

          <label for="phone">Номер телефона</label>
          <input
            v-model="phone"
            type="tel"
            name="phone"
            id="phone"
            required
            placeholder="+7 (___) ___-__-__"
            maxlength="18"
            class="tel border border-solid h-12 text-black"
          />
          <span v-if="phoneError" class="text-red-600">{{ phoneError }}</span>

          <label for="address">Адрес</label>
          <input
            v-model="address"
            type="text"
            name="address"
            id="address"
            required
            class="border border-solid h-12 text-black"
          />

          <label for="comment">Коментарии к заказу</label>
          <textarea
            v-model="comment"
            name="comment"
            id="comment"
            cols="30"
            rows="10"
            class="border border-solid h-12 text-black"
          ></textarea>
        </div>
      </form>
    </div>

    <div>
      <h5 class="py-7 px-12 bg-white text-xl">Ваш заказ</h5>
      <div class="pt-7 px-12 pb-1.5 bg-white flex justify-between items-center">
        <h6 class="text-[#56593D]">Товаров на:</h6>
        <div class="grow border-b border-dashed border-[#56593D] mt-3 mx-2"></div>
        <span class="text-[#56593D]"
          >{{ totalPrice.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') }} тг</span
        >
      </div>
      <div class="pt-7 px-12 pb-6 bg-white flex justify-between items-center">
        <h6 class="text-[#56593D]">Доставка:</h6>
        <div class="grow border-b border-dashed border-[#56593D] mt-3 mx-2"></div>
        <span class="text-[#56593D]">0 тг</span>
      </div>
      <div class="py-7 px-12 border-t bg-white flex justify-between items-center">
        <span>Итоговая цена</span>
        <span>{{ totalPrice.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ') }} тг</span>
      </div>
      <div class="bg-[#ff0000] font-bold flex">
        <button @click="placeAnOrder" class="py-3.5 px-12 text-white text-center grow">
          Оформить заказ
        </button>
      </div>
    </div>
  </div>
</template>
