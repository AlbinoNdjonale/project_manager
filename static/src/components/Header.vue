<script setup>
    import { ref } from 'vue'
    import { RouterLink, useRouter } from 'vue-router'
    import { storeToRefs } from 'pinia'
    import { userStore } from '../stores/user'
    import api from '../api'

    const userstore = userStore()
    const userouter = useRouter()

    const user = storeToRefs(userstore).user

    const dsmenu = ref('none')

    const logout = async e => {
        let out = await api.post(`/api/v1/auth/logout/${user.value.id}`)

        if (out.id ) {
            userstore.set({})
            localStorage.removeItem('user')
            userouter.replace('/')
        }
    }
</script>

<template>
    <header>
        <div>
            <div class = "container">
                <RouterLink to = "/">
                    <h1>Gestor <span>de Projetos</span></h1>
                </RouterLink>

                <nav  id = "nav-desktop">
                    <ul>
                        <li><RouterLink to = "/">Home</RouterLink></li>
                        <li><RouterLink to = "/projects">Projetos</RouterLink></li>
                        <li>
                            <RouterLink v-if = "user.id" id = 'me' to = '/auth/login'> {{ user.name }} </RouterLink>
                            <RouterLink v-else id = 'me' to = '/auth/login'>Login</RouterLink>
                        </li>
                        <li v-if = "user.id" id = "logout">
                            <button @click = "logout"> -> </button>
                            <div>Logout</div>
                        </li>
                    </ul>
                </nav>

                <nav id = "nav-mobile">
                    <button @click = "() => dsmenu = dsmenu=='grid'?'none':'grid'" id = "me">menu</button>
  
                    <nav :style = '{display: dsmenu}'>
                        <RouterLink to = "/">Home</RouterLink>
                        <RouterLink to = "/projects">Projetos</RouterLink>
                        <RouterLink v-if = "user.id" to = '/auth/login'> {{ user.name }} </RouterLink>
                        <RouterLink v-else to = '/auth/login'>Login</RouterLink>
                        <RouterLink v-if = "user.id" @click = "logout" to = "/">logout</RouterLink>
                    </nav>
                </nav>
            </div>
        </div>
    </header>
</template>
    
<style scoped>
    header {
        position: fixed;
        width: 100%;
        max-width: 1700px;
        z-index: 3;
    }

    header > div {
        background: var(--color-1);
        color: var(--color-3);
        max-width: 1700px;
    }

    header > div > div {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 7px 10px;
        margin: auto;
    }

    li {
        list-style: none;
    }

    #nav-desktop li {
        display: inline-block;
    }

    #nav-desktop li:not(:last-child) {
        margin-right: 23px;
    }

    #me {
        background: var(--color-2);
        padding: 6px 20px;
        border-radius: 1rem;
        border: none;
        cursor: pointer;
        color: var(--color-3);
    }

    a {
        color: var(--color-3);
        text-decoration: none;
    }

    #logout > button {
        padding: 5px;
        cursor: pointer;
        color: var(--color-2);
        border: 1px solid var(--color-2);
        background: transparent;
        font-family: monospace;
        border-radius: .4rem;
    }

    #logout > div {
        background: var(--color-3);
        color: var(--color-1);
        position: absolute;
        padding: 6px;
        border-radius: .3rem;
        margin-top: 1px;
        display: none;
    }

    #logout:hover > div {
        display: block;
    }

    #nav-mobile {
        display: none;
    }

    #nav-mobile button {
        width: 150px;
    }

    #nav-mobile > nav {
        background: var(--color-2);
        border-radius: 5px;
        overflow: hidden;
        margin-top: 10px;
        position: absolute;
    }

    #nav-mobile > nav a {
        padding: 7px 10px;
        transition: 0.3s ease;
    }

    #nav-mobile > nav a:hover {
        background: var(--color-4);
    }

    @media screen and (max-width: 671px) {
        #nav-desktop {
            display: none;
        }

        #nav-mobile {
            display: block;
        }
    }

    @media screen and (max-width: 480px) {
        h1 span {
            display: none;
        }
    }
</style>