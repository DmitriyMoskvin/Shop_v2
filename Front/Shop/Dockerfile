# Фаза сборки
FROM node:20 AS build-stage

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект
COPY . .

# Собираем Vue.js проект
RUN npm run build

# Фаза продакшн
FROM nginx:1.23.1

# Копируем файлы из фазы build-stage
COPY --from=build-stage /app/dist /etc/nginx/html

# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]