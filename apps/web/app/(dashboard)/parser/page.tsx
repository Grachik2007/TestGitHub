"use client"

import { useState } from "react"

const logs = [
  {
    id: 1,
    timestamp: "2024-01-24 12:30:45",
    level: "success",
    message: "✅ Sync completed successfully",
    products: 1247,
    duration: "45.32s",
  },
  {
    id: 2,
    timestamp: "2024-01-23 00:00:15",
    level: "success",
    message: "✅ Daily sync completed",
    products: 1245,
    duration: "42.18s",
  },
  {
    id: 3,
    timestamp: "2024-01-22 00:00:08",
    level: "success",
    message: "✅ Daily sync completed",
    products: 1243,
    duration: "38.95s",
  },
]

export default function ParserPage() {
  const [isSyncing, setIsSyncing] = useState(false)
  const [showConfig, setShowConfig] = useState(false)

  const handleSync = async () => {
    setIsSyncing(true)
    // Simulate sync
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setIsSyncing(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-orange-400 to-red-400 bg-clip-text text-transparent">
            🛒 Wonderfulbed Parser
          </h1>
          <p className="text-slate-400">
            Автоматическая синхронизация товаров с ctradei для wonderfulbed.ru
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Status Cards */}
          <div className="bg-gradient-to-br from-green-500/10 to-green-500/5 border border-green-500/20 rounded-2xl p-6">
            <h3 className="text-sm text-slate-400 mb-2">Статус</h3>
            <p className="text-3xl font-bold text-green-400 mb-2">🟢 Active</p>
            <p className="text-xs text-slate-500">Синхронизация активна</p>
          </div>

          <div className="bg-gradient-to-br from-blue-500/10 to-blue-500/5 border border-blue-500/20 rounded-2xl p-6">
            <h3 className="text-sm text-slate-400 mb-2">Товаров синхронизировано</h3>
            <p className="text-3xl font-bold text-blue-400 mb-2">1,247</p>
            <p className="text-xs text-slate-500">За последнюю синхронизацию</p>
          </div>

          <div className="bg-gradient-to-br from-purple-500/10 to-purple-500/5 border border-purple-500/20 rounded-2xl p-6">
            <h3 className="text-sm text-slate-400 mb-2">Успешность</h3>
            <p className="text-3xl font-bold text-purple-400 mb-2">99.1%</p>
            <p className="text-xs text-slate-500">Успешных синхронизаций</p>
          </div>
        </div>

        {/* Next Sync */}
        <div className="bg-gradient-to-br from-slate-800/50 to-slate-900/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-2xl font-bold mb-2">⏰ Следующая синхронизация</h2>
              <p className="text-slate-400">Автоматическое обновление в 00:00 MSK каждый день</p>
            </div>
            <div className="text-right">
              <p className="text-4xl font-bold text-orange-400">00:00</p>
              <p className="text-sm text-slate-400">2024-01-24</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <button
              onClick={handleSync}
              disabled={isSyncing}
              className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${
                isSyncing
                  ? "bg-slate-600 cursor-not-allowed opacity-50"
                  : "bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700"
              } text-white`}
            >
              {isSyncing ? "⏳ Синхронизация..." : "🚀 Синхронизировать сейчас"}
            </button>
            <button
              onClick={() => setShowConfig(!showConfig)}
              className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded-xl font-semibold transition-all"
            >
              ⚙️ Настройки
            </button>
          </div>
        </div>

        {/* Configuration Panel */}
        {showConfig && (
          <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-8 mb-8">
            <h3 className="text-xl font-bold mb-6">⚙️ Конфигурация парсера</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold mb-2">
                  Email ctradei
                </label>
                <input
                  type="email"
                  defaultValue="bgrachik@yandex.ru"
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-400 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">
                  Пароль ctradei
                </label>
                <input
                  type="password"
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-400 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">
                  insales API URL
                </label>
                <input
                  type="url"
                  defaultValue="https://api.insales.ru/v1"
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-400 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold mb-2">
                  insales API Key
                </label>
                <input
                  type="password"
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 text-white placeholder-slate-400 focus:border-orange-500 focus:outline-none"
                />
              </div>

              <div className="pt-4">
                <button className="w-full bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-700 hover:to-red-700 text-white px-6 py-3 rounded-xl font-semibold transition-all">
                  💾 Сохранить конфигурацию
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Connection Test */}
        <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-6 mb-8">
          <h3 className="text-lg font-bold mb-4">🔗 Проверка соединения</h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-1">ctradei</p>
              <p className="font-semibold text-green-400">✅ Connected</p>
            </div>
            <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
              <p className="text-sm text-slate-400 mb-1">insales API</p>
              <p className="font-semibold text-green-400">✅ Connected</p>
            </div>
          </div>
        </div>

        {/* Logs */}
        <div className="bg-slate-800/50 backdrop-blur-xl border border-slate-700 rounded-2xl p-6">
          <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
            <span>📋</span> История синхронизации
          </h3>

          <div className="space-y-3">
            {logs.map((log) => (
              <div
                key={log.id}
                className="bg-slate-700/30 rounded-lg p-4 border border-slate-600 hover:border-orange-500/50 transition"
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-semibold">{log.message}</p>
                    <p className="text-sm text-slate-400">{log.timestamp}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold">
                      {log.products} товаров
                    </p>
                    <p className="text-xs text-slate-400">{log.duration}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
