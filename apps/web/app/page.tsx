"use client"

import Link from "next/link"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 p-24 bg-gradient-to-b from-slate-900 to-slate-800">
      <div className="text-center space-y-6">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          AI Agents Platform
        </h1>
        <p className="text-xl text-slate-400 max-w-2xl">
          Production-ready SaaS platform with multi-agent orchestration, Telegram assistant, and analytics dashboard
        </p>
      </div>

      <div className="flex gap-4">
        <Link
          href="/login"
          className="px-8 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 font-semibold transition"
        >
          Sign In
        </Link>
        <Link
          href="/register"
          className="px-8 py-3 rounded-lg border border-blue-600 hover:bg-blue-600/10 font-semibold transition"
        >
          Sign Up
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-16">
        {[
          { title: "🤖 AI Agents", desc: "Multi-agent orchestration system" },
          { title: "💬 Telegram Bot", desc: "Full-featured Telegram integration" },
          { title: "📊 Analytics", desc: "Real-time analytics dashboard" },
          { title: "💳 Billing", desc: "Stripe subscription management" },
        ].map((item) => (
          <div
            key={item.title}
            className="p-6 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-blue-500/50 transition"
          >
            <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
            <p className="text-sm text-slate-400">{item.desc}</p>
          </div>
        ))}
      </div>
    </main>
  )
}
