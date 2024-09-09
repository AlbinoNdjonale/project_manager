<script setup>
    import { onMounted, ref } from 'vue'
    import { useRouter, RouterLink } from 'vue-router'
    import { userStore } from '../stores/user'
    import { processingrequestStore } from '../stores/processingrequest'
    import composable from '../composable'
    import api from '../api'

    onMounted(() => composable.update_title('Login'))

    const userouter = useRouter()
    const userstore = userStore()

    const processingrequeststore = processingrequestStore()

    const email    = ref('')
    const password = ref('')
    const error = ref(false)

    const login = async e => {
        e.preventDefault()

        processingrequeststore.set(true)

        const user = await api.post(
            '/api/v1/auth/login',
            {
                email: email.value,
                password: password.value
            },
            false,
            () => processingrequeststore.set(false)
        )

        password.value = ''
        email.value    = ''
        
        if (user.id) {
            localStorage.setItem('user', JSON.stringify({
                id: user.id,
                token: user.token
            }))
            
            userstore.set(user)
            userouter.replace('/')
        } else {
            error.value = true
        }
    }
</script>

<template>
    <div id = "login">
        <form @submit = "login">
            <section class = "md">
                <h2>Entrar</h2>
            </section>

            <section class = 'error' :class = "error?'block-display':'none-display'">
                <small>
                    <em> verifica se digitou corretamente o email e a password. </em>
                </small>
            </section>

            <section class = "md">
                <label for="email">E-mail</label>
                <input v-model = "email" type="email" id="email" required>
            </section>

            <section class = "md">
                <label for="password">Palavra Passe</label>
                <input v-model = "password" type="password" id="password" required autocomplete = "current-password">

                <div>
                    <RouterLink to = "/auth/signup"><small>Ainda não tenho uma conta</small></RouterLink>
                </div>
            </section>

            <section>
                <button>Entrar</button>
            </section>
        </form>
    </div>
</template>
