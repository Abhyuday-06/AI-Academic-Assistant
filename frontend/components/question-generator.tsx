"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Upload, FileText, Download, Copy } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"
import { useToast } from "@/hooks/use-toast"
import { api } from "@/lib/api"  // API wrapper
import Link from "next/link"
import Image from "next/image"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"

export function QuestionGenerator() {
  const [syllabusFile, setSyllabusFile] = useState<File | null>(null)
  const [samplePaperResult, setSamplePaperResult] = useState<string>("")
  const [rawResult, setRawResult] = useState<any>(null)
  const [isProcessingSamplePaper, setIsProcessingSamplePaper] = useState(false)
  const [testType, setTestType] = useState<string>("CAT-1")
  const [selectedModules, setSelectedModules] = useState<string[]>(["Module 1", "Module 2"])
  
  const { toast } = useToast()

  const modulesList = Array.from({ length: 8 }, (_, i) => `Module ${i + 1}`)

  const handleModuleChange = (module: string) => {
    setSelectedModules(prev => 
      prev.includes(module) 
        ? prev.filter(m => m !== module)
        : [...prev, module]
    )
  }

  const handleSelectAll = () => {
    setSelectedModules(modulesList)
  }

  const handleDeselectAll = () => {
    setSelectedModules([])
  }

  // Handle File Upload + API Call
  const handleGenerate = async () => {
    if (!syllabusFile) {
      toast({ title: "No File", description: "Please upload a syllabus file first.", variant: "destructive" })
      return
    }
    if (selectedModules.length === 0) {
      toast({ title: "No Modules", description: "Please select at least one module.", variant: "destructive" })
      return
    }

    setIsProcessingSamplePaper(true)

    try {
      // Call FastAPI backend
      const result = await api.generateQuestions(syllabusFile, testType, selectedModules)
      setSamplePaperResult(result.questions || "No questions returned")
      setRawResult(result.raw)
      toast({ title: "Paper Generated", description: `Created from ${syllabusFile.name}` })
    } catch (error) {
      console.error("API call failed:", error)
      setSamplePaperResult("Error generating paper. Please check backend connection.")
      toast({ title: "Error", description: "Failed to generate paper.", variant: "destructive" })
    } finally {
      setIsProcessingSamplePaper(false)
    }
  }

  const handleSyllabusUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSyllabusFile(file)
      toast({ title: "File Uploaded", description: file.name })
    }
  }

  // Copy to Clipboard
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({ title: "Copied", description: "Sample paper copied to clipboard." })
  }

  // Download as File
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
      const blob = await api.exportPDF("question-paper", rawResult, "question_paper")
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = "Question_Paper.pdf"
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
      <header className="bg-background/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <Image
              src="/logo.png"
              alt="EduMate Logo"
              width={36}
              height={36}
              className="rounded-md"
            />
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              AI Academic Assistant
            </h1>
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
          <h2 className="text-3xl font-bold mb-4 text-gray-900 dark:text-white">
            Generate Sample Papers
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Upload syllabus to generate exam-style papers.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Controls Column */}
          <Card className="md:col-span-1 h-fit">
            <CardHeader>
              <CardTitle>Configuration</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              
              {/* Test Type */}
              <div className="space-y-2">
                <Label>Test Type</Label>
                <Select value={testType} onValueChange={setTestType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="CAT-1">CAT-1 (50 Marks)</SelectItem>
                    <SelectItem value="CAT-2">CAT-2 (50 Marks)</SelectItem>
                    <SelectItem value="FAT">FAT (100 Marks)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Modules */}
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <Label>Modules to Cover</Label>
                  <div className="flex space-x-2 text-xs">
                    <button onClick={handleSelectAll} className="text-primary hover:underline">All</button>
                    <span className="text-muted-foreground">|</span>
                    <button onClick={handleDeselectAll} className="text-primary hover:underline">None</button>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {modulesList.map((mod) => (
                    <div key={mod} className="flex items-center space-x-2">
                      <Checkbox 
                        id={mod} 
                        checked={selectedModules.includes(mod)}
                        onCheckedChange={() => handleModuleChange(mod)}
                      />
                      <label htmlFor={mod} className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                        {mod}
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              <Button onClick={handleGenerate} disabled={!syllabusFile || isProcessingSamplePaper} className="w-full">
                {isProcessingSamplePaper ? "Generating..." : "Generate Paper"}
              </Button>

            </CardContent>
          </Card>

          {/* Upload & Output Column */}
          <div className="md:col-span-2 space-y-6">
            {/* Upload Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <FileText className="h-5 w-5" />
                  <span>Upload Syllabus</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-blue-400">
                  <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-lg font-medium">
                    {syllabusFile ? syllabusFile.name : "Drop your syllabus or click to browse"}
                  </p>
                  <p className="text-sm text-gray-500">Supports DOC, PDF, TXT</p>
                  <input
                    id="upload-syllabus"
                    type="file"
                    className="hidden"
                    onChange={handleSyllabusUpload}
                  />
                  <Button onClick={() => document.getElementById("upload-syllabus")?.click()} className="mt-4" variant="outline">
                    {syllabusFile ? "Change File" : "Browse Files"}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Output Card */}
            {samplePaperResult && (
              <Card>
                <CardHeader className="flex justify-between items-center">
                  <CardTitle>Sample Paper</CardTitle>
                  <div className="flex space-x-2">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => copyToClipboard(samplePaperResult)}
                    >
                      <Copy className="h-4 w-4 mr-2" />
                      Copy
                    </Button>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => downloadContent(samplePaperResult, "sample-paper.txt")}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      TXT
                    </Button>
                    <Button
                      size="sm"
                      onClick={downloadPDF}
                    >
                      <FileText className="h-4 w-4 mr-2" />
                      PDF
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <pre className="whitespace-pre-wrap text-sm font-mono bg-muted p-4 rounded-md overflow-auto max-h-[500px]">
                    {samplePaperResult}
                  </pre>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
