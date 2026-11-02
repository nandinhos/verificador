#!/usr/bin/env bash
# Deploy do relatório em check.fssdev.com.br
set -euo pipefail

ROOT="/home/nandodev/projects/verificador-deterministico/discussoes/2026-11-02-avaliacao-mcp-ai"
SSH="ssh -o BatchMode=yes vps3"
STAGE="${1:-all}"

echo "== destino: $($SSH 'hostname')"

if [[ "$STAGE" == "files" || "$STAGE" == "all" ]]; then
  echo "== copiando arquivos"
  tar czf - -C "$ROOT/site" . | $SSH 'mkdir -p /var/www/check.fssdev.com.br && find /var/www/check.fssdev.com.br -mindepth 1 -delete && tar xzf - -C /var/www/check.fssdev.com.br && chown -R www-data:www-data /var/www/check.fssdev.com.br'
  $SSH 'ls -la /var/www/check.fssdev.com.br | head -12'
fi

if [[ "$STAGE" == "http" || "$STAGE" == "all" ]]; then
  echo "== config estágio 1 (HTTP)"
  $SSH 'cat > /etc/nginx/sites-available/check.fssdev.com.br' < "$ROOT/deploy/nginx-check-http.conf"
  $SSH 'ln -sf /etc/nginx/sites-available/check.fssdev.com.br /etc/nginx/sites-enabled/check.fssdev.com.br && nginx -t && systemctl reload nginx'
  echo "== teste local HTTP"
  $SSH 'curl -s -o /dev/null -w "status=%{http_code} bytes=%{size_download}\n" -H "Host: check.fssdev.com.br" http://127.0.0.1/'
fi

if [[ "$STAGE" == "tls" || "$STAGE" == "all" ]]; then
  echo "== certificado"
  $SSH 'certbot certonly --webroot -w /var/www/check.fssdev.com.br -d check.fssdev.com.br --non-interactive --agree-tos --keep-until-expiring 2>&1 | tail -6'
fi

if [[ "$STAGE" == "final" || "$STAGE" == "all" ]]; then
  echo "== config final (HTTP+HTTPS)"
  $SSH 'cat > /etc/nginx/sites-available/check.fssdev.com.br' < "$ROOT/deploy/nginx-check.conf"
  $SSH 'nginx -t && systemctl reload nginx'
  echo "== teste local HTTPS"
  $SSH 'curl -s -o /dev/null -w "status=%{http_code} tls=%{ssl_verify_result}\n" --resolve check.fssdev.com.br:443:127.0.0.1 https://check.fssdev.com.br/'
fi

echo "== fim"
