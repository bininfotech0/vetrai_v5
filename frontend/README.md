# VetrAI Frontend Applications

This directory contains the frontend applications for the VetrAI platform.

## Applications

### Studio Frontend (`/studio`)
- **Port**: 3000
- **Purpose**: Main AI workflow builder interface
- **Technology**: Next.js 14 with TypeScript
- **Features**:
  - LangGraph workflow visual editor (ReactFlow)
  - Real-time job execution monitoring
  - Multi-tenant organization switching
  - File upload/management integration
  - Responsive design with Tailwind CSS

### Admin Dashboard (`/admin`)
- **Port**: 3001  
- **Purpose**: Administrative management interface
- **Technology**: Next.js 14 with TypeScript
- **Features**:
  - User and organization management
  - Billing and subscription administration
  - Support ticket management
  - System monitoring and analytics
  - Theme and branding configuration

### Shared Components (`/shared`)
- Common types, utilities, and constants
- Reusable across both applications
- API client configurations
- Shared styling and components

## Architecture

```
frontend/
├── studio/           # Main workflow interface (Port 3000)
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Next.js pages
│   │   ├── lib/          # Utilities and API clients
│   │   ├── types/        # TypeScript type definitions
│   │   ├── hooks/        # Custom React hooks
│   │   ├── store/        # Redux store and slices
│   │   ├── contexts/     # React contexts
│   │   └── styles/       # Global styles
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── admin/            # Admin dashboard (Port 3001)
│   ├── src/
│   │   ├── components/   # Admin-specific components
│   │   ├── pages/        # Admin pages
│   │   └── ...           # Similar structure to studio
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
└── shared/           # Shared utilities and types
    ├── types/            # Common TypeScript types
    ├── lib/              # Shared utility functions
    ├── constants/        # Shared constants
    └── components/       # Shared React components
```

## Development Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Install Studio dependencies:**
   ```bash
   cd frontend/studio
   npm install
   ```

2. **Install Admin dependencies:**
   ```bash
   cd frontend/admin
   npm install
   ```

### Running in Development

1. **Start Studio (Port 3000):**
   ```bash
   cd frontend/studio
   npm run dev
   ```

2. **Start Admin Dashboard (Port 3001):**
   ```bash
   cd frontend/admin
   npm run dev
   ```

### Building for Production

```bash
# Studio
cd frontend/studio
npm run build

# Admin
cd frontend/admin
npm run build
```

## Docker Development

Both applications are configured for Docker deployment:

```bash
# Build and run all services including frontend
docker-compose up --build

# Access applications
# Studio: http://localhost:3000
# Admin: http://localhost:3001
```

## Environment Variables

Create `.env.local` files in each application directory:

### Studio (`.env.local`)
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000
```

### Admin (`.env.local`)
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## API Integration

Both applications integrate with the VetrAI backend services:
- **Auth Service** (8001): Authentication and authorization
- **Tenancy Service** (8002): Organization management  
- **Keys Service** (8003): API key management
- **Billing Service** (8004): Payment and subscriptions
- **Support Service** (8005): Ticket management
- **Themes Service** (8006): Branding and theming
- **Notifications Service** (8007): Messaging
- **Workers Service** (8008): Workflow execution

## Key Features

### Studio Frontend
- **Workflow Builder**: Visual drag-and-drop interface using ReactFlow
- **Real-time Updates**: WebSocket integration for live execution monitoring
- **Multi-tenant**: Organization context switching
- **Authentication**: JWT-based auth with automatic token refresh
- **Responsive Design**: Mobile-friendly interface

### Admin Dashboard
- **User Management**: CRUD operations for users and organizations
- **Analytics**: System health monitoring and usage statistics
- **Billing Management**: Stripe integration for subscription management
- **Support Tools**: Ticket management and customer support
- **System Configuration**: Theme management and system settings

## Technology Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom design system
- **State Management**: Redux Toolkit + React Context
- **API Client**: Axios with interceptors
- **UI Components**: Custom components with Headless UI
- **Icons**: Heroicons
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast
- **Charts**: Recharts (Admin)
- **Workflow Editor**: ReactFlow (Studio)

## Contributing

1. Follow the existing code structure and conventions
2. Use TypeScript for all new code
3. Ensure responsive design compliance
4. Test API integrations thoroughly
5. Update documentation for new features