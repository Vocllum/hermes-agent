from pathlib import Path


def replace_exact(path: str, old: str, new: str, expected: int = 1) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{path}: expected {expected} matches, got {count}")
    p.write_text(text.replace(old, new), encoding="utf-8")


source = "apps/desktop/src/app/chat/actions/retitle-session.ts"
replace_exact(source, "  const t = translateNow()\n", "")
replace_exact(
    source,
    "t.sidebar.row.regenerateTitleFailed",
    "translateNow('sidebar.row.regenerateTitleFailed')",
    expected=2,
)
replace_exact(
    source,
    "t.sidebar.row.regeneratingTitle",
    "translateNow('sidebar.row.regeneratingTitle')",
)
replace_exact(
    source,
    "t.sidebar.row.regenerateTitleSuccess",
    "translateNow('sidebar.row.regenerateTitleSuccess')",
)

test = "apps/desktop/src/app/chat/actions/retitle-session.test.ts"
replace_exact(
    test,
    '''vi.mock('@/i18n', () => ({
  translateNow: () => ({
    sidebar: {
      row: {
        regenerateTitleFailed: 'Could not regenerate session title',
        regenerateTitleSuccess: 'Session title regenerated',
        regeneratingTitle: 'Regenerating session title...'
      }
    }
  })
}))
''',
    '''vi.mock('@/i18n', () => ({
  translateNow: (key: string) => ({
    'sidebar.row.regenerateTitleFailed': 'Could not regenerate session title',
    'sidebar.row.regenerateTitleSuccess': 'Session title regenerated',
    'sidebar.row.regeneratingTitle': 'Regenerating session title...'
  })[key] ?? key
}))
''',
)
