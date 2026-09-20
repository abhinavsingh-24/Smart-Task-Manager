import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import SmartAssistant from '../components/SmartAssistant'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

function DashboardPage() {
  const { user, logout } = useAuth()
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchDashboardTasks = async () => {
      try {
        setLoading(true)
        setError('')
        const response = await api.get('/api/tasks', {
          params: {
            page: 1,
            limit: 100,
          },
        })
        setTasks(response.data.items || [])
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardTasks()
  }, [])

  const stats = useMemo(() => {
    const totals = {
      total: tasks.length,
      pending: tasks.filter((task) => task.status === 'pending').length,
      in_progress: tasks.filter((task) => task.status === 'in_progress').length,
      completed: tasks.filter((task) => task.status === 'completed').length,
    }

    return totals
  }, [tasks])

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1>Welcome back, {user?.name || 'User'}!</h1>
        </div>
        <div className="dashboard-actions">
          <Link to="/tasks" className="primary-button nav-button">
            Tasks
          </Link>
          <button className="secondary-button" onClick={logout}>
            Logout
          </button>
        </div>
      </div>

      {error && <div className="error-box">{error}</div>}

      {loading ? (
        <div className="page-state">Loading dashboard...</div>
      ) : (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <span>Total tasks</span>
              <strong>{stats.total}</strong>
            </div>
            <div className="stat-card">
              <span>Pending</span>
              <strong>{stats.pending}</strong>
            </div>
            <div className="stat-card">
              <span>In progress</span>
              <strong>{stats.in_progress}</strong>
            </div>
            <div className="stat-card">
              <span>Completed</span>
              <strong>{stats.completed}</strong>
            </div>
          </div>

          <div className="assistant-layout">
            <SmartAssistant tasks={tasks} />
          </div>
        </>
      )}
    </div>
  )
}

export default DashboardPage
