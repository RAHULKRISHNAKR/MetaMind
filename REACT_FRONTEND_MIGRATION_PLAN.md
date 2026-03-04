# React + Vite Frontend Migration Plan

## Overview
Migrate MetaMind frontend from Streamlit to React + Vite for a richer, more interactive user experience.

## Current State
- **Framework**: Streamlit (Python-based)
- **File**: `frontend/app.py` (1000+ lines)
- **Pros**: Quick prototyping, Python integration
- **Cons**: Limited customization, page reloads, less interactive

## Target State
- **Framework**: React 18 + Vite 5
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand or React Query
- **API Client**: Axios with React Query
- **Build Tool**: Vite (fast HMR, optimized builds)

---

## Phase 1: Project Setup & Architecture

### 1.1 Create React + Vite Project
```bash
cd /Users/rahukkrishnakr/Documents/github/MetaMind
npm create vite@latest frontend-react -- --template react-ts
cd frontend-react
npm install
```

### 1.2 Install Core Dependencies
```bash
# UI Framework & Styling
npm install tailwindcss postcss autoprefixer
npm install @radix-ui/react-* # For shadcn/ui components
npm install class-variance-authority clsx tailwind-merge

# State & Data Fetching
npm install @tanstack/react-query axios zustand

# Routing
npm install react-router-dom

# Forms & Validation
npm install react-hook-form zod @hookform/resolvers

# Code Editor (for interactive builder)
npm install @monaco-editor/react

# Visualization
npm install recharts lucide-react

# Utilities
npm install date-fns
```

### 1.3 Project Structure
```
frontend-react/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── layout/          # Layout components
│   │   ├── design/          # Design flow components
│   │   ├── results/         # Results display
│   │   └── code-editor/     # Code generation UI
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── DesignFlow.tsx
│   │   ├── Results.tsx
│   │   └── CodeEditor.tsx
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API services
│   ├── store/               # Zustand stores
│   ├── types/               # TypeScript types
│   ├── utils/               # Utility functions
│   ├── App.tsx
│   └── main.tsx
├── public/
├── index.html
├── vite.config.ts
├── tailwind.config.js
└── package.json
```

---

## Phase 2: Core Components Development

### 2.1 API Service Layer
**File**: `src/services/api.ts`

```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Design API
export const designAPI = {
  startDesign: (data: DesignRequest) => 
    api.post('/api/design', data),
  
  getStatus: (runId: string) => 
    api.get(`/api/design/${runId}/status`),
  
  getProgress: (runId: string) => 
    api.get(`/api/design/${runId}/progress`),
  
  getResult: (runId: string) => 
    api.get(`/api/design/${runId}/result`),
  
  generateCode: (runId: string, data: CodeGenerationRequest) => 
    api.post(`/api/design/${runId}/generate-code`, data),
  
  downloadProject: (runId: string, projectId: string) => 
    api.get(`/api/design/${runId}/download/${projectId}`, {
      responseType: 'blob'
    }),
};
```

### 2.2 React Query Hooks
**File**: `src/hooks/useDesign.ts`

```typescript
import { useMutation, useQuery } from '@tanstack/react-query';
import { designAPI } from '@/services/api';

export const useStartDesign = () => {
  return useMutation({
    mutationFn: designAPI.startDesign,
    onSuccess: (data) => {
      // Handle success
    },
  });
};

export const useDesignProgress = (runId: string, enabled: boolean) => {
  return useQuery({
    queryKey: ['design-progress', runId],
    queryFn: () => designAPI.getProgress(runId),
    enabled,
    refetchInterval: 2000, // Poll every 2 seconds
  });
};

export const useDesignResult = (runId: string) => {
  return useQuery({
    queryKey: ['design-result', runId],
    queryFn: () => designAPI.getResult(runId),
  });
};
```

### 2.3 Design Flow Component
**File**: `src/pages/DesignFlow.tsx`

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useStartDesign } from '@/hooks/useDesign';
import { DesignForm } from '@/components/design/DesignForm';
import { ProgressTracker } from '@/components/design/ProgressTracker';

