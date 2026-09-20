import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import AuthForm from '../components/AuthForm'
import { useAuth } from '../context/AuthContext'

function RegisterPage() {
  const { token, register } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (token) {
    return <Navigate to="/dashboard" replace />
  }

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError('')

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match.')
      setLoading(false)
      return
    }

    try {
      await register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirm_password,
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
      <AuthForm type="register" onSubmit={handleSubmit} loading={loading} error={error} />
      <p className="switch-link">
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  )
}

export default RegisterPage
