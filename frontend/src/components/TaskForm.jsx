import { useEffect, useState } from 'react'

const emptyForm = {
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
  due_date: '',
}

function TaskForm({ task = null, onSubmit, onCancel, submitting = false }) {
  const [formData, setFormData] = useState(emptyForm)

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        status: task.status || 'pending',
        priority: task.priority || 'medium',
        due_date: task.due_date || '',
      })
      return
    }

    setFormData(emptyForm)
  }, [task])

  const handleChange = (event) => {
    const { name, value } = event.target
    setFormData((previous) => ({ ...previous, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit({
      ...formData,
      title: formData.title.trim(),
      description: formData.description.trim(),
      due_date: formData.due_date || null,
    })
  }

  return (
    <div className="modal-backdrop" onClick={onCancel}>
      <div className="modal-card" onClick={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <h2>{task ? 'Edit task' : 'Create task'}</h2>
          <button type="button" className="ghost-button" onClick={onCancel}>
            Close
          </button>
        </div>

        <form className="task-form" onSubmit={handleSubmit}>
          <div className="field-group">
            <label htmlFor="title">Title</label>
            <input
              id="title"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="Finish project proposal"
              required
            />
          </div>

          <div className="field-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Add notes, steps, or context"
            />
          </div>

          <div className="task-form-row">
            <div className="field-group">
              <label htmlFor="status">Status</label>
              <select id="status" name="status" value={formData.status} onChange={handleChange}>
                <option value="pending">Pending</option>
                <option value="in_progress">In progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div className="field-group">
              <label htmlFor="priority">Priority</label>
              <select id="priority" name="priority" value={formData.priority} onChange={handleChange}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          <div className="field-group">
            <label htmlFor="due_date">Due date</label>
            <input id="due_date" name="due_date" type="date" value={formData.due_date} onChange={handleChange} />
          </div>

          <div className="task-form-actions">
            <button type="button" className="secondary-button" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="primary-button" disabled={submitting}>
              {submitting ? 'Saving...' : task ? 'Save changes' : 'Create task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default TaskForm
