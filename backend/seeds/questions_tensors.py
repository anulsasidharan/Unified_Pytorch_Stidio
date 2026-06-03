"""
seeds/questions_tensors.py
--------------------------
20 exercises for Module 01 — Tensors & Operations
  Basic:        8 exercises
  Intermediate: 7 exercises
  Advanced:     5 exercises

Usage:
    python -m seeds.questions_tensors

Requires topics to be seeded first (python -m seeds.topics).
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
import json
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/pytorch_studio"
)

# ---------------------------------------------------------------------------
# QUESTIONS — Module 01: Tensors & Operations
# ---------------------------------------------------------------------------

QUESTIONS = [

    # ═══════════════════════════════════════════════════════════════
    # BASIC (8 exercises)
    # ═══════════════════════════════════════════════════════════════

    {
        "title": "Create Your First Tensor",
        "slug": "create-first-tensor",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## Create Your First Tensor

In PyTorch, a **tensor** is the fundamental data structure — a multi-dimensional array
similar to NumPy's `ndarray` but with GPU support and autograd integration.

### Task
Complete the code to create the following tensors:
1. A **1D tensor** `a` containing the values `[1, 2, 3, 4, 5]`
2. A **2×3 tensor** `b` filled entirely with **zeros**
3. A **3×3 tensor** `c` filled entirely with **ones**
4. A **4×4 tensor** `d` filled with **random values** from a uniform distribution [0, 1)

Then print the **shape** and **dtype** of each tensor.

### Expected Output
```
a shape: torch.Size([5])       dtype: torch.int64
b shape: torch.Size([2, 3])    dtype: torch.float32
c shape: torch.Size([3, 3])    dtype: torch.float32
d shape: torch.Size([4, 4])    dtype: torch.float32
```
""",
        "constraints": "Use only `torch.tensor`, `torch.zeros`, `torch.ones`, `torch.rand`.",
        "starter_code": """import torch

# 1. Create a 1D tensor from a Python list
a = # YOUR CODE HERE

# 2. Create a 2x3 tensor of zeros
b = # YOUR CODE HERE

# 3. Create a 3x3 tensor of ones
c = # YOUR CODE HERE

# 4. Create a 4x4 tensor of random values [0, 1)
d = # YOUR CODE HERE

# Print shape and dtype for each
for name, t in [('a', a), ('b', b), ('c', c), ('d', d)]:
    print(f"{name} shape: {t.shape}   dtype: {t.dtype}")
""",
        "expected_output": "a shape: torch.Size([5])   dtype: torch.int64",
        "expected_output_shape": None,
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "creation", "basics"],
        "xp_reward": 10,
        "time_estimate_mins": 10,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

a = torch.tensor([1, 2, 3, 4, 5])
b = torch.zeros(2, 3)
c = torch.ones(3, 3)
d = torch.rand(4, 4)

for name, t in [('a', a), ('b', b), ('c', c), ('d', d)]:
    print(f"{name} shape: {t.shape}   dtype: {t.dtype}")
""",
                "explanation": (
                    "`torch.tensor()` infers dtype from the Python list — integers become `int64`. "
                    "`torch.zeros()`, `torch.ones()`, and `torch.rand()` default to `float32`. "
                    "You pass dimensions as separate arguments, not a tuple."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [
            {
                "input_data": {},
                "expected_output": {"a_shape": [5], "b_shape": [2, 3], "c_shape": [3, 3], "d_shape": [4, 4]},
                "is_hidden": False,
            }
        ],
    },

    {
        "title": "Tensor dtypes and Type Casting",
        "slug": "tensor-dtypes-casting",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## Tensor dtypes and Type Casting

Every PyTorch tensor has a **dtype** that determines how its values are stored in memory.
Choosing the right dtype affects both **memory usage** and **numerical precision**.

### Common dtypes
| dtype | Description |
|---|---|
| `torch.float32` | 32-bit float (default for most ops) |
| `torch.float64` | 64-bit float (double precision) |
| `torch.int32` | 32-bit integer |
| `torch.int64` | 64-bit integer (default for `torch.tensor([1,2,3])`) |
| `torch.bool` | Boolean |

### Task
1. Create a float32 tensor `x` with values `[1.5, 2.5, 3.5]`
2. Cast `x` to **int32** and store in `x_int`
3. Cast `x` to **float64** and store in `x_double`
4. Create a boolean tensor `mask` where values of `x` are greater than 2.0
5. Print each tensor and its dtype
""",
        "constraints": "Use `.to()` or `.int()` / `.double()` / `.bool()` for casting.",
        "starter_code": """import torch

# 1. Create a float32 tensor
x = # YOUR CODE HERE

# 2. Cast to int32
x_int = # YOUR CODE HERE

# 3. Cast to float64
x_double = # YOUR CODE HERE

# 4. Boolean mask where x > 2.0
mask = # YOUR CODE HERE

print(f"x:        {x}  dtype={x.dtype}")
print(f"x_int:    {x_int}  dtype={x_int.dtype}")
print(f"x_double: {x_double}  dtype={x_double.dtype}")
print(f"mask:     {mask}  dtype={mask.dtype}")
""",
        "expected_output": "x:        tensor([1.5000, 2.5000, 3.5000])  dtype=torch.float32",
        "expected_output_shape": None,
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "dtype", "casting"],
        "xp_reward": 10,
        "time_estimate_mins": 10,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

x = torch.tensor([1.5, 2.5, 3.5], dtype=torch.float32)
x_int = x.to(torch.int32)
x_double = x.to(torch.float64)
mask = x > 2.0

print(f"x:        {x}  dtype={x.dtype}")
print(f"x_int:    {x_int}  dtype={x_int.dtype}")
print(f"x_double: {x_double}  dtype={x_double.dtype}")
print(f"mask:     {mask}  dtype={mask.dtype}")
""",
                "explanation": (
                    "`.to(dtype)` is the universal casting method. Shorthand methods like "
                    "`.int()`, `.double()`, `.float()`, `.bool()` also work but `.to()` is "
                    "preferred in production code for clarity. Note that casting float→int "
                    "truncates (1.5 → 1), it does NOT round."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [
            {
                "input_data": {},
                "expected_output": {"x_dtype": "float32", "x_int_dtype": "int32", "mask_dtype": "bool"},
                "is_hidden": False,
            }
        ],
    },

    {
        "title": "Tensor Indexing and Slicing",
        "slug": "tensor-indexing-slicing",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## Tensor Indexing and Slicing

PyTorch uses NumPy-style indexing. Understanding indexing is essential for
extracting features, masking data, and manipulating batches.

### Task
Given the 3×4 matrix `m` below, complete the following extractions:

```
m = [[10, 20, 30, 40],
     [50, 60, 70, 80],
     [90, 100, 110, 120]]
```

1. `row1` — the entire second row (index 1) → shape `(4,)`
2. `col2` — the entire third column (index 2) → shape `(3,)`
3. `top_right` — the 2×2 submatrix in the top-right corner → shape `(2, 2)`
4. `last` — the very last element (scalar) → value `120`
5. `even_cols` — all rows, columns 0 and 2 only → shape `(3, 2)`
""",
        "constraints": "Use only standard Python-style indexing and slicing. No fancy indexing with lists yet.",
        "starter_code": """import torch

m = torch.tensor([
    [10,  20,  30,  40],
    [50,  60,  70,  80],
    [90, 100, 110, 120]
], dtype=torch.float32)

# 1. Second row
row1 = # YOUR CODE HERE

# 2. Third column
col2 = # YOUR CODE HERE

# 3. Top-right 2x2 submatrix
top_right = # YOUR CODE HERE

# 4. Last element
last = # YOUR CODE HERE

# 5. Columns 0 and 2 (even indices)
even_cols = # YOUR CODE HERE

print("row1:", row1)
print("col2:", col2)
print("top_right:", top_right)
print("last:", last)
print("even_cols:", even_cols)
""",
        "expected_output": "row1: tensor([50., 60., 70., 80.])",
        "expected_output_shape": None,
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "indexing", "slicing"],
        "xp_reward": 10,
        "time_estimate_mins": 12,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

m = torch.tensor([
    [10,  20,  30,  40],
    [50,  60,  70,  80],
    [90, 100, 110, 120]
], dtype=torch.float32)

row1      = m[1]           # or m[1, :]
col2      = m[:, 2]
top_right = m[:2, 2:]
last      = m[-1, -1]
even_cols = m[:, ::2]

