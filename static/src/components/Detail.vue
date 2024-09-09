<script setup>
    const props = defineProps({
        details: {
            required: true
        },
        update: {
            type: Function,
            required: true
        },
        key_: {
            type: String,
            default: null
        },
        remove_item_: {
            type: Function
        },
        global: {
            type: String,
            default: ''
        }
    })

    const remove_key = (id) => {
        const newdetails = {}

        for (const key in props.details) {
            if (key !== id) newdetails[key] = props.details[key]
        }

        props.update(newdetails, props.key_)
    }

    const editkey = (id) => {
        const p     = document.getElementById(`p-key-${id.replaceAll(' ', '-')}-${props.global}`)
        const input = document.getElementById(`input-key-${id.replaceAll(' ', '-')}-${props.global}`)

        p.style.display = 'none'
        input.style.display = 'block'
        input.value = id
        input.focus()

        const end = e => {
            if (e.key && e.key !== 'Enter') return

            p.style.display     = 'block'
            input.style.display = 'none'

            if (id !== input.value.trim()) {
                const value = input.value.trim()
                const newdetails = {}

                for (const key in props.details) {
                    if (key == id && props.details[value] == undefined) newdetails[value] = props.details[key]
                    else newdetails[key] = props.details[key]
                }

                props.update(newdetails, props.key_)
            }
        }

        input.addEventListener('focusout', end)
        input.addEventListener('keypress', end)
    }

    const editvalue = (id) => {        
        const p     = document.getElementById(`p-value-${id.replaceAll(' ', '-')}-${props.global}`)
        const input = document.getElementById(`input-value-${id.replaceAll(' ', '-')}-${props.global}`)

        p.style.display = 'none'
        input.style.display = 'block'
        const value = input.value.trim()
        input.focus()

        const end = e => {
            if (e.key && e.key !== 'Enter') return

            p.style.display     = 'block'
            input.style.display = 'none'

            if (value !== input.value.trim()) {
                const newdetails = input.value.trim()
            
                props.update(newdetails, props.key_)
            }
        }

        input.addEventListener('focusout', end)
        input.addEventListener('keypress', end)   
    }

    const remove_item = (idx) => {
        const newdetails = []

        for (const key in props.details) {
            if (key != idx) newdetails.push(props.details[key])
        }

        props.update(newdetails, props.key_)
    }

    const update_details = (value, key_) => {
        const newdetails = Array.isArray(props.details)?[]:{}

        for (const key in props.details) {
            if (key == key_) newdetails[key] = value
            else newdetails[key] = props.details[key]
        }

        props.update(newdetails, props.key_)
    }

    const add_detail = (value, key_, newdetails = {}) => {
        const newdet = props.details[key_]

        let count = 1

        let newfield = 'novo campo'

        while (newdet[newfield] !== undefined) {
            newfield = `novo campo${count}`
            count++
        }

        newdet[newfield] = value

        for (const key in props.details)
            if (Array.isArray(newdetails))
                if (key == key_) newdetails.push(newdet)
                else newdetails.push(props.details[key])
            else
                if (key == key_) newdetails[key] = newdet
                else newdetails[key] = props.details[key]

        props.update(newdetails, props.key_)
    }

    const remove_detail = (key_) => {
        const newdetails = []

        for (const key in props.details)
            if (key != key_)
                newdetails.push(props.details[key])

        props.update(newdetails, props.key_)
    }

    const add_item = (value) => {
        const newdetails = []

        for (const key in props.details)
            newdetails.push(props.details[key])

        newdetails.push(value)
        props.update(newdetails, props.key_)
    }
</script>

