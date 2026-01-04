"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, Upload, FileText, Download, Copy } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { useToast } from "@/hooks/use-toast"
import Link from "next/link"
import Image from "next/image"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"

import { api } from "@/lib/api"  // import your new API wrapper

export function Summariser() {
  const [summaryFile, setSummaryFile] = useState<File | null>(null)
  const [summaryResult, setSummaryResult] = useState<string>("")
  const [rawResult, setRawResult] = useState<any>(null)
  const [isProcessingSummary, setIsProcessingSummary] = useState(false)
  const [options, setOptions] = useState({
    extract_keywords: true,
    extract_concepts: true,
    extract_questions: false
  })
  
  const { toast } = useToast()

  const handleSummaryUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSummaryFile(file)
      toast({ title: "File Uploaded", description: file.name })
    }
  }

  const handleGenerate = async () => {
    if (!summaryFile) {
      toast({ title: "No File", description: "Please upload a file first.", variant: "destructive" })
      return
    }

    setIsProcessingSummary(true)

    try {
      const result = await api.summariseNotes(summaryFile, options)
      setSummaryResult(result.summary || "No summary returned")
      setRawResult(result)
      toast({ title: "Summary Generated", description: `Processed ${summaryFile.name}` })
    } catch (error) {
      console.error("API call failed:", error)
      setSummaryResult("Error generating summary. Please check backend connection.")
      toast({ title: "Error", description: "Failed to generate summary.", variant: "destructive" })
    } finally {
      setIsProcessingSummary(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({ title: "Copied", description: "Summary copied to clipboard." })
  }

  const downloadContent = (content: string, filename: string) => {
    const blob = new Blob([content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const downloadPDF = async () => {
    if (!rawResult) return
    try {
      const blob = await api.exportPDF("summary", rawResult, "summary")
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "Summary.pdf"
      a.click()
      URL.revokeObjectURL(url)
      toast({ title: "Downloaded", description: "PDF downloaded successfully." })
    } catch (error) {
      console.error("PDF download failed", error)
      toast({ title: "Error", description: "Failed to download PDF.", variant: "destructive" })
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}

      <header className="bg-background/80 backdrop-blur-md border-b border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <Image src="/logo.png"alt="EduMate Logo"width={36} height={36} className="rounded-md"/>
                       
            <h1 className="text-xl font-bold text-foreground">AI Academic Assistant</h1>
          </div>
          <div className="flex items-center space-x-3">
            <Button asChild>
              <Link href="/dashboard">Back to Dashboard</Link>
            </Button>
            <ThemeToggle />
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
     
          <h2 className="text-3xl font-bold mb-4 text-foreground">Summarise Your Notes</h2>
          <p className="text-lg text-muted-foreground">Upload your notes for intelligent summarisation.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Options Column */}
          <Card className="md:col-span-1 h-fit">
            <CardHeader>
              <CardTitle>Options</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox 
                  id="keywords" 
                  checked={options.extract_keywords}
                  onCheckedChange={(c) => setOptions({...options, extract_keywords: !!c})}
                />
                <Label htmlFor="keywords">Extract Keywords</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox 
                  id="concepts" 
                  checked={options.extract_concepts}
                  onCheckedChange={(c) => setOptions({...options, extract_concepts: !!c})}
                />
                <Label htmlFor="concepts">Extract Key Concepts</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox 
                  id="questions" 
                  checked={options.extract_questions}
                  onCheckedChange={(c) => setOptions({...options, extract_questions: !!c})}
                />
                <Label htmlFor="questions">Generate Study Questions</Label>
              </div>

              <Button onClick={handleGenerate} disabled={!summaryFile || isProcessingSummary} className="w-full mt-4">
                {isProcessingSummary ? "Processing..." : "Summarise"}
              </Button>
            </CardContent>
          </Card>

          {/* Upload & Output Column */}
          <div className="md:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5 text-primary" />
                  <span>Upload Notes</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary">
                  <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-lg font-medium text-foreground">
                    {summaryFile ? summaryFile.name : "Drop your files here or click to browse"}
                  </p>
                  <p className="text-sm text-muted-foreground">Supports PPT, DOC, PDF, TXT</p>
                  <input id="upload-notes" type="file" className="hidden" onChange={handleSummaryUpload} />
                  <Button onClick={() => document.getElementById("upload-notes")?.click()} className="mt-4" variant="outline">
                    {summaryFile ? "Change File" : "Browse"}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {summaryResult && (
              <Card>
                <CardHeader className="flex justify-between items-center">
                  <CardTitle>Summary Result</CardTitle>
                  <div className="flex space-x-2">
                    <Button size="sm" variant="outline" onClick={() => copyToClipboard(summaryResult)}>
                      <Copy className="h-4 w-4 mr-2" /> Copy
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => downloadContent(summaryResult, "summary.txt")}>
                      <Download className="h-4 w-4 mr-2" /> TXT
                    </Button>
                    <Button size="sm" onClick={downloadPDF}>
                      <FileText className="h-4 w-4 mr-2" /> PDF
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="prose dark:prose-invert max-w-none">
                    <pre className="whitespace-pre-wrap font-sans text-sm">
                      {summaryResult}
                    </pre>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
