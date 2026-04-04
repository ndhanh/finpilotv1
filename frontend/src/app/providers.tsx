'use client'

import { ReactNode } from 'react'
import { PlanProvider } from '@/context/PlanContext'

export function Providers({ children }: { children: ReactNode }) {
  return <PlanProvider>{children}</PlanProvider>
}
