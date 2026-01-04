"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import Image from "next/image"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  LayoutDashboard,
  HelpCircle,
  User,
  LogOut,
  Menu,
  X,
  FileText,
} from "lucide-react"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { ThemeToggle } from "@/components/theme-toggle"
import { cn } from "@/lib/utils"

const sidebarItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
  { icon: FileText, label: "Summarise Notes", href: "/summariser" },
  { icon: HelpCircle, label: "Question Generator", href: "/question-generator" },
]

interface DashboardLayoutProps {
  children: React.ReactNode
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const pathname = usePathname()
  const router = useRouter()

  const handleLogout = () => {
    router.push("/")
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Top Navigation */}
      <nav className="sticky top-0 z-50 bg-background/80 backdrop-blur-md">
        <div className="px-3 sm:px-4 lg:px-6">
          <div className="flex justify-between items-center h-14 sm:h-16">

            <div className="flex items-center space-x-2 sm:space-x-4">
              {/* Mobile menu toggle */}
              <Button
                variant="ghost"
                size="icon"
                className="lg:hidden h-8 w-8 sm:h-10 sm:w-10"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                {sidebarOpen ? <X className="h-4 w-4 sm:h-5 sm:w-5" /> : <Menu className="h-4 w-4 sm:h-5 sm:w-5" />}
              </Button>

              {/* Logo */}
              <Link href="/dashboard" className="flex items-center space-x-2">
                <Image src="/logo.png" alt="Academic Assistant Logo" width={36} height={36} className="rounded-md" />
                <span className="text-lg sm:text-xl font-bold">Academic Assistant</span>
                <span className="text-sm font-bold sm:hidden">Academic Assistant</span>
              </Link>
            </div>

            <div className="flex items-center space-x-2 sm:space-x-4">
              <ThemeToggle />

              {/* User Menu */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-7 w-7 sm:h-8 sm:w-8 rounded-full">
                    <Avatar className="h-7 w-7 sm:h-8 sm:w-8">
                      <AvatarImage src="/profile-icon.jpg" alt="User" />
                      <AvatarFallback className="text-xs sm:text-sm">Name</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-48 sm:w-56" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium leading-none">Name</p>
                      <p className="text-xs leading-none text-muted-foreground">email@example.com</p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <Link href="/profile" className="flex items-center">
                      <User className="mr-2 h-4 w-4" />
                      <span>Profile</span>
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={handleLogout} className="cursor-pointer">
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>Log out</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex">
{/* Sidebar */}
<aside
  className={cn(
    "fixed top-14 sm:top-16 bottom-0 left-0 z-60 w-56 sm:w-64 bg-transparent transform transition-transform duration-200 ease-in-out lg:translate-x-0 lg:static lg:inset-0",
    sidebarOpen ? "translate-x-0" : "-translate-x-full",
  )}
>
  {/* Inner container with full left edge and top-right rounded */}
<div className="flex flex-col h-full bg-background text-card-foreground border-t border-r border-border rounded-tr-2xl mt-4">

    <nav className="flex-1 px-3 sm:px-4 py-4 sm:py-6 space-y-1 sm:space-y-2">
      {sidebarItems.map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            "flex items-center px-2 sm:px-3 py-2 text-sm font-medium rounded-md transition-colors",
            pathname === item.href
              ? "bg-primary text-primary-foreground"
              : "hover:bg-accent hover:text-accent-foreground text-muted-foreground",
          )}
          onClick={() => setSidebarOpen(false)}
        >
          <item.icon className="mr-2 sm:mr-3 h-4 w-4 sm:h-5 sm:w-5 flex-shrink-0" />
          <span className="truncate">{item.label}</span>
        </Link>
      ))}
    </nav>
  </div>
</aside>


        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black bg-opacity-50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main Content */}
        <main className="flex-1 lg:ml-0 min-w-0">
          <div className="p-3 sm:p-4 lg:p-6">{children}</div>
        </main>
      </div>
    </div>
  )
}
