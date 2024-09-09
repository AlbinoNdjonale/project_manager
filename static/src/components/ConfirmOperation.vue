<script setup>
    const props = defineProps({
        yes: {
            required: true,
            type: Function
        },
        not: {
            required: true,
            type: Function
        }
    })
</script>

<template>
    <div>
        <dialog>
            <section>
                <span>Aviso</span>
            
                <p>Tens a certeza de que desejas efetuar esta operação?</p>

                <section>
                    <button @click = "yes" class = "btn-yes">Sim</button>
                    <button @click = "not" class = "btn-not">Não</button>
                </section>
            </section>
        </dialog>    
    </div>
</template>
        
<style scoped>
    div {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        display: flex;
        z-index: 20;
        justify-content: center;
        align-items: center;
    }

    div dialog {
        background: transparent;
        display: block;
        margin: auto;
        border: none;
        width: 100%;
        padding: 10px;
        max-width: 340px;
    }

    div dialog > section {
        border-top: 3px solid yellow;
        max-width: 340px;
        padding: 10px;
        background: var(--color-3);
        color: var(--color-1);
        border-radius: 5px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, .4);
    }

    div dialog > section > section{
        text-align: right;
    }

    p {
        margin: 20px 0;
        text-align: center;
    }

    button:not(:last-child) {
        margin-right: 10px;
    }

    button {
        padding: 9px 16px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        transition: transform .3s ease;
        color: var(--color-3);
    }

    button:hover {
        transform: scale(1.1);
    }

    .btn-yes {
        background: var(--color-1);
    }

    .btn-not {
        background: var(--color-2);
    }
</style>