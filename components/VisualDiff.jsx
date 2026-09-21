"use client";

/**
 * VisualDiff — renders a token/word-level diff between SI and Draft BL values.
 *
 * Supports three display modes:
 * - "si": renders SI text, highlighting words removed or altered in Draft BL in red/strikethrough
 * - "bl": renders Draft BL text, highlighting words added or altered from SI in green
 * - "inline": renders unified inline diff with both deletions and additions
 */

export default function VisualDiff({ siValue, blValue, mode = "inline" }) {
  if (siValue == null && blValue == null) {
    return <span style={{ color: "var(--text-light)", fontStyle: "italic" }}>n/a</span>;
  }

  const siStr = String(siValue ?? "");
  const blStr = String(blValue ?? "");

  if (siStr === blStr) {
    return <span>{siStr}</span>;
  }

  const siWords = tokenize(siStr);
  const blWords = tokenize(blStr);

  const diff = computeWordDiff(siWords, blWords);

  return (
    <span style={{ lineHeight: 1.7 }}>
      {diff.map((part, i) => {
        if (part.type === "equal") {
          return <span key={i}>{part.value} </span>;
        }

        if (mode === "si") {
          if (part.type === "delete") {
            return (
              <span key={i} className="diff-del" title="Value in SI missing or altered in Draft BL">
                {part.value}
              </span>
            );
          }
          return null; // Don't show BL-only insertions in the SI column
        }

        if (mode === "bl") {
          if (part.type === "insert") {
            return (
              <span key={i} className="diff-add" title="Value in Draft BL not matching original SI">
                {part.value}
              </span>
            );
          }
          return null; // Don't show SI-only deletions in the BL column
        }

        // Default: unified inline diff
        if (part.type === "delete") {
          return (
            <span key={i} className="diff-del">
              {part.value}
            </span>
          );
        }
        if (part.type === "insert") {
          return (
            <span key={i} className="diff-add">
              {part.value}
            </span>
          );
        }
        return null;
      })}
    </span>
  );
}

function tokenize(str) {
  return str.split(/(\s+)/).filter((t) => t.trim().length > 0);
}

/**
 * Word-level Longest Common Subsequence diff.
 * Optimized for field values (typically < 40 words).
 */
function computeWordDiff(oldWords, newWords) {
  const m = oldWords.length;
  const n = newWords.length;

  // Build LCS matrix
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (oldWords[i - 1].toLowerCase() === newWords[j - 1].toLowerCase()) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtrack to assemble diff tokens
  const result = [];
  let i = m;
  let j = n;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && oldWords[i - 1].toLowerCase() === newWords[j - 1].toLowerCase()) {
      result.unshift({ type: "equal", value: newWords[j - 1] });
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      result.unshift({ type: "insert", value: newWords[j - 1] });
      j--;
    } else {
      result.unshift({ type: "delete", value: oldWords[i - 1] });
      i--;
    }
  }

  return result;
}
