import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export function Home() {
  const features = [
    {
      title: 'Intelligent Design',
      description: 'AI-powered pipeline architecture generation with domain-specific optimization',
      icon: '🧠',
    },
    {
      title: 'Iterative Refinement',
      description: 'Automatic reflection and improvement cycles for optimal results',
      icon: '🔄',
    },
    {
      title: 'Code Generation',
      description: 'Generate production-ready code from architecture blueprints',
      icon: '⚡',
    },
    {
      title: 'Version Control',
      description: 'Track and compare different design iterations',
      icon: '📊',
    },
  ]

  const techStack = [
    'LangGraph',
    'FastAPI',
    'React',
    'TypeScript',
    'Tailwind CSS',
    'Grok AI',
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-6 py-12">
        <div className="inline-flex items-center justify-center p-2 bg-blue-100 dark:bg-blue-900 rounded-full mb-4">
          <Badge variant="secondary" className="text-sm">
            🚀 Autonomous AI Pipeline Designer
          </Badge>
        </div>
        
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          MetaMind
        </h1>
        
        <p className="text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
          Design, optimize, and generate AI pipelines with autonomous iterative refinement.
          From requirements to production-ready code.
        </p>

        <div className="flex gap-4 justify-center pt-4">
          <Link to="/design">
            <Button size="lg" className="text-lg">
              Start Designing
            </Button>
          </Link>
          <Link to="/results">
            <Button size="lg" variant="outline" className="text-lg">
              View Results
            </Button>
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {features.map((feature, index) => (
          <Card key={index} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center gap-3">
                <span className="text-4xl">{feature.icon}</span>
                <CardTitle>{feature.title}</CardTitle>
              </div>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base">
                {feature.description}
              </CardDescription>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Tech Stack */}
      <Card>
        <CardHeader>
          <CardTitle>Powered By</CardTitle>
          <CardDescription>
            Built with cutting-edge technologies for maximum performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {techStack.map((tech) => (
              <Badge key={tech} variant="secondary" className="text-sm px-3 py-1">
                {tech}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* How It Works */}
      <Card>
        <CardHeader>
          <CardTitle>How It Works</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <h3 className="font-semibold mb-1">Define Requirements</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Specify your domain, constraints, and objectives
                </p>
              </div>
            </div>
            
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-500 text-white flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <h3 className="font-semibold mb-1">AI Generation</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  MetaMind generates optimized architecture with adaptive weights
                </p>
              </div>
            </div>
            
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-pink-500 text-white flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <h3 className="font-semibold mb-1">Iterative Refinement</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Automatic reflection and improvement until optimal design
                </p>
              </div>
            </div>
            
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-500 text-white flex items-center justify-center font-bold">
                4
              </div>
              <div>
                <h3 className="font-semibold mb-1">Code Generation</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Generate production-ready code and download your project
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Made with Bob
