import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// Modal Serverless GPU Endpoint (Smart/Fine-tuned)
const MODAL_ENDPOINT = 'https://lentera-star--lentera-llama-generate.modal.run'
// VPS Endpoint (Fast/Compressed - Friend A)
const VPS_ENDPOINT = 'http://84.247.150.83:8000/api/chat'

serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders })
    }

    try {
        const body = await req.json()
        const mode = body.mode || 'chat'
        const modelMode = body.model_mode || 'smart' // 'smart' or 'fast'

        // Determine target endpoint
        const targetEndpoint = modelMode === 'fast' ? VPS_ENDPOINT : MODAL_ENDPOINT
        console.log(`🎯 Model Mode: ${modelMode} -> Sending to ${targetEndpoint}`)

        let messages = []
        if (mode === 'mood_analysis') {
            console.log('📊 Mode: Mood Analysis')
            const moodRating = body.mood_rating
            const emotions = body.emotions || []
            const journal = body.journal || '(tidak ada catatan)'

            const systemPrompt = `Kamu adalah asisten refleksi emosional harian untuk aplikasi kesehatan mental LENTERA.

PERAN KAMU:
- Menganalisis kondisi emosional pengguna berdasarkan data harian mereka
- Menggunakan sudut pandang ORANG KEDUA ("kamu", "kondisimu", dll)
- Memberikan insight yang empatik, singkat, dan praktis
- Berbicara dalam Bahasa Indonesia yang natural dan hangat

PENTING - LARANGAN MUTLAK:
❌ JANGAN membuat cerita fiktif
❌ JANGAN memperkenalkan diri
❌ JANGAN bertanya balik ke user
❌ JANGAN pakai sudut pandang orang pertama ("aku", "saya")
❌ JANGAN roleplay sebagai user atau persona lain
❌ JANGAN campur Bahasa Inggris kecuali istilah teknis

FORMAT OUTPUT yang HARUS diikuti:
1. Mulai langsung dengan observasi kondisi emosional (1-2 kalimat)
2. Berikan 2-3 saran self-care yang spesifik dan praktis (gunakan bullet points)
3. Tutup dengan 1 kalimat kata dukungan yang hangat

Contoh format yang BENAR:
"Kondisimu hari ini terlihat [observasi]. [Penjelasan singkat kenapa].

💡 Saran untuk kamu:
• [Saran 1]
• [Saran 2]
• [Saran 3]

[Kata dukungan penutup]"`

            const moodPrompt = `Analisis kondisi harian pengguna berikut:

📊 Data Mood:
- Rating mood: ${moodRating}/5
- Tag emosi: ${emotions.join(', ')}
- Catatan jurnal: "${journal}"

Berikan insight sesuai format yang sudah ditentukan.`

            messages = [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: moodPrompt }
            ]
        } else {
            console.log('💬 Mode: Chat')
            messages = body.messages || []

            // Add default system prompt if empty or no system role present
            const hasSystem = messages.some((m: any) => m.role === 'system')
            if (!hasSystem) {
                messages.unshift({
                    role: 'system',
                    content: `Kamu adalah Sahabat Lentera, asisten kesehatan mental yang empatik, tenang, dan suportif. 

ATURAN KRITIS TENTANG MEMORI:
1. BACA SELURUH riwayat percakapan dengan SANGAT TELITI sebelum merespons
2. INGAT SEMUA detail yang dibagikan user: nama mereka, nama orang lain, cerita, peristiwa, perasaan, dll
3. GUNAKAN informasi dari pesan sebelumnya untuk menunjukkan bahwa kamu benar-benar mendengarkan
4. Jika user bertanya tentang sesuatu yang sudah mereka ceritakan sebelumnya, JAWAB berdasarkan informasi itu
5. Jangan pernah bilang "tidak tahu" atau "lupa" untuk hal yang sudah user ceritakan dalam percakapan ini

Berikan jawaban yang singkat, hangat, dan fokus pada pendengaran aktif. Gunakan Bahasa Indonesia yang natural dan hindari pengulangan kalimat yang sama.`
                })
            }
        }

        console.log(`📤 Proxying ${mode} request to target endpoint`)

        // Forward request to target
        let payload = {}
        if (modelMode === 'fast') {
            const lastMessage = messages[messages.length - 1]?.content || ''
            payload = {
                message: lastMessage,
                user_id: body.user_id || 'anonymous',
                conversation_id: body.conversation_id || `conv_${Date.now()}`
            }
        } else {
            payload = {
                messages: messages,
                max_tokens: body.max_tokens || 256,
                temperature: body.temperature || 0.7,
                repeat_penalty: body.repeat_penalty || 1.1,
            }
        }

        const response = await fetch(targetEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        })

        if (!response.ok) {
            const errorText = await response.text()
            console.error(`❌ ${modelMode.toUpperCase()} endpoint error:`, errorText)
            throw new Error(`${modelMode.toUpperCase()} returned ${response.status}: ${errorText}`)
        }

        const data = await response.json()

        // Handle different response formats (OpenAI-like from Modal/OpenAI vs flat-json from VPS)
        let responseText = ''
        if (data.choices && data.choices[0] && data.choices[0].message) {
            responseText = data.choices[0].message.content || ''
        } else if (data.message) {
            responseText = data.message
        } else if (data.response) {
            responseText = data.response
        }

        console.log(`✅ Successfully received response from ${modelMode.toUpperCase()}`)
        console.log('Response preview:', responseText.substring(0, 100))

        // Transform response based on mode for Flutter AIService compatibility
        let mappedData: any = {}
        if (mode === 'mood_analysis') {
            mappedData = {
                analysis: responseText,
                mood_score: body.mood_rating || 3,
                timestamp: new Date().toISOString()
            }
        } else {
            mappedData = {
                message: responseText,
                conversation_id: data.conversation_id || body.conversation_id || `conv_${Date.now()}`,
                timestamp: data.timestamp || new Date().toISOString(),
                is_crisis: data.is_crisis || false
            }
        }

        return new Response(
            JSON.stringify(mappedData),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
                status: 200,
            },
        )


    } catch (error) {
        console.error('❌ Proxy error:', error.message)
        return new Response(
            JSON.stringify({
                error: 'Failed to process request',
                message: error.message
            }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
                status: 500,
            },
        )
    }
})