export const DesignFlow = () => {
  const navigate = useNavigate();
  const startDesign = useStartDesign();
  const [runId, setRunId] = useState<string | null>(null);

  const handleSubmit = async (data: DesignRequest) => {
    const result = await startDesign.mutateAsync(data);
    setRunId(result.data.run_id);
    navigate(`/design/${result.data.run_id}`);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">
        Design Your AI Pipeline
      </h1>
      <DesignForm onSubmit={handleSubmit} />
    </div>
  );
};
```

### 2.4 Results Dashboard
**File**: `src/pages/Results.tsx`

```typescript
import { useParams } from 'react-router-dom';
import { useDesignResult } from '@/hooks/useDesign';
import { ArchitectureVisualization } from '@/components/results/ArchitectureVisualization';
import { MetricsDisplay } from '@/components/results/MetricsDisplay';
import { CodeGenerationPanel } from '@/components/results/CodeGenerationPanel';

export const Results = () => {
  const { runId } = useParams<{ runId: string }>();
  const { data, isLoading } = useDesignResult(runId!);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ArchitectureVisualization 
          architecture={data.selected_architecture} 
        />
        <MetricsDisplay 
          metrics={data.metrics}
          score={data.score}
        />
      </div>
      <CodeGenerationPanel runId={runId!} />
    </div>
  );
};
```

---

## Phase 3: UI Components with shadcn/ui

### 3.1 Install shadcn/ui
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button card input label select textarea
npx shadcn-ui@latest add tabs badge progress alert
npx shadcn-ui@latest add dialog dropdown-menu tooltip
```

### 3.2 Custom Components

#### Design Form
**File**: `src/components/design/DesignForm.tsx`

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';

const designSchema = z.object({
  business_goal: z.string().min(10),
  domain: z.enum(['healthcare', 'finance', 'ecommerce', 'education', 'legal', 'general']),
  modalities: z.array(z.string()).min(1),
  constraints: z.object({
    budget: z.number().min(0),
    latency_target_ms: z.number().min(0),
    risk_tolerance: z.enum(['low', 'medium', 'high']),
    compliance_level: z.enum(['low', 'medium', 'high']),
    expected_users: z.number().min(0),
  }),
});

export const DesignForm = ({ onSubmit }) => {
  const form = useForm({
    resolver: zodResolver(designSchema),
    defaultValues: {
      business_goal: '',
      domain: 'general',
      modalities: [],
      constraints: {
        budget: 10000,
        latency_target_ms: 500,
        risk_tolerance: 'medium',
        compliance_level: 'medium',
        expected_users: 10000,
      },
    },
  });

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      {/* Form fields */}
    </form>
  );
};
```

#### Progress Tracker
**File**: `src/components/design/ProgressTracker.tsx`

```typescript
import { useDesignProgress } from '@/hooks/useDesign';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

