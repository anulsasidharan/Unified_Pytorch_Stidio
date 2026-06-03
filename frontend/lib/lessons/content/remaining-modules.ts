import type { ModuleCurriculum } from "../types";

/** Shared lesson builder for modules with similar structure */
function tierLessons(
  topicSlug: string,
  topicName: string,
  basics: { title: string; summary: string; bullets: string[]; mermaid: string; code: string; apps: string[] },
  intermediate: typeof basics,
  advanced: typeof basics,
  introExtra: string[],
): ModuleCurriculum {
  return {
    topicSlug,
    intro: {
      overview: [
        `Welcome to **${topicName}**. This module follows a learn-first path: read each lesson, run the sample code, then attempt exercises.`,
        ...introExtra,
      ],
      learningPath: [
        `Lesson 1 — ${basics.title}`,
        `Lesson 2 — ${intermediate.title}`,
        `Lesson 3 — ${advanced.title}`,
        "Practice exercises when you feel ready",
      ],
      prerequisites: ["Complete earlier modules in order for best results"],
    },
    lessons: [
      {
        slug: "foundation",
        title: basics.title,
        order: 1,
        difficulty: "basic",
        summary: basics.summary,
        explanation: basics.bullets,
        mermaid: basics.mermaid,
        diagramCaption: `${topicName} — core concept overview`,
        sampleCode: [{ title: "Try it", code: basics.code, explanation: "Run locally or in Colab before exercises." }],
        realWorldApplications: basics.apps,
        keyTakeaways: basics.bullets.slice(0, 3).map((b) => b.replace(/\*\*/g, "")),
      },
      {
        slug: "applied",
        title: intermediate.title,
        order: 2,
        difficulty: "intermediate",
        summary: intermediate.summary,
        explanation: intermediate.bullets,
        mermaid: intermediate.mermaid,
        diagramCaption: `${topicName} — applied patterns`,
        sampleCode: [{ title: "Try it", code: intermediate.code, explanation: "Experiment by changing hyperparameters." }],
        realWorldApplications: intermediate.apps,
        keyTakeaways: intermediate.bullets.slice(0, 3).map((b) => b.replace(/\*\*/g, "")),
      },
      {
        slug: "production",
        title: advanced.title,
        order: 3,
        difficulty: "advanced",
        summary: advanced.summary,
        explanation: advanced.bullets,
        mermaid: advanced.mermaid,
        diagramCaption: `${topicName} — production considerations`,
        sampleCode: [{ title: "Try it", code: advanced.code, explanation: "Advanced patterns used in research and industry." }],
        realWorldApplications: advanced.apps,
        keyTakeaways: advanced.bullets.slice(0, 3).map((b) => b.replace(/\*\*/g, "")),
      },
    ],
  };
}

export const trainingLoopsCurriculum: ModuleCurriculum = tierLessons(
  "training-loops",
  "Training Loops & Optimization",
  {
    title: "The Canonical Training Loop",
    summary: "Epoch → batch → forward → loss → backward → step — the heartbeat of deep learning.",
    bullets: [
      "An **epoch** is one full pass over the training dataset.",
      "Inside each batch: move data to device, `model.train()`, forward, compute loss, `backward()`, `optimizer.step()`.",
      "Track running loss with `.item()` for logging; keep tensors on GPU during the loop.",
    ],
    mermaid: `flowchart TD
    E[Epoch] --> B[Batch]
    B --> F[forward]
    F --> L[loss]
    L --> BW[backward]
    BW --> S[optimizer.step]`,
    code: `for epoch in range(10):
    for x, y in loader:
        opt.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        opt.step()`,
    apps: ["Training classifiers on CIFAR-10", "Fine-tuning BERT on custom text"],
  },
  {
    title: "Optimizers & Learning Rate",
    summary: "SGD, Adam, and schedulers control how fast weights move in loss landscape.",
    bullets: [
      "**SGD** with momentum is classic; **Adam** adapts per-parameter learning rates — default for many projects.",
      "Learning rate too high → divergence; too low → slow convergence.",
      "`lr_scheduler` reduces LR when validation plateaus (e.g. `ReduceLROnPlateau`).",
    ],
    mermaid: `flowchart LR
    O[Optimizer] --> W[Weights]
    S[Scheduler] --> O`,
    code: `opt = torch.optim.Adam(model.parameters(), lr=1e-3)
sched = torch.optim.lr_scheduler.StepLR(opt, step_size=10, gamma=0.1)`,
    apps: ["AdamW in transformer training", "Cosine schedule in vision transformers"],
  },
  {
    title: "Regularization & Stability",
    summary: "Gradient clipping, weight decay, and mixed precision keep training stable.",
    bullets: [
      "`torch.nn.utils.clip_grad_norm_` prevents exploding gradients in RNNs/transformers.",
      "Weight decay (L2) in AdamW decouples from gradient update — standard in modern training.",
      "AMP (`torch.cuda.amp`) speeds training with automatic float16 where safe.",
    ],
    mermaid: `flowchart TB
    G[gradients] --> C[clip_grad_norm]
    C --> O[optimizer step]`,
    code: `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`,
    apps: ["LLM training with grad clipping", "Mixed precision on NVIDIA A100"],
  },
  ["You will implement the full loop that every PyTorch project shares."],
);

