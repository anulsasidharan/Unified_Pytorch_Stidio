/** Monaco completion snippets for Python 3.11+ */

export const PYTHON_SNIPPETS = [
  {
    label: "def",
    insertText: "def ${1:name}(${2:args}):\n    ${3:pass}",
    detail: "Function definition",
  },
  {
    label: "class",
    insertText: "class ${1:Name}:\n    def __init__(self, ${2:args}):\n        ${3:pass}",
    detail: "Class definition",
  },
  {
    label: "for",
    insertText: "for ${1:item} in ${2:iterable}:\n    ${3:pass}",
    detail: "For loop",
  },
  {
    label: "comp",
    insertText: "[${1:expr} for ${2:item} in ${3:iterable}]",
    detail: "List comprehension",
  },
  {
    label: "with",
    insertText: "with open(${1:path}, ${2:'r'}) as f:\n    ${3:data = f.read()}",
    detail: "Context manager (file)",
  },
  {
    label: "main",
    insertText: 'if __name__ == "__main__":\n    ${1:main()}',
    detail: "Script entry point",
  },
] as const;
