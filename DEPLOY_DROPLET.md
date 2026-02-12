# Atualizar e fazer deploy no Droplet (DigitalOcean)

Passo a passo para puxar a atualização do repositório no Droplet e fazer o deploy do dashboard atrás do Traefik (sem expor porta 8501).

**Droplet atual:** IP `192.241.157.215`. O app está hoje em **http://192.241.157.215:8501/** (porta 8501 exposta). Após o deploy com Traefik, o acesso será apenas por **https://painel.agenciakimera.com** (sem porta 8501 pública).

O projeto já tem: [docker-compose.traefik.yml](docker-compose.traefik.yml) (Traefik, sem portas públicas), [Dockerfile](Dockerfile) (porta 10000), e [.github/workflows/deploy.yml](.github/workflows/deploy.yml) (CI/CD). O deploy pode ser **manual** (SSH + comandos) ou **automático** (push no GitHub dispara o workflow).

---

## Cenário A: Primeira vez no Droplet (setup inicial)

Se o Droplet ainda **não** tem o projeto em `/opt/dashboard_clinic`:

### 1. Conectar no Droplet

```bash
ssh root@192.241.157.215
# ou: ssh ubuntu@192.241.157.215
```

### 2. Criar pasta e clonar o repositório

```bash
sudo mkdir -p /opt/dashboard_clinic
sudo chown $USER:$USER /opt/dashboard_clinic
cd /opt/dashboard_clinic
git clone https://github.com/SEU_USUARIO_OU_ORG/prestige_clinic_dash.git .
```

Substitua pela URL real do seu repositório.

### 3. Criar a rede do Traefik (se ainda não existir)

```bash
docker network create traefik-public 2>/dev/null || true
```

### 4. Definir a imagem (arquivo `.env`)

```bash
echo 'IMAGE=ghcr.io/SEU_GITHUB_OWNER/dashboard_clinic:latest' > .env
```

Substitua `SEU_GITHUB_OWNER` pelo dono do repositório no GitHub. Você pode usar [.env.droplet.example](.env.droplet.example) como referência.

### 5. Parar o container antigo (se existir)

Se o dashboard estava rodando com porta 8501 exposta:

```bash
docker stop dashboard_clinic 2>/dev/null || true
docker rm dashboard_clinic 2>/dev/null || true
```

### 6. Fazer login no GHCR e subir o stack (primeira vez)

```bash
echo SEU_PAT_AQUI | docker login ghcr.io -u SEU_GITHUB_OWNER --password-stdin
docker compose -f docker-compose.traefik.yml pull
docker compose -f docker-compose.traefik.yml up -d
```

### 7. Conferir

```bash
docker ps
docker logs dashboard_clinic --tail 30
```

Acesse: **https://painel.agenciakimera.com**

---

## Cenário B: Droplet já tem o projeto — só atualizar

Quando você já fez o setup (clone em `/opt/dashboard_clinic` e já rodou o compose pelo menos uma vez):

### Opção 1: Atualização manual (SSH)

1. **Conectar no Droplet**

   ```bash
   ssh root@192.241.157.215
   ```

2. **Ir para a pasta do projeto e puxar a nova versão do código**

   ```bash
   cd /opt/dashboard_clinic
   git pull origin main
   ```

   Isso atualiza o `docker-compose.traefik.yml` e qualquer outro arquivo do repositório.

3. **Garantir que a variável IMAGE está definida**

   ```bash
   export IMAGE=ghcr.io/SEU_GITHUB_OWNER/dashboard_clinic:latest
   ```

   Ou use o arquivo `.env` (como no setup inicial).

4. **Puxar a imagem nova e recriar o container**

   ```bash
   docker compose -f docker-compose.traefik.yml pull
   docker compose -f docker-compose.traefik.yml up -d --force-recreate
   ```

5. **Limpar imagens antigas (opcional)**

   ```bash
   docker image prune -f
   ```

**Resumo em uma sequência** (já na pasta do projeto):

```bash
cd /opt/dashboard_clinic
git pull origin main
export IMAGE=ghcr.io/SEU_GITHUB_OWNER/dashboard_clinic:latest   # ou use .env
docker compose -f docker-compose.traefik.yml pull
docker compose -f docker-compose.traefik.yml up -d --force-recreate
```

### Opção 2: Atualização automática (GitHub Actions)

O workflow [.github/workflows/deploy.yml](.github/workflows/deploy.yml) faz: build da imagem, push para o GHCR, SSH no Droplet, **git pull** (para atualizar o compose), `docker compose pull` e `up -d --force-recreate`.

- **Para mudanças de código (app):** dar **push para `main`** é suficiente: a nova imagem é gerada e o workflow atualiza o container no Droplet.
- **Para mudanças no `docker-compose.traefik.yml`:** o workflow executa `git pull` no Droplet, então o arquivo é atualizado automaticamente a cada deploy.

**Secrets necessários no repositório** (Settings → Secrets and variables → Actions):

| Secret            | Descrição                                                      |
| ----------------- | -------------------------------------------------------------- |
| `SSH_PRIVATE_KEY` | Chave privada SSH para acessar o Droplet                       |
| `DROPLET_HOST`    | IP do Droplet (ex.: `192.241.157.215`)                         |
| `DROPLET_USER`    | Ex.: `root` ou `ubuntu` (opcional)                             |
| `GHCR_PAT`        | Token GitHub com `read:packages` para o Droplet puxar a imagem |

**Variável opcional:** `DEPLOY_PATH` — caminho da pasta do projeto no Droplet (padrão: `/opt/dashboard_clinic`). Se o projeto estiver em outro diretório, crie a variável em Settings → Variables e use esse caminho.

---

## Fluxo resumido

- **Manual:** SSH → `cd /opt/dashboard_clinic` → `git pull origin main` → `export IMAGE=...` → `docker compose -f docker-compose.traefik.yml pull` → `docker compose -f docker-compose.traefik.yml up -d --force-recreate`.
- **Automático:** após configurar os secrets, `git push origin main` dispara o workflow; o Droplet recebe `git pull`, puxa a nova imagem e recria o container.

---

## Checklist rápido (atualização manual)

1. SSH no Droplet: `ssh root@192.241.157.215`.
2. `cd /opt/dashboard_clinic`.
3. `git pull origin main`.
4. `export IMAGE=ghcr.io/SEU_OWNER/dashboard_clinic:latest` (ou use `.env`).
5. `docker compose -f docker-compose.traefik.yml pull`.
6. `docker compose -f docker-compose.traefik.yml up -d --force-recreate`.
7. Testar https://painel.agenciakimera.com.

Documentação detalhada (troubleshooting, rede, SSL): [DEPLOY_TRAEFIK.md](DEPLOY_TRAEFIK.md).