print("row1:", row1)
print("col2:", col2)
print("top_right:", top_right)
print("last:", last)
print("even_cols:", even_cols)
""",
                "explanation": (
                    "PyTorch indexing follows `[row, col]` with full NumPy slice syntax `start:stop:step`. "
                    "`m[1]` and `m[1, :]` are equivalent — both return the full second row. "
                    "`m[:, ::2]` steps through columns with stride 2, selecting columns 0 and 2."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [
            {
                "input_data": {},
                "expected_output": {
                    "row1_shape": [4],
                    "col2_shape": [3],
                    "top_right_shape": [2, 2],
                    "even_cols_shape": [3, 2],
                },
                "is_hidden": False,
            }
        ],
    },

    {
        "title": "Reshape, View, and Squeeze",
        "slug": "reshape-view-squeeze",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## Reshape, View, and Squeeze

Reshaping tensors without copying data is one of the most frequent operations
in deep learning — batching, flattening before linear layers, adding dimensions
for broadcasting.

### Task
Starting from a 1D tensor of 24 elements, perform these transformations:

1. `t2d` — reshape to **(4, 6)**
2. `t3d` — reshape to **(2, 3, 4)**
3. `flat` — flatten `t3d` back to 1D → shape `(24,)`
4. `t_with_batch` — add a **batch dimension** at position 0 → shape `(1, 2, 3, 4)`
5. `t_squeezed` — remove the batch dimension from `t_with_batch` → shape `(2, 3, 4)`

Use `-1` as a wildcard dimension where it makes the code cleaner.
""",
        "constraints": "Use `view`, `reshape`, `flatten`, `unsqueeze`, and `squeeze`.",
        "starter_code": """import torch

t = torch.arange(24, dtype=torch.float32)   # [0, 1, 2, ..., 23]

# 1. Reshape to (4, 6)
t2d = # YOUR CODE HERE

# 2. Reshape to (2, 3, 4)
t3d = # YOUR CODE HERE

# 3. Flatten back to 1D
flat = # YOUR CODE HERE

# 4. Add batch dimension at position 0
t_with_batch = # YOUR CODE HERE

# 5. Remove the batch dimension
t_squeezed = # YOUR CODE HERE

print(f"t2d:          {t2d.shape}")
print(f"t3d:          {t3d.shape}")
print(f"flat:         {flat.shape}")
print(f"t_with_batch: {t_with_batch.shape}")
print(f"t_squeezed:   {t_squeezed.shape}")
""",
        "expected_output_shape": "(2, 3, 4)",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "reshape", "view", "squeeze", "unsqueeze"],
        "xp_reward": 10,
        "time_estimate_mins": 12,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

t = torch.arange(24, dtype=torch.float32)

t2d          = t.view(4, 6)
t3d          = t.view(2, 3, 4)
flat         = t3d.flatten()
t_with_batch = t3d.unsqueeze(0)
t_squeezed   = t_with_batch.squeeze(0)

print(f"t2d:          {t2d.shape}")
print(f"t3d:          {t3d.shape}")
print(f"flat:         {flat.shape}")
print(f"t_with_batch: {t_with_batch.shape}")
print(f"t_squeezed:   {t_squeezed.shape}")
""",
                "explanation": (
                    "`view()` is faster than `reshape()` but requires contiguous memory — "
                    "if the tensor isn't contiguous it will raise an error. `reshape()` falls "
                    "back to a copy if needed. `unsqueeze(0)` inserts a size-1 dimension at "
                    "position 0. `squeeze(0)` removes it only if that dimension has size 1."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Element-wise Arithmetic and Reduction Ops",
        "slug": "elementwise-arithmetic-reductions",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## Element-wise Arithmetic and Reduction Ops

Tensors support arithmetic operators that work **element-by-element**.
Reduction operations collapse one or more dimensions into a scalar or smaller tensor.

### Task
Given tensors `a` and `b`, compute:

1. `add_result` — element-wise sum `a + b`
2. `mul_result` — element-wise product `a * b`
3. `total` — sum of **all** elements in `a`
4. `row_means` — mean of each **row** in `a` → shape `(3,)`
5. `col_max` — maximum value in each **column** of `a` → shape `(4,)`
6. `norm` — L2 norm of the entire tensor `a` (Euclidean length)

```
a = [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12]]    shape (3, 4)

b = [[2, 2, 2, 2],
     [2, 2, 2, 2],
     [2, 2, 2, 2]]       shape (3, 4)
```
""",
        "starter_code": """import torch

a = torch.arange(1, 13, dtype=torch.float32).reshape(3, 4)
b = torch.full((3, 4), 2.0)

# 1. Element-wise addition
add_result = # YOUR CODE HERE

# 2. Element-wise multiplication
mul_result = # YOUR CODE HERE

# 3. Sum of all elements
total = # YOUR CODE HERE

# 4. Mean of each row (dim=1)
row_means = # YOUR CODE HERE

# 5. Max of each column (dim=0)
col_max = # YOUR CODE HERE

# 6. L2 norm
norm = # YOUR CODE HERE

print(f"add_result shape: {add_result.shape}")
print(f"mul_result[0]:    {mul_result[0]}")
print(f"total:            {total.item()}")
print(f"row_means:        {row_means}")
print(f"col_max:          {col_max}")
print(f"norm:             {norm.item():.4f}")
""",
        "expected_output": "total:            78.0",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "arithmetic", "reduction", "sum", "mean"],
        "xp_reward": 10,
        "time_estimate_mins": 15,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

a = torch.arange(1, 13, dtype=torch.float32).reshape(3, 4)
b = torch.full((3, 4), 2.0)

add_result = a + b
mul_result = a * b
total      = a.sum()
row_means  = a.mean(dim=1)
col_max    = a.max(dim=0).values
norm       = torch.norm(a)

print(f"add_result shape: {add_result.shape}")
print(f"mul_result[0]:    {mul_result[0]}")
print(f"total:            {total.item()}")
print(f"row_means:        {row_means}")
print(f"col_max:          {col_max}")
print(f"norm:             {norm.item():.4f}")
""",
                "explanation": (
                    "`dim=1` reduces along rows (across columns), producing one value per row. "
                    "`dim=0` reduces along the column axis, producing one value per column. "
                    "`a.max(dim=0)` returns a named tuple `(values, indices)` — use `.values`. "
                    "`torch.norm(a)` computes the Frobenius norm (L2 over all elements)."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Tensor Device Management",
        "slug": "tensor-device-management",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## Tensor Device Management

One of PyTorch's killer features is seamless CPU↔GPU transfer.
All tensors live on a **device** — always check before performing operations
or you'll get a dreaded `RuntimeError: Expected all tensors to be on the same device`.

### Task
1. Create a float32 tensor `cpu_tensor` on **CPU** with values `[[1, 2], [3, 4]]`
2. Detect if a GPU is available and store the device in `device`
3. Move `cpu_tensor` to `device` → `gpu_tensor`
4. Perform matrix multiplication `gpu_tensor @ gpu_tensor` → `result`
5. Move `result` back to **CPU** → `cpu_result`
6. Print the device of each tensor

> **Note**: If no GPU is available, both tensors will be on CPU — that is fine for this exercise.
""",
        "starter_code": """import torch

# 1. Create a tensor on CPU
cpu_tensor = # YOUR CODE HERE

# 2. Detect device
device = # YOUR CODE HERE  (hint: torch.device(...))

# 3. Move to device
gpu_tensor = # YOUR CODE HERE

# 4. Matrix multiplication on device
result = # YOUR CODE HERE

# 5. Move result back to CPU
cpu_result = # YOUR CODE HERE

print(f"cpu_tensor device: {cpu_tensor.device}")
print(f"gpu_tensor device: {gpu_tensor.device}")
print(f"result device:     {result.device}")
print(f"cpu_result device: {cpu_result.device}")
print(f"cpu_result:\\n{cpu_result}")
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "device", "cuda", "cpu", "gpu"],
        "xp_reward": 10,
        "time_estimate_mins": 10,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

cpu_tensor = torch.tensor([[1., 2.], [3., 4.]])
device     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
gpu_tensor = cpu_tensor.to(device)
result     = gpu_tensor @ gpu_tensor
cpu_result = result.cpu()

print(f"cpu_tensor device: {cpu_tensor.device}")
print(f"gpu_tensor device: {gpu_tensor.device}")
print(f"result device:     {result.device}")
print(f"cpu_result device: {cpu_result.device}")
print(f"cpu_result:\\n{cpu_result}")
""",
                "explanation": (
                    "The canonical pattern is `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`. "
                    "`.to(device)` moves any tensor to any device. `.cpu()` is shorthand for `.to('cpu')`. "
                    "Both `@` and `torch.matmul()` perform matrix multiplication — `@` is preferred for clarity."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "In-place Operations and Memory",
        "slug": "inplace-operations-memory",
        "difficulty": "basic",
        "question_type": "debug_model",
        "problem_statement": """## In-place Operations and Memory

In-place operations (those ending with `_`) **modify the tensor directly**
without creating a new one, saving memory. However, they can break autograd
if used carelessly on tensors that require gradients.

### The Bug
The code below has **two bugs** related to in-place operations.
Find and fix them.

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# Bug 1: This modifies x in-place, which will break backprop
x.add_(10)

y = x * 2
loss = y.sum()
loss.backward()   # ← RuntimeError here

# Bug 2: The programmer wants a new tensor z = x + 5,
# but accidentally modifies x in-place instead
x.add_(5)
z = x              # z is now the same object as x, not a copy
print(f"x: {x}")
print(f"z: {z}")  # should be original x + 5, but x has already been modified
```

### Task
Fix both bugs:
1. Replace the in-place op that breaks `requires_grad`
2. Make `z` a proper independent copy = original values + 5
""",
        "starter_code": """import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# FIX BUG 1: replace the in-place operation below
x.add_(10)   # <-- fix this line

y = x * 2
loss = y.sum()
loss.backward()
print(f"x.grad: {x.grad}")   # should be tensor([2., 2., 2.])

# FIX BUG 2: make z an independent tensor = original x + 5
x_original = torch.tensor([1.0, 2.0, 3.0])
x_original.add_(5)   # <-- fix this so z is independent
z = x_original
print(f"x_original: {x_original}")   # should still be [1, 2, 3]
print(f"z: {z}")                     # should be [6, 7, 8]
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "in-place", "autograd", "memory", "debugging"],
        "xp_reward": 10,
        "time_estimate_mins": 15,
        "solutions": [
            {
                "title": "Fixed Solution",
                "code": """import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# FIX 1: use out-of-place addition — creates a NEW tensor, leaves x unchanged
x_shifted = x + 10

y    = x_shifted * 2
loss = y.sum()
loss.backward()
print(f"x.grad: {x.grad}")   # tensor([2., 2., 2.])

# FIX 2: use clone() + out-of-place op so z is truly independent
x_original = torch.tensor([1.0, 2.0, 3.0])
z = x_original + 5   # creates a new tensor, x_original unchanged
print(f"x_original: {x_original}")   # tensor([1., 2., 3.])
print(f"z: {z}")                     # tensor([6., 7., 8.])
""",
                "explanation": (
                    "In-place ops on `requires_grad=True` tensors corrupt the computation graph "
                    "because autograd records the history of operations — modifying the data "
                    "in-place makes that history inconsistent. "
                    "Bug 2: `x.add_(5); z = x` makes z an alias (same storage), not a copy. "
                    "Use `z = x + 5` for a new tensor or `z = x.clone() + 5` to be explicit."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "arange, linspace, and Special Tensors",
        "slug": "arange-linspace-special",
        "difficulty": "basic",
        "question_type": "code_completion",
        "problem_statement": """## arange, linspace, and Special Tensors

PyTorch provides factory functions to create commonly needed tensors
without manually specifying every value.

### Task
Create the following tensors using the appropriate factory function:

1. `range_t` — integers from **0 to 9** inclusive → shape `(10,)`
2. `evens` — even integers from **0 to 20** inclusive → shape `(11,)`
3. `linear` — **50 evenly spaced** float values from **0.0 to 1.0** inclusive → shape `(50,)`
4. `eye4` — **4×4 identity matrix** → shape `(4, 4)`
5. `like_zeros` — a tensor of **zeros** with the same shape and dtype as `linear`
6. `rand_int` — 5 random integers between **10 and 20** (inclusive on both ends) → shape `(5,)`
""",
        "starter_code": """import torch

# 1. 0 to 9
range_t = # YOUR CODE HERE

# 2. Even integers 0, 2, 4, ..., 20
evens = # YOUR CODE HERE

# 3. 50 values from 0.0 to 1.0
linear = # YOUR CODE HERE

# 4. 4x4 identity matrix
eye4 = # YOUR CODE HERE

# 5. Zeros with same shape/dtype as linear
like_zeros = # YOUR CODE HERE

# 6. 5 random ints in [10, 20]
rand_int = # YOUR CODE HERE

print(f"range_t:    {range_t}")
print(f"evens:      {evens}")
print(f"linear[:5]: {linear[:5]}")
print(f"eye4:\\n{eye4}")
print(f"like_zeros: {like_zeros}")
print(f"rand_int:   {rand_int}")
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "creation", "arange", "linspace", "eye"],
        "xp_reward": 10,
        "time_estimate_mins": 10,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

