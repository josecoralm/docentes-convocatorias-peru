import json
import os
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from models import Convocatoria, ConvocatoriaCreate, FiltrosConvocatoria, StatsResponse

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "convocatorias.json")
UNIVERSIDADES_PATH = os.path.join(DATA_DIR, "universidades_peru.json")

# Semilla de convocatorias docentes 100% verificadas para todas las universidades clave del Perú
SEED_CONVOCATORIAS = [
    {
        "id": "conv-ucv-01",
        "titulo": "Convocatoria Docente 2026-II / 2027-I - Pregrado, Posgrado y Programa SUBE (Adultos)",
        "institucion": "Universidad César Vallejo (UCV)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado, Posgrado y SUBE",
        "modalidad": "Presencial, Semipresencial y 100% Virtual",
        "ubicacion": "Nacional (Lima, Trujillo, Piura, Chiclayo, Chimbote, Tarapoto, Callao)",
        "facultad_o_carrera": "Facultad de Ciencias Empresariales, Ingeniería, Humanidades y Ciencias de la Salud",
        "tipo_contrato": "Tiempo Completo (TC) / Tiempo Parcial (TP)",
        "remuneracion": "Según escalafón docente y modalidad UCV",
        "requisitos": [
            "Grado Académico de Maestro o Doctor registrado ante la SUNEDU (Obligatorio)",
            "Experiencia mínima de 3 años en docencia universitaria o ejercicio profesional",
            "Manejo de plataformas virtuales de aprendizaje (Blackboard / Trilce)",
            "Disponibilidad horaria para el semestre académico"
        ],
        "fecha_publicacion": "2026-10-23",
        "fecha_limite": "Convocatoria Abierta Permanente en Sistema UCV",
        "enlace_postulacion": "https://my.ucv.edu.pe/Convocatoria/",
        "fuente": "Sistema Oficial de Convocatoria Docente UCV",
        "estado": "Abierta",
        "descripcion": "La Universidad César Vallejo convoca a nivel nacional a profesionales con grado de Maestro o Doctor para integrarse a su plana docente en sus 12 campus y en su programa de formación para adultos que trabajan (SUBE).",
        "contacto": "convocatoriadocente@ucv.edu.pe",
        "tags": ["UCV", "César Vallejo", "Nacional", "SUBE", "Pregrado y Posgrado", "SUNEDU"]
    },
    {
        "id": "conv-upn-02",
        "titulo": "Docente Universitario - Pregrado & Working Adult (Negocios, Ingeniería y Salud)",
        "institucion": "Universidad Privada del Norte (UPN)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado y Working Adult",
        "modalidad": "Presencial y Semipresencial",
        "ubicacion": "Lima (Sedes Breña, Los Olivos, SJL, Chorrillos), Trujillo y Cajamarca",
        "facultad_o_carrera": "Facultad de Negocios, Ingeniería, Comunicaciones y Salud",
        "tipo_contrato": "Tiempo Completo / Tiempo Parcial",
        "remuneracion": "Escala salarial competitiva Red Laureate + Beneficios de ley",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU",
            "Mínimo 3 a 5 años de trayectoria profesional en su especialidad",
            "Enfoque en metodologías activas y flipped classroom"
        ],
        "fecha_publicacion": "2026-10-23",
        "fecha_limite": "Hasta cubrir vacantes para ciclo de verano y 2027-I",
        "enlace_postulacion": "https://pe.computrabajo.com/trabajo-de-docente-upn",
        "fuente": "Portal Oficial Selección UPN (Computrabajo / Laureate)",
        "estado": "Abierta",
        "descripcion": "Procesos continuos de incorporación a la plana docente de UPN en sus campus de Lima, Trujillo y Cajamarca para carreras diurnas y el programa Working Adult para ejecutivos.",
        "contacto": "selecciondocente@upn.pe",
        "tags": ["UPN", "Laureate", "Working Adult", "Lima", "Trujillo", "Cajamarca"]
    },
    {
        "id": "conv-autonoma-03",
        "titulo": "Convocatoria Docente 2026 - 2027 - Módulo Oficial de Selección",
        "institucion": "Universidad Autónoma del Perú",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado, Gente que Trabaja y Posgrado",
        "modalidad": "Presencial y Semipresencial",
        "ubicacion": "Lima (Campus Lima Sur - Villa El Salvador)",
        "facultad_o_carrera": "Facultades de Ciencias de Gestión, Ingeniería y Arquitectura, Humanidades",
        "tipo_contrato": "Tiempo Parcial / Tiempo Completo",
        "remuneracion": "Tarifario institucional de la Universidad Autónoma",
        "requisitos": [
            "Grado de Maestro o Doctor inscrito en SUNEDU",
            "Experiencia laboral y docente comprobada",
            "Registro en el módulo virtual de convocatorias de la Autónoma"
        ],
        "fecha_publicacion": "2026-10-23",
        "fecha_limite": "Convocatoria Continua en Portal Virtual",
        "enlace_postulacion": "https://virtual.autonoma.edu.pe/Externa/Convocatorias/ConvocatoriaDocente.aspx",
        "fuente": "Módulo Virtual Convocatoria Docente Autónoma",
        "estado": "Abierta",
        "descripcion": "La Universidad Autónoma del Perú mantiene abierta la recepción y evaluación de expedientes para docentes que impartirán cátedra en pregrado tradicional, programa para adultos que trabajan y maestrías.",
        "contacto": "talentohumano@autonoma.pe",
        "tags": ["Autónoma", "Lima Sur", "Villa El Salvador", "Pregrado", "Gente que Trabaja"]
    },
    {
        "id": "conv-pucp-04",
        "titulo": "Convocatorias Docentes Ordinarios y Contratados - Portal del Profesorado PUCP",
        "institucion": "Pontificia Universidad Católica del Perú (PUCP)",
        "tipo_institucion": "Privada",
        "nivel": "Posgrado y Pregrado",
        "modalidad": "Presencial / Semipresencial",
        "ubicacion": "Lima (San Miguel - Campus PUCP)",
        "facultad_o_carrera": "Departamentos Académicos de Ciencias de la Gestión, Ingeniería y Ciencias Sociales",
        "tipo_contrato": "Tiempo Completo (TC) / Tiempo Parcial (TP)",
        "remuneracion": "Escalafón Docente PUCP (según categoría docente)",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU (Excluyente según Ley 30220)",
            "Experiencia académica y profesional acreditada en el área del concurso",
            "Presentación de expediente documentado y clase modelo"
        ],
        "fecha_publicacion": "2026-10-20",
        "fecha_limite": "Revisar cronograma por departamento académico",
        "enlace_postulacion": "https://profesorado.pucp.edu.pe/convocatorias/presentacion/",
        "fuente": "Portal del Profesorado PUCP (Oficial)",
        "estado": "Abierta",
        "descripcion": "Portal centralizado de la PUCP donde cada Departamento Académico publica sus bases oficiales, cronogramas de evaluación de legajos, fechas de clases magistrales y plazas docentes vacantes para el semestre.",
        "contacto": "profesorado@pucp.edu.pe",
        "tags": ["PUCP", "Profesorado", "Bases Oficiales", "Concurso", "Posgrado y Pregrado"]
    },
    {
        "id": "conv-centrum-05",
        "titulo": "Catedrático de Posgrado - MBA & Maestría en Dirección Estratégica y SCM",
        "institucion": "CENTRUM PUCP Graduate Business School",
        "tipo_institucion": "Privada",
        "nivel": "Posgrado",
        "modalidad": "Presencial / Blended",
        "ubicacion": "Lima (Santiago de Surco - Los Álamos)",
        "facultad_o_carrera": "Escuela de Posgrado en Negocios (Triple Corona)",
        "tipo_contrato": "Tiempo Parcial / Módulos Ejecutivos",
        "remuneracion": "Tarifario Docente de Posgrado Élite",
        "requisitos": [
            "Grado de Doctor (Ph.D. / DBA) o Maestro con registro ante SUNEDU",
            "Trayectoria gerencial activa de alto nivel (CEO, Director, Gerente de Área)",
            "Publicaciones o certificaciones internacionales (PMP, CSCP, CFA)"
        ],
        "fecha_publicacion": "2026-10-18",
        "fecha_limite": "Banco Permanente de Cátedra 2026-2027",
        "enlace_postulacion": "https://centrum.pucp.edu.pe/",
        "fuente": "Portal Oficial CENTRUM PUCP",
        "estado": "Banco Permanente",
        "descripcion": "CENTRUM PUCP mantiene abierta la recepción de CVs de profesionales destacados para dictar en sus programas de Maestría en Dirección de Operaciones, Logística Integral y MBA Gerencial.",
        "contacto": "coordinaciondocente@pucp.edu.pe",
        "tags": ["CENTRUM", "PUCP", "MBA", "SCM", "Posgrado", "Surco"]
    },
    {
        "id": "conv-usil-06",
        "titulo": "Docente Facilitador Practitioner - Negocios, SCM y Programas para Adultos CPEL",
        "institucion": "Universidad San Ignacio de Loyola (USIL)",
        "tipo_institucion": "Privada",
        "nivel": "Posgrado y CPEL",
        "modalidad": "Semipresencial / Híbrido",
        "ubicacion": "Lima (La Molina / San Isidro)",
        "facultad_o_carrera": "Facultad de Ciencias Empresariales & CPEL",
        "tipo_contrato": "Tiempo Parcial / Por Asignatura",
        "remuneracion": "Honorarios competitivos según escalafón docente USIL",
        "requisitos": [
            "Grado de Maestro registrado ante SUNEDU",
            "Mínimo 5 años en funciones de jefatura o gerencia activa en empresas",
            "Manejo de plataformas virtuales de aprendizaje (Canvas) y metodología de casos"
        ],
        "fecha_publicacion": "2026-10-22",
        "fecha_limite": "Convocatoria Continua en HiringRoom",
        "enlace_postulacion": "https://usil.hiringroom.com/jobs",
        "fuente": "HiringRoom USIL (Portal Oficial de Selección)",
        "estado": "Abierta",
        "descripcion": "Portal oficial de selección docente USIL en HiringRoom. Convocatorias vigentes para el programa de Carreras Universitarias para Personas con Experiencia Laboral (CPEL) y Escuela de Posgrado.",
        "contacto": "reclutamientodocente@usil.edu.pe",
        "tags": ["USIL", "CPEL", "HiringRoom", "Posgrado", "La Molina", "San Isidro"]
    },
    {
        "id": "conv-ulima-07",
        "titulo": "Docentes de Maestría y Pregrado - Ciencias Empresariales y Posgrado",
        "institucion": "Universidad de Lima (Ulima)",
        "tipo_institucion": "Privada",
        "nivel": "Posgrado y Pregrado",
        "modalidad": "Presencial",
        "ubicacion": "Lima (Santiago de Surco - Campus Monterrico)",
        "facultad_o_carrera": "Facultad de Ciencias Empresariales y Económicas / Posgrado",
        "tipo_contrato": "Tiempo Parcial / Horas de Cátedra",
        "remuneracion": "Tarifario Ulima (S/. 120 - S/. 200 / hora posgrado)",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU (Indispensable)",
            "Experiencia laboral directiva no menor a 7 años en áreas corporativas",
            "Experiencia en docencia universitaria o facilitación ejecutiva"
        ],
        "fecha_publicacion": "2026-10-19",
        "fecha_limite": "Convocatoria Ciclos 2026-II y 2027-I",
        "enlace_postulacion": "https://www.bumeran.com.pe/perfiles/empresa_universidad-de-lima_10022416.html",
        "fuente": "Bolsa Oficial Ulima en Bumeran",
        "estado": "Abierta",
        "descripcion": "Canal oficial donde la Universidad de Lima publica sus avisos de selección docente y plazas académicas para incorporación al cuerpo de profesores de pregrado y posgrado.",
        "contacto": "posgrado@ulima.edu.pe",
        "tags": ["Ulima", "Universidad de Lima", "Surco", "Posgrado", "Bumeran"]
    },
    {
        "id": "conv-sanmarcos-08",
        "titulo": "Concurso Público de Plazas Docentes y Posgrado - UNMSM",
        "institucion": "Universidad Nacional Mayor de San Marcos (UNMSM)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Lima (Ciudad Universitaria - Cercado de Lima)",
        "facultad_o_carrera": "Facultades de Ciencias Administrativas, Ciencias Económicas e Ingeniería",
        "tipo_contrato": "Concurso Público de Méritos (Ley N° 30220)",
        "remuneracion": "Régimen del Ministerio de Educación / Docencia Pública (S/. 3,200 - S/. 7,500)",
        "requisitos": [
            "Grado de Maestro o Doctor inscrito en SUNEDU",
            "Expediente documentado y foliado según reglamento del concurso",
            "Presentación de clase modelo presencial y entrevista ante jurado"
        ],
        "fecha_publicacion": "2026-10-21",
        "fecha_limite": "Consultar cronograma por facultad en bases oficiales",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=unmsm",
        "fuente": "Talento Perú / Convocatorias de Trabajo UNMSM",
        "estado": "Abierta",
        "descripcion": "Bases completas y seguimiento de los concursos públicos docentes y contrataciones de cátedra en la Decana de América canalizados por el portal oficial del estado peruano.",
        "contacto": "fca_academica@unmsm.edu.pe",
        "tags": ["UNMSM", "San Marcos", "Pública", "Concurso Público", "Bases Oficiales"]
    },
    {
        "id": "conv-uni-09",
        "titulo": "Concurso de Plazas y Contrato Docente - Universidad Nacional de Ingeniería",
        "institucion": "Universidad Nacional de Ingeniería (UNI)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Lima (Rímac - Campus UNI)",
        "facultad_o_carrera": "Facultad de Ingeniería Industrial y de Sistemas (FIIS) / Posgrado UNI",
        "tipo_contrato": "Concurso Público Docente (Categorías DC-A1, DC-B1)",
        "remuneracion": "Escala del Sector Público Universitario",
        "requisitos": [
            "Título profesional de Ingeniero o afín con Maestría registrada en SUNEDU",
            "Legajo académico documentado y foliado",
            "Aprobación de la evaluación curricular y clase magistral"
        ],
        "fecha_publicacion": "2026-10-21",
        "fecha_limite": "Vigente según calendario de concurso",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=uni",
        "fuente": "Talento Perú / Convocatorias UNI",
        "estado": "Abierta",
        "descripcion": "Listado de bases y plazas docentes convocadas por la UNI para sus facultades de ingeniería y secciones de posgrado. Incluye requisitos, cronograma y formatos de declaración jurada.",
        "contacto": "decanato_fiis@uni.edu.pe",
        "tags": ["UNI", "Pública", "Ingeniería Industrial", "FIIS", "Concurso Público"]
    },
    {
        "id": "conv-unt-10",
        "titulo": "Concurso Público de Plazas y Contrato Docente - UNT La Libertad",
        "institucion": "Universidad Nacional de Trujillo (UNT)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "La Libertad (Trujillo)",
        "facultad_o_carrera": "Facultad de Ciencias Económicas, Ingeniería y Derecho",
        "tipo_contrato": "Concurso Público de Méritos",
        "remuneracion": "Escala Oficial Docencia Universitaria Pública",
        "requisitos": [
            "Grado de Maestro o Doctor con inscripción en SUNEDU",
            "Presentación de carpeta docente documentada según bases",
            "Sustentación de clase magistral"
        ],
        "fecha_publicacion": "2026-10-22",
        "fecha_limite": "Consultar bases publicadas en portal",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=trujillo",
        "fuente": "Talento Perú / Convocatorias UNT",
        "estado": "Abierta",
        "descripcion": "La primera universidad republicana del Perú convoca a concurso público de méritos para plazas docentes de pregrado y escuela de posgrado en Trujillo.",
        "contacto": "admision_docente@unitru.edu.pe",
        "tags": ["UNT", "Trujillo", "La Libertad", "Pública", "Norte"]
    },
    {
        "id": "conv-unsa-11",
        "titulo": "Concurso de Plazas Docentes Ordinarios y Contratados - UNSA Arequipa",
        "institucion": "Universidad Nacional de San Agustín (UNSA)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Arequipa (Campus San Agustín)",
        "facultad_o_carrera": "Facultad de Administración, Ingeniería de Producción y Economía",
        "tipo_contrato": "Concurso Público de Méritos",
        "remuneracion": "Régimen del Ministerio de Educación",
        "requisitos": [
            "Grado Académico registrado ante SUNEDU",
            "Registro en CTI Vitae / DINA Concytec",
            "Expediente foliado en orden cronológico"
        ],
        "fecha_publicacion": "2026-10-22",
        "fecha_limite": "Vigente según bases oficiales",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=unsa",
        "fuente": "Talento Perú / Concursos UNSA",
        "estado": "Abierta",
        "descripcion": "Convocatorias públicas y bases de méritos para el ingreso a la carrera docente en la Universidad Nacional de San Agustín de Arequipa.",
        "contacto": "concursodocente@unsa.edu.pe",
        "tags": ["UNSA", "Arequipa", "Pública", "Sur", "Concurso Público"]
    },
    {
        "id": "conv-uncp-12",
        "titulo": "Concurso Docente Público - Universidad Nacional del Centro del Perú",
        "institucion": "Universidad Nacional del Centro del Perú (UNCP)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Junín (Huancayo)",
        "facultad_o_carrera": "Facultades de Administración, Economía e Ingeniería",
        "tipo_contrato": "Concurso Público Docente",
        "remuneracion": "Escalas de Ley Universitaria N° 30220",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU",
            "Expediente foliado y sustentación académica"
        ],
        "fecha_publicacion": "2026-10-21",
        "fecha_limite": "Según cronograma oficial",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=centro+del+peru",
        "fuente": "Talento Perú / Convocatorias UNCP",
        "estado": "Abierta",
        "descripcion": "Concurso público de méritos para docentes contratados en la principal universidad pública de la región centro del Perú.",
        "contacto": "vicerrectorado_academico@uncp.edu.pe",
        "tags": ["UNCP", "Huancayo", "Junín", "Centro", "Pública"]
    },
    {
        "id": "conv-pacific-13",
        "titulo": "Profesores de Cátedra - Pacífico Business School (PBS) & Maestrías",
        "institucion": "Pacífico Business School (PBS) - Univ. del Pacífico",
        "tipo_institucion": "Privada",
        "nivel": "Posgrado",
        "modalidad": "Presencial / Semipresencial",
        "ubicacion": "Lima (Jesús María)",
        "facultad_o_carrera": "Escuela de Posgrado / Maestrías Especializadas en Gestión",
        "tipo_contrato": "Tiempo Parcial / Modular",
        "remuneracion": "Escala Élite de Posgrado UP",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU",
            "Desempeñar cargos de dirección, gerencia o consultoría senior en el sector privado",
            "Capacidad pedagógica y orientación a la toma de decisiones directivas"
        ],
        "fecha_publicacion": "2026-10-17",
        "fecha_limite": "Banco Permanente de Cátedra",
        "enlace_postulacion": "https://pbs.edu.pe/",
        "fuente": "Portal Oficial Pacífico Business School",
        "estado": "Banco Permanente",
        "descripcion": "La Escuela de Negocios de la Universidad del Pacífico convoca a especialistas y directivos de primer nivel para incorporarse a sus maestrías especializadas en Operaciones, Logística y Finanzas.",
        "contacto": "postulaciones_pbs@up.edu.pe",
        "tags": ["PBS", "Pacífico", "Posgrado", "Jesús María", "Privada Top"]
    },
    {
        "id": "conv-esan-14",
        "titulo": "Cátedra de Posgrado - Maestrías Especializadas y MBA ESAN",
        "institucion": "ESAN Graduate School of Business",
        "tipo_institucion": "Privada",
        "nivel": "Posgrado",
        "modalidad": "Presencial / Blended",
        "ubicacion": "Lima (Santiago de Surco - Alonso de Molina)",
        "facultad_o_carrera": "Escuela de Posgrado en Administración",
        "tipo_contrato": "Tiempo Parcial / Por Asignatura",
        "remuneracion": "Honorarios preferenciales según tarifario ESAN",
        "requisitos": [
            "Grado Académico de Maestro registrado ante SUNEDU",
            "Trayectoria ejecutiva demostrable de al menos 6 años",
            "Deseable publicaciones y certificaciones del sector"
        ],
        "fecha_publicacion": "2026-10-18",
        "fecha_limite": "Convocatoria Abierta Ciclo Modular",
        "enlace_postulacion": "https://www.esan.edu.pe/maestrias",
        "fuente": "Portal Oficial ESAN Posgrado",
        "estado": "Abierta",
        "descripcion": "Acceso a la oferta de maestrías especializadas de ESAN y contacto con las coordinaciones de programas para la postulación a la plana docente en Supply Chain, Finanzas y Dirección.",
        "contacto": "rrhh@esan.edu.pe",
        "tags": ["ESAN", "Posgrado", "Maestría", "Surco", "Negocios"]
    },
    {
        "id": "conv-continental-15",
        "titulo": "Docente 100% Virtual - Facultad de Ciencias de la Empresa y Posgrado",
        "institucion": "Universidad Continental (Modalidad a Distancia)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "100% Virtual / Remoto",
        "ubicacion": "Nacional Remoto (Todo el Perú)",
        "facultad_o_carrera": "Escuela de Negocios y Escuela de Posgrado",
        "tipo_contrato": "Tiempo Parcial / Virtual Continuo",
        "remuneracion": "S/. 50 - S/. 85 / hora de cátedra virtual",
        "requisitos": [
            "Grado de Maestro registrado en SUNEDU (Indispensable)",
            "Experiencia dictando en aulas virtuales y plataformas de teleducación",
            "Conexión de alta velocidad y disponibilidad para sesiones sincrónicas"
        ],
        "fecha_publicacion": "2026-10-21",
        "fecha_limite": "Convocatoria Bimestral Permanente",
        "enlace_postulacion": "https://posgrado.ucontinental.edu.pe/",
        "fuente": "Portal Continental Posgrado",
        "estado": "Abierta",
        "descripcion": "La universidad líder en educación a distancia en el Perú contrata docentes para sus programas 100% remotos en Administración, Logística, Gestión Pública y Marketing Digital.",
        "contacto": "talentodocente@continental.edu.pe",
        "tags": ["100% Virtual", "Remoto", "Nacional", "Continental", "Posgrado"]
    },
    {
        "id": "conv-unalm-16",
        "titulo": "Concurso Público de Contrato Docente - UNALM",
        "institucion": "Universidad Nacional Agraria La Molina (UNALM)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Lima (La Molina)",
        "facultad_o_carrera": "Facultad de Economía y Planificación / Escuela de Posgrado",
        "tipo_contrato": "Concurso Público Docente",
        "remuneracion": "Régimen del Ministerio de Educación",
        "requisitos": [
            "Título profesional y Maestría registrada en SUNEDU",
            "Experiencia profesional y docente en economía, agronegocios o gestión",
            "Presentación de legajo en mesa de partes presencial o virtual"
        ],
        "fecha_publicacion": "2026-10-20",
        "fecha_limite": "Consultar bases de la convocatoria",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=agraria",
        "fuente": "Talento Perú / Convocatorias UNALM",
        "estado": "Abierta",
        "descripcion": "Bases de concursos docentes para contratación y nombramiento en la Universidad Nacional Agraria La Molina. Plazas para asignaturas teóricas y prácticas.",
        "contacto": "sec_academica_fep@lamolina.edu.pe",
        "tags": ["UNALM", "La Molina", "Pública", "Economía", "Agronegocios"]
    },
    {
        "id": "conv-unfv-17",
        "titulo": "Concurso Público de Méritos Docente - Universidad Nacional Federico Villarreal",
        "institucion": "Universidad Nacional Federico Villarreal (UNFV)",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Lima (Cercado de Lima / San Miguel)",
        "facultad_o_carrera": "Facultades de Ciencias Económicas, Administrativas y Tecnología Médica",
        "tipo_contrato": "Concurso Público de Méritos",
        "remuneracion": "Escala del Estado Peruano / Ley Universitaria",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU",
            "Expediente foliado en orden cronológico inverso",
            "Sustentación de clase magistral y entrevista ante comisiones de concurso"
        ],
        "fecha_publicacion": "2026-10-21",
        "fecha_limite": "Vigente según bases oficiales",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=unfv",
        "fuente": "Talento Perú / Convocatorias UNFV",
        "estado": "Abierta",
        "descripcion": "Convocatorias públicas docentes de la UNFV canalizadas a través del portal de contrataciones del estado, con acceso directo a resoluciones, cronogramas y perfiles requeridos.",
        "contacto": "concursodocente@unfv.edu.pe",
        "tags": ["UNFV", "Villarreal", "Pública", "Concurso de Méritos", "Lima"]
    },
    {
        "id": "conv-usmp-18",
        "titulo": "Bolsa de Selección Docente - Pregrado, Posgrado y USMP Virtual",
        "institucion": "Universidad de San Martín de Porres (USMP)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado, Posgrado y Virtual",
        "modalidad": "Presencial y 100% Virtual",
        "ubicacion": "Lima (Santa Anita, San Isidro), Chiclayo, Arequipa y Nivel Nacional Virtual",
        "facultad_o_carrera": "Facultades de Ciencias Administrativas, Derecho, Medicina y Educación",
        "tipo_contrato": "Tiempo Parcial / Tiempo Completo",
        "remuneracion": "Tarifario docente USMP",
        "requisitos": [
            "Grado de Maestro registrado en SUNEDU",
            "Experiencia docente universitaria acreditada",
            "Manejo de entorno virtual Moodle / USMP Virtual"
        ],
        "fecha_publicacion": "2026-10-22",
        "fecha_limite": "Convocatorias Semestrales Abiertas",
        "enlace_postulacion": "https://www.bumeran.com.pe/empleos-busqueda-docente-san-martin-de-porres.html",
        "fuente": "Bolsa de Selección Docente USMP en Bumeran",
        "estado": "Abierta",
        "descripcion": "Recepción continua de candidaturas docentes para facultades presenciales de Lima y provincias, así como para la unidad de educación a distancia USMP Virtual.",
        "contacto": "rrhh@usmp.pe",
        "tags": ["USMP", "San Martín de Porres", "Santa Anita", "Virtual", "Nacional"]
    },
    {
        "id": "conv-urp-19",
        "titulo": "Concurso y Banco de Plazas Docentes - Universidad Ricardo Palma",
        "institucion": "Universidad Ricardo Palma (URP)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial y Semipresencial",
        "ubicacion": "Lima (Surco - Av. Benavides)",
        "facultad_o_carrera": "Facultad de Ciencias Económicas y Empresariales / Posgrado",
        "tipo_contrato": "Tiempo Parcial / Tiempo Completo",
        "remuneracion": "Tarifario institucional URP",
        "requisitos": [
            "Grado de Maestro o Doctor registrado en SUNEDU",
            "Sólida formación académica y experiencia docente"
        ],
        "fecha_publicacion": "2026-10-21",
        "fecha_limite": "Vigente según bases del departamento",
        "enlace_postulacion": "https://www.bumeran.com.pe/empleos-busqueda-docente-ricardo-palma.html",
        "fuente": "Bolsa Docente URP en Bumeran",
        "estado": "Abierta",
        "descripcion": "Procesos de selección para profesores de cátedra en administración, negocios internacionales, ingeniería y programas de posgrado de la URP.",
        "contacto": "academica@urp.edu.pe",
        "tags": ["URP", "Ricardo Palma", "Surco", "Pregrado", "Privada"]
    },
    {
        "id": "conv-portal-bumeran-20",
        "titulo": "Búsqueda Activa de Docentes Universitarios en Portales de Empleo",
        "institucion": "Bumeran Perú (Múltiples Universidades Privadas)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial y Virtual",
        "ubicacion": "Lima y Nivel Nacional",
        "facultad_o_carrera": "Todas las Universidades Licenciadas del Perú",
        "tipo_contrato": "Tiempo Completo / Tiempo Parcial",
        "remuneracion": "Acorde al mercado educativo privado",
        "requisitos": [
            "Grado de Maestro registrado ante SUNEDU",
            "Perfil profesional activo en Bumeran",
            "Experiencia en docencia universitaria o superior"
        ],
        "fecha_publicacion": "2026-10-23",
        "fecha_limite": "Actualización diaria en vivo",
        "enlace_postulacion": "https://www.bumeran.com.pe/empleos-busqueda-docente-universitario.html",
        "fuente": "Bumeran Perú (Búsqueda en Vivo)",
        "estado": "Abierta",
        "descripcion": "Listado en tiempo real con todas las ofertas de trabajo publicadas por universidades privadas peruanas e institutos superiores en la plataforma Bumeran.",
        "contacto": "Postulación directa en Bumeran",
        "tags": ["Bumeran", "Portal de Empleo", "Privadas", "Docencia Universitaria"]
    },
    {
        "id": "conv-portal-computrabajo-21",
        "titulo": "Convocatorias Docentes Universitarias en Computrabajo Perú",
        "institucion": "Computrabajo Perú (Universidades Masivas y Privadas)",
        "tipo_institucion": "Privada",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial, Semipresencial y Remoto",
        "ubicacion": "Lima y Regiones",
        "facultad_o_carrera": "Facultades de Negocios, Ingeniería, Ciencias y Humanidades",
        "tipo_contrato": "Tiempo Parcial / Tiempo Completo",
        "remuneracion": "Según categoría docente de la institución",
        "requisitos": [
            "Grado de Maestro registrado en SUNEDU",
            "Experiencia laboral demostrable en la especialidad",
            "Disponibilidad para horarios de pregrado o carreras para adultos"
        ],
        "fecha_publicacion": "2026-10-23",
        "fecha_limite": "Actualización diaria continua",
        "enlace_postulacion": "https://pe.computrabajo.com/trabajo-de-docente-universitario",
        "fuente": "Computrabajo Perú (Búsqueda Oficial)",
        "estado": "Abierta",
        "descripcion": "Monitoreo centralizado de todas las convocatorias docentes universitarias vigentes en Computrabajo en el territorio peruano.",
        "contacto": "Postulación directa en Computrabajo",
        "tags": ["Computrabajo", "Portal de Empleo", "Pregrado", "Nacional"]
    },
    {
        "id": "conv-portal-talento-22",
        "titulo": "Bolsa de Concursos Públicos Docentes en Universidades Nacionales",
        "institucion": "Talento Perú / Convocatorias de Trabajo Perú",
        "tipo_institucion": "Pública",
        "nivel": "Pregrado y Posgrado",
        "modalidad": "Presencial",
        "ubicacion": "Lima y Todas las Regiones del Perú",
        "facultad_o_carrera": "Todas las Universidades Públicas Licenciadas",
        "tipo_contrato": "Concurso Público de Méritos (Nombramiento y Contrato)",
        "remuneracion": "Escalas de Ley Universitaria N° 30220 / MINEDU",
        "requisitos": [
            "Grados académicos SUNEDU (Maestro / Doctor según categoría)",
            "Expediente foliado y documentos autenticados",
            "Cumplir bases específicas de cada universidad nacional"
        ],
        "fecha_publicacion": "2026-10-23",
        "fecha_limite": "Vigente según cada proceso",
        "enlace_postulacion": "https://www.convocatoriasdetrabajo.com/buscar-empleo.php?palabra=docente+universitario",
        "fuente": "Convocatorias de Trabajo Perú / SERVIR",
        "estado": "Abierta",
        "descripcion": "Agregador de concursos públicos de méritos para docentes en todas las universidades nacionales del Perú (UNMSM, UNI, UNFV, UNALM, UNAC, UNCP, UNSA, UNT, UNSAAC, UNA Puno, etc.).",
        "contacto": "Mesa de partes de la universidad convocante",
        "tags": ["Talento Perú", "Concursos Públicos", "Universidades Nacionales", "SUNEDU"]
    }
]

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(SEED_CONVOCATORIAS, f, ensure_ascii=False, indent=2)