export const ProgressTracker = ({ runId }: { runId: string }) => {
  const { data } = useDesignProgress(runId, true);

  const stages = data?.progress?.stages || [];
  const currentStage = data?.progress?.current_stage;

  return (
    <div className="space-y-4">
      <Progress value={calculateProgress(stages)} />
      <div className="space-y-2">
        {stages.map((stage, idx) => (
          <div key={idx} className="flex items-center gap-2">
            <Badge variant={stage === currentStage ? 'default' : 'secondary'}>
              {stage}
            </Badge>
            <span className="text-sm text-muted-foreground">
              {data.progress.current_message}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
```

#### Architecture Visualization
**File**: `src/components/results/ArchitectureVisualization.tsx`

```typescript
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export const ArchitectureVisualization = ({ architecture }) => {
  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">{architecture.name}</h2>
      <div className="space-y-4">
        {architecture.modules.map((module, idx) => (
          <div key={idx} className="border-l-4 border-primary pl-4">
            <Badge>{module.layer}</Badge>
            <p className="font-medium mt-2">{module.component}</p>
            <pre className="text-xs text-muted-foreground mt-1">
              {JSON.stringify(module.config, null, 2)}
            </pre>
          </div>
        ))}
      </div>
    </Card>
  );
};
```

#### Metrics Display
**File**: `src/components/results/MetricsDisplay.tsx`

```typescript
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

export const MetricsDisplay = ({ metrics, score }) => {
  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">
        Overall Score: {score.toFixed(1)}
      </h2>
      <div className="space-y-4">
        {Object.entries(metrics).map(([key, value]) => (
          <div key={key}>
            <div className="flex justify-between mb-2">
              <span className="capitalize">{key.replace('_', ' ')}</span>
              <span className="font-medium">{value.toFixed(1)}</span>
            </div>
            <Progress value={value} />
          </div>
        ))}
      </div>
    </Card>
  );
};
```

---

## Phase 4: Code Editor Integration

### 4.1 Monaco Editor Component
**File**: `src/components/code-editor/MonacoEditor.tsx`

```typescript
import Editor from '@monaco-editor/react';

export const MonacoEditor = ({ file, onChange }) => {
  return (
    <Editor
      height="600px"
      language={getLanguage(file.path)}
      value={file.content}
      onChange={onChange}
      theme="vs-dark"
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        scrollBeyondLastLine: false,
      }}
    />
  );
};
```

### 4.2 File Tree Component
**File**: `src/components/code-editor/FileTree.tsx`

```typescript
import { ChevronRight, ChevronDown, File, Folder } from 'lucide-react';

export const FileTree = ({ files, onFileSelect }) => {
  // Recursive tree rendering
  return (
    <div className="space-y-1">
      {files.map(file => (
        <FileTreeNode 
          key={file.path} 
          file={file} 
          onSelect={onFileSelect}
        />
      ))}
    </div>
  );
};
```

---

## Phase 5: Deployment Configuration

### 5.1 Vite Configuration
**File**: `vite.config.ts`

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

### 5.2 Docker Configuration
**File**: `Dockerfile.frontend-react`

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend-react/package*.json ./
RUN npm ci
COPY frontend-react/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 5.3 Update docker-compose.yml
```yaml
services:
  frontend-react:
    build:
      context: .
      dockerfile: Dockerfile.frontend-react
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
```

---

## Phase 6: Migration Strategy

### Option A: Parallel Development (Recommended)
1. Keep existing Streamlit frontend running
2. Develop React frontend in parallel
3. Test both frontends against same backend
4. Switch when React frontend reaches feature parity
5. Deprecate Streamlit frontend

### Option B: Incremental Migration
1. Start with landing page in React
2. Migrate design flow
3. Migrate results display
4. Migrate code editor
5. Remove Streamlit when complete

---

## Implementation Timeline

### Week 1: Setup & Core Infrastructure
- [ ] Create React + Vite project
- [ ] Install dependencies
- [ ] Setup Tailwind CSS + shadcn/ui
- [ ] Create API service layer
- [ ] Setup React Query

### Week 2: Design Flow
- [ ] Build design form with validation
- [ ] Implement progress tracking
- [ ] Add real-time updates
- [ ] Test against backend API

### Week 3: Results Display
- [ ] Architecture visualization
- [ ] Metrics dashboard
- [ ] Reflection feedback display
- [ ] Version comparison

### Week 4: Code Generation
- [ ] Code generation panel
- [ ] Monaco editor integration
- [ ] File tree navigation
- [ ] Download functionality

### Week 5: Polish & Testing
- [ ] Responsive design
- [ ] Error handling
- [ ] Loading states
- [ ] E2E testing
- [ ] Performance optimization

### Week 6: Deployment
- [ ] Docker configuration
- [ ] CI/CD pipeline
- [ ] Production deployment
- [ ] Documentation

---

## Benefits of React + Vite

### Performance
- ⚡ Instant HMR (Hot Module Replacement)
- 📦 Optimized production builds
- 🚀 Fast page loads with code splitting

### Developer Experience
- 💪 TypeScript for type safety
- 🎨 Tailwind CSS for rapid styling
- 🧩 Component reusability
- 🔧 Better debugging tools

### User Experience
- 🎯 No page reloads
- ⚡ Instant interactions
- 🎨 Rich animations
- 📱 Responsive design
- ♿ Better accessibility

### Maintainability
- 📝 Clear component structure
- 🧪 Easy to test
- 📚 Better documentation
- 🔄 Easier to extend

---

## Next Steps

1. **Approve Migration Plan**: Review and approve this plan
2. **Setup Development Environment**: Create React + Vite project
3. **Start with MVP**: Build core design flow first
4. **Iterate**: Add features incrementally
5. **Test**: Ensure feature parity with Streamlit
6. **Deploy**: Switch to React frontend

Would you like me to:
1. Start implementing the React frontend?
2. Create a minimal MVP first?
3. Focus on specific components?
4. Provide more detailed code examples?