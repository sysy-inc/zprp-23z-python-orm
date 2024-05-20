import React, { createContext, useCallback, useContext, useState } from "react"


const loadCommands = () => {
    const commands = localStorage.getItem('commands')
    if (commands) {
        return JSON.parse(commands).map((command: { command: string }) => command.command)
    }
}

interface ICommandsStore {
    commandsHistory: string[]
    currentCommand: string
    setCurrentCommand: React.Dispatch<React.SetStateAction<string>>
    saveCommand: (command: string) => void
}
const commandsContext = createContext<ICommandsStore>({ commandsHistory: [], currentCommand: '', setCurrentCommand: () => { }, saveCommand: () => { } })

function commandsStore() {
    const [commandsHistory, setCommandsHistory] = useState<string[]>(loadCommands() || [])
    const [currentCommand, setCurrentCommand] = useState<string>('')


    const saveCommand = useCallback((command: string) => {
        console.log('command', command)
        setCommandsHistory((prevCommands) => {
            console.log(JSON.stringify([...prevCommands, command].map((command) => ({ command: command }))))
            localStorage.setItem('commands', JSON.stringify([...prevCommands, command].map((command) => ({ command: command }))))
            return [...prevCommands, command]
        })
    }, [])



    return {
        commandsHistory,
        currentCommand,
        setCurrentCommand,
        saveCommand
    }
}

export const CommandsProvider = ({ children }: { children: React.ReactNode }) => {
    const commands = commandsStore()

    return (
        <commandsContext.Provider value={commands}>
            {children}
        </commandsContext.Provider>
    )
}

export function useCommands() {
    return useContext(commandsContext)
}
