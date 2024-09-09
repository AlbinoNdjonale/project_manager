import { ref } from 'vue'
import { defineStore } from 'pinia'

export const processingStore = defineStore('processing', () => {
    const processing = ref(true)
    
    const set = value => {
        processing.value = value
    }

    return {
        processing,
        set
    }
})