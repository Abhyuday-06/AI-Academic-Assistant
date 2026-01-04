"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { HelpCircle, FileText, CheckCircle, Clock, AlertCircle } from "lucide-react"
import Link from "next/link"
import { DashboardLayout } from "@/components/dashboard-layout"
import { useEffect, useState } from "react"
import { api } from "@/lib/api"

const quickActions = [
  {
    icon: FileText,
    title: "Summarise Document",
    description: "Upload and get summary of your materials",
    href: "/summariser",
    color: "bg-primary",
  },
  {
    icon: HelpCircle,
    title: "Generate Questions",
    description: "Practice syllabus-specific questions",
    href: "/question-generator",
    color: "bg-accent",
  },
]

export function DashboardContent() {
  const [recentActivity, setRecentActivity] = useState<any[]>([])

  useEffect(() => {
    const fetchActivity = async () => {
      try {
        const data = await api.getRecentActivity()
        setRecentActivity(data)
      } catch (err) {
        console.error("Error fetching activity:", err)
      }
    }

    fetchActivity()
  }, [])

  return (
    <DashboardLayout>
      <div className="flex flex-col items-center space-y-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted-foreground mt-1 sm:mt-2 text-sm sm:text-base">
            Explore the features below and improve your prep journey!
          </p>
        </div>

        {/* Quick Actions */}
        <div className="w-full">
          <h2 className="text-lg sm:text-xl font-semibold mb-6 text-center text-foreground">Quick Actions</h2>
         <div className="flex flex-wrap justify-center gap-6">
  {quickActions.map((action, index) => (
    <Link key={index} href={action.href}>
      <Card className="hover:shadow-lg transition-shadow cursor-pointer w-96">
        <CardContent className="p-4 sm:p-6 flex flex-col items-center text-center">
          <div className={`p-3 rounded-lg ${action.color} flex items-center justify-center mb-3`}>
            <action.icon className="h-6 w-6 text-primary-foreground" />
          </div>
          <h3 className="font-semibold text-base mb-1 text-foreground">{action.title}</h3>
          <p className="text-sm text-muted-foreground">{action.description}</p>
        </CardContent>
      </Card>
    </Link>
  ))}
</div>



        </div>

        {/* Recent Activity */}
        <div className="w-full">
          <h2 className="text-lg sm:text-xl font-semibold mb-4 text-center text-foreground">Recent Activity</h2>
          <Card>
            <CardHeader className="pb-3 sm:pb-4">
              <CardTitle className="flex items-center justify-center space-x-2 text-base sm:text-lg text-foreground">
              </CardTitle>
              <CardDescription className="text-xs sm:text-sm text-muted-foreground text-center">
              </CardDescription>
            </CardHeader>
            <CardContent>
              {recentActivity.length > 0 ? (
                <div className="flex flex-col space-y-3 sm:space-y-4">
                  {recentActivity.map((activity, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        {activity.status === "completed" ? (
                          <CheckCircle className="h-5 w-5 text-primary" />
                        ) : (
                          <AlertCircle className="h-5 w-5 text-accent" />
                        )}
                        <div className="flex flex-col min-w-0">
                          <p className="text-sm font-medium text-foreground truncate">{activity.action}</p>
                          <p className="text-xs text-muted-foreground">{activity.time}</p>
                        </div>
                      </div>
                      <Badge
                        className={`text-xs ${
                          activity.status === "completed"
                            ? "bg-primary text-primary-foreground"
                            : "bg-accent text-accent-foreground"
                        }`}
                      >
                        {activity.status}
                      </Badge>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-32 text-muted-foreground">
                  <Clock className="h-8 w-8 mb-2 opacity-50" />
                  <p className="text-sm">No recent activity</p>
                  <p className="text-xs opacity-75 text-center">
                    Upload documents or syllabus to see activity here
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
