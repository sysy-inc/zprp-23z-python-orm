import { ModeToggle } from '@/components/mode-toggle'
import { createRootRoute, Link, Outlet } from '@tanstack/react-router'

export const Route = createRootRoute({
    component: () => (
        <div className='dark:bg-zinc-900 min-h-screen'>
            <div className="p-2 flex gap-2  max-w-screen-xl mx-auto">
                <Link to="/" className="[&.active]:font-bold">
                    Home
                </Link>{' '}
                <Link to="/about" className="[&.active]:font-bold">
                    About
                </Link>
                <ModeToggle />
            </div>
            {/* <hr /> */}
            <Outlet />
            {/* <TanStackRouterDevtools /> */}
        </div>
    ),
})
