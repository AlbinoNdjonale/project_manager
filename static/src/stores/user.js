import { ref } from 'vue'
import { defineStore } from 'pinia'

export const userStore = defineStore('user', () => {
    const user = ref({})
    
    const set = value => {
        user.value = value
    }

    const update = (key, value) => {
        user[key] = value
    }

    const _delete = () => {
        user[key] = value
    }

    return {
        user,
        set,
        update,
        delete: _delete
    }
})