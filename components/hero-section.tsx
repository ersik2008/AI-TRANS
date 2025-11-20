"use client"

import { Button } from "@/components/ui/button"
import { ArrowRight, Zap } from "lucide-react"

interface HeroSectionProps {
  onGetStarted: () => void
}

export default function HeroSection({ onGetStarted }: HeroSectionProps) {
  return (
    <section className="pt-40 pb-20 px-6 relative overflow-hidden">
      {/* Background gradient elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl opacity-50"></div>
        <div className="absolute bottom-0 right-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl opacity-50"></div>
      </div>

      <div className="max-w-4xl mx-auto text-center relative z-10">
        <div className="inline-flex items-center gap-2 mb-8 px-4 py-2 rounded-full bg-surface border border-border">
          <Zap className="w-4 h-4 text-accent" />
          <span className="text-sm text-text-secondary">Powered by AI</span>
        </div>

        <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-text-primary via-primary-light to-accent bg-clip-text text-transparent">
          Recognize & Translate Instantly
        </h1>

        <p className="text-xl md:text-2xl text-text-secondary mb-12 leading-relaxed">
          Extract text and speech from any media file. Translate to Russian, English, or Kazakh with AI precision.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button
            onClick={onGetStarted}
            className="bg-primary hover:bg-primary-dark text-white px-8 py-6 rounded-lg font-semibold text-lg flex items-center gap-2 group"
          >
            Get Started
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Button>
          <Button
            variant="outline"
            className="px-8 py-6 rounded-lg font-semibold text-lg border-border hover:bg-surface-elevated bg-transparent"
          >
            Watch Demo
          </Button>
        </div>
      </div>
    </section>
  )
}
