import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      setToken(storedToken)
      api
        .get('/api/auth/me')
        .then((response) => {
          setUser(response.data)
        })
        .catch(() => {
          localStorage.removeItem('token')
          setToken(null)
          setUser(null)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (credentials) => {
    const response = await api.post('/api/auth/login', credentials)
    const accessToken = response.data.access_token
    localStorage.setItem('token', accessToken)
    setToken(accessToken)
    setUser(response.data.user)
    return response.data
  }

  const register = async (payload) => {
    const response = await api.post('/api/auth/register', payload)
    const accessToken = response.data.access_token
    localStorage.setItem('token', accessToken)
    setToken(accessToken)
    setUser(response.data.user)
    return response.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const value = useMemo(
    () => ({ user, token, loading, login, register, logout, setUser }),
    [user, token, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
