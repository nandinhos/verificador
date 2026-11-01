# MCP HTTP: `url` canônica vs `serverUrl` legada — redundância ou compatibilidade poliglota?

## Metadados

- **Data de início:** 2026-10-31
- **Tema / palavras-chave:** MCP, Streamable HTTP, `url`, `serverUrl`, Muse, Antigravity, dev-memory, dialeto de schema
- **Origem:** reflexão própria a partir de configuração real do hub dev-memory
- **Fonte(s):** config ativa Muse (`~/.config/muse/settings.json`), config ativa Antigravity (`~/.gemini/antigravity/mcp_config.json`), manual interno Antigravity `mcp_servers.md:59-71` (citado pelo harness Antigravity)
- **Status:** Concluída

## Contexto

Ao instalar o hub de memória dev-memory (MCP remoto HTTP) no Muse, a entrada `mcpServers.dev-memory` ficou com duas chaves de mesmo valor:

```json
"dev-memory": {
  "type": "http",
  "serverUrl": "https://devmemory.fssdev.com.br/api/mcp",
  "url": "https://devmemory.fssdev.com.br/api/mcp",
  "headers": { "Authorization": "Bearer ***" }
}
```

A revisão local removeu `serverUrl` por aparente redundância. A pergunta levada a outro harness (Google Antigravity / agy): era redundância real ou quebra de compatibilidade? Qual chave cada cliente lê — e a dupla era erro ou defesa?

## Verificação de fontes

| Fonte | Status | Como foi verificada |
|---|---|---|
| Muse lê `url` (só `url` basta) | `OBSERVED` | Teste A/B local: removido `serverUrl`, `initialize` → HTTP 200 (`dev-memory-mcp 1.0.0`), `tools/list` → HTTP 200 |
| Antigravity: `url` canônica (spec 2025-03-26), `serverUrl` aceita como legado | `OBSERVED` (reportado) | Citação do manual interno `mcp_servers.md:59-71` trazida pelo harness Antigravity; não relida localmente neste repo |
| Antigravity `stitch` só com `serverUrl` conecta | `OBSERVED` (reportado) | Config ativa `~/.gemini/antigravity/mcp_config.json` citada pelo Antigravity; prova que a chave legada ainda é viva em cliente real |
| Cloudflare 1010 em probe inicial | `OBSERVED` | Probe com User-Agent default do Python → HTTP 403 `browser_signature_banned`; com UA comum → HTTP 200. Falso-negativo de conectividade, não queda do servidor |

## Análise

Núcleo sólido: `url` é a chave canônica do transporte Streamable HTTP. No Muse, `serverUrl` é ignorada — removê-la daquele arquivo foi correto e sem efeito colateral.

Nuance: a dupla não era erro de quem configurou. Como o mesmo bloco de setup do hub é compartilhado entre harnesses de gerações diferentes (rascunhos antigos com `serverUrl`, clientes modernos com `url`), declarar ambas é uma configuração defensiva "poliglota": cada cliente lê a sua chave e nenhum falha por dialeto de schema. O risco só aparece se os valores divergirem — cada cliente conectaria num endpoint diferente sem erro visível.

Marcação epistêmica: o *efeito* poliglota está provado (ambas funcionam, em clientes distintos). A *intenção* original de quem montou o template é `INFERRED` — plausível, não demonstrada.

| Cliente / Harness | Chave efetiva | `serverUrl` | Só `url` |
|---|---|---|---|
| Muse | `url` | Ignorada | Funciona (provado A/B) |
| Antigravity (agy) | `url` | Fallback legado aceito | Funciona (documentado) |
| Claude Code CLI | `url` | Geralmente não lê | Funciona (reportado) |

## Reflexões e inferências

- Redundância aparente em config multi-harness deve ser tratada como hipótese, não como fato: antes de "limpar", testar A/B (só `url` / só `serverUrl` / ambas divergentes). O teste com valores divergentes revela a chave efetiva sem ambiguidade.
- Diagnóstico de conectividade MCP precisa separar camadas: DNS/TLS, borda (Cloudflare/WAF por User-Agent), auth (Bearer) e handshake (`initialize`/`tools/list`). Um 403 de borda não é servidor fora nem token inválido.

## Anexos

- Handoff efêmero gerado nesta sessão (texto no histórico do chat, 2026-10-31) — pergunta levada ao Antigravity e resposta recebida.

## Fechamento (contrato de resposta)

```
Resultado:   `url` é canônica; `serverUrl` é legado ainda aceito. Remover no Muse: correto. Em bloco compartilhado entre harnesses: manter ambas é defesa poliglota, não redundância.
Evidências:
  OBSERVED:  A/B no Muse (só `url` → HTTP 200); manual Antigravity citado (url canônica + serverUrl legado); stitch só com serverUrl operante (reportado); 403 Cloudflare 1010 por UA default falsificando queda.
  INFERRED:  Intenção poliglota defensiva de quem montou o template compartilhado.
  UNKNOWN:   Comportamento de outros clientes MCP não testados (cada um exige seu A/B).
Confiança:   ALTA — dois harnesses independentes convergem, com teste executável local.
```
