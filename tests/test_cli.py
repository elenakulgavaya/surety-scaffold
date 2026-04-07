import json
from io import StringIO
from unittest.mock import MagicMock, patch

from surety.scaffold.cli import _copy_to_clipboard, main


SIMPLE_JSON = json.dumps({'name': 'Alice'})
SIMPLE_OUTPUT = (
    "from surety import Dictionary, String\n\n\n"
    "class Schema(Dictionary):\n"
    "    Name = String(name='name', required=True)"
)


def test_returns_true_when_pbcopy_succeeds():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        assert _copy_to_clipboard('text') is True


def test_tries_xclip_when_pbcopy_missing():
    def side_effect(cmd, **_):
        if cmd[0] == 'pbcopy':
            raise FileNotFoundError
        return MagicMock(returncode=0)

    with patch('subprocess.run', side_effect=side_effect) as mock_run:
        assert _copy_to_clipboard('text') is True
        assert mock_run.call_args_list[1][0][0][0] == 'xclip'


def test_tries_xdotool_when_pbcopy_and_xclip_missing():
    def side_effect(cmd, **_):
        if cmd[0] in ('pbcopy', 'xclip'):
            raise FileNotFoundError
        return MagicMock(returncode=0)

    with patch('subprocess.run', side_effect=side_effect) as mock_run:
        assert _copy_to_clipboard('text') is True
        assert mock_run.call_args_list[2][0][0][0] == 'xdotool'


def test_returns_false_when_all_commands_missing():
    with patch('subprocess.run', side_effect=FileNotFoundError):
        assert _copy_to_clipboard('text') is False


def _run(argv, stdin=None):
    """Invoke main() with controlled argv and stdin, capture stdout/stderr."""
    with patch('sys.argv', ['surety-scaffold'] + argv):
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            with patch('sys.stderr', new_callable=StringIO) as mock_err:
                if stdin is not None:
                    with patch('sys.stdin', StringIO(stdin)):
                        try:
                            main()
                        except SystemExit as e:
                            return mock_out.getvalue(), mock_err.getvalue(), e.code
                else:
                    try:
                        main()
                    except SystemExit as e:
                        return mock_out.getvalue(), mock_err.getvalue(), e.code
                return mock_out.getvalue(), mock_err.getvalue(), 0


def test_json_argument_produces_output():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=True):
        stdout, _, code = _run([SIMPLE_JSON, '--no-clipboard'])
    assert code == 0
    assert SIMPLE_OUTPUT in stdout


def test_reads_from_stdin_when_no_argument():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=True):
        stdout, _, code = _run([], stdin=SIMPLE_JSON)
    assert code == 0
    assert SIMPLE_OUTPUT in stdout


def test_class_name_long_flag():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=True):
        stdout, _, code = _run(
            [SIMPLE_JSON, '--class-name', 'User', '--no-clipboard']
        )
    assert code == 0
    assert 'class User(Dictionary):' in stdout


def test_class_name_short_flag():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=True):
        stdout, _, code = _run(
            [SIMPLE_JSON, '-c', 'User', '--no-clipboard']
        )
    assert code == 0
    assert 'class User(Dictionary):' in stdout


def test_default_class_name_is_schema():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=True):
        stdout, _, code = _run([SIMPLE_JSON, '--no-clipboard'])

    assert code == 0
    assert 'class Schema(Dictionary):' in stdout


def test_invalid_json_exits_with_error():
    _, stderr, code = _run(['not valid json'])
    assert code == 1
    assert 'Error: invalid JSON' in stderr


def test_copies_to_clipboard_by_default():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=True) as mock_copy:
        _, stderr, _ = _run([SIMPLE_JSON])

    mock_copy.assert_called_once_with(SIMPLE_OUTPUT)
    assert 'Copied to clipboard' in stderr


def test_no_clipboard_flag_skips_copy():
    with patch('surety.scaffold.cli._copy_to_clipboard') as mock_copy:
        _run([SIMPLE_JSON, '--no-clipboard'])

    mock_copy.assert_not_called()

def test_clipboard_failure_prints_message():
    with patch('surety.scaffold.cli._copy_to_clipboard', return_value=False):
        _, stderr, code = _run([SIMPLE_JSON])
    assert code == 0
    assert 'Could not copy to clipboard' in stderr
