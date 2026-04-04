'use client'

import { PlanProvider } from '@/context/PlanContext'
import { DashboardProjection } from '@/components/dashboard/DashboardProjection'

export default function DashboardPage() {
  return (
    <PlanProvider>
      <DashboardProjection />
    </PlanProvider>
  )
}
