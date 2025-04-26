import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CampaignForm } from '../CampaignForm';
import { toast } from 'sonner';

// Mock de las dependencias
jest.mock('sonner', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
  },
}));

describe('CampaignForm', () => {
  const mockOnSubmit = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  it('renderiza correctamente', () => {
    render(<CampaignForm onSubmit={mockOnSubmit} isLoading={false} />);
    
    // Verificar que los campos principales estén presentes
    expect(screen.getByLabelText(/nombre de la campaña/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/descripción/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/estado/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/plantilla de script/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/fecha de inicio/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/fecha de fin/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/máximo de reintentos/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/retraso entre reintentos/i)).toBeInTheDocument();
    
    // Verificar que el botón de envío esté presente
    expect(screen.getByRole('button', { name: /guardar campaña/i })).toBeInTheDocument();
  });
  
  it('muestra errores de validación cuando se envía el formulario con campos requeridos vacíos', async () => {
    render(<CampaignForm onSubmit={mockOnSubmit} isLoading={false} />);
    
    // Borrar el campo de nombre (que es requerido)
    const nameInput = screen.getByLabelText(/nombre de la campaña/i);
    userEvent.clear(nameInput);
    
    // Enviar el formulario
    const submitButton = screen.getByRole('button', { name: /guardar campaña/i });
    userEvent.click(submitButton);
    
    // Verificar que se muestre el mensaje de error
    await waitFor(() => {
      expect(screen.getByText(/el nombre debe tener al menos 3 caracteres/i)).toBeInTheDocument();
    });
    
    // Verificar que no se haya llamado a onSubmit
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
  
  it('llama a onSubmit con los datos correctos cuando el formulario es válido', async () => {
    render(<CampaignForm onSubmit={mockOnSubmit} isLoading={false} />);
    
    // Llenar el formulario con datos válidos
    const nameInput = screen.getByLabelText(/nombre de la campaña/i);
    userEvent.clear(nameInput);
    userEvent.type(nameInput, 'Campaña de Prueba');
    
    const descriptionInput = screen.getByLabelText(/descripción/i);
    userEvent.type(descriptionInput, 'Esta es una campaña de prueba');
    
    // Enviar el formulario
    const submitButton = screen.getByRole('button', { name: /guardar campaña/i });
    userEvent.click(submitButton);
    
    // Verificar que se haya llamado a onSubmit con los datos correctos
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledTimes(1);
      expect(mockOnSubmit).toHaveBeenCalledWith(expect.objectContaining({
        name: 'Campaña de Prueba',
        description: 'Esta es una campaña de prueba',
      }));
    });
    
    // Verificar que se muestre el mensaje de éxito
    expect(toast.success).toHaveBeenCalledWith('Campaña guardada exitosamente');
  });
  
  it('muestra un indicador de carga cuando isLoading es true', () => {
    render(<CampaignForm onSubmit={mockOnSubmit} isLoading={true} />);
    
    // Verificar que se muestre el indicador de carga
    expect(screen.getByText(/enviando/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /enviando/i })).toBeDisabled();
  });
  
  it('valida que la fecha de fin sea posterior a la fecha de inicio', async () => {
    render(<CampaignForm onSubmit={mockOnSubmit} isLoading={false} />);
    
    // Establecer fecha de inicio posterior a la fecha de fin
    const startDateInput = screen.getByLabelText(/fecha de inicio/i);
    const endDateInput = screen.getByLabelText(/fecha de fin/i);
    
    fireEvent.change(startDateInput, { target: { value: '2025-12-31' } });
    fireEvent.change(endDateInput, { target: { value: '2025-01-01' } });
    
    // Enviar el formulario
    const submitButton = screen.getByRole('button', { name: /guardar campaña/i });
    userEvent.click(submitButton);
    
    // Verificar que se muestre el mensaje de error
    await waitFor(() => {
      expect(screen.getByText(/la fecha de fin debe ser posterior a la fecha de inicio/i)).toBeInTheDocument();
    });
    
    // Verificar que no se haya llamado a onSubmit
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
