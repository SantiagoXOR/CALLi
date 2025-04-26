import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Configurar el servidor de mocks
export const server = setupServer(...handlers);
