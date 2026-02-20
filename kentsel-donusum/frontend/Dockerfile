# 1. Asama: Node.js ile production build alinmasi
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
# Frontend'in backend ile konusabilmesi icin environment set ediliyor (-build sirasinda)
# Calisma aninda (runtime) env kullanimi icin ekstra ayarlamalar gerekebilir ama simdilik standard vite kullaniminda
ENV VITE_API_URL=/api

RUN npm run build

# 2. Asama: Uretilen dosyalarin Nginx ile serve edilmesi
FROM nginx:alpine

# React Router icin Nginx SPA config kopyasi
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
