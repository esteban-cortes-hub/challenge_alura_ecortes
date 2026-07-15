# API de licencias de ejemplo

Este documento describe una API ficticia utilizada únicamente para demostrar el funcionamiento del asistente documental.

## Endpoint principal

El endpoint utilizado para enviar varias licencias en una sola solicitud es:

```text
/api/estructura-licencia/bulk
```

El método HTTP utilizado es:

```text
POST
```

## Autenticación

La solicitud debe incluir un token de acceso en el encabezado HTTP:

```text
Authorization: Bearer TOKEN_DE_ACCESO
```

El token no debe almacenarse directamente en el código ni publicarse en el repositorio.

## Formato de la solicitud

La API recibe un arreglo JSON con una o más licencias.

Ejemplo:

```json
[
  {
    "nombre_licencia": "Licencia de colaboración",
    "nombre_cliente": "Empresa de ejemplo",
    "rut_cliente": "12345678-9",
    "portal": "AVAYA",
    "fecha_inicio": "2026-01-01",
    "fecha_vencimiento": "2026-12-31",
    "estado_portal": "Activo"
  }
]
```

## Campos principales

### `nombre_licencia`

Nombre descriptivo de la licencia o servicio contratado.

### `nombre_cliente`

Nombre normalizado del cliente.

### `rut_cliente`

Identificador tributario del cliente.

### `portal`

Sistema desde el cual se obtuvo la licencia.

Valores de ejemplo:

* AVAYA
* MERAKI
* FORTINET

### `fecha_inicio`

Fecha inicial de vigencia de la licencia.

### `fecha_vencimiento`

Fecha en la que termina la vigencia de la licencia.

### `estado_portal`

Estado informado por el portal de origen.

## Respuesta exitosa

Una respuesta correcta puede devolver el código HTTP:

```text
200 OK
```

Ejemplo:

```json
{
  "estado": "OK",
  "procesados": 1,
  "errores": 0
}
```

## Errores posibles

### `400 Bad Request`

La solicitud contiene campos inválidos o incompletos.

### `401 Unauthorized`

El token es inválido o no fue enviado.

### `500 Internal Server Error`

Ocurrió un error inesperado durante el procesamiento.

## Recomendaciones

* Validar los campos antes del envío.
* No incluir secretos en el código.
* Registrar los errores sin exponer credenciales.
* Enviar los registros en lotes pequeños.
* Definir un tiempo máximo de espera para la solicitud.