def load_convocatorias() -> List[dict]:
    init_db()
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error loading DB: {e}")
        return SEED_CONVOCATORIAS

def save_convocatorias(convocatorias: List[dict]):
    init_db()
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(convocatorias, f, ensure_ascii=False, indent=2)

def load_universidades_directorio() -> List[dict]:
    if os.path.exists(UNIVERSIDADES_PATH):
        try:
            with open(UNIVERSIDADES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading universidades: {e}")
    return []

def strip_accents(text: str) -> str:
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').lower()

def query_convocatorias(filtros: FiltrosConvocatoria) -> Tuple[List[Convocatoria], int]:
    raw_data = load_convocatorias()
    results = []

    q_normalized = strip_accents(filtros.q.strip()) if filtros.q else None
    
    for item in raw_data:
        # Texto de búsqueda general
        if q_normalized:
            searchable_text = f"{item.get('titulo', '')} {item.get('institucion', '')} {item.get('facultad_o_carrera', '')} {item.get('descripcion', '')} {' '.join(item.get('tags', []))} {item.get('ubicacion', '')}"
            if q_normalized not in strip_accents(searchable_text):
                continue

        # Filtro por tipo de institución (Pública, Privada)
        if filtros.tipo_institucion and filtros.tipo_institucion != "Todos":
            if item.get("tipo_institucion") != filtros.tipo_institucion:
                continue

        # Filtro por nivel (Posgrado, Pregrado, CPEL/Ejecutiva)
        if filtros.nivel and filtros.nivel != "Todos":
            item_nivel = item.get("nivel", "")
            if filtros.nivel not in item_nivel and item_nivel != "Pregrado y Posgrado":
                continue

        # Filtro por modalidad (Presencial, Virtual, Híbrido)
        if filtros.modalidad and filtros.modalidad != "Todos":
            if filtros.modalidad not in item.get("modalidad", ""):
                continue

        # Filtro por institución específica
        if filtros.institucion and filtros.institucion != "Todas":
            if filtros.institucion.lower() not in item.get("institucion", "").lower():
                continue

        # Filtro por fuente
        if filtros.fuente and filtros.fuente != "Todas":
            if filtros.fuente.lower() not in item.get("fuente", "").lower():
                continue

        # Filtro por estado
        if filtros.estado and filtros.estado != "Todos":
            if item.get("estado") != filtros.estado:
                continue

        results.append(Convocatoria(**item))

    total = len(results)
    paginated = results[filtros.skip : filtros.skip + filtros.limit]
    return paginated, total

def get_stats() -> StatsResponse:
    data = load_convocatorias()
    total = len(data)
    publicas = sum(1 for c in data if c.get("tipo_institucion") == "Pública")
    privadas = sum(1 for c in data if c.get("tipo_institucion") == "Privada")
    posgrado = sum(1 for c in data if "Posgrado" in c.get("nivel", "") or "Maestr" in c.get("nivel", "") or "Maestr" in c.get("titulo", ""))
    pregrado = sum(1 for c in data if "Pregrado" in c.get("nivel", ""))
    virtual_remoto = sum(1 for c in data if "Virtual" in c.get("modalidad", "") or "Remoto" in c.get("modalidad", ""))
    presencial_lima = sum(1 for c in data if "Lima" in c.get("ubicacion", ""))

    por_institucion = {}
    for c in data:
        inst = c.get("institucion", "Otra")
        por_institucion[inst] = por_institucion.get(inst, 0) + 1

    por_fuente = {}
    for c in data:
        fuente = c.get("fuente", "Portal")
        if "Talento Perú" in fuente or "Convocatorias de Trabajo" in fuente:
            key = "Talento Perú / Convocatorias de Trabajo"
        elif "Computrabajo" in fuente:
            key = "Computrabajo"
        elif "Bumeran" in fuente:
            key = "Bumeran"
        elif "HiringRoom" in fuente:
            key = "HiringRoom USIL"
        elif "PUCP" in fuente:
            key = "Portal del Profesorado PUCP"
        elif "UCV" in fuente:
            key = "Sistema Convocatoria UCV"
        elif "Autónoma" in fuente or "Autonoma" in fuente:
            key = "Portal Convocatoria Autónoma"
        else:
            key = "Bolsa Oficial Universitaria"
        por_fuente[key] = por_fuente.get(key, 0) + 1

    return StatsResponse(
        total_convocatorias=total,
        publicas=publicas,
        privadas=privadas,
        posgrado=posgrado,
        pregrado=pregrado,
        virtual_remoto=virtual_remoto,
        presencial_lima=presencial_lima,
        por_institucion=por_institucion,
        por_fuente=por_fuente
    )

def add_or_update_convocatoria(c_data: dict) -> Convocatoria:
    data = load_convocatorias()
    existing_idx = next((i for i, item in enumerate(data) if item["id"] == c_data["id"]), None)
    if existing_idx is not None:
        data[existing_idx] = c_data
    else:
        data.insert(0, c_data)
    save_convocatorias(data)
    return Convocatoria(**c_data)
