# Phase 6.1 — Frontend Project Foundation & Initialization

**Project:** Food Delivery Platform  
**Application:** Customer Application (MVP)  
**Phase:** 6.1 — Frontend Project Foundation & Initialization  
**Technology:** React 19, Vite 8, JavaScript, Tailwind CSS v4  
**Architecture:** Feature-Based Architecture with Shared Infrastructure  
**Branch:** `feature/phase-6-1-foundation`  
**Status:** Implementation tasks completed through Task 29; Task 30 verification and Git commit pending confirmation.

---

# 1. Phase Overview

## 1.1 Objective

Phase 6.1 establishes the technical foundation of the Food Delivery Platform frontend.

The objective is to prepare a maintainable, scalable, and production-oriented React application before implementing customer-facing pages and business features.

This phase establishes:

- Frontend project initialization.
- Development tooling and code quality standards.
- Feature-based folder architecture.
- Styling infrastructure and Figma design tokens.
- Routing and application layouts.
- API communication infrastructure.
- JWT authentication infrastructure.
- Global state and application providers.
- Environment configuration.
- Theme management.
- Global notification handling.
- Git workflow and verification.

The frontend is developed inside the existing Food Delivery Platform repository, alongside the backend.

## 1.2 Project Location

Repository:

```text
D:\Projects\food-delivery-platform
```

Frontend:

```text
D:\Projects\food-delivery-platform\frontend
```

Backend:

```text
D:\Projects\food-delivery-platform\backend
```

The frontend and backend remain separate applications within the same repository.

## 1.3 MVP Scope

The frontend implements the Customer Application only.

The MVP includes:

- Authentication.
- Restaurant discovery.
- Restaurant details and menus.
- Cart management.
- Coupon handling.
- Checkout.
- Payments.
- Order management.
- Reviews.
- Notifications.
- Customer profile and addresses.

Restaurant Portal, Delivery Partner Application, and Admin Dashboard are outside the current MVP scope.

---

# 2. Technology Stack

## 2.1 Core Technologies

| Category | Technology |
|---|---|
| UI Library | React 19 |
| Build Tool | Vite 8 |
| Language | JavaScript |
| Component Syntax | JSX |
| Routing | React Router |
| Server State | TanStack Query |
| HTTP Client | Axios |
| Styling | Tailwind CSS v4 |
| UI Component Foundation | shadcn/ui |
| Icons | Lucide React |
| Animations | Framer Motion |

**Important:** The frontend uses JavaScript and JSX throughout. TypeScript and TSX are not part of the approved frontend implementation.

## 2.2 Forms and Validation

| Technology | Responsibility |
|---|---|
| React Hook Form | Form state and submission |
| Zod | Schema-based validation |
| @hookform/resolvers | React Hook Form and Zod integration |

These dependencies are part of the planned frontend stack. Their feature-level implementation belongs to subsequent development tasks.

## 2.3 Development and Quality Tooling

| Technology | Responsibility |
|---|---|
| ESLint | Static code analysis |
| Prettier | Code formatting |
| Husky | Git hooks |
| lint-staged | Pre-commit validation |

## 2.4 Additional Libraries

| Library | Responsibility |
|---|---|
| React Hot Toast | Global toast notifications |
| clsx | Conditional CSS class composition |
| tailwind-merge | Resolving conflicting Tailwind classes |
| Lucide React | Icon components |
| Framer Motion | UI animations |

---

# 3. Git and Branch Configuration

## 3.1 Development Branch

The frontend foundation branch is:

```text
feature/phase-6-1-foundation
```

The repository already contains the backend application. Frontend development must not create a separate Git repository inside the frontend directory.

## 3.2 Commit Convention

The project follows Conventional Commits.

Format:

```text
<type>(<scope>): <description>
```

Examples:

```text
feat(frontend): initialize frontend application

feat(frontend): configure authentication foundation

feat(frontend): implement shared design system

fix(frontend): correct authentication provider

docs(frontend): document frontend foundation
```

