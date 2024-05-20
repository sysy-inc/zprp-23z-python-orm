import { ModeToggle } from "./components/mode-toggle"
import { TablesList } from "./components/tables-list"
import { Button } from "./components/ui/button"

function App() {

    return (
        <main className="dark:bg-zinc-900 min-w-full min-h-screen flex items-center justify-center" >
            {/* <h1>Skibidi ORM Studio</h1> */}
            <Button>Clicke me</Button>
            {/* <ModeToggle /> */}
            <TablesList />
        </main>
    )
}

export default App