export const lossFunctionsCurriculum: ModuleCurriculum = tierLessons(
  "loss-functions",
  "Loss Functions & Metrics",
  {
    title: "Classification Losses",
    summary: "CrossEntropyLoss combines softmax + NLL for multi-class labels.",
    bullets: [
      "Model outputs **logits** (raw scores); CrossEntropy applies log-softmax internally.",
      "For binary tasks use `BCEWithLogitsLoss` with a single output neuron.",
      "Metrics like accuracy are not differentiable — compute outside autograd for logging.",
    ],
    mermaid: `flowchart LR
    LOG[logits] --> CE[CrossEntropyLoss]
    LBL[labels] --> CE
    CE --> SCALAR[scalar loss]`,
    code: `import torch.nn as nn
criterion = nn.CrossEntropyLoss()
loss = criterion(logits, targets)`,
    apps: ["Image classification", "Intent detection in chatbots"],
  },
  {
    title: "Regression & Custom Losses",
    summary: "MSE and L1 for continuous targets; compose custom losses from tensor ops.",
    bullets: [
      "`MSELoss` penalizes large errors quadratically — sensitive to outliers.",
      "`L1Loss` / Smooth L1 (Huber) used in object detection bounding boxes.",
      "Custom loss = any differentiable function; return a scalar tensor.",
    ],
    mermaid: `flowchart LR
    P[pred] --> M[MSE]
    T[target] --> M`,
    code: `loss = nn.MSELoss()(pred, target)`,
    apps: ["House price prediction", "Super-resolution image quality"],
  },
  {
    title: "Imbalanced & Multi-task Losses",
    summary: "Weight classes, combine losses, and metric learning with triplet losses.",
    bullets: [
      "Pass `weight=` to CrossEntropy for rare classes in medical diagnosis.",
      "Multi-task: `loss = loss_cls + 0.5 * loss_reg` — balance with coefficients.",
      "TripletMarginLoss pulls similar embeddings together in face recognition.",
    ],
    mermaid: `flowchart TB
    L1[loss_cls] --> SUM[+]
    L2[loss_aux] --> SUM`,
    code: `nn.TripletMarginLoss()(anchor, positive, negative)`,
    apps: ["Fraud detection (rare class)", "Face verification embeddings"],
  },
  ["Choosing the right loss is how you tell the model what 'good' means."],
);

