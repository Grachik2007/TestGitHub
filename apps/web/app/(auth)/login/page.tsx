"use client"

import Link from "next/link"

export default function LoginPage() {
  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Sign In</h1>
        <p className="text-slate-400">Welcome back to AI Agents Platform</p>
      </div>

      <form className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Email</label>
          <input
            type="email"
            className="input"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Password</label>
          <input
            type="password"
            className="input"
            placeholder="••••••••"
          />
        </div>

        <button type="submit" className="btn-primary w-full">
          Sign In
        </button>
      </form>

      <p className="text-center text-slate-400">
        Don&apos;t have an account?{" "}
        <Link href="/register" className="text-blue-400 hover:text-blue-300">
          Sign up
        </Link>
      </p>
    </div>
  )
}
