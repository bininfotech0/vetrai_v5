// Shared constants
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    LOGOUT: '/api/v1/auth/logout',
    ME: '/api/v1/auth/me',
    REFRESH: '/api/v1/auth/refresh',
    CHANGE_PASSWORD: '/api/v1/auth/change-password',
  },
  TENANCY: {
    ORGANIZATIONS: '/api/v1/tenancy/organizations',
  },
  KEYS: {
    LIST: '/api/v1/keys',
    CREATE: '/api/v1/keys',
    UPDATE: '/api/v1/keys',
    DELETE: '/api/v1/keys',
    USAGE: '/api/v1/keys/usage',
  },
  BILLING: {
    SUBSCRIPTIONS: '/api/v1/billing/subscriptions',
    INVOICES: '/api/v1/billing/invoices',
    WEBHOOKS: '/api/v1/billing/webhooks',
  },
  SUPPORT: {
    TICKETS: '/api/v1/support/tickets',
    COMMENTS: '/api/v1/support/tickets/:id/comments',
    ATTACHMENTS: '/api/v1/support/tickets/:id/attachments',
  },
  THEMES: {
    LIST: '/api/v1/themes',
    CREATE: '/api/v1/themes',
    UPDATE: '/api/v1/themes/:id',
    DELETE: '/api/v1/themes/:id',
  },
  NOTIFICATIONS: {
    LIST: '/api/v1/notifications',
    TEMPLATES: '/api/v1/notifications/templates',
  },
  WORKERS: {
    JOBS: '/api/v1/workers/jobs',
    TEMPLATES: '/api/v1/workers/templates',
  },
} as const;

export const USER_ROLES = {
  SUPER_ADMIN: 'super_admin',
  ORG_ADMIN: 'org_admin',
  USER: 'user',
  SUPPORT_AGENT: 'support_agent',
  BILLING_ADMIN: 'billing_admin',
} as const;

export const SUBSCRIPTION_PLANS = {
  FREE: 'free',
  STARTER: 'starter',
  PRO: 'pro',
  ENTERPRISE: 'enterprise',
} as const;

export const TICKET_STATUSES = {
  OPEN: 'open',
  IN_PROGRESS: 'in_progress',
  RESOLVED: 'resolved',
  CLOSED: 'closed',
} as const;

export const JOB_STATUSES = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
} as const;