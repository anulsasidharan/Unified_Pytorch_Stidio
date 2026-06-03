import type { ModuleCurriculum } from "../types";

export const tensorsCurriculum: ModuleCurriculum = {
  topicSlug: "tensors",
  intro: {
    overview: [
      "Every PyTorch program starts with tensors — multi-dimensional arrays that hold your data, model weights, and intermediate activations.",
      "Think of a tensor as a generalization of scalars (0D), vectors (1D), matrices (2D), and higher-dimensional grids (3D+). Images are 3D tensors (channels × height × width); batches add a fourth dimension.",
      "Before writing neural networks, you need to be comfortable creating tensors, inspecting their shape and dtype, and applying element-wise and reduction operations.",
    ],
    learningPath: [
      "Understand what a tensor is and how shape/dtype work",
      "Create tensors from Python lists, NumPy, and factory functions",
      "Index, slice, reshape, and broadcast tensors",
      "Practice with guided exercises",
    ],
    prerequisites: ["Basic Python", "Optional: NumPy arrays (similar mental model)"],
  },
  lessons: [
    {
      slug: "what-is-a-tensor",
      title: "What is a Tensor?",
      order: 1,
      difficulty: "basic",
      summary: "Tensors are PyTorch's core data structure — like NumPy arrays with GPU and autograd support.",
      explanation: [
        "A **tensor** stores numbers in a regular grid with a **shape** (e.g. `[3, 224, 224]` for 3 color channels and a 224×224 image) and a **dtype** (e.g. `float32` for weights, `int64` for class labels).",
        "PyTorch tensors can live on **CPU** or **GPU** (`cuda`). Moving data to the GPU is what makes deep learning training fast.",
        "Unlike plain Python lists, tensor operations are **vectorized** — PyTorch runs them in optimized C++/CUDA code, often in parallel across thousands of cores.",
        "Later modules will attach **autograd** to tensors so PyTorch can compute gradients automatically. For now, focus on shape and dtype — most bugs in deep learning are shape mismatches.",
      ],
      mermaid: `flowchart TB
    subgraph dims["Tensor dimensions"]
      S["0D — scalar<br/>torch.tensor(3.14)"]
      V["1D — vector<br/>shape [5]"]
      M["2D — matrix<br/>shape [3, 4]"]
      I["3D — image batch slice<br/>shape [C, H, W]"]
      B["4D — mini-batch<br/>shape [N, C, H, W]"]
    end
    S --> V --> M --> I --> B`,
      diagramCaption: "Each extra dimension adds structure: batch → channels → height → width is the standard image layout.",
      sampleCode: [
        {
          title: "Inspect shape and dtype",
          code: `import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
print(x.shape)   # torch.Size([2, 2])
print(x.dtype)   # torch.float32
print(x.device)  # cpu`,
          explanation: "Always print `.shape`, `.dtype`, and `.device` when debugging — they tell you what operation is valid.",
        },
        {
          title: "Create common tensors",
          code: `import torch

a = torch.tensor([1, 2, 3, 4, 5])      # from Python list
b = torch.zeros(2, 3)                   # 2×3 zeros
c = torch.ones(3, 3)                    # 3×3 ones
d = torch.rand(4, 4)                    # uniform [0, 1)

print(a.shape, b.shape, c.shape, d.shape)`,
          explanation: "Factory functions (`zeros`, `ones`, `rand`) are faster than building from nested Python lists for large arrays.",
        },
      ],
      realWorldApplications: [
        "Image classification: pixel values stored as float tensors normalized to [0, 1]",
        "NLP: token IDs as integer tensors fed into embedding layers",
        "Tabular ML: each row of a spreadsheet becomes a 1D feature tensor",
        "Reinforcement learning: game state vectors as 1D tensors",
      ],
      keyTakeaways: [
        "Shape tells you how many elements along each axis; dtype tells you the numeric type.",
        "Use `torch.tensor()` for small data; use `zeros`/`ones`/`rand` for allocations.",
        "Print shape before and after every transform during learning.",
      ],
      relatedQuestionSlugs: ["create-first-tensor", "tensor-from-list"],
    },
    {
      slug: "indexing-and-reshaping",
      title: "Indexing, Slicing & Reshaping",
      order: 2,
      difficulty: "basic",
      summary: "Select parts of tensors and change their shape without copying data when possible.",
      explanation: [
        "Indexing works like NumPy: `x[0]`, `x[:, 1]`, `x[1:3, :]`. A **view** shares memory with the original tensor; in-place writes on a view affect the parent.",
        "`view()` and `reshape()` change interpretation of the same data (total elements must match). `permute()` swaps dimension order — essential for images (NCHW vs NHWC).",
        "**Broadcasting** lets PyTorch apply operations between tensors of different shapes when dimensions are compatible (e.g. add a bias vector to every row of a batch matrix).",
        "Getting comfortable with `unsqueeze` / `squeeze` prevents silent shape bugs when batching data.",
      ],
      mermaid: `flowchart LR
    A["Tensor [4, 3]"] --> B["x[0, :] → row vector [3]"]
    A --> C["view(12) → [12]"]
    A --> D["unsqueeze(0) → [1, 4, 3]"]
    D --> E["broadcast with [3] bias"]`,
      diagramCaption: "Reshape and indexing change how you read the same underlying storage.",
      sampleCode: [
        {
          title: "Slice and reshape",
          code: `import torch

x = torch.arange(12).reshape(3, 4)
row0 = x[0]           # first row
col1 = x[:, 1]        # second column
flat = x.view(-1)     # 12 elements, -1 infers size

print(row0.shape, col1.shape, flat.shape)`,
          explanation: "`-1` in `view(-1)` means 'infer this dimension' from the total element count.",
        },
        {
          title: "Broadcasting",
          code: `import torch

batch = torch.randn(32, 10)   # 32 samples, 10 features
bias = torch.randn(10)          # per-feature bias
out = batch + bias              # bias broadcasts across batch dim

print(out.shape)  # torch.Size([32, 10])`,
          explanation: "PyTorch aligns trailing dimensions; size-1 dimensions stretch automatically.",
        },
      ],
      realWorldApplications: [
        "Cropping regions of interest in medical imaging (slice a 3D volume)",
        "Flattening image patches before a fully connected layer",
        "Adding per-channel normalization constants in batch norm",
      ],
      keyTakeaways: [
        "Prefer `view`/`reshape` when element count stays the same.",
        "Use `permute` when channel/order matters for conv layers.",
        "Broadcasting avoids slow Python loops over batches.",
      ],
      relatedQuestionSlugs: ["tensor-indexing", "reshape-view", "broadcast-add"],
    },
    {
      slug: "tensor-operations",
      title: "Math & Reduction Operations",
      order: 3,
      difficulty: "intermediate",
      summary: "Element-wise ops, matrix multiply, and reductions (`sum`, `mean`, `argmax`) power most forward passes.",
      explanation: [
        "Element-wise ops (`+`, `*`, `relu`) apply to each entry independently. **Matrix multiply** uses `@` or `torch.matmul` — the workhorse of linear layers.",
        "Reductions collapse dimensions: `x.sum(dim=0)` sums along rows. `keepdim=True` preserves reduced axes as size 1 for broadcasting.",
        "`torch.no_grad()` is used later for inference; for now, know that not every tensor needs gradients during data prep.",
        "Comparing tensors with `==` returns a boolean tensor; use `.all()` or `.any()` for single True/False answers.",
      ],
      mermaid: `flowchart TB
    T["Input tensor"] --> E["Element-wise: +, *, relu"]
    T --> M["matmul / @ — linear layers"]
    T --> R["Reductions: sum, mean, max"]
    R --> L["Loss scalars for training"]`,
      diagramCaption: "Forward passes chain element-wise ops, matmuls, and reductions into a scalar loss.",
      sampleCode: [
        {
          title: "Matrix multiply",
          code: `import torch

W = torch.randn(10, 5)   # weights: in_features → out_features
x = torch.randn(32, 10)    # batch of 32 vectors
y = x @ W                  # (32, 10) @ (10, 5) → (32, 5)

print(y.shape)`,
          explanation: "This is exactly what `nn.Linear(10, 5)` does internally on a batch of inputs.",
        },
        {
          title: "Reductions with keepdim",
          code: `import torch

x = torch.randn(4, 3)
mean_per_col = x.mean(dim=0, keepdim=True)
print(mean_per_col.shape)  # torch.Size([1, 3])`,
          explanation: "`keepdim=True` keeps shapes compatible for broadcasting in normalization code.",
        },
      ],
      realWorldApplications: [
        "Cosine similarity in recommendation systems (dot products of embedding tensors)",
        "Aggregating time-series sensor readings with `mean`/`max` over time dim",
        "Softmax + cross-entropy built from `exp`, `sum`, and `log` on logits",
      ],
      keyTakeaways: [
        "Check matmul shapes: (N, A) @ (A, B) → (N, B).",
        "Pick the correct `dim` for reductions — wrong dim = wrong statistics.",
        "Use vectorized ops; avoid Python for-loops over tensor elements.",
      ],
      relatedQuestionSlugs: ["matmul-basics", "reduction-dim", "element-wise-ops"],
    },
    {
      slug: "gpu-and-dtype",
      title: "Devices, dtypes & Performance Basics",
      order: 4,
      difficulty: "advanced",
      summary: "Move tensors to GPU, pick dtypes wisely, and avoid accidental CPU/GPU sync.",
      explanation: [
        "Use `.to(device)` or `tensor.cuda()` to move tensors to GPU. **Model and data must be on the same device** before forward pass.",
        "Mixed precision (`float16` / `bfloat16`) speeds training on modern GPUs; master `float32` first.",
        "Contiguous memory layout matters for some CUDA kernels — call `.contiguous()` after `permute` if you see performance warnings.",
        "Cloning (`tensor.clone()`) creates an independent copy; views do not.",
      ],
      mermaid: `sequenceDiagram
    participant CPU
    participant GPU
    CPU->>GPU: tensor.to("cuda")
    GPU->>GPU: forward + backward
    GPU->>CPU: .item() / .cpu() for logging`,
      diagramCaption: "Minimize CPU↔GPU transfers; keep the training loop hot on GPU.",
      sampleCode: [
        {
          title: "Device placement",
          code: `import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.randn(3, 3, device=device)
model = torch.nn.Linear(3, 2).to(device)
y = model(x)
print(y.device)`,
          explanation: "Pattern: create `device` once, move model and batches to it in the training loop.",
        },
      ],
      realWorldApplications: [
        "Training ResNet on 8× GPU servers — all batches pinned to CUDA",
        "Edge deployment on CPU with `float32` or quantized `int8` tensors",
        "Scientific computing: `float64` on CPU for numerical stability",
      ],
      keyTakeaways: [
        "One device per forward pass — no mixing CPU weights with GPU data.",
        "Use `.item()` only when you need a Python number (slow on GPU).",
        "Start with float32; optimize dtypes after the loop works.",
      ],
      relatedQuestionSlugs: ["device-transfer", "dtype-cast"],
    },
  ],
};
