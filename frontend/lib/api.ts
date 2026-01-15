"use client"
import axios from "axios"

// Change this to your backend FastAPI base URL
const API = axios.create({
  baseURL: "http://localhost:8000",
})

// Attach token  if available
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const api = {
  // Auth
  signup: async (email: string, password: string, name?: string) => {
    const res = await API.post("/auth/signup", { email, password, name })
    return res.data // { message, user }
  },

  login: async (email: string, password: string) => {
    const res = await API.post("/auth/login", { email, password })
    // Save token for later requests
    if (res.data?.access_token) {
      localStorage.setItem("token", res.data.access_token)
    }
    return res.data // { access_token, refresh_token, user }
  },

  logout: () => {
    localStorage.removeItem("token")
  },

  // Profile
  getProfile: async () => {
    const res = await API.get("/profile")
    return res.data // { name, email, institution, studyLevel, major, joinDate }
  },

  updateProfile: async (profile: any) => {
    const res = await API.put("/profile", profile, {
      headers: { "Content-Type": "application/json" },
    })
    return res.data // updated profile object
  },

  // Notes & AI Features
  summariseNotes: async (file: File, options: { extract_keywords: boolean, extract_concepts: boolean, extract_questions: boolean }) => {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("extract_keywords", options.extract_keywords.toString())
    formData.append("extract_concepts", options.extract_concepts.toString())
    formData.append("extract_questions", options.extract_questions.toString())

    const res = await API.post("/generate-summary", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    // The backend returns { parsed_content: "...", ... }
    // The frontend expects { summary: "..." }
    return {
      summary: res.data.parsed_content,
      ...res.data
    }
  },

  generateQuestions: async (file: File, testType: string, modules: string[]) => {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("test_type", testType)
    formData.append("modules", modules.join(","))

    const res = await API.post("/generate-question-paper", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    
    // The backend returns { question_paper: { paper: [ { q_no, marks, parts: [{text, marks, module}] } ] } }
    
    const paper = res.data.question_paper?.paper || []
    
    // Format the question paper for display
    const textRepresentation = paper.map((q: any) => {
      const partsText = q.parts.map((p: any, idx: number) => {
        const label = p.label ? `(${p.label})` : String.fromCharCode(97 + idx) + "."
        return `   ${label} ${p.text} [${p.marks} marks] (Module: ${p.module.join(", ")})`
      }).join("\n")
      
      return `Q${q.q_no}. [${q.marks} marks]\n${partsText}`
    }).join("\n\n")

    return {
      questions: textRepresentation,
      raw: res.data
    }
  },

  exportPDF: async (type: "summary" | "question-paper", data: any, filename: string) => {
    const res = await API.post("/export-pdf", {
      export_type: type,
      data: data,
      filename: filename
    }, {
      responseType: 'blob' // Important for binary file download
    })
    return res.data
  },

  // Activity
  getRecentActivity: async () => {
    const res = await API.get("/activity")
    return res.data
  },
}