## 3.3 Planned Phase 6.1 Commit

```powershell
git add .
git commit -m "feat(frontend): complete phase 6.1 foundation"
```

This commit must only be created after verification and review of staged changes.

---

# 4. Frontend Folder Architecture

The frontend follows a feature-based architecture with centralized infrastructure.

## 4.1 Target Folder Structure

```text
frontend/
│
├── public/
│
├── src/
│   │
│   ├── app/
│   │
│   ├── assets/
│   │
│   ├── components/
│   │   └── ui/
│   │
│   ├── config/
│   │   └── env.js
│   │
│   ├── constants/
│   │   ├── api.js
│   │   ├── app.js
│   │   └── routes.js
│   │
│   ├── contexts/
│   │   ├── auth-context.jsx
│   │   └── theme-context.jsx
│   │
│   ├── features/
│   │   ├── auth/
│   │   │   └── services/
│   │   │       └── auth-service.js
│   │   │
│   │   ├── restaurant/
│   │   ├── cart/
│   │   ├── checkout/
│   │   ├── coupon/
│   │   ├── order/
│   │   ├── payment/
│   │   ├── review/
│   │   ├── notification/
│   │   └── profile/
│   │
│   ├── hooks/
│   │   ├── use-auth.js
│   │   └── use-theme.js
│   │
│   ├── layouts/
│   │   ├── root-layout.jsx
│   │   ├── public-layout.jsx
│   │   ├── main-layout.jsx
│   │   └── error-layout.jsx
│   │
│   ├── lib/
│   │   └── utils.js
│   │
│   ├── providers/
│   │   ├── query-provider.jsx
│   │   ├── auth-provider.jsx
│   │   ├── theme-provider.jsx
│   │   └── toast-provider.jsx
│   │
│   ├── routes/
│   │   ├── guards/
│   │   │   ├── protected-route.jsx
│   │   │   └── public-route.jsx
│   │   │
│   │   └── app-router.jsx
│   │
│   ├── services/
│   │   ├── api/
│   │   ├── auth/
│   │   │   └── token-storage.js
│   │   │
│   │   ├── client/
│   │   │   └── api-client.js
│   │   │
│   │   ├── errors/
│   │   │   └── api-error.js
│   │   │
│   │   └── interceptors/
│   │       ├── request-interceptor.js
│   │       ├── response-interceptor.js
│   │       └── error-interceptor.js
│   │
│   ├── styles/
│   │   └── tokens.css
│   │
│   ├── types/
│   │
│   ├── utils/
│   │
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
│
├── .env
├── .env.example
├── .gitignore
├── components.json
├── eslint.config.js
├── jsconfig.json
├── package.json
├── package-lock.json
├── prettier.config.js
└── vite.config.js
```

Some feature folders are intentionally empty until their corresponding feature implementation phases.

## 4.2 Architectural Responsibilities

| Directory | Responsibility |
|---|---|
| app | Application-level configuration and composition |
| assets | Static images and other frontend assets |
| components/ui | Primitive UI components and design system |
| config | Environment and runtime configuration |
| constants | Application-wide constant values |
| contexts | React context definitions |
| features | Business-specific functionality |
| hooks | Reusable application hooks |
| layouts | Application-level page layouts |
| lib | Shared third-party library utilities |
| providers | Global React providers |
| routes | Route definitions and guards |
| services | Shared infrastructure and API communication |
| styles | Global styling and design tokens |
| types | Reserved architecture directory; no TypeScript migration |
| utils | Generic utility functions |

---

# 5. Development Tooling Configuration

## 5.1 ESLint

ESLint is configured for JavaScript and JSX.

The configuration includes:

- JavaScript recommended rules.
- React Hooks rules.
- React Fast Refresh rules.
- Browser globals.
- Global exclusions for generated files and dependencies.

A targeted exception is configured for generated shadcn/ui components where the component-export rule conflicts with their generated exports.

