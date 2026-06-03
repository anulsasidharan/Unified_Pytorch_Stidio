"""
Seed Module 07 — CNNs & Computer Vision (20 exercises).
Usage: python -m seeds.questions_cnns
"""

import asyncio

from seeds.loader import build_exercise, seed_questions_for_topic

TOPIC_SLUG = "cnns-computer-vision"

_SPECS: list[tuple] = [
    ("Conv2d output shape", "conv2d-output-shape", "basic", "Apply `Conv2d(3, 16, kernel_size=3, padding=1)` on `(1,3,32,32)`.", "import torch\nfrom torch import nn\nx = torch.randn(1, 3, 32, 32)\nconv = nn.Conv2d(3, 16, kernel_size=3, padding=1)\nprint(conv(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 3, 32, 32)\nconv = nn.Conv2d(3, 16, kernel_size=3, padding=1)\nprint(conv(x).shape)", ["cnn", "conv"], "code_completion"),
    ("MaxPool2d downsample", "maxpool2d-downsample", "basic", "Pool `(1,8,16,16)` with kernel 2 stride 2.", "import torch\nfrom torch import nn\nx = torch.randn(1, 8, 16, 16)\npool = nn.MaxPool2d(2, stride=2)\nprint(pool(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 8, 16, 16)\npool = nn.MaxPool2d(2, stride=2)\nprint(pool(x).shape)", ["cnn", "pool"], "code_completion"),
    ("Simple CNN block", "simple-cnn-block", "basic", "Sequential Conv-ReLU-Pool on dummy image.", "import torch\nfrom torch import nn\nx = torch.randn(2, 1, 28, 28)\nblock = nn.Sequential(\n    nn.Conv2d(1, 8, 3, padding=1),\n    nn.ReLU(),\n    nn.MaxPool2d(2),\n)\nprint(block(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(2, 1, 28, 28)\nblock = nn.Sequential(\n    nn.Conv2d(1, 8, 3, padding=1),\n    nn.ReLU(),\n    nn.MaxPool2d(2),\n)\nprint(block(x).shape)", ["cnn", "block"], "code_completion"),
    ("BatchNorm2d in CNN", "batchnorm2d-in-cnn", "basic", "Conv + BatchNorm2d + ReLU forward.", "import torch\nfrom torch import nn\nx = torch.randn(4, 3, 16, 16)\nlayer = nn.Sequential(nn.Conv2d(3, 6, 3, padding=1), nn.BatchNorm2d(6), nn.ReLU())\nprint(layer(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(4, 3, 16, 16)\nlayer = nn.Sequential(nn.Conv2d(3, 6, 3, padding=1), nn.BatchNorm2d(6), nn.ReLU())\nprint(layer(x).shape)", ["cnn", "batchnorm"], "code_completion"),
    ("Flatten for classifier", "flatten-for-classifier", "basic", "Flatten `(2,8,7,7)` then Linear to 10 classes.", "import torch\nfrom torch import nn\nx = torch.randn(2, 8, 7, 7)\nprint(nn.Sequential(nn.Flatten(), nn.Linear(8*7*7, 10))(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(2, 8, 7, 7)\nprint(nn.Sequential(nn.Flatten(), nn.Linear(8*7*7, 10))(x).shape)", ["cnn", "classifier"], "code_completion"),
    ("LeNet-style stack", "lenet-style-stack", "basic", "Build tiny LeNet: 2 conv layers + linear head for 10 classes.", "import torch\nfrom torch import nn\nclass TinyLeNet(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.features = nn.Sequential(\n            nn.Conv2d(1, 6, 5), nn.ReLU(), nn.MaxPool2d(2),\n            nn.Conv2d(6, 16, 5), nn.ReLU(), nn.MaxPool2d(2),\n        )\n        self.classifier = nn.Linear(16 * 4 * 4, 10)\n    def forward(self, x):\n        x = self.features(x)\n        return self.classifier(x.flatten(1))\nprint(TinyLeNet()(torch.randn(1,1,28,28)).shape)", "import torch\nfrom torch import nn\nclass TinyLeNet(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.features = nn.Sequential(\n            nn.Conv2d(1, 6, 5), nn.ReLU(), nn.MaxPool2d(2),\n            nn.Conv2d(6, 16, 5), nn.ReLU(), nn.MaxPool2d(2),\n        )\n        self.classifier = nn.Linear(16 * 4 * 4, 10)\n    def forward(self, x):\n        x = self.features(x)\n        return self.classifier(x.flatten(1))\nprint(TinyLeNet()(torch.randn(1,1,28,28)).shape)", ["cnn", "lenet"], "code_completion"),
    ("AdaptiveAvgPool", "adaptive-avgpool", "basic", "Use `AdaptiveAvgPool2d((1,1))` before classifier.", "import torch\nfrom torch import nn\nx = torch.randn(2, 512, 7, 7)\nprint(nn.AdaptiveAvgPool2d((1, 1))(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(2, 512, 7, 7)\nprint(nn.AdaptiveAvgPool2d((1, 1))(x).shape)", ["cnn", "pool"], "code_completion"),
    ("Conv stride effect", "conv-stride-effect", "basic", "Conv2d stride=2 halves spatial dims (with appropriate k/p).", "import torch\nfrom torch import nn\nx = torch.randn(1, 3, 32, 32)\nconv = nn.Conv2d(3, 8, kernel_size=3, stride=2, padding=1)\nprint(conv(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 3, 32, 32)\nconv = nn.Conv2d(3, 8, kernel_size=3, stride=2, padding=1)\nprint(conv(x).shape)", ["cnn", "conv"], "code_completion"),
    ("ResNet basic block", "resnet-basic-block", "intermediate", "Implement residual add: `out = F.relu(conv(x) + x)` with channel match.", "import torch\nfrom torch import nn\nimport torch.nn.functional as F\nx = torch.randn(2, 16, 8, 8)\nconv = nn.Conv2d(16, 16, 3, padding=1)\nout = F.relu(conv(x) + x)\nprint(out.shape)", "import torch\nfrom torch import nn\nimport torch.nn.functional as F\nx = torch.randn(2, 16, 8, 8)\nconv = nn.Conv2d(16, 16, 3, padding=1)\nout = F.relu(conv(x) + x)\nprint(out.shape)", ["cnn", "resnet"], "code_completion"),
    ("Depthwise separable conv", "depthwise-separable", "intermediate", "Depthwise 3x3 then pointwise 1x1 conv.", "import torch\nfrom torch import nn\nx = torch.randn(1, 8, 16, 16)\ndepthwise = nn.Conv2d(8, 8, 3, padding=1, groups=8)\npointwise = nn.Conv2d(8, 16, 1)\nprint(pointwise(depthwise(x)).shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 8, 16, 16)\ndepthwise = nn.Conv2d(8, 8, 3, padding=1, groups=8)\npointwise = nn.Conv2d(8, 16, 1)\nprint(pointwise(depthwise(x)).shape)", ["cnn", "efficient"], "code_completion"),
    ("Feature map count", "feature-map-count", "intermediate", "Print number of output channels after conv stack.", "import torch\nfrom torch import nn\nm = nn.Sequential(nn.Conv2d(3, 32, 3, padding=1), nn.Conv2d(32, 64, 3, padding=1))\nx = torch.randn(1, 3, 24, 24)\nprint(m(x).shape[1])", "import torch\nfrom torch import nn\nm = nn.Sequential(nn.Conv2d(3, 32, 3, padding=1), nn.Conv2d(32, 64, 3, padding=1))\nx = torch.randn(1, 3, 24, 24)\nprint(m(x).shape[1])", ["cnn", "features"], "code_completion"),
    ("Global average pool head", "gap-classifier-head", "intermediate", "GAP + Linear classifier on `(N,C,H,W)`.", "import torch\nfrom torch import nn\nx = torch.randn(4, 128, 7, 7)\nhead = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(128, 10))\nprint(head(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(4, 128, 7, 7)\nhead = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(128, 10))\nprint(head(x).shape)", ["cnn", "classifier"], "code_completion"),
    ("Dilated convolution", "dilated-convolution", "intermediate", "Conv2d with dilation=2, padding=2 on 16x16 input.", "import torch\nfrom torch import nn\nx = torch.randn(1, 4, 16, 16)\nconv = nn.Conv2d(4, 4, 3, padding=2, dilation=2)\nprint(conv(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 4, 16, 16)\nconv = nn.Conv2d(4, 4, 3, padding=2, dilation=2)\nprint(conv(x).shape)", ["cnn", "dilated"], "code_completion"),
    ("U-Net skip concat", "unet-skip-concat", "advanced", "Concatenate encoder and decoder feature maps along channel dim.", "import torch\nenc = torch.randn(2, 64, 16, 16)\ndec = torch.randn(2, 64, 16, 16)\nout = torch.cat([enc, dec], dim=1)\nprint(out.shape)", "import torch\nenc = torch.randn(2, 64, 16, 16)\ndec = torch.randn(2, 64, 16, 16)\nout = torch.cat([enc, dec], dim=1)\nprint(out.shape)", ["cnn", "unet"], "code_completion"),
    ("Transposed conv upsample", "transposed-conv-upsample", "advanced", "ConvTranspose2d doubles spatial size.", "import torch\nfrom torch import nn\nx = torch.randn(1, 16, 8, 8)\nup = nn.ConvTranspose2d(16, 8, kernel_size=4, stride=2, padding=1)\nprint(up(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 16, 8, 8)\nup = nn.ConvTranspose2d(16, 8, kernel_size=4, stride=2, padding=1)\nprint(up(x).shape)", ["cnn", "upsample"], "code_completion"),
    ("ViT patch embed shape", "vit-patch-embed-shape", "advanced", "Reshape image `(1,3,224,224)` into patches `(1, 196, 768)` conceptually via conv patch.", "import torch\nfrom torch import nn\nx = torch.randn(1, 3, 224, 224)\npatch = nn.Conv2d(3, 768, kernel_size=16, stride=16)\nfeat = patch(x)\npatches = feat.flatten(2).transpose(1, 2)\nprint(patches.shape)", "import torch\nfrom torch import nn\nx = torch.randn(1, 3, 224, 224)\npatch = nn.Conv2d(3, 768, kernel_size=16, stride=16)\nfeat = patch(x)\npatches = feat.flatten(2).transpose(1, 2)\nprint(patches.shape)", ["cnn", "vit"], "code_completion"),
    ("GPU CNN forward", "gpu-cnn-forward", "advanced", "Move model and input to CPU (Colab uses CUDA); print device of output.", "import torch\nfrom torch import nn\nm = nn.Conv2d(3, 4, 3, padding=1)\nx = torch.randn(1, 3, 16, 16)\ny = m(x)\nprint(y.device)", "import torch\nfrom torch import nn\nm = nn.Conv2d(3, 4, 3, padding=1)\nx = torch.randn(1, 3, 16, 16)\ny = m(x)\nprint(y.device)", ["cnn", "device"], "code_completion"),
    ("Notebook CNN lab", "notebook-cnn-lab", "intermediate", "Train a small CNN on MNIST in Colab.", "import torch\nprint('Open in Colab')", "import torch\nprint('Open in Colab')", ["cnn", "colab"], "notebook_challenge"),
    ("Build mini CNN", "build-mini-cnn", "advanced", "Build 3-layer CNN class for 10-class output.", "import torch\nfrom torch import nn\nclass MiniCNN(nn.Module):\n    def __init__(self):\n        super().__init__()\n        pass\n    def forward(self, x):\n        pass\nprint(MiniCNN()(torch.randn(2,1,28,28)).shape)", "import torch\nfrom torch import nn\nclass MiniCNN(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.net = nn.Sequential(\n            nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),\n            nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),\n            nn.Flatten(), nn.Linear(32*7*7, 10),\n        )\n    def forward(self, x):\n        return self.net(x)\nprint(MiniCNN()(torch.randn(2,1,28,28)).shape)", ["cnn", "build"], "build_from_scratch"),
    ("Predict conv output shape", "predict-conv-output-shape", "basic", "Input `(4, 3, 32, 32)` through Conv2d(3→16, k=3, p=1) — print output shape.", "import torch\nfrom torch import nn\nx = torch.randn(4, 3, 32, 32)\nprint(nn.Conv2d(3, 16, 3, padding=1)(x).shape)", "import torch\nfrom torch import nn\nx = torch.randn(4, 3, 32, 32)\nprint(nn.Conv2d(3, 16, 3, padding=1)(x).shape)", ["cnn", "shape"], "shape_assertion", "(4, 16, 32, 32)"),
]

QUESTIONS = []
for spec in _SPECS:
    kwargs: dict = {}
    if len(spec) == 9:
        title, slug, diff, task, starter, solution, tags, qtype, shape = spec
        kwargs["expected_output_shape"] = shape
    else:
        title, slug, diff, task, starter, solution, tags, qtype = spec
    QUESTIONS.append(
        build_exercise(
            title=title,
            slug=slug,
            difficulty=diff,
            task=task,
            starter_code=starter,
            solution_code=solution,
            tags=tags,
            question_type=qtype,
            **kwargs,
        )
    )


async def main() -> None:
    await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 07 — CNNs")


if __name__ == "__main__":
    asyncio.run(main())
