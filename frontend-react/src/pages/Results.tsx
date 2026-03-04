import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { designAPI } from '@/services/api'
import type { ResultResponse, StatusResponse, ProgressResponse } from '@/types/api'

export function Results() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const runId = searchParams.get('run_id')

  const [status, setStatus] = useState<StatusResponse | null>(null)
  const [progress, setProgress] = useState<ProgressResponse | null>(null)
  const [result, setResult] = useState<ResultResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [polling, setPolling] = useState(true)
  const [activeTab, setActiveTab] = useState('architecture')

  useEffect(() => {
    if (!runId) {
      setError('No run ID provided')
      setPolling(false)
      return
    }

    // If we already have a result, don't poll
    if (result) {
      setPolling(false)
      return
    }

    let intervalId: ReturnType<typeof setInterval> | null = null
    let isActive = true

    const pollStatus = async () => {
      // Don't poll if component unmounted or result already fetched
      if (!isActive || result) {
        return
      }

      try {
        const statusRes = await designAPI.getStatus(runId)
        if (!isActive) return
        setStatus(statusRes.data)

        const progressRes = await designAPI.getProgress(runId)
        if (!isActive) return
        setProgress(progressRes.data)

        if (statusRes.data.status === 'completed') {
          const resultRes = await designAPI.getResult(runId)
          if (!isActive) return
          setResult(resultRes.data)
          setPolling(false)
          // Clear interval immediately
          if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
          }
        } else if (statusRes.data.status === 'failed') {
          if (!isActive) return
          setError('Design process failed')
          setPolling(false)
          // Clear interval immediately
          if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
          }
        }
      } catch (err) {
        if (!isActive) return
        setError(err instanceof Error ? err.message : 'Failed to fetch status')
        setPolling(false)
        // Clear interval on error
        if (intervalId) {
          clearInterval(intervalId)
          intervalId = null
        }
      }
    }

    // Initial poll
    pollStatus()
    
    // Set up interval only if still active
    intervalId = setInterval(() => {
      if (isActive && !result) {
        pollStatus()
      } else if (intervalId) {
        clearInterval(intervalId)
        intervalId = null
      }
    }, 2000)

    // Cleanup function
    return () => {
      isActive = false
      if (intervalId) {
        clearInterval(intervalId)
        intervalId = null
      }
    }
  }, [runId]) // Only depend on runId, not result

  if (!runId) {
    return (
      <div className="max-w-4xl mx-auto">
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>No run ID provided. Please start a new design.</AlertDescription>
        </Alert>
        <Button onClick={() => navigate('/design')} className="mt-4">
          Start New Design
        </Button>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <Alert variant="destructive">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button onClick={() => navigate('/design')} className="mt-4">
          Start New Design
        </Button>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'failed':
        return 'destructive'
      case 'processing':
        return 'default'
      default:
        return 'secondary'
    }
  }

  const progressPercentage = status
    ? (status.current_iteration / status.max_iterations) * 100
    : 0

  return (
    <div className="max-w-6xl mx-auto space-y-8 p-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-gradient-to-r from-primary/10 to-primary/5 p-6 rounded-lg border border-primary/20">
        <div>
          <h1 className="text-4xl font-bold mb-2 text-foreground">Design Results</h1>
          <p className="text-muted-foreground font-medium">Run ID: <span className="font-mono text-sm bg-muted px-2 py-1 rounded">{runId}</span></p>
        </div>
        <Badge variant={getStatusColor(status?.status || 'starting')} className="text-base px-4 py-2">
          {status?.status || 'Starting'}
        </Badge>
      </div>

      {/* Progress Card */}
      {polling && (
        <Card className="border-2 shadow-lg">
          <CardHeader className="bg-muted/50">
            <CardTitle className="text-2xl">Design Progress</CardTitle>
            <CardDescription className="text-base">
              Iteration {status?.current_iteration || 0} of {status?.max_iterations || 3}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6 pt-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm font-medium">
                <span>Progress</span>
                <span className="text-primary">{progressPercentage.toFixed(0)}%</span>
              </div>
              <Progress value={progressPercentage} max={100} className="h-3" />
            </div>
            
            {progress && (
              <div className="space-y-4">
                <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-foreground">Current Stage:</span>
                    <Badge variant="outline" className="font-mono">
                      {progress.progress.current_stage}
                    </Badge>
                  </div>
                  <p className="text-sm text-foreground leading-relaxed">
                    {progress.progress.current_message}
                  </p>
                </div>
                
                {progress.progress.stages.length > 0 && (
                  <div className="space-y-3">
                    <p className="font-semibold text-foreground">Completed Stages:</p>
                    <div className="space-y-2">
                      {progress.progress.stages.map((stage, index) => (
                        <div key={index} className="flex items-start gap-3 p-3 bg-success/5 border border-success/20 rounded-lg">
                          <Badge variant="outline" className="text-xs shrink-0 bg-success/10">
                            {new Date(stage.timestamp).toLocaleTimeString()}
                          </Badge>
                          <span className="text-sm text-foreground leading-relaxed">
                            <span className="font-semibold">{stage.stage}:</span> {stage.message}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Results */}
      {result && (
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="architecture">Architecture</TabsTrigger>
            <TabsTrigger value="metrics">Metrics</TabsTrigger>
            <TabsTrigger value="reflection">Reflection</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          {/* Architecture Tab */}
          <TabsContent value="architecture" className="space-y-6">
            <Card className="border-2 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-primary/10 to-primary/5 border-b">
                <CardTitle className="text-2xl">{result.selected_architecture.name}</CardTitle>
                <CardDescription className="text-base flex gap-4 mt-2">
                  <span className="bg-muted px-3 py-1 rounded-full">Template: <strong>{result.selected_architecture.template}</strong></span>
                  <span className="bg-muted px-3 py-1 rounded-full">Topology: <strong>{result.selected_architecture.topology}</strong></span>
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <div className="space-y-6">
                  <div>
                    <h3 className="text-xl font-semibold mb-4 text-foreground">Architecture Modules</h3>
                    <div className="grid gap-4">
                      {result.selected_architecture.modules.map((module, index) => (
                        <div
                          key={index}
                          className="p-4 border-2 rounded-lg bg-card hover:shadow-md transition-shadow"
                        >
                          <div className="flex items-center justify-between mb-3">
                            <span className="font-semibold text-lg text-foreground">{module.component}</span>
                            <Badge variant="outline" className="text-sm">{module.layer}</Badge>
                          </div>
                          <pre className="text-xs text-foreground bg-muted p-3 rounded overflow-x-auto border">
                            {JSON.stringify(module.config, null, 2)}
                          </pre>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex gap-4 pt-6 border-t">
                    <Button
                      onClick={() => navigate(`/editor?run_id=${runId}`)}
                      size="lg"
                      className="text-base px-6 py-6"
                    >
                      🚀 Generate Code
                    </Button>
                    <Button variant="outline" size="lg" className="text-base px-6 py-6">
                      📥 Export Blueprint
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Metrics Tab */}
          <TabsContent value="metrics" className="space-y-6">
            <Card className="border-2 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-success/10 to-success/5 border-b">
                <CardTitle className="text-2xl">Performance Metrics</CardTitle>
                <CardDescription className="text-base mt-2">
                  Overall Score: <span className="text-2xl font-bold text-success">{result.score.toFixed(2)}</span>
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {Object.entries(result.metrics).map(([key, value]) => (
                    <div key={key} className="p-5 border-2 rounded-lg bg-card hover:shadow-md transition-shadow">
                      <div className="text-sm font-semibold text-muted-foreground mb-2 uppercase tracking-wide">
                        {key.replace(/_/g, ' ')}
                      </div>
                      <div className="text-3xl font-bold text-foreground mb-3">
                        {typeof value === 'number' ? value.toFixed(2) : value}
                      </div>
                      <Progress value={typeof value === 'number' ? value : 0} max={100} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Reflection Tab */}
          <TabsContent value="reflection" className="space-y-6">
            <Card className="border-2 shadow-lg">
              <CardHeader className="bg-gradient-to-r from-primary/10 to-primary/5 border-b">
                <CardTitle className="text-2xl">AI Reflection & Analysis</CardTitle>
                <CardDescription className="text-base mt-2">
                  Confidence Level: <span className="text-xl font-bold text-primary">{(result.reflection.confidence * 100).toFixed(1)}%</span>
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6 pt-6">
                {result.reflection.strengths && result.reflection.strengths.length > 0 && (
                  <div className="p-5 bg-success/5 border-2 border-success/20 rounded-lg">
                    <h3 className="text-xl font-bold mb-4 text-success flex items-center gap-2">
                      ✓ Strengths
                    </h3>
                    <ul className="space-y-3">
                      {result.reflection.strengths.map((strength, index) => (
                        <li key={index} className="flex items-start gap-3">
                          <span className="text-success mt-1">•</span>
                          <span className="text-base text-foreground leading-relaxed">{strength}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {result.reflection.weaknesses && result.reflection.weaknesses.length > 0 && (
                  <div className="p-5 bg-warning/5 border-2 border-warning/20 rounded-lg">
                    <h3 className="text-xl font-bold mb-4 text-warning flex items-center gap-2">
                      ⚠ Weaknesses
                    </h3>
                    <ul className="space-y-3">
                      {result.reflection.weaknesses.map((weakness, index) => (
                        <li key={index} className="flex items-start gap-3">
                          <span className="text-warning mt-1">•</span>
                          <span className="text-base text-foreground leading-relaxed">{weakness}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {result.reflection.improvement_suggestions && result.reflection.improvement_suggestions.length > 0 && (
                  <div className="p-5 bg-primary/5 border-2 border-primary/20 rounded-lg">
                    <h3 className="text-xl font-bold mb-4 text-primary flex items-center gap-2">
                      💡 Improvement Suggestions
                    </h3>
                    <ul className="space-y-3">
                      {result.reflection.improvement_suggestions.map((suggestion, index) => (
                        <li key={index} className="flex items-start gap-3">
                          <span className="text-primary mt-1">•</span>
                          <span className="text-base text-foreground leading-relaxed">{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {(!result.reflection.strengths || result.reflection.strengths.length === 0) &&
                 (!result.reflection.weaknesses || result.reflection.weaknesses.length === 0) &&
                 (!result.reflection.improvement_suggestions || result.reflection.improvement_suggestions.length === 0) && (
                  <div className="text-center py-12 text-muted-foreground">
                    <p className="text-lg">No reflection data available</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Reports Tab */}
          <TabsContent value="reports" className="space-y-4">
            {result.executive_report && (
              <Card>
                <CardHeader>
                  <CardTitle>Executive Report</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose dark:prose-invert max-w-none">
                    <pre className="whitespace-pre-wrap text-sm">
                      {result.executive_report}
                    </pre>
                  </div>
                </CardContent>
              </Card>
            )}

            {result.technical_specification && (
              <Card>
                <CardHeader>
                  <CardTitle>Technical Specification</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose dark:prose-invert max-w-none">
                    <pre className="whitespace-pre-wrap text-sm">
                      {result.technical_specification}
                    </pre>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      )}
    </div>
  )
}

// Made with Bob
