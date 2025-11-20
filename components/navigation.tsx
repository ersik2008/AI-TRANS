"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"

interface NavigationProps {
  onUploadClick: () => void
}

export default function Navigation({ onUploadClick }: NavigationProps) {
  return (
    <nav className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl border-b border-border">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-gradient-primary flex items-center justify-center">
            <span className="text-xl font-bold text-white">A</span>
          </div>
          <span className="text-xl font-bold text-text-primary">AI-Translate</span>
        </div>

        <div className="hidden md:flex items-center gap-8">
          <Link href="#features" className="text-text-secondary hover:text-text-primary transition-colors">
            Features
          </Link>
          <Link href="#how-it-works" className="text-text-secondary hover:text-text-primary transition-colors">
            How it works
          </Link>
          <Link href="#pricing" className="text-text-secondary hover:text-text-primary transition-colors">
            Pricing
          </Link>
        </div>

        <Button
          onClick={onUploadClick}
          className="bg-primary hover:bg-primary-dark text-white font-semibold rounded-full px-6"
        >
          Start Translating
        </Button>
      </div>
    </nav>
  )
}
