import { Link } from 'react-router-dom'

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