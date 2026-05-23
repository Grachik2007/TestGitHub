import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "AI Agents Platform",
  description: "Modern AI SaaS platform with multi-agent orchestration",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-slate-900 text-slate-100">
        {children}
      </body>
    </html>
  )
}
