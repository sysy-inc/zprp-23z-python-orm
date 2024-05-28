import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/mode-sql'
import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/ext-language_tools'
import { useCommands } from '@/hooks/useCommandsHistory'
import { useEffect } from 'react'


export function WorkspaceEditor() {
    const { setCurrentCommand, currentCommand } = useCommands()

    function onChange(newValue: string) {
        setCurrentCommand(newValue)
    }

    useEffect(() => {
        console.log('currentCommandDDDDDDD', currentCommand)
    }, [currentCommand])

    return (
        <AceEditor
            style={{
                width: '100%',
                height: '100%'
            }}
            className=''
            mode="sql"
            theme="github"
            onChange={onChange}
            value={currentCommand}
            name="UNIQUE_ID_OF_DIV"
            editorProps={{ $blockScrolling: true }}
            fontSize={14}
            showPrintMargin={true}
            showGutter={true}
            highlightActiveLine={true}
            placeholder='SELECT * FROM table...'
            setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: true,
                showLineNumbers: true,
                tabSize: 4,
            }}
        />
    )
}
