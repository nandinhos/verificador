# Evidências brutas — mcp.ai (coletadas em 2026-11-02)

Comandos executados contra a API em produção, sem autenticação de conta.

## 1. Metadata OAuth (Authorization Server)
~~~
{"issuer":"https://api.mcp.ai","authorization_endpoint":"https://api.mcp.ai/oauth/authorize","token_endpoint":"https://api.mcp.ai/oauth/token","registration_endpoint":"https://api.mcp.ai/oauth/register","revocation_endpoint":"https://api.mcp.ai/oauth/revoke","jwks_uri":"https://api.mcp.ai/.well-known/jwks.json","response_types_supported":["code"],"subject_types_supported":["public"],"id_token_signing_alg_values_supported":["RS256"],"token_endpoint_auth_methods_supported":["none","client_secret_post"],"grant_types_supported":["authorization_code","refresh_token"],"code_challenge_methods_supported":["S256"],"scopes_supported":["mcp:read","mcp:execute","integrations:read"]}
~~~

## 2. Handshake MCP (initialize, sem autenticacao)
~~~
event: message
data: {"result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{"listChanged":true}},"serverInfo":{"name":"Console","version":"0.9.405","icons":[{"src":"https://api.mcp.ai/i/console.svg?v=0","mimeType":"image/svg+xml"}]},"instructions":"MCP.AI platform v0.9.405 | Adapters: discord vunknown, console vunknown, pluggy v1.7.11. When the user asks about the version (e.g. \"qual a versão\", \"which version\"), call the show_version tool. NEW MCPs/tools/integrations (capabilities not already in this toolkit) come from the official mcp.ai catalog: the `console_search` tool finds them, `console_mcp_install` installs, and `console_invoke` runs a freshly installed tool. You are not authenticated yet. Call the authenticate tool first — it will give the user a browser link to log in and copy a token. No other tools will work until authenticated."},"jsonrpc":"2.0","id":1}

~~~

## 3. tools/list (nomes)
~~~
openfinance_search_bank_connectors, openfinance_list_connections, openfinance_get_item_status, openfinance_provider_status, openfinance_list_accounts, openfinance_list_transactions, openfinance_list_transactions_by_item, openfinance_list_credit_card_bills, openfinance_list_investments, openfinance_list_investment_transactions, openfinance_list_loans, openfinance_get_loan_detail, openfinance_force_sync, openfinance_get_account_balance, openfinance_get_accounts_detail, openfinance_get_credit_card_bill, openfinance_list_categories, openfinance_update_transaction_category, openfinance_disconnect_bank, discord_list_accounts, discord_get_me, discord_list_guilds, discord_get_guild, discord_list_channels, discord_list_guild_members, discord_get_channel, discord_list_messages, discord_get_message, discord_get_user, discord_send_message, discord_send_dm, discord_edit_message, discord_add_reaction, discord_delete_message, console_toolkits_list, console_mcps_list, console_logs_query, console_usage_summary, console_toolkit_create, console_toolkit_update, console_mcp_install, console_mcp_uninstall, console_mcp_subscribe, console_mcp_cancel, console_mcp_resume, console_search, console_describe, console_list_tools, console_invoke, console_request_mcp, show_version, report_bug, connect, toolkit_info, authenticate
TOTAL: 55 tools
~~~

## 4. Resposta da tool authenticate (trecho)

> Reproduzido em 2026-11-02 18:10 UTC. A chamada exige a notificação `notifications/initialized` (HTTP 202) antes; sem ela a API responde "Session not found".

~~~
event: message
data: {"result":{"content":[{"type":"text","text":"The user has not pasted a token yet. Ask them to open this URL in a browser (while logged into mcp.ai), then copy the token:\n\nhttps://app.mcp.ai/agent-auth?toolkit=tk_pub_console\n\nTwo ways to use the token:\n1. PERMANENT (recommended): add it to this MCP server's config in your client as a header — `Authorization: Bearer <token>`. The token does not expire, so the connection survives restarts/reconnects and you never have to paste again.\n2. THIS SESSION ONLY (quick): paste it back to me and I'll call authenticate with { token: \"<pasted_jwt>\" }. This is lost on reconnect, idle, or server restart — you'd have to repeat it."}],"jsonrpc":"2.0","id":7}
~~~

## 5. Headers de https://mcp.ai/ (trecho)
~~~
HTTP/1.1 200 OK
Age: 0
Cache-Control: private, no-cache, no-store, max-age=0, must-revalidate
Content-Type: text/html; charset=utf-8
Date: Mon, 02 Nov 2026 18:08:20 GMT
Link: </index.md>; rel="alternate"; type="text/markdown"
Link: </_next/static/immutable/media/70bc3e132a0a741e-s.p.269kn9uafm0ti.woff2>; rel=preload; as="font"; crossorigin=""; type="font/woff2", </_next/static/immutable/media/83afe278b6a6bb3c-s.p.45535valc9rzk.woff2>; rel=preload; as="font"; crossorigin=""; type="font/woff2"
Server: Vercel
Set-Cookie: mcp_ft=%7B%22ts%22%3A1793642900292%2C%22host%22%3A%22mcp.ai%22%2C%22path%22%3A%22%2F%22%2C%22ref%22%3Anull%2C%22gclid%22%3Anull%2C%22utm_source%22%3Anull%2C%22utm_medium%22%3Anull%2C%22utm_campaign%22%3Anull%2C%22utm_content%22%3Anull%2C%22utm_term%22%3Anull%7D; Path=/; Expires=Sun, 31 Jan 2027 18:08:20 GMT; Max-Age=7776000; Domain=.mcp.ai; Secure; HttpOnly; SameSite=lax
Strict-Transport-Security: max-age=63072000
Vary: rsc, next-router-state-tree, next-router-prefetch, next-router-segment-prefetch
X-Matched-Path: /[lang]
~~~

## 6. Headers de https://api.mcp.ai/ (CORS)
~~~
access-control-allow-headers: Content-Type, mcp-session-id, X-Builder-Token, Authorization
access-control-allow-methods: GET, POST, DELETE, OPTIONS
access-control-allow-origin: *
access-control-expose-headers: mcp-session-id
x-powered-by: Express
Server: cloudflare
~~~

## 7. CNPJ 20.873.739/0001-15 (BrasilAPI, extrato)

> Resposta real da BrasilAPI em 2026-11-02, reduzida aos campos relevantes.

~~~
{
  "razao_social": "DL WEB LTDA",
  "nome_fantasia": "DL WEB",
  "cnpj": "20873739000115",
  "descricao_situacao_cadastral": "ATIVA",
  "data_inicio_atividade": "2014-08-19",
  "natureza_juridica": "Sociedade Empresária Limitada",
  "cnae_fiscal_descricao": "Portais, provedores de conteúdo e outros serviços de informação na internet",
  "municipio": "CAMPO GRANDE",
  "uf": "MS",
  "capital_social": 100000,
  "porte": "DEMAIS",
  "opcao_pelo_simples": false,
  "opcao_pelo_mei": false,
  "qsa": [
    {
      "nome_socio": "DOUGLAS PESENTE DE LACERDA",
      "qualificacao_socio": "Sócio-Administrador",
      "data_entrada_sociedade": "2014-08-19"
    }
  ]
}
~~~
