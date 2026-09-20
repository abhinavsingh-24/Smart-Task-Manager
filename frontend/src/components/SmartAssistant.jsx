function SmartAssistant({ tasks }) {
  const priorityScore = {
    low: 1,
    medium: 2,
    high: 3,
  }

  const pendingTasks = tasks.filter((task) => task.status !== 'completed')
  const nextTask = [...pendingTasks].sort((a, b) => {
    const scoreDiff = (priorityScore[b.priority] || 0) - (priorityScore[a.priority] || 0)
    if (scoreDiff !== 0) return scoreDiff
    return new Date(a.due_date || '9999-12-31') - new Date(b.due_date || '9999-12-31')
  })[0]

  const dueSoon = [...tasks]
    .filter((task) => task.status !== 'completed' && task.due_date)
    .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
    .slice(0, 2)

  const suggestions = [
    pendingTasks.length > 0
      ? `Focus on ${nextTask?.title || 'your next priority task'} first to keep momentum high.`
      : 'Everything is complete. Add a new task to keep the workflow moving.',
    dueSoon.length
      ? `You have ${dueSoon.length} task${dueSoon.length > 1 ? 's' : ''} due soon: ${dueSoon.map((task) => task.title).join(', ')}.`
      : 'No urgent due dates are approaching right now.',
    'Break larger work into a short next step, then mark the task as in progress once it starts.',
  ]

  return (
    <section className="smart-assistant-card">
      <div className="assistant-heading">
        <p className="eyebrow">Smart assistant</p>
        <h2>Today’s focus</h2>
      </div>

      <p className="assistant-summary">
        {pendingTasks.length > 0
          ? `You have ${pendingTasks.length} active task${pendingTasks.length > 1 ? 's' : ''} in motion. ${nextTask ? nextTask.title : 'Choose your next task'} is the strongest candidate for immediate attention.`
          : 'There are no active tasks right now. Planning one new task will keep your workload steady.'}
      </p>

      <ul className="assistant-suggestions">
        {suggestions.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  )
}

export default SmartAssistant
