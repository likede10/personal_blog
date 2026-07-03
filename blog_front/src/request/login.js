import res from '@/utils/request'


export const login_request = async() => {
    const data = await res.post('/login/register')
    return data
}