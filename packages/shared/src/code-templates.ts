import type { CodeLanguage } from './types/enums.js';

/** Starter code templates keyed by question slug */
export const QUESTION_CODE_TEMPLATES: Record<
  string,
  Partial<Record<CodeLanguage, string>>
> = {
  'two-sum': {
    python: `def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []

if __name__ == "__main__":
    import sys
    lines = sys.stdin.read().strip().split("\\n")
    n = int(lines[0])
    nums = list(map(int, lines[1].split()))
    target = int(lines[2])
    result = two_sum(nums, target)
    print(*result)`,
    javascript: `function twoSum(nums, target) {
  // Write your solution here
}

const fs = require('fs');
const lines = fs.readFileSync(0, 'utf8').trim().split('\\n');
const n = parseInt(lines[0], 10);
const nums = lines[1].split(' ').map(Number);
const target = parseInt(lines[2], 10);
const result = twoSum(nums, target);
console.log(result.join(' '));`,
  },
  'valid-palindrome': {
    python: `def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

if __name__ == "__main__":
    import sys
    s = sys.stdin.read().strip()
    print(str(is_palindrome(s)).lower())`,
    javascript: `function isPalindrome(s) {
  // Write your solution here
}

const fs = require('fs');
const s = fs.readFileSync(0, 'utf8').trim();
console.log(String(isPalindrome(s)).toLowerCase());`,
  },
};

export function getStarterCode(slug: string, language: CodeLanguage): string {
  const templates = QUESTION_CODE_TEMPLATES[slug];
  if (templates?.[language]) {
    return templates[language]!;
  }

  if (language === 'python') {
    return `# Read from stdin and write to stdout for: ${slug}
import sys

def solve():
    data = sys.stdin.read().strip()
    # TODO: implement
    print(data)

if __name__ == "__main__":
    solve()`;
  }

  return `// Read from stdin and write to stdout for: ${slug}
const fs = require('fs');

function solve() {
  const data = fs.readFileSync(0, 'utf8').trim();
  // TODO: implement
  console.log(data);
}

solve();`;
}
