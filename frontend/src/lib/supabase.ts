import { createClient } from "@supabase/supabase-js"
import { setAuthTokenProvider } from "./api-client"

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || "https://placeholder.supabase.co"
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || "placeholder-anon-key"

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
  },
})

// Wire Supabase session token to API client
setAuthTokenProvider(async () => {
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token || null
})
