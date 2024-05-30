import { Sidebar } from '@/components/Sidebar'
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable'
import { Outlet, createRootRoute } from '@tanstack/react-router'

export const Route = createRootRoute({
    component: () => (
        <div className='dark:bg-zinc-900 min-h-screen flex flex-col'>
            {/* <div className="p-2 flex gap-2  max-w-screen-xl mx-auto">
                <Link to="/" className="[&.active]:font-bold">
                    Home
                </Link>{' '}
                <Link to="/about" className="[&.active]:font-bold">
                    About
                </Link>
                <ModeToggle />
            </div> */}
            {/* <hr /> */}
            <ResizablePanelGroup direction='horizontal' className='h-full flex-1'>
                <ResizablePanel defaultSize={10}>
                    <Sidebar />
                </ResizablePanel>
                <ResizableHandle />
                <ResizablePanel>
                    <Outlet />
                </ResizablePanel>
            </ResizablePanelGroup>
            {/* <TanStackRouterDevtools /> */}
        </div >
    ),
})
