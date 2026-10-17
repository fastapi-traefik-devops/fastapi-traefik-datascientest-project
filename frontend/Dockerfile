FROM node:26.11.1-bookworm-slim@sha256:86f07bc9c5dce4578cf37e5a418b7bfc7f817cda25cde66e2b66e95ed86c4567 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
ARG VITE_API_URL=""
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

FROM nginxinc/nginx-unprivileged:1.30.5-alpine@sha256:56b8272e43a0525f67aed68d1e0794a712d10e3e45a563e118e9a77c817e6f86 AS runtime
COPY --from=build --chown=101:101 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
USER 101:101
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1/