export const datasetsCurriculum: ModuleCurriculum = tierLessons(
  "datasets-dataloaders",
  "Datasets & DataLoaders",
  {
    title: "Dataset & DataLoader Basics",
    summary: "Dataset defines __len__ and __getitem__; DataLoader batches and shuffles.",
    bullets: [
      "`TensorDataset` wraps tensors for quick experiments.",
      "`DataLoader(dataset, batch_size=32, shuffle=True)` yields (batch_x, batch_y) tuples.",
      "Collate function stacks samples into batched tensors automatically.",
    ],
    mermaid: `flowchart LR
    DS[Dataset] --> DL[DataLoader]
    DL --> B1[batch 1]
    DL --> B2[batch 2]`,
    code: `from torch.utils.data import DataLoader, TensorDataset
loader = DataLoader(TensorDataset(X, Y), batch_size=32, shuffle=True)`,
    apps: ["Any supervised training pipeline"],
  },
  {
    title: "Transforms & Custom Datasets",
    summary: "Augment images on the fly; read files from disk in __getitem__.",
    bullets: [
      "`torchvision.transforms` — Resize, RandomFlip, Normalize for images.",
      "Custom Dataset: store file paths in __init__, load image in __getitem__.",
      "Normalize with dataset-specific mean/std (e.g. ImageNet statistics).",
    ],
    mermaid: `flowchart LR
    IMG[raw image] --> T[transforms]
    T --> TENSOR[tensor batch]`,
    code: `transforms.Compose([transforms.Resize(224), transforms.ToTensor()])`,
    apps: ["Medical imaging pipelines", "Satellite imagery datasets"],
  },
  {
    title: "Performance & Distributed Loading",
    summary: "num_workers, pin_memory, and DistributedSampler for scale.",
    bullets: [
      "`num_workers>0` loads batches in parallel CPU processes.",
      "`pin_memory=True` speeds CPU→GPU transfer when using CUDA.",
      "DistributedSampler ensures each GPU sees disjoint shards per epoch.",
    ],
    mermaid: `flowchart TB
    W1[worker 0] --> Q[batch queue]
    W2[worker 1] --> Q
    Q --> GPU`,
    code: `DataLoader(ds, batch_size=64, num_workers=4, pin_memory=True)`,
    apps: ["Large-scale training on 8×GPU nodes", "Jupyter → production pipelines"],
  },
  ["Efficient data loading often determines GPU utilization."],
);

export const cnnsCurriculum: ModuleCurriculum = tierLessons(
  "cnns-computer-vision",
  "CNNs & Computer Vision",
  {
    title: "Convolutions & Feature Maps",
    summary: "Conv2d slides filters across images to detect local patterns (edges, textures).",
    bullets: [
      "Input shape NCHW: (batch, channels, height, width).",
      "`nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)` produces feature maps.",
      "Receptive field grows with depth — deeper layers see larger image context.",
    ],
    mermaid: `flowchart LR
    IMG[Image] --> C1[Conv + ReLU]
    C1 --> C2[Conv + ReLU]
    C2 --> P[Pooling]`,
    code: `nn.Conv2d(3, 16, kernel_size=3, padding=1)`,
    apps: ["Photo tagging", "Autonomous vehicle perception", "Quality inspection on factory lines"],
  },
  {
    title: "Pooling & CNN Architectures",
    summary: "Downsample with MaxPool; stack blocks like small VGG or ResNet stages.",
    bullets: [
      "`MaxPool2d` reduces spatial size, increases channel depth in classic designs.",
      "BatchNorm stabilizes activations between conv layers.",
      "torchvision.models provides pretrained ResNet, EfficientNet, etc.",
    ],
    mermaid: `flowchart TB
    B1[conv block] --> B2[conv block]
    B2 --> GAP[global avg pool]
    GAP --> FC[classifier]`,
    code: `from torchvision import models
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)`,
    apps: ["Radiology assist", "Retail shelf object detection"],
  },
  {
    title: "Advanced Vision Patterns",
    summary: "Transfer learning, U-Net skips, and multi-scale features for segmentation.",
    bullets: [
      "Replace `model.fc` for new class count when fine-tuning ResNet.",
      "U-Net: encoder path + decoder with skip connections for pixel-wise labels.",
      "Feature Pyramid Networks merge scales for object detection.",
    ],
    mermaid: `flowchart LR
    ENC[encoder] --> DEC[decoder]
    ENC -.skip.-> DEC`,
    code: `# freeze backbone, train new head
for p in model.parameters():
    p.requires_grad = False
model.fc = nn.Linear(512, num_classes)`,
    apps: ["Tumor segmentation in MRI", "Satellite land-use maps"],
  },
  ["Vision models power a huge share of deployed PyTorch systems."],
);

