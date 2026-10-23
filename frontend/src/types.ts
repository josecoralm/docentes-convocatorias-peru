export interface Convocatoria {
  id: string;
  titulo: string;
  institucion: string;
  tipo_institucion: 'Pública' | 'Privada' | 'Escuela de Posgrado' | 'Instituto Superior';
  nivel: string;
  modalidad: string;
  ubicacion: string;
  facultad_o_carrera: string;
  tipo_contrato: string;
  remuneracion?: string;
  requisitos: string[];
  fecha_publicacion: string;
  fecha_limite: string;
  enlace_postulacion: string;
  fuente: string;
  estado: 'Abierta' | 'Banco Permanente' | 'Próxima' | 'Cerrada';
  descripcion: string;
  contacto?: string;
  tags: string[];
}

export interface PlatformStats {
  total_convocatorias: number;
  publicas: number;
  privadas: number;
  posgrado: number;
  pregrado: number;
  virtual_remoto: number;
  presencial_lima: number;
  por_institucion: Record<string, number>;
  por_fuente: Record<string, number>;
}

export interface UniversidadDirectorio {
  siglas: string;
  nombre: string;
  tipo: 'Pública' | 'Privada';
  region: string;
  enlace_docente: string;
  portal_nombre: string;
  niveles: string;
}
