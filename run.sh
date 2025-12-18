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
echo "🚀 Starting Docker containers..."
echo ""

# Start services
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

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
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "💡 Try asking: 'Find all cafes within 200 meters of the largest park'"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop:     docker-compose down"
echo ""
