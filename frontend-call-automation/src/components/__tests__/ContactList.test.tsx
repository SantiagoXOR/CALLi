import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { render } from "../../__tests__/utils";
import { ContactList } from "../ContactList";

// Mock de las funciones de callback
const mockOnViewContact = jest.fn();
const mockOnEditContact = jest.fn();
const mockOnCreateContact = jest.fn();

describe("ContactList Component", () => {
  // Configuración básica para cada prueba
  const renderContactList = () => {
    return render(
      <ContactList
        onViewContact={mockOnViewContact}
        onEditContact={mockOnEditContact}
        onCreateContact={mockOnCreateContact}
      />
    );
  };

  beforeEach(() => {
    // Limpiar los mocks antes de cada prueba
    jest.clearAllMocks();
  });

  it("renderiza correctamente y muestra el título", () => {
    renderContactList();

    // Verificar que se muestre el título usando un selector más específico
    const title = screen.getByRole("heading", { name: /contactos/i });
    expect(title).toBeInTheDocument();
  });

  it("muestra un botón para crear nuevo contacto", () => {
    renderContactList();

    // Verificar que se muestre el botón de nuevo contacto usando un selector más robusto
    const newButton = screen.getByRole("button", { name: /nuevo contacto/i });
    expect(newButton).toBeInTheDocument();
  });

  it("llama a la función onCreateContact al hacer clic en el botón de nuevo contacto", async () => {
    renderContactList();

    // Hacer clic en el botón de nuevo contacto usando un selector más robusto
    const newButton = screen.getByRole("button", { name: /nuevo contacto/i });
    await userEvent.click(newButton);

    // Verificar que se haya llamado a la función
    expect(mockOnCreateContact).toHaveBeenCalledTimes(1);
  });

  it("muestra un campo de búsqueda", () => {
    renderContactList();

    // Verificar que se muestre el campo de búsqueda usando un selector más robusto
    // Buscar por rol y placeholder para mayor robustez
    const searchInputs = screen.getAllByRole("textbox");
    const searchInput = searchInputs.find((input) =>
      input.getAttribute("placeholder")?.includes("Buscar")
    );
    expect(searchInput).toBeDefined();

    // Verificar que se muestre el botón de búsqueda usando un selector más específico
    const searchButton = screen.getByRole("button", { name: /buscar/i });
    expect(searchButton).toBeInTheDocument();
  });

  it("muestra un mensaje cuando hay un error al cargar los contactos", () => {
    // Simular un error en la carga
    jest.spyOn(console, "error").mockImplementation(() => {});

    renderContactList();

    // Verificar que se muestre el mensaje de error
    expect(
      screen.getByText("Error al cargar los contactos")
    ).toBeInTheDocument();

    // Restaurar console.error
    jest.restoreAllMocks();
  });

  it("muestra un indicador de carga mientras se cargan los contactos", () => {
    renderContactList();

    // Verificar que se muestre el indicador de carga
    expect(screen.getByText("Cargando contactos...")).toBeInTheDocument();
  });
});
