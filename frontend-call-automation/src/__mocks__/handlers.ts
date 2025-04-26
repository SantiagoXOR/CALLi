import { rest } from "msw";

// Datos de ejemplo para las pruebas
const mockContacts = [
  {
    id: "1",
    name: "Juan Pérez",
    phone_number: "+1234567890",
    email: "juan@example.com",
    notes: "Cliente importante",
    tags: ["cliente", "vip"],
    created_at: "2023-01-01T00:00:00.000Z",
    updated_at: "2023-01-01T00:00:00.000Z",
    status: "active",
  },
  {
    id: "2",
    name: "María García",
    phone_number: "+0987654321",
    email: "maria@example.com",
    notes: "Contacto nuevo",
    tags: ["cliente"],
    created_at: "2023-01-02T00:00:00.000Z",
    updated_at: "2023-01-02T00:00:00.000Z",
    status: "active",
  },
];

// Datos de ejemplo para campañas
const mockCampaigns = [
  {
    id: "1",
    name: "Campaña de Ventas Q1",
    description: "Campaña para el primer trimestre",
    status: "active",
    script_template: "Hola {name}, te llamamos de...",
    contact_list_ids: ["1"],
    schedule_start: "2023-01-01T00:00:00.000Z",
    schedule_end: "2023-03-31T00:00:00.000Z",
    calling_hours_start: "09:00",
    calling_hours_end: "18:00",
    max_retries: 3,
    retry_delay_minutes: 60,
    total_calls: 100,
    successful_calls: 75,
    created_at: "2022-12-15T00:00:00.000Z",
    updated_at: "2023-01-01T00:00:00.000Z",
  },
  {
    id: "2",
    name: "Campaña de Fidelización",
    description: "Campaña para clientes existentes",
    status: "draft",
    script_template: "Hola {name}, queremos agradecerte por...",
    contact_list_ids: ["2"],
    schedule_start: "2023-04-01T00:00:00.000Z",
    schedule_end: "2023-06-30T00:00:00.000Z",
    calling_hours_start: "10:00",
    calling_hours_end: "17:00",
    max_retries: 2,
    retry_delay_minutes: 120,
    total_calls: 0,
    successful_calls: 0,
    created_at: "2023-03-15T00:00:00.000Z",
    updated_at: "2023-03-15T00:00:00.000Z",
  },
];

