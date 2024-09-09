<script setup>
    import { onMounted, ref } from 'vue'
    import { useRouter, RouterLink } from 'vue-router'
    import { processingrequestStore } from '../stores/processingrequest'
    import composable from '../composable'
    import api from '../api'

    onMounted(() => composable.update_title('Signup'))

    const userouter = useRouter()

    const name      = ref('')
    const email     = ref('')
    const password1 = ref('')
    const password2 = ref('')

    const error = ref(false)
    const errorpass = ref(false)

    const processingrequeststore = processingrequestStore()

    const signup = async e => {
        e.preventDefault()

        if (password1.value.trim() !== password2.value.trim()) {
            errorpass.value = true
            return   
        }

        processingrequeststore.set(true)

        const user = await api.post(
            '/api/v1/users/',
            {
                name    : name.value,
                email   : email.value,
                password: password1.value,
                is_admin: false
            },
            false,
            () => processingrequeststore.set(false)
        )

        if (user.id) {
            name.value      = ''
            email.value     = ''
            password1.value = ''
            password2.value = ''

            userouter.replace('/auth/login')
        } else {
            error.value = true
            console.log(user)
        }
    }
</script>

<template>
    <div id = "signup">
        <form @submit = "signup">
            <section class = "md">
                <h2>Registrar</h2>
            </section>

            <section class = 'error' :class = "error?'block-display':'none-display'">
                <small>
                    <em> verifica se digitou corretamente todos os campos. </em>
                </small>
            </section>

            <section class = 'error' :class = "errorpass?'block-display':'none-display'">
                <small>
                    <em> as palavras passe são diferente. </em>
                </small>
            </section>

            <section class = "md">
                <label for="username">Name</label>
                <input v-model = "name" type="name" id="name" required>
            </section>

            <section class = "md">
                <label for="email">E-mail</label>
                <input v-model = "email" type="email" id="email" required>
            </section>

            <section class = "md">
                <label for="password1">Palavra passe</label>
                <input v-model = "password1" type="password" id="password1" required autocomplete = "new-password">
            </section>

            <section class = "md">
                <label for = "password2">Confirma a Palavra passe</label>
                <input v-model = "password2" type="password" id="password2" required autocomplete = "new-password">
            
                <div>
                    <RouterLink to = "/auth/login"><small>Ja tenho uma conta</small></RouterLink>
                </div>
            </section>

            <section>
                <button>Registrar</button>
            </section>
        </form>
    </div>
</template>
