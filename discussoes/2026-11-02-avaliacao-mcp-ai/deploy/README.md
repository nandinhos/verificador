# Deploy — check.fssdev.com.br

Publicação do relatório em `/var/www/check.fssdev.com.br` (VPS `srv084270`, Ubuntu 24.04, nginx 1.24).

## Arquivos

| Arquivo | Papel |
|---|---|
| `nginx-check-http.conf` | estágio 1, só HTTP, para o desafio ACME |
| `nginx-check.conf` | configuração final: HTTP (ACME + redirecionamento condicional) e HTTPS com cabeçalhos |
| `deploy.sh` | executa `files`, `http`, `tls`, `final` ou `all` |

## Ordem

```bash
./deploy.sh files   # envia o conteúdo de ../site
./deploy.sh http    # vhost provisório
./deploy.sh tls     # certbot certonly --webroot
./deploy.sh final   # vhost definitivo + reload
```

## Decisões

- **Sem `add_header` dentro de `location`**: no nginx, um `add_header` em nível de location anula a herança dos cabeçalhos definidos no `server`. Por isso o cache usa `expires` e os cabeçalhos de segurança ficam só no `server`.
- **Redirecionamento HTTP→HTTPS condicional** a `X-Forwarded-Proto: https`: se a Cloudflare estiver em modo Flexible, o origin recebe HTTP e um 301 incondicional criaria laço.
- **CSP restritiva** (`default-src 'none'`), compatível porque o site não usa estilo nem script inline.
- **`X-Robots-Tag: noindex`** em todas as respostas. O `robots.txt` do domínio é servido pela Cloudflare (política de Content Signals), então o origin não controla esse arquivo na borda.

## Pendências de plataforma (fora do servidor)

1. **SSL/TLS da Cloudflare em Full (strict)** — hoje o site funciona nos dois modos, mas só Full (strict) valida o certificado na origem.
2. **Seis subdomínios ainda publicam o IP de origem** (`events`, `eventshomologacao`, `matchenginelinkedn`, `nextcloud`, `reportshtml`, `transcricoesyoutube` resolvem para 201.46.120.198). Enquanto isso, esconder a origem é parcial: qualquer um descobre o IP por esses registros.
3. Depois de proxiar todos, vale restringir 80/443 no firewall aos ranges da Cloudflare.
