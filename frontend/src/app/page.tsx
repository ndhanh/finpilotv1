import { redirect } from 'next/navigation'

/**
 * Main app lives at app.finpilot.vn; marketing is a separate deploy (finpilot.vn).
 * Root route sends users straight into the planning flow.
 */
export default function Home() {
  redirect('/plan-templates')
}
