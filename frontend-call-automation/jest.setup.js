// Learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
    pathname: '',
  }),
  useParams: () => ({}),
  usePathname: () => '',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock sonner toast
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    info: jest.fn(),
    warning: jest.fn(),
  },
  Toaster: () => null,
}));

// Mock axios
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    get: jest.fn(),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn(),
    interceptors: {
      request: { use: jest.fn(), eject: jest.fn() },
      response: { use: jest.fn(), eject: jest.fn() },
    },
  })),
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  defaults: { baseURL: '' },
}));

// Mock para date-fns
jest.mock('date-fns', () => ({
  formatDistanceToNow: jest.fn(() => 'hace 2 días'),
  format: jest.fn(() => '01/01/2023'),
  parseISO: jest.fn(() => new Date()),
  isValid: jest.fn(() => true),
  addDays: jest.fn((date) => date),
  subDays: jest.fn((date) => date),
}));

jest.mock('date-fns/locale', () => ({
  es: {},
}));

// Mock para zod
jest.mock('zod', () => {
  const actual = jest.requireActual('zod');
  return {
    ...actual,
    z: {
      ...actual.z,
      object: jest.fn().mockReturnValue({
        shape: {},
        refine: jest.fn().mockReturnThis(),
      }),
      string: jest.fn().mockReturnValue({
        min: jest.fn().mockReturnThis(),
        max: jest.fn().mockReturnThis(),
        email: jest.fn().mockReturnThis(),
        optional: jest.fn().mockReturnThis(),
        or: jest.fn().mockReturnThis(),
        regex: jest.fn().mockReturnThis(),
        refine: jest.fn().mockReturnThis(),
      }),
      number: jest.fn().mockReturnValue({
        int: jest.fn().mockReturnThis(),
        min: jest.fn().mockReturnThis(),
        max: jest.fn().mockReturnThis(),
        optional: jest.fn().mockReturnThis(),
      }),
      array: jest.fn().mockReturnValue({
        optional: jest.fn().mockReturnThis(),
      }),
    },
  };
});

// Mock para @hookform/resolvers/zod
jest.mock('@hookform/resolvers/zod', () => ({
  zodResolver: jest.fn(() => jest.fn()),
}));

// Mock for IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe() {
    return null;
  }
  unobserve() {
    return null;
  }
  disconnect() {
    return null;
  }
};

// Mock for ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor(callback) {
    this.callback = callback;
  }
  observe() {
    return null;
  }
  unobserve() {
    return null;
  }
  disconnect() {
    return null;
  }
};

// Mock para window.URL.createObjectURL
global.URL.createObjectURL = jest.fn(() => 'mock-url');
global.URL.revokeObjectURL = jest.fn();

// Mock para fetch
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(''),
    blob: () => Promise.resolve(new Blob()),
    arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
    formData: () => Promise.resolve(new FormData()),
    ok: true,
    status: 200,
    statusText: 'OK',
    headers: new Headers(),
  })
);