export const rnnsCurriculum: ModuleCurriculum = tierLessons(
  "rnns-lstms",
  "RNNs, LSTMs & Sequences",
  {
    title: "Sequential Data & RNNs",
    summary: "RNNs maintain a hidden state across time steps for sequences.",
    bullets: [
      "Input shape often (batch, seq_len, features).",
      "`nn.RNN` passes hidden state from step t to t+1.",
      "Vanishing gradients limit plain RNNs on long sequences — LSTM/GRU help.",
    ],
    mermaid: `flowchart LR
    x1[x_t-1] --> h1[h_t-1]
    x2[x_t] --> h2[h_t]
    h1 --> h2`,
    code: `rnn = nn.RNN(input_size=10, hidden_size=20, batch_first=True)`,
    apps: ["Time-series forecasting", "Sensor logs", "Early NLP before transformers"],
  },
  {
    title: "LSTM & GRU",
    summary: "Gated cells control what to remember and forget across long contexts.",
    bullets: [
      "`nn.LSTM` returns output sequence and final (h, c) states.",
      "Bidirectional stacks two RNNs — sees future and past (not for generation).",
      "`pack_padded_sequence` skips padding tokens efficiently.",
    ],
    mermaid: `flowchart TB
    LSTM[LSTM cell] --> G[gates: input, forget, output]`,
    code: `lstm = nn.LSTM(10, 20, num_layers=2, bidirectional=True, batch_first=True)`,
    apps: ["Speech recognition legacy models", "Anomaly detection in logs"],
  },
  {
    title: "Seq2Seq & Attention Preview",
    summary: "Encoder-decoder maps one sequence to another; attention focuses on relevant timesteps.",
    bullets: [
      "Encoder compresses input; decoder generates output token by token.",
      "Teacher forcing feeds ground-truth previous tokens during training.",
      "Attention (Module 09) largely replaced fixed-context LSTM encoders in NLP.",
    ],
    mermaid: `flowchart LR
    ENC[encoder] --> CTX[context]
    CTX --> DEC[decoder]`,
    code: `# conceptual: dec_out, (h, c) = decoder(emb, (h, c))`,
    apps: ["Machine translation (historical)", "Caption generation"],
  },
  ["Modern LLMs use transformers, but RNNs still appear in edge/time-series niches."],
);

export const transformersCurriculum: ModuleCurriculum = tierLessons(
  "transformers-attention",
  "Transformers & Attention",
  {
    title: "Attention Intuition",
    summary: "Attention weighs which inputs matter when producing each output.",
    bullets: [
      "Query, Key, Value vectors from linear projections of embeddings.",
      "Scores = QK^T / sqrt(d_k); softmax → weights; weighted sum of V.",
      "Self-attention: all positions attend to all positions in one sequence.",
    ],
    mermaid: `flowchart LR
    Q[Q] --> S[scores]
    K[K] --> S
    S --> W[softmax weights]
    W --> V[V]
    V --> O[output]`,
    code: `scores = Q @ K.transpose(-2, -1) / (Q.size(-1) ** 0.5)
weights = scores.softmax(dim=-1)
out = weights @ V`,
    apps: ["ChatGPT-style LLMs", "Vision transformers (ViT)", "Protein structure (AlphaFold)"],
  },
  {
    title: "Multi-Head & Transformer Block",
    summary: "Parallel heads learn different relationships; blocks stack depth.",
    bullets: [
      "Multi-head attention runs h parallel attention ops, concatenates results.",
      "Pre-norm vs post-norm LayerNorm placement affects training stability.",
      "Positional encoding injects order information (sinusoidal or learned).",
    ],
    mermaid: `flowchart TB
    X --> MHA[Multi-Head Attention]
    MHA --> ADD1[+ residual]
    ADD1 --> FFN[Feed Forward]
    FFN --> ADD2[+ residual]`,
    code: `nn.TransformerEncoderLayer(d_model=512, nhead=8, batch_first=True)`,
    apps: ["BERT fine-tuning", "Stable Diffusion text encoders"],
  },
  {
    title: "Masking & Efficient Variants",
    summary: "Causal masks for generation; FlashAttention for speed at scale.",
    bullets: [
      "Causal mask prevents attending to future tokens during language modeling.",
      "Padding masks ignore pad tokens in batched sentences.",
      "Research variants (Linformer, Performer) reduce O(n²) cost — production often uses optimized kernels.",
    ],
    mermaid: `flowchart TB
    CAU[causal mask] --> ATT[attention]
    PAD[padding mask] --> ATT`,
    code: `# attn_mask: upper triangular -inf for GPT-style training`,
    apps: ["Code completion APIs", "Document summarization"],
  },
  ["Transformers dominate modern PyTorch NLP and increasingly vision."],
);

