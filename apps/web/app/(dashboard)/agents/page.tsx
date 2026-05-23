"use client"

import { useState } from "react"

const agents = [
  {
    id: "seo",
    name: "🔍 SEO Agent",
    description: "Анализ ключевых слов и оптимизация контента",
    status: "active",
    tasks: 1234,
    successRate: 98.5,
    color: "from-blue-500 to-cyan-500",
    icon: "🔍",
  },
  {
    id: "supplier",
    name: "🏭 Supplier Agent",
    description: "Поиск и анализ поставщиков",
    status: "active",
    tasks: 567,
    successRate: 95.2,
    color: "from-green-500 to-emerald-500",
    icon: "🏭",
  },
  {
    id: "product",
    name: "📦 Product Agent",
    description: "Исследование трендов и товаров",
    status: "active",
    tasks: 892,
    successRate: 96.8,
    color: "from-purple-500 to-pink-500",
    icon: "📦",
  },
  {
    id: "parser",
    name: "🛒 Wonderfulbed Parser",
    description: "Парсинг товаров с ctradei для wonderfulbed.ru",
    status: "active",
    tasks: 45,
    successRate: 99.1,
    color: "from-orange-500 to-red-500",
    icon: "🛒",
    nextRun: "2024-01-24 00:00 MSK",
  },
  {
    id: "pricing",
    name: "💰 Pricing Agent",
    description: "Оптимизация цен и анализ конкурентов",
    status: "idle",
    tasks: 234,
    successRate: 94.7,
    color: "from-yellow-500 to-orange-500",
    icon: "💰",
  },
]

export default function AgentsPage() {
  const [selectedAgent, setSelectedAgent] = useState(agents[3])
  const [showChat, setShowChat] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            🤖 AI Agents Management
          </h1>
          <p className="text-slate-400 text-lg">
            Управление мультиагентной системой для автоматизации задач
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Agents List */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-6">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <span>📋</span> Доступные Агенты
              </h2>

              <div className="space-y-3">
                {agents.map((agent) => (
                  <button
                    key={agent.id}
                    onClick={() => setSelectedAgent(agent)}
                    className={`w-full text-left p-4 rounded-xl transition-all duration-300 ${
                      selectedAgent.id === agent.id
                        ? "bg-gradient-to-r " + agent.color + " shadow-lg"
                        : "bg-slate-700/50 hover:bg-slate-700 border border-slate-600"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xl">{agent.icon}</span>
                      <span
                        className={`text-xs px-2 py-1 rounded-full ${
                          agent.status === "active"
                            ? "bg-green-500/20 text-green-400"
                            : "bg-slate-600/20 text-slate-400"
                        }`}
                      >
                        {agent.status === "active" ? "🟢" : "⚫"} {agent.status}
                      </span>
                    </div>
                    <p className="font-semibold text-sm">{agent.name}</p>
                    <p className="text-xs text-slate-400 mt-1">
                      {agent.description}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Agent Details */}
          <div className="lg:col-span-2 space-y-6">
            {/* Main Card */}
            <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-8 overflow-hidden relative">
              {/* Background gradient */}
              <div
                className={`absolute inset-0 opacity-10 bg-gradient-to-br ${selectedAgent.color}`}
              ></div>

              <div className="relative z-10">
                <div className="flex items-start justify-between mb-8">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-5xl">{selectedAgent.icon}</span>
                      <div>
                        <h3 className="text-3xl font-bold">
                          {selectedAgent.name}
                        </h3>
                        <p className="text-slate-400">
                          {selectedAgent.description}
                        </p>
                      </div>
                    </div>
                  </div>
                  <span
                    className={`px-4 py-2 rounded-full text-sm font-semibold ${
                      selectedAgent.status === "active"
                        ? "bg-green-500/20 text-green-400"
                        : "bg-slate-600/20 text-slate-400"
                    }`}
                  >
                    {selectedAgent.status === "active" ? "🟢 Active" : "⚫ Idle"}
                  </span>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-4 mb-8">
                  <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                    <p className="text-slate-400 text-sm mb-1">Всего задач</p>
                    <p className="text-2xl font-bold text-blue-400">
                      {selectedAgent.tasks}
                    </p>
                  </div>
                  <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                    <p className="text-slate-400 text-sm mb-1">Успешность</p>
                    <p className="text-2xl font-bold text-green-400">
                      {selectedAgent.successRate}%
                    </p>
                  </div>
                  <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
                    <p className="text-slate-400 text-sm mb-1">Статус</p>
                    <p className="text-2xl font-bold text-purple-400">
                      {selectedAgent.status === "active" ? "✨ Active" : "💤 Idle"}
                    </p>
                  </div>
                </div>

                {/* Next Run for Parser */}
                {selectedAgent.id === "parser" && (
                  <div className="bg-orange-500/10 border border-orange-500/20 rounded-xl p-4 mb-6">
                    <p className="text-sm text-slate-400 mb-1">
                      ⏰ Следующее обновление
                    </p>
                    <p className="text-lg font-bold text-orange-400">
                      {selectedAgent.nextRun}
                    </p>
                    <p className="text-xs text-slate-500 mt-2">
                      Автоматическое обновление товаров каждый день в 00:00 MSK
                    </p>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => setShowChat(!showChat)}
                    className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold py-3 rounded-xl transition-all duration-300 flex items-center justify-center gap-2"
                  >
                    💬 Chat с агентом
                  </button>
                  <button className="bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-xl transition-all duration-300 flex items-center justify-center gap-2">
                    ⚙️ Настройки
                  </button>
                </div>
              </div>
            </div>

            {/* Recent Tasks */}
            <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-6">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <span>📊</span> Последние задачи
              </h3>
              <div className="space-y-3">
                {[1, 2, 3].map((item) => (
                  <div
                    key={item}
                    className="bg-slate-700/30 rounded-lg p-4 flex items-center justify-between border border-slate-600"
                  >
                    <div>
                      <p className="font-semibold">Task #{item + 1000}</p>
                      <p className="text-sm text-slate-400">
                        Выполнено {Math.random() * 30 + 10 | 0} минут назад
                      </p>
                    </div>
                    <span className="text-green-400 text-lg">✅</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Chat Modal */}
        {showChat && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-slate-800 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[80vh] flex flex-col">
              <div className="flex items-center justify-between p-6 border-b border-slate-700">
                <div>
                  <h3 className="text-xl font-bold">
                    {selectedAgent.icon} Chat с {selectedAgent.name}
                  </h3>
                </div>
                <button
                  onClick={() => setShowChat(false)}
                  className="text-slate-400 hover:text-white text-2xl"
                >
                  ✕
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0 text-white text-xs">
                    🤖
                  </div>
                  <div className="bg-slate-700 rounded-lg p-4 max-w-xs">
                    <p className="text-sm">
                      Привет! Я {selectedAgent.name.split(" ")[2] || "агент"}. Чем я могу тебе помочь?
                    </p>
                  </div>
                </div>
              </div>

              <div className="p-6 border-t border-slate-700">
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Напиши свой вопрос..."
                    className="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-3 text-white placeholder-slate-400 focus:border-blue-500 focus:outline-none"
                  />
                  <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition">
                    Отправить
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
