"""
seeds/topics.py
---------------
Seed script for all 13 PyTorch Learning Studio modules.

Usage:
    python -m seeds.topics

Requires DATABASE_URL in environment (or .env file loaded).
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/pytorch_studio")

TOPICS = [
    {
        "module_number": 1,
        "name": "Tensors & Operations",
        "slug": "tensors",
        "description": (
            "Master the foundational building block of all PyTorch programs. "
            "Learn to create, manipulate, index, and transform tensors — the "
            "multi-dimensional arrays that power every neural network computation."
        ),
        "icon": "🧮",
        "color": "#6366f1",   # indigo
        "order_index": 1,
    },
    {
        "module_number": 2,
        "name": "Autograd & Backpropagation",
        "slug": "autograd",
        "description": (
            "Understand PyTorch's automatic differentiation engine. Learn how "
            "computation graphs are built, how gradients flow backwards, and how "
            "to write custom differentiable functions."
        ),
        "icon": "🔄",
        "color": "#8b5cf6",   # violet
        "order_index": 2,
    },
    {
        "module_number": 3,
        "name": "Neural Network Basics",
        "slug": "nn-module",
        "description": (
            "Build neural networks using nn.Module. Learn to define layers, "
            "compose architectures with containers, initialize weights, and "
            "understand the parameter lifecycle."
        ),
        "icon": "🧠",
        "color": "#ec4899",   # pink
        "order_index": 3,
    },
    {
        "module_number": 4,
        "name": "Training Loops & Optimization",
        "slug": "training-loops",
        "description": (
            "Master the canonical PyTorch training loop. Learn optimizers, "
            "learning rate scheduling, gradient clipping, mixed-precision "
            "training, and advanced optimization strategies."
        ),
        "icon": "⚙️",
        "color": "#f59e0b",   # amber
        "order_index": 4,
    },
    {
        "module_number": 5,
        "name": "Loss Functions & Metrics",
        "slug": "loss-functions",
        "description": (
            "Explore built-in loss functions and learn to design custom ones. "
            "Understand when to use each loss, implement differentiable metrics, "
            "and handle class imbalance."
        ),
        "icon": "📉",
        "color": "#ef4444",   # red
        "order_index": 5,
    },
    {
        "module_number": 6,
        "name": "Datasets & DataLoaders",
        "slug": "datasets-dataloaders",
        "description": (
            "Build efficient data pipelines. Learn the Dataset and DataLoader "
            "APIs, write custom datasets, apply transforms, and tune "
            "multi-worker loading for maximum GPU utilization."
        ),
        "icon": "🗄️",
        "color": "#10b981",   # emerald
        "order_index": 6,
    },
    {
        "module_number": 7,
        "name": "CNNs & Computer Vision",
        "slug": "cnns-computer-vision",
        "description": (
            "Build convolutional networks for image tasks. From LeNet to "
            "ResNets with skip connections, feature visualization, and "
            "advanced architectures like U-Net and FPN."
        ),
        "icon": "👁️",
        "color": "#3b82f6",   # blue
        "order_index": 7,
    },
    {
        "module_number": 8,
        "name": "RNNs, LSTMs & Sequences",
        "slug": "rnns-lstms",
        "description": (
            "Process sequential data with recurrent networks. Covers RNN, "
            "LSTM, GRU, bidirectional models, sequence packing, and "
            "Seq2Seq architectures with attention."
        ),
        "icon": "🔁",
        "color": "#06b6d4",   # cyan
        "order_index": 8,
    },
    {
        "module_number": 9,
        "name": "Transformers & Attention",
        "slug": "transformers-attention",
        "description": (
            "Implement attention mechanisms and transformer blocks from scratch. "
            "Covers scaled dot-product attention, multi-head attention, "
            "positional encoding, causal masking, and modern efficient variants."
        ),
        "icon": "⚡",
        "color": "#f97316",   # orange
        "order_index": 9,
    },
    {
        "module_number": 10,
        "name": "Transfer Learning & Fine-tuning",
        "slug": "transfer-learning",
        "description": (
            "Leverage pretrained models for new tasks. Learn to freeze layers, "
            "replace heads, apply layer-wise learning rates, and use "
            "parameter-efficient fine-tuning methods like LoRA."
        ),
        "icon": "🔀",
        "color": "#84cc16",   # lime
        "order_index": 10,
    },
    {
        "module_number": 11,
        "name": "Model Saving & Deployment",
        "slug": "model-deployment",
        "description": (
            "Take models from research to production. Learn state_dict "
            "checkpointing, TorchScript (trace vs script), ONNX export, "
            "torch.compile, and mobile deployment."
        ),
        "icon": "🚀",
        "color": "#64748b",   # slate
        "order_index": 11,
    },
    {
        "module_number": 12,
        "name": "GPU / CUDA & Performance",
        "slug": "gpu-cuda",
        "description": (
            "Maximize hardware utilization. Covers device management, "
            "memory pinning, profiling with torch.profiler, DataParallel, "
            "DistributedDataParallel, and FSDP for multi-GPU training."
        ),
        "icon": "🖥️",
        "color": "#14b8a6",   # teal
        "order_index": 12,
    },
    {
        "module_number": 13,
        "name": "PyTorch Lightning & Best Practices",
        "slug": "pytorch-lightning",
        "description": (
            "Eliminate boilerplate with PyTorch Lightning. Covers "
            "LightningModule, LightningDataModule, Trainer, callbacks, "
            "logging integrations, and the Fabric API for maximum flexibility."
        ),
        "icon": "⚡🔥",
        "color": "#a855f7",   # purple
        "order_index": 13,
    },
]


async def seed_topics():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if topics already seeded
        result = await session.execute(text("SELECT COUNT(*) FROM topics"))
        count = result.scalar()

        if count > 0:
            print(f"[skip] Topics table already has {count} rows. Skipping seed.")
            print("    To re-seed, run: DELETE FROM topics; then re-run this script.")
            return

        for topic in TOPICS:
            await session.execute(
                text("""
                    INSERT INTO topics (
                        module_number, name, slug, description,
                        icon, color, order_index, total_questions, is_active
                    ) VALUES (
                        :module_number, :name, :slug, :description,
                        :icon, :color, :order_index, 0, TRUE
                    )
                """),
                topic
            )

        await session.commit()
        print(f"[ok] Seeded {len(TOPICS)} PyTorch modules successfully.")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_topics())
