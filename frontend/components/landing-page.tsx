"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Brain, BookOpen, MessageSquare, Menu, X, LogIn, UserPlus } from "lucide-react"
import Link from "next/link"
import { ThemeToggle } from "@/components/theme-toggle"
import { AuthDialog } from "@/components/auth/auth-dialog"
import Image from "next/image"
import Lottie from "lottie-react"
import studentAnimation from "@/public/animations/student.json"



const features = [
  {
    icon: BookOpen,
    title: "One-Click Summaries",
    description: "Get bite-sized notes from pages of content.",
  },
  {
    icon: MessageSquare,
    title: "Smart Practice Questions",
    description: "Generate exam-style questions instantly from syllabus.",
  },
]

export function LandingPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-md ">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-8">
          <div className="flex justify-between items-center h-14 sm:h-16">
            <div className="flex items-center space-x-2">
               <Image src="/logo.png"alt="EduMate Logo"width={36} height={36} className="rounded-md"/>
              <span className="text-lg sm:text-xl font-bold">Academic Assistant</span>
            </div>

            <div className="hidden md:flex items-center space-x-6 lg:space-x-8">
              <Link
                href="#features"
                className="text-muted-foreground hover:text-primary transition-colors text-sm lg:text-base"
              >
                Features
              </Link>
              <ThemeToggle />
              <div className="flex items-center space-x-3">
                <AuthDialog defaultMode="signin">
                  <Button variant="outline" size="sm" className="text-sm bg-transparent">
                    Sign In
                  </Button>
                </AuthDialog>
                <AuthDialog defaultMode="signup">
                  <Button size="sm" className="text-sm">
                    Sign Up
                  </Button>
                </AuthDialog>
              </div>
            </div>

            <div className="md:hidden flex items-center space-x-2">
              <ThemeToggle />
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="h-8 w-8"
              >
                {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
              </Button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-background border-t border-border">
            <div className="px-3 py-2 space-y-2">
              <Link
                href="#features"
                className="block py-2 text-muted-foreground hover:text-primary text-sm"
              >
                Features
              </Link>
              <div className="flex flex-col space-y-2 pt-2">
                <AuthDialog defaultMode="signin">
                  <Button variant="outline" size="sm" className="w-full justify-start bg-transparent">
                    
                    Sign In
                  </Button>
                </AuthDialog>
                <AuthDialog defaultMode="signup">
                  <Button size="sm" className="w-full justify-start">
                 
                    Sign Up
                  </Button>
                </AuthDialog>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="py-4 sm:py-6 lg:py-8 px-3 sm:px-4 lg:px-8">
  <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
    
    {/* Left: Text + CTAs */}
    <div className="text-center md:text-left">
      <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 sm:mb-6">
        Your Personalized AI Study Partner
      </h1>
      <p className="text-base sm:text-lg lg:text-xl text-muted-foreground mb-6 sm:mb-8 max-w-xl">
        Tired of drowning in notes? Take help to summarize, practice, and make yourself exam-ready in minutes.
      </p>

      {/* CTA Buttons */}
<div className="pt-8 flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center md:justify-start mt-2">
  <AuthDialog defaultMode="signup">
    <Button size="lg" className="text-base sm:text-lg px-6 sm:px-8 py-2 sm:py-3 w-full sm:w-auto">
      Get Started Free
    </Button>
  </AuthDialog>
  <AuthDialog defaultMode="signin">
    <Button
      variant="outline"
      size="lg"
      className="text-base sm:text-lg px-6 sm:px-8 py-2 sm:py-3 bg-transparent w-full sm:w-auto"
    >
      Sign In
    </Button>
  </AuthDialog>
</div>


      <p className="text-xs sm:text-sm text-muted-foreground mt-4">
        Access through Guest Mode?{" "}
        <Link href="/dashboard" className="text-primary hover:underline">
          Click here!
        </Link>
      </p>
    </div>

    {/* Right: Animation */}
    <div className="flex justify-center md:justify-end">
      <Lottie 
        animationData={studentAnimation} 
        loop={true} 
        className="w-full max-w-md"
      />
    </div>
  </div>
</section>



      <section
  id="features"
  className="py-12 sm:py-16 lg:py-20 px-3 sm:px-4 lg:px-8 bg-card text-card-foreground"
>
  <div className="max-w-7xl mx-auto">
    <div className="text-center mb-12 sm:mb-16">
      <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-3 sm:mb-4">
         Features
      </h2>

    </div>

    <div className="flex flex-wrap justify-center gap-6 sm:gap-8">
  {features.map((feature, index) => (
    <Card
      key={index}
      className="p-4 sm:p-6 hover:shadow-lg transition-shadow w-72 sm:w-80 lg:w-96 flex justify-center"
    >
      <CardContent className="p-0 flex flex-col items-center text-center">
        <feature.icon className="h-10 w-10 sm:h-12 sm:w-12 text-primary mb-3 sm:mb-4" />
        <h3 className="text-lg sm:text-xl font-semibold mb-2">
          {feature.title}
        </h3>
        <p className="text-sm sm:text-base text-muted-foreground">
          {feature.description}
        </p>
      </CardContent>
    </Card>
  ))}
</div>

  </div>
</section>

      

      {/* Footer */}
     <footer className="bg-secondary text-secondary-foreground py-1 sm:py-3 px-3 sm:px-4 lg:px-8">
  <div className="max-w-7xl mx-auto">
    <div className=" mt-2 sm:mt-1 pt-1 sm:pt-1 text-center text-muted-foreground">
      <p className="text-s">&copy; 2025 AI Academic Assistant. All rights reserved.</p>
    </div>
  </div>
</footer>
    </div>
  )
}
