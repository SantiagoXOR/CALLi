describe('Gestión de Contactos', () => {
  beforeEach(() => {
    // Visitar la página de contactos
    cy.visit('/contacts');

    // Esperar a que la página cargue completamente
    cy.get('h1').contains('Contactos').should('be.visible');
  });

  it('muestra la lista de contactos', () => {
    // Verificar que se muestre la tabla de contactos
    cy.get('table').should('exist');

    // Verificar que se muestren las columnas correctas
    cy.get('th').contains('Nombre').should('be.visible');
    cy.get('th').contains('Teléfono').should('be.visible');
    cy.get('th').contains('Email').should('be.visible');
  });

  it('permite crear un nuevo contacto', () => {
    // Hacer clic en el botón de nuevo contacto
    cy.get('button').contains('Nuevo Contacto').click();

    // Verificar que se muestre el formulario de creación
    cy.get('h2').contains('Nuevo Contacto').should('be.visible');

    // Llenar el formulario
    cy.get('input[name="name"]').type('Contacto de Prueba');
    cy.get('input[name="phone_number"]').type('+1234567890');
    cy.get('input[name="email"]').type('test@example.com');

    // Agregar una etiqueta
    cy.get('input[placeholder*="etiqueta"]').type('test-tag');
    cy.get('button').contains('Añadir').click();

    // Verificar que se haya agregado la etiqueta
    cy.contains('test-tag').should('be.visible');

    // Enviar el formulario
    cy.get('button').contains('Guardar Contacto').click();

    // Verificar que se vuelva a la lista de contactos
    cy.get('h1').contains('Contactos').should('be.visible');

    // Verificar que se muestre el nuevo contacto
    cy.contains('Contacto de Prueba').should('be.visible');
  });

  it('permite ver los detalles de un contacto', () => {
    // Hacer clic en el botón de ver detalles del primer contacto
    cy.get('button[title="Ver detalles"]').first().click();

    // Verificar que se muestre la vista de detalle
    cy.get('h2').contains('Detalles del Contacto').should('be.visible');

    // Verificar que se muestren los detalles del contacto
    cy.get('h3').should('exist');
    cy.get('button').contains('Editar').should('be.visible');
    cy.get('button').contains('Eliminar').should('be.visible');

    // Volver a la lista
    cy.get('button').contains('Volver a la lista').click();

    // Verificar que se vuelva a la lista de contactos
    cy.get('h1').contains('Contactos').should('be.visible');
  });

  it('permite editar un contacto', () => {
    // Hacer clic en el botón de editar del primer contacto
    cy.get('button[title="Editar"]').first().click();

    // Verificar que se muestre el formulario de edición
    cy.get('h2').contains('Editar Contacto').should('be.visible');

    // Modificar el nombre
    cy.get('input[name="name"]').clear().type('Contacto Actualizado');

    // Enviar el formulario
    cy.get('button').contains('Guardar Contacto').click();

    // Verificar que se vuelva a la lista de contactos
    cy.get('h1').contains('Contactos').should('be.visible');

    // Verificar que se muestre el contacto actualizado
    cy.contains('Contacto Actualizado').should('be.visible');
  });

  it('permite eliminar un contacto', () => {
    // Obtener el nombre del primer contacto
    cy.get('td').eq(0).invoke('text').as('contactName');

    // Hacer clic en el botón de eliminar del primer contacto
    cy.get('button[title="Eliminar"]').first().click();

    // Confirmar la eliminación
    cy.get('button').contains('Eliminar').click();

    // Verificar que se muestre un mensaje de éxito
    cy.contains('Contacto eliminado').should('be.visible');

    // Verificar que el contacto ya no aparezca en la lista
    cy.get('@contactName').then((contactName) => {
      cy.contains(contactName.toString()).should('not.exist');
    });
  });

  it('permite buscar contactos', () => {
    // Escribir en el campo de búsqueda
    cy.get('input[placeholder*="Buscar"]').type('Juan');

    // Hacer clic en el botón de búsqueda
    cy.get('button').contains('Buscar').click();

    // Verificar que se filtren los resultados
    cy.get('td').contains('Juan').should('be.visible');

    // Limpiar la búsqueda
    cy.get('input[placeholder*="Buscar"]').clear();
    cy.get('button').contains('Buscar').click();

    // Verificar que se muestren todos los contactos
    cy.get('table tbody tr').should('have.length.at.least', 1);
  });
});
