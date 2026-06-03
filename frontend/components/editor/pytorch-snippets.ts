/** Monaco completion snippets for PyTorch 2.x */
export const PYTORCH_SNIPPETS = [
  {
    label: "nn.Linear",
    insertText: "nn.Linear(${1:in_features}, ${2:out_features})",
    detail: "Fully connected layer",
  },
  {
    label: "nn.Conv2d",
    insertText:
      "nn.Conv2d(${1:in_channels}, ${2:out_channels}, kernel_size=${3:3}, padding=${4:1})",
    detail: "2D convolution",
  },
  {
    label: "nn.ReLU",
    insertText: "nn.ReLU()",
    detail: "ReLU activation",
  },
  {
    label: "nn.Sequential",
    insertText: "nn.Sequential(\n\t${1:layers}\n)",
    detail: "Sequential container",
  },
  {
    label: "training_step",
    insertText:
      "optimizer.zero_grad()\noutputs = model(inputs)\nloss = criterion(outputs, targets)\nloss.backward()\noptimizer.step()",
    detail: "Canonical training step",
  },
  {
    label: "torch.randn",
    insertText: "torch.randn(${1:shape})",
    detail: "Random normal tensor",
  },
  {
    label: "F.relu",
    insertText: "F.relu(${1:x})",
    detail: "Functional ReLU",
  },
  {
    label: "F.cross_entropy",
    insertText: "F.cross_entropy(${1:logits}, ${2:targets})",
    detail: "Cross-entropy loss",
  },
  {
    label: "DataLoader",
    insertText:
      "DataLoader(${1:dataset}, batch_size=${2:32}, shuffle=${3:True}, num_workers=0)",
    detail: "PyTorch DataLoader",
  },
  {
    label: "no_grad",
    insertText: "with torch.no_grad():\n\t${1:pass}",
    detail: "Disable autograd",
  },
];
