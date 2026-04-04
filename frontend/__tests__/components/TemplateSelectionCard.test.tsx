import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import { TemplateSelectionCard } from '@/components/planning/TemplateSelectionCard'
import { PlanTemplate } from '@/types/template'

/**
 * Test suite for TemplateSelectionCard component
 *
 * Tests rendering, interaction, and state changes for template cards
 */

const mockAvailableTemplate: PlanTemplate = {
  id: 'home_purchase',
  name_vi: 'Mua nhà',
  description_vi: 'Lập kế hoạch tài chính cho việc mua nhà',
  icon: '🏠',
  status: 'available',
  wizard_steps: ['income', 'expenses', 'goals'],
}

const mockComingSoonTemplate: PlanTemplate = {
  id: 'emergency_fund',
  name_vi: 'Quỹ dự phòng',
  description_vi: 'Xây dựng quỹ dự phòng cho khẩn cấp',
  icon: '🆘',
  status: 'coming_soon',
  wizard_steps: ['income', 'expenses'],
}

describe('TemplateSelectionCard', () => {
  it('renders template information correctly', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockAvailableTemplate}
        onClick={mockClick}
      />
    )

    expect(screen.getByText('🏠')).toBeInTheDocument()
    expect(screen.getByText('Mua nhà')).toBeInTheDocument()
    expect(
      screen.getByText('Lập kế hoạch tài chính cho việc mua nhà')
    ).toBeInTheDocument()
  })

  it('shows "Bắt đầu" button for available templates', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockAvailableTemplate}
        onClick={mockClick}
      />
    )

    const button = screen.getByRole('button', { name: /Bắt đầu/i })
    expect(button).toBeInTheDocument()
    expect(button).not.toBeDisabled()
  })

  it('shows "Sắp có" label for coming soon templates', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockComingSoonTemplate}
        onClick={mockClick}
      />
    )

    expect(screen.getByText('Sắp có')).toBeInTheDocument()
    expect(
      screen.getByText('Tính năng này sắp được phát hành')
    ).toBeInTheDocument()
  })

  it('disables button for coming soon templates', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockComingSoonTemplate}
        onClick={mockClick}
      />
    )

    const button = screen.getByRole('button', { name: /Sắp có/i })
    expect(button).toBeDisabled()
  })

  it('calls onClick with template id when available button is clicked', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockAvailableTemplate}
        onClick={mockClick}
      />
    )

    const button = screen.getByRole('button', { name: /Bắt đầu/i })
    fireEvent.click(button)

    expect(mockClick).toHaveBeenCalledWith('home_purchase')
    expect(mockClick).toHaveBeenCalledTimes(1)
  })

  it('does not call onClick when coming soon button is clicked', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockComingSoonTemplate}
        onClick={mockClick}
      />
    )

    const button = screen.getByRole('button', { name: /Sắp có/i })
    fireEvent.click(button)

    expect(mockClick).not.toHaveBeenCalled()
  })

  it('respects disabled prop for available templates', () => {
    const mockClick = jest.fn()

    render(
      <TemplateSelectionCard
        template={mockAvailableTemplate}
        onClick={mockClick}
        disabled={true}
      />
    )

    const button = screen.getByRole('button', { name: /Bắt đầu/i })
    expect(button).toBeDisabled()

    fireEvent.click(button)
    expect(mockClick).not.toHaveBeenCalled()
  })

  it('applies correct styling for available templates', () => {
    const mockClick = jest.fn()

    const { container } = render(
      <TemplateSelectionCard
        template={mockAvailableTemplate}
        onClick={mockClick}
      />
    )

    const card = container.querySelector('[class*="border-blue-500"]')
    expect(card).toBeInTheDocument()
  })

  it('applies correct styling for disabled templates', () => {
    const mockClick = jest.fn()

    const { container } = render(
      <TemplateSelectionCard
        template={mockComingSoonTemplate}
        onClick={mockClick}
      />
    )

    const card = container.querySelector('[class*="border-gray-300"]')
    expect(card).toBeInTheDocument()
  })
})
