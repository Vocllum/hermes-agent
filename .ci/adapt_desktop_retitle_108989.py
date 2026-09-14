from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, got {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


source = "apps/desktop/src/app/chat/actions/retitle-session.ts"
replace_once(source, "  const t = translateNow()\n", "")
for key in (
    "regenerateTitleFailed",
    "regeneratingTitle",
    "regenerateTitleSuccess",
):
    replace_once(
        source,
        f"t.sidebar.row.{key}",
        f"translateNow('sidebar.row.{key}')",
    )

# regenerateTitleFailed appears twice in the source; the first loop replaces only
# one occurrence, so update the second explicitly.
replace_once(
    source,
    "t.sidebar.row.regenerateTitleFailed",
    "translateNow('sidebar.row.regenerateTitleFailed')",
)

test = "apps/desktop/src/app/chat/actions/retitle-session.test.ts"
replace_once(
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