<template>
    <div v-if = "Array.isArray(details)">
        <div class = "wrapper">
            <div class = "opt">
                <button v-if = "remove_item_" class = "btn-rm" @click = "remove_item_(key_)"></button>
                <button class = "btn-add" @click = "add_item('item')"></button>
                <button class = "btn-add-list" @click = "add_item([])"></button>
                <button class = "btn-add-super" @click = "add_item({})"></button>
            </div>
            <p class = "subitem">-</p>
        </div>

        <ul>
            <li v-for = "(item, key) in details">
                <div :class = "(typeof item === 'object' && item !== null && !Array.isArray(item))?'obj':''">
                    <div v-if = "(typeof item === 'object' && item !== null && !Array.isArray(item))" class = "wrapper-1">
                        <div>
                            <button class = "btn-rm" @click = "remove_detail(key)"></button>
                            <button class = "btn-add" @click = "add_detail('valor', key, [])"></button>
                            <button class = "btn-add-list" @click = "add_detail([], key, [])"></button>
                            <button class = "btn-add-super" @click = "add_item({}, key, [])"></button>
                        </div>
                    </div>
                    
                    <div class = "in-obj">
                        <Detail :global = '`${global}-${key_}`' :remove_item_ = 'remove_item' :details = 'item' :key_ = 'key.toString()' :update = 'update_details'/>
                    </div>
                </div>
            </li>
        </ul>
    </div>

    <div v-else-if = "(typeof details === 'object' && details !== null)"  v-for = "(value, key) in details" class = "attr">
        <input :style = '{display: "none"}' :id = "`input-key-${key.replaceAll(' ', '-')}-${global}`" class = "key">
        <div :id = "`p-key-${key.replaceAll(' ', '-')}-${global}`">
            <div class = "wrapper">
                <div class = "opt">
                    <button class = "btn-rm" @click = "remove_key(key)"></button>
                </div>
                <p @dblclick = "editkey(key)" class = "key">{{ key }}</p>
            </div>
        </div>
        
        <div :class = "(typeof value === 'object' && value !== null && !Array.isArray(value))?'obj':''">
            <div v-if = "(typeof value === 'object' && value !== null && !Array.isArray(value))" class = "wrapper-1">
                <div>
                    <button class = "btn-add" @click = "add_detail('valor', key)"></button>
                    <button class = "btn-add-list" @click = "add_detail([], key)"></button>
                    <button class = "btn-add-super" @click = "add_detail({}, key)"></button>
                </div>
            </div>

            <div class = "in-obj">
                <Detail :global = '`${global}-${key_}`' :details = 'value' :key_ = 'key' :update = 'update_details'/>
            </div>
        </div>
    </div>

    <div v-else>
        <div class = "wrapper">
            <input :style = '{display: "none"}' :id = "`input-value-${key_.replaceAll(' ', '-')}-${global}`" :value = 'details'>
            
            <div :id = "`p-value-${key_.replaceAll(' ', '-')}-${global}`">
                <div v-if = "remove_item_" class = "opt">
                    <button @click = "remove_item_(key_)" class = "btn-rm"></button>
                </div>
                <p @dblclick = "editvalue(key_)" class = "value">{{ details }}</p>
            </div>
        </div>
    </div>
</template>
    
<style scoped>
    .attr {
        flex: 1 1 200px;
        background: #f9f9f9;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 10px;
        border-radius: 8px;
    }

    ul {
        padding-left: 18px;
    }

    li:not(:last-child) {
        margin-bottom: 7px;
    }

    .obj {
        background: var(--color-3);
        border: 1px solid #ddd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
        border-radius: 8px;
    }

    .obj .in-obj {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }

    .key {
        font-weight: bold;
        margin-bottom: 7px;
        padding: 5px;
    }

    .value, .subitem {
        padding: 5px;
    }

    input.key {
        padding: 5.5px;
    }

    input {
        outline: none;
        border: none;
        padding: 5.5px;
        border-radius: 5px;
        border: 1px solid #ddd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .wrapper-1 {
        text-align: right;
        margin-bottom: 10px;
    }

    .wrapper-1 > div > button:not(:last-child) {
        margin-right: 5px;
    }

    .wrapper {
        display: inline-block;
    }

    .opt {
        position: absolute;
        display: none;
    }

    .opt button, .obj button {
        padding: 6px;
        border: none;
        border-radius: 50%;
        cursor: pointer;
    }

    .btn-rm {
        background: var(--color-2);
    }

    .btn-add {
        background: #0ac90a;
    }

    .btn-add-list {
        background: #0a0ac9;
    }

    .btn-add-super {
        background: #c9c90a;
    }

    *:hover > .opt {
        display: flex;
        gap: 5px;
    }
</style>