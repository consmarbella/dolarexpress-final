# GSC + Análisis SERP: clúster monetario "cupo dólar" (2026-10-20)

Fuentes: Google Search Console (`sc-domain:dolarexpress.cl`, 2026-07-01 → 2026-10-19, 250 queries) y SERPs Google Chile en vivo vía DataForSEO (depth 10, `gl=cl`, `lang=es`). **Este reporte es solo investigación: no se modificó ninguna página del sitio.**

## 1. Resumen GSC (16 semanas)

- **24 clics / 1.523 impresiones.** Posición media global muy dañada por cola larga de páginas doorways desindexadas/parciales (~100 queries pos 70-95).
- Clúster monetario perdido: **pos 59-79, ~570 impresiones, ~3 clics**.
- Clúster productivo actual: casa de cambio (pos 2-10).
- Marca casi nula (~15 imp).

### Queries del clúster monetario

| Query | Imp | Pos media |
|---|---|---|
| avance cupo en dolares | 102 | 64.9 |
| cambio cupo dolar | 81 | 64.6 |
| cambio cupo en dolares | 71 | 67.3 |
| cupo dolar | 44 | 66.2 |
| vender dolares | 34 | 63.8 |
| compra dolares | 39 | 5 |
| cambiar cupo de tarjeta por efectivo | 30 | 68.2 |
| avance dolares tarjeta credito | 25 | 71.4 |
| vender cupo dolar | 7 | 42.7 (2 clics, único contacto) |

### Clúster que sí funciona (referencia)

casa de cambio (pos 2.2, 3 clics), casa de cambio cerca de mi (3.4), venta dolares (5.2), compra de dolares (9.9), casa de cambio vitacura (10.2, 68 imp).

## 2. SERP en vivo: quién ocupa el top del clúster perdido

45 resultados orgánicos analizados en 5 queries. Dominios recurrentes:

| Competidor | Apariciones | Rango pos | Rol |
|---|---|---|---|
| vendercomprardolares.com | 7 | 3-9 | Programático por banco/tarjeta |
| www.ecash.cl | 5 | 10-13 | Multi-ciudad, multi-sucursal |
| girodolares.cl | 3 | 3-12 | Landing + blog legal |
| cupoendolares.cl | 3 | 7-13 | Contenido + tags |
| www.tucupodolar.cl | 2 | 2-2 | Landing direct-to-conversion |
| tucupoendolares.cl | 1 | 4 | Landing |
| vendomisdolares.cl | 1 | 3-8 | Landing FAQ |
| cupodolares.cl | 1 | 9 | Guía premium |
| Banco BICE | 1 | **2** en la query mayor | Banco directa |
| Medios (ADNradio, TVN, Cooperativa, T13, Radio Agricultura, El Destape, Perfil) | variado | 2-14 | Contenido editorial de respaldo |
| Wise, Reddit, Facebook, Instagram | variado | 4-10 | Señal de contexto |

**Lectura:** no hay un ganador único; el top-10 es un ring de 7-8 microsites peers + 1 banco + medios. Nada indica que falte autoridad de dominio masiva: falta **relevancia temática por página**.

## 3. Teardown de los 5 competidores que se repiten

### vendercomprardolares.com — el más expuesto (7/45 resultados)
Patrón programático: una URL por banco + tarjeta (`/post/cupo-dolar-tarjeta/banco-estado.php`, etc.). Cada página: listado de tarjetas con cupo USD del banco, beneficios, requisitos, cómo funciona, remoto sí/no, opiniones, bloque "Otras guías" interlinking. Headline: "Cambiar los Dólares de la Tarjeta de Crédito del Banco Estado por dinero en efectivo".

### ecash.cl — máxima cobertura local
Cookies/ciudades: Las Condes, Santiago, Maipú, Quillota, Antofagasta, Curicó, Concepción, Temuco, Valdivia (9 emails por ciudad, 15+ teléfonos). Temas: altos montos, avance online, seguridad. Está en el top-10 de casi todo, menor posición: probablemente saturado/menos enfocado por query.

