import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'FinPilot — Lập kế hoạch tài chính cá nhân',
  description:
    'Nền tảng lập kế hoạch tài chính cho người Việt: mục tiêu rõ ràng, mô phỏng và lộ trình thực tế.',
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_MARKETING_URL ?? 'http://localhost:3001'
  ),
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
