"""Create frontend directory skeleton per CLAUDE.md §4."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "frontend"

DIRS = [
    "app/(auth)/login",
    "app/(auth)/register",
    "app/dashboard",
    "app/modules",
    "app/modules/[slug]",
    "app/modules/[slug]/[questionId]",
    "app/tracker",
    "app/revision",
    "app/import",
    "app/tutor",
    "app/profile",
    "components/editor",
    "components/question",
    "components/tracker",
    "components/tutor",
    "components/ui",
    "lib",
    "store",
]

PAGES = {
    "app/(auth)/login/page.tsx": "// Phase 2: login page\n",
    "app/(auth)/register/page.tsx": "// Phase 2: register page\n",
    "app/dashboard/page.tsx": "// Phase 2: dashboard\n",
    "app/modules/page.tsx": "// Phase 2: module browser\n",
    "app/modules/[slug]/page.tsx": "// Phase 2: module overview\n",
    "app/modules/[slug]/[questionId]/page.tsx": "// Phase 2: exercise page\n",
    "app/tracker/page.tsx": "// Phase 2: daily tracker\n",
    "app/revision/page.tsx": "// Phase 2: revision queue\n",
    "app/import/page.tsx": "// Phase 2: external import\n",
    "app/tutor/page.tsx": "// Phase 2: AI tutor\n",
    "app/profile/page.tsx": "// Phase 2: profile\n",
}

COMPONENTS = [
    "components/editor/CodeEditor.tsx",
    "components/editor/OutputPanel.tsx",
    "components/editor/ShapeValidator.tsx",
    "components/question/QuestionCard.tsx",
    "components/question/SolutionViewer.tsx",
    "components/question/HintDrawer.tsx",
    "components/question/ColabLauncher.tsx",
    "components/question/DifficultyBadge.tsx",
    "components/tracker/StreakCounter.tsx",
    "components/tracker/HeatmapCalendar.tsx",
    "components/tracker/ProgressRing.tsx",
    "components/tracker/WeeklyChart.tsx",
    "components/tutor/ChatInterface.tsx",
    "components/tutor/MessageBubble.tsx",
    "components/tutor/CodeSuggestion.tsx",
    "lib/api.ts",
    "lib/auth.ts",
    "lib/utils.ts",
    "store/useUserStore.ts",
    "store/useProgressStore.ts",
    "store/useTutorStore.ts",
]


def main() -> None:
    for rel in DIRS:
        (ROOT / rel).mkdir(parents=True, exist_ok=True)
    for rel, content in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    for rel in COMPONENTS:
        path = ROOT / rel
        if not path.exists():
            path.write_text("// Phase 2 placeholder\n", encoding="utf-8")
    (ROOT / "components/ui/.gitkeep").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "components/ui/.gitkeep").write_text("", encoding="utf-8")
    print(f"Frontend skeleton at {ROOT}")


if __name__ == "__main__":
    main()
