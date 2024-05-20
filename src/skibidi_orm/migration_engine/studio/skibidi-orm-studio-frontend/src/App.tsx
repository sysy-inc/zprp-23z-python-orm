import { ModeToggle } from "./components/mode-toggle"
import { Button } from "./components/ui/button"

function App() {

    return (
        <main className="dark:bg-zinc-900 min-w-full min-h-screen" >
            <h1>Skibidi ORM Studio</h1>
            <Button>Clicke me</Button>
            <ModeToggle />
        </main>
    )
}

export default App
