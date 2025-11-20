import { FileText, Languages, Zap, Lock } from "lucide-react"

const features = [
  {
    icon: FileText,
    title: "Multi-Format Support",
    description: "Process audio, video, and images all in one place.",
  },
  {
    icon: Languages,
    title: "3 Language Support",
    description: "Translate to Russian, English, or Kazakh instantly.",
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "Advanced AI models for accurate and quick results.",
  },
  {
    icon: Lock,
    title: "Secure & Private",
    description: "Your data is encrypted and never stored on our servers.",
  },
]

export default function FeaturesSection() {
  return (
    <section id="features" className="py-20 px-6 bg-gradient-to-b from-transparent to-surface/50">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">Powerful Features</h2>
          <p className="text-text-secondary text-lg">Everything you need for professional translation</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <div key={index} className="glass-effect card-hover p-6">
                <div className="w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center mb-4">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-text-secondary text-sm">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
