"use client"

import { QueryClientProvider, QueryClient } from "@tanstack/react-query"

export default function Providers({ children }){

    const client = new QueryClient({
        defaultOptions: {
            queries: {
            retry: 1,
            staleTime:3600 * 60  * 5
            }
        }
    })

    return (
        <QueryClientProvider client={client}>{children}</QueryClientProvider>
    )
}