import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { render } from "../../__tests__/utils";
import { ContactImport } from "../ContactImport";

// Mock para toast
const mockToast = {
  error: jest.fn(),
  success: jest.fn(),
};

// Mock de sonner
jest.mock("sonner", () => ({
  toast: mockToast,
}));

// Mock de las funciones de callback
const mockOnCancel = jest.fn();
const mockOnSuccess = jest.fn();

describe("ContactImport Component", () => {
  // Configuración básica para cada prueba
  const renderContactImport = () => {
    return render(
      <ContactImport onCancel={mockOnCancel} onSuccess={mockOnSuccess} />
    );
  };

  beforeEach(() => {
    // Limpiar los mocks antes de cada prueba
    jest.clearAllMocks();
  });

  it("renderiza correctamente el componente de importación", () => {
    renderContactImport();

    // Verificar que se muestre el título
    expect(screen.getByText("Importar Contactos")).toBeInTheDocument();

    // Verificar que se muestre la descripción
    expect(
      screen.getByText(/Importa contactos desde un archivo CSV/i)
    ).toBeInTheDocument();

    // Verificar que se muestre el botón de seleccionar archivo
    expect(screen.getByLabelText("Archivo CSV")).toBeInTheDocument();
  });

  it("muestra instrucciones para el formato del archivo", () => {
    renderContactImport();

    // Verificar que se muestren las instrucciones
    expect(
      screen.getByText(/El archivo debe tener las siguientes columnas/i)
    ).toBeInTheDocument();
    expect(screen.getByText(/nombre/i)).toBeInTheDocument();
    expect(screen.getByText(/teléfono/i)).toBeInTheDocument();
  });

  it("llama a la función onCancel al hacer clic en el botón de cancelar", async () => {
    renderContactImport();

    // Hacer clic en el botón de cancelar
    const cancelButton = screen.getByRole("button", { name: "Cancelar" });
    await userEvent.click(cancelButton);

    // Verificar que se haya llamado a la función
    expect(mockOnCancel).toHaveBeenCalledTimes(1);
  });

  it("muestra un mensaje de error al intentar importar sin seleccionar un archivo", async () => {
    renderContactImport();

    // Hacer clic en el botón de importar sin seleccionar un archivo
    const importButton = screen.getByRole("button", { name: /Importar/i });
    await userEvent.click(importButton);

    // Verificar que se muestre un mensaje de error
    expect(mockToast.error).toHaveBeenCalledWith(
      "Por favor, selecciona un archivo CSV"
    );
  });

  it("permite seleccionar un archivo CSV", async () => {
    renderContactImport();

    // Crear un archivo CSV de prueba
    const file = new File(["name,phone,email"], "contacts.csv", {
      type: "text/csv",
    });

    // Seleccionar el archivo
    const fileInput = screen.getByLabelText("Archivo CSV");
    await userEvent.upload(fileInput, file);

    // Verificar que se muestre el nombre del archivo
    expect(screen.getByText("contacts.csv")).toBeInTheDocument();
  });

  it("muestra un mensaje de error si el archivo no es CSV", async () => {
    renderContactImport();

    // Crear un archivo no CSV
    const file = new File(["test"], "test.txt", { type: "text/plain" });

    // Seleccionar el archivo
    const fileInput = screen.getByLabelText("Archivo CSV");
    await userEvent.upload(fileInput, file);

    // Verificar que se muestre un mensaje de error
    expect(mockToast.error).toHaveBeenCalledWith(
      "Por favor, selecciona un archivo CSV válido"
    );
  });

  it("muestra botones para importar y cancelar", () => {
    renderContactImport();

    // Verificar que se muestren los botones
    expect(
      screen.getByRole("button", { name: "Importar" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Cancelar" })
    ).toBeInTheDocument();
  });

  it("deshabilita el botón de importar cuando está cargando", () => {
    render(
      <ContactImport
        onCancel={mockOnCancel}
        onSuccess={mockOnSuccess}
        isLoading={true}
      />
    );

    // Verificar que el botón esté deshabilitado
    const importButton = screen.getByRole("button", { name: "Importando..." });
    expect(importButton).toBeDisabled();
  });
});
