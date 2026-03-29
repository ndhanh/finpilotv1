import { CtaButton } from './CtaButton'

type Props = {
  planUrl: string
}

export function CTASection({ planUrl }: Props) {
  return (
    <section className="bg-gradient-to-br from-primary-600 to-primary-800 py-16 md:py-24">
      <div className="mx-auto max-w-3xl px-4 text-center">
        <h2 className="text-3xl font-bold text-white md:text-4xl">
          Sẵn sàng nhìn thấy lộ trình của chính bạn?
        </h2>
        <p className="mt-4 text-lg text-primary-100">
          Vài phút để nhập thông tin cơ bản — bạn nhận góc nhìn rõ ràng hơn về mục tiêu tài chính, không cần
          đăng ký tài khoản để bắt đầu.
        </p>
        <div className="mt-10 flex flex-col items-center gap-4">
          <CtaButton
            href={planUrl}
            className="bg-white !text-primary-700 shadow-lg hover:!bg-slate-50 hover:!text-primary-800"
          />
          <p className="text-sm text-primary-200/90">Không cần đăng nhập · Bắt đầu miễn phí</p>
        </div>
      </div>
    </section>
  )
}