### girodolares.cl — posicionamiento limpio
H1 "Cupo en dólares Chile — cómo funciona y cuánto pagan". Cubre: qué es, para qué sirve, cómo se calcula la tasa, **legalidad** ("¿Es legal convertir el cupo a pesos en Chile?"), FAQ, cotización por ciudad, oficina Providencia, "sin claves bancarias / sin tope máximo / cotización antes del compromiso", "desde 2002". Tel +56963026000.

### cupodolares.cl — guía de máxima calidad del nicho
"Guía para entender cómo funciona y qué opciones tienes". Cubre: cómo ver tu cupo, 3 formas de usarlo, legalidad, **qué pagan por el cupo**, cupo de empresa, cómo saber si es confiable. Trust: "21.000 personas ya convirtieron su cupo", "la empresa con más trayectoria del mercado". Tel/F: (22) 9589833.

### vendomisdolares.cl — FAQ-first
Todo es pregunta-respuesta: documentos necesarios, tarjeta bloqueada, operación no presencial, cómo se paga la deuda al banco, garantías remotas, cómo aumentar el plazo, tarjetas compatibles.

### Patrón común que dolarexpress.cl NO tiene en el clúster

1. **Página por banco** (todos: por banco exacto + tarjeta). En Google la intent de "cambio cupo en dolares" es inevitablemente bancaria.
2. **Legalidad + seguridad + FAQ explícita** ("¿es legal?", "¿se paga la deuda en USD al banco?", "¿pago con voucher en clp?").
3. **Qué pagan / tasas** — transparencia de spread.
4. **Confianza dura**: años operando, nº de casos, teléfono y oficina visibles, WhatsApp por ciudad.
5. **Páginas de ciudad** (ecash y giro clasifican por ciudad = casa de cambio cerca de mí).

## 4. Diagnóstico

- dolarexpress.cl compite bien en "casa de cambio" pero es **invisible en el clúster cupo**, aunque opera exactamente ese negocio.
- Con 7 líneas propias en el top-10 de la query mayor, el nicho está lleno de microsites con <10 páginas: el diferencial no es DR, es **page-level topical match** + señales de confianza.
- La pos 42.7 ya registrada en "vender cupo dolar" (2 clics) sugiere que el dominio está a saltos cortos de la zona de clics con contenidos correctos.

## 5. Recomendaciones priorizadas (propuestas — NO implementadas)

1. **P0 — Página/landings por banco**: replicar el patrón de vendercomprardolares (Banco de Chile, Estado, Santander, Edwards, BICE, Scotiabank + bancos bursátiles). Alinear título con intent: "Cambiar el cupo en dólares de [Banco] por pesos".
2. **P0 — Bloque FAQ + legalidad**: qué es, cómo se cifra el avance, cómo se paga la deuda en USD, seguridad en operación remota, tarjeta bloqueada, voucher CLP. Marcar con FAQPage JSON-LD (la infraestructura JSON-LD del sitio ya existe tras Fase 8).
3. **P1 — Transparencia de tasa**: sección/página "cuánto pagan por el cupo hoy" con tabla tipo cupodolares.cl (Santiago centro 1.195 vs óptimo 1.405 informado en needle).
4. **P1 — Señales de confianza**: años activos, casos procesados, teléfono/WhatsApp visible en hero, fotos/ubicación de oficina nivel girodolares.
5. **P2 — Ciudad**: una landing por comuna donde se opera (Partir de Las Condes/Providencia/Vitacura ya rankeando en "casa de cambio vitacura"); evitar saturación tipo ecash.
6. **P2 — Consistencia y limpieza**: mantener el patrón on-page validado de Fase 8 (.Formatting, JSON-LD, canonicals); el patrón "banco-chile" es la plantilla a extender.
7. **Monitor**: repetir este SERP pull mensual vía DataForSEO ($0.002/query) — costo insignificante para vigilar el ring y detectar cambios.

## Anexo técnico

- SERPs guardadas en `%TEMP%\opencode\serps_money_all.json` y `serp-vender-cupo-dolar.json`.
- Teardowns en `%TEMP%\opencode\competitor_pages.json` + `parse_raw_giro.json`.
- DataForSEO balance tras estas llamadas: suficiente para ~90 flattened queries más (costo $0.002/query).
- Via de scraping: Google/DDG/Brave bloquean la IP local (captcha); los free-scrapers no sirven para SERP chilena — DataForSEO es la vía estable.
