import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { designAPI } from '@/services/api'
import type { DesignRequest } from '@/types/api'

export function Design() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [demoLoading, setDemoLoading] = useState(false)
  
  const [formData, setFormData] = useState<DesignRequest>({
    business_goal: '',
    domain: 'healthcare',
    modalities: ['text'],
    constraints: {
      budget: 50000,
      latency_target_ms: 1000,
      risk_tolerance: 'medium',
      compliance_level: 'medium',
      expected_users: 1000,
    },
    max_iterations: 3,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await designAPI.startDesign(formData)
      // Navigate to results page with the run_id
      navigate(`/results?run_id=${response.data.run_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start design')
    } finally {
      setLoading(false)
    }
  }

  const handleDemoClick = async (domain: string) => {
    setDemoLoading(true)
    setError(null)

    try {
      const response = await designAPI.startDemoDesign(domain)
      // Navigate to results page with the demo run_id
      navigate(`/results?run_id=${response.data.run_id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start demo')
    } finally {
      setDemoLoading(false)
    }
  }

  const domains: Array<{ value: DesignRequest['domain']; label: string }> = [
    { value: 'healthcare', label: 'Healthcare' },
    { value: 'finance', label: 'Finance' },
    { value: 'ecommerce', label: 'E-Commerce' },
    { value: 'education', label: 'Education' },
    { value: 'legal', label: 'Legal' },
    { value: 'general', label: 'General' },
  ]

  const modalityOptions: Array<{ value: DesignRequest['modalities'][number]; label: string }> = [
    { value: 'text', label: 'Text' },
    { value: 'vision', label: 'Vision' },
    { value: 'multimodal', label: 'Multimodal' },
    { value: 'tabular', label: 'Tabular' },
  ]

  const toggleModality = (modality: DesignRequest['modalities'][number]) => {
    setFormData(prev => ({
      ...prev,
      modalities: prev.modalities.includes(modality)
        ? prev.modalities.filter(m => m !== modality)
        : [...prev.modalities, modality],
    }))
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-2">Design AI Pipeline</h1>
        <p className="text-slate-600 dark:text-slate-400">
          Define your requirements and let MetaMind generate an optimized architecture
        </p>
      </div>

      {/* Demo Mode Section */}
      <Card className="border-2 border-blue-200 dark:border-blue-800 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Badge variant="secondary" className="bg-blue-600 text-white">✨ Demo Mode</Badge>
            <CardTitle className="text-xl">Try Instant Results</CardTitle>
          </div>
          <CardDescription className="text-slate-700 dark:text-slate-300">
            Experience MetaMind with pre-cached scenarios - get results instantly without waiting for AI processing
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            {/* Healthcare Demo */}
            <Card className="border-2 hover:border-blue-400 transition-colors cursor-pointer">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  🏥 Healthcare
                </CardTitle>
                <CardDescription>Patient Monitoring System</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  AI-powered real-time patient vital signs monitoring with anomaly detection
                </p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="outline" className="text-xs">Real-time</Badge>
                  <Badge variant="outline" className="text-xs">HIPAA Compliant</Badge>
                  <Badge variant="outline" className="text-xs">Alert System</Badge>
                </div>
                <Button
                  onClick={() => handleDemoClick('healthcare')}
                  disabled={demoLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {demoLoading ? 'Loading...' : '⚡ Try Healthcare Demo'}
                </Button>
              </CardContent>
            </Card>

            {/* E-commerce Demo */}
            <Card className="border-2 hover:border-blue-400 transition-colors cursor-pointer">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  🛒 E-Commerce
                </CardTitle>
                <CardDescription>Product Recommendation Engine</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  Personalized product recommendations using collaborative filtering and vision AI
                </p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="outline" className="text-xs">Sub-200ms</Badge>
                  <Badge variant="outline" className="text-xs">Multi-modal</Badge>
                  <Badge variant="outline" className="text-xs">A/B Testing</Badge>
                </div>
                <Button
                  onClick={() => handleDemoClick('ecommerce')}
                  disabled={demoLoading}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {demoLoading ? 'Loading...' : '⚡ Try E-Commerce Demo'}
                </Button>
              </CardContent>
            </Card>
          </div>
          
          <div className="text-center pt-2">
            <p className="text-sm text-slate-600 dark:text-slate-400">
              💡 Demo results are pre-cached and appear instantly - perfect for presentations and testing the UI
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Divider */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-background px-2 text-muted-foreground">
            Or create your own custom design
          </span>
        </div>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Business Goal */}
        <Card>
          <CardHeader>
            <CardTitle>Business Goal</CardTitle>
            <CardDescription>
              Describe what you want your AI pipeline to accomplish
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Textarea
              value={formData.business_goal}
              onChange={(e) => setFormData({ ...formData, business_goal: e.target.value })}
              placeholder="Example: Build a patient diagnosis system that analyzes medical records, lab results, and imaging data to provide diagnostic recommendations with confidence scores..."
              rows={6}
              required
            />
          </CardContent>
        </Card>

        {/* Domain Selection */}
        <Card>
          <CardHeader>
            <CardTitle>Domain</CardTitle>
            <CardDescription>
              Select the primary domain for your AI pipeline
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Select
              value={formData.domain}
              onChange={(e) => setFormData({ ...formData, domain: e.target.value as DesignRequest['domain'] })}
              required
            >
              {domains.map((domain) => (
                <option key={domain.value} value={domain.value}>
                  {domain.label}
                </option>
              ))}
            </Select>
          </CardContent>
        </Card>

        {/* Modalities */}
        <Card>
          <CardHeader>
            <CardTitle>Data Modalities</CardTitle>
            <CardDescription>
              Select the types of data your pipeline will process
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {modalityOptions.map((option) => (
                <Badge
                  key={option.value}
                  variant={
                    formData.modalities.includes(option.value)
                      ? 'default'
                      : 'outline'
                  }
                  className="cursor-pointer"
                  onClick={() => toggleModality(option.value)}
                >
                  {option.label}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Constraints */}
        <Card>
          <CardHeader>
            <CardTitle>Constraints</CardTitle>
            <CardDescription>
              Define budget, latency, and other requirements
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Budget */}
            <div className="space-y-2">
              <Label htmlFor="budget">Budget (USD)</Label>
              <Input
                id="budget"
                type="number"
                value={formData.constraints.budget}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    constraints: { ...formData.constraints, budget: parseInt(e.target.value) || 0 },
                  })
                }
                min="0"
                required
              />
            </div>

            {/* Latency */}
            <div className="space-y-2">
              <Label htmlFor="latency">Latency Target (ms)</Label>
              <Input
                id="latency"
                type="number"
                value={formData.constraints.latency_target_ms}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    constraints: { ...formData.constraints, latency_target_ms: parseInt(e.target.value) || 0 },
                  })
                }
                min="0"
                required
              />
            </div>

            {/* Expected Users */}
            <div className="space-y-2">
              <Label htmlFor="users">Expected Users</Label>
              <Input
                id="users"
                type="number"
                value={formData.constraints.expected_users}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    constraints: { ...formData.constraints, expected_users: parseInt(e.target.value) || 0 },
                  })
                }
                min="0"
                required
              />
            </div>

            {/* Risk Tolerance */}
            <div className="space-y-2">
              <Label htmlFor="risk">Risk Tolerance</Label>
              <Select
                id="risk"
                value={formData.constraints.risk_tolerance}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    constraints: { ...formData.constraints, risk_tolerance: e.target.value as 'low' | 'medium' | 'high' },
                  })
                }
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </Select>
            </div>

            {/* Compliance Level */}
            <div className="space-y-2">
              <Label htmlFor="compliance">Compliance Level</Label>
              <Select
                id="compliance"
                value={formData.constraints.compliance_level}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    constraints: { ...formData.constraints, compliance_level: e.target.value as 'low' | 'medium' | 'high' },
                  })
                }
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Max Iterations */}
        <Card>
          <CardHeader>
            <CardTitle>Optimization Settings</CardTitle>
            <CardDescription>
              Configure the iterative refinement process
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Label htmlFor="iterations">Maximum Iterations</Label>
              <Input
                id="iterations"
                type="number"
                value={formData.max_iterations}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    max_iterations: parseInt(e.target.value) || 1,
                  })
                }
                min="1"
                max="10"
              />
              <p className="text-sm text-slate-500">
                Number of refinement cycles (1-10). Higher values may produce better results but take longer.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Submit Button */}
        <div className="flex justify-end gap-4">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/')}
            disabled={loading}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={loading} size="lg">
            {loading ? 'Starting Design...' : 'Start Design Process'}
          </Button>
        </div>
      </form>
    </div>
  )
}

// Made with Bob
