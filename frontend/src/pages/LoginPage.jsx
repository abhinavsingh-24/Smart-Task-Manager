import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import AuthForm from '../components/AuthForm'
import { useAuth } from '../context/AuthContext'

function LoginPage() {
  const { token, login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (token) {
    const redirectTo = location.state?.from?.pathname || '/dashboard'
    return <Navigate to={redirectTo} replace />
  }

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError('')

    try {
      await login({
        email: formData.email,
        password: formData.password,
      })
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <AuthForm type="login" onSubmit={handleSubmit} loading={loading} error={error} />
      <p className="switch-link">
        Need an account? <Link to="/register">Sign up</Link>
      </p>
    </div>
  )
}

export default LoginPage
