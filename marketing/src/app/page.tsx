import { CTASection } from '@/components/landing/CTASection'
import { FAQSection } from '@/components/landing/FAQSection'
import { FeatureSection } from '@/components/landing/FeatureSection'
import { HeroSection } from '@/components/landing/HeroSection'
import { LandingFooter } from '@/components/landing/LandingFooter'
import { LandingHeader } from '@/components/landing/LandingHeader'
import { ProblemSection } from '@/components/landing/ProblemSection'
import { SolutionSection } from '@/components/landing/SolutionSection'
import { TrustSection } from '@/components/landing/TrustSection'
import { WowSection } from '@/components/landing/WowSection'
import { getAppPlanUrl } from '@/lib/app-url'

export default function MarketingHome() {
  const planUrl = getAppPlanUrl()

  return (
    <>
      <LandingHeader planUrl={planUrl} />
      <main>
        <HeroSection planUrl={planUrl} />
        <ProblemSection />
        <SolutionSection />
        <WowSection />
        <FeatureSection />
        <TrustSection />
        <CTASection planUrl={planUrl} />
        <FAQSection />
      </main>
      <LandingFooter />
    </>
  )
}
