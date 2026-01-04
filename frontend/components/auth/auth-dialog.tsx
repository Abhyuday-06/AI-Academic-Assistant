"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"
import { SignInForm } from "./sign-in-form"
import { SignUpForm } from "./sign-up-form"

interface AuthDialogProps {
  children: React.ReactNode
  defaultMode?: "signin" | "signup"
}

export function AuthDialog({ children, defaultMode = "signin" }: AuthDialogProps) {
  const [open, setOpen] = useState(false)
  const [mode, setMode] = useState<"signin" | "signup">(defaultMode)

  const handleClose = () => {
    setOpen(false)
  }

  const switchToSignIn = () => {
    setMode("signin")
  }

  const switchToSignUp = () => {
    setMode("signup")
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-md p-0 gap-0">
        {mode === "signin" ? (
          <SignInForm onClose={handleClose} onSwitchToSignUp={switchToSignUp} />
        ) : (
          <SignUpForm onClose={handleClose} onSwitchToSignIn={switchToSignIn} />
        )}
      </DialogContent>
    </Dialog>
  )
}
