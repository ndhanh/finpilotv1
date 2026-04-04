import { TemplateSelectionPage } from '@/components/planning/TemplateSelectionPage'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Chọn Kế Hoạch | FinPilot',
  description: 'Chọn mẫu kế hoạch tài chính để bắt đầu',
}

/**
 * Template Selection Page Route
 *
 * Displays the template selection interface where users can choose
 * which financial planning template to use (house purchase, emergency fund, etc.)
 */
export default function PlanTemplatesPage() {
  return <TemplateSelectionPage />
}
