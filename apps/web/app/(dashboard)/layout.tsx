export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen bg-slate-900">
      <aside className="w-64 border-r border-slate-800 bg-slate-950 p-6 overflow-y-auto">
        <h2 className="text-xl font-bold mb-8">AI Agents Platform</h2>
        <nav className="space-y-2">
          {[
            { href: "/dashboard", label: "Dashboard", icon: "📊" },
            { href: "/dashboard/agents", label: "AI Agents", icon: "🤖" },
            { href: "/dashboard/parser", label: "Wonderfulbed Parser", icon: "🛒" },
            { href: "/dashboard/pricing", label: "Smart Pricing", icon: "💰" },
            { href: "/dashboard/analytics", label: "Analytics", icon: "📈" },
            { href: "/dashboard/billing", label: "Billing", icon: "💳" },
            { href: "/dashboard/settings", label: "Settings", icon: "⚙️" },
          ].map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-slate-800 transition text-slate-400 hover:text-white"
            >
              <span>{item.icon}</span>
              <span className="text-sm">{item.label}</span>
            </a>
          ))}
        </nav>

        <div className="mt-8 pt-8 border-t border-slate-800">
          <h3 className="text-xs font-semibold text-slate-500 mb-4 px-4">AGENTS</h3>
          <div className="space-y-2">
            {[
              { id: "seo", name: "SEO Agent", icon: "🔍" },
              { id: "supplier", name: "Supplier", icon: "🏭" },
              { id: "product", name: "Product", icon: "📦" },
              { id: "pricing", name: "Pricing", icon: "💰" },
            ].map((agent) => (
              <div
                key={agent.id}
                className="flex items-center gap-2 px-4 py-2 rounded text-xs text-slate-400 hover:text-white hover:bg-slate-800/50 transition cursor-pointer"
              >
                <span>{agent.icon}</span>
                {agent.name}
              </div>
            ))}
          </div>
        </div>
      </aside>
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  )
}
