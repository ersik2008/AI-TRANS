"use client"

import { useState } from "react"
import FileUpload from "@/components/file-upload"
import ProcessingPanel from "@/components/processing-panel"
import { ArrowLeft } from "lucide-react"

interface UploadSectionProps {
  onBack: () => void
}

export default function UploadSection({ onBack }: UploadSectionProps) {
  const [file, setFile] = useState<File | null>(null)
  const [targetLanguage, setTargetLanguage] = useState<"ru" | "en" | "kk">("en")
  const [jobId, setJobId] = useState<string | null>(null)

  const handleUpload = async (uploadedFile: File) => {
    setFile(uploadedFile)
    // Job creation will be handled in ProcessingPanel
  }

  const handleJobCreated = (id: string) => {
    setJobId(id)
  }

  return (
    <section className="min-h-screen pt-32 pb-20 px-6">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Back
        </button>

        {!jobId ? (
          <div className="space-y-8">
            <div>
              <h1 className="text-4xl font-bold mb-2">Upload Your Media</h1>
              <p className="text-text-secondary text-lg">Choose a file to recognize text and translate</p>
            </div>

            <FileUpload onFileSelect={handleUpload} />

            {file && (
              <div className="glass-effect p-6 space-y-6">
                <div>
                  <label className="block text-sm font-medium mb-3">Target Language</label>
                  <div className="grid grid-cols-3 gap-4">
                    {[
                      { code: "ru", label: "Russian" },
                      { code: "en", label: "English" },
                      { code: "kk", label: "Kazakh" },
                    ].map((lang) => (
                      <button
                        key={lang.code}
                        onClick={() => setTargetLanguage(lang.code as "ru" | "en" | "kk")}
                        className={`py-3 px-4 rounded-lg font-medium transition-all ${
                          targetLanguage === lang.code
                            ? "bg-primary text-white"
                            : "bg-surface-elevated text-text-secondary hover:bg-surface"
                        }`}
                      >
                        {lang.label}
                      </button>
                    ))}
                  </div>
                </div>

                <ProcessingPanel file={file} targetLanguage={targetLanguage} onJobCreated={handleJobCreated} />
              </div>
            )}
          </div>
        ) : (
          <ProcessingPanel file={file!} targetLanguage={targetLanguage} jobId={jobId} onJobCreated={handleJobCreated} />
        )}
      </div>
    </section>
  )
}
