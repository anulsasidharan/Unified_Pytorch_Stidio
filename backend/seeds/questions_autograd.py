"""
Seed Module 02 — Autograd & Backpropagation (20 exercises).
Usage: python -m seeds.questions_autograd
"""

import asyncio

from seeds.loader import build_exercise, seed_questions_for_topic

TOPIC_SLUG = "autograd"

_SPECS: list[tuple] = [
    ("Enable requires_grad", "requires-grad-flag", "basic", "Create `x = torch.tensor([2.0], requires_grad=True)` and print `x.requires_grad`.", "import torch\nx = # YOUR CODE\nprint(x.requires_grad)", "import torch\nx = torch.tensor([2.0], requires_grad=True)\nprint(x.requires_grad)", ["autograd", "requires_grad"], "code_completion"),
    ("Scalar backward", "scalar-backward", "basic", "Define `y = x ** 2` with `x` requiring grad, call `y.backward()`, print `x.grad`.", "import torch\nx = torch.tensor([3.0], requires_grad=True)\ny = x ** 2\n# backward and print grad", "import torch\nx = torch.tensor([3.0], requires_grad=True)\ny = x ** 2\ny.backward()\nprint(x.grad)", ["autograd", "backward"], "code_completion"),
    ("Vector Jacobian", "vector-jacobian", "basic", "For `y = x * 2` where `x` is length 3, call backward with `gradient=torch.ones_like(y)`.", "import torch\nx = torch.ones(3, requires_grad=True)\ny = x * 2\n# backward with ones_like gradient\nprint(x.grad)", "import torch\nx = torch.ones(3, requires_grad=True)\ny = x * 2\ny.backward(torch.ones_like(y))\nprint(x.grad)", ["autograd", "vector"], "code_completion"),
    ("no_grad context", "no-grad-context", "basic", "Inside `torch.no_grad()`, set `y = x * 2` and verify `y.requires_grad` is False.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\nwith torch.no_grad():\n    y = # YOUR CODE\nprint(y.requires_grad)", "import torch\nx = torch.tensor([1.0], requires_grad=True)\nwith torch.no_grad():\n    y = x * 2\nprint(y.requires_grad)", ["autograd", "no_grad"], "code_completion"),
    ("detach tensor", "detach-tensor", "basic", "Detach `x` to `z`, add 1 to `z`, backward on `y = x*2`; `x.grad` should be 2.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\ny = x * 2\nz = # detach here\nz += 1\ny.backward()\nprint(x.grad)", "import torch\nx = torch.tensor([1.0], requires_grad=True)\ny = x * 2\nz = x.detach()\nz += 1\ny.backward()\nprint(x.grad)", ["autograd", "detach"], "code_completion"),
    ("grad accumulation", "grad-accumulation", "basic", "Call `backward()` twice on the same leaf without zeroing; show grads add.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\nfor _ in range(2):\n    (x * 2).backward(retain_graph=True)\nprint(x.grad)", "import torch\nx = torch.tensor([1.0], requires_grad=True)\nfor _ in range(2):\n    (x * 2).backward(retain_graph=True)\nprint(x.grad)", ["autograd", "accumulation"], "code_completion"),
    ("zero_grad pattern", "zero-grad-pattern", "basic", "Backward once, zero grad, backward again; print grad after each step.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\n(x*3).backward()\nprint('first', x.grad)\n# zero and second backward", "import torch\nx = torch.tensor([1.0], requires_grad=True)\n(x*3).backward()\nprint('first', x.grad)\nx.grad.zero_()\n(x*3).backward()\nprint('second', x.grad)", ["autograd", "optimizer-prep"], "code_completion"),
    ("grad_fn chain", "grad-fn-chain", "intermediate", "Build `y = (x.sin()).mean()` and print `y.grad_fn`.", "import torch\nx = torch.randn(4, requires_grad=True)\ny = x.sin().mean()\nprint(y.grad_fn)", "import torch\nx = torch.randn(4, requires_grad=True)\ny = x.sin().mean()\nprint(y.grad_fn)", ["autograd", "graph"], "code_completion"),
    ("Freeze parameters", "freeze-parameters", "intermediate", "Freeze all params on `nn.Linear(2,2)`; backward should leave grads None.", "import torch\nfrom torch import nn\nm = nn.Linear(2, 2)\n# freeze all params\nx = torch.randn(1, 2)\nloss = m(x).sum()\nloss.backward()\nprint(any(p.grad is not None for p in m.parameters()))", "import torch\nfrom torch import nn\nm = nn.Linear(2, 2)\nfor p in m.parameters():\n    p.requires_grad = False\nx = torch.randn(1, 2)\nloss = m(x).sum()\nloss.backward()\nprint(any(p.grad is not None for p in m.parameters()))", ["autograd", "nn"], "code_completion"),
    ("Gradient clipping", "clip-grad-norm", "intermediate", "Apply `clip_grad_norm_` with max norm 1.0 after backward.", "import torch\nfrom torch import nn\nm = nn.Linear(10, 1)\nx = torch.randn(4, 10)\nloss = m(x).sum()\nloss.backward()\n# clip here\nprint('clipped')", "import torch\nfrom torch import nn\nm = nn.Linear(10, 1)\nx = torch.randn(4, 10)\nloss = m(x).sum()\nloss.backward()\ntorch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)\nprint('clipped')", ["autograd", "clipping"], "code_completion"),
    ("Higher-order grad", "higher-order-grad", "intermediate", "Second derivative of `y = x**3` at `x=2` with `create_graph=True`.", "import torch\nx = torch.tensor([2.0], requires_grad=True)\ny = x ** 3\ndy = torch.autograd.grad(y, x, create_graph=True)[0]\nd2y = torch.autograd.grad(dy, x)[0]\nprint(d2y)", "import torch\nx = torch.tensor([2.0], requires_grad=True)\ny = x ** 3\ndy = torch.autograd.grad(y, x, create_graph=True)[0]\nd2y = torch.autograd.grad(dy, x)[0]\nprint(d2y)", ["autograd", "higher-order"], "code_completion"),
    ("Custom autograd Function", "custom-autograd-fn", "intermediate", "Implement `DoubleFn` with forward/backward doubling values.", "import torch\nclass DoubleFn(torch.autograd.Function):\n    @staticmethod\n    def forward(ctx, inp):\n        pass\n    @staticmethod\n    def backward(ctx, grad_out):\n        pass\nx = torch.tensor([2.0], requires_grad=True)\ny = DoubleFn.apply(x)\ny.backward()\nprint(x.grad)", "import torch\nclass DoubleFn(torch.autograd.Function):\n    @staticmethod\n    def forward(ctx, inp):\n        ctx.save_for_backward(inp)\n        return inp * 2\n    @staticmethod\n    def backward(ctx, grad_out):\n        return grad_out * 2\nx = torch.tensor([2.0], requires_grad=True)\ny = DoubleFn.apply(x)\ny.backward()\nprint(x.grad)", ["autograd", "custom"], "code_completion"),
    ("Stop gradient via detach", "stop-gradient-detach", "intermediate", "Branch with detach; only non-detached path updates `x`.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\na = x * 2\nb = a.detach() * 3\n(a + b).backward()\nprint(x.grad)", "import torch\nx = torch.tensor([1.0], requires_grad=True)\na = x * 2\nb = a.detach() * 3\n(a + b).backward()\nprint(x.grad)", ["autograd", "detach"], "code_completion"),
    ("Safe in-place pattern", "inplace-on-leaf", "intermediate", "Clone leaf before in-place add, then backward.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\nx_safe = x.clone()\nx_safe += 1\ny = x_safe * 2\ny.backward()\nprint(x.grad)", "import torch\nx = torch.tensor([1.0], requires_grad=True)\nx_safe = x.clone()\nx_safe += 1\ny = x_safe * 2\ny.backward()\nprint(x.grad)", ["autograd", "inplace"], "code_completion"),
    ("Register backward hook", "backward-hook", "advanced", "Register hook printing grad norm on `x`.", "import torch\nx = torch.tensor([1.0, 2.0], requires_grad=True)\n# register hook\n(x**2).sum().backward()", "import torch\nx = torch.tensor([1.0, 2.0], requires_grad=True)\ndef hook(grad):\n    print(float(grad.norm()))\n    return grad\nx.register_hook(hook)\n(x**2).sum().backward()", ["autograd", "hooks"], "code_completion"),
    ("Gradient checkpoint", "grad-checkpoint-concept", "advanced", "Use `checkpoint` on `relu` forward; print output shape.", "import torch\nfrom torch.utils.checkpoint import checkpoint\ndef f(inp):\n    return inp.relu()\nx = torch.randn(4, requires_grad=True)\ny = checkpoint(f, x)\nprint(y.shape)", "import torch\nfrom torch.utils.checkpoint import checkpoint\ndef f(inp):\n    return inp.relu()\nx = torch.randn(4, requires_grad=True)\ny = checkpoint(f, x)\nprint(y.shape)", ["autograd", "checkpoint"], "code_completion"),
    ("float64 gradients", "mixed-dtype-grad", "advanced", "Verify `.grad` dtype matches float64 parameter.", "import torch\nfrom torch import nn\nm = nn.Linear(2, 1, dtype=torch.float64)\nx = torch.randn(3, 2, dtype=torch.float64)\nloss = m(x).sum()\nloss.backward()\nprint(m.weight.grad.dtype)", "import torch\nfrom torch import nn\nm = nn.Linear(2, 1, dtype=torch.float64)\nx = torch.randn(3, 2, dtype=torch.float64)\nloss = m(x).sum()\nloss.backward()\nprint(m.weight.grad.dtype)", ["autograd", "dtype"], "code_completion"),
    ("Detect anomaly mode", "detect-anomaly", "advanced", "Enable anomaly detection and run valid backward.", "import torch\ntorch.autograd.set_detect_anomaly(True)\nx = torch.tensor([1.0], requires_grad=True)\n(x*2).backward()\nprint('ok')", "import torch\ntorch.autograd.set_detect_anomaly(True)\nx = torch.tensor([1.0], requires_grad=True)\n(x*2).backward()\nprint('ok')", ["autograd", "debug"], "code_completion"),
    ("Jacobian helper", "jacobian-functional", "advanced", "Compute Jacobian of `f(x)=x**2` at scalar input.", "import torch\nfrom torch.autograd.functional import jacobian\ndef f(inp):\n    return inp ** 2\nx = torch.tensor([2.0])\nprint(jacobian(f, x))", "import torch\nfrom torch.autograd.functional import jacobian\ndef f(inp):\n    return inp ** 2\nx = torch.tensor([2.0])\nprint(jacobian(f, x))", ["autograd", "jacobian"], "code_completion"),
    ("Computation graph check", "conceptual-graph-mcq", "basic", "Print whether `y=x*2` keeps `requires_grad` when `x` is a leaf with grad enabled.", "import torch\nx = torch.tensor([1.0], requires_grad=True)\ny = x * 2\nprint('graph' if y.requires_grad else 'no-graph')", "import torch\nx = torch.tensor([1.0], requires_grad=True)\ny = x * 2\nprint('graph' if y.requires_grad else 'no-graph')", ["autograd", "concept"], "conceptual_mcq"),
]

QUESTIONS = [
    build_exercise(
        title=title,
        slug=slug,
        difficulty=diff,
        task=task,
        starter_code=starter,
        solution_code=solution,
        tags=tags,
        question_type=qtype,
    )
    for title, slug, diff, task, starter, solution, tags, qtype in _SPECS
]


async def main() -> None:
    await seed_questions_for_topic(TOPIC_SLUG, QUESTIONS, "Module 02 — Autograd")


if __name__ == "__main__":
    asyncio.run(main())
