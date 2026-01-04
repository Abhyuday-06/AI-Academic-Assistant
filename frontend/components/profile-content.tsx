"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { User, Mail, School, Calendar, Edit, Save, X, ArrowLeft } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { api } from "@/lib/api"


export function ProfileContent() {
  const [isEditing, setIsEditing] = useState(false)
  const [profile, setProfile] = useState<any>(null)
  const [editedProfile, setEditedProfile] = useState<any>(null)
  const { toast } = useToast()

  // Fetch profile data
  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await api.getProfile()
        setProfile(data)
        setEditedProfile(data)
      } catch {
        // fallback to guest
        const guestProfile = {
          name: "Guest User",
          email: "guest@example.com",
          institution: "N/A",
          studyLevel: "N/A",
          major: "N/A",
          joinDate: "—",
        }
        setProfile(guestProfile)
        setEditedProfile(guestProfile)
      }
    }
    fetchProfile()
  }, [])

  const handleEdit = () => {
    setIsEditing(true)
    setEditedProfile(profile)
  }

  const handleSave = async () => {
    try {
      const updated = await api.updateProfile(editedProfile)
      setProfile(updated)
      toast({
        title: "Profile Updated",
        description: "Your profile information has been saved successfully.",
      })
    } catch {
      toast({
        title: "Error",
        description: "Could not save profile data.",
        variant: "destructive",
      })
    } finally {
      setIsEditing(false)
    }
  }

  const handleCancel = () => {
    setEditedProfile(profile)
    setIsEditing(false)
  }

  const handleInputChange = (field: string, value: string) => {
    setEditedProfile((prev: any) => ({ ...prev, [field]: value }))
  }

  if (!profile) {
    return <p className="text-center mt-10">Loading profile...</p>
  }

  return (
    <div className="container max-w-4xl mx-auto py-8 space-y-6">
      {/* Top Nav Back Button */}
      <div className="flex items-center mb-6">
        <Link href="/dashboard">
          <Button variant="ghost" className="flex items-center space-x-2">
            <ArrowLeft className="h-4 w-4" />
            <span>Back to Dashboard</span>
          </Button>
        </Link>
      </div>

      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Profile</h1>
        <p className="text-gray-600 dark:text-gray-300 mt-2">
          Manage your personal information.
        </p>
      </div>

      {/* Profile Header */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center space-x-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src="/placeholder.svg?height=96&width=96" alt="Profile" />
              <AvatarFallback className="text-2xl">
                {profile.name
                  .split(" ")
                  .map((n: string) => n[0])
                  .join("")}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{profile.name}</h2>
              <p className="text-gray-600 dark:text-gray-300">{profile.email}</p>
              <div className="flex items-center space-x-2 mt-2">
                <Badge variant="secondary">{profile.studyLevel}</Badge>
                <Badge variant="outline">{profile.major}</Badge>
              </div>
            </div>
            {profile.name !== "Guest User" && (
              <>
                <Button onClick={isEditing ? handleSave : handleEdit} className="flex items-center space-x-2">
                  {isEditing ? (
                    <>
                      <Save className="h-4 w-4" />
                      <span>Save</span>
                    </>
                  ) : (
                    <>
                      <Edit className="h-4 w-4" />
                      <span>Edit Profile</span>
                    </>
                  )}
                </Button>
                {isEditing && (
                  <Button variant="outline" onClick={handleCancel}>
                    <X className="h-4 w-4" />
                  </Button>
                )}
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Profile Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <User className="h-5 w-5" />
            <span>Personal Information</span>
          </CardTitle>
          <CardDescription>Your basic profile information</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[
              { id: "name", label: "Full Name", icon: User, value: profile.name },
              { id: "email", label: "Email Address", icon: Mail, value: profile.email },
              { id: "institution", label: "Institution", icon: School, value: profile.institution },
              { id: "studyLevel", label: "Study Level", icon: Calendar, value: profile.studyLevel },
              { id: "major", label: "Major/Field of Study", icon: School, value: profile.major },
            ].map((field) => (
              <div key={field.id} className="space-y-2">
                <Label htmlFor={field.id}>{field.label}</Label>
                {isEditing && profile.name !== "Guest User" ? (
                  <Input
                    id={field.id}
                    value={editedProfile[field.id]}
                    onChange={(e) => handleInputChange(field.id, e.target.value)}
                  />
                ) : (
                  <div className="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-800 rounded">
                    <field.icon className="h-4 w-4 text-gray-500" />
                    <span>{field.value}</span>
                  </div>
                )}
              </div>
            ))}

            {/* Join Date (read-only) */}
            <div className="space-y-2">
              <Label>Member Since</Label>
              <div className="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-800 rounded">
                <Calendar className="h-4 w-4 text-gray-500" />
                <span>{profile.joinDate}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