The rule should not be disabled globally without a specific reason.

## 5.2 Prettier

Prettier is used for consistent source formatting.

Expected scripts:

```json
{
  "format": "prettier --write .",
  "format:check": "prettier --check ."
}
```

The following should be excluded from formatting:

```text
node_modules/
dist/
coverage/
package-lock.json
.env
.env.*
*.min.js
*.min.css
```

## 5.3 Husky and lint-staged

Husky manages Git hooks.

The pre-commit hook runs lint-staged.

The hook file is:

```text
frontend/.husky/pre-commit
```

Its intended content:

```sh
cd frontend
npx lint-staged
```

The package's prepare script configures the hook path from the repository root.

---

# 6. Tailwind CSS and Figma Design Tokens

## 6.1 Styling Architecture

The project uses:

- Tailwind CSS v4.
- CSS custom properties.
- shadcn/ui.
- Semantic design tokens.
- Mobile-first responsive styling.

Styling hierarchy:

```text
Figma Design Tokens
        ↓
CSS Variables
        ↓
Tailwind Utilities
        ↓
Primitive UI Components
        ↓
Shared Components
        ↓
Feature Components
```

Visual styling should not contain business logic.

## 6.2 Figma Token Files

The project has two supplied token files:

```text
Light.tokens.json
Dark.tokens.json
```

The CSS implementation is maintained in:

```text
src/styles/tokens.css
```

The default theme is light.

Dark mode is selected through:

```html
data-theme="dark"
```

## 6.3 Light Theme Colors

| Token | Value |
|---|---|
| Primary | #4CAF50 |
| On Primary | #FFFFFF |
| Primary Container | #C8E6C9 |
| On Primary Container | #1B5E20 |
| Secondary | #FF9800 |
| On Secondary | #FFFFFF |
| Secondary Container | #FFE0B2 |
| On Secondary Container | #E65100 |
| Tertiary | #F44336 |
| On Tertiary | #FFFFFF |
| Tertiary Container | #FFCDD2 |
| On Tertiary Container | #B71C1C |
| Error | #B3261E |
| On Error | #FFFFFF |
| Error Container | #FFDAD4 |
| On Error Container | #410E0B |
| Surface | #FFFFFF |
| On Surface | #000000 |
| Surface Variant | #F5F5F5 |
| On Surface Variant | #616161 |
| Outline | #BDBDBD |
| Outline Variant | #757575 |
| Veg | #388E3C |
| Non Veg | #D32F2F |

## 6.4 Dark Theme Colors

| Token | Value |
|---|---|
| Primary | #81C784 |
| On Primary | #000000 |
| Primary Container | #388E3C |
| On Primary Container | #FFFFFF |
| Secondary | #FFB74D |
| On Secondary | #000000 |
| Secondary Container | #F57C00 |
| On Secondary Container | #FFFFFF |
| Tertiary | #EF9A9A |
| On Tertiary | #000000 |
| Tertiary Container | #C62828 |
| On Tertiary Container | #FFFFFF |
| Error | #F2B8B5 |
| On Error | #000000 |
| Error Container | #601410 |
| On Error Container | #FFDAD4 |
| Surface | #121212 |
| On Surface | #FFFFFF |
| Surface Variant | #212121 |
| On Surface Variant | #BDBDBD |
| Outline | #424242 |
| Outline Variant | #9E9E9E |
| Veg | #66BB6A |
| Non Veg | #E57373 |

**Important:** Preserve the original Figma values. Do not replace them with generic Tailwind colors or invent new palette values.

## 6.5 Global CSS

The global stylesheet is:

```text
src/index.css
```

It imports:

```css
@import "tailwindcss";
@import "./styles/tokens.css";
```

It also establishes:

- Global box sizing.
- Base body typography.
- Minimum viewport dimensions.
- Root layout.
- Form control font inheritance.
- Image and media behavior.
- Link defaults.

---

# 7. Vite and Import Alias Configuration

