from enum import Enum
from models.CodeLlamaModel import CodeLlamaModel
from models.OpenAIModelVector import OpenAIModelVector
from models.DeepSeekModel import DeepSeekModel
from models.ClaudeModel import ClaudeModel
from models.OpenAIModel import OpenAIModel

""" Options for command line arguments"""

def get_enum_values(enum_class):
    return [member.value for member in enum_class]

class Prompt(Enum):
    IMAGE_COMPARE = "image_compare"
    IMAGE_ANALYZE = "image_analyze"
    IMAGE_ANALYZE_ANNOTATION = "image_analyze_annotations"
    IMAGE_STYLE = "image_style"
    IMAGE_STYLE_ANNOTATIONS = "image_style_annotations"
    CODE_LINES = "code_lines"
    CODE_TEMPLATE = "code_template"
    CODE_TABLE = "code_table"
    CODE_HINT = "code_hint"
    CODE_EXPLANATION = "code_explanation"
    CODE_ANNOTATION = "code_annotation"

    def __str__(self):
        return self.value

class Scope(Enum):
    IMAGE = "image"
    CODE = "code"

    def __str__(self):
        return self.value
    
model_mapping = {
    "deepSeek-R1:70B": DeepSeekModel,
    "openai": OpenAIModel,
    "openai-vector": OpenAIModelVector,
    "codellama:latest": CodeLlamaModel,
    "claude-3.7-sonnet": ClaudeModel
}

class Models(Enum):
    OPENAI = "openai"
    OPENAIVECTOR = "openai-vector"
    LLAMA = "llama3.2-vision:90b"
    LLAVA = "llava:34b"
    DEEPSEEK = "deepSeek-R1:70B"
    CODELLAMA = "codellama:latest"
    CLAUDE = "claude-3.7-sonnet"

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
    DIRECT = "direct"

    def __str__(self):
        return self.value