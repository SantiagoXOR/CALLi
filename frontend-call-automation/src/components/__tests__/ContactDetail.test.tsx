import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { render } from "../../__tests__/utils";
import { ContactDetail } from "../ContactDetail";

// Mock de las funciones de callback
const mockOnEdit = jest.fn();
const mockOnBack = jest.fn();

// Mock para useGetContact
jest.mock("@/services/contactService", () => ({
  useGetContact: jest.fn(() => ({
    data: {
      id: "1",
      name: "Juan Pérez",
      phone_number: "+1234567890",
      email: "juan@example.com",
      notes: "Cliente importante",
      tags: ["cliente", "vip"],
      created_at: "2023-01-01T00:00:00.000Z",
      updated_at: "2023-01-01T00:00:00.000Z",
    },
    isLoading: false,
    error: null,
  })),
  useDeleteContact: jest.fn(() => ({
    mutateAsync: jest.fn(() => Promise.resolve({ success: true })),
    isPending: false,
  })),
}));

describe("ContactDetail Component", () => {
  // Configuración básica para cada prueba
  const renderContactDetail = (contactId: string = "1") => {
    return render(
      <ContactDetail
        contactId={contactId}
        onEdit={mockOnEdit}
        onBack={mockOnBack}
      />
    );
  };

  beforeEach(() => {
    // Limpiar los mocks antes de cada prueba
    jest.clearAllMocks();
  });

  it("renderiza correctamente y muestra los detalles del contacto", () => {
    renderContactDetail();

    // Verificar que se muestre el título
    expect(screen.getByText("Detalles del Contacto")).toBeInTheDocument();

    // Verificar que se muestren los detalles del contacto
    expect(screen.getByText("Juan Pérez")).toBeInTheDocument();
    expect(screen.getByText("+1234567890")).toBeInTheDocument();
    expect(screen.getByText("juan@example.com")).toBeInTheDocument();
    expect(screen.getByText("cliente")).toBeInTheDocument();
    expect(screen.getByText("vip")).toBeInTheDocument();
  });

  it("muestra los botones de acción (editar y eliminar)", () => {
    renderContactDetail();

    // Verificar que se muestren los botones
    expect(screen.getByRole("button", { name: /Editar/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Eliminar/i })).toBeInTheDocument();
  });

  it("llama a la función onEdit al hacer clic en el botón de editar", async () => {
    renderContactDetail();

    // Hacer clic en el botón de editar
    const editButton = screen.getByRole("button", { name: /Editar/i });
    await userEvent.click(editButton);

    // Verificar que se haya llamado a la función con el ID correcto
    expect(mockOnEdit).toHaveBeenCalledTimes(1);
    expect(mockOnEdit).toHaveBeenCalledWith("1");
  });

  it("llama a la función onBack al hacer clic en el botón de volver", async () => {
    renderContactDetail();

    // Hacer clic en el botón de volver
    const backButton = screen.getByRole("button", { name: /Volver a la lista/i });
    await userEvent.click(backButton);

    // Verificar que se haya llamado a la función
    expect(mockOnBack).toHaveBeenCalledTimes(1);
  });

  it("muestra el diálogo de confirmación al hacer clic en eliminar", async () => {
    renderContactDetail();

    // Hacer clic en el botón de eliminar
    const deleteButton = screen.getByRole("button", { name: /Eliminar/i });
    await userEvent.click(deleteButton);

    // Verificar que se muestre el diálogo de confirmación
    expect(screen.getByText("¿Estás seguro?")).toBeInTheDocument();
  });

  it("muestra un indicador de carga mientras se cargan los datos", () => {
    // Sobreescribir el mock para simular carga
    jest.mock("@/services/contactService", () => ({
      useGetContact: jest.fn(() => ({
        data: null,
        isLoading: true,
        error: null,
      })),
      useDeleteContact: jest.fn(() => ({
        mutateAsync: jest.fn(),
        isPending: false,
      })),
    }));

    renderContactDetail();

    // Verificar que se muestre el indicador de carga
    expect(screen.getByText("Cargando detalles del contacto...")).toBeInTheDocument();
  });
});