// Handlers para interceptar las peticiones HTTP durante las pruebas
export const handlers = [
  // ===== CONTACTOS =====

  // GET /api/contacts - Obtener lista de contactos
  rest.get("*/api/contacts", (req, res, ctx) => {
    const page = Number(req.url.searchParams.get("page")) || 1;
    const limit = Number(req.url.searchParams.get("limit")) || 10;
    const search = req.url.searchParams.get("search") || "";
    const skip = Number(req.url.searchParams.get("skip")) || 0;

    let filteredContacts = [...mockContacts];

    // Aplicar filtro de búsqueda si existe
    if (search) {
      filteredContacts = filteredContacts.filter(
        (contact) =>
          contact.name.toLowerCase().includes(search.toLowerCase()) ||
          contact.email?.toLowerCase().includes(search.toLowerCase()) ||
          contact.phone_number.includes(search)
      );
    }

    // Calcular paginación
    const startIndex = skip || (page - 1) * limit;
    const endIndex = startIndex + limit;
    const paginatedContacts = filteredContacts.slice(startIndex, endIndex);

    return res(
      ctx.status(200),
      ctx.json({
        data: paginatedContacts,
        total: filteredContacts.length,
        page,
        limit,
        totalPages: Math.ceil(filteredContacts.length / limit),
      })
    );
  }),

  // GET /api/contacts/:id - Obtener un contacto por ID
  rest.get("*/api/contacts/:id", (req, res, ctx) => {
    const { id } = req.params;
    const contact = mockContacts.find((c) => c.id === id);

    if (!contact) {
      return res(
        ctx.status(404),
        ctx.json({ message: "Contacto no encontrado" })
      );
    }

    return res(ctx.status(200), ctx.json(contact));
  }),

  // POST /api/contacts - Crear un nuevo contacto
  rest.post("*/api/contacts", async (req, res, ctx) => {
    const newContact = await req.json();

    // Simular creación de contacto
    const createdContact = {
      id: String(mockContacts.length + 1),
      ...newContact,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      status: newContact.status || "active",
    };

    return res(ctx.status(201), ctx.json(createdContact));
  }),

  // PUT /api/contacts/:id - Actualizar un contacto
  rest.put("*/api/contacts/:id", async (req, res, ctx) => {
    const { id } = req.params;
    const updatedData = await req.json();
    const contactIndex = mockContacts.findIndex((c) => c.id === id);

    if (contactIndex === -1) {
      return res(
        ctx.status(404),
        ctx.json({ message: "Contacto no encontrado" })
      );
    }

    const updatedContact = {
      ...mockContacts[contactIndex],
      ...updatedData,
      updated_at: new Date().toISOString(),
    };

    return res(ctx.status(200), ctx.json(updatedContact));
  }),

  // DELETE /api/contacts/:id - Eliminar un contacto
  rest.delete("*/api/contacts/:id", (req, res, ctx) => {
    const { id } = req.params;
    const contactIndex = mockContacts.findIndex((c) => c.id === id);

    if (contactIndex === -1) {
      return res(
        ctx.status(404),
        ctx.json({ message: "Contacto no encontrado" })
      );
    }

    return res(ctx.status(200), ctx.json({ success: true }));
  }),

  // POST /api/contacts/import - Importar contactos
  rest.post("*/api/contacts/import", async (req, res, ctx) => {
    // Simular importación exitosa
    return res(
      ctx.status(200),
      ctx.json({
        imported: 5,
        errors: 1,
        total: 6,
      })
    );
  }),

  // GET /api/contacts/tags - Obtener todas las etiquetas
  rest.get("*/api/contacts/tags", (req, res, ctx) => {
    // Extraer todas las etiquetas únicas de los contactos
    const allTags = mockContacts.reduce((tags, contact) => {
      if (contact.tags && contact.tags.length > 0) {
        return [...tags, ...contact.tags];
      }
      return tags;
    }, []);

    // Eliminar duplicados
    const uniqueTags = [...new Set(allTags)];

    return res(ctx.status(200), ctx.json(uniqueTags));
  }),

  // GET /api/contacts/export - Exportar contactos
  rest.get("*/api/contacts/export", (req, res, ctx) => {
    // Simular descarga de archivo
    return res(
      ctx.status(200),
      ctx.set("Content-Type", "text/csv"),
      ctx.set("Content-Disposition", 'attachment; filename="contacts.csv"'),
      ctx.body(
        'name,phone,email,tags,notes\nJuan Pérez,+1234567890,juan@example.com,"cliente,vip",Cliente importante\nMaría García,+0987654321,maria@example.com,cliente,Contacto nuevo'
      )
    );
  }),

  // ===== CAMPAÑAS =====

  // GET /api/campaigns - Obtener lista de campañas
  rest.get("*/api/campaigns", (req, res, ctx) => {
    const page = Number(req.url.searchParams.get("page")) || 1;
    const limit = Number(req.url.searchParams.get("limit")) || 10;
    const skip = Number(req.url.searchParams.get("skip")) || 0;

    // Calcular paginación
    const startIndex = skip || (page - 1) * limit;
    const endIndex = startIndex + limit;
    const paginatedCampaigns = mockCampaigns.slice(startIndex, endIndex);

    return res(
      ctx.status(200),
      ctx.json({
        data: paginatedCampaigns,
        total: mockCampaigns.length,
      })
    );
  }),

  // GET /api/campaigns/:id - Obtener una campaña por ID
  rest.get("*/api/campaigns/:id", (req, res, ctx) => {
    const { id } = req.params;
    const campaign = mockCampaigns.find((c) => c.id === id);

    if (!campaign) {
      return res(
        ctx.status(404),
        ctx.json({ message: "Campaña no encontrada" })
      );
    }

    return res(ctx.status(200), ctx.json(campaign));
  }),

  // POST /api/campaigns - Crear una nueva campaña
  rest.post("*/api/campaigns", async (req, res, ctx) => {
    const newCampaign = await req.json();

    // Simular creación de campaña
    const createdCampaign = {
      id: String(mockCampaigns.length + 1),
      ...newCampaign,
      total_calls: 0,
      successful_calls: 0,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    return res(ctx.status(201), ctx.json(createdCampaign));
  }),

  // PUT /api/campaigns/:id - Actualizar una campaña
  rest.put("*/api/campaigns/:id", async (req, res, ctx) => {
    const { id } = req.params;
    const updatedData = await req.json();
    const campaignIndex = mockCampaigns.findIndex((c) => c.id === id);

    if (campaignIndex === -1) {
      return res(
        ctx.status(404),
        ctx.json({ message: "Campaña no encontrada" })
      );
    }

    const updatedCampaign = {
      ...mockCampaigns[campaignIndex],
      ...updatedData,
      updated_at: new Date().toISOString(),
    };

    return res(ctx.status(200), ctx.json(updatedCampaign));
  }),

  // DELETE /api/campaigns/:id - Eliminar una campaña
  rest.delete("*/api/campaigns/:id", (req, res, ctx) => {
    const { id } = req.params;
    const campaignIndex = mockCampaigns.findIndex((c) => c.id === id);

    if (campaignIndex === -1) {
      return res(
        ctx.status(404),
        ctx.json({ message: "Campaña no encontrada" })
      );
    }

    return res(ctx.status(200), ctx.json({ success: true }));
  }),

  // ===== AUTENTICACIÓN =====

  // POST /auth/login - Iniciar sesión
  rest.post("*/auth/login", async (req, res, ctx) => {
    const { email, password } = await req.json();

    // Simular autenticación exitosa
    if (email === "test@example.com" && password === "password") {
      return res(
        ctx.status(200),
        ctx.json({
          user: {
            id: "1",
            email: "test@example.com",
            name: "Usuario de Prueba",
            role: "admin",
          },
          token: "mock-jwt-token",
        })
      );
    }

    // Simular error de autenticación
    return res(
      ctx.status(401),
      ctx.json({
        message: "Credenciales inválidas",
      })
    );
  }),

  // POST /auth/register - Registrar usuario
  rest.post("*/auth/register", async (req, res, ctx) => {
    const userData = await req.json();

    // Simular registro exitoso
    return res(
      ctx.status(201),
      ctx.json({
        user: {
          id: "2",
          email: userData.email,
          name: userData.name,
          role: "user",
        },
        token: "mock-jwt-token",
      })
    );
  }),

  // GET /auth/user - Obtener usuario actual
  rest.get("*/auth/user", (req, res, ctx) => {
    // Verificar token de autenticación
    const authHeader = req.headers.get("Authorization");

    if (authHeader && authHeader.startsWith("Bearer ")) {
      return res(
        ctx.status(200),
        ctx.json({
          id: "1",
          email: "test@example.com",
          name: "Usuario de Prueba",
          role: "admin",
        })
      );
    }

    // Simular error de autenticación
    return res(
      ctx.status(401),
      ctx.json({
        message: "No autenticado",
      })
    );
  }),

  // POST /auth/logout - Cerrar sesión
  rest.post("*/auth/logout", (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        success: true,
      })
    );
  }),
];
