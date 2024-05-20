import { TablesList } from '@/components/tables-list'
import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/')({
    component: Index,
})

function Index() {
    return (
        <main className='flex items-center justify-center'>
            <TablesList />
        </main>
    )
}
