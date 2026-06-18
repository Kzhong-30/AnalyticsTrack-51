import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import request from '../utils/request'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isClient = computed(() => userInfo.value?.role === 'client')
  const isLawyer = computed(() => userInfo.value?.role === 'lawyer')
  const isAdmin = computed(() => userInfo.value?.role === 'admin')

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setUserInfo(info) {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  async function login(username, password) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    const res = await request.post('/auth/login', formData)
    setToken(res.access_token)
    await fetchUserInfo()
    return res
  }

  async function fetchUserInfo() {
    try {
      const res = await request.get('/auth/me')
      setUserInfo(res)
      return res
    } catch (e) {
      console.error('获取用户信息失败', e)
    }
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    isClient,
    isLawyer,
    isAdmin,
    setToken,
    setUserInfo,
    login,
    fetchUserInfo,
    logout
  }
})
