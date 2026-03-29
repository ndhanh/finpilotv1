import Link from 'next/link'
import { CtaButton } from './CtaButton'

type Props = {
  planUrl: string
}

export function LandingHeader({ planUrl }: Props) {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="text-xl font-bold tracking-tight text-slate-900">
          Fin<span className="text-primary-600">Pilot</span>
        </Link>
        <nav className="flex items-center gap-3">
          <a
            href="#faq"
            className="hidden text-sm font-medium text-slate-600 hover:text-slate-900 sm:inline"
          >
            Câu hỏi thường gặp
          </a>
          <CtaButton href={planUrl} className="!px-5 !py-2.5 text-sm" />
        </nav>
      </div>
    </header>
  )
}
