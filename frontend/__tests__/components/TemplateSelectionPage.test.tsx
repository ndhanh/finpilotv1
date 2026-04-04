import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import { TemplateSelectionPage } from '@/components/planning/TemplateSelectionPage'
import { useTemplateSelection } from '@/hooks/useTemplateSelection'
import { usePlan } from '@/hooks/usePlan'
import { useRouter } from 'next/navigation'

/**
 * Test suite for TemplateSelectionPage component
 *
 * Tests rendering, loading states, error handling, and template selection flow
 */

jest.mock('@/hooks/useTemplateSelection')
jest.mock('@/hooks/usePlan')
jest.mock('next/navigation')

const mockHook = useTemplateSelection as jest.MockedFunction<
  typeof useTemplateSelection
>
const mockPlanHook = usePlan as jest.MockedFunction<typeof usePlan>
const mockRouter = useRouter as jest.MockedFunction<typeof useRouter>

const mockTemplates = [
  {
    id: 'home_purchase',
    name_vi: 'Mua nhà',
    description_vi: 'Lập kế hoạch tài chính cho việc mua nhà',
    icon: '🏠',
    status: 'available' as const,
    wizard_steps: ['income', 'expenses', 'goals'],
  },
  {
    id: 'emergency_fund',
    name_vi: 'Quỹ dự phòng',
    description_vi: 'Xây dựng quỹ dự phòng cho khẩn cấp',
    icon: '🆘',
    status: 'coming_soon' as const,
    wizard_steps: ['income', 'expenses'],
  },
]

describe('TemplateSelectionPage', () => {
  const mockPush = jest.fn()
  const mockSetSelectedTemplate = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    mockRouter.mockReturnValue({
      push: mockPush,
      replace: jest.fn(),
      prefetch: jest.fn(),
      refresh: jest.fn(),
    } as any)
    mockPlanHook.mockReturnValue({
      plan: {},
      setPlan: jest.fn(),
      setSelectedTemplate: mockSetSelectedTemplate,
      isFieldComplete: jest.fn(),
      getProgress: jest.fn(),
    } as any)
  })

  it('shows loading state while fetching templates', () => {
    mockHook.mockReturnValue({
      templates: [],
      loading: true,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    expect(screen.getByText('Đang tải các mẫu kế hoạch...')).toBeInTheDocument()
  })

  it('shows error state when template loading fails', () => {
    mockHook.mockReturnValue({
      templates: [],
      loading: false,
      error: 'Failed to load templates',
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    expect(screen.getByText('Có lỗi xảy ra')).toBeInTheDocument()
    expect(
      screen.getByText('Không thể tải các mẫu kế hoạch. Vui lòng thử lại sau.')
    ).toBeInTheDocument()
  })

  it('renders templates when loaded successfully', async () => {
    mockHook.mockReturnValue({
      templates: mockTemplates,
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    expect(screen.getByText('Chọn kế hoạch của bạn')).toBeInTheDocument()
    expect(
      screen.getByText(
        'Chọn một mẫu kế hoạch để bắt đầu quản lý tài chính của bạn'
      )
    ).toBeInTheDocument()
    expect(screen.getByText('Mua nhà')).toBeInTheDocument()
    expect(screen.getByText('Quỹ dự phòng')).toBeInTheDocument()
  })

  it('displays empty state when no templates available', () => {
    mockHook.mockReturnValue({
      templates: [],
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    expect(screen.getByText('Không có mẫu kế hoạch nào')).toBeInTheDocument()
  })

  it('handles template selection and navigation', async () => {
    mockHook.mockReturnValue({
      templates: mockTemplates,
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    const buttons = screen.getAllByRole('button', { name: /Bắt đầu/i })
    fireEvent.click(buttons[0])

    await waitFor(() => {
      expect(mockSetSelectedTemplate).toHaveBeenCalledWith(mockTemplates[0])
      expect(mockPush).toHaveBeenCalledWith('/plan/home_purchase/income')
    })
  })

  it('does not navigate when coming soon template is clicked', async () => {
    mockHook.mockReturnValue({
      templates: mockTemplates,
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    const comingSoonButtons = screen.getAllByRole('button', { name: /Sắp có/i })
    expect(comingSoonButtons[0]).toBeDisabled()

    fireEvent.click(comingSoonButtons[0])

    await waitFor(() => {
      expect(mockSetSelectedTemplate).not.toHaveBeenCalled()
      expect(mockPush).not.toHaveBeenCalled()
    })
  })

  it('displays footer info about changing selection later', () => {
    mockHook.mockReturnValue({
      templates: mockTemplates,
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    expect(
      screen.getByText(
        'Bạn có thể thay đổi lựa chọn của mình bất cứ lúc nào trong các cài đặt'
      )
    ).toBeInTheDocument()
  })

  it('renders responsive grid layout', () => {
    mockHook.mockReturnValue({
      templates: mockTemplates,
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    const { container } = render(<TemplateSelectionPage />)

    const grid = container.querySelector('[class*="grid-cols"]')
    expect(grid).toBeInTheDocument()
    expect(grid).toHaveClass('grid')
  })

  it('handles retry on error', () => {
    mockHook.mockReturnValue({
      templates: [],
      loading: false,
      error: 'Failed to load templates',
      getTemplate: jest.fn(),
    } as any)

    const reloadSpy = jest.fn()
    Object.defineProperty(window.location, 'reload', {
      configurable: true,
      value: reloadSpy,
    })

    render(<TemplateSelectionPage />)

    const retryButton = screen.getByRole('button', { name: /Thử lại/i })
    fireEvent.click(retryButton)

    expect(reloadSpy).toHaveBeenCalled()
  })

  it('renders all templates with correct icons and descriptions', () => {
    mockHook.mockReturnValue({
      templates: mockTemplates,
      loading: false,
      error: null,
      getTemplate: jest.fn(),
    } as any)

    render(<TemplateSelectionPage />)

    // Check first template
    expect(screen.getByText('🏠')).toBeInTheDocument()
    expect(
      screen.getByText('Lập kế hoạch tài chính cho việc mua nhà')
    ).toBeInTheDocument()

    // Check second template
    expect(screen.getByText('🆘')).toBeInTheDocument()
    expect(
      screen.getByText('Xây dựng quỹ dự phòng cho khẩn cấp')
    ).toBeInTheDocument()
  })
})
