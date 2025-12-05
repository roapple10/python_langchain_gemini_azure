<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution)
- Modified principles: N/A (new constitution)
- Added sections: Core Principles, Performance Standards, Accessibility Requirements, Development Workflow
- Removed sections: N/A
- Templates requiring updates:
  - ✅ plan-template.md - Constitution Check section aligns with principles
  - ✅ spec-template.md - Success Criteria section aligns with performance requirements
  - ✅ tasks-template.md - Test-first workflow aligns with TDD principle
  - ⚠️ Follow-up: Ensure all future plans reference constitution principles
- Follow-up TODOs: None
-->

# Forest Focus Constitution

## Core Principles

### I. Radical Simplicity (NON-NEGOTIABLE)
Every feature, component, and decision MUST prioritize simplicity over cleverness. 
- YAGNI (You Aren't Gonna Need It): Do not build features "just in case"
- Single Responsibility: Each component has one clear purpose
- Minimal Dependencies: Prefer native browser APIs over frameworks when possible
- Clear Naming: Code should read like documentation
- No Over-Engineering: Reject abstractions that don't provide immediate, measurable value

### II. Offline-First Architecture (NON-NEGOTIABLE)
The application MUST function completely offline without network dependencies.
- All data persistence via localStorage (no backend required)
- No external API calls for core functionality
- Graceful degradation: App works even if browser APIs are limited
- Progressive Enhancement: Core features work without JavaScript if possible
- Service Worker optional: Only if it adds clear value without complexity

### III. Test-First Development (NON-NEGOTIABLE)
TDD is mandatory: Tests written → User approved → Tests fail → Then implement.
- Red-Green-Refactor cycle strictly enforced
- Every feature MUST have tests before implementation
- Tests must be independent and runnable in isolation
- Test coverage: Critical paths MUST have tests; aim for >80% coverage
- Tests document expected behavior and serve as living documentation

### IV. Performance Standards (NON-NEGOTIABLE)
Performance is a feature, not an afterthought.
- Page Load: Initial page load MUST be <2 seconds on 3G connection
- Animations: All animations MUST maintain 60fps (16.67ms per frame)
- Bundle Size: Keep initial bundle <200KB (gzipped)
- Runtime Performance: No janky interactions; smooth scrolling and transitions
- Lazy Loading: Defer non-critical resources

### V. Responsive Design (NON-NEGOTIABLE)
The application MUST work seamlessly across all device sizes.
- Mobile-First: Design for smallest screen first, enhance for larger screens
- Touch Targets: Minimum 44x44px for interactive elements
- Viewport: Proper viewport meta tag and responsive units (rem, %, vw/vh)
- Breakpoints: Use logical breakpoints (mobile: <768px, tablet: 768-1024px, desktop: >1024px)
- Flexible Layouts: Use CSS Grid/Flexbox, avoid fixed widths

### VI. Accessibility Support (NON-NEGOTIABLE)
The application MUST be accessible to all users.
- WCAG 2.1 Level AA compliance minimum
- Keyboard Navigation: All features accessible via keyboard
- Screen Reader Support: Proper ARIA labels and semantic HTML
- Color Contrast: Minimum 4.5:1 for normal text, 3:1 for large text
- Focus Indicators: Visible focus states for all interactive elements
- Alt Text: Meaningful alt text for images and icons

## Performance Constraints

### Load Time Requirements
- Initial HTML load: <500ms
- Critical CSS inline: <50KB
- JavaScript execution: <1s for Time to Interactive (TTI)
- Total page load: <2s on 3G (1.6 Mbps down, 750 Kbps up)

### Animation Performance
- Use CSS transforms and opacity (GPU-accelerated properties)
- Avoid layout-triggering properties (width, height, top, left)
- Use `requestAnimationFrame` for JavaScript animations
- Debounce/throttle scroll and resize handlers
- Test on low-end devices (target: iPhone 6S or equivalent)

### Bundle Optimization
- Code splitting: Lazy load routes/components
- Tree shaking: Remove unused code
- Minification: Production builds must be minified
- Compression: Enable gzip/brotli compression
- Image optimization: Use WebP format, lazy load images

## Accessibility Requirements

### Semantic HTML
- Use proper HTML5 semantic elements (nav, main, article, section, header, footer)
- Form labels MUST be associated with inputs
- Headings MUST follow logical hierarchy (h1 → h2 → h3)

### ARIA Usage
- Use ARIA labels when semantic HTML is insufficient
- ARIA live regions for dynamic content updates
- Proper ARIA roles for custom components
- Avoid ARIA when native HTML provides the same functionality

### Keyboard Navigation
- Tab order follows visual flow
- All interactive elements reachable via Tab
- Escape key closes modals/dropdowns
- Enter/Space activate buttons and links
- Arrow keys navigate lists/menus where appropriate

### Visual Accessibility
- Color is not the only indicator of state/importance
- Text alternatives for icons and images
- Sufficient color contrast ratios
- Scalable text (no fixed pixel sizes that break zoom)

## Development Workflow

### Test-First Process
1. Write failing test(s) that describe desired behavior
2. Get user/team approval on test expectations
3. Verify tests fail (Red phase)
4. Write minimal code to make tests pass (Green phase)
5. Refactor while keeping tests green (Refactor phase)
6. Repeat for next feature

### Code Review Requirements
- All PRs MUST include tests for new features
- Performance impact MUST be assessed (bundle size, load time)
- Accessibility MUST be verified (keyboard nav, screen reader)
- Simplicity MUST be maintained (no unnecessary complexity)

### Quality Gates
Before merging any PR:
- ✅ All tests pass
- ✅ Bundle size within limits
- ✅ Performance budgets met
- ✅ Accessibility audit passed
- ✅ Code review approved
- ✅ No console errors/warnings

## Technology Constraints

### Preferred Stack
- **Frontend Framework**: React with TypeScript (or vanilla JS if simpler)
- **Build Tool**: Vite (fast, simple, modern)
- **Testing**: Vitest (fast, Vite-native)
- **Styling**: CSS Modules or Tailwind CSS (utility-first, small bundle)
- **State Management**: React Context/useState (avoid Redux unless complexity justifies)

### Avoid
- Heavy frameworks that add unnecessary complexity
- Dependencies that significantly increase bundle size
- Runtime dependencies that require network access
- Tools that don't support offline development

## Governance

### Constitution Authority
This constitution supersedes all other development practices and guidelines. 
Any deviation MUST be justified and documented in the Complexity Tracking section of implementation plans.

### Amendment Process
- Amendments require team discussion and consensus
- Version increments follow semantic versioning:
  - MAJOR: Backward incompatible principle changes
  - MINOR: New principles or significant expansions
  - PATCH: Clarifications and minor refinements
- All amendments MUST update this document with version and date

### Compliance
- All implementation plans MUST include a "Constitution Check" section
- Code reviews MUST verify constitution compliance
- Violations MUST be documented with justification or fixed before merge
- Regular audits ensure ongoing compliance

### Version History
- **Version**: 1.0.0
- **Ratified**: 2025-01-27
- **Last Amended**: 2025-01-27
