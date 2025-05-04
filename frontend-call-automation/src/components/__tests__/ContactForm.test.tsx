import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { render } from "../../__tests__/utils";
import { ContactForm } from "../ContactForm";

import { Contact } from "@/types/contact";

// Mock de las funciones de callback
const mockOnSubmit = jest.fn();
const mockOnCancel = jest.fn();

describe("ContactForm Component", () => {
  // Datos de ejemplo para las pruebas
  const mockContact: Contact = {
    id: "1",
    name: "Juan Pérez",
    phone_number: "+1234567890",
    email: "juan@example.com",
    notes: "Cliente importante",
    tags: ["cliente", "vip"],
    created_at: "2023-01-01T00:00:00.000Z",
    updated_at: "2023-01-01T00:00:00.000Z",
    status: "active",
  };

  // Configuración para renderizar el formulario de creación
  const renderCreateForm = () => {
    return render(
      <ContactForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        isLoading={false}
      />
    );
  };

  // Configuración para renderizar el formulario de edición
  const renderEditForm = () => {
    return render(
      <ContactForm
        contact={mockContact}
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        isLoading={false}
      />
    );
  };

  // Configuración para renderizar el formulario en estado de carga
  const renderLoadingForm = () => {
    return render(
      <ContactForm
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        isLoading={true}
      />
    );
  };

  beforeEach(() => {
    // Limpiar los mocks antes de cada prueba
    jest.clearAllMocks();
  });

  it("renderiza correctamente el formulario de creación", () => {
    renderCreateForm();

    // Verificar que se muestre el título correcto
    expect(screen.getByText("Nuevo Contacto")).toBeInTheDocument();

    // Verificar que los campos estén presentes usando roles y accesibilidad
    expect(
      screen.getByRole("textbox", { name: /nombre/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /teléfono/i })
    ).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: /email/i })).toBeInTheDocument();

    // Verificar que los botones estén presentes
    expect(
      screen.getByRole("button", { name: /cancelar/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /guardar contacto/i })
    ).toBeInTheDocument();
  });

  it("renderiza correctamente el formulario de edición con datos", () => {
    renderEditForm();

    // Verificar que se muestre el título correcto
    expect(screen.getByText("Editar Contacto")).toBeInTheDocument();

    // Verificar que los campos tengan los valores correctos usando roles
    expect(screen.getByRole("textbox", { name: /nombre/i })).toHaveValue(
      "Juan Pérez"
    );
    expect(screen.getByRole("textbox", { name: /teléfono/i })).toHaveValue(
      "+1234567890"
    );
    expect(screen.getByRole("textbox", { name: /email/i })).toHaveValue(
      "juan@example.com"
    );

    // Verificar que se muestren las etiquetas
    expect(screen.getByText("cliente")).toBeInTheDocument();
    expect(screen.getByText("vip")).toBeInTheDocument();
  });

  it("llama a onCancel al hacer clic en el botón de cancelar", async () => {
    renderCreateForm();

    // Hacer clic en el botón de cancelar
    const cancelButton = screen.getByRole("button", { name: "Cancelar" });
    await userEvent.click(cancelButton);

    // Verificar que se haya llamado a la función onCancel
    expect(mockOnCancel).toHaveBeenCalledTimes(1);
  });

  it("muestra un indicador de carga cuando isLoading es true", () => {
    renderLoadingForm();

    // Verificar que se muestre el indicador de carga
    expect(screen.getByText("Guardando...")).toBeInTheDocument();

    // Verificar que el botón esté deshabilitado
    const submitButton = screen.getByRole("button", { name: "Guardando..." });
    expect(submitButton).toBeDisabled();
  });

  it("permite agregar etiquetas", async () => {
    renderCreateForm();

    // Buscar el campo de etiquetas por su rol y nombre
    const tagInputs = screen.getAllByRole("textbox");
    const tagInput = tagInputs.find((input) =>
      input.getAttribute("placeholder")?.includes("etiqueta")
    );

    // Verificar que se haya encontrado el campo
    expect(tagInput).toBeDefined();

    if (tagInput) {
      // Agregar una etiqueta
      await userEvent.type(tagInput, "nueva-etiqueta");

      // Hacer clic en el botón de añadir (buscando por texto o aria-label)
      // Intentar encontrar el botón de diferentes maneras para mayor robustez
      let addButton;
      try {
        addButton = screen.getByRole("button", { name: /agregar/i });
      } catch (error) {
        try {
          addButton = screen.getByLabelText(/agregar etiqueta/i);
        } catch (error) {
          // Si no se encuentra por role o aria-label, buscar por test-id
          addButton = screen.getByTestId("add-tag-button"); // Using explicit data-testid for reliability
        }
      }

      expect(addButton).toBeDefined();
      await userEvent.click(addButton);

      // Verificar que se haya agregado la etiqueta
      expect(screen.getByText("nueva-etiqueta")).toBeInTheDocument();
    }
  });

  it("envía el formulario con los datos correctos", async () => {
    renderCreateForm();

    // Llenar los campos del formulario usando roles para mayor robustez
    await userEvent.type(
      screen.getByRole("textbox", { name: /nombre/i }),
      "Nuevo Contacto"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: /teléfono/i }),
      "+1234567890"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: /email/i }),
      "nuevo@example.com"
    );

    // Agregar una etiqueta
    const tagInputs = screen.getAllByRole("textbox");
    const tagInput = tagInputs.find((input) =>
      input.getAttribute("placeholder")?.includes("etiqueta")
    );

    if (tagInput) {
      await userEvent.type(tagInput, "test-tag");
      // Intentar encontrar el botón de diferentes maneras para mayor robustez
      let addButton;
      try {
        addButton = screen.getByRole("button", { name: /agregar/i });
      } catch (error) {
        try {
          addButton = screen.getByLabelText(/agregar etiqueta/i);
        } catch (error) {
          // Si no se encuentra por role o aria-label, buscar por test-id
          addButton = screen.getByTestId("add-tag-button");
        }
      }

      expect(addButton).toBeDefined();
      await userEvent.click(addButton);
    }

    // Enviar el formulario
    const submitButton = screen.getByRole("button", {
      name: /guardar contacto/i,
    });
    await userEvent.click(submitButton);

    // Verificar que se haya llamado a la función onSubmit con los datos correctos
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledTimes(1);
      expect(mockOnSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          name: "Nuevo Contacto",
          phone_number: "+1234567890",
          email: "nuevo@example.com",
          tags: ["test-tag"],
        })
      );
    });
  });
});
