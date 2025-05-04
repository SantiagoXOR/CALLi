describe('Gestión de Campañas', () => {
  beforeEach(() => {
    // Visitar la página de campañas
    cy.visit('/campaigns');

    // Esperar a que la página cargue completamente
    cy.get('h1').contains('Campañas').should('be.visible');
  });

  it('muestra la lista de campañas', () => {
    // Verificar que se muestre la tabla de campañas
    cy.get('table').should('exist');

    // Verificar que se muestren las columnas correctas
    cy.get('th').contains('Nombre').should('be.visible');
    cy.get('th').contains('Estado').should('be.visible');
    cy.get('th').contains('Fecha de inicio').should('be.visible');
  });

  it('permite crear una nueva campaña', () => {
    // Hacer clic en el botón de nueva campaña
    cy.get('button').contains('Nueva Campaña').click();

    // Verificar que se muestre el formulario de creación
    cy.get('h2').contains('Nueva Campaña').should('be.visible');

    // Llenar el formulario - Paso 1: Información básica
    cy.get('input[name="name"]').type('Campaña de Prueba');
    cy.get('textarea[name="description"]').type('Descripción de prueba');

    // Avanzar al siguiente paso
    cy.get('button').contains('Siguiente').click();

    // Paso 2: Seleccionar contactos
    cy.get('button').contains('Seleccionar Contactos').click();

    // Seleccionar algunos contactos
    cy.get('input[type="checkbox"]').first().check();
    cy.get('button').contains('Añadir Seleccionados').click();

    // Avanzar al siguiente paso
    cy.get('button').contains('Siguiente').click();

    // Paso 3: Configurar script
    cy.get('textarea[name="script_template"]').type('Hola {name}, te llamamos de la empresa para ofrecerte nuestros servicios.');

    // Avanzar al siguiente paso
    cy.get('button').contains('Siguiente').click();

    // Paso 4: Configurar programación
    cy.get('input[name="schedule_start"]').type('2025-01-01');
    cy.get('input[name="schedule_end"]').type('2025-12-31');
    cy.get('input[name="calling_hours_start"]').type('09:00');
    cy.get('input[name="calling_hours_end"]').type('18:00');

    // Crear la campaña
    cy.get('button').contains('Crear Campaña').click();

    // Verificar que se vuelva a la lista de campañas
    cy.get('h1').contains('Campañas').should('be.visible');

    // Verificar que se muestre la nueva campaña
    cy.contains('Campaña de Prueba').should('be.visible');
  });

  it('permite ver los detalles de una campaña', () => {
    // Hacer clic en el botón de ver detalles de la primera campaña
    cy.get('button[title="Ver detalles"]').first().click();

    // Verificar que se muestre la vista de detalle
    cy.get('h2').contains('Detalles de la Campaña').should('be.visible');

    // Verificar que se muestren los detalles de la campaña
    cy.get('h3').should('exist');
    cy.get('button').contains('Editar').should('be.visible');
    cy.get('button').contains('Eliminar').should('be.visible');

    // Volver a la lista
    cy.get('button').contains('Volver a la lista').click();

    // Verificar que se vuelva a la lista de campañas
    cy.get('h1').contains('Campañas').should('be.visible');
  });

  it('permite editar una campaña', () => {
    // Hacer clic en el botón de editar de la primera campaña
    cy.get('button[title="Editar"]').first().click();

    // Verificar que se muestre el formulario de edición
    cy.get('h2').contains('Editar Campaña').should('be.visible');

    // Modificar el nombre
    cy.get('input[name="name"]').clear().type('Campaña Actualizada');

    // Guardar los cambios
    cy.get('button').contains('Guardar Cambios').click();

    // Verificar que se vuelva a la lista de campañas
    cy.get('h1').contains('Campañas').should('be.visible');

    // Verificar que se muestre la campaña actualizada
    cy.contains('Campaña Actualizada').should('be.visible');
  });

  it('permite eliminar una campaña', () => {
    // Obtener el nombre de la primera campaña
    cy.get('td').eq(0).invoke('text').as('campaignName');

    // Hacer clic en el botón de eliminar de la primera campaña
    cy.get('button[title="Eliminar"]').first().click();

    // Confirmar la eliminación
    cy.get('button').contains('Eliminar').click();

    // Verificar que se muestre un mensaje de éxito
    cy.contains('Campaña eliminada').should('be.visible');

    // Verificar que la campaña ya no aparezca en la lista
    cy.get('@campaignName').then((campaignName) => {
      cy.contains(campaignName.toString()).should('not.exist');
    });
  });

  it('permite filtrar campañas por estado', () => {
    // Seleccionar el filtro de estado
    cy.get('select').select('active');

    // Verificar que se filtren los resultados
    cy.get('td').contains('Activa').should('be.visible');

    // Cambiar el filtro
    cy.get('select').select('draft');

    // Verificar que se filtren los resultados
    cy.get('td').contains('Borrador').should('be.visible');
  });
});
