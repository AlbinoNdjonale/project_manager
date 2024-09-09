<script setup>
    import { onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { storeToRefs } from 'pinia'

    import { userStore } from '../stores/user'

    const props = defineProps({
        ignore: {
            default: false
        }
    })

    const userouter = useRouter()
    const userstore = userStore()

    const user = storeToRefs(userstore).user

    onMounted(() => {
        if (!user.value.id && !props.ignore) userouter.replace('/auth/login')
    })
</script>

<template>
    <slot v-if = "user.id || ignore"></slot>    
</template>