export const transferLearningCurriculum: ModuleCurriculum = tierLessons(
  "transfer-learning",
  "Transfer Learning & Fine-tuning",
  {
    title: "Why Transfer Learning",
    summary: "Reuse features learned on large datasets; train less on your small task.",
    bullets: [
      "Pretrained weights encode general edges/textures or language syntax.",
      "Replace classifier head; train head first with frozen backbone.",
      "Unfreeze layers gradually for better adaptation.",
    ],
    mermaid: `flowchart LR
    PT[pretrained weights] --> FT[fine-tune on your data]`,
    code: `model = models.resnet50(weights=weights)
model.fc = nn.Linear(model.fc.in_features, num_classes)`,
    apps: ["Medical imaging with 500 labels", "Custom product classifier"],
  },
  {
    title: "Discriminative Learning Rates",
    summary: "Lower LR for early layers, higher for new head — protects generic features.",
    bullets: [
      "Parameter groups in optimizer: `[{'params': head.parameters(), 'lr': 1e-3}, {'params': backbone.parameters(), 'lr': 1e-5}]`.",
      "More augmentation when data is tiny to avoid overfitting.",
    ],
    mermaid: `flowchart TB
    HEAD[head lr high] --> OPT
    BACK[backbone lr low] --> OPT`,
    code: `optim = torch.optim.Adam([
    {"params": head.parameters(), "lr": 1e-3},
    {"params": backbone.parameters(), "lr": 1e-5},
])`,
    apps: ["HuggingFace Trainer fine-tunes", "Kaggle vision wins"],
  },
  {
    title: "PEFT & LoRA",
    summary: "Update small adapter matrices instead of full billion-parameter weights.",
    bullets: [
      "LoRA adds low-rank matrices to attention layers — huge memory savings.",
      "Freeze base model; only train adapters for deployment-specific tasks.",
      "Popular for LLM customization on consumer GPUs.",
    ],
    mermaid: `flowchart LR
    W[frozen W] --> OUT
    A[LoRA A·B] --> OUT`,
    code: `# libraries: peft, transformers integrate LoRA configs`,
    apps: ["Enterprise chatbots on private docs", "Style-tuned image models"],
  },
  ["Most production vision/NLP starts with a pretrained checkpoint."],
);

export const deploymentCurriculum: ModuleCurriculum = tierLessons(
  "model-deployment",
  "Model Saving & Deployment",
  {
    title: "Checkpoints & state_dict",
    summary: "Save learnable weights with torch.save(model.state_dict()).",
    bullets: [
      "Always save `state_dict`, not whole model pickle, for portability.",
      "Include optimizer and epoch in checkpoint dict for resume training.",
      "Load with `model.load_state_dict(torch.load(path))` after matching architecture.",
    ],
    mermaid: `flowchart LR
    TRAIN[training] --> CKPT[checkpoint .pt]
    CKPT --> INF[inference server]`,
    code: `torch.save(model.state_dict(), "weights.pt")
model.load_state_dict(torch.load("weights.pt", map_location=device))`,
    apps: ["Resume long GPU jobs", "Share weights across team"],
  },
  {
    title: "TorchScript & ONNX",
    summary: "Export graphs for C++ runtimes, mobile, or non-Python services.",
    bullets: [
      "`torch.jit.trace` records ops for fixed input shapes.",
      "`torch.onnx.export` targets ONNX Runtime, TensorRT, mobile engines.",
      "Watch for unsupported ops — test exported model outputs match PyTorch.",
    ],
    mermaid: `flowchart LR
    PT[PyTorch] --> ONNX[ONNX]
    ONNX --> TRT[TensorRT / mobile]`,
    code: `traced = torch.jit.trace(model, example_input)`,
    apps: ["Real-time inference APIs", "iOS/Android PyTorch Mobile"],
  },
  {
    title: "torch.compile & Serving",
    summary: "Compile for speed; batch requests in production with monitoring.",
    bullets: [
      "`model = torch.compile(model)` fuses kernels on PyTorch 2+.",
      "Serve with TorchServe, FastAPI + ONNX, or Triton Inference Server.",
      "Log latency, input drift, and OOD detection in production.",
    ],
    mermaid: `flowchart TB
    REQ[requests] --> BATCH[batch]
    BATCH --> COMPILE[compiled model]
    COMPILE --> RESP[responses]`,
    code: `model = torch.compile(model)  # PyTorch 2.x`,
    apps: ["E-commerce recommendation latency SLAs", "Fraud scoring microservices"],
  },
  ["Deployment is where models create business value."],
);

