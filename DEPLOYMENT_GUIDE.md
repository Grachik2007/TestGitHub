# 🚀 Complete Deployment Guide - Wonderfulbed AI SaaS Platform

This guide walks you through the final setup steps to get your automated product feed system live.

## ✅ What's Already Done

- ✅ Parser implementation with ctradei authentication
- ✅ Smart pricing engine (30% margin calculation)
- ✅ Feed generation (YML, CSV, JSON formats)
- ✅ GitHub Actions workflow configured
- ✅ Test data infrastructure in place
- ✅ All core logic tested and verified

## 📋 Setup Checklist

### Step 1: Set Up GitHub Secrets (2 minutes)

Your GitHub Actions workflow needs credentials to access ctradei.

1. Go to: **https://github.com/Grachik2007/TestGitHub/settings/secrets/actions**

2. Click **"New repository secret"** and create these two secrets:

   **Secret #1: CTRADEI_LOGIN**
   - Name: `CTRADEI_LOGIN`
   - Value: `bgrachik@yandex.ru`
   - Click "Add secret"

   **Secret #2: CTRADEI_PASSWORD**
   - Name: `CTRADEI_PASSWORD`
   - Value: `89682753114Grach`
   - Click "Add secret"

3. ✅ Done! GitHub Actions can now authenticate with ctradei

---

### Step 2: Enable GitHub Pages (2 minutes)

Your feeds need to be published to a static URL that insales can access.

1. Go to: **https://github.com/Grachik2007/TestGitHub/settings/pages**

2. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `gh-pages`
   - **Folder**: Select `/ (root)`
   - Click "Save"

3. Wait 1-2 minutes for GitHub to enable Pages

4. ✅ Done! You should see a green message "Your site is live at https://grachik2007.github.io/TestGitHub/"

---

### Step 3: Run First Sync (5 minutes)

Test that everything works by manually triggering the workflow.

1. Go to: **https://github.com/Grachik2007/TestGitHub/actions**

2. Find the workflow: **"🔄 Daily Parser Sync - ctradei to GitHub Pages"**

3. Click **"Run workflow"** dropdown button

4. Click **"Run workflow"** (keep default settings)

5. Watch the workflow run (should take 1-2 minutes)

6. After it completes:
   - All steps should be ✅ green
   - Check the artifacts in the workflow logs

7. ✅ Done! Your feeds have been generated and published

---

### Step 4: Verify Feed Files (2 minutes)

Make sure the feeds are accessible.

Open these URLs in your browser (they should show XML/CSV content):

1. **YML Feed**: https://grachik2007.github.io/TestGitHub/products.yml
   - Should show XML content with your products
   - Content-Type: `text/xml`

2. **CSV Feed**: https://grachik2007.github.io/TestGitHub/products.csv
   - Should show CSV content
   - Content-Type: `text/csv`

3. **Summary**: https://grachik2007.github.io/TestGitHub/summary.json
   - Should show JSON with statistics

---

### Step 5: Connect to insales (3 minutes)

Now insales can automatically pull your products.

1. Log in to **insales admin panel**

2. Navigate to: **Товары → Импорт**

3. Create import:
   - **URL**: https://grachik2007.github.io/TestGitHub/products.yml
   - **Периодичность**: каждый час
   - Click **"Сохранить"**

4. ✅ Done! insales will now sync products every hour

---

## 📊 How It Works

Every day at **00:30 MSK**:
1. GitHub Actions downloads latest products from ctradei
2. Merges CSV (prices) + YML (descriptions)
3. Calculates smart prices (30% margin)
4. Publishes to GitHub Pages
5. insales automatically pulls the new data

---

## 🔗 Important Links

- **GitHub Secrets**: https://github.com/Grachik2007/TestGitHub/settings/secrets/actions
- **GitHub Pages**: https://github.com/Grachik2007/TestGitHub/settings/pages
- **Workflow Status**: https://github.com/Grachik2007/TestGitHub/actions
- **Live YML Feed**: https://grachik2007.github.io/TestGitHub/products.yml

---

**🎉 Your automated product sync system is ready!**

Total setup time: **~15 minutes**
Monthly cost: **$0** (completely free)
Maintenance: **0 hours** (fully automatic)