## 7.1 Vite Configuration

File:

```text
vite.config.js
```

The configuration includes:

- React plugin.
- Tailwind CSS v4 Vite plugin.
- `@` alias pointing to `src`.

Expected configuration:

```javascript
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
```

## 7.2 JavaScript Path Configuration

File:

```text
jsconfig.json
```

Expected configuration:

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}
```

Example:

```javascript
import apiClient from "@/services/client/api-client";
```

---

# 8. shadcn/ui and Shared Utility

shadcn/ui was initialized.

The project includes:

```text
components.json
src/components/ui/button.jsx
src/lib/utils.js
```

The `cn()` utility combines conditional classes and resolves Tailwind conflicts.

Expected implementation:

```javascript
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
```

shadcn/ui components are treated as project-owned source code and may be customized to match Figma.

---

# 9. Routing Infrastructure

## 9.1 React Router

React Router is configured using `createBrowserRouter` and `RouterProvider`.

The central route definition is:

```text
src/routes/app-router.jsx
```

## 9.2 Layouts

Four layout components were established:

| Layout | Responsibility |
|---|---|
| RootLayout | Root route composition |
| PublicLayout | Public-facing pages |
| MainLayout | Authenticated customer application |
| ErrorLayout | Route error handling |

Layouts use `Outlet` to render nested routes.

## 9.3 Planned Frontend Routes

| Route | Access |
|---|---|
| `/` | Public |
| `/login` | Public |
| `/register` | Public |
| `/restaurants` | Public |
| `/restaurants/:restaurantId` | Public |
| `/menu/:menuItemId` | Public |
| `/cart` | Protected |
| `/checkout` | Protected |
| `/orders` | Protected |
| `/orders/:orderId` | Protected |
| `/notifications` | Protected |
| `/profile` | Protected |
| `/addresses` | Protected |
| `/reviews` | Protected |

The actual page components are implemented in later feature phases.

## 9.4 Route Guards

Two guard components were created:

```text
src/routes/guards/protected-route.jsx
src/routes/guards/public-route.jsx
```

ProtectedRoute:

- Checks authentication.
- Waits for authentication initialization.
- Redirects unauthenticated visitors to `/login`.
- Preserves the original requested location.

PublicRoute:

- Waits for authentication initialization.
- Prevents authenticated customers from unnecessarily visiting login/register pages.
- Redirects them to an appropriate destination.

**Integration status:** The guard components were created, but their integration with actual login/register and protected page routes must be completed when those pages are implemented.

---

# 10. API Communication Infrastructure

## 10.1 API Base URL

The local development API base URL is:

```text
http://localhost:8000/api/v1
```

Frontend environment variable:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 10.2 Axios Client

File:

```text
src/services/client/api-client.js
```

The Axios client configures:

- Centralized API base URL.
- 15-second timeout.
- JSON Accept header.
- JSON Content-Type header.
- Request interceptor.
- Response interceptor.
- Error interceptor.

## 10.3 Interceptors

| Interceptor | Responsibility |
|---|---|
| Request | Attaches JWT and logs development request metadata |
| Response | Centralizes successful response handling |
| Error | Normalizes backend and network errors |

## 10.4 API Error Class

File:

```text
src/services/errors/api-error.js
```

The normalized error object includes:

- `code`
- `message`
- `details`
- `status`
- `traceId`

The error interceptor supports:

- FastAPI `detail` string errors.
- FastAPI validation error arrays.
- Standardized `message` and `code` responses.
- Network errors.
- Timeout errors.
- HTTP status information.

The backend's actual error response contract remains unchanged.

## 10.5 API Endpoint Constants

File:

```text
src/constants/api.js
```

All documented backend endpoints are centralized here.

The endpoint groups include:

- Authentication.
- Restaurants.
- Menu items.
- Cart.
- Coupons.
- Customer.
- Orders.
- Payments.
- Reviews.
- Notifications.

### Coupon API

Dedicated coupon validation:

```text
GET /coupons/validate
```

Cart coupon operations:

```text
POST /cart/coupon
DELETE /cart/coupon
```

Coupon validation is separate from applying a coupon to the cart.

The frontend endpoint constants use relative paths because the Axios base URL already includes `/api/v1`.

---

# 11. Authentication Infrastructure

## 11.1 Backend Authentication Contract

The frontend follows the supplied backend API documentation.

| Operation | Method | Endpoint |
|---|---|---|
| Register | POST | `/auth/register` |
| Login | POST | `/auth/login` |
| Current customer | GET | `/auth/me` |

Login response includes:

```json
{
  "access_token": "JWT_ACCESS_TOKEN",
  "token_type": "bearer",
  "customer": {
    "customer_id": "uuid",
    "email": "customer@example.com",
    "full_name": "Customer Name"
  }
}
```

The documented backend token expiry is 24 hours.

Refresh tokens are not implemented in the documented backend contract.

A logout API endpoint is not documented.

## 11.2 JWT Storage

File:

```text
src/services/auth/token-storage.js
```

For the current MVP foundation, the access token is stored in `sessionStorage`.

Functions:

- `getAccessToken()`
- `setAccessToken(token)`
- `removeAccessToken()`
- `hasAccessToken()`

This is a development/MVP storage decision, not a claim that browser storage is the strongest production security model.

JavaScript-accessible storage is exposed to successful XSS attacks. A future production security review should consider an HttpOnly, Secure, appropriately configured SameSite cookie approach if supported by the backend.

## 11.3 Request Interceptor

The Axios request interceptor automatically attaches:

```http
Authorization: Bearer <access_token>
```

Protected API services therefore do not need to manually add the JWT header.

The token itself must never be written to console logs.

## 11.4 Authentication Service

File:

```text
src/features/auth/services/auth-service.js
```

Implemented functions:

| Function | Responsibility |
|---|---|
| `register()` | Registers a customer |
| `login()` | Authenticates and stores the JWT |
| `getCurrentCustomer()` | Retrieves authenticated customer |
| `logout()` | Clears the locally stored token |

Logout is currently client-side because the documented backend has no logout endpoint.

## 11.5 Authentication Context

File:

```text
src/contexts/auth-context.jsx
```

Defines the shared authentication context.

The hook is separated into:

```text
src/hooks/use-auth.js
```

This separation also avoids the React Fast Refresh ESLint error caused by exporting a non-component hook from a component-related context module.

## 11.6 Authentication Provider

File:

```text
src/providers/auth-provider.jsx
```

Responsibilities:

- Maintains current customer state.
- Maintains authentication loading state.
- Restores an existing session.
- Calls `/auth/me` when a token exists.
- Clears invalid or unusable tokens.
- Exposes login.
- Exposes registration.
- Exposes logout.
- Exposes customer state update functionality.

## 11.7 Authentication Initialization

Application startup flow:

```text
Application Starts
        ↓
