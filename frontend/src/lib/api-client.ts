/**
 * NextTech API Client
 * Chuẩn hóa request, response, Bearer token injection và error handling
 */

export interface ApiErrorResponse {
  code: string
  message: string
  details?: Record<string, any>
}

export class ApiError extends Error {
  status: number
  code: string
  details?: Record<string, any>

  constructor(status: number, message: string, code = "API_ERROR", details?: Record<string, any>) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.code = code
    this.details = details
  }
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

let authTokenProvider: (() => string | null | Promise<string | null>) | null = null

export function setAuthTokenProvider(provider: () => string | null | Promise<string | null>) {
  authTokenProvider = provider
}

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean | undefined>
}

export async function apiClient<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { params, headers: customHeaders, ...customConfig } = options

  // Build full URL with query parameters
  const url = new URL(endpoint.startsWith("http") ? endpoint : `${BASE_URL}${endpoint}`)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        url.searchParams.append(key, String(value))
      }
    })
  }

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...customHeaders,
  }

  if (authTokenProvider) {
    const token = await authTokenProvider()
    if (token) {
      ;(headers as Record<string, string>)["Authorization"] = `Bearer ${token}`
    }
  }

  const config: RequestInit = {
    ...customConfig,
    headers,
  }

  const response = await fetch(url.toString(), config)

  if (!response.ok) {
    let errorData: Partial<ApiErrorResponse> = {}
    try {
      errorData = await response.json()
    } catch {
      errorData = { message: response.statusText }
    }

    throw new ApiError(
      response.status,
      errorData.message || `Request failed with status ${response.status}`,
      errorData.code || "UNKNOWN_ERROR",
      errorData.details
    )
  }

  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}

// Convenience methods
export const api = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    apiClient<T>(endpoint, { ...options, method: "GET" }),
  post: <T>(endpoint: string, body?: any, options?: RequestOptions) =>
    apiClient<T>(endpoint, { ...options, method: "POST", body: body ? JSON.stringify(body) : undefined }),
  put: <T>(endpoint: string, body?: any, options?: RequestOptions) =>
    apiClient<T>(endpoint, { ...options, method: "PUT", body: body ? JSON.stringify(body) : undefined }),
  delete: <T>(endpoint: string, options?: RequestOptions) =>
    apiClient<T>(endpoint, { ...options, method: "DELETE" }),
}
