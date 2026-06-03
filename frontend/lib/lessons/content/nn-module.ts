import type { ModuleCurriculum } from "../types";

export const nnModuleCurriculum: ModuleCurriculum = {
  topicSlug: "nn-module",
  intro: {
    overview: [
      "`nn.Module` is how you package layers, parameters, and forward logic into reusable building blocks — the LEGO bricks of deep learning.",
      "Subclasses implement `__init__` (define layers) and `forward` (data flow). PyTorch registers parameters automatically when you assign `nn.Linear`, `nn.Conv2d`, etc.",
      "Containers like `nn.Sequential` stack layers; understanding parameter shapes helps you debug dimension errors before runtime.",
    ],
    learningPath: [
      "Build a custom nn.Module",
      "Use layers, activations, and Sequential",
      "Parameters, buffers, and weight init",
      "Practice exercises",
    ],
    prerequisites: ["Tensors", "Autograd basics"],
  },
  lessons: [
    {
      slug: "nn-module-basics",
      title: "nn.Module & forward()",
      order: 1,
      difficulty: "basic",
      summary: "Encapsulate layers in a class; call the model like a function — it runs forward().",
      explanation: [
        "Never call `forward()` directly for training — use `model(x)` so hooks and autograd work correctly.",
        "Child modules assigned in `__init__` are tracked: `self.fc = nn.Linear(10, 2)` registers weights.",
        "Activations (`ReLU`, `Softmax`) are separate modules or functional APIs (`F.relu`).",
      ],
      mermaid: `flowchart LR
    X["input x"] --> M["MyModel.forward"]
    M --> L1["Linear"]
    L1 --> A["ReLU"]
    A --> L2["Linear"]
    L2 --> Y["output"]`,
      diagramCaption: "forward() defines the path from input tensor to prediction.",
      sampleCode: [
        {
          title: "Tiny classifier",
          code: `import torch
from torch import nn

class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 2),
        )
    def forward(self, x):
        return self.net(x)

model = TinyNet()
print(model(torch.randn(16, 4)).shape)  # [16, 2]`,
          explanation: "Batch dimension 16 flows through unchanged except in the class dimension.",
        },
      ],
      realWorldApplications: [
        "Custom heads on pretrained vision backbones",
        "Multi-input models (tabular + image) with several submodules",
      ],
      keyTakeaways: ["Subclass nn.Module", "Define layers in __init__", "Implement forward"],
    },
    {
      slug: "layers-and-parameters",
      title: "Layers, Parameters & Initialization",
      order: 2,
      difficulty: "intermediate",
      summary: "Linear and Conv layers own learnable weights; init affects whether training converges.",
      explanation: [
        "`model.parameters()` yields all `nn.Parameter` tensors for the optimizer.",
        "`nn.Parameter` can wrap custom learnable scalars (e.g. temperature in contrastive learning).",
        "Bad initialization → saturated activations or vanishing gradients; use `nn.init` helpers.",
      ],
      mermaid: `flowchart TB
    M["nn.Module"] --> P["nn.Parameter — weights"]
    M --> B["buffers — running stats, not trained"]
    P --> O["Optimizer"]`,
      diagramCaption: "Only Parameters receive gradients; buffers move with .to(device) but are not updated by SGD.",
      sampleCode: [
        {
          title: "Count parameters",
          code: `total = sum(p.numel() for p in model.parameters())
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(total, trainable)`,
          explanation: "Compare model sizes before downloading large checkpoints.",
        },
      ],
      realWorldApplications: [
        "GPT-scale models: billions of parameters in Linear layers",
        "Custom ScaleLayer with learnable scalar (see exercises)",
      ],
      keyTakeaways: ["parameters() for optimizer", "Buffers for BatchNorm running mean"],
      relatedQuestionSlugs: ["custom-layer-forward", "weight-tying"],
    },
    {
      slug: "containers-and-composition",
      title: "Sequential, ModuleList & Skip Connections",
      order: 3,
      difficulty: "advanced",
      summary: "Compose depth with containers; ResNet-style skips need explicit forward wiring.",
      explanation: [
        "`nn.Sequential` only works for straight pipelines — no branches.",
        "ResNets add input to output: `return F.relu(x + self.block(x))` — requires custom forward.",
        "ModuleDict / ModuleList help when you need dynamic layer sets.",
      ],
      mermaid: `flowchart LR
    IN["x"] --> B["block(x)"]
    IN --> ADD["+"]
    B --> ADD
    ADD --> OUT["out"]`,
      diagramCaption: "Residual connection: gradient can flow directly through the skip path.",
      sampleCode: [
        {
          title: "Residual block sketch",
          code: `class ResBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, dim), nn.ReLU(),
            nn.Linear(dim, dim),
        )
    def forward(self, x):
        return torch.relu(x + self.block(x))`,
          explanation: "Skip connections made very deep networks trainable — foundation of modern vision.",
        },
      ],
      realWorldApplications: ["ResNet, U-Net skip paths", "Transformer blocks with residual + norm"],
      keyTakeaways: ["Sequential for chains", "Custom forward for branches and skips"],
    },
  ],
};
