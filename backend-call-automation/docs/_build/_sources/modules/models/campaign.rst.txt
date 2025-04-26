Modelo Campaign
===============

.. automodule:: app.models.campaign
   :members:
   :undoc-members:
   :show-inheritance:

Descripción
-----------

El modelo Campaign representa una campaña de llamadas automatizadas en el sistema.

Estructura
----------

.. autoclass:: app.models.campaign.CampaignBase
   :members:
   :inherited-members:

.. autoclass:: app.models.campaign.CampaignCreate
   :members:
   :inherited-members:

.. autoclass:: app.models.campaign.CampaignUpdate
   :members:
   :inherited-members:

.. autoclass:: app.models.campaign.Campaign
   :members:
   :inherited-members:

Estados
-------

.. autoclass:: app.models.campaign.CampaignStatus
   :members:

Validaciones
------------

- **schedule_end**: Debe ser posterior a schedule_start
- **calling_hours_end**: Debe ser posterior a calling_hours_start
- **max_retries**: Debe ser >= 0
- **retry_delay_minutes**: Debe ser >= 0
- **pending_calls**: Debe ser >= 0
- **total_calls**: Debe ser >= 0
- **successful_calls**: Debe ser >= 0
- **failed_calls**: Debe ser >= 0

Ejemplo
-------

.. code-block:: python

   from datetime import datetime, timedelta
   from uuid import UUID
   from app.models.campaign import CampaignCreate

   campaign = CampaignCreate(
       name="Campaña de Ventas Q2",
       description="Campaña para promocionar nuevos productos",
       status="draft",
       schedule_start=datetime.now(),
       schedule_end=datetime.now() + timedelta(days=30),
       contact_list_ids=[UUID("123e4567-e89b-12d3-a456-426614174000")],
       script_template="Hola {nombre}, te llamamos de...",
       max_retries=3,
       retry_delay_minutes=60,
       calling_hours_start="09:00",
       calling_hours_end="18:00"
   )
