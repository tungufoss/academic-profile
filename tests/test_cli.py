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
