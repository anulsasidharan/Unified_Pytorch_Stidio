"""
Seed Module 06 — Datasets & DataLoaders (20 exercises).
Usage: python -m seeds.questions_datasets
"""

import asyncio

from seeds.loader import build_exercise, seed_questions_for_topic

TOPIC_SLUG = "datasets-dataloaders"

_SPECS: list[tuple] = [
    ("Custom Dataset length", "custom-dataset-len", "basic", "Implement `__len__` returning 10 for `SimpleDS`.", "import torch\nfrom torch.utils.data import Dataset\nclass SimpleDS(Dataset):\n    def __len__(self):\n        pass\n    def __getitem__(self, idx):\n        return torch.tensor([idx], dtype=torch.float32)\nprint(len(SimpleDS()))", "import torch\nfrom torch.utils.data import Dataset\nclass SimpleDS(Dataset):\n    def __len__(self):\n        return 10\n    def __getitem__(self, idx):\n        return torch.tensor([idx], dtype=torch.float32)\nprint(len(SimpleDS()))", ["dataloader", "dataset"], "code_completion"),
    ("Custom Dataset getitem", "custom-dataset-getitem", "basic", "Return tuple `(x, y)` from `__getitem__`.", "import torch\nfrom torch.utils.data import Dataset\nclass PairDS(Dataset):\n    def __len__(self):\n        return 5\n    def __getitem__(self, idx):\n        pass\nds = PairDS()\nprint(ds[0][0].shape, ds[0][1].shape)", "import torch\nfrom torch.utils.data import Dataset\nclass PairDS(Dataset):\n    def __len__(self):\n        return 5\n    def __getitem__(self, idx):\n        return torch.randn(3), torch.tensor(idx)\nds = PairDS()\nprint(ds[0][0].shape, ds[0][1].shape)", ["dataloader", "dataset"], "code_completion"),
    ("DataLoader batch", "dataloader-batch", "basic", "Create DataLoader with batch_size=4 from range dataset.", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nx = torch.arange(20).float().unsqueeze(1)\nds = TensorDataset(x)\nloader = # YOUR CODE\nbatch = next(iter(loader))\nprint(batch[0].shape)", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nx = torch.arange(20).float().unsqueeze(1)\nds = TensorDataset(x)\nloader = DataLoader(ds, batch_size=4)\nbatch = next(iter(loader))\nprint(batch[0].shape)", ["dataloader", "batch"], "code_completion"),
    ("Shuffle DataLoader", "dataloader-shuffle", "basic", "Enable shuffle=True and iterate one batch.", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.arange(8).float())\nloader = DataLoader(ds, batch_size=2, shuffle=True)\nprint(next(iter(loader))[0])", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.arange(8).float())\nloader = DataLoader(ds, batch_size=2, shuffle=True)\nprint(next(iter(loader))[0])", ["dataloader", "shuffle"], "code_completion"),
    ("num_workers zero", "dataloader-num-workers", "basic", "Create loader with num_workers=0 (safe default).", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.randn(16, 4))\nloader = DataLoader(ds, batch_size=8, num_workers=0)\nprint(len(loader))", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.randn(16, 4))\nloader = DataLoader(ds, batch_size=8, num_workers=0)\nprint(len(loader))", ["dataloader", "workers"], "code_completion"),
    ("TensorDataset pair", "tensor-dataset-pair", "basic", "Build TensorDataset from `X` and `y` tensors.", "import torch\nfrom torch.utils.data import TensorDataset\nX = torch.randn(12, 5)\ny = torch.randint(0, 2, (12,))\nds = # YOUR CODE\nprint(len(ds), ds[0][0].shape, ds[0][1].shape)", "import torch\nfrom torch.utils.data import TensorDataset\nX = torch.randn(12, 5)\ny = torch.randint(0, 2, (12,))\nds = TensorDataset(X, y)\nprint(len(ds), ds[0][0].shape, ds[0][1].shape)", ["dataloader", "tensor"], "code_completion"),
    ("RandomSplit", "random-split", "basic", "Split dataset 80/20 with `random_split`.", "import torch\nfrom torch.utils.data import TensorDataset, random_split\nds = TensorDataset(torch.randn(100, 3))\ntrain, val = random_split(ds, [80, 20])\nprint(len(train), len(val))", "import torch\nfrom torch.utils.data import TensorDataset, random_split\nds = TensorDataset(torch.randn(100, 3))\ntrain, val = random_split(ds, [80, 20])\nprint(len(train), len(val))", ["dataloader", "split"], "code_completion"),
    ("Subset indices", "subset-dataset", "basic", "Use `Subset` with indices `[0,2,4]`.", "import torch\nfrom torch.utils.data import TensorDataset, Subset\nds = TensorDataset(torch.arange(10).float())\nsub = Subset(ds, [0, 2, 4])\nprint(len(sub), sub[1][0].item())", "import torch\nfrom torch.utils.data import TensorDataset, Subset\nds = TensorDataset(torch.arange(10).float())\nsub = Subset(ds, [0, 2, 4])\nprint(len(sub), sub[1][0].item())", ["dataloader", "subset"], "code_completion"),
    ("collate_fn pad", "collate-fn-pad", "intermediate", "Pad variable-length sequences in collate_fn.", "import torch\nfrom torch.utils.data import DataLoader\n\ndef collate(batch):\n    # YOUR CODE: pad to max len\n    pass\n\ndata = [torch.randn(3), torch.randn(5), torch.randn(2)]\nloader = DataLoader(data, batch_size=3, collate_fn=collate)\nprint(next(iter(loader)).shape)", "import torch\nfrom torch.utils.data import DataLoader\n\ndef collate(batch):\n    max_len = max(x.size(0) for x in batch)\n    out = torch.zeros(len(batch), max_len)\n    for i, x in enumerate(batch):\n        out[i, : x.size(0)] = x\n    return out\n\ndata = [torch.randn(3), torch.randn(5), torch.randn(2)]\nloader = DataLoader(data, batch_size=3, collate_fn=collate)\nprint(next(iter(loader)).shape)", ["dataloader", "collate"], "code_completion"),
    ("WeightedRandomSampler", "weighted-random-sampler", "intermediate", "Oversample class 1 using WeightedRandomSampler.", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler\nlabels = torch.tensor([0,0,0,1])\nweights = torch.tensor([1., 1., 1., 3.])\nsampler = WeightedRandomSampler(weights, num_samples=8, replacement=True)\nds = TensorDataset(labels.float())\nloader = DataLoader(ds, batch_size=2, sampler=sampler)\nprint(len(loader))", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset, WeightedRandomSampler\nlabels = torch.tensor([0,0,0,1])\nweights = torch.tensor([1., 1., 1., 3.])\nsampler = WeightedRandomSampler(weights, num_samples=8, replacement=True)\nds = TensorDataset(labels.float())\nloader = DataLoader(ds, batch_size=2, sampler=sampler)\nprint(len(loader))", ["dataloader", "sampler"], "code_completion"),
    ("Compose transforms", "compose-transforms", "intermediate", "Chain `ToTensor` style lambda transforms manually.", "import torch\n\ndef to_float(x):\n    return x.float()\n\ndef add_noise(x):\n    return x + 0.01 * torch.randn_like(x)\n\nx = torch.tensor([1, 2, 3])\nfor fn in [to_float, add_noise]:\n    x = fn(x)\nprint(x.dtype)", "import torch\n\ndef to_float(x):\n    return x.float()\n\ndef add_noise(x):\n    return x + 0.01 * torch.randn_like(x)\n\nx = torch.tensor([1, 2, 3])\nfor fn in [to_float, add_noise]:\n    x = fn(x)\nprint(x.dtype)", ["dataloader", "transforms"], "code_completion"),
    ("pin_memory flag", "pin-memory-flag", "intermediate", "Create DataLoader with pin_memory=False on CPU.", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.randn(8, 2))\nloader = DataLoader(ds, batch_size=4, pin_memory=False)\nprint(loader.pin_memory)", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.randn(8, 2))\nloader = DataLoader(ds, batch_size=4, pin_memory=False)\nprint(loader.pin_memory)", ["dataloader", "performance"], "code_completion"),
    ("drop_last batch", "drop-last-batch", "intermediate", "Use drop_last=True when len not divisible by batch_size.", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.randn(10, 2))\nloader = DataLoader(ds, batch_size=4, drop_last=True)\nprint(len(loader))", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nds = TensorDataset(torch.randn(10, 2))\nloader = DataLoader(ds, batch_size=4, drop_last=True)\nprint(len(loader))", ["dataloader", "batch"], "code_completion"),
    ("ConcatDataset", "concat-dataset", "intermediate", "Concatenate two TensorDatasets.", "import torch\nfrom torch.utils.data import ConcatDataset, TensorDataset\nds1 = TensorDataset(torch.zeros(5))\nds2 = TensorDataset(torch.ones(3))\nmerged = ConcatDataset([ds1, ds2])\nprint(len(merged))", "import torch\nfrom torch.utils.data import ConcatDataset, TensorDataset\nds1 = TensorDataset(torch.zeros(5))\nds2 = TensorDataset(torch.ones(3))\nmerged = ConcatDataset([ds1, ds2])\nprint(len(merged))", ["dataloader", "concat"], "code_completion"),
    ("IterableDataset stub", "iterable-dataset-stub", "advanced", "Implement IterableDataset yielding 3 items.", "import torch\nfrom torch.utils.data import IterableDataset\nclass StreamDS(IterableDataset):\n    def __iter__(self):\n        for i in range(3):\n            yield torch.tensor([i])\nprint(len(list(StreamDS())))", "import torch\nfrom torch.utils.data import IterableDataset\nclass StreamDS(IterableDataset):\n    def __iter__(self):\n        for i in range(3):\n            yield torch.tensor([i])\nprint(len(list(StreamDS())))", ["dataloader", "iterable"], "code_completion"),
    ("DistributedSampler concept", "distributed-sampler-concept", "advanced", "Print num_samples formula for 100 samples, 4 replicas, rank 0.", "import math\nnum_samples = 100\nreplicas = 4\nrank = 0\nper_replica = math.ceil(num_samples / replicas)\nprint(per_replica)", "import math\nnum_samples = 100\nreplicas = 4\nrank = 0\nper_replica = math.ceil(num_samples / replicas)\nprint(per_replica)", ["dataloader", "distributed"], "conceptual_mcq"),
    ("Map-style vs iterable", "map-vs-iterable", "advanced", "Print whether TensorDataset supports __getitem__.", "import torch\nfrom torch.utils.data import TensorDataset\nds = TensorDataset(torch.randn(4))\nprint(hasattr(ds, '__getitem__'))", "import torch\nfrom torch.utils.data import TensorDataset\nds = TensorDataset(torch.randn(4))\nprint(hasattr(ds, '__getitem__'))", ["dataloader", "concept"], "conceptual_mcq"),
    ("Build Dataset class", "build-dataset-class", "advanced", "Full Dataset returning image tensor `(3,32,32)` and label.", "import torch\nfrom torch.utils.data import Dataset\nclass ImgDS(Dataset):\n    def __init__(self, n):\n        self.n = n\n    def __len__(self):\n        return self.n\n    def __getitem__(self, idx):\n        pass\nds = ImgDS(6)\nprint(ds[0][0].shape, ds[0][1])", "import torch\nfrom torch.utils.data import Dataset\nclass ImgDS(Dataset):\n    def __init__(self, n):\n        self.n = n\n    def __len__(self):\n        return self.n\n    def __getitem__(self, idx):\n        return torch.randn(3, 32, 32), idx % 2\nds = ImgDS(6)\nprint(ds[0][0].shape, ds[0][1])", ["dataloader", "build"], "build_from_scratch"),
    ("Notebook DataLoader lab", "notebook-dataloader-lab", "intermediate", "Colab lab: benchmark num_workers for image loading.", "import torch\nprint('Open in Colab')", "import torch\nprint('Open in Colab')", ["dataloader", "colab"], "notebook_challenge"),
    ("Predict batch shape", "predict-batch-shape", "basic", "DataLoader batch of `(N=8, C=3, H=32, W=32)` images — print batch dim 0.", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nimgs = torch.randn(8, 3, 32, 32)\nloader = DataLoader(TensorDataset(imgs), batch_size=8)\nprint(next(iter(loader))[0].shape[0])", "import torch\nfrom torch.utils.data import DataLoader, TensorDataset\nimgs = torch.randn(8, 3, 32, 32)\nloader = DataLoader(TensorDataset(imgs), batch_size=8)\nprint(next(iter(loader))[0].shape[0])", ["dataloader", "shape"], "shape_assertion", "(8, 3, 32, 32)"),
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
    await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 06 — Datasets & DataLoaders")


if __name__ == "__main__":
    asyncio.run(main())
