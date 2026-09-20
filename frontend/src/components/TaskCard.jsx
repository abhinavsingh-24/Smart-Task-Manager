function TaskCard({ task, onEdit, onDelete }) {
  const statusLabel = {
    pending: 'Pending',
    in_progress: 'In progress',
    completed: 'Completed',
  }

  const priorityLabel = {
    low: 'Low',
    medium: 'Medium',
    high: 'High',
  }

  return (
    <article className="task-card">
      <div className="task-card-header">
        <div>
          <h3>{task.title}</h3>
          <p>{task.description || 'No description provided.'}</p>
        </div>
        <div className="task-badges">
          <span className={`badge status-${task.status}`}>{statusLabel[task.status] || task.status}</span>
          <span className={`badge priority-${task.priority}`}>{priorityLabel[task.priority] || task.priority}</span>
        </div>
      </div>

      <div className="task-meta">
        {task.due_date ? <span>Due: {task.due_date}</span> : <span>No due date</span>}
      </div>

      <div className="task-actions">
        <button type="button" className="secondary-button small" onClick={() => onEdit(task)}>
          Edit
        </button>
        <button type="button" className="danger-button small" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>
    </article>
  )
}

export default TaskCard
