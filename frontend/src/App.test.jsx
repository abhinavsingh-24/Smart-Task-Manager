import '@testing-library/jest-dom/vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import App from './App'
import api from './services/api'

vi.mock('./services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}))

describe('App', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('renders the login screen for unauthenticated users', () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>,
    )

    expect(screen.getByText(/smart task manager/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument()
  })

  it('shows the task manager dashboard for authenticated users', async () => {
    localStorage.setItem('token', 'demo-token')
    api.get.mockImplementation((url) => {
      if (url === '/api/auth/me') {
        return Promise.resolve({ data: { id: 'u1', name: 'Jane Doe', email: 'jane@example.com' } })
      }

      if (url === '/api/tasks') {
        return Promise.resolve({
          data: {
            items: [
              { id: '1', title: 'First task', description: 'Example', status: 'pending', priority: 'high', due_date: '2026-09-22' },
            ],
            total: 1,
            page: 1,
            pages: 1,
          },
        })
      }

      return Promise.resolve({ data: {} })
    })

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <App />
      </MemoryRouter>,
    )

    expect(await screen.findByText(/welcome back, jane doe/i)).toBeInTheDocument()
    expect(await screen.findByText('Total tasks')).toBeInTheDocument()
    expect(screen.getAllByText('1').length).toBeGreaterThan(0)
    expect(screen.getByText(/smart assistant/i)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /tasks/i })).toBeInTheDocument()
  })

  it('keeps dashboard stats aligned with the authenticated task list', async () => {
    const tasksPayload = {
      items: [
        { id: '1', title: 'One task', description: 'Example', status: 'pending', priority: 'high', due_date: '2026-09-22' },
      ],
      total: 1,
      page: 1,
      pages: 1,
    }

    localStorage.setItem('token', 'demo-token')
    api.get.mockImplementation((url) => {
      if (url === '/api/auth/me') {
        return Promise.resolve({ data: { id: 'u1', name: 'Jane Doe', email: 'jane@example.com' } })
      }

      if (url === '/api/tasks') {
        return Promise.resolve({ data: tasksPayload })
      }

      return Promise.resolve({ data: {} })
    })

    const { unmount } = render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <App />
      </MemoryRouter>,
    )

    await screen.findByText(/welcome back, jane doe/i)
    expect(screen.getByText('Total tasks')).toBeInTheDocument()
    expect(screen.getAllByText('1').length).toBeGreaterThan(0)

    unmount()

    render(
      <MemoryRouter initialEntries={['/tasks']}>
        <App />
      </MemoryRouter>,
    )

    const taskCards = await screen.findAllByText(/One task/i)
    expect(taskCards.length).toBeGreaterThan(0)
    expect(screen.getByText(/one task/i)).toBeInTheDocument()
  })
})
