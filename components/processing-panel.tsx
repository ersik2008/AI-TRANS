"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Loader2, Check, Copy } from "lucide-react"
import axios from "axios"

interface Segment {
  start: number;
  end: number;
  text: string;
}

interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  text: string;
  confidence: number;
}

interface ProcessingPanelProps {
  file: File
  targetLanguage: "ru" | "en" | "kk"
  jobId?: string
  onJobCreated: (id: string) => void
}

const LANGUAGE_NAMES = {
  ru: "Russian",
  en: "English",
  kk: "Kazakh",
}

export default function ProcessingPanel({
  file,
  targetLanguage,
  jobId: initialJobId,
  onJobCreated,
}: ProcessingPanelProps) {
  const [jobId, setJobId] = useState(initialJobId)
  const [status, setStatus] = useState("uploading")
  const [result, setResult] = useState(null)
  const [sourceText, setSourceText] = useState("")
  const [translatedText, setTranslatedText] = useState("")
  const [segments, setSegments] = useState<Segment[]>([])
  const [imageBboxes, setImageBboxes] = useState<BoundingBox[]>([])
  const [audioUrl, setAudioUrl] = useState("")
  const [error, setError] = useState("")
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (!jobId && !initialJobId) {
      uploadFile()
    } else if (initialJobId) {
      setStatus("processing")
      pollResults(initialJobId)
    }
  }, [initialJobId])

  const uploadFile = async () => {
    try {
      setStatus("uploading")
      const formData = new FormData()
      formData.append("file", file)
      formData.append("target_language", targetLanguage)  // Здесь фикс: "target_lang" вместо "target_language"

      const response = await axios.post("http://localhost:8000/api/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })

      const newJobId = response.data.job_id
      setJobId(newJobId)
      onJobCreated(newJobId)
      setStatus("processing")
      pollResults(newJobId)
    } catch (err: unknown) {
      let errorMessage = (err as any).response?.data?.detail || "Failed to upload file. Check file type and backend logs."
      if (typeof errorMessage !== 'string') {
        errorMessage = JSON.stringify(errorMessage)  // Ensure it's a string to avoid React render error
      }
      setError(errorMessage)
      setStatus("error")
    }
  }

  const pollResults = async (id: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/result/${id}`)
        const data = response.data

        setResult(data)  // Store full result

        if (data.status === "completed") {
          setSourceText(data.source_text || "")
          setTranslatedText(data.translated_text || "")
          setSegments(data.segments || [])
          setImageBboxes(data.image_bboxes || [])
          setAudioUrl(data.audio_url || "")
          setStatus("completed")
          clearInterval(interval)
        } else if (data.status === "failed") {
          setError(data.error_message || "Processing failed. Check backend logs for details.")
          setStatus("error")
          clearInterval(interval)
        } else if (data.status === "pending" || data.status === "processing") {
          // Continue polling for pending or processing
        } else {
          setError("Unknown job status: " + data.status)
          setStatus("error")
          clearInterval(interval)
        }
      } catch (err: unknown) {
        setError("Failed to fetch results: " + ((err as any).message || "Unknown error"))
        setStatus("error")
        clearInterval(interval)
      }
    }, 2000)  // Poll every 2 seconds to reduce load

    return () => clearInterval(interval)
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const statusSteps = [
    { id: "uploading", label: "Uploading" },
    { id: "processing", label: "Processing" },
    { id: "completed", label: "Completed" },
  ]

  return (
    <div className="space-y-8">
      {/* Progress indicator */}
      <div className="glass-effect p-6 rounded-lg">
        <div className="flex items-center justify-between mb-4">
          {statusSteps.map((step, idx) => (
            <div key={step.id} className="flex items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
                  status === step.id || statusSteps.findIndex((s) => s.id === status) > idx
                    ? "bg-primary text-white"
                    : "bg-surface text-text-secondary"
                }`}
              >
                {statusSteps.findIndex((s) => s.id === status) > idx ? (
                  <Check className="w-6 h-6" />
                ) : status === step.id ? (
                  <Loader2 className="w-6 h-6 animate-spin" />
                ) : (
                  idx + 1
                )}
              </div>
              {idx < statusSteps.length - 1 && (
                <div
                  className={`h-1 flex-1 mx-2 rounded-full ${
                    statusSteps.findIndex((s) => s.id === status) > idx ? "bg-primary" : "bg-border"
                  }`}
                />
              )}
            </div>
          ))}
        </div>
        <p className="text-center text-text-secondary">
          {status === "uploading" && "Uploading your file..."}
          {status === "processing" && "Recognizing text and translating..."}
          {status === "completed" && "Translation complete!"}
          {status === "error" && "An error occurred"}
        </p>
      </div>

      {/* Results */}
      {status === "completed" && result && (
        <div className="grid md:grid-cols-2 gap-6">
          <div className="glass-effect p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-4 flex items-center justify-between">
              Source Text
              <button
                onClick={() => copyToClipboard(sourceText)}
                className="p-2 hover:bg-surface rounded-lg transition-colors"
              >
                <Copy className={`w-5 h-5 ${copied ? "text-success" : "text-text-secondary"}`} />
              </button>
            </h3>
            <p className="text-text-secondary leading-relaxed whitespace-pre-wrap">{sourceText}</p>
          </div>

          <div className="glass-effect p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-4 flex items-center justify-between">
              Translation ({LANGUAGE_NAMES[targetLanguage]})
              <button
                onClick={() => copyToClipboard(translatedText)}
                className="p-2 hover:bg-surface rounded-lg transition-colors"
              >
                <Copy className={`w-5 h-5 ${copied ? "text-success" : "text-text-secondary"}`} />
              </button>
            </h3>
            <p className="text-text-secondary leading-relaxed whitespace-pre-wrap">{translatedText}</p>
          </div>

          {/* Segments */}
          {segments.length > 0 && (
            <div className="glass-effect p-6 rounded-lg md:col-span-2">
              <h3 className="text-lg font-semibold mb-4">Segments</h3>
              <ul className="space-y-2">
                {segments.map((seg, idx) => (
                  <li key={idx} className="text-text-secondary">
                    [{seg.start.toFixed(1)}s - {seg.end.toFixed(1)}s]: {seg.text}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Image Bboxes */}
          {imageBboxes.length > 0 && (
            <div className="glass-effect p-6 rounded-lg md:col-span-2">
              <h3 className="text-lg font-semibold mb-4">Recognized Text (OCR)</h3>
              <ul className="space-y-2">
                {imageBboxes.map((bbox, idx) => (
                  <li key={idx} className="text-text-secondary">
                    {bbox.text} (confidence: {bbox.confidence.toFixed(2)}, position: x={bbox.x}, y={bbox.y}, w={bbox.width}, h={bbox.height})
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Audio */}
          {audioUrl && (
            <div className="glass-effect p-6 rounded-lg md:col-span-2">
              <h3 className="text-lg font-semibold mb-4">Generated Audio</h3>
              <audio controls src={`http://localhost:8000${audioUrl}`} className="w-full">
                Your browser does not support the audio element.
              </audio>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="glass-effect p-6 rounded-lg border border-error bg-error/10">
          <p className="text-error font-medium">{error}</p>
          <Button onClick={uploadFile} className="mt-4 bg-primary hover:bg-primary-dark">
            Try Again
          </Button>
        </div>
      )}
    </div>
  )
}