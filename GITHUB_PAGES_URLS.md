# 🌐 GitHub Pages - Where to Find Your Feeds & Dashboard

## 📍 Base URLs

Your AI agents platform and product feeds are automatically deployed to GitHub Pages and accessible at:

**Base URL:** `https://grachik2007.github.io/TestGitHub/`

## 🎯 Agent Management Dashboard

**Access the beautiful agent management interface here:**

```
https://grachik2007.github.io/TestGitHub/agents.html
```

### Features:
- 🤖 5 AI agents with live status
- 📊 Task statistics and success rates
- 🛒 Wonderfulbed parser with sync controls
- 📋 Product feed links
- ⏰ Next sync time (00:30 MSK)
- 🎨 Beautiful purple gradient UI with animations

## 📋 Product Feeds

### Yandex Market Feed (Russian E-commerce)
```
https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml
```
- Format: XML
- Use for: Яндекс.Маркета, Яндекс.Каталог
- Auto-updates: Daily at 00:30 MSK
- Fields: Shop info, categories, offers with prices and images

### Google Merchant Center Feed
```
https://grachik2007.github.io/TestGitHub/feeds/google-merchant.xml
```
- Format: XML (RSS with Google namespaces)
- Use for: Google Shopping, Google Ads
- Auto-updates: Daily at 00:30 MSK
- Fields: Product ID, title, description, price, availability, image

### JSON Product Feed (API)
```
https://grachik2007.github.io/TestGitHub/feeds/products.json
```
- Format: JSON
- Use for: Custom integrations, mobile apps, API clients
- Auto-updates: Daily at 00:30 MSK
- Contains: Full product data with features and target audience

## 🔗 Landing Page

```
https://grachik2007.github.io/TestGitHub/
```

This page shows:
- Links to all three product feeds
- Access to agent management dashboard
- Last sync timestamp
- Feed update schedule (daily 00:30 MSK)

## ⚙️ How it Works

### Daily Update Process
1. **Trigger**: GitHub Actions runs every day at 00:30 MSK (21:30 UTC)
2. **Generate**: Python scripts create all feed formats
3. **Deploy**: Files automatically pushed to gh-pages branch
4. **Publish**: GitHub Pages serves the updated files
5. **Available**: Feeds and dashboard instantly available at above URLs

### Manual Update
You can manually trigger feed generation:
```bash
# Go to: https://github.com/Grachik2007/TestGitHub/actions
# Select: "Generate Product Feed" workflow
# Click: "Run workflow"
```

## 📊 Current Status

- ✅ Workflows configured
- ✅ Dashboard generated
- ✅ Feed generators ready
- ⏳ **Awaiting PR merge** to activate automation
- ⏳ GitHub Pages will auto-deploy on first workflow run

## 🚀 Next Steps

1. **Merge PR #1** to main branch
2. **First workflow run** will generate feeds
3. **Visit URLs above** to see live dashboard and feeds
4. **Feeds auto-update** daily at 00:30 MSK

## 🔑 Integration

### For ctradei (Product Source)
- Products will be fetched from ctradei API
- Enriched with GigaChat (Russian LLM)
- Synced to wonderfulbed.ru via insales API
- Feed URLs become your product distribution channels

### For wonderfulbed.ru
- XML feeds can be imported directly
- Products stay synchronized
- Stock levels auto-update
- Pricing syncs daily

## 📱 Mobile Access

All URLs work on mobile devices:
- Dashboard responsive design
- Feed URLs accessible from any HTTP client
- Perfect for monitoring on phone

## 🔒 Security Notes

- Feeds are public (anyone can access URLs)
- No authentication required for feed access
- API credentials stored in GitHub Secrets
- Sensitive data never exposed in feeds

## 📞 Troubleshooting

**Feeds not showing?**
- Workflows require PR to be merged to main
- Check Actions tab for workflow status
- GitHub Pages may need 1-2 minutes to deploy

**Dashboard looks empty?**
- Sample products load immediately
- Real ctradei products appear after first sync
- Check parser status in dashboard

**Wrong timestamp?**
- Server time: UTC
- Sync scheduled: 00:30 MSK (21:30 UTC previous day)
- Times shown in feeds are generated time

---

**Last Updated:** 2024-01-24
**Dashboard URL:** https://grachik2007.github.io/TestGitHub/agents.html
**Primary Feed:** https://grachik2007.github.io/TestGitHub/feeds/yandex-market.xml
