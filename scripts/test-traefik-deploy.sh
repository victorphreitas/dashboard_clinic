#!/usr/bin/env bash
# Run this on the Droplet (or any host with Docker) to verify the Traefik stack.
# Usage: ./scripts/test-traefik-deploy.sh [--teardown]
# Requires: Docker and docker compose. Run on the server: scp + ssh, or clone repo there.
set -e

command -v docker >/dev/null 2>&1 || { echo "Docker not found. Run this script on the Droplet (or a host with Docker)."; exit 127; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPOSE_FILE="$REPO_ROOT/docker-compose.traefik.yml"
TEARDOWN=false

for arg in "$@"; do
  [ "$arg" = "--teardown" ] && TEARDOWN=true
done

echo "=== 1. Network ==="
docker network create traefik-public 2>/dev/null || true
docker network inspect traefik-public --format '{{.Name}}' | grep -q traefik-public && echo "OK: traefik-public exists"

echo ""
echo "=== 2. Build (if no IMAGE set) ==="
if [ -z "$IMAGE" ]; then
  docker build -t dashboard_clinic:latest "$REPO_ROOT"
  echo "OK: image dashboard_clinic:latest built"
else
  echo "OK: using IMAGE=$IMAGE (skip build)"
fi

echo ""
echo "=== 3. Compose config validation ==="
docker compose -f "$COMPOSE_FILE" config --quiet && echo "OK: compose config valid" || { echo "FAIL: invalid config"; exit 1; }

echo ""
echo "=== 4. Start stack ==="
cd "$REPO_ROOT"
docker compose -f "$COMPOSE_FILE" up -d
echo "Waiting for container to be healthy (up to 60s)..."
for i in $(seq 1 30); do
  status="$(docker inspect dashboard_clinic --format '{{.State.Health.Status}}' 2>/dev/null || echo "starting")"
  [ "$status" = "healthy" ] && break
  [ $i -eq 30 ] && { echo "WARN: healthcheck did not pass in time. Check: docker logs dashboard_clinic"; exit 1; }
  sleep 2
done
echo "OK: container healthy"

echo ""
echo "=== 5. Health endpoint (from inside container) ==="
code=$(docker exec dashboard_clinic curl -sf -o /dev/null -w "%{http_code}" http://localhost:10000/_stcore/health 2>/dev/null || echo "000")
[ "$code" = "200" ] && echo "OK: GET /_stcore/health => $code" || { echo "FAIL: health returned $code"; exit 1; }

echo ""
echo "=== 6. No public port (expected) ==="
ports=$(docker port dashboard_clinic 2>/dev/null || true)
[ -z "$ports" ] && echo "OK: no host ports exposed" || echo "INFO: ports: $ports"

echo ""
echo "=== 7. Attached to traefik-public ==="
docker network inspect traefik-public --format '{{range .Containers}}{{.Name}} {{end}}' | grep -q dashboard_clinic && echo "OK: dashboard_clinic on traefik-public" || { echo "FAIL: not on network"; exit 1; }

echo ""
echo "=== All checks passed. ==="
echo "If Traefik is running on this host, open https://painel.agenciakimera.com.br (DNS must point here)."
echo "Logs: docker logs dashboard_clinic"

if [ "$TEARDOWN" = true ]; then
  echo ""
  echo "=== Teardown (--teardown) ==="
  docker compose -f "$COMPOSE_FILE" down
  echo "Done."
fi
