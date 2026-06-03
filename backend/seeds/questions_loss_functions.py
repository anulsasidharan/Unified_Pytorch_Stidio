"""
Seed Module 05 — Loss Functions & Metrics (20 exercises).
Usage: python -m seeds.questions_loss_functions
"""

import asyncio

from seeds.loader import build_exercise, seed_questions_for_topic

TOPIC_SLUG = "loss-functions"

_SPECS: list[tuple] = [
    ("MSE loss", "mse-loss", "basic", "Compute MSE between predictions and targets shape `(4,)`.", "import torch\nfrom torch import nn\npred = torch.randn(4)\ntarget = torch.randn(4)\nloss = # YOUR CODE\nprint(loss.shape)", "import torch\nfrom torch import nn\npred = torch.randn(4)\ntarget = torch.randn(4)\nloss = nn.MSELoss()(pred, target)\nprint(loss.shape)", ["loss", "mse"], "code_completion"),
    ("CrossEntropy loss", "crossentropy-loss-fn", "basic", "Use `CrossEntropyLoss` on logits `(3,5)` and class indices length 3.", "import torch\nfrom torch import nn\nlogits = torch.randn(3, 5)\ntargets = torch.tensor([1, 0, 4])\nloss = # YOUR CODE\nprint(loss.item() >= 0)", "import torch\nfrom torch import nn\nlogits = torch.randn(3, 5)\ntargets = torch.tensor([1, 0, 4])\nloss = nn.CrossEntropyLoss()(logits, targets)\nprint(loss.item() >= 0)", ["loss", "classification"], "code_completion"),
    ("BCEWithLogitsLoss", "bce-with-logits", "basic", "Binary classification loss on logits `(4,)` and float targets.", "import torch\nfrom torch import nn\nlogits = torch.randn(4)\ntargets = torch.tensor([1., 0., 1., 0.])\nloss = nn.BCEWithLogitsLoss()(logits, targets)\nprint(round(loss.item(), 3))", "import torch\nfrom torch import nn\nlogits = torch.randn(4)\ntargets = torch.tensor([1., 0., 1., 0.])\nloss = nn.BCEWithLogitsLoss()(logits, targets)\nprint(round(loss.item(), 3))", ["loss", "binary"], "code_completion"),
    ("NLLLoss with log_softmax", "nll-loss", "basic", "Apply `log_softmax` on dim=-1 then `NLLLoss`.", "import torch\nfrom torch import nn\nimport torch.nn.functional as F\nlogits = torch.randn(2, 4)\ntargets = torch.tensor([2, 1])\nlog_probs = # YOUR CODE\nloss = nn.NLLLoss()(log_probs, targets)\nprint(loss.item())", "import torch\nfrom torch import nn\nimport torch.nn.functional as F\nlogits = torch.randn(2, 4)\ntargets = torch.tensor([2, 1])\nlog_probs = F.log_softmax(logits, dim=-1)\nloss = nn.NLLLoss()(log_probs, targets)\nprint(loss.item())", ["loss", "nll"], "code_completion"),
    ("L1 loss", "l1-loss", "basic", "Compute mean absolute error with `L1Loss`.", "import torch\nfrom torch import nn\npred = torch.tensor([1., 3., 5.])\ntarget = torch.tensor([2., 2., 6.])\nprint(nn.L1Loss()(pred, target).item())", "import torch\nfrom torch import nn\npred = torch.tensor([1., 3., 5.])\ntarget = torch.tensor([2., 2., 6.])\nprint(nn.L1Loss()(pred, target).item())", ["loss", "l1"], "code_completion"),
    ("Smooth L1 Huber", "smooth-l1-loss", "basic", "Use `SmoothL1Loss` on two tensors.", "import torch\nfrom torch import nn\npred = torch.randn(5)\ntarget = torch.randn(5)\nprint(nn.SmoothL1Loss()(pred, target).item())", "import torch\nfrom torch import nn\npred = torch.randn(5)\ntarget = torch.randn(5)\nprint(nn.SmoothL1Loss()(pred, target).item())", ["loss", "huber"], "code_completion"),
    ("KL divergence", "kl-div-loss", "basic", "Compute `KLDivLoss` between log-probs and target distribution.", "import torch\nfrom torch import nn\nimport torch.nn.functional as F\nlog_probs = F.log_softmax(torch.randn(3, 4), dim=-1)\ntarget = torch.softmax(torch.randn(3, 4), dim=-1)\nprint(nn.KLDivLoss(reduction='batchmean')(log_probs, target).item())", "import torch\nfrom torch import nn\nimport torch.nn.functional as F\nlog_probs = F.log_softmax(torch.randn(3, 4), dim=-1)\ntarget = torch.softmax(torch.randn(3, 4), dim=-1)\nprint(nn.KLDivLoss(reduction='batchmean')(log_probs, target).item())", ["loss", "kl"], "code_completion"),
    ("Reduction sum vs mean", "loss-reduction", "basic", "Compare MSE `reduction='sum'` vs `'mean'` on same tensors.", "import torch\nfrom torch import nn\npred = torch.ones(4)\ntarget = torch.zeros(4)\ns = nn.MSELoss(reduction='sum')(pred, target)\nm = nn.MSELoss(reduction='mean')(pred, target)\nprint(s.item(), m.item())", "import torch\nfrom torch import nn\npred = torch.ones(4)\ntarget = torch.zeros(4)\ns = nn.MSELoss(reduction='sum')(pred, target)\nm = nn.MSELoss(reduction='mean')(pred, target)\nprint(s.item(), m.item())", ["loss", "reduction"], "code_completion"),
    ("Custom MSE loss", "custom-mse-loss", "intermediate", "Implement MSE without `nn.MSELoss`.", "import torch\ndef custom_mse(pred, target):\n    # YOUR CODE\n    pass\nprint(custom_mse(torch.randn(3), torch.randn(3)).item())", "import torch\ndef custom_mse(pred, target):\n    return ((pred - target) ** 2).mean()\nprint(custom_mse(torch.randn(3), torch.randn(3)).item())", ["loss", "custom"], "code_completion"),
    ("Focal loss sketch", "focal-loss-sketch", "intermediate", "Implement simplified focal modulating factor `(1-pt)**2 * ce`.", "import torch\nimport torch.nn.functional as F\nlogits = torch.randn(2, 3)\ntargets = torch.tensor([0, 2])\nce = F.cross_entropy(logits, targets, reduction='none')\npt = torch.exp(-ce)\nfocal = ((1 - pt) ** 2 * ce).mean()\nprint(focal.item())", "import torch\nimport torch.nn.functional as F\nlogits = torch.randn(2, 3)\ntargets = torch.tensor([0, 2])\nce = F.cross_entropy(logits, targets, reduction='none')\npt = torch.exp(-ce)\nfocal = ((1 - pt) ** 2 * ce).mean()\nprint(focal.item())", ["loss", "focal"], "code_completion"),
    ("Label smoothing CE", "label-smoothing-ce", "intermediate", "Use `CrossEntropyLoss(label_smoothing=0.1)`.", "import torch\nfrom torch import nn\nloss_fn = nn.CrossEntropyLoss(label_smoothing=0.1)\nlogits = torch.randn(4, 10)\ntargets = torch.randint(0, 10, (4,))\nprint(loss_fn(logits, targets).item())", "import torch\nfrom torch import nn\nloss_fn = nn.CrossEntropyLoss(label_smoothing=0.1)\nlogits = torch.randn(4, 10)\ntargets = torch.randint(0, 10, (4,))\nprint(loss_fn(logits, targets).item())", ["loss", "smoothing"], "code_completion"),
    ("Multi-task loss sum", "multi-task-loss", "intermediate", "Combine MSE and CE losses with weights 0.5 each.", "import torch\nfrom torch import nn\nmse = nn.MSELoss()(torch.randn(3), torch.randn(3))\nce = nn.CrossEntropyLoss()(torch.randn(3,4), torch.tensor([0,1,2]))\ntotal = 0.5 * mse + 0.5 * ce\nprint(total.item())", "import torch\nfrom torch import nn\nmse = nn.MSELoss()(torch.randn(3), torch.randn(3))\nce = nn.CrossEntropyLoss()(torch.randn(3,4), torch.tensor([0,1,2]))\ntotal = 0.5 * mse + 0.5 * ce\nprint(total.item())", ["loss", "multitask"], "code_completion"),
    ("Class weights CE", "weighted-cross-entropy", "intermediate", "Pass `weight` tensor to CrossEntropyLoss.", "import torch\nfrom torch import nn\nweights = torch.tensor([1.0, 2.0, 0.5])\nloss_fn = nn.CrossEntropyLoss(weight=weights)\nprint(loss_fn(torch.randn(2,3), torch.tensor([0,1])).item())", "import torch\nfrom torch import nn\nweights = torch.tensor([1.0, 2.0, 0.5])\nloss_fn = nn.CrossEntropyLoss(weight=weights)\nprint(loss_fn(torch.randn(2,3), torch.tensor([0,1])).item())", ["loss", "imbalance"], "code_completion"),
    ("Triplet margin loss", "triplet-margin-loss", "intermediate", "Use `TripletMarginLoss` on anchor/positive/negative embeddings.", "import torch\nfrom torch import nn\nloss_fn = nn.TripletMarginLoss()\na, p, n = torch.randn(3, 8), torch.randn(3, 8), torch.randn(3, 8)\nprint(loss_fn(a, p, n).item())", "import torch\nfrom torch import nn\nloss_fn = nn.TripletMarginLoss()\na, p, n = torch.randn(3, 8), torch.randn(3, 8), torch.randn(3, 8)\nprint(loss_fn(a, p, n).item())", ["loss", "metric-learning"], "code_completion"),
    ("Contrastive loss pair", "contrastive-loss-pair", "advanced", "Implement cosine embedding loss style distance penalty.", "import torch\nimport torch.nn.functional as F\nx1, x2 = F.normalize(torch.randn(4), dim=0), F.normalize(torch.randn(4), dim=0)\ndist = (x1 - x2).pow(2).sum()\nprint(dist.item())", "import torch\nimport torch.nn.functional as F\nx1, x2 = F.normalize(torch.randn(4), dim=0), F.normalize(torch.randn(4), dim=0)\ndist = (x1 - x2).pow(2).sum()\nprint(dist.item())", ["loss", "contrastive"], "code_completion"),
    ("Dice loss sketch", "dice-loss-sketch", "advanced", "Compute soft Dice coefficient for binary masks.", "import torch\npred = torch.sigmoid(torch.randn(1, 8, 8))\ntarget = (torch.rand(1, 8, 8) > 0.5).float()\ninter = (pred * target).sum()\ndice = (2 * inter + 1) / (pred.sum() + target.sum() + 1)\nprint(dice.item())", "import torch\npred = torch.sigmoid(torch.randn(1, 8, 8))\ntarget = (torch.rand(1, 8, 8) > 0.5).float()\ninter = (pred * target).sum()\ndice = (2 * inter + 1) / (pred.sum() + target.sum() + 1)\nprint(dice.item())", ["loss", "segmentation"], "code_completion"),
    ("Perceptual loss concept", "perceptual-loss-concept", "advanced", "Use MSE between feature maps as perceptual proxy.", "import torch\nfrom torch import nn\nfeat_pred = torch.randn(2, 16)\nfeat_tgt = torch.randn(2, 16)\nprint(nn.MSELoss()(feat_pred, feat_tgt).item())", "import torch\nfrom torch import nn\nfeat_pred = torch.randn(2, 16)\nfeat_tgt = torch.randn(2, 16)\nprint(nn.MSELoss()(feat_pred, feat_tgt).item())", ["loss", "perceptual"], "code_completion"),
    ("Margin ranking loss", "margin-ranking-loss", "advanced", "Apply `MarginRankingLoss` on two scores and label.", "import torch\nfrom torch import nn\nloss_fn = nn.MarginRankingLoss()\nx1, x2 = torch.randn(5), torch.randn(5)\ny = torch.ones(5)\nprint(loss_fn(x1, x2, y).item())", "import torch\nfrom torch import nn\nloss_fn = nn.MarginRankingLoss()\nx1, x2 = torch.randn(5), torch.randn(5)\ny = torch.ones(5)\nprint(loss_fn(x1, x2, y).item())", ["loss", "ranking"], "code_completion"),
    ("Notebook loss lab", "notebook-loss-lab", "intermediate", "Open Colab notebook to compare classification losses on imbalanced data.", "import torch\nprint('Open in Colab')", "import torch\nprint('Open in Colab')", ["loss", "colab"], "notebook_challenge"),
    ("Predict CE output shape", "predict-ce-loss-shape", "basic", "CrossEntropyLoss returns scalar; verify with `.dim()==0`.", "import torch\nfrom torch import nn\nloss = nn.CrossEntropyLoss()(torch.randn(2,3), torch.tensor([0,1]))\nprint(loss.dim())", "import torch\nfrom torch import nn\nloss = nn.CrossEntropyLoss()(torch.randn(2,3), torch.tensor([0,1]))\nprint(loss.dim())", ["loss", "shape"], "shape_assertion", "()"),
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
    await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 05 — Loss Functions")


if __name__ == "__main__":
    asyncio.run(main())
