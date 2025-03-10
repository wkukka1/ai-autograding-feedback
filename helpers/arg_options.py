from enum import Enum

""" Options for command line arguments"""

def get_enum_values(enum_class):
    return [member.value for member in enum_class]

class Prompt(Enum):
    IMAGE_COMPARE = "image_compare"
    IMAGE_ANALYZE = "image_analyze"
    IMAGE_STYLE = "image_style"
    CODE_LINES = "code_lines"
    CODE_TEMPLATE = "code_template"
    CODE_TABLE = "code_table"
    CODE_HINT = "code_hint"
    CODE_EXPLAIN = "code_explain"

    def __str__(self):
        return self.value

class Scope(Enum):
    IMAGE = "image"
    CODE = "code"

    def __str__(self):
        return self.value
    
class Models(Enum):
    OPENAI = "openai"
    LLAMA = "llama3.2-vision:90b"
    DEEPSEEK = "deepSeek-R1:70B"
    CODELLAMA = "codellama:latest"

    def __str__(self):
        return self.value
    
class FileType(Enum):
    JUPYTER = "jupyter"
    PYTHON = "python"

    def __str__(self):
        return self.value
    
class OutputType(Enum):
    STDOUT = "stdout"
    MARKDOWN = "markdown"

    def __str__(self):
        return self.value