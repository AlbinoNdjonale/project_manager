<script setup>
  import { onMounted } from 'vue'
  import { RouterView } from 'vue-router'
  import { storeToRefs } from 'pinia'
  import { userStore } from './stores/user'
  import { processingStore } from './stores/processing'
  import { processingrequestStore } from './stores/processingrequest'
  import api from './api'

  const processingstore = processingStore()
  const processingrequeststore = processingrequestStore()

  const userstore = userStore()

  const processing = storeToRefs(processingstore).processing
  const processingrequest = storeToRefs(processingrequeststore).processingrequest

  onMounted(async () => {
    let user = localStorage.getItem('user')

    if (user) {
      user = JSON.parse(user)

      if (user.id) {
        user = await api.get(`/api/v1/users/${user.id}`)

        if (user.id) {
          userstore.set(user)
        } else {
          localStorage.removeItem('user')
        }
      }
    }
    
    processingstore.set(false)
  })
</script>

<template>
  <div v-if = "processingrequest">
    <h2>AGUARDE . . .</h2>
  </div>
  <RouterView v-if = "!processing" />
  <div v-else>
    <h2>AGUARDE . . .</h2>
  </div>
</template>

<style scoped>
  div {
    position: fixed;
    z-index: 30;
    width: 100%;
    height: 100vh;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  h2 {
    background: var(--color-1);
    color: var(--color-2);
    padding: 10px;
    text-align: center;
    border-radius: 5px;
    border: 2px solid var(--color-2);
  }
</style>
