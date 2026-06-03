import type { ModuleCurriculum } from "../types";

export const autogradCurriculum: ModuleCurriculum = {
  topicSlug: "autograd",
  intro: {
    overview: [
      "Neural networks learn by adjusting weights to reduce a loss. **Autograd** is PyTorch's engine that computes those adjustments automatically via calculus (chain rule).",
      "When `requires_grad=True`, PyTorch records every operation on a tensor into a **computation graph**. Calling `.backward()` on a scalar loss propagates gradients backward to every leaf parameter.",
      "You do not implement backprop by hand for standard layers — but you must understand when gradients flow, when they are blocked, and how to debug vanishing or exploding values.",
    ],
    learningPath: [
      "Learn computation graphs and `requires_grad`",
      "Practice `.backward()` and reading `.grad`",
      "Detach, freeze, and custom autograd functions",
      "Apply concepts in exercises",
    ],
    prerequisites: ["Module 01 — Tensors & Operations"],
  },
  lessons: [
    {
      slug: "computation-graph",
      title: "Computation Graphs & requires_grad",
      order: 1,
      difficulty: "basic",
      summary: "PyTorch builds a graph of operations so it can differentiate your loss with respect to parameters.",
      explanation: [
        "Set `requires_grad=True` on tensors that should receive gradients (usually **model parameters** and sometimes inputs for research).",
        "Operations on tracked tensors are recorded. The graph is implicit — you do not draw it manually.",
        "Only **scalar** losses can call `.backward()` directly; for vector losses use `.sum()` or `.mean()` first.",
        "Leaf tensors are graph entry points; their `.grad` fields fill after backward.",
      ],
      mermaid: `flowchart BT
    L["loss (scalar)"] --> A["activation"]
    A --> W["weights (requires_grad)"]
    W --> I["input"]
    L -.->|backward| G["∂loss/∂weights stored in .grad"]`,
      diagramCaption: "Gradients flow backward from loss to each parameter with requires_grad=True.",
      sampleCode: [
        {
          title: "Simple gradient",
          code: `import torch

x = torch.tensor([2.0], requires_grad=True)
y = x ** 2
y.backward()
print(x.grad)  # tensor([4.])  because d(x²)/dx = 2x`,
          explanation: "dy/dx = 2x; at x=2 the gradient is 4.",
        },
      ],
      realWorldApplications: [
        "Training any neural net: loss.backward() then optimizer.step()",
        "Sensitivity analysis: gradients of outputs w.r.t. inputs in finance/simulation",
        "Neural style transfer: gradients w.r.t. image pixels",
      ],
      keyTakeaways: [
        "requires_grad on parameters; backward from scalar loss.",
        "x.grad accumulates — zero grad between steps with optimizer.zero_grad().",
      ],
      relatedQuestionSlugs: ["conceptual-graph-mcq", "simple-backward"],
    },
    {
      slug: "backward-and-grad",
      title: "backward(), grad & Optimizer Step",
      order: 2,
      difficulty: "intermediate",
      summary: "The training triad: zero_grad → backward → step uses autograd gradients to update weights.",
      explanation: [
        "`optimizer.zero_grad()` clears old gradients (they accumulate by default).",
        "`loss.backward()` computes ∂loss/∂θ for all parameters θ in the graph.",
        "`optimizer.step()` applies the update rule (SGD, Adam, …) using `.grad`.",
        "If loss does not decrease, check: graph disconnected? grad None? learning rate too high?",
      ],
      mermaid: `sequenceDiagram
    participant O as Optimizer
    participant M as Model
    participant L as Loss
    O->>O: zero_grad()
    M->>L: forward
    L->>L: backward()
    O->>M: step() updates weights`,
      diagramCaption: "Every training iteration repeats this cycle.",
      sampleCode: [
        {
          title: "Mini training step",
          code: `import torch
from torch import nn

model = nn.Linear(1, 1)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
x = torch.tensor([[1.0]])
target = torch.tensor([[2.0]])

opt.zero_grad()
pred = model(x)
loss = (pred - target).pow(2).mean()
loss.backward()
opt.step()
print(loss.item())`,
          explanation: "After step, loss should drop over many iterations on this toy problem.",
        },
      ],
      realWorldApplications: [
        "Fine-tuning LLMs: same loop at billion-parameter scale with AdamW",
        "Physics-informed ML: custom loss terms each contributing to backward",
      ],
      keyTakeaways: [
        "Always zero_grad before backward in standard loops.",
        "Inspect param.grad is not None for parameters you expect to train.",
      ],
    },
    {
      slug: "detach-and-freeze",
      title: "detach(), no_grad & Freezing Layers",
      order: 3,
      difficulty: "advanced",
      summary: "Control where gradients flow — essential for transfer learning and inference.",
      explanation: [
        "`tensor.detach()` cuts the graph; downstream ops do not backprop into detached inputs.",
        "`with torch.no_grad():` disables tracking for inference or metric computation — saves memory and speed.",
        "Freezing: set `requires_grad=False` on parameters you do not want to update (e.g. pretrained backbone).",
        "`torch.utils.checkpoint` trades compute for memory by not storing all activations — advanced training trick.",
      ],
      mermaid: `flowchart LR
    P["pretrained backbone<br/>requires_grad=False"] --> H["new head<br/>requires_grad=True"]
    H --> L["loss"]
    L -.->|gradients only| H`,
      diagramCaption: "Transfer learning: train the head, freeze the backbone.",
      sampleCode: [
        {
          title: "Freeze backbone",
          code: `for param in backbone.parameters():
    param.requires_grad = False

# only head parameters appear in optimizer if you pass head.parameters()`,
          explanation: "Frozen parameters still run forward; they just do not receive .grad updates.",
        },
      ],
      realWorldApplications: [
        "Image classifiers with frozen ResNet features + trainable linear head",
        "Evaluation loops wrapped in torch.no_grad()",
        "Exporting ONNX — inference without autograd",
      ],
      keyTakeaways: [
        "no_grad for inference; detach for stopping grad through a tensor.",
        "Optimizer must only include parameters you intend to train.",
      ],
      relatedQuestionSlugs: ["grad-checkpoint-concept"],
    },
  ],
};
