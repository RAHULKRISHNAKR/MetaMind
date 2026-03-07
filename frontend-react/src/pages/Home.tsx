/*import { Link } from 'react-router-dom'
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
      {/* Hero Section }
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

      {/* Features Grid }
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

      {/* Tech Stack }
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

      {/* How It Works }
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
}*/


import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export function Home() {
  const techStack = [
    'LangGraph',
    'FastAPI',
    'React',
    'TypeScript',
    'Tailwind CSS',
    'Grok AI',
  ]

  const steps = [
    {
      number: '01',
      title: 'Define Requirements',
      description: 'Specify your domain, constraints, and objectives',
      color: 'from-blue-500 to-blue-600',
      accent: 'blue',
    },
    {
      number: '02',
      title: 'AI Generation',
      description: 'MetaMind generates optimized architecture with adaptive weights',
      color: 'from-purple-500 to-purple-600',
      accent: 'purple',
    },
    {
      number: '03',
      title: 'Iterative Refinement',
      description: 'Automatic reflection and improvement until optimal design',
      color: 'from-pink-500 to-pink-600',
      accent: 'pink',
    },
    {
      number: '04',
      title: 'Code Generation',
      description: 'Generate production-ready code and download your project',
      color: 'from-green-500 to-green-600',
      accent: 'green',
    },
  ]

  return (
    <div
      className="min-h-screen bg-white dark:bg-slate-950"
      style={{ fontFamily: "'DM Sans', 'Helvetica Neue', sans-serif" }}
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

        .hero-title {
          font-family: 'DM Serif Display', Georgia, serif;
          font-size: clamp(3.5rem, 10vw, 7rem);
          line-height: 0.95;
          letter-spacing: -0.03em;
          background: linear-gradient(135deg, #2563eb 0%, #9333ea 50%, #ec4899 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .fade-up {
          animation: fadeUp 0.7s ease forwards;
          opacity: 0;
        }
        .fade-up-1 { animation-delay: 0.1s; }
        .fade-up-2 { animation-delay: 0.25s; }
        .fade-up-3 { animation-delay: 0.4s; }
        .fade-up-4 { animation-delay: 0.55s; }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(20px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        .step-card {
          position: relative;
          overflow: hidden;
          transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .step-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 20px 40px -12px rgba(0,0,0,0.12);
        }
        .step-card::before {
          content: '';
          position: absolute;
          inset: 0;
          opacity: 0;
          transition: opacity 0.3s;
        }
        .step-card:hover::before { opacity: 1; }

        .step-number {
          font-family: 'DM Serif Display', Georgia, serif;
          font-size: 4rem;
          line-height: 1;
          letter-spacing: -0.04em;
          opacity: 0.08;
          position: absolute;
          top: 1rem;
          right: 1.25rem;
          pointer-events: none;
        }

        .tech-badge {
          transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .tech-badge:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }

        .divider-line {
          height: 1px;
          background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        }
        .dark .divider-line {
          background: linear-gradient(90deg, transparent, #1e293b, transparent);
        }

        .pill-badge {
          background: linear-gradient(135deg, rgba(37,99,235,0.08), rgba(147,51,234,0.08));
          border: 1px solid rgba(147,51,234,0.15);
          color: #7c3aed;
          font-size: 0.75rem;
          font-weight: 500;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          padding: 0.35rem 1rem;
          border-radius: 999px;
        }
        .dark .pill-badge {
          color: #a78bfa;
          border-color: rgba(167,139,250,0.2);
          background: rgba(167,139,250,0.08);
        }

        .cta-primary {
          background: linear-gradient(135deg, #2563eb, #9333ea);
          border: none;
          color: white;
          font-weight: 500;
          letter-spacing: 0.01em;
          padding: 0.75rem 2rem;
          border-radius: 10px;
          transition: opacity 0.2s, transform 0.2s;
        }
        .cta-primary:hover {
          opacity: 0.9;
          transform: translateY(-1px);
        }

        .cta-secondary {
          background: transparent;
          border: 1.5px solid #e2e8f0;
          font-weight: 500;
          letter-spacing: 0.01em;
          padding: 0.75rem 2rem;
          border-radius: 10px;
          transition: border-color 0.2s, background 0.2s, transform 0.2s;
        }
        .cta-secondary:hover {
          border-color: #9333ea;
          background: rgba(147,51,234,0.04);
          transform: translateY(-1px);
        }
        .dark .cta-secondary {
          border-color: #334155;
        }
        .dark .cta-secondary:hover {
          border-color: #a78bfa;
          background: rgba(167,139,250,0.06);
        }
      `}</style>

      <div className="max-w-3xl mx-auto px-6 py-20 space-y-24">

        {/* Hero */}
        <section className="space-y-8">
          <div className="fade-up fade-up-1">
            <span className="pill-badge">Autonomous AI Pipeline Designer</span>
          </div>

          <h1 className="hero-title fade-up fade-up-2">
            Meta<br />Mind
          </h1>

          <p
            className="fade-up fade-up-3 text-lg text-slate-500 dark:text-slate-400 max-w-md leading-relaxed"
            style={{ fontWeight: 300 }}
          >
            Design, optimize, and generate AI pipelines with autonomous iterative refinement —
            from requirements to production-ready code.
          </p>

          <div className="flex gap-3 fade-up fade-up-4">
            <Link to="/design">
              <button className="cta-primary">Start Designing</button>
            </Link>
            <Link to="/results">
              <button className="cta-secondary">View Results</button>
            </Link>
          </div>
        </section>

        <div className="divider-line" />

        {/* How It Works */}
        <section className="space-y-10">
          <div className="space-y-1">
            <p className="text-xs font-medium tracking-widest text-slate-400 uppercase">Process</p>
            <h2
              className="text-2xl text-slate-900 dark:text-slate-100"
              style={{ fontFamily: "'DM Serif Display', Georgia, serif", fontWeight: 400 }}
            >
              How It Works
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {steps.map((step, i) => (
              <div
                key={i}
                className="step-card rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
              >
                <span className={`step-number bg-gradient-to-br ${step.color} bg-clip-text`}
                  style={{ WebkitTextFillColor: 'transparent' }}>
                  {step.number}
                </span>
                <div className="relative space-y-2 pr-12">
                  <div
                    className={`inline-block w-1 h-5 rounded-full bg-gradient-to-b ${step.color} mb-3`}
                  />
                  <h3 className="font-semibold text-slate-900 dark:text-slate-100 text-[0.95rem]">
                    {step.title}
                  </h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed" style={{ fontWeight: 300 }}>
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="divider-line" />

        {/* Powered By */}
        <section className="space-y-8 pb-8">
          <div className="space-y-1">
            <p className="text-xs font-medium tracking-widest text-slate-400 uppercase">Stack</p>
            <h2
              className="text-2xl text-slate-900 dark:text-slate-100"
              style={{ fontFamily: "'DM Serif Display', Georgia, serif", fontWeight: 400 }}
            >
              Powered By
            </h2>
          </div>

          <div className="flex flex-wrap gap-2">
            {techStack.map((tech) => (
              <span
                key={tech}
                className="tech-badge inline-block text-sm px-4 py-2 rounded-xl
                           bg-slate-50 dark:bg-slate-900
                           border border-slate-100 dark:border-slate-800
                           text-slate-700 dark:text-slate-300
                           font-medium"
              >
                {tech}
              </span>
            ))}
          </div>
        </section>

      </div>
    </div>
  )
}