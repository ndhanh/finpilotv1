import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import { PlanProvider, usePlanContext } from '@/context/PlanContext'
import { PlanTemplate } from '@/types/template'

/**
 * Test suite for PlanContext
 *
 * Tests template selection persistence and integration with plan data
 */

const mockTemplate: PlanTemplate = {
  id: 'home_purchase',
  name_vi: 'Mua nhà',
  description_vi: 'Lập kế hoạch tài chính cho việc mua nhà',
  icon: '🏠',
  status: 'available',
  wizard_steps: ['income', 'expenses', 'goals'],
}

// Test component that uses PlanContext
function TestComponent() {
  const context = usePlanContext()

  return (
    <div>
      <div data-testid="selected-template">
        {context.planData.selectedTemplate?.name_vi || 'No template'}
      </div>
      <div data-testid="template-id">
        {context.planData.templateId || 'No templateId'}
      </div>
      <button
        onClick={() => context.setSelectedTemplate(mockTemplate)}
        data-testid="set-template-button"
      >
        Set Template
      </button>
      <button
        onClick={() => context.setSelectedTemplate(null)}
        data-testid="clear-template-button"
      >
        Clear Template
      </button>
      <button
        onClick={() => context.updateField('goalName', 'Buy a house')}
        data-testid="update-goal-button"
      >
        Update Goal
      </button>
      <div data-testid="goal-name">
        {context.planData.goalName || 'No goal'}
      </div>
    </div>
  )
}

describe('PlanContext', () => {
  it('should initialize with empty template', () => {
    render(
      <PlanProvider>
        <TestComponent />
      </PlanProvider>
    )

    const templateElement = screen.getByTestId('selected-template')
    expect(templateElement).toHaveTextContent('No template')
  })

  it('should set selected template', async () => {
    render(
      <PlanProvider>
        <TestComponent />
      </PlanProvider>
    )

    const setButton = screen.getByTestId('set-template-button')
    setButton.click()

    await waitFor(() => {
      const templateElement = screen.getByTestId('selected-template')
      expect(templateElement).toHaveTextContent('Mua nhà')
    })
  })

  it('should set template ID when template is selected', async () => {
    render(
      <PlanProvider>
        <TestComponent />
      </PlanProvider>
    )

    const setButton = screen.getByTestId('set-template-button')
    setButton.click()

    await waitFor(() => {
      const templateIdElement = screen.getByTestId('template-id')
      expect(templateIdElement).toHaveTextContent('home_purchase')
    })
  })

  it('should clear template when setSelectedTemplate receives null', async () => {
    render(
      <PlanProvider>
        <TestComponent />
      </PlanProvider>
    )

    // Set template first
    const setButton = screen.getByTestId('set-template-button')
    setButton.click()

    await waitFor(() => {
      const templateElement = screen.getByTestId('selected-template')
      expect(templateElement).toHaveTextContent('Mua nhà')
    })

    // Clear template
    const clearButton = screen.getByTestId('clear-template-button')
    clearButton.click()

    await waitFor(() => {
      const templateElement = screen.getByTestId('selected-template')
      expect(templateElement).toHaveTextContent('No template')
    })
  })

  it('should persist plan data while template is selected', async () => {
    render(
      <PlanProvider>
        <TestComponent />
      </PlanProvider>
    )

    // Set template
    const setButton = screen.getByTestId('set-template-button')
    setButton.click()

    await waitFor(() => {
      const templateElement = screen.getByTestId('selected-template')
      expect(templateElement).toHaveTextContent('Mua nhà')
    })

    // Update other plan data
    const updateButton = screen.getByTestId('update-goal-button')
    updateButton.click()

    await waitFor(() => {
      const goalElement = screen.getByTestId('goal-name')
      expect(goalElement).toHaveTextContent('Buy a house')

      // Template should still be there
      const templateElement = screen.getByTestId('selected-template')
      expect(templateElement).toHaveTextContent('Mua nhà')
    })
  })

  it('should maintain template through multiple updates', async () => {
    render(
      <PlanProvider>
        <TestComponent />
      </PlanProvider>
    )

    // Set template
    const setButton = screen.getByTestId('set-template-button')
    setButton.click()

    await waitFor(() => {
      const templateIdElement = screen.getByTestId('template-id')
      expect(templateIdElement).toHaveTextContent('home_purchase')
    })

    // Update plan multiple times
    const updateButton = screen.getByTestId('update-goal-button')

    updateButton.click()
    await waitFor(() => {
      const goalElement = screen.getByTestId('goal-name')
      expect(goalElement).toHaveTextContent('Buy a house')
    })

    // Verify template is still intact
    const templateIdElement = screen.getByTestId('template-id')
    expect(templateIdElement).toHaveTextContent('home_purchase')
  })

  it('should throw error when usePlanContext used outside provider', () => {
    // Suppress console.error for this test
    const consoleError = jest.spyOn(console, 'error').mockImplementation()

    const InvalidComponent = () => {
      try {
        usePlanContext()
        return <div>Should not render</div>
      } catch (e) {
        return <div data-testid="error">Error thrown</div>
      }
    }

    render(<InvalidComponent />)

    expect(screen.getByTestId('error')).toBeInTheDocument()

    consoleError.mockRestore()
  })
})
