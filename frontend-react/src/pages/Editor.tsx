import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { MonacoCodeEditor } from '@/components/MonacoCodeEditor'
import { designAPI } from '@/services/api'

export function Editor() {
  const [searchParams] = useSearchParams()
  const runId = searchParams.get('run_id')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [projectId, setProjectId] = useState<string | null>(null)
  const [generatedFiles, setGeneratedFiles] = useState<string[]>([])
  const [showFiles, setShowFiles] = useState(false)
  const [selectedFile, setSelectedFile] = useState<string | null>(null)
  const [fileContent, setFileContent] = useState<string>('')
  const [isEditing, setIsEditing] = useState(false)
  const [showEditor, setShowEditor] = useState(false)

  const handleGenerateCode = async () => {
    if (!runId) {
      setError('No run ID provided')
      return
    }

    setLoading(true)
    setError(null)

    try {
      console.log('Generating code for run_id:', runId)
      const response = await designAPI.generateCode(runId, {
        project_name: `metamind-project-${Date.now()}`,
      })
      console.log('Full response:', response)
      console.log('Response data:', response.data)
      console.log('Response data keys:', Object.keys(response.data))
      console.log('Response data stringified:', JSON.stringify(response.data, null, 2))
      
      // Handle different response structures
      const responseData = response.data as any
      
      // Check if code generation was successful
      if (responseData.status !== 'success') {
        console.error('Code generation failed:', responseData)
        setError(responseData.message || 'Code generation failed')
        return
      }
      
      // Store generated files list
      if (responseData.files_generated && Array.isArray(responseData.files_generated)) {
        setGeneratedFiles(responseData.files_generated)
        console.log('Stored generated files:', responseData.files_generated)
      }
      
      // Extract project identifier from download_url or project_path
      let projectId = responseData.project_id || responseData.projectId || responseData.id
      
      // If no direct project_id, extract from download_url
      if (!projectId && responseData.download_url) {
        // Extract the last part of the download URL as project ID
        const urlParts = responseData.download_url.split('/')
        projectId = urlParts[urlParts.length - 1]
        console.log('Extracted project ID from download_url:', projectId)
      }
      
      // If still no project_id, use project_path
      if (!projectId && responseData.project_path) {
        projectId = responseData.project_path.split('/').pop()
        console.log('Extracted project ID from project_path:', projectId)
      }
      
      if (!projectId) {
        console.error('No project ID found in response')
        console.error('Response data:', responseData)
        console.error('Available keys:', Object.keys(responseData))
        setError(`Code generated but no project ID returned. Response keys: ${Object.keys(responseData).join(', ')}`)
        return
      }
      
      setProjectId(projectId)
      console.log('Project ID set:', projectId)
      console.log('Files generated:', responseData.files_generated?.length || 0)
    } catch (err) {
      console.error('Code generation error:', err)
      if (err instanceof Error) {
        setError(err.message)
      } else if (typeof err === 'object' && err !== null && 'response' in err) {
        const axiosError = err as any
        setError(axiosError.response?.data?.detail || 'Failed to generate code')
      } else {
        setError('Failed to generate code')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!runId || !projectId) {
      setError('Missing run ID or project ID')
      return
    }

    setLoading(true)
    setError(null)

    try {
      console.log('Downloading project:', { runId, projectId })
      const response = await designAPI.downloadProject(runId, projectId)
      console.log('Download response received, size:', response.data.size || response.data.length)
      
      const blob = new Blob([response.data], { type: 'application/zip' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${projectId}.zip`
      document.body.appendChild(a)
      a.click()
      
      // Cleanup
      setTimeout(() => {
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }, 100)
      
      console.log('Download initiated successfully')
    } catch (err) {
      console.error('Download error:', err)
      if (err instanceof Error) {
        setError(err.message)
      } else if (typeof err === 'object' && err !== null && 'response' in err) {
        const axiosError = err as any
        setError(axiosError.response?.data?.detail || 'Failed to download project')
      } else {
        setError('Failed to download project')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 p-6">
      <div className="bg-gradient-to-r from-primary/10 to-primary/5 p-6 rounded-lg border border-primary/20">
        <h1 className="text-4xl font-bold mb-2 text-foreground">Code Editor</h1>
        <p className="text-lg text-muted-foreground">
          Generate and edit code from your architecture blueprint
        </p>
        {runId && (
          <p className="text-sm text-muted-foreground mt-2">
            Run ID: <span className="font-mono bg-muted px-2 py-1 rounded">{runId}</span>
          </p>
        )}
      </div>

      {error && (
        <Alert variant="destructive" className="border-2">
          <AlertDescription className="text-base">{error}</AlertDescription>
        </Alert>
      )}

      {!projectId ? (
        <Card className="border-2 shadow-lg">
          <CardHeader className="bg-muted/50">
            <CardTitle className="text-2xl">Generate Code</CardTitle>
            <CardDescription className="text-base">
              Create production-ready code from your architecture design
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <Button
              onClick={handleGenerateCode}
              disabled={loading || !runId}
              size="lg"
              className="text-base px-8 py-6"
            >
              {loading ? '⏳ Generating Code...' : '🚀 Generate Code'}
            </Button>
            {!runId && (
              <p className="text-sm text-destructive mt-2">
                No run ID found. Please start a design first.
              </p>
            )}
          </CardContent>
        </Card>
      ) : (
        <Card className="border-2 shadow-lg border-success/50">
          <CardHeader className="bg-success/10">
            <CardTitle className="text-2xl text-success">✅ Code Generated Successfully</CardTitle>
            <CardDescription className="text-base">
              Project ID: <span className="font-mono bg-muted px-2 py-1 rounded">{projectId}</span>
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4 pt-6">
            <Alert className="bg-success/10 border-success/20">
              <AlertDescription className="text-base">
                Your code has been generated successfully! You can now download the project.
              </AlertDescription>
            </Alert>

            <div className="flex gap-4">
              <Button
                onClick={handleDownload}
                size="lg"
                className="text-base px-6 py-6"
                disabled={loading}
              >
                {loading ? '⏳ Downloading...' : '📥 Download Project'}
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="text-base px-6 py-6"
                onClick={() => setShowFiles(!showFiles)}
              >
                {showFiles ? '🔼 Hide Files' : '👁️ View Files'}
              </Button>
              <Button
                variant="default"
                size="lg"
                className="text-base px-6 py-6"
                onClick={() => setShowEditor(!showEditor)}
              >
                {showEditor ? '📋 Hide Editor' : '✏️ Open Monaco Editor'}
              </Button>
            </div>
            
            {showFiles && generatedFiles.length > 0 && (
              <Card className="mt-4 border-primary/20">
                <CardHeader>
                  <CardTitle className="text-lg">Generated Files ({generatedFiles.length})</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {generatedFiles.map((file, index) => {
                      const fileName = file.split('/').pop() || file
                      const fileExt = fileName.split('.').pop()
                      const getFileIcon = (ext: string | undefined) => {
                        switch (ext) {
                          case 'py': return '🐍'
                          case 'txt': return '📄'
                          case 'md': return '📝'
                          case 'yml':
                          case 'yaml': return '⚙️'
                          case 'env': return '🔐'
                          default: return '📦'
                        }
                      }
                      
                      return (
                        <div
                          key={index}
                          className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg border hover:bg-muted transition-colors"
                        >
                          <span className="text-2xl">{getFileIcon(fileExt)}</span>
                          <div className="flex-1">
                            <p className="font-mono text-sm font-medium text-foreground">
                              {fileName}
                            </p>
                            <p className="text-xs text-muted-foreground font-mono">
                              {file}
                            </p>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </CardContent>
              </Card>
            )}
          </CardContent>
        </Card>
      )}

      {showEditor && generatedFiles.length > 0 && (
        <Card className="overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Monaco Code Editor</CardTitle>
              <CardDescription>
                Interactive code editor with file tree navigation and syntax highlighting
              </CardDescription>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowEditor(false)}
            >
              Close Editor
            </Button>
          </CardHeader>
          <CardContent className="p-0">
            <MonacoCodeEditor
              files={generatedFiles}
              projectId={projectId || 'unknown'}
            />
          </CardContent>
        </Card>
      )}
    </div>
  )
}

// Made with Bob
