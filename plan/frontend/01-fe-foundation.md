# FE-01 – Frontend Foundation

## Mục tiêu
Tạo nền tảng UI và application shell.

## Stack bắt buộc
- React + Vite + TypeScript
- Tailwind CSS + shadcn/ui
- React Router
- TanStack Query
- Zustand
- React Hook Form + Zod
- npm

Không tự đổi sang Next.js hoặc framework khác.

## Tasks

### FE-01.1 App shell
- [x] Root layout
- [x] Header
- [x] Sidebar
- [x] Main content container
- [x] Responsive behavior theo scope

### FE-01.2 Design system
- [x] NextTech colors
- [x] Typography
- [x] Buttons
- [x] Inputs
- [x] Select
- [x] Tabs
- [x] Badge
- [x] Card
- [x] Progress
- [x] Tooltip
- [x] Modal
- [x] Toast

### FE-01.3 State patterns
- [x] Loading
- [x] Empty
- [x] Error
- [x] Retry
- [x] Disabled
- [x] Permission denied

### FE-01.4 Data & form foundation
- [x] TanStack Query provider
- [x] API client
- [x] Query key convention
- [x] Zustand chỉ cho client state cần thiết
- [x] React Hook Form + Zod pattern

### FE-01.5 Routing
- [x] `/login`
- [x] `/dashboard`
- [x] `/learn`
- [x] `/learn/:topicId`
- [x] `/quiz/:quizId`
- [x] `/exercise/:exerciseId`
- [x] `/skills`
- [x] `/recommendations`
- [x] `/prediction`
- [x] `/admin/*`

## Tests
- [x] Component smoke tests
- [x] Navigation tests
- [x] Error boundary test
- [x] Keyboard focus basic check
- [x] No console error on initial pages
- [x] `npm run build` pass
- [x] lockfile committed

## Done
- [x] App shell usable
- [x] Tokens reused, no random hard-coded palette
- [x] Common states reusable