range_t    = torch.arange(10)
evens      = torch.arange(0, 21, 2)
linear     = torch.linspace(0.0, 1.0, 50)
eye4       = torch.eye(4)
like_zeros = torch.zeros_like(linear)
rand_int   = torch.randint(10, 21, (5,))

print(f"range_t:    {range_t}")
print(f"evens:      {evens}")
print(f"linear[:5]: {linear[:5]}")
print(f"eye4:\\n{eye4}")
print(f"like_zeros: {like_zeros}")
print(f"rand_int:   {rand_int}")
""",
                "explanation": (
                    "`torch.arange(start, stop, step)` — stop is **exclusive**. "
                    "`torch.linspace(start, stop, n)` — stop is **inclusive**, generates exactly n points. "
                    "`torch.randint(low, high, size)` — high is **exclusive**, so use 21 to include 20. "
                    "`torch.zeros_like(t)` inherits shape and dtype from `t`."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    # ═══════════════════════════════════════════════════════════════
    # INTERMEDIATE (7 exercises)
    # ═══════════════════════════════════════════════════════════════

    {
        "title": "Broadcasting: Rules and Practice",
        "slug": "broadcasting-rules-practice",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": """## Broadcasting: Rules and Practice

Broadcasting allows PyTorch to perform operations between tensors of **different shapes**
by automatically expanding dimensions — without copying data.

### Broadcasting Rules (applied right-to-left on dimensions)
1. If tensors have different number of dims, **prepend 1s** to the smaller shape
2. Dimensions are compatible if they are **equal** or one of them is **1**
3. The output shape is the **maximum** of each dimension

### Example
```
A: (3, 1, 4)  +  B: (2, 4)
→ B treated as: (1, 2, 4)
→ Result shape: (3, 2, 4)
```

### Task
**Without running the code first**, predict the output shape of each operation,
then implement and verify:

1. `r1 = a + b` where `a.shape=(4, 1)`, `b.shape=(1, 3)` → predicted shape: ?
2. `r2 = x - y` where `x.shape=(2, 3, 4)`, `y.shape=(3, 1)` → predicted shape: ?
3. `r3 = m * v` where `m.shape=(5, 4)`, `v.shape=(4,)` → predicted shape: ?
4. Normalize each row of `data` (shape `5×3`) by subtracting the row mean and dividing by row std

**Implement the normalization in r4 using broadcasting — no loops.**
""",
        "starter_code": """import torch

# Setup
a = torch.ones(4, 1)
b = torch.ones(1, 3)
x = torch.ones(2, 3, 4)
y = torch.ones(3, 1)
m = torch.ones(5, 4)
v = torch.ones(4)

# 1-3: Predict then compute
r1 = # YOUR CODE HERE  (predicted shape: ?)
r2 = # YOUR CODE HERE  (predicted shape: ?)
r3 = # YOUR CODE HERE  (predicted shape: ?)

print(f"r1 shape: {r1.shape}")
print(f"r2 shape: {r2.shape}")
print(f"r3 shape: {r3.shape}")

# 4: Row-wise normalization (subtract row mean, divide by row std)
torch.manual_seed(42)
data = torch.randn(5, 3)

r4 = # YOUR CODE HERE  — normalize WITHOUT any Python for-loops

print(f"r4 shape:       {r4.shape}")
print(f"r4 row means:   {r4.mean(dim=1)}")    # should be ~0
print(f"r4 row stds:    {r4.std(dim=1)}")     # should be ~1
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "broadcasting", "normalization", "intermediate"],
        "xp_reward": 20,
        "time_estimate_mins": 20,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch

a = torch.ones(4, 1)
b = torch.ones(1, 3)
x = torch.ones(2, 3, 4)
y = torch.ones(3, 1)
m = torch.ones(5, 4)
v = torch.ones(4)

r1 = a + b          # (4,1) + (1,3)  → (4, 3)
r2 = x - y          # (2,3,4) - (3,1) → (2, 3, 4)
r3 = m * v          # (5,4)  * (4,)   → (5, 4)

print(f"r1 shape: {r1.shape}")
print(f"r2 shape: {r2.shape}")
print(f"r3 shape: {r3.shape}")

torch.manual_seed(42)
data = torch.randn(5, 3)

row_mean = data.mean(dim=1, keepdim=True)   # shape (5, 1)
row_std  = data.std(dim=1, keepdim=True)    # shape (5, 1)
r4 = (data - row_mean) / row_std            # broadcast: (5,3) - (5,1)

print(f"r4 shape:       {r4.shape}")
print(f"r4 row means:   {r4.mean(dim=1)}")
print(f"r4 row stds:    {r4.std(dim=1)}")
""",
                "explanation": (
                    "The critical detail is `keepdim=True`. Without it, `.mean(dim=1)` produces shape `(5,)` "
                    "and `data - row_mean` would fail or broadcast incorrectly. With `keepdim=True`, shape is "
                    "`(5, 1)` which broadcasts correctly against `(5, 3)`. This is the canonical "
                    "row-wise normalization pattern."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Matrix Multiplication: mm, bmm, and einsum",
        "slug": "matmul-bmm-einsum",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": """## Matrix Multiplication: mm, bmm, and einsum

Matrix multiplication is the backbone of neural networks.
PyTorch provides multiple APIs — knowing when to use each is important
for writing readable and efficient code.

| Function | Use case |
|---|---|
| `torch.mm(A, B)` | 2D × 2D only |
| `torch.matmul(A, B)` or `A @ B` | Any dims, broadcasting supported |
| `torch.bmm(A, B)` | Batched 3D: (B,m,k) × (B,k,n) |
| `torch.einsum(eq, A, B)` | Expressive notation for any contraction |

### Task
1. `out1` — multiply `W` (3×4) by `x` (4×1) using `torch.mm` → shape `(3, 1)`
2. `out2` — batch matrix multiply `queries` (8×5×64) by `keys_T` (8×64×5) using `torch.bmm` → shape `(8, 5, 5)` (attention scores)
3. `out3` — outer product of vectors `u` (3,) and `v` (4,) using `torch.einsum` → shape `(3, 4)`
4. `out4` — batched dot product: element-wise multiply then sum over last dim for `A` (32×128) and `B` (32×128) → shape `(32,)` using einsum
""",
        "starter_code": """import torch
torch.manual_seed(0)

W       = torch.randn(3, 4)
x       = torch.randn(4, 1)
queries = torch.randn(8, 5, 64)
keys_T  = torch.randn(8, 64, 5)
u       = torch.randn(3)
v       = torch.randn(4)
A       = torch.randn(32, 128)
B       = torch.randn(32, 128)

# 1. 2D matrix multiplication
out1 = # YOUR CODE HERE

# 2. Batched matrix multiplication
out2 = # YOUR CODE HERE

# 3. Outer product via einsum
out3 = # YOUR CODE HERE

# 4. Batched dot product via einsum
out4 = # YOUR CODE HERE

