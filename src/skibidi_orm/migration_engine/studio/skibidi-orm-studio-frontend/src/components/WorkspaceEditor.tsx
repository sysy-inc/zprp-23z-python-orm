import AceEditor from 'react-ace'
import 'ace-builds/src-noconflict/theme-dracula'
import 'ace-builds/src-noconflict/mode-sql'
import 'ace-builds/src-noconflict/ext-language_tools'
import { useCommands } from '@/hooks/useCommandsHistory'
import { useTheme } from './theme-provider'


export function WorkspaceEditor() {
    const { setCurrentCommand, currentCommand } = useCommands()
    const { theme } = useTheme()

    function onChange(newValue: string) {
        setCurrentCommand(newValue)
    }

    return (
        <AceEditor
            style={{
                width: '100%',
                height: '100%'
            }}
            className=''
            mode="sql"
            theme={theme === 'dark' ? 'dracula' : 'github'}
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
