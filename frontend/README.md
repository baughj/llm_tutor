# CodeMentor Frontend

React + TypeScript frontend for the LLM Coding Tutor Platform.

## Technology Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Material-UI (MUI)** - Component library
- **Redux Toolkit** - State management
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Emotion** - CSS-in-JS styling

## Project Structure

```
src/
├── components/      # Reusable UI components
│   └── Layout/      # Layout components
├── hooks/           # Custom React hooks
│   ├── useRedux.ts  # Typed Redux hooks
│   └── useResponsive.ts  # Responsive breakpoint hooks
├── pages/           # Page components (routes)
├── routes/          # Route configuration
├── services/        # API services
│   ├── api.ts       # Axios client with interceptors
│   └── authService.ts  # Authentication API calls
├── store/           # Redux store
│   ├── index.ts     # Store configuration
│   └── slices/      # Redux slices
├── theme/           # MUI theme configuration
├── types/           # TypeScript type definitions
└── utils/           # Utility functions
```

## Getting Started

### Prerequisites

- Node.js 22+
- npm 11+

### Installation

```bash
npm install
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Configure:
- `VITE_API_BASE_URL` - Backend API URL (default: http://localhost:5000/api)

### Development

Start the development server:

```bash
npm run dev
```

The app will open at http://localhost:3000

### Build

Build for production:

```bash
npm run build
```

Output will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Path Aliases

The project uses path aliases for cleaner imports:

```typescript
import { Button } from '@components/Button';
import { useAuth } from '@hooks/useAuth';
import { authService } from '@services/authService';
```

Available aliases:
- `@/` → `src/`
- `@components/` → `src/components/`
- `@pages/` → `src/pages/`
- `@services/` → `src/services/`
- `@store/` → `src/store/`
- `@hooks/` → `src/hooks/`
- `@utils/` → `src/utils/`
- `@types/` → `src/types/`
- `@theme/` → `src/theme/`

## Code Style

- Use functional components with hooks
- Prefer TypeScript interfaces over types for object shapes
- Use `type` keyword for type-only imports (due to verbatimModuleSyntax)
- Follow Material-UI design patterns
- Use responsive design with MUI breakpoints

## State Management

Redux Toolkit is configured for global state. Example usage:

```typescript
import { useAppDispatch, useAppSelector } from '@hooks/useRedux';
import { setCredentials } from '@store/slices/authSlice';

function MyComponent() {
  const dispatch = useAppDispatch();
  const user = useAppSelector((state) => state.auth.user);

  const handleLogin = () => {
    dispatch(setCredentials({ user, token }));
  };
}
```

## API Client

Axios is configured with interceptors for authentication:

```typescript
import { authService } from '@services/authService';

const user = await authService.login({ email, password });
```

The API client automatically:
- Adds Bearer token from localStorage
- Redirects to login on 401 responses
- Proxies `/api` requests to backend during development

## Responsive Design

See [RESPONSIVE_DESIGN.md](./RESPONSIVE_DESIGN.md) for detailed guidelines.

Quick example:

```typescript
import { useResponsive } from '@hooks/useResponsive';

function MyComponent() {
  const { isMobile, isDesktop } = useResponsive();

  return (
    <Box sx={{ padding: { xs: 2, md: 4 } }}>
      {isMobile ? <MobileView /> : <DesktopView />}
    </Box>
  );
}
```

## Build Optimization

The Vite build is configured with:
- Code splitting for vendor, MUI, and Redux bundles
- Tree shaking for smaller bundle sizes
- Minification with esbuild
- Source maps for debugging
- 1MB chunk size warning limit

## Next Steps (Work Stream B4)

This frontend framework is ready for implementing:
- Authentication UI (login, register forms)
- Protected routes
- User profile pages
- Dashboard components

## License

Proprietary - CodeMentor Platform
