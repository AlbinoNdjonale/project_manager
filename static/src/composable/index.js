import { userStore } from '../stores/user'
import api from '../api'

const userstore = userStore()

const update_title = title => {
    const title_element = document.querySelector('title')

    title_element.innerText = `Gestor de Projectos | ${title}`
}

const formatnumber = number => {
    const response = []

    const elements = number.toString().split('').reverse()
        
    for (let index = 0; index < elements.length; index++) {
        if (index % 3 == 0 && index != 0) response.push(' ')
        response.push(elements[index])
    }

    return response.reverse().join('')+' KZ'
}

const deleteproject = async (id, callback = null) => {
    const project = await api.delete(`/api/v1/projects/${id}`, callback)

    if (project.id) {
        userstore.user.projects = userstore.user.projects
            .filter(item => item.id != id)
            return true
    }

    return false
}

export default {
    update_title,
    formatnumber,
    deleteproject
}