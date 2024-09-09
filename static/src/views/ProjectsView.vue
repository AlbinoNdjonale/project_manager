<script setup>
    import { onMounted, ref, computed } from 'vue'
    import { storeToRefs } from 'pinia'
    import { userStore } from '../stores/user'
    import { processingrequestStore } from '../stores/processingrequest'
    import api from '../api'

    import Header from '../components/Header.vue'
    import Footer from '../components/Footer.vue'
    import OnlyUser from '../components/OnlyUser.vue'
    import CardProject from '../components/CardProject.vue'
    import ManipulateProject from '../components/ManipulateProject.vue'
    import composable from '../composable'
    
    const isaddproject = ref(false)
    const userstore    = userStore()
    const user         = storeToRefs(userstore).user

    const processingrequeststore = processingrequestStore()

    onMounted(() => composable.update_title('Projects'))

    const budgettotal = computed(() => {
        let total = 0

        for (const project of user.value.projects) {
            if (project.budget) total += project.budget
        }

        return composable.formatnumber(total)
    })

    const addproject = async data => {
        processingrequeststore.set(true)

        const project = await api.post(
            '/api/v1/projects/',
            data,
            false,
            () => processingrequeststore.set(false)
        )

        if (project.id) {
            user.value.projects.push(project)

            isaddproject.value = false
        } else {
            console.log(project)
        }
    }
</script>

<template>
    <Header />

    <main>
        <OnlyUser>
            <div v-if = "user.projects.length">
                <section id = "tools">
                    <h2 id = "projects-title">Projetos</h2>

                    <div>
                        <div>Numero de projetos: {{ user.projects.length }}</div>
                        <div>Orçamento Total: {{ budgettotal }}</div>
                    </div>
                </section>

                <section id = 'projects'>
                    <button @click = "() => {isaddproject=true}" class = 'add'> + </button>

                    <CardProject
                    v-for = "project in user.projects"
                    :id = "project.id"
                    :title = "project.title"
                    :description = "project.description"
                    :date = "project.started"
                    :budget = "project.budget"
                    :is_completed = "project.is_completed"
                    />
                </section>
            </div>

            <section id = 'add' v-else>
                <button @click = "() => {isaddproject=true}" class = 'add'> + </button>
            </section>

            <ManipulateProject
              v-if = "isaddproject"
              action = "Adicionar"
              :event = "addproject"
              :close = "() => {isaddproject=false}"
              />
        </OnlyUser>
    </main>

    <Footer />
</template>
        
<style scoped>
    main {
        padding-top: 51px;
        min-height: 100vh;
    }

    #tools {
        background: var(--color-3);
        padding: 2px;
        position: fixed;
        width: 100%;
        z-index: 2;
        box-shadow: 0 0 10px rgba(0, 0, 0, .1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
    }

    #tools > div {
        display: flex;
    }

    #tools > div > div {
        background: rgba(0, 0, 0, .1);
        padding: 5px;
        border-radius: 6px;
    }

    #tools div:not(:last-child) {
        margin-right: 10px;
    }

    #add {
        position: fixed;
        width: 100%;
        height: 100vh;
        top: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    #projects {
        display: flex;
        align-items: start;
        padding: 10px;
        flex-wrap: wrap;
        padding-top: 60px;
    }

    .add {
        flex: 1 1 300px;
        margin: 10px;
        padding: 20px;
        border-radius: 5px;
        border: none;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, .4);
        cursor: pointer;
        transition: transform 0.3s ease;
        font-size: 100px;
        max-width: 300px;
        width: 100%;
    }

    .add:hover {
        transform: translateY(-5px);
    }

    #add .add {
        aspect-ratio: 1/1;
    }

    @media screen and (max-width: 674px) {
        .add {
            margin: 10px auto;
        }
    }

    @media screen and (max-width: 469px) {
        h2#projects-title {
            display: none;
        }
    }
</style>