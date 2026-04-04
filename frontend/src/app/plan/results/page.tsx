import { redirect } from 'next/navigation'

/** Kết quả dự báo được hiển thị tại /dashboard */
export default function PlanResultsRedirectPage() {
  redirect('/dashboard')
}
