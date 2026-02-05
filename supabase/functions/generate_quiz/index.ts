import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

const MODAL_ENDPOINT = Deno.env.get('MODAL_ENDPOINT') || ''
const MODAL_TOKEN = Deno.env.get('MODAL_TOKEN') || ''

interface MoodEntry {
    mood_rating: number
    mood_tags: string[]
    journal_text?: string
    created_at: string
}

interface QuizRequest {
    user_id: string
    mood_history: MoodEntry[]
    count?: number
}

serve(async (req) => {
    // CORS headers
    if (req.method === 'OPTIONS') {
        return new Response(null, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
            },
        })
    }

    try {
        const body: QuizRequest = await req.json()
        const { mood_history, count = 3 } = body

        // If no mood history, return static questions
        if (!mood_history || mood_history.length === 0) {
            return new Response(
                JSON.stringify({
                    questions: getStaticQuestions().slice(0, count),
                    personalized: false,
                }),
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                }
            )
        }

        // Analyze mood patterns
        const avgRating = mood_history.reduce((sum, m) => sum + m.mood_rating, 0) / mood_history.length
        const allTags = mood_history.flatMap(m => m.mood_tags)
        const tagCounts = allTags.reduce((acc, tag) => {
            acc[tag] = (acc[tag] || 0) + 1
            return acc
        }, {} as Record<string, number>)
        const commonTags = Object.entries(tagCounts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 3)
            .map(([tag]) => tag)

        const journalSummary = mood_history
            .filter(m => m.journal_text)
            .map(m => m.journal_text)
            .join('. ')
            .slice(0, 500) // Limit context size

        // Build AI prompt
        const aiPrompt = `Kamu adalah AI edukator kesehatan mental untuk aplikasi LENTERA. 

Berdasarkan mood history user 7 hari terakhir:
- Rating mood rata-rata: ${avgRating.toFixed(1)}/5
- Tag yang sering muncul: ${commonTags.join(', ')}
${journalSummary ? `- Tema jurnal: "${journalSummary}"` : ''}

Buatlah ${count} pertanyaan trivia edukatif tentang kesehatan mental yang RELEVAN dengan pola mood user di atas. 

PENTING:
1. Fokus pada coping strategies untuk mood yang sering dialami
2. Berikan tips praktis yang dapat diterapkan sehari-hari
3. Gunakan Bahasa Indonesia yang santai dan friendly
4. Pastikan pertanyaan dan jawaban akurat secara medis

Format output HARUS dalam JSON berikut (tanpa markdown, hanya pure JSON):
{
  "questions": [
    {
      "question": "Pertanyaan yang relevan dengan mood user?",
      "options": ["Opsi A", "Opsi B", "Opsi C", "Opsi D"],
      "correctAnswer": "Opsi B",
      "explanation": "Penjelasan singkat kenapa ini benar dan bagaimana ini membantu."
    }
  ]
}

Contoh untuk user yang sering stress:
{
  "questions": [
    {
      "question": "Ketika merasa stress, teknik pernapasan yang paling efektif adalah?",
      "options": ["Bernapas cepat", "4-7-8 breathing", "Menahan napas lama", "Napas dangkal"],
      "correctAnswer": "4-7-8 breathing",
      "explanation": "Teknik 4-7-8 (tarik napas 4 detik, tahan 7 detik, buang 8 detik) membantu menenangkan sistem saraf dan menurunkan kortisol."
    }
  ]
}

Hasilkan ${count} pertanyaan sekarang:`

        // Call AI endpoint
        const messages = [
            {
                role: 'system',
                content: 'Kamu adalah AI edukator kesehatan mental yang membuat kuis edukatif. Selalu respond dengan valid JSON.',
            },
            {
                role: 'user',
                content: aiPrompt,
            },
        ]

        const aiResponse = await fetch(MODAL_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${MODAL_TOKEN}`,
            },
            body: JSON.stringify({
                messages,
                max_tokens: 1000,
                temperature: 0.7,
            }),
        })

        if (!aiResponse.ok) {
            console.error('AI endpoint failed:', await aiResponse.text())
            throw new Error('AI generation failed')
        }

        const aiData = await aiResponse.json()
        let aiMessage = ''

        if (aiData.choices && aiData.choices[0] && aiData.choices[0].message) {
            aiMessage = aiData.choices[0].message.content || ''
        } else if (aiData.message) {
            aiMessage = aiData.message
        }

        // Parse AI response (remove markdown if present)
        let cleanedMessage = aiMessage.trim()
        if (cleanedMessage.startsWith('```json')) {
            cleanedMessage = cleanedMessage.replace(/```json\n?/g, '').replace(/```\n?/g, '')
        } else if (cleanedMessage.startsWith('```')) {
            cleanedMessage = cleanedMessage.replace(/```\n?/g, '')
        }

        const quizData = JSON.parse(cleanedMessage)

        return new Response(
            JSON.stringify({
                questions: quizData.questions,
                personalized: true,
            }),
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            }
        )
    } catch (error) {
        console.error('Error generating quiz:', error)

        // Fallback to static questions
        return new Response(
            JSON.stringify({
                questions: getStaticQuestions().slice(0, 3),
                personalized: false,
                error: error.message,
            }),
            {
                status: 200, // Return 200 with fallback
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            }
        )
    }
})

function getStaticQuestions() {
    return [
        {
            question: 'Berapa lama waktu tidur yang ideal untuk orang dewasa?',
            options: ['5-6 jam', '7-9 jam', '10-12 jam', '4-5 jam'],
            correctAnswer: '7-9 jam',
            explanation: 'Orang dewasa membutuhkan 7-9 jam tidur per malam untuk kesehatan optimal.',
        },
        {
            question: 'Apa yang dimaksud dengan mindfulness?',
            options: [
                'Berpikir tentang masa lalu',
                'Fokus pada saat ini',
                'Merencanakan masa depan',
                'Multitasking',
            ],
            correctAnswer: 'Fokus pada saat ini',
            explanation: 'Mindfulness adalah praktik untuk fokus pada momen saat ini tanpa judgment.',
        },
        {
            question: 'Aktivitas fisik yang disarankan per minggu adalah?',
            options: ['30 menit', '75 menit', '150 menit', '300 menit'],
            correctAnswer: '150 menit',
            explanation: 'WHO merekomendasikan 150 menit aktivitas fisik intensitas sedang per minggu.',
        },
    ]
}