Check Stored JWT
        ↓
Token Exists?
   /           \
 No             Yes
 |               |
Unauthenticated  GET /auth/me
 |               |
 |          Request Successful?
 |             /       \
 |            Yes       No
 |             |         |
 |       Restore User   Clear Token
 |             |         |
  \            |        /
       Authentication Ready
```

---

# 12. Global Application Providers

The application provider hierarchy is:

```jsx
<StrictMode>
  <QueryProvider>
    <ThemeProvider>
      <AuthProvider>
        <ToastProvider>
          <RouterProvider router={router} />
        </ToastProvider>
      </AuthProvider>
    </ThemeProvider>
  </QueryProvider>
</StrictMode>
```

## 12.1 QueryProvider

File:

```text
src/providers/query-provider.jsx
```

Provides TanStack Query.

Configured defaults:

- Query stale time: 60 seconds.
- Query retry: 1.
- Refetch on window focus: disabled.
- Mutation retry: 0.

## 12.2 ThemeProvider

File:

```text
src/providers/theme-provider.jsx
```

Provides:

- Current theme.
- Dark-mode state.
- Theme toggle.
- Explicit theme change.
- Theme persistence through localStorage.

Theme context:

```text
src/contexts/theme-context.jsx
```

Theme hook:

```text
src/hooks/use-theme.js
```

## 12.3 ToastProvider

File:

```text
src/providers/toast-provider.jsx
```

Uses React Hot Toast.

Supports:

- Success notifications.
- Error notifications.
- Loading notifications.
- Informational notifications.

One global `Toaster` is used for the application.

---

# 13. Environment and Application Configuration

## 13.1 Environment Configuration

File:

```text
src/config/env.js
```

Centralizes:

- API base URL.
- Application name.
- Development mode.
- Production mode.

## 13.2 Environment Variables

`.env`:

```env
VITE_APP_NAME=Food Delivery Platform
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

