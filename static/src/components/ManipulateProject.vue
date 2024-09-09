<script setup>
    import { ref } from 'vue'
    import { userStore } from '../stores/user'
    import ConfirmOperation from '../components/ConfirmOperation.vue'

    const props = defineProps({
        close: {
            required: true,
            type: Function
        },
        event: {
            required: true,
            type: Function
        },
        project: {
            default: {}
        },
        action: {
            required: true,
            type: String
        }

    })

    const userstore    = userStore()

    const title        = ref(props.project.title?props.project.title:'')
    const description  = ref(props.project.description?props.project.description:'')
    const started      = ref(props.project.started?`${props.project.started.year}-${props.project.started.month<10?0:''}${props.project.started.month}-${props.project.started.day<10?0:''}${props.project.started.day}`:'')
    const budget       = ref(props.project.budget?props.project.budget:'')
    const is_completed = ref(props.project.is_completed?props.project.is_completed:null)

    const confirmadd = ref(false)

    const click = async () => {
        confirmadd.value = false

        const data = {
            title: title.value.trim()==''?null:title.value.trim(),
            description: description.value.trim()==''?null:description.value.trim(),
            admin_id: userstore.user.id,
            started: started.value==''?null:started.value,
            budget: budget.value==''?null:parseFloat(budget.value)
        }

        if (is_completed.value != null)
            data.is_completed = is_completed.value
        
        await props.event(data)
    }
</script>

<template>
    <section id = 'dialog-add-project'>
        <dialog>
            <form @submit = "e => { e.preventDefault(); confirmadd = true }">
                <div id = 'top'>
                    <h2>{{ action }} Projecto</h2>

                    <button type="button" @click = "() => {close()}" id = 'btn-close'></button>
                </div>

                <section>
                    <label for = "title">Titulo</label>
                    <input v-model = "title" type = "text" id = "title" required>
                </section>

                <section>
                    <label for = "description">Descrição</label>
                    <textarea v-model = "description" id = "description" rows = "6" required></textarea>
                </section>

                <section>
                    <label for = "date">Data</label>
                    <input v-model = "started" type = "date" id = "date">
                </section>

                <section>
                    <label for = "budget">Orçamento</label>
                    <input v-model = "budget" type = "number" id = "budget">
                </section>

                <section v-if = "action == 'Editar'">
                    <label for = "is_completed">Feito</label>
                    <input v-model = "is_completed" type = "checkbox" id = "is_completed">
                </section>

                <section>
                    <button type="submit" id = 'btn-add'>Confirmar</button>
                    <ConfirmOperation v-if = "confirmadd" :yes = "click" :not = "() => {confirmadd=false}"/>
                </section>
            </form>
        </dialog>    
    </section>
</template>
    
<style>
    #dialog-add-project {
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

    #dialog-add-project #top {
        display: flex;
        justify-content: space-between;
        align-items: start;
    }

    #dialog-add-project h2 {
        margin-bottom: 15px;
    }

    #dialog-add-project textarea {
        resize: none;
    }

    #dialog-add-project textarea, #dialog-add-project input {
        padding: 7px;
        outline: none;
        border: 2px solid transparent;
        border-radius: 5px;
        margin-top: 2px;
    }

    #dialog-add-project textarea:focus, #dialog-add-project input:focus {
        border-color: var(--color-2);
    }

    #dialog-add-project #btn-add {
        padding: 10px 18px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        background: var(--color-2);
        color: var(--color-3);
        transition: background 0.3s ease, transform 0.3s ease;;
    }

    #dialog-add-project #btn-add:hover {
        background: var(--color-4);
        transform: scale(1.1);
    }

    #dialog-add-project #btn-close {
        background: var(--color-2);
        border-radius: 50%;
        cursor: pointer;
        aspect-ratio: 1/1;
        width: 20px;
        border: none;
    }

    #dialog-add-project dialog {
        background: transparent;
        display: block;
        margin: auto;
        border: none;
        width: 100%;
        max-width: 440px;
        padding: 10px;
    }

    #dialog-add-project dialog > form {
        background: var(--color-1);
        color: var(--color-3);
        border-radius: 5px;
        padding: 20px;
    }

    #dialog-add-project dialog > form > section:not(:last-child) {
        margin-bottom: 10px;
        display: grid;
    }

    input[type='checkbox'] {
        background: red;
        text-align: left;
        width: 20px;
    }
</style>