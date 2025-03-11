<script setup>
import { RouterView } from 'vue-router'

import Header from './components/Header.vue'

import Footer from './components/Footer.vue'
</script>

<template>
  <div class="wrapper">
    <Header />
    <body class="bg-[#e3e8eb] pt-5">
      <div class="p-5 xl:w-4/5 xl:m-auto pt-45 pt-40">
        <RouterView />
      </div>
    </body>
    <Footer />
  </div>
</template>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type='number'] {
  -moz-appearance: textfield;
}

body {
  margin: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1;
}

footer {
  flex-shrink: 0;
}
</style>
