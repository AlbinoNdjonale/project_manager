<script setup>
    import { onMounted, ref, reactive, computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { userStore } from '../stores/user'
    import Header from '../components/Header.vue'
    import Footer from '../components/Footer.vue'
    import OnlyUser from '../components/OnlyUser.vue'
    import ManipulateProject from '../components/ManipulateProject.vue'
    import ConfirmOperation from '../components/ConfirmOperation.vue'
    import { processingrequestStore } from '../stores/processingrequest'
    import Detail from '../components/Detail.vue'
    import composable from '../composable'
    import api from '../api'

    const host = document.location.origin

    const userstore = userStore()
    const userouter = useRouter()

    const processingrequeststore = processingrequestStore()

    const props = defineProps({
        project_id: {
            type: String
        },
        link: {
            type: String
        },
        invite: {
            default: false
        }
    })

    const project      = ref({})
    const confirmdel   = ref(false)
    const notfound     = ref(false)
    const isediproject = ref(false)
    const isaddauthor  = ref(false)
    const iseditinvite = ref(false)
    const write        = ref(false)

    const confirmaddauthor = ref(false)
    const confirmdelauthor = ref(false)
    const author = reactive({
        id: '',
        name: '',
        email: '',
        gender: 'M',
        birth: '',
    })

    const details     = ref({})
    const sliceinvite = (start = '', end = '') => props.invite?`${start}invite/${props.link}${end}`:''

    onMounted(async () => {
        processingrequeststore.set(true)

        const findproject = await api.get(
            (
                props.invite?
                `/api/v1/projects/invite/${props.link}`:
                `/api/v1/projects/${props.project_id}`
            ),
            () => processingrequeststore.set(false)
        )

        if (findproject.id) {
            composable.update_title(findproject.title)
            project.value = findproject

            details.value = await api.get(`/api/v1/details${sliceinvite('/')}/${project.value.id}`)
        }
        else  notfound.value = true
    })

    const budgetcomputed = computed(() => {
        return composable.formatnumber(project.value.budget)
    })

    const editproject = async data => {
        processingrequeststore.set(true)

        const editproject = await api.update(
            (
                props.invite?
                `/api/v1/projects/invite/${props.link}`:
                `/api/v1/projects/${project.value.id}`
            ),
            data,
            false,
            () => processingrequeststore.set(false)
        )

        if (editproject.id) {
            project.value = editproject

            if (!props.invite)
                for (let index = 0; index < userstore.user.projects.length; index++) {
                    if (userstore.user.projects[index].id == project.value.id) {
                        userstore.user.projects[index] = project.value
                        break
                    }
                }

            isediproject.value = false
        } else {
            console.log(editproject)
        }
    }

    const deleteproject = async () => {
        confirmdel.value = false

        processingrequeststore.set(true)

        const del = await composable.deleteproject(project.value.id, () => processingrequeststore.set(false))

        if (del) {
            userouter.replace('/projects')
        }
    }

    const addauthor = async () => {
        confirmaddauthor.value = false

        processingrequeststore.set(true)

        const author_ = await api.post(
            `/api/v1/authors/${sliceinvite()}`, {
                name: author.name,
                email: author.email,
                gender: author.gender,
                birth: author.birth,
                project_id: project.value.id
            },
            false,
            () => processingrequeststore.set(false)
        )

        if (author_.id) {
            author_.gender = author_.gender.value
            project.value.authors.push(author_)

            author.name   = ''
            author.email  = ''
            author.gender = 'M'
            author.birth  = ''

            isaddauthor.value = false
        } else {
            console.log(author_)
        }
    }

    const showformaddauthor = e => {
        e.preventDefault()

        confirmaddauthor.value = true
    }

    const delauthor = async () => {
        confirmdelauthor.value = false

        processingrequeststore.set(true)

        const author_ = await api.delete(`/api/v1/authors${sliceinvite('/')}/${author.id}`, () => processingrequeststore.set(false))

        if (author_.id) {
            project.value.authors = project.value.authors.filter(item => item.id != author_.id)
        }
    }

    const add_detail = value => {
        let count = 1

        let newfield = 'novo campo'

        while (details.value[newfield] !== undefined) {
            newfield = `novo campo${count}`
            count++
        }

        details.value[newfield] = value
    }

    const update_details = (newdetails, _key) => {
        details.value = newdetails
    }

    const save_detail = async () => {
        processingrequeststore.set(true)

        details.value = await api.update(
            `/api/v1/details${sliceinvite('/')}/${project.value.id}`,
            details.value,
            false,
            () => processingrequeststore.set(false)
        )
    }

    const create_link = async e => {
        e.preventDefault()

        processingrequeststore.set(true)

        const link = await api.post(`/api/v1/links/`, {
            write: write.value,
            project_id: parseInt(props.project_id)
        }, false, () => processingrequeststore.set(false))

        if (link.id) {
            project.value.links.push(link)

            write.value = false
        } else
            console.log(link)
    }

    const remove_link = async linkid => {
        processingrequeststore.set(true)

        const link = await api.delete(`/api/v1/links/${linkid}`, () => processingrequeststore.set(false))

        if (link.id) {
            project.value.links = project.value.links.filter(item => linkid != item.id)
        } else
            console.log(link)
    }

    const update_link = async (linkid, write) => {
        processingrequeststore.set(true)

        const link = await api.update(`/api/v1/links/${linkid}`, {
            write
        }, false, () => processingrequeststore.set(false))

        if (link.id) {
            project.value.links = project.value.links.map(item => linkid != item.id?item:link)
        } else
            console.log(link)
    }
</script>

<template>
    <OnlyUser :ignore = 'invite'>
        <div v-if = "!notfound">
            <Header />

            <main v-if = "project.id">
                <section id = 'project-prophile' class = "card">
                    <h2>{{ project.title }}</h2>

                    <p id = 'description' class = "mb">
                        {{ project.description }}
                    </p>

                    <p class = "mb">
                        feito: <input type = "checkbox" disabled :checked = "project.is_completed">
                    </p>

                    <div id = 'info' class = "mb">
                        <span v-if = "project.started">Data: {{ project.started.day }}.{{ project.started.month }}.{{ project.started.year }}</span>
                        <span v-if = "project.budget">Orçamento: {{ budgetcomputed }}</span>
                    </div>

                    <div class = 'opitions'>
                        <button @click = "() => { confirmdel = !invite }" class = "btn-del">Deletar</button>
                        <button @click = "() => { isediproject = true }" class = "btn-edi">Editar</button>

                        <ConfirmOperation v-if = "confirmdel" :yes = "deleteproject" :not = "() => { confirmdel = false }" />
                        <ManipulateProject
                          v-if = "isediproject"
                          action = "Editar"
                          :event = "editproject"
                          :close = "() => { isediproject = false }"
                          :project = "project"/>
                    </div>
                </section>

                <section id = "authors">
                    <h2>Autores</h2>

                    <section>
                        <button @click = "() => {isaddauthor=true}" id = "add" class = "card"> + </button>

                        <div v-for = "author_ in project.authors" class = "card">
                            <h3 class = "mb1">{{ author_.name }}</h3>
                            <p class = "mb1">{{ author_.email }}</p>
                            <p class = "mb1">Nascimento: {{ author_.birth.day }}.{{ author_.birth.month }}.{{ author_.birth.year }}</p>
                            <p class = "mb1">genero: {{ author_.gender }}</p>

                            <div class = 'opitions'>
                                <button @click = "() => {confirmdelauthor = true; author.id = author_.id}" class = "btn-del">deletar</button>
                            </div>
                        </div>
                    </section>
                </section>

                <section id = "details">
                    <div>
                        <div class = 'wrapper'>
                            <button class = "btn-save-detail" @click = "save_detail">salvar</button>
                            <div id = 'opt'>
                                <button @click = "add_detail('valor')" class = "btn-add-detail">add</button>
                                <button @click = "add_detail([])" class = "btn-add-detail-list">add. lista</button>
                                <button @click = "add_detail({})" class = "btn-add-detail-super">super add</button>
                            </div>
                        </div>

                        <div id = "content">
                            <Detail :update = 'update_details' :details = 'details'/>
                        </div>
                    </div>
                </section>

                <section v-if = "!invite" id = 'invite'>
                    <button @click = "() => { iseditinvite = true }">convidar</button>
                </section>

                <section v-if = "iseditinvite" id = 'invite-form' class = "wp-dialog">
                    <dialog>
                        <div>
                            <div class = 'top'>
                                <h2>Gerenciamento de Links</h2>

                                <button @click = "() => { iseditinvite = false }" class = "btn-close"></button>
                            </div>
                            <form @submit = "create_link">
                                <section>
                                    <label for = "write">Permissão de escrita</label>
                                    <input v-model = "write" type = "checkbox">
                                </section>

                                <section>
                                    <button class = "btn-add">gerar link</button>
                                </section>
                            </form>
                            
                            <section id = "list-link">
                                <div v-for = "invite in project.links">
                                    <div>
                                        <div>
                                            <label for="">Permissão de escrita</label>
                                            <input v-model = "invite.write" type="checkbox">
                                        </div>

                                        <div>
                                            <small><button @click = "update_link(invite.id, invite.write)" class = "btn-add-detail">salvar</button></small>
                                            <small><button @click = "remove_link(invite.id)" class = "btn-rm">remover</button></small>
                                        </div>
                                    </div>
                                    <small><a :href = "`${host}/projects/invites/${invite.value}`" target = "blanck">{{ host }}/projects/invites/{{ invite.value }}</a></small>
                                </div>
                            </section>
                        </div>
                    </dialog>
                </section>

                <section v-if = "isaddauthor" class = "wp-dialog" id = "dialog-add-author">
                    <dialog>
                        <form @submit = "showformaddauthor">
                            <div class = 'top'>
                                <h2>Adicionar Autor</h2>

                                <button @click = "() => {isaddauthor=false}" type="button" class = "btn-close"></button>
                            </div>

                            <section>
                                <label for = "name">Nome</label>
                                <input type = "text" v-model = "author.name" id = "name" required>
                            </section>

                            <section>
                                <label for = "email">E-mail</label>
                                <input type = "email" v-model = "author.email" id = "email" required>
                            </section>

                            <section>
                                <label for = "birth">Data de Nascimento</label>
                                <input type = "date" v-model = "author.birth" id = "birth" required>
                            </section>

                            <section>
                                <label for = "gender">Genero</label>
                                <select id = "gender" v-model = "author.gender" required>
                                    <option value = "M">M</option>
                                    <option value = "F">F</option>
                                </select>
                            </section>

                            <section>
                                <button type="submit" class = 'btn-add'>confirmar</button>
                            </section>
                        </form>
                    </dialog>
                </section>

                <ConfirmOperation v-if = "confirmaddauthor" :yes = "addauthor" :not = "() => {confirmaddauthor = false}"/>
                <ConfirmOperation v-if = "confirmdelauthor" :yes = "delauthor" :not = "() => {confirmdelauthor = false}"/>
            </main>

            <Footer />
        </div>
        <div v-else>
            <h2>Pagina Não encontrada</h2>
        </div>
    </OnlyUser>
</template>
        
<style scoped>
    main {
        padding-top: 70px;
        min-height: 100vh;
    }

    h2 {
        margin-bottom: 15px;
    }

    .card {
        background: var(--color-3);
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, .1);
    }

    .mb {
        margin-bottom: 25px;
    }

    .mb1 {
        margin-bottom: 10px;
    }

    #project-prophile {
        width: 100%;
        max-width: 500px;
        margin: auto;
        margin-bottom: 20px;
        text-align: center;
    }

    #description {
        word-break: break-all;
    }

    #info span {
        padding: 7px;
        background: rgba(0, 0, 0, .2);
        border-radius: 5px;
        margin: 10px;
    }

    .opitions {
        text-align: left;
    }

    .opitions button {
        padding: 10px 18px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        color: var(--color-3);
        transition: transform .3s ease;
    }

    button:hover {
        transform: scale(1.1);
    }

    .opitions button:not(:last-child) {
        margin-right: 10px;
    }

    .btn-del {
        background: var(--color-2);
    }

    .btn-edi {
        background: var(--color-1);
    }

    #authors h2 {
        text-align: center;
    }

    #authors section {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: start;
        padding: 10px;
    }

    #authors > section > div {
        margin: 5px;
        flex: 1;
        max-width: 320px;
        text-align: center;
    }

    #add {
        border: none;
        cursor: pointer;
        font-size: 100px;
        flex: 1;
        background: transparent;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, .4);
        max-width: 320px;
        transition: transform 0.3s ease;
        margin: 5px;
    }

    #add:hover {
        transform: translateY(-5px);
    }

    .wp-dialog {
        position: fixed;
        display: flex;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        justify-content: center;
        align-items: center;
        z-index: 10;
    }

    .wp-dialog .top {
        display: flex;
        justify-content: space-between;
        align-items: start;
    }

    .wp-dialog h2 {
        margin-bottom: 15px;
    }

    .wp-dialog select, .wp-dialog input {
        padding: 7px;
        outline: none;
        border: 2px solid transparent;
        border-radius: 5px;
        margin-top: 2px;
    }

    .wp-dialog select:focus, .wp-dialog input:focus {
        border-color: var(--color-2);
    }

    .wp-dialog .btn-add {
        padding: 10px 18px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        background: var(--color-2);
        color: var(--color-3);
        transition: background 0.3s ease, transform 0.3s ease;;
    }

    .wp-dialog .btn-add:hover {
        background: var(--color-4);
        transform: scale(1.1);
    }

    .wp-dialog .btn-close {
        background: var(--color-2);
        border-radius: 50%;
        cursor: pointer;
        aspect-ratio: 1/1;
        width: 20px;
        border: none;
    }

    .wp-dialog dialog {
        display: block;
        background: transparent;
        margin: auto;
        border: none;
        width: 100%;
        max-width: 440px;
        padding: 10px;
    }

    .wp-dialog dialog > * {
        background: var(--color-1);
        color: var(--color-3);
        border-radius: 5px;
        padding: 20px;
    }

    .wp-dialog dialog form > section:not(:last-child) {
        margin-bottom: 10px;
        display: grid;
    }

    #details {
        padding: 20px;
    }

    #details > div {
        padding: 20px;
        background: var(--color-3);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
        border-radius: 5px;
    }

    #details > div > div#content {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        align-items: start;
    }

    .wrapper {
        display: flex;
        justify-content: space-between;
        margin-bottom: 7px;
    }

    .wrapper button {
        padding: 6px;
        border: none;
        cursor: pointer;
        border-radius: 5px;
        color: var(--color-3);
        transition: transform .3s ease;
    }

    #details div > div#opt button:not(:last-child) {
        margin-right: 10px;
    }

    .btn-rm {
        background: var(--color-2);
    }

    .btn-add-detail, .btn-save-detail {
        background: #0ac90a;
    }

    .btn-add-detail-list {
        background: #0a0ac9;
    }

    .btn-add-detail-super {
        background: #c9c90a;
    }

    #invite {
        padding: 10px;
        text-align: right;
    }

    #invite button {
        padding: 4px 12px;
        cursor: pointer;
        transition: transform .3s ease;
    }

    #invite-form dialog {
        display: block;
    }
    
    #list-link {
        display: grid;
        row-gap: 10px;
        margin-top: 20px;
        max-height: 205px;
        overflow-y: auto;
    }

    #list-link > div {
        background: var(--color-3);
        padding: 5px;
        border-radius: 5px;
    }

    #list-link > div > div {
        display: flex;
        justify-content: space-between;
        color: #111;
    }

    #list-link > div > div > div > *:not(:last-child) {
        margin-right: 10px;
    }

    #list-link button {
        padding: 4px 12px;
        cursor: pointer;
        transition: transform .3s ease;
        border: none;
        border-radius: 5px;
        color: var(--color-3);
    }

    #list-link a {
        word-break: break-all;
    }
</style>