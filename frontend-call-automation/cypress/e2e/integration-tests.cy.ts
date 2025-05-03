describe('Pruebas de Integración del Sistema', () => {
  beforeEach(() => {
    // Visitar la página de inicio y hacer login
    cy.visit('/');
    cy.get('button').contains('Iniciar Sesión').click();
    cy.get('input[name="email"]').type('test@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    // Verificar que el login fue exitoso
    cy.get('h1').contains('Dashboard').should('be.visible');
  });

  describe('Flujo Completo de Campaña', () => {
    it('crea una campaña, añade contactos y programa una llamada', () => {
      // 1. Crear contactos
      cy.get('a').contains('Contactos').click();
      cy.get('button').contains('Nuevo Contacto').click();
      cy.get('input[name="name"]').type('Juan Pérez');
      cy.get('input[name="phone"]').type('+5491123456789');
      cy.get('input[name="email"]').type('juan@example.com');
      cy.get('button').contains('Guardar').click();

      // Verificar que el contacto se creó correctamente
      cy.contains('Contacto creado correctamente').should('be.visible');
      cy.contains('Juan Pérez').should('be.visible');

      // 2. Crear una campaña
      cy.get('a').contains('Campañas').click();
      cy.get('button').contains('Nueva Campaña').click();

      // Paso 1: Información básica
      cy.get('input[name="name"]').type('Campaña de Prueba de Integración');
      cy.get('textarea[name="description"]').type('Descripción de la campaña de prueba');
      cy.get('button').contains('Siguiente').click();

      // Paso 2: Seleccionar contactos
      cy.get('button').contains('Seleccionar Contactos').click();
      cy.contains('Juan Pérez').parent().find('input[type="checkbox"]').check();
      cy.get('button').contains('Añadir Seleccionados').click();
      cy.get('button').contains('Siguiente').click();

      // Paso 3: Configurar script
      cy.get('textarea[name="script_template"]').type('Hola {name}, te llamamos para informarte sobre nuestros nuevos servicios.');
      cy.get('button').contains('Siguiente').click();

      // Paso 4: Configurar programación
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomorrowFormatted = tomorrow.toISOString().split('T')[0];

      cy.get('input[name="schedule_start"]').type(tomorrowFormatted);
      cy.get('input[name="schedule_end"]').type(tomorrowFormatted);
      cy.get('input[name="calling_hours_start"]').type('09:00');
      cy.get('input[name="calling_hours_end"]').type('18:00');
      cy.get('button').contains('Crear Campaña').click();

      // Verificar que la campaña se creó correctamente
      cy.contains('Campaña creada correctamente').should('be.visible');
      cy.contains('Campaña de Prueba de Integración').should('be.visible');

      // 3. Ver detalles de la campaña
      cy.contains('Campaña de Prueba de Integración').click();
      cy.get('h2').contains('Detalles de la Campaña').should('be.visible');
      cy.contains('Contactos: 1').should('be.visible');

      // 4. Verificar que la llamada está programada
      cy.get('a').contains('Llamadas').click();
      cy.contains('Juan Pérez').should('be.visible');
      cy.contains('Programada').should('be.visible');
    });
  });

  describe('Integración con Servicios Externos', () => {
    it('verifica la integración con Twilio', () => {
      // Navegar a la página de configuración
      cy.get('a').contains('Configuración').click();
      cy.get('button').contains('Probar Conexión Twilio').click();

      // Verificar que la conexión es exitosa
      cy.contains('Conexión con Twilio exitosa').should('be.visible');
    });

    it('verifica la integración con ElevenLabs', () => {
      // Navegar a la página de configuración
      cy.get('a').contains('Configuración').click();
      cy.get('button').contains('Probar Conexión ElevenLabs').click();

      // Verificar que la conexión es exitosa
      cy.contains('Conexión con ElevenLabs exitosa').should('be.visible');
    });
  });

  describe('Escenarios de Error', () => {
    it('maneja correctamente errores de validación', () => {
      // Intentar crear un contacto con datos inválidos
      cy.get('a').contains('Contactos').click();
      cy.get('button').contains('Nuevo Contacto').click();
      cy.get('input[name="name"]').type('Test');
      cy.get('input[name="phone"]').type('123'); // Número inválido
      cy.get('button').contains('Guardar').click();

      // Verificar que se muestra el error
      cy.contains('Número de teléfono inválido').should('be.visible');
    });

    it('maneja correctamente errores de servidor', () => {
      // Simular error de servidor al crear una campaña
      cy.intercept('POST', '**/api/campaigns', {
        statusCode: 500,
        body: {
          error: 'Error interno del servidor'
        }
      }).as('createCampaign');

      // Intentar crear una campaña
      cy.get('a').contains('Campañas').click();
      cy.get('button').contains('Nueva Campaña').click();
      cy.get('input[name="name"]').type('Campaña con Error');
      cy.get('textarea[name="description"]').type('Esta campaña generará un error');
      cy.get('button').contains('Siguiente').click();
      cy.get('button').contains('Siguiente').click(); // Saltar selección de contactos
      cy.get('textarea[name="script_template"]').type('Script de prueba');
      cy.get('button').contains('Siguiente').click();

      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomorrowFormatted = tomorrow.toISOString().split('T')[0];

      cy.get('input[name="schedule_start"]').type(tomorrowFormatted);
      cy.get('input[name="schedule_end"]').type(tomorrowFormatted);
      cy.get('input[name="calling_hours_start"]').type('09:00');
      cy.get('input[name="calling_hours_end"]').type('18:00');
      cy.get('button').contains('Crear Campaña').click();

      // Verificar que se muestra el error
      cy.wait('@createCampaign');
      cy.contains('Error al crear la campaña').should('be.visible');
    });
  });

  describe('Rendimiento bajo Carga', () => {
    it('carga correctamente una lista grande de contactos', () => {
      // Simular una respuesta con muchos contactos
      cy.intercept('GET', '**/api/contacts*', {
        fixture: 'large-contacts-list.json'
      }).as('getContacts');

      // Navegar a la página de contactos
      cy.get('a').contains('Contactos').click();

      // Esperar a que se carguen los contactos
      cy.wait('@getContacts');

      // Verificar que la paginación funciona
      cy.get('[data-testid="pagination"]').should('be.visible');
      cy.get('[data-testid="pagination"]').contains('1').should('be.visible');
      cy.get('[data-testid="pagination"]').contains('2').click();

      // Verificar que se cargó la segunda página
      cy.url().should('include', 'page=2');
    });
  });
});
