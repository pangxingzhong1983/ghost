# Ghost C2 Docker Deployment

## Quick Start

### Build and run with Docker Compose (recommended)

```bash
# Build the image (supports multi-arch: amd64, arm64)
docker-compose build --pull

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f ghost

# Stop the service
docker-compose down
```

### Build and run with Docker directly

```bash
# Build the image
docker build -t ghost-c2:latest .

# Run the container
docker run -d \
  --name ghost-c2 \
  -p 443:443 \
  -p 80:80 \
  -v ghost-config:/root/.ghost \
  --restart unless-stopped \
  ghost-c2:latest
```

## Configuration

### Persistent Storage

The container uses a Docker volume `ghost-config` to persist:
- Generated credentials (`/root/.ghost/crypto/`)
- Configuration files (`/root/.ghost/ghost.conf`)

### Custom Configuration

Mount a custom config file:

```bash
docker run -d \
  -v $(pwd)/my-ghost.conf:/root/.ghost/ghost.conf \
  -v ghost-config:/root/.ghost/crypto \
  ghost-c2:latest
```

### WebUI Access

If you've built the WebUI, you can expose it:

```bash
# In docker-compose.yml, add port mapping:
# - "8081:8080"  # Adjust based on your WebUI port
```

## Multi-Architecture Support

The Dockerfile is multi-stage and supports:
- `linux/amd64` (x86_64)
- `linux/arm64` (aarch64)

To build for multiple architectures:

```bash
# Using docker buildx (requires setup)
docker buildx build --platform linux/amd64,linux/arm64 -t ghost-c2:latest --push .

# Or with docker-compose
docker-compose build --pull
```

## Security Notes

1. **Non-root user**: The container runs as a non-root user (`ghost`) by default.
2. **Capabilities**: Only `NET_BIND_SERVICE` capability is added to bind to port 443.
3. **Seccomp/AppArmor**: Consider adding security profiles in production.
4. **Credentials**: Always persist credentials in a Docker volume or external mount.
5. **Network**: Use custom networks to isolate the C2 server.

## Production Deployment Checklist

- [ ] Change default passwords after first run
- [ ] Use custom SSL certificates (place in config)
- [ ] Enable firewall rules to restrict access
- [ ] Configure log rotation
- [ ] Set up monitoring/alerting
- [ ] Regular backups of `/root/.ghost`
- [ ] Keep container image updated

## Troubleshooting

### Permission denied on port 443

The container needs `NET_BIND_SERVICE` capability to bind to port <1024. The docker-compose.yml already includes this.

If running directly with `docker run`:
```bash
docker run ... --cap-add NET_BIND_SERVICE --cap-drop ALL ...
```

### Module import errors

Some modules may need additional system packages. If you encounter import errors, you may need to extend the Dockerfile:

```dockerfile
RUN apt-get update && apt-get install -y \
    libpcap-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

### Container exits immediately

Check the logs:
```bash
docker logs ghost-c2
```

The container may need interactive mode if running ghostsh:
```bash
docker run -it ghost-c2:latest
```

## Image Size

The multi-stage build keeps the image relatively small (~200-300MB). If you need even smaller:
- Use `python:3.10-alpine` as base (requires rebuilding native extensions for musl)
- Remove unused modules from `ghost/packages/`
