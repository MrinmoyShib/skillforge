export const LANGUAGES = {
  python: { 
    name: 'Python 3',
    label: 'Python 3.8+',
    icon: '🐍', 
    color: 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60', 
    badgeClass: 'bg-emerald-950/60 text-emerald-300 border-emerald-800/60',
    monacoId: 'python',
    gradientClass: 'from-emerald-500 to-teal-400',
    accentText: 'text-emerald-400',
    borderHover: 'hover:border-emerald-500/50',
    bgHighlight: 'bg-emerald-950/30',
    filename: 'solution.py',
    placeholder: 'Write your Python 3 solution here...',
    ext: 'py'
  },
  javascript: { 
    name: 'JavaScript',
    label: 'JavaScript (Node.js)',
    icon: '🟨', 
    color: 'bg-amber-950/60 text-amber-300 border-amber-800/60', 
    badgeClass: 'bg-amber-950/60 text-amber-300 border-amber-800/60',
    monacoId: 'javascript',
    gradientClass: 'from-amber-500 to-yellow-400',
    accentText: 'text-amber-400',
    borderHover: 'hover:border-amber-500/50',
    bgHighlight: 'bg-amber-950/30',
    filename: 'solution.js',
    placeholder: 'Write your JavaScript (Node.js) solution here...',
    ext: 'js'
  },
  cpp: { 
    name: 'C++',
    label: 'C++ (GCC 9.2)',
    icon: '⚡', 
    color: 'bg-cyan-950/60 text-cyan-300 border-cyan-800/60', 
    badgeClass: 'bg-cyan-950/60 text-cyan-300 border-cyan-800/60',
    monacoId: 'cpp',
    gradientClass: 'from-cyan-500 to-indigo-400',
    accentText: 'text-cyan-400',
    borderHover: 'hover:border-cyan-500/50',
    bgHighlight: 'bg-cyan-950/30',
    filename: 'solution.cpp',
    placeholder: 'Write your C++ solution here...',
    ext: 'cpp'
  },
};

export function getLanguageInfo(item, prob = null) {
  const raw = (typeof item === 'string' ? item : item?.language?.slug || item?.language || item?.track || item?.category?.slug || item?.slug || '').toLowerCase();
  
  const key = (raw.includes('python') || raw.startsWith('py') || raw.includes('/py-') || raw.includes('py-')) ? 'python' :
              (raw.includes('javascript') || raw.includes('node') || raw.startsWith('js') || raw.includes('/js-') || raw.includes('js-')) ? 'javascript' :
              (raw.includes('cpp')) ? 'cpp' : null;
              
  return LANGUAGES[key] || { 
    name: 'Unknown', 
    label: 'Unknown',
    icon: '📄', 
    color: 'bg-slate-500/20 text-slate-400 border-slate-500/60', 
    badgeClass: 'bg-slate-500/20 text-slate-400 border-slate-500/60',
    monacoId: 'plaintext',
    gradientClass: 'from-slate-500 to-slate-400',
    accentText: 'text-slate-400',
    borderHover: 'hover:border-slate-500/50',
    bgHighlight: 'bg-slate-950/30',
    filename: 'solution.txt',
    placeholder: 'Write your solution here...',
    ext: 'txt'
  };
}
