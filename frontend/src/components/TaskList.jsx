import TaskCard from './TaskCard'

function TaskList({ tasks, onEdit, onDelete }) {
  if (!tasks.length) {
    return (
      <div className="empty-state">
        <h3>No tasks yet</h3>
        <p>Create your first task to start organizing your work.</p>
      </div>
    )
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onEdit={onEdit} onDelete={onDelete} />
      ))}
    </div>
  )
}

export default TaskList
