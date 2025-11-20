"use client"

import type React from "react"

import { useCallback } from "react"
import { Upload, FileAudio, FileVideo, ImageIcon } from "lucide-react"

interface FileUploadProps {
  onFileSelect: (file: File) => void
}

export default function FileUpload({ onFileSelect }: FileUploadProps) {
  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault()
      const files = e.dataTransfer.files
      if (files.length > 0) {
        onFileSelect(files[0])
      }
    },
    [onFileSelect],
  )

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.currentTarget.files
    if (files && files.length > 0) {
      onFileSelect(files[0])
    }
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      className="glass-effect border-2 border-dashed border-border rounded-xl p-12 text-center cursor-pointer hover:border-primary transition-colors group"
    >
      <input type="file" onChange={handleChange} accept="audio/*,video/*,image/*" className="hidden" id="file-input" />
      <label htmlFor="file-input" className="cursor-pointer block">
        <div className="w-16 h-16 rounded-lg bg-gradient-primary flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
          <Upload className="w-8 h-8 text-white" />
        </div>
        <h3 className="text-xl font-semibold mb-2">Drop your file here</h3>
        <p className="text-text-secondary mb-4">or click to browse</p>

        <div className="flex items-center justify-center gap-6 text-text-tertiary">
          <div className="flex items-center gap-2">
            <FileAudio className="w-5 h-5" />
            <span className="text-sm">Audio</span>
          </div>
          <div className="flex items-center gap-2">
            <FileVideo className="w-5 h-5" />
            <span className="text-sm">Video</span>
          </div>
          <div className="flex items-center gap-2">
            <ImageIcon className="w-5 h-5" />
            <span className="text-sm">Image</span>
          </div>
        </div>
      </label>
    </div>
  )
}
