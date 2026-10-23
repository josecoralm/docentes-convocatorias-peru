import React, { useState, useEffect, useMemo } from 'react';
import { 
  Search, 
  GraduationCap, 
  Building2, 
  MapPin, 
  Calendar, 
  ExternalLink, 
  Filter, 
  RefreshCw, 
  CheckCircle2, 
  AlertCircle, 
  Sparkles, 
  Briefcase, 
  Globe, 
  Clock, 
  Bookmark, 
  Share2, 
  FileText, 
  X,
  ChevronRight,
  ShieldCheck,
  Award,
  BookOpen,
  School,
  Check
} from 'lucide-react';
import { Convocatoria, PlatformStats, UniversidadDirectorio } from './types';

export default function App() {
  const [convocatorias, setConvocatorias] = useState<Convocatoria[]>([]);
  const [universidadesDirectorio, setUniversidadesDirectorio] = useState<UniversidadDirectorio[]>([]);
  const [stats, setStats] = useState<PlatformStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [syncing, setSyncing] = useState<boolean>(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  // Marcador de postulaciones persistente en localStorage
  interface PostulacionInfo {
    id?: string;
    fecha: string;
    nota?: string;
    titulo?: string;
    institucion?: string;
    enlace?: string;
  }
  const [postuladas, setPostuladas] = useState<Record<string, PostulacionInfo>>(() => {
    try {
      const saved = localStorage.getItem('docentes_postulaciones');
      return saved ? JSON.parse(saved) : {};
    } catch (e) {
      return {};
    }
  });

  const togglePostulacion = (id: string, conv?: Convocatoria, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    setPostuladas(prev => {
      const updated = { ...prev };
      if (updated[id]) {
        delete updated[id];
      } else {
        const c = conv || convocatorias.find(item => item.id === id);
        updated[id] = {
          id: id,
          fecha: new Date().toLocaleDateString('es-PE', { day: '2-digit', month: '2-digit', year: 'numeric' }),
          titulo: c?.titulo,
          institucion: c?.institucion,
          enlace: c?.enlace_postulacion
        };
      }
      localStorage.setItem('docentes_postulaciones', JSON.stringify(updated));
      return updated;
    });
  };

  const isConvocatoriaPostulada = (c: Convocatoria) => {
    if (postuladas[c.id]) return true;
    for (const [key, val] of Object.entries(postuladas)) {
      if (key === c.id) return true;
      if (val.titulo && c.titulo && val.titulo.toLowerCase().trim() === c.titulo.toLowerCase().trim()) return true;
      if (val.id && val.id === c.id) return true;
    }
    return false;
  };

  const updateNota = (id: string, nota: string) => {
    setPostuladas(prev => {
      if (!prev[id]) return prev;
      const updated = {
        ...prev,
        [id]: { ...prev[id], nota }
      };
      localStorage.setItem('docentes_postulaciones', JSON.stringify(updated));
      return updated;
    });
  };

  // Filtros
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [activeTab, setActiveTab] = useState<string>('todos'); // 'todos' | 'privadas' | 'publicas' | 'posgrado' | 'virtual' | 'postuladas'
  const [selectedModalidad, setSelectedModalidad] = useState<string>('Todos');
  const [selectedTipo, setSelectedTipo] = useState<string>('Todos');
  const [selectedUniversidad, setSelectedUniversidad] = useState<string>('Todas');

  // Modales
  const [selectedConvocatoria, setSelectedConvocatoria] = useState<Convocatoria | null>(null);
  const [showChecklistModal, setShowChecklistModal] = useState<boolean>(false);
  const [showDirectorioModal, setShowDirectorioModal] = useState<boolean>(false);
  const [searchDirectorio, setSearchDirectorio] = useState<string>('');
  const [filterDirectorioTipo, setFilterDirectorioTipo] = useState<string>('Todos');

  // Cargar datos iniciales
  const fetchData = async () => {
    try {
      setLoading(true);
      const [resConvs, resStats, resDirectorio] = await Promise.all([
        fetch('/api/convocatorias?limit=150'),
        fetch('/api/stats'),
        fetch('/api/universidades-directorio')
      ]);

      if (resConvs.ok) {
        const dataConvs = await resConvs.json();
        setConvocatorias(dataConvs.items || []);
      }
      if (resStats.ok) {
        const dataStats = await resStats.json();
        setStats(dataStats);
      }
      if (resDirectorio.ok) {
        const dataDir = await resDirectorio.json();
        setUniversidadesDirectorio(dataDir.universidades || []);
      }
    } catch (err) {
      console.error("Error al cargar convocatorias:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Sincronizar scrapers en vivo
  const handleSyncNow = async () => {
    try {
      setSyncing(true);
      setSyncMessage("Rastreando portales de empleo y universidades en tiempo real...");
      const res = await fetch('/api/sync/sync-now', { method: 'POST' });
      if (res.ok) {
        const result = await res.json();
        setSyncMessage(`¡Sincronización completada! ${result.new_items_added} nuevas convocatorias añadidas.`);
        await fetchData();
        setTimeout(() => setSyncMessage(null), 5000);
      } else {
        setSyncMessage("La sincronización se inició en segundo plano.");
        setTimeout(() => setSyncMessage(null), 4000);
      }
    } catch (err) {
      console.error("Error al sincronizar:", err);
      setSyncMessage("Error de conexión al sincronizar scrapers.");
      setTimeout(() => setSyncMessage(null), 4000);
    } finally {
      setSyncing(false);
    }
  };

  // Lista única de universidades para el filtro desplegable
  const listaUniversidades = useMemo(() => {
    const unis = new Set<string>();
    convocatorias.forEach(c => {
      if (c.institucion && !c.institucion.includes('Computrabajo') && !c.institucion.includes('Bumeran') && !c.institucion.includes('Talento Perú')) {
        unis.add(c.institucion);
      }
    });
    return Array.from(unis).sort();
  }, [convocatorias]);

  const stripAccents = (str: string) => {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  };

  // Filtrado del Directorio Nacional de Universidades (Modal)
  const filteredDirectorio = useMemo(() => {
    return universidadesDirectorio.filter(u => {
      if (searchDirectorio.trim() !== '') {
        const term = stripAccents(searchDirectorio);
        const text = stripAccents(`${u.nombre} ${u.siglas} ${u.region} ${u.portal_nombre} ${u.niveles}`);
        if (!text.includes(term)) return false;
      }
      if (filterDirectorioTipo !== 'Todos' && u.tipo !== filterDirectorioTipo) {
        return false;
      }
      return true;
    });
  }, [universidadesDirectorio, searchDirectorio, filterDirectorioTipo]);

  // Conteos exactos y consistentes
  const countTotal = convocatorias.length;
  const countPrivadas = useMemo(() => convocatorias.filter(c => c.tipo_institucion === 'Privada').length, [convocatorias]);
  const countPublicas = useMemo(() => convocatorias.filter(c => c.tipo_institucion === 'Pública').length, [convocatorias]);
  const countPosgrado = useMemo(() => convocatorias.filter(c => {
    const text = (c.nivel + ' ' + c.titulo + ' ' + c.tags.join(' ')).toLowerCase();
    return text.includes('posgrado') || text.includes('maestr') || text.includes('doctor');
  }).length, [convocatorias]);
  const countVirtual = useMemo(() => convocatorias.filter(c => {
    const mod = c.modalidad.toLowerCase();
    return mod.includes('virtual') || mod.includes('remoto');
  }).length, [convocatorias]);
  const countPostuladas = useMemo(() => {
    const matched = convocatorias.filter(isConvocatoriaPostulada).length;
    return Math.max(matched, Object.keys(postuladas).length);
  }, [convocatorias, postuladas]);

  const handleOpenPostuladas = () => {
    setActiveTab('postuladas');
    setSelectedUniversidad('Todas');
    setSelectedModalidad('Todos');
    setSelectedTipo('Todos');
    setSearchTerm('');
  };

  // Filtrado de convocatorias
  const filteredConvocatorias = useMemo(() => {
    return convocatorias.filter((item) => {
      // Si estamos en la pestaña de Mis Postulaciones, filtrar por postulación
      if (activeTab === 'postuladas') {
        if (!isConvocatoriaPostulada(item)) return false;
        if (searchTerm.trim() !== '') {
          const term = stripAccents(searchTerm);
          const fullText = stripAccents(`${item.titulo} ${item.institucion} ${item.facultad_o_carrera}`);
          if (!fullText.includes(term)) return false;
        }
        return true;
      }

      // Búsqueda por texto (insensible a tildes y mayúsculas)
      if (searchTerm.trim() !== '') {
        const term = stripAccents(searchTerm);
        const fullText = stripAccents(`${item.titulo} ${item.institucion} ${item.facultad_o_carrera} ${item.ubicacion} ${item.tags.join(' ')} ${item.descripcion}`);
        if (!fullText.includes(term)) return false;
      }

      // Filtros de pestañas
      if (activeTab === 'posgrado') {
        const text = (item.nivel + ' ' + item.titulo + ' ' + item.tags.join(' ')).toLowerCase();
        if (!text.includes('posgrado') && !text.includes('maestr') && !text.includes('doctor')) {
          return false;
        }
      } else if (activeTab === 'publicas') {
        if (item.tipo_institucion !== 'Pública') return false;
      } else if (activeTab === 'privadas') {
        if (item.tipo_institucion !== 'Privada') return false;
      } else if (activeTab === 'virtual') {
        const mod = item.modalidad.toLowerCase();
        if (!mod.includes('virtual') && !mod.includes('remoto')) {
          return false;
        }
      }

      // Filtro desplegable Modalidad
      if (selectedModalidad !== 'Todos') {
        if (!item.modalidad.toLowerCase().includes(selectedModalidad.toLowerCase())) {
          return false;
        }
      }

      // Filtro desplegable Tipo
      if (selectedTipo !== 'Todos') {
        if (item.tipo_institucion !== selectedTipo) {
          return false;
        }
      }

      // Filtro desplegable Universidad
      if (selectedUniversidad !== 'Todas') {
        if (!item.institucion.toLowerCase().includes(selectedUniversidad.toLowerCase())) {
          return false;
        }
      }

      return true;
    });
  }, [convocatorias, searchTerm, activeTab, selectedModalidad, selectedTipo, selectedUniversidad, postuladas]);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      {/* Top Notification Toast */}
      {syncMessage && (
        <div className="fixed top-5 right-5 z-50 bg-indigo-600 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 border border-indigo-400 animate-bounce">
          <Sparkles className="w-5 h-5 text-amber-300" />
          <span className="text-sm font-semibold">{syncMessage}</span>
        </div>
      )}

      {/* Main Navbar */}
      <header className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white ring-2 ring-indigo-400/20">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-bold tracking-tight text-white">Docentes Convocatorias</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 font-semibold border border-indigo-500/20">
                  Perú 🇵🇪
                </span>
              </div>
              <p className="text-xs text-slate-400">Todas las Universidades Públicas, Privadas & Posgrado</p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <button 
              onClick={() => setShowDirectorioModal(true)}
              className="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/30 transition shadow-sm cursor-pointer"
            >
              <School className="w-4 h-4 text-amber-400" />
              <span>Directorio de Universidades</span>
              <span className="bg-amber-400/20 text-amber-200 text-[10px] px-1.5 py-0.5 rounded-full font-bold">
                {universidadesDirectorio.length || 'Todas'}
              </span>
            </button>

            <button 
              onClick={() => setShowChecklistModal(true)}
              className="hidden md:inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
            >
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Checklist SUNEDU</span>
            </button>

            <button 
              onClick={handleSyncNow}
              disabled={syncing}
              className="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${syncing ? 'animate-spin' : ''}`} />
              <span>{syncing ? 'Rastreando...' : 'Sincronizar'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Hero Header */}
      <section className="relative overflow-hidden pt-10 pb-12 bg-gradient-to-b from-slate-900 via-slate-900 to-slate-950 border-b border-slate-800">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(99,102,241,0.15),rgba(255,255,255,0))]"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto mb-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-950/60 border border-indigo-700/40 text-indigo-300 text-xs font-medium mb-4">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              Todas las Universidades del Perú en una Sola Plataforma
            </div>
            <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-white mb-4">
              Convocatorias Docentes Universitarias y de Posgrado
            </h1>
            <p className="text-base text-slate-300 leading-relaxed">
              Encuentra plazas de cátedra en <strong className="text-white">todas las universidades públicas y privadas</strong>: 
              UPN, César Vallejo (UCV), Autónoma, San Marcos (UNMSM), UNI, PUCP, UPC, UTP, Continental, Agraria (UNALM), Villarreal, ESAN y Pacífico.
            </p>
          </div>

          {/* Quick Metrics Bar - Desglose Matemático 100% Consistente y Clickeable */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 max-w-6xl mx-auto mb-4">
            {/* Bloque 1: Suma Total */}
            <button
              onClick={() => setActiveTab('todos')}
              className={`border rounded-xl p-3 text-center transition cursor-pointer flex flex-col justify-between ${
                activeTab === 'todos'
                  ? 'bg-indigo-950/80 border-indigo-400 ring-2 ring-indigo-500/40 shadow-lg'
                  : 'bg-slate-800/60 backdrop-blur border-slate-700/60 hover:border-indigo-500/50'
              }`}
            >
              <div className="text-2xl font-bold text-indigo-400">{countTotal}</div>
              <div className="text-xs text-white font-semibold mt-0.5">Total Convocatorias</div>
              <div className="text-[10px] text-indigo-300/80 mt-1">Suma total vigentes</div>
            </button>

            {/* Bloque 2: Privadas */}
            <button
              onClick={() => setActiveTab('privadas')}
              className={`border rounded-xl p-3 text-center transition cursor-pointer flex flex-col justify-between ${
                activeTab === 'privadas'
                  ? 'bg-purple-950/80 border-purple-400 ring-2 ring-purple-500/40 shadow-lg'
                  : 'bg-slate-800/60 backdrop-blur border-slate-700/60 hover:border-purple-500/50'
              }`}
            >
              <div className="text-2xl font-bold text-purple-400">{countPrivadas}</div>
              <div className="text-xs text-white font-semibold mt-0.5">Univ. Privadas</div>
              <div className="text-[10px] text-purple-300/80 mt-1">UPN, UCV, Autónoma...</div>
            </button>

            {/* Bloque 3: Públicas */}
            <button
              onClick={() => setActiveTab('publicas')}
              className={`border rounded-xl p-3 text-center transition cursor-pointer flex flex-col justify-between ${
                activeTab === 'publicas'
                  ? 'bg-sky-950/80 border-sky-400 ring-2 ring-sky-500/40 shadow-lg'
                  : 'bg-slate-800/60 backdrop-blur border-slate-700/60 hover:border-sky-500/50'
              }`}
            >
              <div className="text-2xl font-bold text-sky-400">{countPublicas}</div>
              <div className="text-xs text-white font-semibold mt-0.5">Concursos Públicos</div>
              <div className="text-[10px] text-sky-300/80 mt-1">San Marcos, UNI, UNFV...</div>
            </button>

            {/* Bloque 4: Posgrado & Maestrías */}
            <button
              onClick={() => setActiveTab('posgrado')}
              className={`border rounded-xl p-3 text-center transition cursor-pointer flex flex-col justify-between ${
                activeTab === 'posgrado'
                  ? 'bg-amber-950/80 border-amber-400 ring-2 ring-amber-500/40 shadow-lg'
                  : 'bg-slate-800/60 backdrop-blur border-slate-700/60 hover:border-amber-500/50'
              }`}
            >
              <div className="text-2xl font-bold text-amber-400">{countPosgrado}</div>
              <div className="text-xs text-white font-semibold mt-0.5">Posgrado & Maestrías</div>
              <div className="text-[10px] text-amber-300/80 mt-1">Plazas de Maestría</div>
            </button>

            {/* Bloque 5: 100% Virtual */}
            <button
              onClick={() => setActiveTab('virtual')}
              className={`border rounded-xl p-3 text-center transition cursor-pointer flex flex-col justify-between ${
                activeTab === 'virtual'
                  ? 'bg-emerald-950/80 border-emerald-400 ring-2 ring-emerald-500/40 shadow-lg'
                  : 'bg-slate-800/60 backdrop-blur border-slate-700/60 hover:border-emerald-500/50'
              }`}
            >
              <div className="text-2xl font-bold text-emerald-400">{countVirtual}</div>
              <div className="text-xs text-white font-semibold mt-0.5">100% Virtual / Remoto</div>
              <div className="text-[10px] text-emerald-300/80 mt-1">Cátedra a distancia</div>
            </button>

            {/* Bloque 6: Mis Postulaciones */}
            <button 
              onClick={handleOpenPostuladas}
              className={`border rounded-xl p-3 text-center transition cursor-pointer flex flex-col justify-between ${
                activeTab === 'postuladas'
                  ? 'bg-emerald-950/80 border-emerald-400 ring-2 ring-emerald-500/40 shadow-lg shadow-emerald-500/10'
                  : 'bg-slate-800/60 backdrop-blur border-slate-700/60 hover:border-emerald-500/50'
              }`}
            >
              <div className="text-2xl font-bold text-emerald-400">{countPostuladas}</div>
              <div className="text-xs text-emerald-300 font-semibold mt-0.5 flex items-center justify-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                Mis Postulaciones
              </div>
              <div className="text-[10px] text-emerald-400/80 mt-1">Tus expedientes</div>
            </button>
          </div>

          {/* Banner explicativo del desglose */}
          <div className="max-w-4xl mx-auto mb-6 p-2 bg-slate-800/40 border border-slate-700/50 rounded-xl text-center text-xs text-slate-300 flex items-center justify-center gap-2">
            <span className="text-amber-400 font-bold">ℹ️ Desglose oficial:</span>
            <span>{countPrivadas} Universidades Privadas + {countPublicas} Concursos Públicos = <strong className="text-white">{countTotal} Convocatorias Vigentes</strong> en total.</span>
          </div>

          {/* Search Box */}
          <div className="max-w-4xl mx-auto">
            <div className="relative flex items-center bg-slate-800/90 rounded-2xl p-2 border border-slate-700 shadow-2xl focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-500/20 transition">
              <Search className="w-5 h-5 text-slate-400 ml-3" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar por universidad (UPN, Vallejo, Autónoma, San Marcos, UNI, PUCP...), asignatura o especialidad..."
                className="w-full bg-transparent px-3 py-2 text-white placeholder-slate-400 text-sm focus:outline-none"
              />
              {searchTerm && (
                <button onClick={() => setSearchTerm('')} className="p-1 text-slate-400 hover:text-white mr-2">
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Navigation Tabs & Secondary Filters */}
      <section className="bg-slate-950 border-b border-slate-800 py-3 sticky top-20 z-30 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-2.5">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
            
            {/* Category Tabs */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 lg:pb-0 custom-scrollbar">
              <button
                onClick={() => setActiveTab('todos')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                  activeTab === 'todos'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                Todas las Convocatorias ({countTotal})
              </button>

              <button
                onClick={() => setActiveTab('privadas')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                  activeTab === 'privadas'
                    ? 'bg-purple-600 text-white shadow-sm'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                Universidades Privadas ({countPrivadas})
              </button>

              <button
                onClick={() => setActiveTab('publicas')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                  activeTab === 'publicas'
                    ? 'bg-sky-600 text-white shadow-sm'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                Concursos Públicos ({countPublicas})
              </button>

              <button
                onClick={() => setActiveTab('posgrado')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition flex items-center gap-1.5 ${
                  activeTab === 'posgrado'
                    ? 'bg-amber-600 text-white shadow-sm'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <Award className="w-3.5 h-3.5 text-amber-300" />
                Posgrado & Maestrías ({countPosgrado})
              </button>

              <button
                onClick={() => setActiveTab('virtual')}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition flex items-center gap-1.5 ${
                  activeTab === 'virtual'
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <Globe className="w-3.5 h-3.5" />
                100% Virtual ({countVirtual})
              </button>

              <button
                onClick={handleOpenPostuladas}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition flex items-center gap-1.5 ${
                  activeTab === 'postuladas'
                    ? 'bg-emerald-600 text-white shadow-sm ring-2 ring-emerald-400/40'
                    : 'bg-slate-900 text-emerald-400 hover:bg-slate-800 border border-emerald-900/50'
                }`}
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Mis Postulaciones ({countPostuladas})</span>
              </button>
            </div>

            {/* Dropdown Filters */}
            <div className="flex flex-wrap items-center gap-2 self-start lg:self-auto">
              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <Building2 className="w-3.5 h-3.5 text-indigo-400" />
                <select
                  value={selectedUniversidad}
                  onChange={(e) => setSelectedUniversidad(e.target.value)}
                  className="bg-slate-900 border border-slate-700 rounded-md text-xs text-white px-2 py-1 focus:outline-none focus:border-indigo-500 max-w-[170px] truncate"
                >
                  <option value="Todas">Todas las Universidades</option>
                  {listaUniversidades.map((uni, i) => (
                    <option key={i} value={uni}>{uni}</option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <Filter className="w-3.5 h-3.5" />
                <select
                  value={selectedModalidad}
                  onChange={(e) => setSelectedModalidad(e.target.value)}
                  className="bg-slate-900 border border-slate-700 rounded-md text-xs text-white px-2 py-1 focus:outline-none focus:border-indigo-500"
                >
                  <option value="Todos">Modalidad: Todas</option>
                  <option value="Presencial">Presencial</option>
                  <option value="Híbrido">Semipresencial / Híbrido</option>
                  <option value="Virtual">100% Virtual</option>
                </select>
              </div>

              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <select
                  value={selectedTipo}
                  onChange={(e) => setSelectedTipo(e.target.value)}
                  className="bg-slate-900 border border-slate-700 rounded-md text-xs text-white px-2 py-1 focus:outline-none focus:border-indigo-500"
                >
                  <option value="Todos">Gestión: Todos</option>
                  <option value="Pública">Pública</option>
                  <option value="Privada">Privada</option>
                </select>
              </div>
            </div>

          </div>

          {/* Quick University Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pt-1 pb-0.5 custom-scrollbar border-t border-slate-850">
            <span className="text-[11px] text-slate-400 font-medium shrink-0 flex items-center gap-1 mr-1">
              <Building2 className="w-3 h-3 text-indigo-400" />
              Filtrar por Universidad:
            </span>
            {[
              { label: 'Todas', value: 'Todas' },
              { label: 'UPN', value: 'Universidad Privada del Norte' },
              { label: 'César Vallejo (UCV)', value: 'César Vallejo' },
              { label: 'Autónoma', value: 'Autónoma' },
              { label: 'San Marcos (UNMSM)', value: 'San Marcos' },
              { label: 'UNI', value: 'Universidad Nacional de Ingeniería' },
              { label: 'PUCP', value: 'PUCP' },
              { label: 'UPC', value: 'UPC' },
              { label: 'UTP', value: 'UTP' },
              { label: 'Continental', value: 'Continental' }
            ].map((chip, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedUniversidad(chip.value)}
                className={`px-2.5 py-0.5 rounded-md text-[11px] font-medium whitespace-nowrap transition cursor-pointer ${
                  selectedUniversidad === chip.value
                    ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                    : 'bg-slate-900 text-slate-300 hover:bg-slate-800 border border-slate-800'
                }`}
              >
                {chip.label}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content Area - Solo Convocatorias Vigentes */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        <div>
          <div className="flex items-center justify-between mb-6">
            <div className="text-sm text-slate-400">
              Mostrando <strong className="text-white font-semibold">{filteredConvocatorias.length}</strong> convocatorias vigentes
            </div>
            <div className="flex items-center gap-2">
              {selectedUniversidad !== 'Todas' && (
                <span className="text-xs text-indigo-300 bg-indigo-950 px-3 py-1 rounded-full border border-indigo-800">
                  Uni: {selectedUniversidad}
                </span>
              )}
              {searchTerm && (
                <div className="text-xs text-indigo-400 bg-indigo-950/60 px-3 py-1 rounded-full border border-indigo-800">
                  Búsqueda: "{searchTerm}"
                </div>
              )}
            </div>
          </div>

          {loading ? (
            <div className="py-20 flex flex-col items-center justify-center text-slate-400">
              <RefreshCw className="w-8 h-8 animate-spin text-indigo-500 mb-3" />
              <p className="text-sm">Cargando convocatorias de universidades del Perú...</p>
            </div>
          ) : filteredConvocatorias.length === 0 ? (
            <div className="py-16 text-center bg-slate-800/40 rounded-2xl border border-slate-800 max-w-lg mx-auto p-8">
              <GraduationCap className="w-12 h-12 text-slate-600 mx-auto mb-3" />
              <h3 className="text-lg font-bold text-white mb-1">No se encontraron convocatorias</h3>
              <p className="text-xs text-slate-400 mb-4">
                Prueba modificando tus términos de búsqueda o los filtros seleccionados.
              </p>
                <button
                  onClick={() => {
                    setSearchTerm('');
                    setActiveTab('todos');
                    setSelectedModalidad('Todos');
                    setSelectedTipo('Todos');
                    setSelectedUniversidad('Todas');
                  }}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition"
                >
                  Restablecer filtros
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {filteredConvocatorias.map((conv) => {
                  const isPosgrado = conv.nivel.toLowerCase().includes('posgrado') || conv.titulo.toLowerCase().includes('maestría') || conv.tags.some(t => t.toLowerCase().includes('maestr') || t.toLowerCase().includes('posgrado'));
                  const isPublica = conv.tipo_institucion === 'Pública';
                  const isPostulado = isConvocatoriaPostulada(conv);
                  const postuladoInfo = postuladas[conv.id] || Object.values(postuladas).find(p => p.titulo && p.titulo.toLowerCase().trim() === conv.titulo.toLowerCase().trim());

                  return (
                    <div
                      key={conv.id}
                      className={`rounded-2xl border shadow-lg hover:shadow-xl transition duration-200 flex flex-col justify-between p-5 group relative ${
                        isPostulado
                          ? 'bg-slate-850/95 border-emerald-500/50 ring-1 ring-emerald-500/30 shadow-emerald-950/20'
                          : 'bg-slate-850/80 hover:bg-slate-800/90 border-slate-800 hover:border-slate-700 hover:shadow-indigo-500/5'
                      }`}
                    >
                      <div>
                        {/* Top Badges & Postulado Marker */}
                        <div className="flex items-start justify-between gap-2 mb-3">
                          <div className="flex flex-wrap gap-1.5 items-center">
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-md uppercase tracking-wider ${
                              isPublica 
                                ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30' 
                                : 'bg-purple-500/10 text-purple-300 border border-purple-500/30'
                            }`}>
                              {conv.tipo_institucion}
                            </span>

                            {isPosgrado && (
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                                <Award className="w-2.5 h-2.5" />
                                Posgrado & Maestría
                              </span>
                            )}

                            <span className="text-[10px] font-medium px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                              {conv.estado}
                            </span>
                          </div>

                          {/* Botón de Marcador Postulado en la Card */}
                          <button
                            onClick={(e) => togglePostulacion(conv.id, conv, e)}
                            className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition flex items-center gap-1.5 border shadow-sm ${
                              isPostulado
                                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50 hover:bg-rose-500/20 hover:text-rose-300 hover:border-rose-500/50'
                                : 'bg-slate-800/90 text-slate-400 border-slate-700 hover:text-emerald-300 hover:border-emerald-500/40'
                            }`}
                            title={isPostulado ? "Hacer clic para desmarcar postulación" : "Marcar como postulado"}
                          >
                            <CheckCircle2 className={`w-3.5 h-3.5 ${isPostulado ? 'text-emerald-400' : 'text-slate-500'}`} />
                            <span>{isPostulado ? 'Postulado ✓' : 'Marcar postulado'}</span>
                          </button>
                        </div>

                        {/* Banner de Estado Postulado si aplica */}
                        {isPostulado && (
                          <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-lg px-2.5 py-1.5 mb-3 text-[11px] text-emerald-300 flex items-center justify-between">
                            <span className="flex items-center gap-1.5 font-semibold">
                              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                              Postulaste el {postuladoInfo?.fecha || 'Recientemente'}
                            </span>
                            {postuladoInfo?.nota && (
                              <span className="text-[10px] text-emerald-300/80 truncate max-w-[140px] italic">
                                "{postuladoInfo.nota}"
                              </span>
                            )}
                          </div>
                        )}

                        {/* Institution Name */}
                        <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-400 mb-1">
                          <Building2 className="w-3.5 h-3.5 shrink-0" />
                          <span className="line-clamp-1">{conv.institucion}</span>
                        </div>

                        {/* Job Title */}
                        <h3 className="text-base font-bold text-white mb-2 leading-snug group-hover:text-indigo-200 transition line-clamp-2">
                          {conv.titulo}
                        </h3>

                        {/* Academic Unit */}
                        <p className="text-xs text-slate-400 mb-3 flex items-center gap-1.5 line-clamp-1">
                          <GraduationCap className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                          <span>{conv.facultad_o_carrera}</span>
                        </p>

                        {/* Details Box */}
                        <div className="bg-slate-900/80 rounded-xl p-3 border border-slate-800/80 space-y-2 mb-4 text-xs">
                          <div className="flex items-center gap-2 text-slate-300">
                            <MapPin className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                            <span className="truncate">{conv.ubicacion}</span>
                          </div>
                          <div className="flex items-center gap-2 text-slate-300">
                            <Globe className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                            <span className="truncate">{conv.modalidad}</span>
                          </div>
                          <div className="flex items-center gap-2 text-slate-300">
                            <Briefcase className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                            <span className="truncate">{conv.tipo_contrato}</span>
                          </div>
                          <div className="flex items-center gap-2 text-slate-300 font-medium">
                            <Clock className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                            <span className="truncate text-amber-300">{conv.fecha_limite}</span>
                          </div>
                        </div>

                        {/* Key Requirements Snippet */}
                        <div className="space-y-1 mb-4">
                          {conv.requisitos.slice(0, 2).map((req, i) => (
                            <div key={i} className="flex items-start gap-1.5 text-[11px] text-slate-400">
                              <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />
                              <span className="line-clamp-1">{req}</span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Actions Bar */}
                      <div className="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
                        <button
                          onClick={() => setSelectedConvocatoria(conv)}
                          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition"
                        >
                          Ficha Completa
                        </button>

                        <a
                          href={conv.enlace_postulacion}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition"
                        >
                          <span>Postular / Bases</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
      </main>

      {/* Modal: Detalle de Convocatoria */}
      {selectedConvocatoria && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar p-6 shadow-2xl relative">
            <button
              onClick={() => setSelectedConvocatoria(null)}
              className="absolute top-5 right-5 p-1 rounded-lg text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 mb-2">
              <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-md uppercase tracking-wider ${
                selectedConvocatoria.tipo_institucion === 'Pública' 
                  ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30' 
                  : 'bg-purple-500/10 text-purple-300 border border-purple-500/30'
              }`}>
                {selectedConvocatoria.tipo_institucion}
              </span>
              <span className="text-[10px] font-medium px-2.5 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                {selectedConvocatoria.estado}
              </span>
            </div>

            <h2 className="text-xl font-bold text-white mb-1">
              {selectedConvocatoria.titulo}
            </h2>
            <div className="text-sm font-semibold text-indigo-400 mb-4 flex items-center gap-1.5">
              <Building2 className="w-4 h-4" />
              <span>{selectedConvocatoria.institucion}</span>
            </div>

            {/* Marcador y Seguimiento de Postulación en el Modal */}
            {(() => {
              const isSelectedPostulado = isConvocatoriaPostulada(selectedConvocatoria);
              const postuladoInfo = postuladas[selectedConvocatoria.id] || Object.values(postuladas).find(p => p.titulo && p.titulo.toLowerCase().trim() === selectedConvocatoria.titulo.toLowerCase().trim());

              return (
                <div className={`p-4 rounded-xl border mb-5 transition ${
                  isSelectedPostulado
                    ? 'bg-emerald-950/40 border-emerald-500/50 shadow-inner'
                    : 'bg-slate-800/50 border-slate-700/60'
                }`}>
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${
                        isSelectedPostulado
                          ? 'bg-emerald-500/20 text-emerald-400 ring-2 ring-emerald-500/40'
                          : 'bg-slate-800 text-slate-400'
                      }`}>
                        <CheckCircle2 className="w-5 h-5" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-white">
                          {isSelectedPostulado
                            ? '¡Ya has postulado a esta convocatoria!'
                            : '¿Ya enviaste tu expediente a esta convocatoria?'}
                        </h4>
                        <p className="text-xs text-slate-400">
                          {isSelectedPostulado
                            ? `Registrado en tu historial el ${postuladoInfo?.fecha || 'Recientemente'}.`
                            : 'Márcala para llevar un control estricto de tus postulaciones y expedientes en trámite.'}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => togglePostulacion(selectedConvocatoria.id, selectedConvocatoria)}
                      className={`px-4 py-2 rounded-xl text-xs font-bold transition shrink-0 flex items-center justify-center gap-2 ${
                        isSelectedPostulado
                          ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-rose-500/30'
                          : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-md shadow-emerald-600/30'
                      }`}
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span>{isSelectedPostulado ? 'Desmarcar postulación' : 'Marcar como Postulado'}</span>
                    </button>
                  </div>

                  {isSelectedPostulado && (
                    <div className="mt-3 pt-3 border-t border-emerald-800/40">
                      <label className="text-[11px] font-semibold text-emerald-300 mb-1.5 block">
                        Notas de seguimiento personal (opcional):
                      </label>
                      <input
                        type="text"
                        value={postuladas[selectedConvocatoria.id]?.nota || postuladoInfo?.nota || ''}
                        onChange={(e) => updateNota(selectedConvocatoria.id, e.target.value)}
                        placeholder="Ej: Expediente foliado enviado por mesa de partes virtual / N° trámite #1420 / Entrevista pendiente..."
                        className="w-full bg-slate-900 border border-emerald-700/50 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-400"
                      />
                    </div>
                  )}
                </div>
              );
            })()}

            {/* Quick Grid Specs */}
            <div className="grid grid-cols-2 gap-3 bg-slate-950/70 p-4 rounded-xl border border-slate-800 text-xs mb-5">
              <div>
                <span className="text-slate-500 block mb-0.5">Facultad / Unidad:</span>
                <span className="text-slate-200 font-medium">{selectedConvocatoria.facultad_o_carrera}</span>
              </div>
              <div>
                <span className="text-slate-500 block mb-0.5">Nivel Académico:</span>
                <span className="text-slate-200 font-medium">{selectedConvocatoria.nivel}</span>
              </div>
              <div>
                <span className="text-slate-500 block mb-0.5">Modalidad & Sede:</span>
                <span className="text-slate-200 font-medium">{selectedConvocatoria.modalidad} - {selectedConvocatoria.ubicacion}</span>
              </div>
              <div>
                <span className="text-slate-500 block mb-0.5">Tipo de Contrato:</span>
                <span className="text-slate-200 font-medium">{selectedConvocatoria.tipo_contrato}</span>
              </div>
              <div>
                <span className="text-slate-500 block mb-0.5">Fecha Límite:</span>
                <span className="text-amber-400 font-semibold">{selectedConvocatoria.fecha_limite}</span>
              </div>
              <div>
                <span className="text-slate-500 block mb-0.5">Fuente Oficial:</span>
                <span className="text-indigo-300 font-medium">{selectedConvocatoria.fuente}</span>
              </div>
            </div>

            {/* Remuneration */}
            {selectedConvocatoria.remuneracion && (
              <div className="mb-4 bg-indigo-950/30 border border-indigo-900/60 p-3 rounded-xl text-xs">
                <span className="text-indigo-400 font-semibold block mb-0.5">Rango Salarial / Honorarios:</span>
                <span className="text-indigo-200">{selectedConvocatoria.remuneracion}</span>
              </div>
            )}

            {/* Description */}
            <div className="mb-5">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Descripción del Puesto / Concurso</h4>
              <p className="text-xs text-slate-300 leading-relaxed bg-slate-800/40 p-3 rounded-xl border border-slate-800">
                {selectedConvocatoria.descripcion}
              </p>
            </div>

            {/* Requirements */}
            <div className="mb-6">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Requisitos y Perfil Requerido</h4>
              <ul className="space-y-2">
                {selectedConvocatoria.requisitos.map((req, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{req}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Footer Buttons */}
            <div className="pt-4 border-t border-slate-800 flex items-center justify-end gap-3">
              <button
                onClick={() => setSelectedConvocatoria(null)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition"
              >
                Cerrar
              </button>

              <a
                href={selectedConvocatoria.enlace_postulacion}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition"
              >
                <span>Ir al Portal Oficial de Postulación</span>
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Checklist SUNEDU & Guía */}
      {showChecklistModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-y-auto custom-scrollbar p-6 shadow-2xl relative">
            <button
              onClick={() => setShowChecklistModal(false)}
              className="absolute top-5 right-5 p-1 rounded-lg text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2.5 mb-2">
              <div className="p-2 rounded-lg bg-emerald-600/20 text-emerald-400">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <h2 className="text-xl font-bold text-white">Checklist Esencial para Docencia Universitaria en Perú</h2>
            </div>
            <p className="text-xs text-slate-400 mb-5">
              Requisitos exigidos por la <strong>Ley Universitaria N° 30220</strong> y estándares de comités evaluadores peruanos.
            </p>

            <div className="space-y-4 text-xs text-slate-300">
              <div className="p-4 bg-slate-850 rounded-xl border border-slate-800">
                <h4 className="font-bold text-white text-sm mb-1.5 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  1. Grado de Maestro Inscrito en SUNEDU (Excluyente)
                </h4>
                <p className="text-slate-400 leading-relaxed">
                  Por ley, para dictar tanto en pregrado como en posgrado es obligatorio contar con el grado de Maestro o Doctor registrado en la base de datos de SUNEDU. Descarga la constancia digital desde <code>enlinea.sunedu.gob.pe</code>.
                </p>
              </div>

              <div className="p-4 bg-slate-850 rounded-xl border border-slate-800">
                <h4 className="font-bold text-white text-sm mb-1.5 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  2. Hoja de Vida Foliada vs. CV Ejecutivo
                </h4>
                <p className="text-slate-400 leading-relaxed">
                  • <strong>Universidades Públicas (UNI, UNMSM, UNFV, UNT, UNSA):</strong> Requieren expediente foliado de atrás hacia adelante con copias autenticadas de certificados.<br/>
                  • <strong>Universidades Privadas y Posgrado (UCV, UPN, Autónoma, PUCP, Ulima):</strong> CV ejecutivo moderno de 2 a 3 páginas enfocado en experiencia directiva, proyectos y asignaturas dominadas.
                </p>
              </div>

              <div className="p-4 bg-slate-850 rounded-xl border border-slate-800">
                <h4 className="font-bold text-white text-sm mb-1.5 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  3. Preparación de Clase Modelo (15 - 20 minutos)
                </h4>
                <p className="text-slate-400 leading-relaxed">
                  Ten preparado un deck tipo en PPT con: Logro de la sesión, dinámica interactiva / caso de estudio real, y rúbrica de evaluación. Es la prueba decisiva ante el jurado calificador.
                </p>
              </div>

              <div className="p-4 bg-slate-850 rounded-xl border border-slate-800">
                <h4 className="font-bold text-white text-sm mb-1.5 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  4. Registro en CTI Vitae / DINA (Concytec)
                </h4>
                <p className="text-slate-400 leading-relaxed">
                  Tener actualizado tu perfil CTI Vitae suma puntaje significativo en la tabla de méritos de concursos docentes universitarios.
                </p>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 text-right">
              <button
                onClick={() => setShowChecklistModal(false)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold rounded-lg transition"
              >
                Entendido
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Directorio Nacional de Todas las Universidades */}
      {showDirectorioModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar p-6 shadow-2xl relative flex flex-col">
            <button
              onClick={() => setShowDirectorioModal(false)}
              className="absolute top-5 right-5 p-1 rounded-lg text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 transition"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2.5 mb-2">
              <div className="p-2 rounded-lg bg-amber-500/20 text-amber-400">
                <School className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-white">Directorio Oficial de Universidades del Perú</h2>
                <p className="text-xs text-slate-400">
                  Acceso directo a los portales de selección, concursos públicos y bancos de talento de todas las universidades licenciadas.
                </p>
              </div>
            </div>

            {/* Filtros del Directorio */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 my-4 bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <div className="relative w-full sm:w-72">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  value={searchDirectorio}
                  onChange={(e) => setSearchDirectorio(e.target.value)}
                  placeholder="Buscar por universidad o región..."
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-amber-500"
                />
              </div>

              <div className="flex items-center gap-1.5 self-start sm:self-auto">
                {['Todos', 'Pública', 'Privada'].map((tipo) => (
                  <button
                    key={tipo}
                    onClick={() => setFilterDirectorioTipo(tipo)}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                      filterDirectorioTipo === tipo
                        ? 'bg-amber-600 text-white shadow-sm'
                        : 'bg-slate-800 text-slate-400 hover:text-white'
                    }`}
                  >
                    {tipo === 'Todos' ? `Todas (${universidadesDirectorio.length})` : tipo === 'Pública' ? 'Públicas' : 'Privadas'}
                  </button>
                ))}
              </div>
            </div>

            {/* Grid del Directorio */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 overflow-y-auto max-h-[55vh] pr-1 custom-scrollbar">
              {filteredDirectorio.map((uni, idx) => (
                <div
                  key={idx}
                  className="bg-slate-850/90 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 flex flex-col justify-between hover:shadow-lg transition group"
                >
                  <div>
                    <div className="flex items-start justify-between gap-2 mb-1.5">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider ${
                        uni.tipo === 'Pública'
                          ? 'bg-sky-500/10 text-sky-400 border border-sky-500/30'
                          : 'bg-purple-500/10 text-purple-300 border border-purple-500/30'
                      }`}>
                        {uni.tipo}
                      </span>
                      <span className="text-[10px] font-bold text-slate-300 bg-slate-800 px-2 py-0.5 rounded">
                        {uni.siglas}
                      </span>
                    </div>

                    <h4 className="font-bold text-white text-xs mb-1 group-hover:text-amber-300 transition line-clamp-1">
                      {uni.nombre}
                    </h4>

                    <div className="flex items-center gap-1 text-[11px] text-slate-400 mb-2">
                      <MapPin className="w-3 h-3 text-rose-400 shrink-0" />
                      <span className="line-clamp-1">{uni.region}</span>
                    </div>

                    <div className="bg-slate-950/60 rounded-md p-2 border border-slate-800/80 mb-2.5 space-y-0.5 text-[10px] text-slate-300">
                      <div><span className="text-slate-500">Niveles:</span> {uni.niveles}</div>
                      <div><span className="text-slate-500">Canal:</span> <span className="text-indigo-300">{uni.portal_nombre}</span></div>
                    </div>
                  </div>

                  <a
                    href={uni.enlace_docente}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center justify-center gap-1.5 w-full py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition"
                  >
                    <span>Ver Portal de Convocatorias</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              ))}
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Mostrando {filteredDirectorio.length} universidades</span>
              <button
                onClick={() => setShowDirectorioModal(false)}
                className="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded-lg transition"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-slate-950 border-t border-slate-800 py-8 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <GraduationCap className="w-4 h-4 text-indigo-400" />
            <span className="text-slate-300 font-semibold">Docentes Convocatorias Perú</span>
            <span>— Plataforma unificada de universidades públicas, privadas y posgrado</span>
          </div>

          <div className="flex flex-wrap items-center gap-3 text-slate-400">
            <span>UPN • UCV • Autónoma • UNMSM • UNI • PUCP • Ulima • USIL • Continental • UTP</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
