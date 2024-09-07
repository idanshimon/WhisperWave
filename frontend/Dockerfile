# Frontend Dockerfile (React)

# ---- Frontend Build Stage ----
    FROM node:18 AS build

    # Set the working directory inside the container for frontend
    WORKDIR /app
    
    # Copy frontend dependencies and install them
    COPY frontend/package.json frontend/package-lock.json ./
    RUN npm install
    
    # Copy the rest of the frontend code and build it
    COPY frontend/ ./
    RUN npm run build
    
    # ---- Nginx Stage ----
    FROM nginx:alpine
    
    # Copy the build output from the previous stage to Nginx’s static folder
    COPY --from=build /app/build /usr/share/nginx/html
    
    # Expose Nginx port (80)
    EXPOSE 80
    
    # Start Nginx
    CMD ["nginx", "-g", "daemon off;"]
    