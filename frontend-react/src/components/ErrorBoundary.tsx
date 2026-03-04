import { Component, type ErrorInfo, type ReactNode } from 'react'
import { Alert, AlertDescription, AlertTitle } from './ui/alert'
import { Button } from './ui/button'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-4 bg-slate-50">
          <div className="max-w-2xl w-full">
            <Alert variant="destructive">
              <AlertTitle className="text-xl font-bold mb-2">
                Something went wrong
              </AlertTitle>
              <AlertDescription className="space-y-4">
                <p>The application encountered an error:</p>
                <pre className="bg-slate-900 text-white p-4 rounded overflow-auto text-sm">
                  {this.state.error?.message}
                </pre>
                <pre className="bg-slate-900 text-white p-4 rounded overflow-auto text-xs max-h-40">
                  {this.state.error?.stack}
                </pre>
                <Button
                  onClick={() => window.location.reload()}
                  className="mt-4"
                >
                  Reload Page
                </Button>
              </AlertDescription>
            </Alert>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// Made with Bob