`.env.example` contains the same variable names and safe example values.

`.env` must not be committed.

Only browser-safe configuration should use the `VITE_` prefix. Secrets, database passwords, JWT signing keys, and private API credentials must never be exposed through Vite environment variables.

## 13.3 Application Constants

File:

```text
src/constants/app.js
```

Contains application metadata and configuration defaults, including the application name, description, pagination defaults, and currently selected currency/locale settings.

The INR and India-related values should be confirmed against the approved product requirements before they are treated as immutable business rules.

## 13.4 Route Constants

File:

```text
src/constants/routes.js
```

Centralizes frontend route path patterns.

Dynamic route values must be inserted using actual resource identifiers.

---

# 14. Phase 6.1 Task Breakdown

| Task | Description | Implementation |
|---|---|---|
| 1 | Environment verification | Completed |
| 2 | Vite React application initialization | Completed |
| 3 | Git branch setup | Completed |
| 4 | Existing project inspection | Completed |
| 5 | Prettier installation | Completed |
| 6 | Husky and lint-staged | Completed |
| 7 | Prettier ignore configuration | Completed |
| 8 | Feature-based folder structure | Completed |
| 9 | Initial App and entry point | Completed |
| 10 | Global CSS foundation | Completed |
| 11 | Figma design tokens | Completed |
| 12 | Import alias configuration | Completed |
| 13 | Frontend dependencies | Completed |
| 14 | Tailwind CSS v4 | Completed |
| 15 | shadcn/ui initialization | Completed |
| 16 | Shared `cn()` utility | Completed |
| 17 | TanStack Query provider | Completed |
| 18 | React Router foundation | Completed |
| 19 | Application layouts | Completed |
| 20 | Axios shared client | Completed |
| 21 | Axios interceptors and error normalization | Completed |
| 22 | Backend API documentation review and endpoint constants | Completed |
| 23 | FastAPI error response compatibility | Completed |
| 24 | JWT token storage and request injection | Completed |
| 25 | Authentication API service | Completed |
| 26 | Authentication Context and Provider | Completed |
| 27 | Protected and public route guards | Components created; route integration pending |
| 28 | Environment and application constants | Implemented; verify current values |
| 29 | Global providers and theme management | Implemented |
| 30 | Foundation verification and Git commit | Pending confirmation |

---

# 15. Verification and Quality Gates

The following commands must be executed from:

```text
D:\Projects\food-delivery-platform\frontend
```

## 15.1 Git Branch

```powershell
git branch --show-current
```

Expected:

```text
feature/phase-6-1-foundation
```

## 15.2 Environment Protection

```powershell
git check-ignore -v .env
```

```powershell
git ls-files .env
```

```powershell
git check-ignore .env.example
```

Expected:

- `.env` is ignored.
- `.env` is not tracked.
- `.env.example` is not ignored.

## 15.3 ESLint

```powershell
npm run lint
```

Expected: No lint errors.

## 15.4 Prettier

```powershell
npm run format:check
```

If required:

