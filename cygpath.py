import subprocess
import os
from typing import Literal, Optional, Union
import sys

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

StrPath: TypeAlias = Union[os.PathLike[str], str]

OutputType: TypeAlias = Literal['dos', 'mixed', 'unix', 'windows']


def pathconv(path: str,
             output_type: OutputType,
             absolute: bool = False,
             long: Optional[bool] = None,
             proc: bool = False,
             ) -> str:
    args = ['cygpath', '--type', output_type]

    if absolute:
        args.append('--absolute')

    if long is True:
        args.append('--long')
    elif long is False:
        args.append('--short-name')

    if proc:
        args.append('--proc-cygdrive')

    args.append(path)

    p = subprocess.run(args,
                       capture_output=True,
                       check=True,
                       text=True,
                       )
    return p.stdout.rstrip('\n')
