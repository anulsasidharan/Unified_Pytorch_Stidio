import Link from "next/link";

export default function ProfilePage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Profile</h1>
      <p className="text-[var(--text-muted)]">
        Account preferences and editor settings live on the{" "}
        <Link href="/settings" className="text-[var(--python-blue)] hover:opacity-80">
          Settings
        </Link>{" "}
        page.
      </p>
    </div>
  );
}
