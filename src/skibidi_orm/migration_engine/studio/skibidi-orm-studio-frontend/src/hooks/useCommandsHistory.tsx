import { useState } from "react"


const loadCommands = () => {
    const commands = localStorage.getItem('commands')
    if (commands) {
        return JSON.parse(commands).map((command: { command: string }) => command.command)
    }
}

export function useCommandsHistory() {
    const [commands, setCommands] = useState<string[]>(loadCommands() || [])

    const addCommand = (command: string) => {

        console.log('command', command)
        setCommands((prevCommands) => {
            console.log(JSON.stringify([...prevCommands, command].map((command) => ({ command: command }))))
            localStorage.setItem('commands', JSON.stringify([...prevCommands, command].map((command) => ({ command: command }))))
            return [...prevCommands, command]
        })
    }



    return { addCommand, commands }
}
