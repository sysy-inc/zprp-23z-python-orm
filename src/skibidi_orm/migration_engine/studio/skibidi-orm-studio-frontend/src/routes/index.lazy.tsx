import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/')({
    component: Index,
})

function Index() {
    return (
        <main className='flex items-center justify-center w-full h-full'>
            <p className='text-muted-foreground'>Select table to inspect</p>
        </main>
    )
}