print(f"out1 shape: {out1.shape}")    # (3, 1)
print(f"out2 shape: {out2.shape}")    # (8, 5, 5)
print(f"out3 shape: {out3.shape}")    # (3, 4)
print(f"out4 shape: {out4.shape}")    # (32,)
""",
        "expected_output_shape": "(8, 5, 5)",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "matmul", "einsum", "bmm", "linear-algebra"],
        "xp_reward": 20,
        "time_estimate_mins": 20,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch
torch.manual_seed(0)

W       = torch.randn(3, 4)
x       = torch.randn(4, 1)
queries = torch.randn(8, 5, 64)
keys_T  = torch.randn(8, 64, 5)
u       = torch.randn(3)
v       = torch.randn(4)
A       = torch.randn(32, 128)
B       = torch.randn(32, 128)

out1 = torch.mm(W, x)
out2 = torch.bmm(queries, keys_T)
out3 = torch.einsum('i,j->ij', u, v)
out4 = torch.einsum('bd,bd->b', A, B)

print(f"out1 shape: {out1.shape}")
print(f"out2 shape: {out2.shape}")
print(f"out3 shape: {out3.shape}")
print(f"out4 shape: {out4.shape}")
""",
                "explanation": (
                    "Einsum notation: letters represent dimensions, repeated letters are summed over. "
                    "`'i,j->ij'` = outer product (no shared letter, so no summation). "
                    "`'bd,bd->b'` = batch dot product (d is shared and absent from output, so summed). "
                    "`bmm` is faster than `matmul` for guaranteed 3D inputs because it skips the generality checks."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Views vs Copies: contiguous() and clone()",
        "slug": "views-copies-contiguous-clone",
        "difficulty": "intermediate",
        "question_type": "debug_model",
        "problem_statement": """## Views vs Copies: contiguous() and clone()

In PyTorch, many operations return **views** — they share underlying storage
with the original tensor. Modifying a view modifies the original.

This is efficient (no copy overhead) but can cause subtle bugs.

### The Bug
The code below tries to:
1. Permute `x` and then flatten it for a linear layer
2. Detach a gradient tensor and modify it safely

It has **two bugs**. Find and fix them.

```python
import torch
import torch.nn as nn

# Bug 1
x = torch.randn(2, 3, 4)
x_permuted = x.permute(0, 2, 1)   # (2, 4, 3)
x_flat = x_permuted.view(2, -1)   # RuntimeError: non-contiguous
# ^ view() fails on non-contiguous tensors

# Bug 2
w = torch.randn(5, requires_grad=True)
grads = w.grad if w.grad is not None else torch.zeros_like(w)
grads += 1   # modifying grads also modifies w.grad in-place!
             # (shared storage — not a safe copy)
```
""",
        "starter_code": """import torch

# ── BUG 1 ─────────────────────────────────────────────────────────
x = torch.randn(2, 3, 4)
x_permuted = x.permute(0, 2, 1)   # (2, 4, 3) — non-contiguous after permute

# FIX: make x_flat work correctly — shape should be (2, 12)
x_flat = x_permuted.view(2, -1)   # <-- fix this line
print(f"x_flat shape: {x_flat.shape}")   # should be (2, 12)

# ── BUG 2 ─────────────────────────────────────────────────────────
w = torch.randn(5, requires_grad=True)
y = (w * 2).sum()
y.backward()

# FIX: get a safe, independent copy of w.grad
grads = w.grad    # <-- fix: this is NOT a copy; it shares storage
grads += 1        # this modifies w.grad too!

print(f"w.grad after modification: {w.grad}")   # should be all 2s (unmodified)
print(f"grads: {grads}")                        # should be all 3s (2 + 1)
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "contiguous", "clone", "view", "memory", "debugging"],
        "xp_reward": 20,
        "time_estimate_mins": 20,
        "solutions": [
            {
                "title": "Fixed Solution",
                "code": """import torch

# FIX 1: call .contiguous() before .view(), OR use .reshape() which handles it
x = torch.randn(2, 3, 4)
x_permuted = x.permute(0, 2, 1)

x_flat = x_permuted.contiguous().view(2, -1)   # fix: make contiguous first
# Alternative: x_flat = x_permuted.reshape(2, -1)  # reshape handles non-contiguous

print(f"x_flat shape: {x_flat.shape}")

# FIX 2: clone() creates independent storage
w = torch.randn(5, requires_grad=True)
y = (w * 2).sum()
y.backward()

grads = w.grad.clone()   # fix: clone creates a copy with independent storage
grads += 1

print(f"w.grad after modification: {w.grad}")   # still [2,2,2,2,2] — unmodified
print(f"grads: {grads}")                        # [3,3,3,3,3]
""",
                "explanation": (
                    "`permute()` changes the stride pattern without moving data — the result is non-contiguous. "
                    "`view()` requires contiguous memory layout (C-order). Fix: `.contiguous().view()` or just `.reshape()`. "
                    "`clone()` creates a tensor with new storage. Without it, `grads = w.grad` is just "
                    "another name for the same memory — any in-place op on `grads` modifies `w.grad`."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Fancy Indexing with Boolean Masks",
        "slug": "fancy-indexing-boolean-masks",
        "difficulty": "intermediate",
        "question_type": "build_from_scratch",
        "problem_statement": """## Fancy Indexing with Boolean Masks

Boolean masking lets you select, filter, and modify tensor elements based
on conditions — essential for implementing attention masks, padding masks,
and data cleaning pipelines.

### Task
You have a batch of logits from a model: shape `(4, 6)` — 4 samples, 6 classes.

1. `high_confidence_mask` — boolean mask where logits > 0.5 → shape `(4, 6)`
2. `high_confidence_values` — the actual logit values that meet this threshold → 1D tensor
3. `clamped` — copy of logits where all values **below -0.5 are set to -0.5** and **above 0.5 are set to 0.5** (clamping) → shape `(4, 6)`
4. `top2_per_row` — indices of the **top 2 logits** in each row → shape `(4, 2)`
5. `zeroed` — copy of logits where the bottom 3 logits per row are zeroed out → shape `(4, 6)`

Do steps 1–5 without any Python for-loops.
""",
        "starter_code": """import torch
torch.manual_seed(7)

logits = torch.randn(4, 6)
print("logits:\\n", logits, "\\n")

# 1. Boolean mask: logits > 0.5
high_confidence_mask = # YOUR CODE HERE

# 2. Values where mask is True (1D)
high_confidence_values = # YOUR CODE HERE

# 3. Clamp values to [-0.5, 0.5]
clamped = # YOUR CODE HERE

# 4. Indices of top 2 logits per row
top2_per_row = # YOUR CODE HERE

# 5. Zero out the bottom 3 logits per row
zeroed = # YOUR CODE HERE (hint: torch.topk)

print(f"high_confidence_mask:\\n{high_confidence_mask}")
print(f"high_confidence_values: {high_confidence_values}")
print(f"clamped:\\n{clamped}")
print(f"top2_per_row:\\n{top2_per_row}")
print(f"zeroed:\\n{zeroed}")
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "indexing", "boolean-mask", "topk", "intermediate"],
        "xp_reward": 20,
        "time_estimate_mins": 25,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch
torch.manual_seed(7)

logits = torch.randn(4, 6)

high_confidence_mask   = logits > 0.5
high_confidence_values = logits[high_confidence_mask]
clamped                = torch.clamp(logits, min=-0.5, max=0.5)
top2_per_row           = torch.topk(logits, k=2, dim=1).indices

# Zero bottom 3: keep top 3, zero the rest
zeroed = torch.zeros_like(logits)
top3_indices = torch.topk(logits, k=3, dim=1).indices
zeroed.scatter_(1, top3_indices, logits.gather(1, top3_indices))

print(f"high_confidence_mask:\\n{high_confidence_mask}")
print(f"high_confidence_values: {high_confidence_values}")
print(f"clamped:\\n{clamped}")
print(f"top2_per_row:\\n{top2_per_row}")
print(f"zeroed:\\n{zeroed}")
""",
                "explanation": (
                    "`logits[mask]` returns a 1D tensor of all values where mask is True — the positions are not preserved. "
                    "`torch.clamp()` is the idiomatic way to clip values to a range. "
                    "`torch.topk(k, dim)` returns (values, indices); for zeroing-out, we use `scatter_` to place "
                    "only the top-k values back into a zeros tensor — a common pattern in sparse attention."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Stacking, Concatenating, and Splitting Tensors",
        "slug": "stack-cat-split",
        "difficulty": "intermediate",
        "question_type": "code_completion",
        "problem_statement": """## Stacking, Concatenating, and Splitting Tensors

Assembling mini-batches, combining feature maps, and splitting model outputs
all require fluent use of `torch.cat`, `torch.stack`, and their inverses.

| Function | What it does |
|---|---|
| `torch.cat([A, B], dim)` | Concatenate along **existing** dim — shapes must match on all other dims |
| `torch.stack([A, B], dim)` | Stack along a **new** dim — all tensors must have identical shapes |
| `torch.split(t, size, dim)` | Split into chunks of given size along dim |
| `torch.chunk(t, n, dim)` | Split into n equal chunks |
| `torch.unbind(t, dim)` | Returns tuple of tensors with that dim removed |

### Task
1. `batch` — stack 4 single-sample tensors (each shape `(3, 32, 32)`) into a batch → shape `(4, 3, 32, 32)`
2. `tall` — concatenate `top` (shape `(3, 4)`) and `bottom` (shape `(5, 4)`) vertically → shape `(8, 4)`
3. `wide` — concatenate `left` (shape `(6, 3)`) and `right` (shape `(6, 5)`) horizontally → shape `(6, 8)`
4. `chunks` — split `wide` into 2 equal tensors along dim=1 → each shape `(6, 4)`
5. `frames` — unbind `batch` along dim=0 → tuple of 4 tensors each shape `(3, 32, 32)`
""",
        "starter_code": """import torch
