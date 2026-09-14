from tui_gateway import server


def _session(sid: str, cwd: str) -> dict:
    return {
        "id": sid,
        "cwd": cwd,
        "git_branch": "main",
        "git_repo_root": "",
        "started_at": 1,
        "last_active": 1,
    }


def test_configured_default_root_folds_into_pathless_home_but_nested_repo_stays_auto(
    monkeypatch, tmp_path
):
    configured = tmp_path / "Hermes"
    nested = configured / "nested"
    configured.mkdir()
    nested.mkdir()

    sessions = [_session("home-session", str(configured)), _session("nested-session", str(nested))]
    discovered = [
        {"root": str(configured), "label": "Hermes", "sessions": 1, "last_active": 1},
        {"root": str(nested), "label": "nested", "sessions": 1, "last_active": 1},
    ]

    def resolve(cwd: str):
        if cwd == str(configured):
            return {"repo_root": str(configured), "worktree_root": str(configured)}
        if cwd == str(nested):
            return {"repo_root": str(nested), "worktree_root": str(nested)}
        return None

    monkeypatch.setattr(server, "_profile_configured_cwd", lambda _home: str(configured))
    monkeypatch.setattr(
        server,
        "_project_tree_inputs",
        lambda _db, _limit, *, include_discovered: (sessions, [], discovered, None),
    )
    monkeypatch.setattr(server.git_probe, "warm_roots", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(server.git_probe, "resolve", resolve)

    tree, _active = server._build_project_tree(
        object(), preview_limit=3, hydrate=True, session_limit=10, include_discovered=True
    )

    by_id = {project["id"]: project for project in tree["projects"]}
    home = by_id["__no_project__"]

    assert str(configured) not in by_id
    assert home["path"] is None
    assert home["isNoProject"] is True
    assert {
        session["id"]
        for repo in home["repos"]
        for group in repo["groups"]
        for session in group["sessions"]
    } == {"home-session"}

    nested_project = by_id[str(nested)]
    assert nested_project["isAuto"] is True
    assert nested_project["label"] == "nested"
