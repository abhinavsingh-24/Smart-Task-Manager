import { useState } from 'react'

function AuthForm({ type, onSubmit, loading, error }) {
  const isRegister = type === 'register'
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirm_password: '',
  })

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((previous) => ({ ...previous, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit(formData)
  }

  return (
    <div className="auth-card">
      <div className="auth-header">
        <h1>Smart Task Manager</h1>
        <p>{isRegister ? 'Create your account' : 'Welcome back'}</p>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        {isRegister && (
          <div className="field-group">
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
              required
            />
          </div>
        )}

        <div className="field-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="name@example.com"
            required
          />
        </div>

        <div className="field-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="••••••••"
            minLength={8}
            required
          />
        </div>

        {isRegister && (
          <div className="field-group">
            <label htmlFor="confirm_password">Confirm password</label>
            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              value={formData.confirm_password}
              onChange={handleChange}
              placeholder="Repeat password"
              minLength={8}
              required
            />
          </div>
        )}

        {error && <div className="error-box">{error}</div>}

        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? 'Please wait...' : isRegister ? 'Create account' : 'Login'}
        </button>
      </form>
    </div>
  )
}

export default AuthForm
