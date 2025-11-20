"use client"

import { useState } from "react"
import Navigation from "@/components/navigation"
import HeroSection from "@/components/hero-section"
import FeaturesSection from "@/components/features-section"
import UploadSection from "@/components/upload-section"
import Footer from "@/components/footer"

export default function Home() {
  const [showUpload, setShowUpload] = useState(false)

  return (
    <main className="min-h-screen bg-background">
      <Navigation onUploadClick={() => setShowUpload(true)} />
      {!showUpload ? (
        <>
          <HeroSection onGetStarted={() => setShowUpload(true)} />
          <FeaturesSection />
        </>
      ) : (
        <UploadSection onBack={() => setShowUpload(false)} />
      )}
      <Footer />
    </main>
  )
}
