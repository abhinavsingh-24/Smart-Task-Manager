import { useEffect, useMemo, useState } from 'react'
import TaskForm from '../components/TaskForm'
import TaskList from '../components/TaskList'
import api from '../services/api'

const initialFilters = {
  page: 1,
  limit: 6,
  search: '',
  status: 'all',
  priority: 'all',
  sort: 'newest',
}

function TasksPage() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState(initialFilters)
  const [pagination, setPagination] = useState({ total: 0, page: 1, pages: 1 })
  const [showForm, setShowForm] = useState(false)
  const [selectedTask, setSelectedTask] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const fetchTasks = async (nextFilters = filters) => {
    try {
      setLoading(true)
      setError('')
      const params = {
        page: nextFilters.page,
        limit: nextFilters.limit,
        status: nextFilters.status === 'all' ? undefined : nextFilters.status,
        priority: nextFilters.priority === 'all' ? undefined : nextFilters.priority,
        sort: nextFilters.sort,
        search: nextFilters.search || undefined,
      }

      const response = await api.get('/api/tasks', { params })
      setTasks(response.data.items || [])
      setPagination({
        total: response.data.total || 0,
        page: response.data.page || 1,
        pages: response.data.pages || 1,
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks(filters)
  }, [filters.page, filters.limit, filters.status, filters.priority, filters.sort])

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (filters.search !== initialFilters.search || filters.page !== initialFilters.page) {
        fetchTasks({ ...filters, page: 1 })
      }
    }, 250)

    return () => clearTimeout(timeoutId)
  }, [filters.search])

  const summary = useMemo(() => {
    return {
      total: pagination.total,
      pending: tasks.filter((task) => task.status === 'pending').length,
      inProgress: tasks.filter((task) => task.status === 'in_progress').length,
      completed: tasks.filter((task) => task.status === 'completed').length,
    }
  }, [tasks, pagination.total])

  const handleCreateOrUpdate = async (payload) => {
    try {
      setSubmitting(true)
      if (selectedTask) {
        await api.put(`/api/tasks/${selectedTask.id}`, payload)
      } else {
        await api.post('/api/tasks', payload)
      }

      setShowForm(false)
      setSelectedTask(null)
      await fetchTasks({ ...filters, page: 1 })
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (taskId) => {
    const confirmed = window.confirm('Delete this task?')
    if (!confirmed) return

    try {
      await api.delete(`/api/tasks/${taskId}`)
      await fetchTasks({ ...filters, page: 1 })
    } catch (err) {
      setError(err.message)
    }
  }

  const openEditTask = (task) => {
    setSelectedTask(task)
    setShowForm(true)
  }

  const closeForm = () => {
    setShowForm(false)
    setSelectedTask(null)
  }

  return (
    <div className="tasks-page">
      <div className="tasks-header">
        <div>
          <p className="eyebrow">Tasks</p>
          <h1>Task board</h1>
        </div>
        <button className="primary-button" onClick={() => setShowForm(true)}>
          New task
        </button>
      </div>

      <div className="stats-grid compact">
        <div className="stat-card">
          <span>Total</span>
          <strong>{summary.total}</strong>
        </div>
        <div className="stat-card">
          <span>Pending</span>
          <strong>{summary.pending}</strong>
        </div>
        <div className="stat-card">
          <span>In progress</span>
          <strong>{summary.inProgress}</strong>
        </div>
        <div className="stat-card">
          <span>Completed</span>
          <strong>{summary.completed}</strong>
        </div>
      </div>

      <div className="filters-panel">
        <input
          type="search"
          placeholder="Search tasks..."
          value={filters.search}
          onChange={(event) => setFilters((previous) => ({ ...previous, search: event.target.value, page: 1 }))}
        />

        <select value={filters.status} onChange={(event) => setFilters((previous) => ({ ...previous, status: event.target.value, page: 1 }))}>
          <option value="all">All statuses</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In progress</option>
          <option value="completed">Completed</option>
        </select>

        <select value={filters.priority} onChange={(event) => setFilters((previous) => ({ ...previous, priority: event.target.value, page: 1 }))}>
          <option value="all">All priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>

        <select value={filters.sort} onChange={(event) => setFilters((previous) => ({ ...previous, sort: event.target.value, page: 1 }))}>
          <option value="newest">Newest</option>
          <option value="oldest">Oldest</option>
          <option value="due_date">Due date</option>
          <option value="priority">Priority</option>
        </select>
      </div>

      {error && <div className="error-box">{error}</div>}

      {loading ? (
        <div className="page-state">Loading tasks...</div>
      ) : (
        <>
          <TaskList tasks={tasks} onEdit={openEditTask} onDelete={handleDelete} />

          <div className="pagination-row">
            <button
              type="button"
              className="secondary-button"
              disabled={pagination.page <= 1}
              onClick={() => setFilters((previous) => ({ ...previous, page: previous.page - 1 }))}
            >
              Previous
            </button>
            <span>
              Page {pagination.page} of {pagination.pages}
            </span>
            <button
              type="button"
              className="secondary-button"
              disabled={pagination.page >= pagination.pages}
              onClick={() => setFilters((previous) => ({ ...previous, page: previous.page + 1 }))}
            >
              Next
            </button>
          </div>
        </>
      )}

      {showForm && (
        <TaskForm
          task={selectedTask}
          submitting={submitting}
          onSubmit={handleCreateOrUpdate}
          onCancel={closeForm}
        />
      )}
    </div>
  )
}

export default TasksPage
