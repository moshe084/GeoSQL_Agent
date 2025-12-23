#!/bin/bash

# Geo-SQL Agent Startup Script

echo "🌍 Starting Geo-SQL Agent..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "⚡ IMPORTANT: Edit .env and add your OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "^OPENAI_API_KEY=sk-" .env; then
    echo "❌ OPENAI_API_KEY not configured in .env"
    echo "Please edit .env and add: OPENAI_API_KEY=sk-your-key-here"
    exit 1
fi

echo "✅ Configuration validated"
echo ""

# Ask user which mode to run
echo "Select deployment mode:"
echo "  1) Development (with hot reload) - http://localhost:3000"
echo "  2) Production (optimized) - http://localhost:3010"
echo ""
read -p "Enter choice [1 or 2] (default: 2): " mode_choice
mode_choice=${mode_choice:-2}

if [ "$mode_choice" = "1" ]; then
    PROFILE="development"
    FRONTEND_PORT="3000"
    echo "🔧 Starting in DEVELOPMENT mode..."
else
    PROFILE="production"
    FRONTEND_PORT="3010"
    echo "🚀 Starting in PRODUCTION mode..."
fi

echo ""
echo "🐳 Building and starting Docker containers..."
echo ""

# Start services with selected profile
docker-compose --profile $PROFILE up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check if services are running
if docker ps | grep -q "geo-sql-postgis"; then
    echo "✅ PostGIS database is running"
fi

if docker ps | grep -q "geo-sql-backend"; then
    echo "✅ Backend API is running"
fi

if docker ps | grep -q "geo-sql-frontend"; then
    echo "✅ Frontend is running"
fi

echo ""
echo "🎉 Geo-SQL Agent is ready!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:$FRONTEND_PORT"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "💡 Try asking: 'Find all cafes within 200 meters of the largest park'"
echo ""
echo "📊 To view logs: docker-compose --profile $PROFILE logs -f"
echo "🛑 To stop:     docker-compose --profile $PROFILE down"
echo ""
