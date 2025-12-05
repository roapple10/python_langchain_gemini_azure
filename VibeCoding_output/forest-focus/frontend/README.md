# Forest Focus - Pomodoro Timer

A Forest-style Pomodoro timer web application built with React, TypeScript, and Vite.

## Features

- 25-minute focus sessions with visual tree growth
- Pause, resume, and cancel functionality
- Personal forest visualization
- Statistics tracking (total trees, focus time, daily streak)
- Browser notifications
- Offline-first (localStorage persistence)
- Responsive design (mobile, tablet, desktop)
- Accessibility support (WCAG 2.1 AA)

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── hooks/         # Custom React hooks
│   ├── services/      # Business logic
│   ├── types/         # TypeScript types
│   ├── styles/        # CSS files
│   └── utils/         # Utility functions
└── tests/             # Test files
```

## Development

This project follows Test-Driven Development (TDD):
1. Write tests first
2. Ensure tests fail
3. Implement functionality
4. Refactor while keeping tests green

## Performance Targets

- Page load: <2 seconds on 3G
- Animations: 60fps
- Bundle size: <200KB gzipped

## License

MIT