```powershell
npm run format
```

Then rerun the formatting check.

## 15.5 Production Build

```powershell
npm run build
```

Expected: Successful Vite production build.

## 15.6 Git Diff Validation

```powershell
git diff --check
```

```powershell
git status --short
```

Review the staged changes before committing.

## 15.7 Git Commit

After all checks pass:

```powershell
git add .
```

```powershell
git status
```

```powershell
git commit -m "feat(frontend): complete phase 6.1 foundation"
```

Then:

```powershell
git status
```

Expected:

```text
nothing to commit, working tree clean
```

Do not mark Task 30 complete until these checks and the commit have actually succeeded.

---

# 16. Known Implementation Boundaries and Follow-Up Checks

The following points must be considered before building on this foundation.

1. The actual frontend login and registration pages have not yet been implemented.
2. Protected and public route guards exist, but must be integrated when their corresponding page routes are created.
3. The initial `App.jsx` is a temporary foundation/verification component, not the finished customer homepage.
4. The API error interceptor supports the documented FastAPI error format, but field-level form error mapping is a later form architecture task.
5. The backend does not document a logout endpoint or refresh-token flow.
6. Token storage currently uses sessionStorage and requires a production security review.
7. The coupon validation endpoint must be checked against the actual backend router before implementing its frontend service.
8. The current frontend API endpoint constants should be compared against the actual backend API documentation and implementation before feature development.
9. The INR currency and India-specific application defaults should be checked against approved product requirements.
10. The current Figma color tokens should remain the source of truth for visual styling.

Do not redesign the backend, database schema, API contracts, or approved frontend architecture during subsequent phases unless an actual implementation blocker requires it.

---

# 17. Phase 6.1 Exit Criteria

Phase 6.1 can be formally marked complete when:

- The Vite React application is operational.
- JavaScript and JSX are used consistently.
- The approved folder architecture exists.
- Tailwind CSS and shadcn/ui are configured.
- Figma color tokens are integrated.
- Import aliases work.
- React Router is configured.
- Layout foundations exist.
- TanStack Query is configured.
- Axios and interceptors are configured.
- Authentication service and context are configured.
- JWT token handling is implemented.
- Route guard components exist.
- Environment configuration is centralized.
- Theme and toast providers are configured.
- ESLint passes.
- Prettier passes.
- Production build succeeds.
- `.env` is protected from Git.
- Git changes are committed.
- Working tree is clean.

---

# 18. Next Phase

## Phase 6.2 — Shared UI Components and Design System Implementation

**Objective:** Implement the reusable UI foundation based on the approved Figma design and existing design-system architecture.

The next phase will focus on:

1. Design token and styling foundation review.
2. Typography system.
3. Color and semantic styling utilities.
4. Spacing, border radius, borders, and elevation.
5. Primitive UI components.
6. Shared reusable UI components.
7. Loading, empty, error, and feedback components.
8. Overlay and interaction components.
9. Responsive behavior.
10. Accessibility and component verification.

The project will follow the established layered component architecture:

```text
Primitive Components
        ↓
Shared Components
        ↓
Feature Components
        ↓
Page Components
```

The implementation should use shadcn/ui as the primary component foundation while preserving the ability to customize the components to match the approved Figma designs.

Do not begin implementing complete business pages in this phase.

---

# 19. Final Engineering Principle

The frontend should be developed as a maintainable product application, not as a collection of disconnected screens.

Every implementation should follow these principles:

- Preserve approved architecture.
- Use JavaScript and JSX.
- Keep API communication outside UI components.
- Keep business logic inside its owning feature.
- Reuse primitive and shared UI components appropriately.
- Avoid premature abstraction.
- Use actual Figma design tokens.
- Follow mobile-first responsive design.
- Implement accessible interactions.
- Validate every meaningful implementation with lint, formatting, and build checks.
- Keep the backend API contract unchanged unless a genuine requirement demands a change.

**End of Phase 6.1 Documentation.**