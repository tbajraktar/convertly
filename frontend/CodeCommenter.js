class CodeCommenter {
    constructor() {
        // Regex Patterns
        this.patterns = {
            js: {
                function: /(async\s+)?function\s+(\w+)\s*\(([^)]*)\)/g,
                arrow: /(const|let|var)\s+(\w+)\s*=\s*(async\s+)?\(([^)]*)\)\s*=>/g,
                class: /class\s+(\w+)/g
            },
            python: {
                def: /def\s+(\w+)\s*\(([^)]*)\):/g,
                class: /class\s+(\w+)(?:\([^)]*\))?:/g
            }
        };
    }

    addComments(code, language) {
        let commentedCode = code;

        if (language === 'javascript') {
            // JS Functions
            commentedCode = commentedCode.replace(this.patterns.js.function, (match, async, name, params) => {
                return `${this.generateJSDoc(name, params)}\n${match}`;
            });
            // JS Arrow Functions
            commentedCode = commentedCode.replace(this.patterns.js.arrow, (match, type, name, async, params) => {
                return `${this.generateJSDoc(name, params)}\n${match}`;
            });
            // JS Classes
            commentedCode = commentedCode.replace(this.patterns.js.class, (match, name) => {
                return `/**\n * Class ${name}\n * Description of the class.\n */\n${match}`;
            });

        } else if (language === 'python') {
            // Python Def (Insert docstring AFTER the match, inside the function body)
            // This is trickier with regex replace alone because we need to insert *after* the colon and indentation.
            // Simplified approach: Insert before for now, or careful splice?
            // Standard python docstrings go INSIDE.
            // Let's do a split/join approach for better robustness or just insert before as "Header comments" if strictly requested?
            // "Header Documentation: Every function/class must have a header"
            // For python, commonly docstrings are inside. But let's try to allow standard header style or inside.
            // actually, regex replace logic is simplest if we put it before (comment style) or we need to detect indent.
            // Let's stick to putting standard Docstring format *after* the definition line with correct indentation.

            const lines = code.split('\n');
            const newLines = [];

            lines.forEach(line => {
                newLines.push(line);

                // Check class
                const classMatch = line.match(this.patterns.python.class);
                if (classMatch) {
                    const indent = this.getIndent(line) + '    ';
                    newLines.push(`${indent}"""\n${indent}Class ${classMatch[1]}\n${indent}Description.\n${indent}"""`);
                }

                // Check def
                const defMatch = line.match(this.patterns.python.def);
                if (defMatch) {
                    const indent = this.getIndent(line) + '    ';
                    newLines.push(`${indent}${this.generateDocString(defMatch[1], defMatch[2], indent)}`);
                }
            });
            commentedCode = newLines.join('\n');
        }

        return commentedCode;
    }

    getIndent(line) {
        const match = line.match(/^\s*/);
        return match ? match[0] : '';
    }

    generateJSDoc(name, paramsStr) {
        const params = paramsStr.split(',').map(p => p.trim()).filter(p => p);
        let doc = `/**\n * ${name} - Description\n`;
        params.forEach(param => {
            // Simple param name extraction (ignoring defaults for name)
            const cleanParam = param.split('=')[0].trim();
            doc += ` * @param {any} ${cleanParam} - Description\n`;
        });
        doc += ` * @returns {any} Description\n */`;
        return doc;
    }

    generateDocString(name, paramsStr, indent) {
        const params = paramsStr.split(',').map(p => p.trim()).filter(p => p);
        let doc = `"""\n${indent}${name} - Description\n\n${indent}Args:\n`;
        params.forEach(param => {
            const cleanParam = param.split('=')[0].split(':')[0].trim(); // Handle type hints and defaults
            doc += `${indent}    ${cleanParam} (Any): Description\n`;
        });
        doc += `\n${indent}Returns:\n${indent}    Any: Description\n${indent}"""`;
        return doc;
    }

    format(code, language) {
        if (!window.prettier || !window.prettierPlugins) {
            console.warn("Prettier not loaded");
            return code;
        }

        try {
            if (language === 'javascript') {
                return prettier.format(code, {
                    parser: "babel",
                    plugins: [prettierPlugins.babel, prettierPlugins.estree],
                    semi: true,
                    singleQuote: true
                });
            }
            // Add other languages if plugins available
            return code;
        } catch (e) {
            console.error("Prettier formatting error:", e);
            return code; // Return original on error
        }
    }
}

window.CodeCommenter = new CodeCommenter();
