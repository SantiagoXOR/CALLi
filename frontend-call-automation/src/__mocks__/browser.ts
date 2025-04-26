import { setupWorker } from 'msw';
import { handlers } from './handlers';

// Configurar el worker para pruebas en el navegador
export const worker = setupWorker(...handlers);
