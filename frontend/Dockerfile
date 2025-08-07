# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Instala dependências do projeto
COPY package.json package-lock.json* ./
RUN npm ci

# Copia o restante do código
COPY . .

# Renomeia arquivo de configuração Vite para ESM
# Caso o arquivo esteja como vite.config.js, renomeie para vite.config.mjs antes de build
RUN if [ -f vite.config.js ]; then mv vite.config.js vite.config.mjs; fi

# Expõe a porta de desenvolvimento do Vite
EXPOSE 5173

# Inicia o servidor de desenvolvimento do Vite
CMD ["npm", "run", "dev"]
