# Introducción a iTop

iTop es una plataforma de gestión de servicios de tecnología de la información y una CMDB.

Una CMDB permite registrar y relacionar elementos de configuración, como servidores, aplicaciones, dispositivos de red, contratos, organizaciones y servicios.

## Funciones principales

iTop permite gestionar:

* Organizaciones y clientes.
* Personas y contactos.
* Servidores y dispositivos.
* Aplicaciones y servicios.
* Incidentes.
* Solicitudes de usuario.
* Cambios.
* Problemas.
* Contratos y licencias.

## Integraciones

iTop puede integrarse con otros sistemas mediante servicios web y APIs REST.

Una integración puede utilizarse para:

* Crear registros.
* Consultar objetos.
* Actualizar información.
* Sincronizar inventarios.
* Enviar información desde procesos automatizados.
* Relacionar objetos de la CMDB.

## Automatización

Una herramienta de automatización como Apache Airflow puede consultar información desde sistemas externos, transformar los datos y enviarlos posteriormente a una API de iTop.

Un flujo simplificado puede ser:

```text
Sistema de origen
        ↓
Apache Airflow
        ↓
Transformación de datos
        ↓
API REST
        ↓
iTop
```

## Seguridad

Las credenciales, tokens y contraseñas utilizadas por las integraciones no deben escribirse directamente en el código fuente.

Deben almacenarse en mecanismos seguros, como variables de entorno, gestores de secretos o conexiones protegidas.
