<script setup>
    import { computed, ref } from 'vue'
    import { RouterLink }  from 'vue-router'
    import ConfirmOperation from '../components/ConfirmOperation.vue'
    import { processingrequestStore } from '../stores/processingrequest'
    import composable from '../composable'

    const props = defineProps({
        id: {
            required: true,
            type: Number
        },
        title: {
            required: true,
            type: String
        },
        description: {
            required: true,
            type: String
        },
        budget: {
            type: Number
        },
        date: {
            type: Object
        },
        is_completed: {
            required: true,
            type: Boolean
        }
    })

    const processingrequeststore = processingrequestStore()

    const confirmdel = ref(false)

    const deleteproject = async () => {
        confirmdel.value = false

        processingrequeststore.set(true)
        await composable.deleteproject(props.id, () => processingrequeststore.set(false))
    }

    const descriptioncomputed = computed(() => {
        return `${ props.description.slice(0, 60) }${ props.description.length>60?'...':''}`
    })

    const budgetcomputed = computed(() => {
        return composable.formatnumber(props.budget)
    })

</script>

<template>
    <div class = "card">
        <div class = "top">
            <h3>{{ title }}</h3>

            <button @click = "() => {confirmdel = true}" class = "btn-close"></button>
        </div>

        <p>
            {{ descriptioncomputed }}
        </p>

        <p>
            <em v-if = "budget">orçamento: {{ budgetcomputed }}</em>
            <em v-if = "date">data: {{ date.day }}.{{ date.month }}.{{ date.year }}</em>
            <em>feito: <input disabled type="checkbox" :checked = 'is_completed'></em>
        </p>

        <RouterLink :to = '`/projects/${id}`'><button>ver</button></RouterLink>
    </div>
    <ConfirmOperation v-if = "confirmdel" :yes = "deleteproject" :not = "() => {confirmdel = false}"/>
</template>
    
<style scoped>
    .card {
        background: var(--color-3);
        flex: 1 1 300px;
        margin: 10px;
        padding: 20px;
        max-width: 300px;
        width: 100%;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, .1);
        transition: transform 0.3s ease;
    }

    .card:hover {
        transform: translateY(-5px);
    }

    .card h3 {
        margin-bottom: 10px;
    }

    .card p {
        font-size: .9rem;
        margin-bottom: 20px;
        white-space: pre-wrap;
        word-break: break-all;
        display: grid;
    }

    .card a > button {
        display: inline-block;
        padding: 8px 16px;
        background: var(--color-2);
        color: var(--color-3);
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .card a > button:hover {
        background: var(--color-4);
        transform: scale(1.1);
    }

    .top {
        display: flex;
        justify-content: space-between;
        align-items: start;
    }

    .btn-close {
        background: var(--color-2);
        border-radius: 50%;
        cursor: pointer;
        aspect-ratio: 1/1;
        width: 17px;
        border: none;
    }

    @media screen and (max-width: 674px) {
        .card {
            margin: 10px auto;
        }
    }
</style>