torch.manual_seed(1)

samples = [torch.randn(3, 32, 32) for _ in range(4)]
top    = torch.randn(3, 4)
bottom = torch.randn(5, 4)
left   = torch.randn(6, 3)
right  = torch.randn(6, 5)

# 1. Stack samples into a batch
batch = # YOUR CODE HERE

# 2. Vertical concatenation
tall = # YOUR CODE HERE

# 3. Horizontal concatenation
wide = # YOUR CODE HERE

# 4. Split wide into 2 equal chunks
chunks = # YOUR CODE HERE

# 5. Unbind batch along dim 0
frames = # YOUR CODE HERE

print(f"batch shape:    {batch.shape}")       # (4, 3, 32, 32)
print(f"tall shape:     {tall.shape}")        # (8, 4)
print(f"wide shape:     {wide.shape}")        # (6, 8)
print(f"chunks[0]:      {chunks[0].shape}")   # (6, 4)
print(f"len(frames):    {len(frames)}")       # 4
print(f"frames[0]:      {frames[0].shape}")   # (3, 32, 32)
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "cat", "stack", "split", "intermediate"],
        "xp_reward": 20,
        "time_estimate_mins": 18,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch
torch.manual_seed(1)

samples = [torch.randn(3, 32, 32) for _ in range(4)]
top    = torch.randn(3, 4)
bottom = torch.randn(5, 4)
left   = torch.randn(6, 3)
right  = torch.randn(6, 5)

batch  = torch.stack(samples, dim=0)
tall   = torch.cat([top, bottom], dim=0)
wide   = torch.cat([left, right], dim=1)
chunks = torch.chunk(wide, 2, dim=1)
frames = torch.unbind(batch, dim=0)

print(f"batch shape:    {batch.shape}")
print(f"tall shape:     {tall.shape}")
print(f"wide shape:     {wide.shape}")
print(f"chunks[0]:      {chunks[0].shape}")
print(f"len(frames):    {len(frames)}")
print(f"frames[0]:      {frames[0].shape}")
""",
                "explanation": (
                    "`stack` creates a NEW dimension; all input tensors must have the same shape. "
                    "`cat` requires matching shapes on ALL dimensions except the concatenation dim. "
                    "`chunk` may return fewer chunks if the size doesn't divide evenly — use `split(size)` "
                    "for exact chunk sizes. `unbind` is the inverse of `stack` — it removes the specified dim."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Tensor to NumPy and Back",
        "slug": "tensor-numpy-interop",
        "difficulty": "intermediate",
        "question_type": "build_from_scratch",
        "problem_statement": """## Tensor to NumPy and Back

Real pipelines mix PyTorch with NumPy (for data loading, metrics, plotting).
Understanding the **shared memory** relationship between CPU tensors and NumPy arrays
is critical to avoiding silent bugs.

### Key Rules
- `.numpy()` returns a NumPy array that **shares memory** with the CPU tensor
- Modifying the NumPy array **modifies the tensor** and vice versa
- GPU tensors must be moved to CPU before `.numpy()`
- `requires_grad=True` tensors must be `.detach()`ed first
- `torch.from_numpy(arr)` creates a tensor that **shares memory** with the array

### Task
1. Convert a CPU tensor `t` to a NumPy array `arr` using `.numpy()`
2. Modify `arr[0]` to 99 — observe that `t[0]` also changes
3. Create a NEW independent NumPy array `arr_copy` from `t` (modifying it must NOT affect `t`)
4. Convert a NumPy array `np_data` back to a tensor `t2` using `torch.from_numpy`
5. Safely convert a GPU/grad tensor `g` to NumPy (handle both cases)
""",
        "starter_code": """import torch
import numpy as np

# ── Part 1-3: CPU tensor ↔ NumPy ─────────────────────────────────
t = torch.tensor([1.0, 2.0, 3.0, 4.0])

# 1. Convert to NumPy (shared memory)
arr = # YOUR CODE HERE

# 2. Modify arr[0] and check if t changes
arr[0] = 99
print(f"t after arr[0]=99: {t}")        # should show 99.0

# 3. Independent NumPy copy (modifying it should NOT change t)
arr_copy = # YOUR CODE HERE
arr_copy[0] = 0
print(f"t after arr_copy[0]=0: {t}")    # should still show 99.0

# ── Part 4: NumPy → Tensor ───────────────────────────────────────
np_data = np.array([10.0, 20.0, 30.0], dtype=np.float32)
t2 = # YOUR CODE HERE

print(f"t2: {t2}  dtype={t2.dtype}")

# ── Part 5: Safe conversion of grad/GPU tensor ───────────────────
g = torch.randn(3, requires_grad=True)
y = g * 2

# Safely convert y to numpy (it has grad_fn, possibly on GPU)
y_np = # YOUR CODE HERE

