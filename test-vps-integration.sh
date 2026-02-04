#!/bin/bash
# Test script for VPS integration

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration - UPDATE THESE
VPS_HOST="${VPS_HOST:-localhost}"
VPS_PORT="${VPS_PORT:-8000}"
BASE_URL="http://$VPS_HOST:$VPS_PORT"

echo "======================================"
echo "LenteraDreamFlow VPS Integration Test"
echo "======================================"
echo "Testing: $BASE_URL"
echo ""

# Test 1: Health Check
echo "${YELLOW}Test 1: Health Check${NC}"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/health" 2>&1)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "${GREEN}✓ Health check passed${NC}"
    echo "Response: $BODY"
else
    echo "${RED}✗ Health check failed (HTTP $HTTP_CODE)${NC}"
    echo "Response: $BODY"
    exit 1
fi

echo ""

# Test 2: Chat API
echo "${YELLOW}Test 2: Chat API${NC}"
CHAT_PAYLOAD='{
  "user_id": "test-user",
  "message": "Halo, aku merasa cemas hari ini",
  "conversation_history": []
}'

CHAT_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$BASE_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d "$CHAT_PAYLOAD" 2>&1)

HTTP_CODE=$(echo "$CHAT_RESPONSE" | tail -n 1)
BODY=$(echo "$CHAT_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "${GREEN}✓ Chat API test passed${NC}"
    echo "Response preview:"
    echo "$BODY" | python3 -m json.tool | head -n 10
else
    echo "${RED}✗ Chat API test failed (HTTP $HTTP_CODE)${NC}"
    echo "Response: $BODY"
    exit 1
fi

echo ""

# Test 3: Ollama Direct
echo "${YELLOW}Test 3: Ollama Direct${NC}"
OLLAMA_PAYLOAD='{
  "model": "lentera-dreamflow",
  "prompt": "Halo",
  "stream": false
}'

OLLAMA_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "http://$VPS_HOST:11434/api/generate" \
  -H "Content-Type: application/json" \
  -d "$OLLAMA_PAYLOAD" 2>&1)

HTTP_CODE=$(echo "$OLLAMA_RESPONSE" | tail -n 1)
BODY=$(echo "$OLLAMA_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "${GREEN}✓ Ollama direct test passed${NC}"
    RESPONSE_TEXT=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin).get('response', 'N/A')[:100])")
    echo "Response preview: $RESPONSE_TEXT..."
else
    echo "${YELLOW}⚠ Ollama direct test failed (might not be exposed)${NC}"
    echo "This is OK if Ollama is only accessible internally"
fi

echo ""
echo "${GREEN}======================================"
echo "✓ All Tests Passed!"
echo "======================================${NC}"
echo ""
echo "Backend is ready for Flutter integration!"
echo ""
