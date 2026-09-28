#!/bin/bash
# NexaVideo - 28 Module Creator - One File Solution

echo "NexaVideo 28 Modules bana raha hun..."

mkdir -p app/src/main
mkdir -p core-common core-ui
mkdir -p feature-auth feature-feed feature-video feature-upload feature-profile
mkdir -p feature-social feature-comments feature-messaging feature-notifications
mkdir -p feature-creator feature-earnings feature-dashboard
mkdir -p data-auth data-user data-video data-database data-storage data-analytics
mkdir -p backend-api backend-security
mkdir -p admin-panel docker ci-cd config docs testing

# Main files
echo "rootProject.name = \"NexaVideo\"" > settings.gradle
echo "include ':app'" >> settings.gradle

cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  backend:
    build: ./backend-api
    ports: ["3000:3000"]
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: nexavideo
EOF

cat > README.md << 'EOF'
# NexaVideo - 28 Module Live
All 28 modules created with single file!
EOF

echo "Ho gaya! 28 Modules Ready ✅"
ls -1
