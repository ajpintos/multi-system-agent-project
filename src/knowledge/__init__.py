"""
Base de conocimiento interna de Los chicos de Henry.
Cada lista contiene documentos LangChain que el agente especialista
usará como fuente de recuperación (RAG).
"""
from langchain_core.documents import Document

RRHH_DOCUMENTS = [
    Document(
        page_content=(
            "El proceso de selección de Los chicos de Henry consta de 4 etapas: "
            "1) Revisión de CV, 2) Test técnico online (48 hs), "
            "3) Entrevista con RRHH (45 min), 4) Entrevista técnica con el equipo (1 hora). "
            "El tiempo promedio del proceso completo es de 2 semanas."
        ),
        metadata={"departamento": "RRHH", "tema": "seleccion"},
    ),
    Document(
        page_content=(
            "Política de vacaciones: todos los empleados tienen 15 días hábiles de vacaciones "
            "anuales a partir del primer año. Se pueden tomar en bloques mínimos de 5 días. "
            "Las vacaciones deben solicitarse con 30 días de anticipación a través del portal HR."
        ),
        metadata={"departamento": "RRHH", "tema": "vacaciones"},
    ),
    Document(
        page_content=(
            "Beneficios del empleado en Los chicos de Henry: prepaga médica (OSDE 210), "
            "bono anual por performance (hasta 15% del salario), trabajo remoto 3 días por semana, "
            "presupuesto de USD 500/año para capacitación, acceso a plataformas de e-learning."
        ),
        metadata={"departamento": "RRHH", "tema": "beneficios"},
    ),
    Document(
        page_content=(
            "Onboarding: el proceso de incorporación dura 2 semanas. La primera semana incluye "
            "presentación del equipo, accesos a sistemas y lectura de documentación. "
            "La segunda semana incluye tareas guiadas con un buddy asignado. "
            "El empleado recibe el equipamiento el primer día."
        ),
        metadata={"departamento": "RRHH", "tema": "onboarding"},
    ),
]

TECH_DOCUMENTS = [
    Document(
        page_content=(
            "Stack tecnológico de Los chicos de Henry: Backend en Python (FastAPI), "
            "Frontend en React + TypeScript, base de datos PostgreSQL y Redis para caché. "
            "Infraestructura en AWS (ECS, RDS, ElastiCache). CI/CD con GitHub Actions. "
            "Monitoreo con Datadog."
        ),
        metadata={"departamento": "Tech", "tema": "stack"},
    ),
    Document(
        page_content=(
            "Proceso de deployment: los deploys a producción se realizan los martes y jueves. "
            "Se requiere al menos 2 approvals en el PR, suite de tests en verde al 100% "
            "y revisión del Tech Lead. Los hotfixes pueden deployarse cualquier día "
            "con aprobación del CTO."
        ),
        metadata={"departamento": "Tech", "tema": "deployment"},
    ),
    Document(
        page_content=(
            "Guías de código: se usa ruff para linting y formatting con line-length=120. "
            "Toda función pública debe tener docstring. Los commits siguen Conventional Commits. "
            "Las ramas siguen el patrón feature/*, bugfix/*, hotfix/*. "
            "Code coverage mínimo del 80%."
        ),
        metadata={"departamento": "Tech", "tema": "guias_codigo"},
    ),
    Document(
        page_content=(
            "Infraestructura y logging: el logging se realiza con structlog y se centraliza en "
            "CloudWatch. Las variables de entorno se gestionan con AWS Secrets Manager. "
            "El sistema de logging usa niveles INFO, WARNING y ERROR con formato JSON en producción."
        ),
        metadata={"departamento": "Tech", "tema": "infraestructura"},
    ),
]

MARKETING_DOCUMENTS = [
    Document(
        page_content=(
            "Canales de marketing activos: LinkedIn (principal para B2B, 15 K seguidores), "
            "Newsletter semanal (8 K suscriptores, tasa de apertura 32%), "
            "Blog técnico (20 K visitas/mes), Google Ads (presupuesto USD 3 K/mes), "
            "eventos y webinars mensuales."
        ),
        metadata={"departamento": "Marketing", "tema": "canales"},
    ),
    Document(
        page_content=(
            "Métricas clave de campaña: CTR promedio en LinkedIn 2,3%, costo por lead USD 45, "
            "tasa de conversión lead-a-cliente 8%, NPS actual 72. "
            "Las campañas se evalúan mensualmente con OKRs específicos por canal."
        ),
        metadata={"departamento": "Marketing", "tema": "metricas"},
    ),
    Document(
        page_content=(
            "Buyer persona principal — 'Tech Leader Tomás': CTO o VP de Ingeniería, "
            "empresa mediana (50–500 empleados), industria fintech o retail. "
            "Pain principal: escalar el equipo técnico rápidamente. "
            "Presupuesto de decisión USD 50 K–200 K/año."
        ),
        metadata={"departamento": "Marketing", "tema": "buyer_persona"},
    ),
    Document(
        page_content=(
            "Presupuesto de marketing Q1 2026: total USD 45 K. "
            "Distribución: 40% digital (Google/LinkedIn Ads), 25% eventos y sponsorships, "
            "20% contenido (diseño, redacción), 15% herramientas y tecnología (HubSpot, Canva Pro)."
        ),
        metadata={"departamento": "Marketing", "tema": "presupuesto"},
    ),
]

FINANZAS_DOCUMENTS = [
    Document(
        page_content=(
            "Proceso de pagos a proveedores: las facturas deben cargarse en el portal de proveedores "
            "al menos 10 días antes del vencimiento. Los pagos se procesan los días 15 y 30 de cada mes. "
            "Para montos mayores a USD 10 K se requiere aprobación del CFO."
        ),
        metadata={"departamento": "Finanzas", "tema": "pagos_proveedores"},
    ),
    Document(
        page_content=(
            "Política de gastos: los empleados pueden realizar gastos con tarjeta corporativa "
            "hasta USD 500 sin aprobación previa. Entre USD 500 y USD 2 000 requiere aprobación "
            "del manager. Más de USD 2 000 requiere aprobación del CFO. "
            "Los gastos deben justificarse con factura dentro de 5 días hábiles."
        ),
        metadata={"departamento": "Finanzas", "tema": "gastos"},
    ),
    Document(
        page_content=(
            "Facturación a clientes: las facturas se emiten el último día del mes por los servicios "
            "prestados. El plazo de pago estándar es de 30 días netos. "
            "Los clientes con pagos atrasados reciben un recargo del 2% mensual. "
            "El área de Finanzas envía recordatorios automáticos a los 15 días de vencido."
        ),
        metadata={"departamento": "Finanzas", "tema": "facturacion"},
    ),
    Document(
        page_content=(
            "Presupuesto anual 2026: ingresos proyectados USD 2,1 M, costos operativos USD 1,4 M, "
            "EBITDA objetivo 33%. El presupuesto se revisa trimestralmente. "
            "Las solicitudes de presupuesto adicional deben presentarse antes del día 20 "
            "de cada trimestre."
        ),
        metadata={"departamento": "Finanzas", "tema": "presupuesto"},
    ),
]
