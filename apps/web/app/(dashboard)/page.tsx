"use client"

export default function DashboardPage() {
  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-slate-400">Welcome back to your AI Agents Platform</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {[
          { label: "Total Tasks", value: "1,234", change: "+12%" },
          { label: "Success Rate", value: "98.5%", change: "+2.3%" },
          { label: "Tokens Used", value: "45,678", change: "-5%" },
          { label: "Cost This Month", value: "$127.50", change: "+$25" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="card"
          >
            <p className="text-slate-400 text-sm mb-2">{stat.label}</p>
            <p className="text-3xl font-bold mb-2">{stat.value}</p>
            <p className="text-xs text-green-400">{stat.change}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Recent Tasks</h3>
          <div className="space-y-3">
            {[1, 2, 3].map((item) => (
              <div key={item} className="flex items-center gap-4 p-3 bg-slate-700/50 rounded">
                <div className="w-2 h-2 rounded-full bg-green-400"></div>
                <div className="flex-1">
                  <p className="font-medium">Task #{item}</p>
                  <p className="text-xs text-slate-400">SEO Agent - 2 minutes ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Agents Status</h3>
          <div className="space-y-3">
            {[
              { name: "SEO Agent", status: "active" },
              { name: "Supplier Agent", status: "active" },
              { name: "Product Agent", status: "idle" },
              { name: "Pricing Agent", status: "active" },
            ].map((agent) => (
              <div key={agent.name} className="flex items-center justify-between">
                <span>{agent.name}</span>
                <span className={`text-xs px-2 py-1 rounded ${
                  agent.status === "active"
                    ? "bg-green-500/20 text-green-400"
                    : "bg-slate-600/20 text-slate-400"
                }`}>
                  {agent.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
