import { ref } from 'vue'
import { defineStore } from 'pinia'

export const processingrequestStore = defineStore('processingrequest', () => {
    const processingrequest = ref(false)
    
    const set = value => {
        processingrequest.value = value
    }

    return {
        processingrequest,
        set
    }
})