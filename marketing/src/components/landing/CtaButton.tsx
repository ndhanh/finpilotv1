import Link from 'next/link'
import type { ReactNode } from 'react'

type Props = {
  href: string
  className?: string
  children?: ReactNode
}

export function CtaButton({ href, className = '', children = 'Bắt đầu ngay' }: Props) {
  return (
    <Link
      href={href}
      className={`inline-flex items-center justify-center rounded-xl bg-primary-600 px-8 py-3.5 text-base font-semibold text-white shadow-md shadow-primary-600/20 transition hover:bg-primary-700 hover:shadow-lg ${className}`}
    >
      {children}
    </Link>
  )
}
