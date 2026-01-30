import { serve } from "https://deno.land/std@0.168.0/http/server.ts"

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
    if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders })
    }

    try {
        const body = await req.json()
        const { endpoint, ...payload } = body

        // Base VPS URL should not include the path if we want to be generic
        // Expecting VPS_BASE_URL like http://84.247.150.83:8000
        const VPS_BASE_URL = Deno.env.get('VPS_BASE_URL') || 'http://84.247.150.83:8000'
        const targetEndpoint = endpoint || '/api/chat'
        const VPS_API_URL = `${VPS_BASE_URL}${targetEndpoint}`

        const VPS_API_KEY = Deno.env.get('VPS_API_KEY')
        const VPS_AUTH_HEADER = Deno.env.get('VPS_AUTH_HEADER_NAME') || 'Authorization'

        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        }

        if (VPS_API_KEY) {
            headers[VPS_AUTH_HEADER] = VPS_API_KEY
        }

        const response = await fetch(VPS_API_URL, {
            method: 'POST',
            headers,
            body: JSON.stringify(payload),
        })

        const data = await response.json()

        return new Response(
            JSON.stringify(data),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
                status: response.status,
            },
        )

    } catch (error) {
        return new Response(
            JSON.stringify({ error: error.message }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' },
                status: 500,
            },
        )
    }
})
