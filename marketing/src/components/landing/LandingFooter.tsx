export function LandingFooter() {
  const year = new Date().getFullYear()
  return (
    <footer className="border-t border-slate-200 bg-white py-10">
      <div className="mx-auto max-w-6xl px-4 text-center text-sm text-slate-500">
        <p>© {year} FinPilot. Lập kế hoạch tài chính cá nhân cho người Việt.</p>
        <p className="mt-2 text-xs text-slate-400">
          Thông tin trên trang mang tính giới thiệu; sản phẩm thực tế có thể khác theo từng giai đoạn phát triển.
        </p>
      </div>
    </footer>
  )
}
