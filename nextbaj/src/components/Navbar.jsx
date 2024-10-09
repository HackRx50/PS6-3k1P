"use client"

import Link from "next/link"
import React from "react"
import {
  ClerkProvider,
  SignInButton,
  SignedIn,
  SignedOut,
  UserButton
} from '@clerk/nextjs'
import Username from "./Username"

function Navbar() {
  return (
    <nav className="bg-gradient-to-r from-green-400 to-blue-500 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/admin/" className="text-white text-lg font-semibold hover:text-yellow-300 transition">
          Home
        </Link>
        <div className="flex items-center space-x-6">
          <Link
            href="/admin/videos"
            className="text-white hover:text-yellow-300 transition">
            Videos
          </Link>
          <Link
            href="/admin/upload"
            className="text-white hover:text-yellow-300 transition">
            Generate Video
          </Link>
          <Link
            href="/admin/analytics"
            className="text-white hover:text-yellow-300 transition">
            Admin Analytics
          </Link>
          <SignedIn>
            <div className="flex items-center space-x-4">
              <UserButton />
              <Username className="text-white" />
            </div>
          </SignedIn>
          <SignedOut>
            <SignInButton mode="modal">
              <button className="text-blue-500 bg-white hover:bg-yellow-300 py-2 px-4 rounded transition">
                Sign In
              </button>
            </SignInButton>
          </SignedOut>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
