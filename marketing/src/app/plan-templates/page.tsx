"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * Marketing Site Template Selection Route
 *
 * Implements Option B: Redirect to the frontend plan-templates route
 * Marketing site visitors are redirected to the actual app for template selection
 */
export default function MarketingPlanTemplatesPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to the frontend application's plan-templates page
    // In production, adjust the domain as needed (NEXT_PUBLIC_FRONTEND_URL or similar)
    const frontendUrl =
      process.env.NEXT_PUBLIC_FRONTEND_URL || "http://localhost:3000";
    window.location.href = `${frontendUrl}/plan-templates`;
  }, [router]);

  // Show loading state while redirecting
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-flex items-center justify-center mb-4">
          <div className="w-8 h-8 border-4 border-blue-500 border-t-blue-600 rounded-full animate-spin"></div>
        </div>
        <p className="text-gray-600">Redirecting to template selection...</p>
      </div>
    </div>
  );
}
