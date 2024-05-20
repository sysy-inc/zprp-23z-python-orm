import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React from 'react'
import { ThemeProvider } from './theme-provider'
import { Toaster } from 'react-hot-toast'

const queryClient = new QueryClient()

interface ProvidersProps {
    children: React.ReactNode
}
export const Providers: React.FC<ProvidersProps> = ({ children }) => {
    return (
        <QueryClientProvider client={queryClient}>
            <ThemeProvider defaultTheme='dark' storageKey='vite-ui-theme'>
                <Toaster />
                {children}
            </ThemeProvider>
        </QueryClientProvider>
    )
}
