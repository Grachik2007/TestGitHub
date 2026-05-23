export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen bg-slate-900">
      <aside className="w-64 border-r border-slate-800 bg-slate-950 p-6">
        <h2 className="text-xl font-bold mb-8">AI Agents</h2>
        <nav className="space-y-4">
          {[
            { href: "#", label: "Dashboard", icon: "📊" },
            { href: "#", label: "Agents", icon: "🤖" },
            { href: "#", label: "Analytics", icon: "📈" },
            { href: "#", label: "Billing", icon: "💳" },
            { href: "#", label: "Settings", icon: "⚙️" },
          ].map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-slate-800 transition text-slate-400 hover:text-white"
            >
              <span>{item.icon}</span>
              {item.label}
            </a>
          ))}
        </nav>
      </aside>
      <main className="flex-1">{children}</main>
    </div>
  )
}
