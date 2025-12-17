#!/bin/bash

# LENTERA Backend - Quick Start Script
# This script helps you set up the backend quickly

echo "🌟 LENTERA Backend Setup"
echo "========================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker is running
if ! docker ps &> /dev/null; then
    echo "❌ Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is installed and running"
echo ""

# Create .env file if not exists
if [ ! -f backend/.env ]; then
    echo "📝 Creating .env file..."
    cp backend/.env.example backend/.env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🚀 Starting Docker containers..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 5

echo ""
echo "📥 Downloading Ollama model (phi - 2.7GB)..."
echo "This may take a few minutes..."
docker exec -it lentera-ollama ollama pull phi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Service URLs:"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Ollama: http://localhost:11434"
echo ""
echo "🔍 Check status:"
echo "  docker ps"
echo ""
echo "📝 View logs:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f ollama"
echo ""
echo "🛑 Stop services:"
echo "  docker-compose down"
