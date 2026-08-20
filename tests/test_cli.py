import json

from academic_profile.cli import main


def test_default_command_prints_help(capsys):
    assert main([]) == 0

    captured = capsys.readouterr()

    assert "Public-safe academic profile data helpers." in captured.out


def test_doctor_outputs_status(capsys):
    assert main(["doctor"]) == 0

    captured = capsys.readouterr()

    assert '"package": "academic-profile"' in captured.out
    assert '"status": "ok"' in captured.out


def test_schemes_lists_bundled_schemes(capsys):
    assert main(["schemes"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert [scheme["plugin"] for scheme in payload] == ["icelandic-universities"]
    assert payload[0]["id"] == "matskerfi-opinberra-haskola"
    assert payload[0]["entries"] > 0


def test_schemes_can_print_review_notes(capsys):
    assert main(["schemes", "icelandic-universities", "--review-notes"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert payload[0]["review_notes"]
    assert any(entry["code"] == "A10.5" for entry in payload[0]["entry_review_notes"])


def test_schemes_rejects_unknown_scheme(capsys):
    assert main(["schemes", "nope"]) == 1

    payload = json.loads(capsys.readouterr().out)

    assert payload["status"] == "invalid"
    assert "unknown reporting scheme" in payload["error"]