export const gpuCudaCurriculum: ModuleCurriculum = tierLessons(
  "gpu-cuda",
  "GPU / CUDA & Performance",
  {
    title: "CUDA Basics in PyTorch",
    summary: "device, to(cuda), and cuda.is_available() — fundamentals of GPU training.",
    bullets: [
      "One process per GPU is typical; use `cuda:0`, `cuda:1` explicitly in multi-GPU scripts.",
      "Synchronize only when needed — `torch.cuda.synchronize()` for accurate timing.",
      "Empty cache with `torch.cuda.empty_cache()` does not free memory held by tensors still in scope.",
    ],
    mermaid: `flowchart LR
    CPU[CPU tensors] -->|to device| GPU[GPU tensors]`,
    code: `device = torch.device("cuda:0")
x = x.to(device)`,
    apps: ["Any large model training"],
  },
  {
    title: "Profiling & Memory",
    summary: "Find bottlenecks with profiler; avoid OOM with batch size and checkpointing.",
    bullets: [
      "`torch.profiler` shows slow ops and kernel launches.",
      "Gradient checkpointing trades compute for activation memory.",
      "Mixed precision reduces memory footprint on modern GPUs.",
    ],
    mermaid: `flowchart TB
    PROF[profiler] --> BOTTLENECK[slow op]
    BOTTLENECK --> FIX[kernel / batch / AMP]`,
    code: `with torch.profiler.profile() as prof:
    model(x)`,
    apps: ["Optimize transformer training step", "Debug DataLoader stalls"],
  },
  {
    title: "Multi-GPU Training",
    summary: "DataParallel (simple) vs DistributedDataParallel (production).",
    bullets: [
      "`nn.DataParallel` — easy but slower; single-process multi-GPU.",
      "`DistributedDataParallel` — one process per GPU, scales to clusters.",
      "FSDP shards parameters for very large models that do not fit one GPU.",
    ],
    mermaid: `flowchart TB
    G0[GPU0] --> A[all-reduce grads]
    G1[GPU1] --> A`,
    code: `# DDP: torch.distributed.init_process_group + DistributedDataParallel(model)`,
    apps: ["Training LLMs on clusters", "Horovod / SLURM HPC jobs"],
  },
  ["Performance work comes after correct training loops."],
);

export const lightningCurriculum: ModuleCurriculum = tierLessons(
  "pytorch-lightning",
  "PyTorch Lightning & Best Practices",
  {
    title: "Why Lightning",
    summary: "Organize training code into LightningModule — less boilerplate, clearer structure.",
    bullets: [
      "`training_step`, `validation_step`, `configure_optimizers` replace manual loops.",
      "Trainer handles device placement, logging, checkpointing, early stopping.",
      "Keeps research code focused on model logic, not infrastructure.",
    ],
    mermaid: `flowchart LR
    LM[LightningModule] --> TR[Trainer]
    TR --> LOG[logs + checkpoints]`,
    code: `class LitModel(L.LightningModule):
    def training_step(self, batch, batch_idx):
        loss = ...
        return loss`,
    apps: ["Research labs standardizing experiments", "Kaggle teams moving fast"],
  },
  {
    title: "DataModule & Callbacks",
    summary: "LightningDataModule centralizes data; callbacks hook into training events.",
    bullets: [
      "DataModule: `setup`, `train_dataloader`, `val_dataloader`.",
      "Callbacks: ModelCheckpoint, EarlyStopping, LearningRateMonitor.",
      "Integrations: W&B, TensorBoard, MLflow loggers built-in.",
    ],
    mermaid: `flowchart TB
    DM[DataModule] --> TR[Trainer]
    CB[callbacks] --> TR`,
    code: `trainer = L.Trainer(max_epochs=10, callbacks=[ModelCheckpoint()])`,
    apps: ["Reproducible experiment grids", "Hyperparameter search"],
  },
  {
    title: "Fabric & Production Patterns",
    summary: "Lightning Fabric for custom loops; best practices for maintainable PyTorch.",
    bullets: [
      "Fabric: fine-grained control without full Trainer abstraction.",
      "Type hints, config files (Hydra), seed everything for reproducibility.",
      "Test small overfit batch before full dataset training.",
    ],
    mermaid: `flowchart LR
    FAB[Fabric] --> LOOP[your loop + less boilerplate]`,
    code: `fabric = Fabric(accelerator="cuda", devices=1)
fabric.launch()`,
    apps: ["Teams migrating from raw loops to structured training", "Large collaboration repos"],
  },
  ["Lightning is optional but teaches professional project structure."],
);
