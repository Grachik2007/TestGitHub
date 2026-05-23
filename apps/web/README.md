# Next.js Frontend

Modern Next.js 15 dashboard for AI Agents Platform.

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- npm or yarn

### Setup

1. **Install dependencies**
```bash
npm install
```

2. **Setup environment**
```bash
cp .env.example .env.local
```

3. **Run development server**
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
app/              - Next.js app directory
├── (auth)/       - Authentication pages
├── (dashboard)/  - Dashboard pages
└── api/          - API routes

components/       - React components
├── layout/       - Layout components
├── agents/       - Agent-related components
├── analytics/    - Analytics components
└── ui/           - Reusable UI components

lib/              - Utility functions
store/            - Zustand state management
services/         - API service layer
hooks/            - Custom React hooks
types/            - TypeScript types
public/           - Static files
styles/           - Global styles
```

## 🎨 Features

- Dark/Light theme toggle
- Responsive mobile UI
- Real-time analytics
- Agent chat interface
- Billing management
- User authentication
- Modern animations with Framer Motion
- TypeScript support

## 📦 Technologies

- **Framework**: Next.js 15
- **Styling**: Tailwind CSS
- **State**: Zustand
- **Data Fetching**: React Query
- **UI Components**: Lucide React
- **Animations**: Framer Motion
- **Forms**: React Hook Form
- **Validation**: Zod

## 🔧 Development

### Code Quality

```bash
npm run lint      # Run ESLint
npm run format    # Format with Prettier
npm run type-check # Type checking
```

### Build

```bash
npm run build
npm start        # Run production build
```

## 📚 Documentation

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [React Query](https://tanstack.com/query/latest)

## 📝 License

MIT
