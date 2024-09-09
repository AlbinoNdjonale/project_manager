import process from 'process'

const URL_BASE = process.env.NODE_ENV==='development'?"http://127.0.0.1:8000":document.location.origin

const then = data => {

    const auth = data.headers.get('WWW-Authenticate')

    if (auth) localStorage.setItem('auth', auth)
    
    const class_status = data.status.toString()[0]
  
    if (class_status !== "5") return data.json()
    
    return null
}

const get = async (url, callback = null) => {
    let res

    try {
        await fetch(URL_BASE+url, {
            method: 'GET',
            headers: {
                'WWW-Authenticate': localStorage.getItem('auth')
            }
        })
            .then(then)
            .then(_res => res = _res)
    } catch (error) {
        res = null
    }

    if (callback) callback()

    return res
}

const body = async (url, data, method, useFormData = true, callback = null) => {
    let res
    
    let body = JSON.stringify(data)
  
    if (useFormData) {
        body = new FormData()
        for (const key in data) {
            body.append(key, String(data[key]))
        }
    }
    
    try {
        await fetch(URL_BASE+url, {
            method: method,
            headers: {
                'WWW-Authenticate': localStorage.getItem('auth')
            },
            body
        })
        .then(then)
        .then(_res => { res = _res}) 
    } catch (error) {
        res = null
    }

    if (callback) callback()

    return res
}

const post = async (url, data, useFormData = true, callback = null) => {
    return await body(url, data, 'POST', useFormData, callback)
}

const update = async (url, data, useFormData = true, callback = null) => {
    return await body(url, data, 'PUT', useFormData, callback)
}

const _delete = async (url, callback) => {
    let res

    try {
        await fetch(URL_BASE+url, {
            method: "DELETE",
            headers: {
                'WWW-Authenticate': localStorage.getItem('auth')
            }
        })
        .then(then)
        .then(_res => { res = _res}) 
    } catch (error) {
        res = null
    }

    if (callback) callback()

    return res
}

export default {
    get,
    post,
    update,
    delete: _delete
}