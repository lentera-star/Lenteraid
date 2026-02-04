import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// Modal Serverless GPU Endpoint
const MODAL_ENDPOINT = 'https://lentera-star--lentera-llama-generate.modal.run'

serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders })
    }

    try {
        const body = await req.json()
        const mode = body.mode || 'chat'

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
        }

        console.log(`📤 Proxying ${mode} request to Modal GPU endpoint`)

        // Forward request to Modal
        const response = await fetch(MODAL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: messages,
                max_tokens: body.max_tokens || 512,
                temperature: body.temperature || 0.7,
            }),
        })

        if (!response.ok) {
            const errorText = await response.text()
            console.error('❌ Modal endpoint error:', errorText)
            throw new Error(`Modal returned ${response.status}: ${errorText}`)
        }

        const data = await response.json()

        console.log('✅ Successfully received response from Modal')
        console.log('Response preview:', JSON.stringify(data).substring(0, 200))

        return new Response(
            JSON.stringify(data),
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

