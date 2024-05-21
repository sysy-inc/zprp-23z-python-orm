import React, { createContext, useContext, useState } from "react"


interface ICommandResultStore {
    commandResult: any[]
    setCommandResult: React.Dispatch<React.SetStateAction<any[]>>
}
const commandResultContext = createContext<ICommandResultStore>({ commandResult: [], setCommandResult: () => { } })

function commandResultStore() {
    const [commandResult, setCommandResult] = useState<any[]>([])

    return {
        commandResult,
        setCommandResult
    }
}

export const CommandResultProvider = ({ children }: { children: React.ReactNode }) => {
    const commands = commandResultStore()

    return (
        <commandResultContext.Provider value={commands} >
            {children}
        </commandResultContext.Provider>
    )
}

export function useCommandResult() {
    return useContext(commandResultContext)
}