print(f"y_np: {y_np}  type={type(y_np)}")
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "numpy", "interop", "intermediate"],
        "xp_reward": 20,
        "time_estimate_mins": 20,
        "solutions": [
            {
                "title": "Clean Solution",
                "code": """import torch
import numpy as np

t   = torch.tensor([1.0, 2.0, 3.0, 4.0])
arr = t.numpy()

arr[0] = 99
print(f"t after arr[0]=99: {t}")       # tensor([99., 2., 3., 4.])

arr_copy = t.numpy().copy()             # .copy() breaks the shared memory link
arr_copy[0] = 0
print(f"t after arr_copy[0]=0: {t}")   # still tensor([99., 2., 3., 4.])

np_data = np.array([10.0, 20.0, 30.0], dtype=np.float32)
t2 = torch.from_numpy(np_data)
print(f"t2: {t2}  dtype={t2.dtype}")

g = torch.randn(3, requires_grad=True)
y = g * 2
y_np = y.detach().cpu().numpy()        # detach removes from graph, .cpu() ensures CPU
print(f"y_np: {y_np}  type={type(y_np)}")
""",
                "explanation": (
                    "`.numpy()` zero-copy shares storage — fast but dangerous. Always `.copy()` if you "
                    "need independence. For tensors with `grad_fn`: `.detach()` creates a new tensor that "
                    "shares data but is removed from the computation graph. The safe idiom is always "
                    "`.detach().cpu().numpy()` — order matters: detach first, then move to CPU, then convert."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    # ═══════════════════════════════════════════════════════════════
    # ADVANCED (5 exercises)
    # ═══════════════════════════════════════════════════════════════

    {
        "title": "Implement Softmax from Scratch (Numerically Stable)",
        "slug": "softmax-from-scratch-stable",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": """## Implement Softmax from Scratch (Numerically Stable)

Softmax converts raw logits into probabilities. The naive formula is:

$$\\text{softmax}(x_i) = \\frac{e^{x_i}}{\\sum_j e^{x_j}}$$

### The Problem with Naive Softmax
For large logits (e.g., 1000), `exp(1000)` overflows to `inf`.
For very negative logits, `exp(-1000) = 0`, causing division by zero.

### The Fix: Subtract the max
$$\\text{softmax}(x_i) = \\frac{e^{x_i - \\max(x)}}{\\sum_j e^{x_j - \\max(x)}}$$

This is mathematically identical but numerically stable.

### Task
1. Implement `naive_softmax(x)` — the direct formula (will overflow for large values)
2. Implement `stable_softmax(x)` — subtracting row-wise max before exp
3. Implement `stable_softmax_batched(x)` — for a **2D batch** input, apply softmax along dim=1
4. Verify against `torch.nn.functional.softmax` on a normal input
5. Show that naive fails and stable succeeds on `large_logits`

**All implementations must use only raw tensor ops — no `F.softmax`.**
""",
        "starter_code": """import torch
import torch.nn.functional as F

def naive_softmax(x: torch.Tensor) -> torch.Tensor:
    \"\"\"x: 1D tensor\"\"\"
    # YOUR CODE HERE
    pass

def stable_softmax(x: torch.Tensor) -> torch.Tensor:
    \"\"\"x: 1D tensor — numerically stable\"\"\"
    # YOUR CODE HERE
    pass

def stable_softmax_batched(x: torch.Tensor) -> torch.Tensor:
    \"\"\"x: 2D tensor (batch, classes) — apply softmax along dim=1\"\"\"
    # YOUR CODE HERE
    pass

# Test on normal input
torch.manual_seed(0)
logits = torch.randn(5)
print(f"naive:    {naive_softmax(logits)}")
print(f"stable:   {stable_softmax(logits)}")
print(f"F.softmax:{F.softmax(logits, dim=0)}")
print(f"Match: {torch.allclose(stable_softmax(logits), F.softmax(logits, dim=0))}")

# Test on large logits
large_logits = torch.tensor([1000.0, 1001.0, 999.0])
print(f"\\nnaive on large:  {naive_softmax(large_logits)}")    # expect nan/inf
print(f"stable on large: {stable_softmax(large_logits)}")    # expect valid probs

# Test batched
batch = torch.randn(4, 10)
out = stable_softmax_batched(batch)
print(f"\\nbatched shape: {out.shape}")
print(f"row sums: {out.sum(dim=1)}")    # should all be 1.0
""",
        "expected_output_shape": "(4, 10)",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "softmax", "numerical-stability", "advanced", "implementation"],
        "xp_reward": 30,
        "time_estimate_mins": 30,
        "solutions": [
            {
                "title": "Complete Solution",
                "code": """import torch
import torch.nn.functional as F

def naive_softmax(x: torch.Tensor) -> torch.Tensor:
    e_x = torch.exp(x)
    return e_x / e_x.sum()

def stable_softmax(x: torch.Tensor) -> torch.Tensor:
    x_shifted = x - x.max()
    e_x = torch.exp(x_shifted)
    return e_x / e_x.sum()

def stable_softmax_batched(x: torch.Tensor) -> torch.Tensor:
    # keepdim=True for correct broadcasting: (B,1) broadcasts against (B,C)
    x_shifted = x - x.max(dim=1, keepdim=True).values
    e_x = torch.exp(x_shifted)
    return e_x / e_x.sum(dim=1, keepdim=True)

torch.manual_seed(0)
logits = torch.randn(5)
print(f"naive:    {naive_softmax(logits)}")
print(f"stable:   {stable_softmax(logits)}")
print(f"F.softmax:{F.softmax(logits, dim=0)}")
print(f"Match: {torch.allclose(stable_softmax(logits), F.softmax(logits, dim=0))}")

large_logits = torch.tensor([1000.0, 1001.0, 999.0])
print(f"\\nnaive on large:  {naive_softmax(large_logits)}")
print(f"stable on large: {stable_softmax(large_logits)}")

batch = torch.randn(4, 10)
out = stable_softmax_batched(batch)
print(f"\\nbatched shape: {out.shape}")
print(f"row sums: {out.sum(dim=1)}")
""",
                "explanation": (
                    "Subtracting the max shifts all values to (-inf, 0], so exp is always in (0, 1]. "
                    "Mathematically: softmax(x-c) = softmax(x) because c cancels in numerator and denominator. "
                    "For the batched version, `keepdim=True` on both max and sum is mandatory for correct broadcasting."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Efficient Pairwise Distance Matrix",
        "slug": "pairwise-distance-matrix",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": """## Efficient Pairwise Distance Matrix

Computing the pairwise L2 distance between all rows in a matrix is a core
operation in clustering, k-NN, and metric learning.

$$D_{ij} = \\| A_i - B_j \\|_2$$

### Naive approach (avoid this)
```python
D = torch.zeros(m, n)
for i in range(m):
    for j in range(n):
        D[i, j] = torch.norm(A[i] - B[j])
```
This is O(m×n×d) and very slow in Python.

### Efficient approach using the expansion
$$\\| A_i - B_j \\|^2 = \\| A_i \\|^2 + \\| B_j \\|^2 - 2 A_i \\cdot B_j$$

Which in matrix form is:
```
D² = sum(A², dim=1, keepdim) + sum(B², dim=1, keepdim).T - 2 * A @ B.T
```

### Task
1. Implement `pairwise_l2(A, B)` using the efficient matrix form (no loops)
2. Verify against a slow loop-based reference on a small input
3. Benchmark: measure time for A=(500, 128), B=(300, 128) for both methods
4. Compute the **argmin** of each row of D (nearest neighbor index in B for each point in A)
""",
        "starter_code": """import torch
import time

def pairwise_l2_slow(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    \"\"\"Reference: O(m*n) Python loop — correct but slow\"\"\"
    m, n = A.shape[0], B.shape[0]
    D = torch.zeros(m, n)
    for i in range(m):
        for j in range(n):
            D[i, j] = torch.norm(A[i] - B[j])
    return D

def pairwise_l2(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    \"\"\"
    Efficient pairwise L2 distance: shape (m, n)
    A: (m, d)
    B: (n, d)
    \"\"\"
    # YOUR CODE HERE — no loops, use matrix expansion
    pass

# ── Correctness check ────────────────────────────────────────────
torch.manual_seed(42)
A_small = torch.randn(4, 3)
B_small = torch.randn(5, 3)

D_slow = pairwise_l2_slow(A_small, B_small)
D_fast = pairwise_l2(A_small, B_small)

print("Shapes match:", D_slow.shape == D_fast.shape)
print("Values match:", torch.allclose(D_slow, D_fast, atol=1e-5))

# ── Benchmark ────────────────────────────────────────────────────
A_large = torch.randn(500, 128)
B_large = torch.randn(300, 128)

t0 = time.time()
D_fast_large = pairwise_l2(A_large, B_large)
print(f"Fast:  {(time.time()-t0)*1000:.2f}ms  shape={D_fast_large.shape}")

# ── Nearest neighbors ────────────────────────────────────────────
nearest_indices = # YOUR CODE HERE — argmin of each row in D_fast_large
print(f"nearest_indices shape: {nearest_indices.shape}")  # (500,)
print(f"first 5: {nearest_indices[:5]}")
""",
        "expected_output_shape": "(500, 300)",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "broadcasting", "performance", "knn", "advanced"],
        "xp_reward": 30,
        "time_estimate_mins": 35,
        "solutions": [
            {
                "title": "Efficient Matrix Expansion Solution",
                "code": """import torch
import time

def pairwise_l2_slow(A, B):
    m, n = A.shape[0], B.shape[0]
    D = torch.zeros(m, n)
    for i in range(m):
        for j in range(n):
            D[i, j] = torch.norm(A[i] - B[j])
    return D

def pairwise_l2(A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    A_sq = (A ** 2).sum(dim=1, keepdim=True)   # (m, 1)
    B_sq = (B ** 2).sum(dim=1, keepdim=True).T  # (1, n)
    AB   = A @ B.T                               # (m, n)
    D_sq = A_sq + B_sq - 2 * AB
    return torch.sqrt(torch.clamp(D_sq, min=0))  # clamp avoids sqrt of tiny negatives

torch.manual_seed(42)
A_small = torch.randn(4, 3)
B_small = torch.randn(5, 3)

D_slow = pairwise_l2_slow(A_small, B_small)
D_fast = pairwise_l2(A_small, B_small)
print("Shapes match:", D_slow.shape == D_fast.shape)
print("Values match:", torch.allclose(D_slow, D_fast, atol=1e-5))

A_large = torch.randn(500, 128)
B_large = torch.randn(300, 128)
t0 = time.time()
D_fast_large = pairwise_l2(A_large, B_large)
print(f"Fast:  {(time.time()-t0)*1000:.2f}ms  shape={D_fast_large.shape}")

nearest_indices = D_fast_large.argmin(dim=1)
print(f"nearest_indices shape: {nearest_indices.shape}")
print(f"first 5: {nearest_indices[:5]}")
""",
                "explanation": (
                    "The identity `||a-b||² = ||a||² + ||b||² - 2a·b` turns O(m·n·d) element-wise "
                    "subtraction into O(m·n) matmul + O(m+n) norms — massively faster. "
                    "`torch.clamp(min=0)` before sqrt handles floating-point precision errors where "
                    "D_sq is a tiny negative (e.g., -1e-8) due to rounding."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Custom CUDA-Style Operation with torch.compile",
        "slug": "torch-compile-optimization",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": """## Optimizing with torch.compile (PyTorch 2.0+)

`torch.compile()` uses TorchDynamo to trace your Python code and compile it
to optimized kernels via Triton or C++ backends — often yielding 2–4× speedups
with a single line change.

### Task
You have a custom **GELU activation** implementation and a **LayerNorm** function
that are called millions of times during training. Your job is to:

1. Implement `gelu(x)` from scratch using the exact formula:
   $$\\text{GELU}(x) = x \\cdot \\Phi(x) = x \\cdot \\frac{1}{2}\\left[1 + \\text{erf}\\left(\\frac{x}{\\sqrt{2}}\\right)\\right]$$

2. Implement `layer_norm(x, eps=1e-5)` — normalize each sample (last dim) to mean=0, std=1, then scale and shift with learnable `gamma` and `beta`

3. Wrap both in a `forward(x)` function and create compiled/uncompiled versions

4. Benchmark the compiled vs uncompiled version on a large input

5. Verify correctness against `torch.nn.functional.gelu` and `torch.nn.functional.layer_norm`

> **Note**: `torch.compile` requires PyTorch 2.0+. If unavailable, the exercise still works — just comment out the compile step and focus on the implementations.
""",
        "starter_code": """import torch
import torch.nn.functional as F
import time

def gelu(x: torch.Tensor) -> torch.Tensor:
    \"\"\"GELU activation using erf formula\"\"\"
    # YOUR CODE HERE
    pass

def layer_norm(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, eps: float = 1e-5) -> torch.Tensor:
    \"\"\"
    Apply LayerNorm over the last dimension.
    x:     (*, d)
    gamma: (d,)
    beta:  (d,)
    \"\"\"
    # YOUR CODE HERE
    pass

def forward(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor) -> torch.Tensor:
    \"\"\"Apply GELU then LayerNorm\"\"\"
    return layer_norm(gelu(x), gamma, beta)

# ── Correctness ───────────────────────────────────────────────────
torch.manual_seed(0)
x     = torch.randn(4, 64)
gamma = torch.ones(64)
beta  = torch.zeros(64)

my_gelu   = gelu(x)
ref_gelu  = F.gelu(x)
print(f"GELU match: {torch.allclose(my_gelu, ref_gelu, atol=1e-6)}")

my_ln  = layer_norm(x, gamma, beta)
ref_ln = F.layer_norm(x, (64,), gamma, beta)
print(f"LayerNorm match: {torch.allclose(my_ln, ref_ln, atol=1e-5)}")

# ── Compile & Benchmark ───────────────────────────────────────────
compiled_forward = torch.compile(forward) if hasattr(torch, 'compile') else forward

x_large = torch.randn(512, 1024)
g_large = torch.ones(1024)
b_large = torch.zeros(1024)

# Warmup
for _ in range(3):
    _ = forward(x_large, g_large, b_large)

N = 100
t0 = time.time()
for _ in range(N):
    _ = forward(x_large, g_large, b_large)
print(f"Uncompiled: {(time.time()-t0)/N*1000:.3f}ms/call")

# Warmup compiled
for _ in range(3):
    _ = compiled_forward(x_large, g_large, b_large)

t0 = time.time()
for _ in range(N):
    _ = compiled_forward(x_large, g_large, b_large)
print(f"Compiled:   {(time.time()-t0)/N*1000:.3f}ms/call")
""",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "torch-compile", "gelu", "layernorm", "advanced", "performance"],
        "xp_reward": 30,
        "time_estimate_mins": 40,
        "solutions": [
            {
                "title": "Complete Solution",
                "code": """import torch
import torch.nn.functional as F
import math
import time

def gelu(x: torch.Tensor) -> torch.Tensor:
    return x * 0.5 * (1.0 + torch.erf(x / math.sqrt(2.0)))

def layer_norm(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, eps: float = 1e-5) -> torch.Tensor:
    mean = x.mean(dim=-1, keepdim=True)
    var  = x.var(dim=-1, keepdim=True, unbiased=False)
    x_hat = (x - mean) / torch.sqrt(var + eps)
    return gamma * x_hat + beta

def forward(x, gamma, beta):
    return layer_norm(gelu(x), gamma, beta)

torch.manual_seed(0)
x     = torch.randn(4, 64)
gamma = torch.ones(64)
beta  = torch.zeros(64)

print(f"GELU match: {torch.allclose(gelu(x), F.gelu(x), atol=1e-6)}")
print(f"LayerNorm match: {torch.allclose(layer_norm(x, gamma, beta), F.layer_norm(x, (64,), gamma, beta), atol=1e-5)}")

compiled_forward = torch.compile(forward) if hasattr(torch, 'compile') else forward

x_large = torch.randn(512, 1024)
g_large = torch.ones(1024)
b_large = torch.zeros(1024)

for _ in range(3): _ = forward(x_large, g_large, b_large)
N = 100
t0 = time.time()
for _ in range(N): _ = forward(x_large, g_large, b_large)
print(f"Uncompiled: {(time.time()-t0)/N*1000:.3f}ms/call")

for _ in range(3): _ = compiled_forward(x_large, g_large, b_large)
t0 = time.time()
for _ in range(N): _ = compiled_forward(x_large, g_large, b_large)
print(f"Compiled:   {(time.time()-t0)/N*1000:.3f}ms/call")
""",
                "explanation": (
                    "LayerNorm uses `unbiased=False` (population variance, not sample variance) to match PyTorch's "
                    "nn.LayerNorm. The eps is added inside the sqrt for numerical stability. "
                    "torch.compile works best on functions called many times with the same input shapes — "
                    "it traces once and reuses the compiled kernel. Speedup is most visible on GPU."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Sparse Tensors and Embeddings",
        "slug": "sparse-tensors-embeddings",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": """## Sparse Tensors and Embeddings

When your data is mostly zeros (e.g., one-hot encodings, adjacency matrices),
**sparse tensors** save memory by storing only non-zero values.

### Task
1. Create a sparse COO tensor representing a 5×5 matrix where only positions
   `(0,1)=0.5`, `(2,3)=1.2`, `(4,0)=3.0` are non-zero
2. Convert it to dense format and verify values
3. Implement a manual **embedding lookup** from scratch:
   - Given an embedding matrix `E` of shape `(vocab_size, embed_dim)`
   - And token indices `ids` of shape `(batch, seq_len)`
   - Return the embedded representations without using `nn.Embedding`
4. Compare your manual lookup against `nn.Embedding` for correctness
5. Implement **embedding bag**: given variable-length sequences stored as a flat
   list + offsets, compute the **mean** embedding per sequence

Example of embedding bag input:
```
sequences = [tokens for seq 0] + [tokens for seq 1] + [tokens for seq 2]
offsets   = [start index of each sequence]
```
""",
        "starter_code": """import torch
import torch.nn as nn

# ── Part 1-2: Sparse COO Tensor ───────────────────────────────────
# Create sparse tensor: (0,1)=0.5, (2,3)=1.2, (4,0)=3.0  size=5×5
indices = # YOUR CODE HERE  shape (2, nnz)
values  = # YOUR CODE HERE  shape (nnz,)
sparse_t = # YOUR CODE HERE  torch.sparse_coo_tensor(...)

print(f"sparse_t shape:  {sparse_t.shape}")
print(f"nnz:             {sparse_t._nnz()}")

dense = sparse_t.to_dense()
print(f"dense:\\n{dense}")

# ── Part 3-4: Manual Embedding Lookup ────────────────────────────
torch.manual_seed(0)
vocab_size, embed_dim = 100, 16
E = torch.randn(vocab_size, embed_dim)

batch_ids = torch.randint(0, vocab_size, (4, 10))   # (batch=4, seq_len=10)

# Manual lookup — no nn.Embedding, no loops
manual_embeds = # YOUR CODE HERE  shape (4, 10, 16)

# Reference
emb_layer = nn.Embedding(vocab_size, embed_dim)
emb_layer.weight.data = E
ref_embeds = emb_layer(batch_ids)

print(f"Manual shape: {manual_embeds.shape}")
print(f"Match ref:    {torch.allclose(manual_embeds, ref_embeds)}")

# ── Part 5: Embedding Bag (mean pooling) ─────────────────────────
# 3 sequences of different lengths: [2, 4, 3] tokens
input_ids = torch.tensor([1, 3,         # seq 0: len 2
                           7, 2, 5, 9,   # seq 1: len 4
                           4, 6, 8])     # seq 2: len 3

offsets = # YOUR CODE HERE  start index of each sequence

# Compute mean embedding per sequence using offsets — no loops
result = # YOUR CODE HERE  shape (3, embed_dim)

print(f"result shape: {result.shape}")   # (3, 16)
""",
        "expected_output_shape": "(3, 16)",
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "sparse", "embeddings", "advanced"],
        "xp_reward": 30,
        "time_estimate_mins": 45,
        "solutions": [
            {
                "title": "Complete Solution",
                "code": """import torch
import torch.nn as nn

# Sparse COO
indices  = torch.tensor([[0, 2, 4], [1, 3, 0]])  # rows, cols
values   = torch.tensor([0.5, 1.2, 3.0])
sparse_t = torch.sparse_coo_tensor(indices, values, size=(5, 5))

print(f"sparse_t shape:  {sparse_t.shape}")
print(f"nnz:             {sparse_t._nnz()}")
dense = sparse_t.to_dense()
print(f"dense:\\n{dense}")

# Manual embedding lookup
torch.manual_seed(0)
vocab_size, embed_dim = 100, 16
E = torch.randn(vocab_size, embed_dim)
batch_ids = torch.randint(0, vocab_size, (4, 10))

manual_embeds = E[batch_ids]   # fancy indexing: E[(4,10)] → (4, 10, 16)

emb_layer = nn.Embedding(vocab_size, embed_dim)
emb_layer.weight.data = E
ref_embeds = emb_layer(batch_ids)

print(f"Manual shape: {manual_embeds.shape}")
print(f"Match ref:    {torch.allclose(manual_embeds, ref_embeds)}")

# Embedding bag — mean per sequence
input_ids = torch.tensor([1, 3, 7, 2, 5, 9, 4, 6, 8])
offsets   = torch.tensor([0, 2, 6])   # seq 0 starts at 0, seq 1 at 2, seq 2 at 6

# Use nn.EmbeddingBag for reference (same as manual mean)
bag = nn.EmbeddingBag(vocab_size, embed_dim, mode='mean')
bag.weight.data = E
result = bag(input_ids, offsets)

print(f"result shape: {result.shape}")
""",
                "explanation": (
                    "The key insight for manual embedding lookup: `E[batch_ids]` where `batch_ids` has shape `(4,10)` "
                    "returns shape `(4, 10, 16)` — PyTorch applies fancy indexing to the first dimension. "
                    "For sparse COO: indices shape is `(n_dims, nnz)`, not `(nnz, n_dims)`. "
                    "`EmbeddingBag` handles variable-length sequences efficiently using offsets "
                    "without requiring padding — it's faster than manual mean-pooling for production use."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },

    {
        "title": "Quantized Tensors: INT8 Inference",
        "slug": "quantized-tensors-int8",
        "difficulty": "advanced",
        "question_type": "build_from_scratch",
        "problem_statement": """## Quantized Tensors: INT8 Inference

**Quantization** reduces model size and speeds up inference by representing
weights in lower precision (e.g., INT8 instead of FP32).

The mapping from float to int8:
$$x_{\\text{int8}} = \\text{clamp}\\left(\\text{round}\\left(\\frac{x}{\\text{scale}}\\right) + \\text{zero\\_point}, -128, 127\\right)$$

Dequantization (back to float):
$$x_{\\text{float}} = \\text{scale} \\times (x_{\\text{int8}} - \\text{zero\\_point})$$

### Task
1. Implement `quantize_tensor(x, num_bits=8)` — compute scale and zero_point from tensor statistics, then quantize to INT8
2. Implement `dequantize_tensor(x_q, scale, zero_point)` — recover approximate float values
3. Compute the **quantization error** (max absolute difference) between original and dequantized
4. Apply your quantizer to the weight matrix of a `nn.Linear` layer and compare the output of:
   - Original FP32 linear layer
   - Manually dequantized-weight linear layer
5. Measure memory savings: compare storage size of FP32 vs INT8 weights
""",
        "starter_code": """import torch
import torch.nn as nn

def quantize_tensor(x: torch.Tensor, num_bits: int = 8):
    \"\"\"
    Asymmetric min-max quantization.
    Returns: (x_quantized_int8, scale, zero_point)
    \"\"\"
    # YOUR CODE HERE
    # 1. Compute qmin, qmax from num_bits
    # 2. Compute scale from x.min(), x.max()
    # 3. Compute zero_point
    # 4. Quantize and clamp to [qmin, qmax]
    pass

def dequantize_tensor(x_q: torch.Tensor, scale: float, zero_point: int) -> torch.Tensor:
    \"\"\"Recover approximate float values from quantized tensor\"\"\"
    # YOUR CODE HERE
    pass

# ── Test on a weight matrix ───────────────────────────────────────
torch.manual_seed(42)
W = torch.randn(64, 128)   # typical linear layer weight

x_q, scale, zp = quantize_tensor(W)
W_deq = dequantize_tensor(x_q, scale, zp)

print(f"Original dtype:     {W.dtype}")
print(f"Quantized dtype:    {x_q.dtype}")
print(f"Scale:              {scale:.6f}")
print(f"Zero point:         {zp}")
print(f"Max quant error:    {(W - W_deq).abs().max().item():.6f}")

# ── Linear layer comparison ───────────────────────────────────────
linear = nn.Linear(128, 64, bias=False)
linear.weight.data = W

x_in = torch.randn(8, 128)

out_fp32 = linear(x_in)

# Replace weight with dequantized version
linear_q = nn.Linear(128, 64, bias=False)
linear_q.weight.data = W_deq
out_q = linear_q(x_in)

print(f"\\nOutput max diff:    {(out_fp32 - out_q).abs().max().item():.6f}")
print(f"Output relative err:{((out_fp32 - out_q).abs() / out_fp32.abs().clamp(min=1e-8)).mean().item():.4f}")

# ── Memory savings ────────────────────────────────────────────────
fp32_bytes = # YOUR CODE HERE  (W.numel() * 4)
int8_bytes  = # YOUR CODE HERE  (x_q.numel() * 1)

print(f"\\nFP32 size:  {fp32_bytes:,} bytes")
print(f"INT8 size:  {int8_bytes:,} bytes")
print(f"Compression: {fp32_bytes / int8_bytes:.1f}x")
""",
        "expected_output_shape": None,
        "gpu_required": False,
        "colab_link": "",
        "tags": ["tensors", "quantization", "int8", "inference", "advanced"],
        "xp_reward": 30,
        "time_estimate_mins": 45,
        "solutions": [
            {
                "title": "Complete INT8 Quantization Solution",
                "code": """import torch
import torch.nn as nn

def quantize_tensor(x: torch.Tensor, num_bits: int = 8):
    qmin = -(2 ** (num_bits - 1))       # -128
    qmax =  (2 ** (num_bits - 1)) - 1   # 127

    x_min = x.min().item()
    x_max = x.max().item()

    scale = (x_max - x_min) / (qmax - qmin)
    zero_point = round(qmin - x_min / scale)
    zero_point = int(max(qmin, min(qmax, zero_point)))

    x_q = torch.clamp(torch.round(x / scale) + zero_point, qmin, qmax).to(torch.int8)
    return x_q, scale, zero_point

def dequantize_tensor(x_q: torch.Tensor, scale: float, zero_point: int) -> torch.Tensor:
    return scale * (x_q.float() - zero_point)

torch.manual_seed(42)
W = torch.randn(64, 128)
x_q, scale, zp = quantize_tensor(W)
W_deq = dequantize_tensor(x_q, scale, zp)

print(f"Original dtype:     {W.dtype}")
print(f"Quantized dtype:    {x_q.dtype}")
print(f"Scale:              {scale:.6f}")
print(f"Zero point:         {zp}")
print(f"Max quant error:    {(W - W_deq).abs().max().item():.6f}")

linear   = nn.Linear(128, 64, bias=False)
linear.weight.data = W
x_in     = torch.randn(8, 128)
out_fp32 = linear(x_in)

linear_q = nn.Linear(128, 64, bias=False)
linear_q.weight.data = W_deq
out_q    = linear_q(x_in)

print(f"\\nOutput max diff:    {(out_fp32 - out_q).abs().max().item():.6f}")
print(f"Output relative err:{((out_fp32 - out_q).abs() / out_fp32.abs().clamp(min=1e-8)).mean().item():.4f}")

fp32_bytes = W.numel() * 4
int8_bytes  = x_q.numel() * 1
print(f"\\nFP32 size:  {fp32_bytes:,} bytes")
print(f"INT8 size:  {int8_bytes:,} bytes")
print(f"Compression: {fp32_bytes / int8_bytes:.1f}x")
""",
                "explanation": (
                    "Asymmetric quantization allows zero_point != 0, which handles ranges not centered on zero "
                    "(e.g., ReLU outputs which are all positive). The 4× memory compression comes from "
                    "int8 (1 byte) vs float32 (4 bytes). Quantization error of ~0.01 is typical for INT8 "
                    "and acceptable for inference — training requires higher precision."
                ),
                "is_optimal": True,
            }
        ],
        "test_cases": [],
    },
]


# ---------------------------------------------------------------------------
# Seeder
# ---------------------------------------------------------------------------

async def seed_questions_tensors():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Get topic_id for tensors module
        result = await session.execute(
            text("SELECT id FROM topics WHERE slug = 'tensors'")
        )
        row = result.fetchone()
        if not row:
            print("[error] 'tensors' topic not found. Run seeds/topics.py first.")
            return
        topic_id = row[0]

        # Check if already seeded
        result = await session.execute(
            text("SELECT COUNT(*) FROM questions WHERE topic_id = :tid"),
            {"tid": topic_id}
        )
        count = result.scalar()
        if count > 0:
            print(f"[skip] Module 01 already has {count} questions. Skipping.")
            return

        inserted = 0
        for raw in QUESTIONS:
            q = dict(raw)
            solutions = q.pop("solutions", [])
            test_cases = q.pop("test_cases", [])

            result = await session.execute(
                text("""
                    INSERT INTO questions (
                        topic_id, title, slug, difficulty, question_type,
                        problem_statement, constraints, starter_code,
                        expected_output, expected_output_shape,
                        pytorch_version, gpu_required, colab_link,
                        tags, xp_reward, time_estimate_mins,
                        is_published, source
                    ) VALUES (
                        :topic_id, :title, :slug, :difficulty, :question_type,
                        :problem_statement, :constraints, :starter_code,
                        :expected_output, :expected_output_shape,
                        :pytorch_version, :gpu_required, :colab_link,
                        :tags, :xp_reward, :time_estimate_mins,
                        TRUE, 'internal'
                    ) RETURNING id
                """),
                {
                    "topic_id": topic_id,
                    "title": q["title"],
                    "slug": q["slug"],
                    "difficulty": q["difficulty"],
                    "question_type": q["question_type"],
                    "problem_statement": q["problem_statement"],
                    "constraints": q.get("constraints"),
                    "starter_code": q.get("starter_code"),
                    "expected_output": q.get("expected_output"),
                    "expected_output_shape": q.get("expected_output_shape"),
                    "pytorch_version": "2.x",
                    "gpu_required": q.get("gpu_required", False),
                    "colab_link": q.get("colab_link", ""),
                    "tags": q.get("tags", []),
                    "xp_reward": q.get("xp_reward", 10),
                    "time_estimate_mins": q.get("time_estimate_mins", 15),
                }
            )
            question_id = result.scalar()

            for idx, sol in enumerate(solutions):
                await session.execute(
                    text("""
                        INSERT INTO solutions (
                            question_id, title, code, explanation,
                            is_optimal, order_index
                        ) VALUES (
                            :question_id, :title, :code, :explanation,
                            :is_optimal, :order_index
                        )
                    """),
                    {
                        "question_id": question_id,
                        "title": sol["title"],
                        "code": sol["code"],
                        "explanation": sol.get("explanation", ""),
                        "is_optimal": sol.get("is_optimal", False),
                        "order_index": idx + 1,
                    }
                )

            for idx, tc in enumerate(test_cases):
                await session.execute(
                    text("""
                        INSERT INTO test_cases (
                            question_id, input_data, expected_output,
                            is_hidden, order_index
                        ) VALUES (
                            :question_id, :input_data, :expected_output,
                            :is_hidden, :order_index
                        )
                    """),
                    {
                        "question_id": question_id,
                        "input_data": json.dumps(tc["input_data"]),
                        "expected_output": json.dumps(tc["expected_output"]),
                        "is_hidden": tc.get("is_hidden", False),
                        "order_index": idx + 1,
                    }
                )

            inserted += 1

        await session.commit()

        # Update total_questions count on topic
        await session.execute(
            text("UPDATE topics SET total_questions = :count WHERE id = :tid"),
            {"count": inserted, "tid": topic_id}
        )
        await session.commit()

    await engine.dispose()

    print(f"[ok] Seeded {inserted} questions for Module 01 — Tensors & Operations")
    print(f"    Breakdown:")
    basic_count = sum(1 for q in QUESTIONS if q.get("difficulty") == "basic")
    inter_count = sum(1 for q in QUESTIONS if q.get("difficulty") == "intermediate")
    adv_count   = sum(1 for q in QUESTIONS if q.get("difficulty") == "advanced")
    print(f"    Basic:        {basic_count}")
    print(f"    Intermediate: {inter_count}")
    print(f"    Advanced:     {adv_count}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_questions_tensors())
